#!/usr/local/bin/python3
# CSCI B551 Fall 2020
#
# Authors: Andrew Corum (amcorum)
#
# based on skeleton code by D. Crandall, 11/2020
#
# ./break_code.py : attack encryption
#


import random
import math
import copy 
import sys
import encode
import re
import time
import json
from os import path

TIME_LIMIT = 360
TRANS_LL_FILE = "./transLL.json"
transLL = {}
letters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

# For each pair of letters, calculate the log-likelihood that they appear in
# the English language. Store in dictionary "transLL".
# Assumes corpus is already filled with english words
# Then save transLL to file for future use
def create_trans_ll():
    for a in letters:
        for b in letters:
            numAX = len(re.findall(rf"{a}(?=.)", corpus))
            numAB = len(re.findall(rf"{a}(?={b})", corpus))
            transLL[a+b] = float('-30') if numAB == 0 else math.log(numAB) - math.log(numAX)
    # Save transLL to file for future use
    j = json.dumps(transLL)
    f = open(TRANS_LL_FILE, 'w')
    f.write(j)
    f.close()

# Determine log likelihood that the string contains english text
def eng_ll(string):
    engLL = 0
    for i in range(0, len(string)-1):
        ll = transLL[string[i]+string[i+1]]
        if ll == float('-inf'): return float('-inf')
        engLL += ll 
    return engLL

# Decode s given replace_table and rearrange_table
def decode(s, replace_table, rearrange_table):
    # Invert replacement table
    inv_replace = {val: key for key, val in replace_table.items()}
    # Invert rearrangement table
    inv_rearrange = [rearrange_table.index(i) for i in range(len(rearrange_table))]
    return encode.encode(s, inv_replace, inv_rearrange)

# Create a random replace_table and rearrange_table
# (based on code provided in `apply_code.py`)
def rand_tables():
    letters = list(range(ord('a'), ord('z')+1))
    random.shuffle(letters)
    replace_table = dict(zip(map(chr, range(ord('a'), ord('z')+1)), map(chr, letters)))
    rearrange_table = list(range(0, 4))
    random.shuffle(rearrange_table)
    return replace_table, rearrange_table

# Create new encoding tables by performing one random swap
def new_tables(T):
    repT, arrT = T[0].copy(), T[1].copy()
    n1 = random.randint(0, 29)
    # Swap in rearrange_table
    if n1 < 4:
        n2 = random.choice(list(range(n1)) + list(range(n1+1, 4)))
        arrT[n1], arrT[n2] = arrT[n2], arrT[n1]
    # Swap in replace_table
    else:
        n1 -= 4
        n2 = random.choice(list(range(n1)) + list(range(n1+1, 26)))
        n1 = chr(n1 + 97)
        n2 = chr(n2 + 97)
        repT[n1], repT[n2] = repT[n2], repT[n1]
    return repT, arrT

# Perform Metropolis-Hastings walk, maximizing eng_ll(plaintext)
def metro_hastings(ciphertext, maxIter=10000):
    T0 = rand_tables()
    if len(ciphertext) > 2500:
        ciphertext = ciphertext[:2500]
    print(eng_ll(decode(ciphertext, T0[0], T0[1])))
    prob0 = eng_ll(decode(ciphertext, T0[0], T0[1]))
    i = 0
    while i < maxIter:
        if i%1000 == 0: print("i =", i, "p =", prob0)
        T1 = new_tables(T0)
        prob1 = eng_ll(decode(ciphertext, T1[0], T1[1]))
        if prob1 > prob0:
            T0, prob0 = T1, prob1
        elif random.random() < math.exp(prob1-prob0):
            T0, prob0 = T1, prob1
        i += 1
    print(eng_ll(decode(ciphertext, T0[0], T0[1])))
    return T0[0], T0[1]

# Given ciphertext c, attempt to decrypt and return plaintext
def break_code(ciphertext):
    # Get transLL probabilities from file, or calculate
    if path.exists(TRANS_LL_FILE):
        print("Getting log-likelihood eng letter transition probabilities from file...")
        f = open(TRANS_LL_FILE, 'r')
        global transLL
        transLL = json.loads(f.read())
        f.close()
    else:
        print("Calculating log-likelihood eng letter transition probabilities...")
        create_trans_ll()

    print("Performing Metropolis-Hastings search for ciphertext decoding...")
    best_T = None
    best_prob = float('-inf')
    # Repeatedly perform metro-hastings until timeout
    # Return the best decoding (one with highest probability)
    while time.perf_counter() - START_TIME < TIME_LIMIT:
        print("Time:", time.perf_counter() - START_TIME)
        T = metro_hastings(ciphertext)
        prob = eng_ll(decode(ciphertext, T[0], T[1]))
        if prob > best_prob:
            best_T, best_prob = T, prob
    print("Best prob:", best_prob)
    return decode(ciphertext, best_T[0], best_T[1])

if __name__== "__main__":
    if(len(sys.argv) != 4):
        raise Exception("usage: ./break_code.py coded-file corpus output-file")

    START_TIME = time.perf_counter()
    encoded = encode.read_clean_file(sys.argv[1])
    corpus = encode.read_clean_file(sys.argv[2])
    decoded = break_code(encoded)

    with open(sys.argv[3], "w") as file:
        print(decoded, file=file)

