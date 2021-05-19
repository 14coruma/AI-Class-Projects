# AI player for Betsy game
# Standard piece valuations taken from wikipedia
# Used pseudocode from wikipedia to help construct alpha-beta algorithm
# Some ideas for heuristics taken from a Cornell webpage about Chess AI:
# (https://www.cs.cornell.edu/boom/2004sp/ProjectArch/Chess/algorithms.html)
# Piece-square tables taken from freecodecamp.org:
# (https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/)
from BetsyBoard import Board
from PieceSquares import *
import time
import random
from os import environ
environ["OMP_NUM_THREADS"] = "1"
import numpy as np

VALUE = {'.': 0,
         'P': 10, 'p': -10,
         'N': 30, 'n': -30,
         'B': 30, 'b': -30,
         'R': 50, 'r': -50,
         'Q': 90, 'q': -90,
         'K': 50000, 'k': -50000}
nodeCount = 0

class AI:
    # INitialize the AI class (with a time limit)
    def __init__(self, timeLimit):
        self.timeLimit = timeLimit
    
    # Given a Board obj, determine the best possible move
    def get_move(self, board):
        self.time = time.perf_counter()
        self.escapeTime = 0.03 # Extra time to back out and save files
        self.board = board

        depth = 1                    # Limit on depth of minimax
        move, lastMove = 0, 0        # Move returned by alphabeta (tuple)
        val, lastVal = 0, 0          # Evaluation returned by alphabeta
        pv, lastPv = [None], [None]  # Principal Variation array (for sorting move space)

        #  global nodeCount
        #  nodeCount = 0
        # Iterative depth search
        # Break out of this loop if time limit reached
        while time.perf_counter()-self.time < self.timeLimit-self.escapeTime and depth <= 100:
            if move != ():
                lastMove = move
                lastVal = val
                lastPv = pv[:]
            pv = [None]
            a = float('-inf')
            b = float('inf')
            move, val = self.alphabeta(board, self.eval_b(board), depth, a, b, 2, pv, lastPv)
            depth += 1
            #  print("depth: {}, time: {}, nodeCount: {}".format(depth-1, time.perf_counter()-self.time, nodeCount))

        # If something went wrong, just return a legal move
        if lastMove == 0:
            print("Failed search!")
            lastMove = board.move_space()[0]

        board.make_move(lastMove)
        return board

    # Implement alphabeta recursively
    # Returns a tuple (move, evaluate(move))
    # Based on pseudocode from en.wikipedia.org/wiki/Alpha-beta_pruning
    # @param board: current Board obj
    # @param bScore: score of current board
    # @param a, b: alpha and beta (respectively)
    # @param extraDepth: limit of additional depth to be added to tree
    # @param pv: Principal Variation array (to be constructed during search)
    # @param lastPv: PV array from last iteration (to sort moves for better pruning)
    def alphabeta(self, board, bScore, depth, a, b, extraDepth, pv, lastPv):
        #  global nodeCount
        #  nodeCount += 1
        bestMove = None
        v1, v2 = 0, 0
        line = [None] # For current pv construction
        if depth == 0 or board.gameOver:
            pv = []
            return ((), bScore)

        moves = board.move_space()
        random.shuffle(moves)
        # First show moves in lastPv
        # Then sort moves based on highest gain (ie AI.eval(move, 0))
        moves.sort(key=lambda x: abs(AI.eval_m(x, 0))+200*int(x in lastPv), reverse=True)

        # Max player (upper / white)
        if board.upper:
            v1 = float('-inf')
            for move in moves:
                if time.perf_counter()-self.time >= self.timeLimit - self.escapeTime:
                    return ((), 0)
                board.make_move(move)
                # If a capture was made towards bottom of tree, search 1 level deeper
                if extraDepth>depth-1 and move[5] != '.':
                    v2 = self.alphabeta(board, AI.eval_m(move, bScore), depth, a, b, extraDepth-1, line, lastPv)[1]
                else:
                    v2 = self.alphabeta(board, AI.eval_m(move, bScore), depth-1, a, b, extraDepth, line, lastPv)[1]
                board.undo_move(move)
                if v2 > v1:
                    v1 = v2
                    bestMove = move
                # If alpha updated, also update PV
                if v1 > a:
                    a = v1
                    if pv: pv[0] = move
                    else: pv = [move]
                    pv += line
                if a >= b:
                    break
        # Min player (lower / black)
        else:
            v1 = float('inf')
            for move in moves:
                if time.perf_counter()-self.time >= self.timeLimit - self.escapeTime:
                    return ((), 0)
                board.make_move(move)
                # If a capture was made towards bottom of tree, search deeper
                if extraDepth>depth-1 and move[5] != '.':
                    v2 = self.alphabeta(board, AI.eval_m(move, bScore), depth, a, b, extraDepth-1, line, lastPv)[1]
                else:
                    v2 = self.alphabeta(board, AI.eval_m(move, bScore), depth-1, a, b, extraDepth, line, lastPv)[1]
                board.undo_move(move)
                if v2 < v1:
                    v1 = v2
                    bestMove = move
                # If beta updated, also update PV
                if v1 < b:
                    b = v1
                    if pv: pv[0] = move
                    else: pv = [move]
                    pv += line
                if a >= b:
                    break
        return bestMove, v1

    # Evaluate move given a move and previous board's score
    def eval_m(move, prevScore):
        row0, col0, row1, col1, piece, capture, queen = move
        # Remove value of captured piece
        score = prevScore - VALUE[capture]
        # Update value of moved piece's position
        score += POS_VALUE[piece][row1][col1] - POS_VALUE[piece][row0][col0]
        # Update value of captured piece's position
        score -= POS_VALUE[capture][row1][col1]
        return score

    # Evaluate a board
    def eval_b(self, board):
        score = 0
        # Raw piece values
        r = 0
        for row in board.board:
            c = 0
            for piece in row:
                # Piece values
                score += VALUE[piece]
                # Piece position (See PieceSquares.py)
                score += POS_VALUE[piece][r][c]
                c += 1
            r += 1

        return score
