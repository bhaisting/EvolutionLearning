import OthelloGamer as gamer
import random as rand

# CHANGEABLE VARIABLES
GENSIZE = 256
INPUTSIZE = 64
HIDDENSIZE = 128
OUTPUTSIZE = 64
MUTATIONRATE = 0.03
WEIGHTFACTOR = 1
GENERATIONCOUNT = 100
BOARDSIZE = 64
BOARDDIM = 8
GROUPSIZE = 8
TESTSIZE = 4

def main():
    generation = []
    for i in range(GENSIZE):
        generation.append([gamer.OthelloGamer(),0])
    for iterations in range(GENERATIONCOUNT):
        best = []
        print("Generation: "+str(iterations))
        nextGen = []
        # Split the generation into groups and play each player against
        # each other player in the group, then sort the group by their record
        # and kill the worse half
        for i in range(GENSIZE//GROUPSIZE):
            for j in range(i*GROUPSIZE, (i+1)*GROUPSIZE):
                for k in range(j+1, (i+1)*GROUPSIZE):
                    result = generation[j][0].runSim(generation[k][0])
                    if result > 0:
                        generation[j][1] += 1
                    elif result < 0:
                        generation[k][1] += 1
                    else:
                        generation[j][1] += 0.5
                        generation[k][1] += 0.5
            temp = generation[i*GROUPSIZE : (i+1)*GROUPSIZE]
            temp.sort(reverse = True, key = lambda i: i[1])
            best.append(temp[0][0])
            temp = temp[:GROUPSIZE//2]
            nextGen += temp
        generation = nextGen
        
        # Run best of each group against randomly generated untrained players
        winCount = 0
        lossCount = 0
        tieCount = 0
        gamesPlayed = 0
        for i in best:
            for j in range(TESTSIZE):
                gamesPlayed += 1
                result = i.runSim(gamer.OthelloGamer())
                if result > 0:
                    winCount += 1
                elif result < 0:
                    lossCount += 1
                else:
                    tieCount += 1
        print("Running best of generation against random newbies")
        print("Games Played: "+str(gamesPlayed))
        print("Total Wins: "+str(winCount))
        print("Total Ties: "+str(tieCount))
        print("Total Losses: "+str(lossCount))
        
        for i in range(GENSIZE//2): # Create the next generation and reset
            generation[i][1] = 0
            generation.append([generation[i][0].createChild(), 0])    
        rand.shuffle(generation)

    # Simulation is done, find the best player and print (NOTE: this can take 
    # a long time because every player plays every other player)
    for i in range(GENSIZE):
        for j in range(i+1,GENSIZE):
            result = generation[i][0].runSim(generation[j][0])
            if result > 0:
                generation[i][1] += 1
            elif result < 0:
                generation[j][1] += 1
            else:
                generation[i][1] += 0.5
                generation[j][1] += 0.5
    generation.sort(reverse = True, key = lambda i: i[1])
    print("You are now playing the best Othello player the system produced:")
    print(generation[0][0].playGame())

if __name__ == "__main__":
    main()
