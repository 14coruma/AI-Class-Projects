# Class to allow a human to play the Betsy game
import re

from BetsyBoard import Board

class Human:
    def __init__(self):
        pass

    # Given a board obj, get human's move input
    # (Can assume board has already been shown to user)
    def get_move(self, board):
        string = ""
        move = ()
        while True:
            i = input("Enter your move: ").strip()
            move = board.algebra_to_move(i)
            if not move:
                print("Please enter a move in algebraic notation.")
                board.pretty_print()
                continue

            if move not in board.move_space():
                print("Please choose a legal move.")
                board.pretty_print()
            else:
                break
        board.make_move(move)
        return board
