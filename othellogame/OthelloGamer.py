import othellogame as nn
import random as rand
import numpy as np
import functions as func

class OthelloGamer(object):
    def __init__(self):
        self.weights1 = np.array([[nn.WEIGHTFACTOR*(rand.random()-0.5)
                                   for i in range(nn.INPUTSIZE+1)]
                                    for j in range(nn.HIDDENSIZE)])
        self.weights2 = np.array([[nn.WEIGHTFACTOR*(rand.random()-0.5)
                                   for i in range(nn.HIDDENSIZE+1)]
                                    for j in range(nn.OUTPUTSIZE)])

    # Performs matrix multiplication to perform the forward pass
    def forwardpass(self, board, player):
        known = np.array(board)
        if player == -1:
            for i in range(nn.BOARDSIZE):
                known[i] = 0-known[i]
        known = np.append(known, 1)
        # hin =  the inputs times the weights matrix
        hin = np.matmul(self.weights1,known)
        # normalize the values
        hout = np.array([func.sigmoid(x) for x in hin])
        hout = np.append(hout,1)
        # outin = outputs of hidden layer times the weights matrix
        outin = np.matmul(self.weights2,hout)
        # normalize
        outout = [func.sigmoid(x) for x in outin]
        return outout
    
    # Create an asexually reproduced child of itself with mutations
    def createChild(self):
        child = OthelloGamer()
        for i in range(nn.HIDDENSIZE):
            for j in range(nn.INPUTSIZE+1): 
                num = rand.random()
                if num < nn.MUTATIONRATE/2: # Mutation 1: Create new weight
                    child.weights1[i][j] = nn.WEIGHTFACTOR*(rand.random()-0.5)
                elif num < nn.MUTATIONRATE: # Mutation 2: Add to parent weight
                    child.weights1[i][j] = self.weights1[i][j] + \
                                            nn.WEIGHTFACTOR*(rand.random()-0.5)
                else:
                    child.weights1[i][j] = self.weights1[i][j]
        for i in range(nn.OUTPUTSIZE):
            for j in range(nn.HIDDENSIZE+1):
                num = rand.random()
                if num < nn.MUTATIONRATE/2: # Mutation 1: Create new weight
                    child.weights2[i][j] = nn.WEIGHTFACTOR*(rand.random()-0.5)
                elif num < nn.MUTATIONRATE: # Mutation 2: Add to parent weight
                    child.weights2[i][j] = self.weights2[i][j] + \
                                            nn.WEIGHTFACTOR*(rand.random()-0.5)
                else:
                    child.weights2[i][j] = self.weights2[i][j]
        return child
    
    # Performs a game of othello between two systems
    def runSim(self, player2, printMovement = False):
        board = func.generateBoard()
        totalPieces = nn.BOARDSIZE-4
        currPlayer = (2*rand.randint(0,1))-1
        
        while totalPieces != 0: # Go until there are no moves or no pieces
            moves = func.possibleMoves(currPlayer, board)
            if not moves: # No moves available for the current player, switch
                currPlayer = 0 - currPlayer
                moves = func.possibleMoves(currPlayer, board)
                if not moves: # No moves for either player, end the game
                    break
            
            # Get the list of decisions from the playing network
            decisions = {}
            if currPlayer == 1:
                decisions = self.forwardpass(board, currPlayer)
            else:
                decisions = player2.forwardpass(board, currPlayer)
            
            # Find the highest prioritized move that is valid
            bestchoice = np.argmax(decisions)
            while bestchoice not in moves:
                decisions[bestchoice] = 0
                bestchoice = np.argmax(decisions)

            # Update the board, current player, and total pieces
            board = func.placePiece(currPlayer,board,bestchoice,moves[bestchoice])
            currPlayer = 0 - currPlayer
            totalPieces -= 1
        return sum(board)
    
    # Play a game of Othello against the network.
    def playGame(self):
        board = func.generateBoard()
        totalPieces = nn.BOARDSIZE-4
        currPlayer = 1
        func.visualizeBoard(board)
        
        while totalPieces != 0:
            # Check that there are valid moves and switch if necessary
            moves = func.possibleMoves(currPlayer, board)
            if not moves:
                currPlayer = 0 - currPlayer
                moves = func.possibleMoves(currPlayer, board)
                if not moves:
                    break
                
            choice = -1
            if currPlayer == 1: # Human playing
                print("Your move! (You are X)")
                while choice not in moves:
                    x = int(input("Input x (Upper left is (0,0)): "))
                    y = int(input("Input y (Upper left is (0,0)): "))
                    choice = func.translate(x,y)
            else: # Follow the procedure to produce network output
                print("Opponent's move:")
                decisions = self.forwardpass(board, currPlayer)
                bestchoice = np.argmax(decisions)
                while bestchoice not in moves:
                    decisions[bestchoice] = 0
                    bestchoice = np.argmax(decisions)
                choice = bestchoice
            
            # Update board, current player, and number of pieces. Then print
            # the board
            board = func.placePiece(currPlayer,board,choice,moves[choice])
            func.visualizeBoard(board)
            currPlayer = 0 - currPlayer
            totalPieces -= 1
                    
        return sum(board)
        #func.visualizeBoard()