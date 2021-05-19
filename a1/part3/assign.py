#!/usr/local/bin/python3

# Written by Andrew Corum
# For B551 Fall 2020
# No outside code was used (other than what can be found at https://docs.python.org)

import sys
from itertools import combinations
import heapq
import copy
import random

# Parse the input file for list of students and preferences
# Returns a dictionary
# Key: (string) Student name
# Value: (list) [ [pref teammates], [ppl to avoid] ]
def parse_input(filename):
    students = {}
    with open(filename, "r") as f:
        for line in f.read().strip("\n").split("\n"):
            prefs = line.split(" ")
            students[prefs[0]] = [prefs[1].split("-")]
            if prefs[2] == "_":
                students[prefs[0]].append([])
            else:
                students[prefs[0]].append(prefs[2].split(","))
    return students

# Print a state in the desired format
# A state is a list of groups. Each group is a list of names.
def print_state(state):
    for group in state:
        print(*group, sep='-')
    print(evaluate(state))

# Calculate the cost of particuar grouping of students
def evaluate(state):
    # Cost per team (grading)
    cost = k * len(state)
    for group in state:
        for student in group:
            # Cost for wrong # of ppl in group
            cost += 1 if len(group) != len(students[student][0]) else 0
            # Cost if group missing a preffered teammate
            for requested in students[student][0]:
                if requested == student or requested == "zzz" or requested == "xxx":
                    continue
                cost += n if requested not in group else 0
            # Cost if group containing bad teammate
            for avoid in students[student][1]:
                cost += m if avoid in group else 0
    return cost

# Calculate the change in cost when combining group0 and group1
def evalUpdate(group0, group1):
    return evaluate([group0 + group1]) - evaluate([group0]) - evaluate([group1])

# Get list of possible teams when combining 2 groups (with maxgroup size = 3)
# Also calculate the cost of the new states
def successors(cost, state):
    succ = []
    # Combine two groups
    combs = combinations(state, 2)
    for c in combs:
        # Don't combine if too large
        if len(c[0] + c[1]) > maxGroupSize:
            continue
        stateCopy = copy.deepcopy(state)
        stateCopy.remove(c[0])
        stateCopy.remove(c[1])
        stateCopy += [c[0] + c[1]]
        succ.append((cost+evalUpdate(c[0], c[1]), stateCopy))
        del stateCopy
    return succ

# Best first search to find best grouping, outputing results as they are discovered
# Fringe size is limited to help speed up large problems
# (although optimal solution not always found)
def search(state):
    minCost = float('inf')
    while True:
        # Shuffle students at beginning to avoid bias
        random.shuffle(state[1])
        fringe = [state]
        i = 0
        while len(fringe) > 0 and i < maxFringe*len(names):
            i+=1
            cost, currState = heapq.heappop(fringe)
            if cost < minCost:
                minCost = cost
                print_state(currState)
            # Get successors
            temp = successors(cost, currState)
            for sCost, s in temp:
                heapq.heappush(fringe, (sCost, s))
            if len(fringe) >= maxFringe:
                fringe = heapq.nsmallest(maxFringe, fringe)

if __name__ == "__main__":
    # Get args
    if len(sys.argv) != 5:
        sys.exit("./assign.py [input-file] [k] [m] [n]")
    k = int(sys.argv[2])
    m = int(sys.argv[3])
    n = int(sys.argv[4])
    random.seed(42)

    students = parse_input(sys.argv[1])
    numStud = len(students)
    names = [*students]
    maxGroupSize = 3
    maxFringe = 1000

    # Begin search, starting with all students in a solo group
    start = [[i] for i in names]
    search((evaluate(start), start))
