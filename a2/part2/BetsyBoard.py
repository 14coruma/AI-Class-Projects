# Board state for Betsy game
import re
from os import environ
environ["OMP_NUM_THREADS"] = "1"
import numpy as np

class bcolors:
    WHITE = '\033[37m'
    BLACK = '\033[30m'
    GREEN = '\033[102m'
    BLUE = '\033[104m'
    ENDC = '\033[0m'

class Board:
    # Initialize a board state
    def __init__(self, upper, board, gameOver=False, winner=''):
        self.board = np.copy(board)
        self.upper = upper
        self.pieces = {
                'p': self.parakeet, 'r': self.robin, 'n': self.nighthawk,
                'q': self.quetzal, 'k': self.kingfisher, 'b': self.bluejay
        }
        self.gameOver = gameOver
        self.winner = winner
    
    # Convert the board into a string
    def __str__(self):
        return ''.join(map(str, self.board.flatten()))

    def __gt__(self, other):
        return True

    def algebra_to_move(self, string):
        num = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        pattern = re.compile("^([KQRNB]?)([a-h]?)([1-8]?)(x?)([a-h])([1-8])\+*$") 
        m = pattern.match(string)
        if not m:
            return False
        g = m.groups()
        piece = 'P' if g[0] == '' else g[0]
        r2 = int(g[5])-1
        c2 = num[g[4]]
        capture = sefl.board[r2][c2] if g[3] == 'x' else '.'
        if not self.upper: piece = piece.lower()
        if g[1] and g[2]:
            return (num[g[1]], int(g[2])-1, r2, c2, piece, capture)
        elif g[1]:
            c = num[g[1]]
            for r in range(len(self.board)):
                move = (r, c, r2, c2, piece, capture)
                if self.board[r][c] == piece:
                    if move in self.pieces[piece.lower()](r, c):
                        return move
        elif g[2]:
            r = int(g[2])-1
            for c in range(len(self.board[0])):
                move = (r, c, r2, c2, piece, capture)
                if self.board[r][c] == piece:
                    if move in self.pieces[piece.lower()](r, c):
                        return move
        else:
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    move = (r, c, r2, c2, piece, capture)
                    if self.board[r][c] == piece:
                        if move in self.pieces[piece.lower()](r, c):
                            return move
        return False

    # Print the board in a pretty square
    def pretty_print(self):
        print(" abcdefgh")
        r = 0
        for row in self.board:
            string = str(r+1)
            c = 0
            for piece in row:
                string += bcolors.GREEN if (c+r)%2 == 0 else bcolors.BLUE
                string += bcolors.BLACK if piece.islower() else bcolors.WHITE
                if piece == '.':
                    string += ' '
                else:
                    string += piece
                string += bcolors.ENDC
                c += 1
            string += str(r+1)
            r += 1
            print(string)
        print(" abcdefgh")

    # Given a Move 4-tuple, update the board, then
    # update the current player
    def make_move(self, move):
        row0, col0, row1, col1, oldPiece, capture, newPiece = move
        self.board[row0][col0] = '.'
        self.board[row1][col1] = newPiece
        self.upper = not self.upper
        if capture == 'k':
            self.gameOver = True
            self.winner = 'w'
        elif capture == 'K':
            self.gameOver = True
            self.winner = 'b'

    # Given a Move 4-tuple, undo the move
    def undo_move(self, move):
        row0, col0, row1, col1, oldPiece, capture, newPiece = move
        self.upper = not self.upper
        self.gameOver = False
        self.winner = ''
        self.board[row0][col0] = oldPiece
        self.board[row1][col1] = capture

    # Return set of all possible moves given current state
    def move_space(self):
        moves = []
        r = 0
        for row in self.board:
            c = 0
            for piece in row:
                if piece != "." and piece.isupper() == self.upper:
                    moves += self.pieces[piece.lower()](r, c)
                c += 1
            r += 1 
        return moves

    #
    # Below is code for calculating possible moves for each piece
    # It works, but it gets messy... sorry
    #
 
    # Return list of moves of Robin in position (r, c)
    def robin(self, r, c):
        moves = []
        piece = 'R' if self.upper else 'r'
        self.horiz_vert_moves(moves, r, c, piece)
        return moves

    # Return list of moves for Blue Jay in position (r,c)
    def bluejay(self, r, c):
        moves = []
        piece = 'B' if self.upper else 'b'
        self.diag_moves(moves, r, c, piece)
        return moves

    # Return list of moves for Quetzal in position (r,c)
    def quetzal(self, r, c):
        moves = []
        piece = 'Q' if self.upper else 'q'
        self.horiz_vert_moves(moves, r, c, piece)
        self.diag_moves(moves, r, c, piece)
        return moves
   
    # Return list of moves for Kingfisher in position (r,c)
    def kingfisher(self, r, c):
        moves = []
        piece = 'K' if self.upper else 'k'
        if r > 0: self.basic_move(moves, r, c, r-1, c, piece)
        if r > 0 and c > 0: self.basic_move(moves, r, c, r-1, c-1, piece)
        if c > 0: self.basic_move(moves, r, c, r, c-1, piece)
        if r < 7 and c > 0: self.basic_move(moves, r, c, r+1, c-1, piece)
        if r < 7: self.basic_move(moves, r, c, r+1, c, piece)
        if r < 7 and c < 7: self.basic_move(moves, r, c, r+1, c+1, piece)
        if c < 7: self.basic_move(moves, r, c, r, c+1, piece)
        if r > 0 and c < 7: self.basic_move(moves, r, c, r-1, c+1, piece)
        return moves

    # Return list of moves for Nighthawk from position (r,c)
    def nighthawk(self, r, c):
        moves = []
        piece = 'N' if self.upper else 'n'
        if r > 0 and c > 1: self.basic_move(moves, r, c, r-1, c-2, piece)
        if r > 0 and c < 6: self.basic_move(moves, r, c, r-1, c+2, piece)
        if r > 1 and c > 0: self.basic_move(moves, r, c, r-2, c-1, piece)
        if r > 1 and c < 7: self.basic_move(moves, r, c, r-2, c+1, piece)
        if r < 7 and c > 1: self.basic_move(moves, r, c, r+1, c-2, piece)
        if r < 7 and c < 6: self.basic_move(moves, r, c, r+1, c+2, piece)
        if r < 6 and c > 0: self.basic_move(moves, r, c, r+2, c-1, piece)
        if r < 6 and c < 7: self.basic_move(moves, r, c, r+2, c+1, piece)
        return moves

    # Update 'moves' list with new move (if space is available)
    # Return True if more moves may be found in this direction
    # Return False if no more moves can be found in this direction
    def basic_move(self, moves, r0, c0, r1, c1, piece, queen=False):
        char = self.board[r1][c1]
        newPiece = ('Q' if self.upper else 'q') if queen else piece
        if char == '.':
            moves.append((r0,c0,r1,c1,piece,'.',newPiece))
            return True
        elif char.islower() == self.upper:
            moves.append((r0,c0,r1,c1,piece,char,newPiece))
        return False

    # Update "moves" list with new moves in horizontal and vertical directions
    # Use for Robin and Quetzal
    def horiz_vert_moves(self, moves, r, c, piece):
        for newR in range(r-1, -1, -1):
            if not self.basic_move(moves, r, c, newR, c, piece): break
        for newR in range(r+1, 8):
            if not self.basic_move(moves, r, c, newR, c, piece): break
        for newC in range(c-1, -1, -1):
            if not self.basic_move(moves, r, c, r, newC, piece): break
        for newC in range(c+1, 8):
            if not self.basic_move(moves, r, c, r, newC, piece): break

    # Update "moves"  list with new moves in diagonal directions
    # Use for Blue Jay and Quetzal
    def diag_moves(self, moves, r, c, piece):
        newR, newC = r, c
        while newR > 0 and newC > 0:
            newR -= 1
            newC -= 1
            if not self.basic_move(moves, r, c, newR, newC, piece): break
        newR, newC = r, c
        while newR > 0 and newC < 7:
            newR -= 1
            newC += 1
            if not self.basic_move(moves, r, c, newR, newC, piece): break
        newR, newC = r, c
        while newR < 7 and newC > 0:
            newR += 1
            newC -= 1
            if not self.basic_move(moves, r, c, newR, newC, piece): break
        newR, newC = r, c
        while newR < 7 and newC < 7:
            newR += 1
            newC += 1
            if not self.basic_move(moves, r, c, newR, newC, piece): break
    
    # Return list of moves of parakeet in position (r, c)
    def parakeet(self, r, c):
        moves = []
        # White moves (upper)
        if self.upper:
            # Move normally
            if r < 6:
                if self.board[r+1][c] == '.':
                    # Move once
                    self.basic_move(moves,r,c,r+1,c,'P')
                    # Move twice
                    if r == 1 and self.board[r+2][c] == '.':
                        self.basic_move(moves,r,c,r+2,c,'P')
                # Attack diagonally
                if c < 7 and self.board[r+1][c+1].islower():
                    self.basic_move(moves,r,c,r+1,c+1,'P')
                if c > 0 and self.board[r+1][c-1].islower():
                    self.basic_move(moves,r,c,r+1,c-1,'P')
            # Move to last row
            if r == 6:
                # Move once
                if self.board[7][c] == '.':
                    self.basic_move(moves,6,c,7,c,'P',True)
                # Attack diagonally
                if c < 7 and self.board[7][c+1].islower():
                    self.basic_move(moves,6,c,7,c+1,'P',True)
                if c > 0 and self.board[r+1][c-1].islower():
                    self.basic_move(moves,6,c,7,c-1,'P',True)
        # Black moves (lower)
        else:
            # Move normally
            if r > 1:
                if self.board[r-1][c] == '.':
                    # Move once
                    self.basic_move(moves,r,c,r-1,c,'p')
                    # Move twice
                    if r == 6 and self.board[r-2][c] == '.':
                        self.basic_move(moves,r,c,r-2,c,'p')
                # Attack diagonally
                if c < 7 and self.board[r-1][c+1].isupper():
                    self.basic_move(moves,r,c,r-1,c+1,'p')
                if c > 0 and self.board[r-1][c-1].isupper():
                    self.basic_move(moves,r,c,r-1,c-1,'p')
            # Move to last row
            if r == 1:
                # Move once
                if self.board[0][c] == '.':
                    self.basic_move(moves,1,c,0,c,'p',True)
                # Attack diagonally
                if c < 7 and self.board[0][c+1].isupper():
                    self.basic_move(moves,1,c,0,c+1,'p',True)
                if c > 0 and self.board[0][c-1].isupper():
                    self.basic_move(moves,1,c,0,c-1,'p',True)
        return moves
