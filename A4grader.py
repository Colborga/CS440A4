import os
import A4 as useThisCode
import copy
import signal

# Code to limit running time of specific parts of code.
#  To use, do this for example...
#
#  signal.alarm(seconds)
#  try:
#    ... run this ...
#  except TimeoutException:
#     print(' 0/8 points. Your depthFirstSearch did not terminate in', seconds/60, 'minutes.')
# Exception to signal exceeding time limit.


class TimeoutException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def timeout(signum, frame):
    raise TimeoutException


# Comment next line for Python2
# signal.signal(signal.SIGALRM, timeout)


# Eval all function defs in students notebook. Assumes the following command
# has been executed.
#   jupyter nbconvert --to script *.ipynb --stdout > nbconvert.py

if False:
    print('========================RUNNING INSTRUCTOR''S SOLUTION!')
    import A4 as useThisCode
elif False:
    print('Extracting python code from notebook and storing in nbconvert.py')
    import subprocess
    with open('nbconvert.py', 'w') as outputFile:
        subprocess.call(['jupyter', 'nbconvert', '--to', 'script',
                         '*.ipynb', '--stdout'], stdout=outputFile)
    # from https://stackoverflow.com/questions/30133278/import-only-functions-from-a-python-file
    import sys
    import ast
    import types
    with open('nbconvert.py') as fp:
        tree = ast.parse(fp.read(), 'eval')
    print('Removing all statements that are not function or class defs, import or global assignment statments.')
    '''
    for node in tree.body[:]:
        if (not isinstance(node, ast.FunctionDef) and
            not isinstance(node, ast.ClassDef) and
            not isinstance(node, ast.Import) and
            not isinstance(node, ast.Assign)):
            tree.body.remove(node)
    '''
    # Now write remaining code to py file and import it
    module = types.ModuleType('nbconvertStripped')
    code = compile(tree, 'nbconvertStripped.py', 'exec')
    sys.modules['nbconvertStripped'] = module
    exec(code, module.__dict__)
    import nbconvertStripped as useThisCode
negamax = useThisCode.negamax
# negamaxab = useThisCode.negamaxab
negamaxIDS = useThisCode.negamaxIDS
negamaxIDSab = useThisCode.negamaxIDSab
TTT = useThisCode.TTT
# playGames = useThisCode.playGames
playGame = useThisCode.playGame
# ebf = useThisCode.ebf


g = 0

seconds = 60 * 5


class TTT2(object):

    def __init__(self, board):
        self.board = board
        self.player = 'X'
        self.playerLookAHead = self.player
        self.movesExplored = 0

    def getWinningValue(self):
        return 1
    
    def locations(self, c):
        return [i for i, mark in enumerate(self.board) if mark == c]

    def getNumberMovesExplored(self):
        return self.movesExplored
    
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
            return None # -0.1  # was None in lecture notes

    def isOver(self):
        return self.getUtility() is not None

    def makeMove(self, move):
        self.board[move] = self.playerLookAHead
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'
        self.movesExplored += 1

    def changePlayer(self):
        self.player = 'X' if self.player == 'O' else 'O'
        self.playerLookAHead = self.player

    def unmakeMove(self, move):
        self.board[move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def __str__(self):
        s = '{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(*self.board)
        return s

# def opponent(board):
#     blanks = [i for i, mark in enumerate(board) if mark == ' ']
#     return blanks[-1]
#     # return random.choice(blanks)
#     # return blanks[0]


'''
O X 
O  
  X
'''


startBoard = ['O', 'X', ' ', 'O', ' ', ' ', ' ', 'X', ' ']
print('\nTesting negamax starting from', startBoard)
game = TTT2(startBoard)
value, move = negamax(game, 5)
if value == 1:
    g += 10
    print('\n--- 10/10 points. negamax correctly returns value of', value)
else:
    print('\n---  0/10 points. negamax returned value', value, ' It should return value of 1.')

n = game.getNumberMovesExplored()
if 100 < n < 500:
    g += 10
    print('\n--- 10/10 points. negamax correctly explored', n, 'states.')
else:
    print('\n---  0/10 points. negamax explored', n, 'states. It should have explored between 100 and 500.')
    

'''
O X X
O O 
  X
'''


startBoard = ['O', 'X', 'X', 'O', 'O', ' ', ' ', 'X', ' ']
print('\nTesting negamax starting from', startBoard)
game = TTT2(startBoard)
value, move = negamax(game, 5)
if value == -1 and move in [5, 6, 8]:
    g += 10
    print('\n--- 10/10 points. negamax correctly returns value of', value, 'and move of', move)
else:
    print('\n---  0/10 points. negamax returned value', value, 'and move', move,' It should return value of -1 and move of 5, 6, or 8.')

startBoard = ['O', 'X', 'X', 'O', 'O', ' ', ' ', 'X', ' ']
print('\nTesting negamaxIDS with max depth of 5, starting from', startBoard)
game = TTT2(startBoard)
value, move = negamaxIDS(game, 5)
if value == -1 and move in [5, 6, 8]:
    g += 10
    print('\n--- 10/10 points. negamaxIDS correctly returns value of', value, 'and move of', move)
else:
    print('\n---  0/10 points. negamaxIDS returned value of', value, 'and move of', move,'It should return value of -1 and move of 5, 6, or 8.')



startBoard = ['O', 'X', 'X', 'O', 'O', ' ', ' ', 'X', ' ']
print('\nTesting negamaxIDSab starting from', startBoard)
game = TTT2(startBoard)
value, move = negamaxIDSab(game, 5)
if value == -1 and move in [5, 6, 8]:
    g += 20
    print('\n--- 20/20 points. negamaxIDSab correctly returns value of', value, 'and move of', move)
else:
    print('\n---  0/20 points. negamaxIDSab returned value of', value, 'and move of', move,'It should return value of -1 and move of 5, 6, or 8.')


def opponent(board):
    blanks = [i for i, mark in enumerate(board) if mark == ' ']
    return blanks[-1]

def myPlayGame(game, opponent, maxDepthLimit, negamaxF=negamax):
    print(game)
    while not game.isOver():
        score, move = negamaxF(game, maxDepthLimit)
        if move == None :
            print('move is None. Stopping.')
            break
        game.makeMove(move)
        print('Player', game.player, 'to', move, 'for score' ,score)
        print(game)
        if not game.isOver():
            game.changePlayer()
            opponentMove = opponent(game.board)
            game.makeMove(opponentMove)
            print('Player', game.player, 'to', opponentMove)
            print(game)
            game.changePlayer()


print('\nTesting playGame with opponent that always plays in highest numbered position.')
game = TTT()
myPlayGame(game, opponent, 10)
board = game.board
if board[:3].count('X') == 3:
    g += 10
    print('\n--- 10/10 points. playGame correctly wins by filling top row with X''s.')
else:
    print('\n---  0/10 points. playGame does not correctly win by filling top row with X''s.')
    



    
name = os.getcwd().split('/')[-1]

print('\n{} Execution Grade is {}/70'.format(name, g))

print('\n Remaining 30 points will be based on the output of your playGames function.')

print('\n{} FINAL GRADE is __/100'.format(name))
