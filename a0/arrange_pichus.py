#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Andrew Corum
#
# Based on skeleton code in CSCI B551, Fall 2020
#


import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Count total # of pichus on board
def count_pichus(board):
    return sum([ row.count('p') for row in board ] )

# Return a string with the board rendered in a human-pichuly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Given a range of columns, check if pichu is found before an obstruction
def check_cols(board, row, cols):
    for c in cols:
        obj = board[row][c]
        if obj == 'p' :
            return False
        elif obj == 'X' or obj == '@':
            break
    return True

# Given a range of rows, check if pichu is found before an obstruction
def check_rows(board, rows, col):
    for r in rows:
        obj = board[r][col]
        if obj == 'p':
            return False
        elif obj == 'X' or obj == '@':
            break
    return True

# Check places diagonal of given (row,col) to see if pichu is found before an obstruction
def check_diags(board, row, col):
    # Check positive diag "/"
    r,c = row, col
    height, width = len(board), len(board[0])
    while r > 0 and c < width-1:
        r -= 1
        c += 1
        obj = board[r][c]
        if obj == 'p':
            return False
        elif obj == 'X' or obj == '@':
            break
    r,c = row, col
    while r < height-1 and c > 0:
        r += 1
        c -= 1
        obj = board[r][c]
        if obj == 'p':
            return False
        elif obj == 'X' or obj == '@':
            break
    
    # Check negative diag "\"
    r,c = row, col
    while r > 0 and c > 0:
        r -= 1
        c -= 1
        obj = board[r][c]
        if obj == 'p':
            return False
        elif obj == 'X' or obj == '@':
            break
    r,c = row, col
    while r < height-1 and c < width-1:
        r += 1
        c += 1
        obj = board[r][c]
        if obj == 'p':
            return False
        elif obj == 'X' or obj == '@':
            break

    return True

# Returns true iff the given position is a legal location for a pichu
# Assumes that board[row][col] == '.'
def legal_state(board, row, col):
    return check_rows(board, reversed(range(row)), col) and check_rows(board, range(row,len(board)), col) and check_cols(board, row, reversed(range(col))) and check_cols(board, row, range(col,len(board[0])))

# (EC) Returns true iff the given position is a legal location for a pichu
# Assumes that board[row][col] == '.'
def legal_state_EC(board, row, col):
    return check_rows(board, reversed(range(row)), col) and check_rows(board, range(row,len(board)), col) and check_cols(board, row, reversed(range(col))) and check_cols(board, row, range(col,len(board[0]))) and check_diags(board, row, col)

# Add a pichu to the board at the given position, and appends tuple to list of successors:
# (newBoard, rowWherePichuAdded)
def add_pichu(succ, board, row, col):
    if legal_state(board, row, col):
        succ.append((board[0:row] + [board[row][0:col] + ['p',] + board[row][col+1:]] + board[row+1:], row))

# (EC) Add a pichu to the board at the given position, and appends tuple to list of successors:
# (newBoard, rowWherePichuAdded)
def add_pichu_EC(succ, board, row, col):
    if legal_state_EC(board, row, col):
        succ.append((board[0:row] + [board[row][0:col] + ['p',] + board[row][col+1:]] + board[row+1:], row))

# Get list of successors of given board state and the row to which a pichu was last added
def successors(board, lastRow):
    succ = []
    for r in range(lastRow, len(board)):
        for c in range(0,len(board[0])):
            if board[r][c] == '.':
                add_pichu(succ, board, r, c) 
    return succ

# (EC) Get list of successors of given board state and the row to which a pichu was last added
def successors_EC(board, lastRow):
    succ = []
    for r in range(lastRow, len(board)):
        for c in range(0,len(board[0])):
            if board[r][c] == '.':
                add_pichu_EC(succ, board, r, c) 
    return succ

# check if board is a goal state
def is_goal(board):
    return count_pichus(board) == K 

# Solve!
def solve(initial_board):
    fringe = [(initial_board,0)]
    while len(fringe) > 0:
        currBoard,lastRow = fringe.pop(0)
        for s in successors(currBoard, lastRow):
            if is_goal(s[0]):
                return(s[0])
            fringe.append(s)

    return False

# Solve the extra credit problem
def solve_EC(initial_board):
    fringe = [(initial_board,0)]
    maxPichu = 0
    maxBoard = initial_board
    while len(fringe) > 0:
        currBoard,lastRow = fringe.pop(0)
        for s in successors_EC(currBoard, lastRow):
            if count_pichus(s[0]) > maxPichu:
                maxBoard = s[0]
            fringe.append(s)        
    return maxBoard

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])

    # This is K, the number of agents
    K = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_board(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map) if K > 0 else solve_EC(house_map)
    print ("Here's what we found:")
    print (printable_board(solution) if solution else "None")
