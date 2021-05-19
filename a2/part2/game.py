#!/usr/bin/python3
# Run a game of Betsy between two players locally
# For testing purposes
from argparse import ArgumentParser
import time
from os import environ
environ["OMP_NUM_THREADS"] = "1"
import numpy as np

from BetsyBoard import Board
from BetsyAI import AI
from HumanPlayer import Human

BOARD_SIZE = (8,8)
START_BOARD = "RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr"

def get_args():
    parser = ArgumentParser(description="Execute a game of Betsy between two players")
    parser.add_argument("white", type=str, nargs=1, choices=['AI', 'Human'],
            help="white player ('AI' or 'Human')")
    parser.add_argument("black", type=str, nargs=1, choices=['AI', 'Human'],
            help="black player ('AI' or 'Human')")
    parser.add_argument("time", type=int, nargs=1,
            help="the player's time limit, in seconds")
    args = parser.parse_args()
    return args

def format_args(args):
    b = np.fromiter(START_BOARD, dtype=np.dtype('U1'), count=64).reshape(BOARD_SIZE)
    return b, args.white[0], args.black[0], args.time[0]

def main():
    args = get_args()
    boardArr, wPlayer, bPlayer, timeLimit = format_args(args)
    board = Board(True, boardArr)

    white = AI(timeLimit) if wPlayer == 'AI' else Human()
    black = AI(timeLimit) if bPlayer == 'AI' else Human()

    # Run the game until someone wins or cheats
    while not board.gameOver:
        # White's turn
        board.pretty_print()
        t = time.perf_counter()
        print("\nWhite's move...")
        board = white.get_move(board)
        print("Time elapsed: {}".format(time.perf_counter() - t))
        if board.gameOver:
            break

        # Black's turn
        board.pretty_print()
        t = time.perf_counter()
        print("\nBlack's move...")
        board = black.get_move(board)
        print("Time elapsed: {}".format(time.perf_counter() - t))
        print(board)

    board.pretty_print()
    print("{} wins!".format('White' if board.winner == 'w' else 'Black'))

if __name__ == "__main__":
    main()
