import foodsurvivor as nn
import random as rand
import numpy as np
import functions as func

class Survivor(object):
    def __init__(self):
        self.weights1 = np.array([[nn.WEIGHTFACTOR*(rand.random()-0.5)
                                   for i in range(nn.INPUTSIZE+1)]
                                    for j in range(nn.HIDDENSIZE)])
        self.weights2 = np.array([[nn.WEIGHTFACTOR*(rand.random()-0.5)
                                   for i in range(nn.HIDDENSIZE+1)]
                                    for j in range(nn.OUTPUTSIZE)])

    # Performs matrix multiplication to perform the forward pass
    def forwardpass(self, survLoc, foodLoc):
        known = np.array([survLoc[0]/nn.XSIZE,survLoc[1]/nn.YSIZE,
                          foodLoc[0]/nn.XSIZE,foodLoc[1]/nn.YSIZE,1])
        # hin =  the inputs times the weights matrix
        hin = np.matmul(self.weights1,known)
        # normalize the values
        hout = np.array([func.sigmoid(x) for x in hin])
        hout = np.append(hout,1)
        # outin = outputs of hidden layer times the weights matrix
        outin = np.matmul(self.weights2,hout)
        # normalize
        outout = [func.sigmoid(x) for x in outin]
        # closer to 1 or 0 -> move in that direction
        outout = [outout[0], 1-outout[0], outout[1], 1-outout[1]]
        return np.argmax(outout)
    
    # Create an asexually reproduced child of itself with mutations
    def createChild(self):
        child = Survivor()
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
    
    # Performs a run of the simulation until the survivor dies, then returns
    # the fitness.
    def runSim(self, printMovement = False):
        fitness = 0
        survivorLoc = [nn.XSIZE//2, nn.YSIZE//2]
        foodLoc = func.generateFood(survivorLoc)
        health = nn.INITIALFOOD
        while health >= 0: 
            move = self.forwardpass(survivorLoc, foodLoc)
            if move == 0: # RIGHT
                survivorLoc[0] = (survivorLoc[0]+1)%nn.XSIZE
            elif move == 1: # LEFT
                survivorLoc[0] = (survivorLoc[0]-1)%nn.XSIZE
            elif move == 2: # UP
                survivorLoc[1] = (survivorLoc[1]+1)%nn.YSIZE
            elif move == 3: # DOWN
                survivorLoc[1] = (survivorLoc[1]-1)%nn.YSIZE
                
            if survivorLoc == foodLoc: # found some food!
                health += nn.FOODBONUS
                foodLoc = func.generateFood(survivorLoc)
                fitness += 1
            health -= 1
            if printMovement: # option to print the locations of everything
                print("Survivor: "+str(survivorLoc)+" Food: "+str(foodLoc))
        # fitness = number of food + 1-(distance to next food)/((X+Y)/2)
        return fitness + (1-func.distance(survivorLoc, foodLoc)/
                          ((nn.XSIZE+nn.YSIZE)/2))