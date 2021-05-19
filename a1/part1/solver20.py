#!/usr/local/bin/python3
# solver20.py : 2020 Sliding tile puzzle solver
#
# Code by: Alex Fuerst (alfuerst), Andrew Corum (amcorum), Kaitlynne Wilkerson (kwilker)
#
# Based on skeleton code by D. Crandall, September 2020
#
from queue import PriorityQueue
### kwilker: I had difficulty getting the PriorityQueue to work so I did some searching online and found heapq as an alternative. I got a quick explanation of how to use it from this website: https://www.pythonpool.com/python-priority-queue/ . It helped me write the push/ pop statements on lines 392 and 409. 
import heapq
import sys

MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
ROWS = 4
COLS = 5
solved = {1:(0,0), 2:(0,1), 3:(0,2), 4:(0,3), 5:(0,4), 6:(1,0), 7:(1,1), 8:(1,2), 9:(1,3), 10:(1,4), 11:(2,0), 12:(2,1), 13:(2,2), 14:(2,3), 15:(2,4), 16:(3,0), 17:(3,1), 18:(3,2), 19:(3,3), 20:(3,4)}
row1 = [1,2,3,4,5]
row2 = [6,7,8,9,10]
row3 = [11,12,13,14,15]
row4 = [16, 17, 18, 19, 20]
col1 = [1,6,11,16]
col2 = [2,7,12,17]
col3 = [3,8,13,18]
col4 = [4,9,14,19]
col5 = [5,10,15,20]

def valid_index(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row*COLS):(row*COLS+COLS)]
    return ( state[:(row*COLS)] + change_row[-dir:] + change_row[:-dir] + state[(row*COLS+COLS):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::COLS]
    s = list(state)
    s[col::COLS] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

# return a list of possible successor states
def successors(state):
    return [ (shift_row(state, row, dir)) for dir in (-1,1) for row in range(0, ROWS) ] + \
        [ (shift_col(state, col, dir)) for dir in (-1,1) for col in range(0, COLS) ]

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) 

### kwilker: creates a dictionary of current values and a list of the current values of each R/C
def defPlaces (state):
    curr_pos = {}
    curr_row_1 = []
    curr_row_2 = []
    curr_row_3 = []
    curr_row_4 = []
    for i in range(0,5):
        curr_row_1 += [state[i]]
        curr_pos[state[i]] = (0,i)
    c = 0
    for i in range(5,10):
        curr_row_2 += [state[i]]
        curr_pos[state[i]] = (1,c)
        c += 1
    c = 0
    for i in range(10,15):
        curr_row_3 += [state[i]]
        curr_pos[state[i]] = (2,c)
        c+=1
    c = 0
    for i in range(15,20):
        curr_row_4 += [state[i]]
        curr_pos[state[i]] = (3,c)
        c+=1
    curr_col_1 = [curr_row_1[0], curr_row_2[0], curr_row_3[0], curr_row_4[0]]
    curr_col_2 = [curr_row_1[1], curr_row_2[1], curr_row_3[1], curr_row_4[1]]
    curr_col_3 = [curr_row_1[2], curr_row_2[2], curr_row_3[2], curr_row_4[2]]
    curr_col_4 = [curr_row_1[3], curr_row_2[3], curr_row_3[3], curr_row_4[3]]
    curr_col_5 = [curr_row_1[4], curr_row_2[4], curr_row_3[4], curr_row_4[4]]
    set_up = (curr_row_1, curr_row_2, curr_row_3, curr_row_4, curr_col_1, curr_col_2, curr_col_3, curr_col_4, curr_col_5)
    return curr_pos, set_up


## kwilker: figures out which states from R1 and C1 should be moved and ranks how far away they are; returns list of best moves to solve
def search (state):
    current, set_up = defPlaces(state)
    curr_row_1, curr_row_2, curr_row_3, curr_row_4, curr_col_1, curr_col_2, curr_col_3, curr_col_4, curr_col_5 = set_up
    smallest = 1000
    order = []
    temp = []
    u = 0
    d = 0
    l = 0
    ri = 0
    cr1 = 0
    cr2 = 0
    cr3 = 0
    cr4 = 0
    cc1 = 0
    cc2 = 0
    cc3 = 0
    cc4 = 0
    cc5 = 0
    o = []
    possible_moves = []
    h = 0 
    same = 0
    for i in range(len(row1)):
        val = row1[i]
        goal_pos = solved[val]
        curr_pos = current[val]
        ## kwilker: accounts for num of moves with wrap around
        if curr_pos[1] == 0 and goal_pos[1] == 4:
            r = 1
            l = 1
            ri = 4
        elif curr_pos[1] == 1 and goal_pos[1] == 4:
            r = 2
            l = 2
            ri = 3
        elif curr_pos[1] == 0 and goal_pos[1] == 3:
            r = 2
            l = 2
            ri = 3
        elif curr_pos[1] == 1 and goal_pos[1] == 3:
            r = 2
            l = 3
            ri = 2
        elif curr_pos[1] == 4 and goal_pos[1] == 0:
            r = 1 
            l = 4
            ri = 1
        elif curr_pos[1] == 4 and goal_pos[1] == 1:
            r = 2
            l = 3
            ri = 2
        elif curr_pos[1] == 3 and goal_pos[1] == 0:
            r = 2
            l = 3
            ri = 2
        elif curr_pos[1] == 3 and goal_pos[1] == 1:
            r = 2
            l = 2
            ri = 3
        else:
            r = abs(goal_pos[1] - curr_pos[1])
            l = abs(goal_pos[1] - (curr_pos[1]-1))
            ri = abs(goal_pos[1] - (curr_pos[1] +1))
        if curr_pos[0] == 0 and goal_pos[0] == 3:
            c = 1
            u = 1
            d = 3
        elif curr_pos[0] == 3 and goal_pos[0] == 0:
            c = 1
            u = 3
            d = 1
        else:
            c = abs(goal_pos[0] - curr_pos[0])
            u = abs(goal_pos[0] - (curr_pos[0] - 1))
            d = abs(goal_pos[0] - (curr_pos[0] + 1))
        ## kwilker: total num of moves to be made is the sum of moves in the row or col
        total_moves = r + c
        ## kwilker: directions used to determine whether a move in that direction would take more or less moves
        directions = (u, d, l, ri)
        ## kwilker: prunes repeated 1 in R1 and C1
        if val != 1:
            temp += [(val , curr_pos, total_moves, directions)]
    for i in range(len(col1)):
        val = col1[i]
        goal_pos = solved[val]
        curr_pos = current[val]
        ## kwilker: see lines 117 - 168
        if curr_pos[1] == 0 and goal_pos[1] == 4:
            r = 1
            l = 1
            ri = 4
        elif curr_pos[1] == 1 and goal_pos[1] == 4:
            r = 2
            l = 2
            ri = 3
        elif curr_pos[1] == 0 and goal_pos[1] == 3:
            r = 2
            l = 2
            ri = 3
        elif curr_pos[1] == 1 and goal_pos[1] == 3:
            r = 2
            l = 3
            ri = 2
        elif curr_pos[1] == 4 and goal_pos[1] == 0:
            r = 1 
            l = 4
            ri = 1
        elif curr_pos[1] == 4 and goal_pos[1] == 1:
            r = 2
            l = 3
            ri = 2
        elif curr_pos[1] == 3 and goal_pos[1] == 0:
            r = 2
            l = 3
            ri = 2
        elif curr_pos[1] == 3 and goal_pos[1] == 1:
            r = 2
            l = 2
            ri = 3
        else:
            r = abs(goal_pos[1] - curr_pos[1])
            l = abs(goal_pos[1] - (curr_pos[1]-1))
            ri = abs(goal_pos[1] - (curr_pos[1] +1))
        if curr_pos[0] == 0 and goal_pos[0] == 3:
            c = 1
            u = 1
            d = 3
        elif curr_pos[0] == 3 and goal_pos[0] == 0:
            c = 1
            u = 3
            d = 1
        else:
            c = abs(goal_pos[0] - curr_pos[0])
            u = abs(goal_pos[0] - (curr_pos[0] - 1))
            d = abs(goal_pos[0] - (curr_pos[0] + 1))
        total_moves = r + c
        directions = (u, d, l, ri)   
        temp += [(val , curr_pos, total_moves, directions)]
    ## kwilker: sorts the temp list, removes any tiles requiring 0 moves, orders remaining tiles by smallest num of moves to make; adds ordered values to list order and deletes from temp
    c = 0
    temp.sort()
    while temp:
        for i in temp:
            num, curr_pos, total, directions = i
            if total == 0:
                temp.remove(i)
            elif total <= smallest:
                order += [(c, i)] 
                temp.remove(i)
                c += 1

    ## kwilker: checks if any tiles canonically in R1/C1 are in the same R or C; if so, it is assumed that a move by the smallest tile in list would also move the other tiles and those are pruned as tiles to be moved  
    o = []
    if len(order) > 1: 
        for i in order:
            num, curr_pos, total, directions = i[1]
            if curr_pos[0] == 0:
                cr1 += 1
                if cr1 > 1 and num not in o:
                    o += [num]
                    same += 1
            elif curr_pos[0] == 1:
                cr2 += 1
                if cr2 > 1 and num not in o:
                    o += [num]
                    same += 1
            elif curr_pos[0] == 2:
                cr3 += 1
                if cr3 > 1 and num not in o:
                    o += [num]
                    same += 1
            elif curr_pos[0] == 3:
                cr4 += 1
                if cr4 > 1 and num not in o:
                    o += [num]
                    same += 1
            if curr_pos[1] == 0:
                cc1 += 1
                if cc1 > 1 and num not in o:
                    o += [num]
                    same += 1
            elif curr_pos[1] == 1:
                cc2 += 1
                if cc2 > 1 and num not in o:
                    o += [num]
                    same += 1
            elif curr_pos[1] == 2:
                cc3 += 1
                if cc3 > 1 and num not in o:
                    o += [num]
                    same += 1
            elif curr_pos[1] == 3:
                cc4 += 1
                if cc4 > 1 and num not in o:
                    o += [num]
                    same += 1
            elif curr_pos[1] == 4:
                cc5 += 1
                if cc5 > 1 and num not in o:
                    o += [num]
                    same += 1
    for i in order:
        num, curr_pos, total, directions = i[1]
        h += total
        for x in o:
            if num == x:
                order.remove(i)
    for i in order:
        num, curr_pos, total, directions = i[1]
        if num in temp: 
            pass
        else: 
            s = rightPlace(curr_pos, num, directions)
            possible_moves += [(i[0], num, total, s)]
    ## kwilker: returns a heuristic value, which is (the number of moves each tile canonically in R1/C1 needs to take to get to goal position) - (number of tiles in same row or col) -> always less than or equal to n value of the board
    h_val = abs(h - same)
    return possible_moves, h_val

### kwilker: checks to see if the vals of R1/C1 that can be moved are in the right row or col; this ensures that we don't move in a direction that would be counterproductive; returns list of moves generated in code 
def rightPlace(pos, num, directions):
    r = False
    c = False
    goal_pos = solved[num]
    if goal_pos[0] == pos[0]:
        r = True
    if goal_pos[1] == pos[1]:
        c = True
    possible = posMove(num, pos, (r,c), directions)
    return possible 

### kwilker: Based on the results from rightPlace, determine whether a move in L/R or U/D direction is possible; returns best moves for each valid tile that can be moved 
def posMove(num, pos, moves, directions):
    row, col = moves
    col_move = True
    row_move = True
    if row == True:
        col_move = False
    if col == True: 
        row_move = False
    passTo = ((row_move, pos[0]), (col_move, pos[1]))
    lstMoves = code(num, passTo, directions)
    return lstMoves

### kwilker: Takes values from posMoves and turns them into moves. Decides whether a R or L and U or D move is better based on which direction would result in fewer moves. Returns list of moves 
def code (num, nextMoves, directions):
    possMoves = []
    temp = []
    t = []
    row, col = nextMoves
    u, d, l, r = directions
    col_first = False
    row_first = False
    if row[0] == True and col[0] == True:
        if l < r:
            temp += ['L'+ str(row[1]+1)] 
        elif l > r:
            temp += ['R' + str(row[1]+1)]
        else: 
            if l < u and l < d:
                row_first = True
                t += [('L'+ str(row[1]+1), 'r', row_first)]
            if l >= u:  
                col_first = True
                if l >= d:
                    t += [('D'+ str(col[1]+1), 'c', col_first)]
                else:
                    t += [('U'+ str(col[1]+1), 'c', col_first)]
        if u < d:
            temp += ['U'+ str(col[1]+1)]
        elif u > d: 
            temp += ['D' + str(col[1]+1)]
    elif row[0] == False and col[0] == True:
        if u <= d:
            temp += ['U'+ str(col[1]+1)]
        elif u > d: 
            temp += ['D' + str(col[1]+1)]
    elif row[0] == True and col[0] == False: 
        if l <= r:
            temp += ['L'+ str(row[1]+1)] 
        elif l > r:
            temp += ['R' + str(row[1]+1)]
    for i in temp:
        if i not in possMoves:
            possMoves += [i]
    for i in t:
        move, d, d_value = i
        if d == 'c' and d_value == True:
            if move not in possMoves:
                possMoves += [move]
        elif d == 'r' and d_value == True:
            if move not in possMoves:
                possMoves += [move]
    return possMoves


# The solver! - using BFS right now
def solve(initial_board):
    fringe = [(0, (initial_board, [])) ]
    while len(fringe) > 0:
        possible = []        
        valid_successor =[]
        ## kwilker: see line 9
        (h_val, (state, route_so_far)) = heapq.heappop(fringe)
        possible, h_val = search(state)
        f = len(route_so_far) + h_val
        for (succ, move) in successors( state ):
            ## kwilker: lines 396 to 401 prune potential moves that were not calculated to get the goal state efficiently 
            for i in possible:
                moves = i[3]
                h = i[2]
                for x in moves:
                    if x == move:
                        valid_successor += [(succ, move, f)]
        for (succ, move, f) in valid_successor:
            if is_goal(succ):
                return( route_so_far + [move,] )
            new_path = route_so_far + [move]
            ## kwilker: only adds to fringe if path length is less than equal to size of f 
            if len(new_path) <= f:
                ## kwilker: see line 9
                heapq.heappush(fringe, (f,(succ, route_so_far + [move,], )))
    return False


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))