import Gamer as gamer

# CHANGEABLE VARIABLES
GENSIZE = 500
MAXDICEROLL = 15
HIDDENSIZE = 6
INPUTSIZE = 3
OUTPUTSIZE = 1
GOALAMOUNT = 300
MUTATIONRATE = 0.03
WEIGHTFACTOR = 10
GENERATIONCOUNT = 200

def main():
    generation = []
    for i in range(GENSIZE):
        generation.append(gamer.Gamer())
    for iterations in range(GENERATIONCOUNT):
        count = 0
        for i in range(GENSIZE):
            generation[i] = (generation[i].runSim(),generation[i])
            count += generation[i][0]
        generation.sort(reverse = True, key = lambda i: i[0])
        
        # Stat tracking
        print("Generation: "+str(iterations))
        print("Best Fitness: "+str(round(generation[0][0],5)))
        print("Worst Fitness: "+str(round(generation[GENSIZE-1][0],5)))
        print("Median Fitness: "+str(round(generation[GENSIZE//2][0],5)))
        print("Average Fitness: "+str(round(count/GENSIZE,5))+"\n")
        
        # Kill the weaker half
        generation = generation[:(GENSIZE//2)]
        for i in range(GENSIZE//2): # Refill and reproduce the generation list
            generation[i] = (generation[i][1])
            generation.append(generation[i].createChild())
    # Simulation is done, print the best gambler's decision making
    for i in range(GENSIZE):
        generation[i] = (generation[i].runSim(),generation[i])
    generation.sort(reverse = True, key = lambda i: i[0])
    print("Best performing gambler:")
    generation[0][1].runSim(True)

if __name__ == "__main__":
    main()