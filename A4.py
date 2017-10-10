class TTT(object):
    def __init__(self):
        self.board = [' '] * 9
        self.player = 'X'
        self.movesExplored = 0
        if False:
            self.board = ['X', 'X', ' ', 'X', 'O', 'O', ' ', ' ', ' ']
            self.player = 'O'
        self.playerLookAHead = self.player

    def getWinningValue(self):
        return 1

    def locations(self, c):
        return [i for i, mark in enumerate(self.board) if mark == c]

    def getMoves(self):
        moves = self.locations(' ')
        return moves

    def getUtility(self):
        whereX = self.locations('X')
        whereO = self.locations('O')
        wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]
        isXWon = any([all([wi in whereX for wi in w]) for w in wins])
        isOWon = any([all([wi in whereO for wi in w]) for w in wins])
        if isXWon:
            return 1 if self.playerLookAHead is 'X' else -1
        elif isOWon:
            return 1 if self.playerLookAHead is 'O' else -1
        elif ' ' not in self.board:
            return 0
        else:
            return None  ########################################################## CHANGED FROM -0.1

    def isOver(self):
        return self.getUtility() is not None

    def makeMove(self, move):
        self.movesExplored += 1
        self.board[move] = self.playerLookAHead
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def changePlayer(self):
        self.player = 'X' if self.player == 'O' else 'O'
        self.playerLookAHead = self.player

    def unmakeMove(self, move):
        self.board[move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def getMovesExplored(self):
        return self.movesExplored
    def getBoard(self):
        return self.board

    def __str__(self):
        s = '{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(*self.board)
        return s


def negamax(game, depthLeft):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None # call to negamax knows the move
    # Find best move and its value from current state
    bestValue, bestMove = None, None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamax(game, depthLeft-1)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if bestValue is None or value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue, bestMove = value, move
    return bestValue, bestMove


def negamaxIDS(game, depthLeft):
    #This is calling negamax for each depth, this works because it will return at the minimum depth at which there is a winning value.
    for depth in range(depthLeft + 1):
        bestVal, bestMove = negamax(game, depth)
        if bestVal == game.getWinningValue():
            return bestVal, bestMove
    return bestVal, bestMove

def negamaxIDSab(game, depthLeft):
    for depth in range(depthLeft + 1):
        bestVal, bestMove = negamaxIDSabrunner(game, depth)
        if bestVal == game.getWinningValue():
            return bestVal, bestMove
    return bestVal, bestMove


def negamaxIDSabrunner(game, depthLeft, alpha = -10000, beta = 10000):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None # call to negamax knows the move
    # Find best move and its value from current state
    bestValue, bestMove = None, None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamax(game, depthLeft-1)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if value == game.getWinningValue():
            return value, move
        if bestValue is None or value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue, bestMove = value, move
        if bestValue > alpha:
             alpha = bestValue
        if alpha >= beta:
            return bestValue, bestMove
    return bestValue, bestMove

def ebf(nNodes, depth, precision=0.01):
    if nNodes == 0:
        return 0

    def ebfRec(low, high):
        mid = (low + high) * 0.5
        if mid == 1:
            estimate = 1 + depth
        else:
            estimate = (1 - mid**(depth + 1)) / (1 - mid)
        if abs(estimate - nNodes) < precision:
            return mid
        if estimate > nNodes:
            return ebfRec(low, mid)
        else:
            return ebfRec(mid, high)

    return ebfRec(1, nNodes)

def opponent(board):
    return board.index(' ')


def playGame(game, opponent, depthLimit, negaFun, printBoard):
    if printBoard:
        print(game)
    while not game.isOver():
        if negaFun == 'normal':
            score, move = negamax(game, depthLimit)
        elif negaFun == 'ids':
            score, move = negamaxIDS(game, depthLimit)
        elif negaFun == 'idsab':
            score, move = negamaxIDSab(game, depthLimit)

        if move == None:
            print('move is None. Stopping.')
            break
        game.makeMove(move)
        if printBoard:
            print('Player', game.player, 'to', move, 'for score', score)
            print(game)
        if not game.isOver():
            game.changePlayer()
            opponentMove = opponent(game.board)
            game.makeMove(opponentMove)
            if printBoard:
                print('Player', game.player, 'to', opponentMove)  ### FIXED ERROR IN THIS LINE!
                print(game)
            game.changePlayer()

def playGames():
    game = TTT()
    playGame(game, opponent, 20, 'normal', False)
    board = game.getBoard()
    numX = board.count('X')
    numMoves = 9 - board.count(' ')

    print('Negamax made ', numX, 'moves.  ', game.getMovesExplored(), ' Moves explored for ebf(', game.getMovesExplored(), ', ', numMoves, ') of ', ebf(game.getMovesExplored(), numMoves))

    game = TTT()
    playGame(game, opponent, 20, 'ids', False)
    board = game.getBoard()
    numX = board.count('X')
    numMoves = 9 - board.count(' ')

    print('Negamax made ', numX, 'moves.  ', game.getMovesExplored(), ' Moves explored for ebf(',
          game.getMovesExplored(), ', ', numMoves, ') of ', ebf(game.getMovesExplored(), numMoves))

    game = TTT()
    playGame(game, opponent, 20, 'idsab', False)
    board = game.getBoard()
    numX = board.count('X')
    numMoves = 9 - board.count(' ')

    print('Negamax made ', numX, 'moves.  ', game.getMovesExplored(), ' Moves explored for ebf(',
          game.getMovesExplored(), ', ', numMoves, ') of ', ebf(game.getMovesExplored(), numMoves))


if __name__ == "__main__":
   playGames()