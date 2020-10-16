import dicegame as nn
import random as rand
import numpy as np
import functions as func

class Gamer(object):
    def __init__(self):
        self.weights1 = np.array([[nn.WEIGHTFACTOR*(rand.random()-0.5)
                                   for i in range(nn.INPUTSIZE+1)]
                                    for j in range(nn.HIDDENSIZE)])
        self.weights2 = np.array([[nn.WEIGHTFACTOR*(rand.random()-0.5)
                                   for i in range(nn.HIDDENSIZE+1)]
                                    for j in range(nn.OUTPUTSIZE)])

    # Performs matrix multiplication to perform the forward pass
    def forwardpass(self, maxroll, potential, total):
        known = np.array([maxroll, potential, total, 1])
        # hin =  the inputs times the weights matrix
        hin = np.matmul(self.weights1,known)
        # normalize the values
        hout = np.array([func.sigmoid(x) for x in hin])
        hout = np.append(hout,1)
        # outin = outputs of hidden layer times the weights matrix
        outin = np.matmul(self.weights2,hout)
        # normalize
        outout = [func.sigmoid(x) for x in outin]
        # round the output, 1 = roll again, 0 = stop
        return round(outout[0])
    
    # Create an asexually reproduced child of itself with mutations
    def createChild(self):
        child = Gamer()
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
    
    # Performs a run of the simulation until the gambler wins or runs out of
    # time
    def runSim(self, printMovement = False):
        fitness = nn.GOALAMOUNT
        total = 0
        
        while total < nn.GOALAMOUNT:
            if fitness == 0:
                return 0;
            maxroll = rand.randint(1,nn.MAXDICEROLL)
            potential = maxroll
            if printMovement: # option to print the locations of everything
                    print("First roll: "+str(maxroll))
                    
            # Go until the neural net tells us to stop or roll < maxroll
            while(self.forwardpass(maxroll/nn.MAXDICEROLL, 
                                   potential/nn.GOALAMOUNT,
                                   total/nn.GOALAMOUNT) == 1):
                roll = rand.randint(1,nn.MAXDICEROLL)
                if printMovement: # option to print the locations of everything
                    print("Roll: "+str(roll)+" Maxroll: "+str(maxroll))
                if roll < maxroll: # dump potential and exit round
                    potential = 0
                    break
                maxroll = max(roll, maxroll)
                potential += roll


            fitness -= 1
            total += potential
            if printMovement: # option to print the locations of everything
                print("Total: "+str(total)+" Points gained: "+str(potential))

        return fitness