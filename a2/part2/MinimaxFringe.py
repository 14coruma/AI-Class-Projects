# This code creates minimax w/ alpha-beta pruning using the fringe
# From initial testing, it seems like the recursive method of traversing
# the game tree is faster, so it will be used in the final product.

# Implement alphabeta with a fringe
# Returns the board, already updated after making best move
def f_alphabeta(self, board, depth):
    bestMove = None
    # Nodes are a list: [board, depth, score, a, b]
    fringe = [[board, depth, None, float('-inf'), float('inf')]]
    while fringe:
        currBoard, currDepth, currVal, currA, currB = fringe.pop()
        if time.perf_counter()-self.time >= self.timeLimit-self.escapeTime:
            return ()
        if currVal is None:
            if currDepth == 0:
                currVal = self.evaluate(currBoard)
                fringe.append([currBoard, currDepth, currVal, currA, currB])
            else:
                currVal = float('-inf') if currBoard.upper else float('inf')
                fringe.append([currBoard, currDepth, currVal, currA, currB])
                for move in currBoard.move_space():
                    newBoard = copy.deepcopy(currBoard)
                    newBoard.make_move(move)
                    fringe.append([newBoard, currDepth-1, None, currA, currB])
        else:
            for i in range(len(fringe)-1, -1, -1):
                node = fringe[i]
                if node[1] == currDepth+1:
                    bestVal = node[2]
                    if (node[0].upper and currVal>bestVal) or ((not node[0].upper) and currVal<bestVal):
                        bestVal = currVal
                        if i == 0: bestMove = currBoard
                    a = node[3]
                    b = node[4]
                    if node[0].upper:
                        a = max(a, bestVal)
                        if a >= b:
                            fringe = fringe[:i+1]
                    else:
                        b = min(b, bestVal)
                        if a >= b:
                            fringe = fringe[:i+1]
                    fringe[i] = [node[0], currDepth+1, bestVal, a, b]
                    for j in range(i+1, len(fringe)):
                        fringe[j][3] = a
                        fringe[j][4] = b
                    break
    return bestMove

# Old evaluation function (fancy, but slow)
def evaluate(self, board):
    weight = {'piece': 10, 'pawn': 0, 'mobility': 0, 'seen': 0, 
              'database': 1000}
    score = {}
    for key in weight.keys():
        score[key] = 0
    opening = {'.': 0,
             'P': 1, 'p': -1,
             'N': 3, 'n': -3,
             'B': 3, 'b': -3,
             'R': 5, 'r': -5,
             'Q': 9, 'q': -9,
             'K': 5000, 'k': -5000}
    middlegame = {'.': 0,
                  'P': 1, 'p': -1,
                  'N': 3.5, 'n': -3.5,
                  'B': 3.5, 'b': -3.5,
                  'R': 5.25, 'r': -5.25,
                  'Q': 10, 'q': -10,
                  'K': 5000, 'k': -5000}
    value = None
    if len(self.curr_game) > 18 and len(self.curr_game) < 40:
        value = middlegame
    else:
        value = opening
    r = 0
    for row in board.board:
        for piece in row:
            # Piece values
            score['piece'] += value[piece]
            # Pawn advancement
            if piece == 'P':
                score['pawn'] += r-1
            elif piece == 'p':
                score['pawn'] -= 6-r
        r += 1

    # Total player mobility
    currUpper = board.upper
    board.upper = True
    score['mobility'] += len(board.move_space())
    board.upper = False
    score['mobility'] -= len(board.move_space())
    board.upper = currUpper

    # If board has been seen before (don't want to be stalling)
    if str(board) in self.curr_game:
        score['seen'] += -1 if not board.upper and self.board.upper else 0
        score['seen'] += 1 if board.upper and not self.board.upper else 0

    # Use board rating from database
    if len(self.curr_game)<=8 and str(board) in self.database:
        score['database'] = self.database[str(board)][0] - 0.5
    
    total = 0
    for k in score.keys():
        total += score[k] * weight[k]
    return total

