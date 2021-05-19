#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Andrew Corum
#
# Based on skeleton code provided in CSCI B551, Fall 2020.


import sys
import json

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col,'S'), (row-1,col,'N'), (row,col-1,'W'), (row,col+1,'E'))

	# Return only moves that are within the board and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@") ]

# Perform search on the map
def search1(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]

        # fringe: ("p" location, distance from start, compass moves from start)
        fringe=[(pichu_loc,0,'')]
        # visited: keep track of which states have been previously visited
        visited={pichu_loc:True}

        while fringe:
            (curr_move, curr_dist, curr_string)=fringe.pop(0)
            for (move_y, move_x, string) in moves(house_map, *curr_move):
                move = (move_y,move_x)
                if move in visited:
                   continue
                else:
                    visited[move] = True
                if house_map[move[0]][move[1]]=="@":
                        return curr_dist+1, curr_string+string
                else:
                        fringe.append((move, curr_dist + 1, curr_string+string))

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search1(house_map)
        print("Here's the solution I found:")
        if solution:
            print("{0} {1}".format(solution[0], solution[1]))
        else:
            print("Inf")
