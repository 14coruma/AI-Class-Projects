#!/usr/bin/python3
# Given a current player, board, and time limit,
# determine & output the recommended next move
from argparse import ArgumentParser, RawTextHelpFormatter
import re
from os import environ
environ["OMP_NUM_THREADS"] = "1"
import numpy as np

from BetsyBoard import Board
from BetsyAI import AI

BOARD_SIZE = (8,8)

# Handle program arguments
def get_args():
    parser = ArgumentParser(description="Compute recommended move for "
            + "the current player given the current board state.",
            formatter_class=RawTextHelpFormatter)
    parser.add_argument("player", type=str, nargs=1, choices=['b','w'],
            help="the current player ('b' or 'w')")
    parser.add_argument("board", type=str, nargs=1,
            help="the current board state, encoded as follows:\n"
            + "8x8 grid flattened into single-line (64 char) string\n"
            + ".     - empty square\n"
            + "P/p - white/black Parakeet\n"
            + "R/r - white/black Robin\n"
            + "N/n - white/black Nighthawk\n"
            + "Q/q - white/black Quetzal\n"
            + "K/k - white/black Kingfisher\n"
            + "B/b - white/black Blue Jay\n")
    parser.add_argument("time", type=int, nargs=1,
            help="the player's time limit, in seconds")
    args = parser.parse_args()
    # Check that args.board is formatted properly
    if len(args.board[0]) != BOARD_SIZE[0] * BOARD_SIZE[1]:
        raise ValueError("bad board size")
    pattern = re.compile("^[\.PpRrNnQqKkBb]*$")
    if not pattern.match(args.board[0]):
        raise ValueError("illegal character(s) in board")
    return args

# Put arguments into proper format, then return as 3-tuple
# player - str
# board - list, with shape BOARD_SIZE
# time - int
def format_args(args):
    board = np.fromiter(args.board[0], dtype=np.dtype('U1'), count=64).reshape(BOARD_SIZE)
    return args.player[0] == 'w', board, args.time[0]

# Main
def main():
    args = get_args()
    upper, boardArr, timeLimit = format_args(args)
    board = Board(upper, boardArr)
    bot = AI(timeLimit)
    move = bot.get_move(board)
    print(move)

if __name__ == "__main__":
    main()
