from math import isnan
from math import e
import othellogame as nn

# Returns the sigmoid function 
def sigmoid(x):
    ret = 1/(1+e**(-x))
    if isnan(ret):
        return 0
    return ret

# Generate the default starter board
def generateBoard():
    board = [0 for i in range(nn.BOARDSIZE)]
    board[nn.BOARDSIZE//2 - nn.BOARDDIM//2 - 1] = -1
    board[nn.BOARDSIZE//2- nn.BOARDDIM//2] = 1
    board[nn.BOARDSIZE//2 + nn.BOARDDIM//2 - 1] = 1
    board[nn.BOARDSIZE//2 + nn.BOARDDIM//2] = -1
    return board

# Translate an x and y coordinate into the equivalent on a linear board
def translate(x, y):
    return y*nn.BOARDDIM + x

# Returns all possible moves the player can make along with the directions the
# move would effect
def possibleMoves(player, board):
    moves = {}
    for i in range(nn.BOARDSIZE): # Cycle through every tile to check validity
        if board[i] == 0:
            x = i % nn.BOARDDIM
            y = i // nn.BOARDDIM
            
            # upper left
            if x-1 >= 0 and y-1 >= 0 and board[translate(x-1,y-1)] == 0-player:
                index = 2
                while x-index >= 0 and y-index >= 0:
                    if board[translate(x-index,y-index)] == player:
                        if i in moves:
                            moves[i].append('UL')
                        else:
                            moves[i] = ['UL']
                        break
                    if board[translate(x-index, y-index)] == 0: # invalid
                        break
                    index += 1
                    
            # upper
            if y-1 >= 0 and board[translate(x,y-1)] == 0-player:
                index = 2
                while y-index >= 0:
                    if board[translate(x,y-index)] == player:
                        if i in moves:
                            moves[i].append('UP')
                        else:
                            moves[i] = ['UP']
                        break
                    if board[translate(x,y-index)] == 0: # invalid
                        break
                    index += 1
                    
            # upper right
            if x+1 < nn.BOARDDIM and y-1 >= 0 and board[translate(x+1,y-1)] == 0-player:
                index = 2
                while x+index < nn.BOARDDIM and y-index >= 0:
                    if board[translate(x+index,y-index)] == player:
                        if i in moves:
                            moves[i].append('UR')
                        else:
                            moves[i] = ['UR']
                        break
                    if board[translate(x+index, y-index)] == 0: # invalid
                        break
                    index += 1
                    
            # left
            if x-1 >= 0 and board[translate(x-1,y)] == 0-player:
                index = 2
                while x-index >= 0:
                    if board[translate(x-index,y)] == player:
                        if i in moves:
                            moves[i].append('LEFT')
                        else:
                            moves[i] = ['LEFT']
                        break
                    if board[translate(x-index, y)] == 0: # invalid
                        break
                    index += 1
            
            # right
            if x+1 < nn.BOARDDIM and board[translate(x+1,y)] == 0-player:
                index = 2
                while x+index < nn.BOARDDIM:
                    if board[translate(x+index,y)] == player:
                        if i in moves:
                            moves[i].append('RIGHT')
                        else:
                            moves[i] = ['RIGHT']
                        break
                    if board[translate(x+index, y)] == 0: # invalid
                        break
                    index += 1
            
            # lower left
            if x-1 >= 0 and y+1 < nn.BOARDDIM and board[translate(x-1,y+1)] == 0-player:
                index = 2
                while x-index >= 0 and y+index < nn.BOARDDIM:
                    if board[translate(x-index,y+index)] == player:
                        if i in moves:
                            moves[i].append('LL')
                        else:
                            moves[i] = ['LL']
                        break
                    if board[translate(x-index, y+index)] == 0: # invalid
                        break
                    index += 1
            
            # lower
            if y+1 < nn.BOARDDIM and board[translate(x,y+1)] == 0-player:
                index = 2
                while y+index < nn.BOARDDIM:
                    if board[translate(x,y+index)] == player:
                        if i in moves:
                            moves[i].append('LOW')
                        else:
                            moves[i] = ['LOW']
                        break
                    if board[translate(x, y+index)] == 0: # invalid
                        break
                    index += 1
            
            # lower right
            if x+1 < nn.BOARDDIM and y+1 < nn.BOARDDIM and board[translate(x+1,y+1)] == 0-player:
                index = 2
                while x+index < nn.BOARDDIM and y+index < nn.BOARDDIM:
                    if board[translate(x+index,y+index)] == player:
                        if i in moves:
                            moves[i].append('LR')
                        else:
                            moves[i] = ['LR']
                        break
                    if board[translate(x+index, y+index)] == 0: # invalid
                        break
                    index += 1
    return moves

# Prints a visualization of the board for humans to understand
def visualizeBoard(board):
    for i in range(nn.BOARDDIM):
        temp  = board[i*nn.BOARDDIM:(i+1)*nn.BOARDDIM]
        for j in range(nn.BOARDDIM):
            if temp[j] == 1:
                temp[j] = 'X'
            elif temp[j] == -1:
                temp[j] = 'O'
            else:
                temp[j] = ' '
        print(temp)

# Place a piece at a given location on the board, then return the board
# moves gives all directions where tiles need to be flipped
def placePiece(player, board, position, moves):
    board[position] = player
    x = position % nn.BOARDDIM
    y = position // nn.BOARDDIM
            
    # upper left
    if 'UL' in moves:
        index = 1
        while x-index >= 0 and y-index >= 0:
            if board[translate(x-index,y-index)] == player:
                break
            else:
                board[translate(x-index,y-index)] = player
            index += 1
                    
    # upper
    if 'UP' in moves:
        index = 1
        while y-index >= 0:
            if board[translate(x,y-index)] == player:
                break
            else:
                board[translate(x,y-index)] = player
            index += 1
                    
    # upper right
    if 'UR' in moves:
        index = 1
        while x+index < nn.BOARDDIM and y-index >= 0:
            if board[translate(x+index,y-index)] == player:
                break
            else:
                board[translate(x+index,y-index)] = player
            index += 1
                    
    # left
    if 'LEFT' in moves:
        index = 1
        while x-index >= 0:
            if board[translate(x-index,y)] == player:
                break
            else:
                board[translate(x-index, y)] = player
            index += 1
            
    # right
    if 'RIGHT' in moves:
        index = 1
        while x+index < nn.BOARDDIM:
            if board[translate(x+index,y)] == player:
                break
            else:
                board[translate(x+index, y)] = player
            index += 1
            
    # lower left
    if 'LL' in moves:
        index = 1
        while x-index >= 0 and y+index < nn.BOARDDIM:
            if board[translate(x-index,y+index)] == player:
                break
            else:
                board[translate(x-index, y+index)] = player
            index += 1
            
    # lower
    if 'LOW' in moves:
        index = 1
        while y+index <= nn.BOARDDIM:
            if board[translate(x,y+index)] == player:
                break
            else:
                board[translate(x, y+index)] = player
            index += 1

    # lower right
    if 'LR' in moves:
        index = 1
        while x+index < nn.BOARDDIM and y+index < nn.BOARDDIM:
            if board[translate(x+index,y+index)] == player:
                break
            else:
                board[translate(x+index, y+index)] = player
            index += 1
    return board