from math import isnan
from math import e
import random as rand
import foodsurvivor as nn

# Returns the sigmoid function 
def sigmoid(x):
    ret = 1/(1+e**(-x))
    if isnan(ret):
        return 0
    return ret

# Returns the manhattan distance between two points
def distance(loc1,loc2):
    xval = min(abs(loc2[0]-loc1[0]), nn.XSIZE-abs(loc2[0]-loc1[0]))
    yval = min(abs(loc2[1]-loc1[1]), nn.YSIZE-abs(loc2[1]-loc1[1]))
    return xval + yval   

# Given the current location, returns a new food spot
def generateFood(loc):
    food = [rand.randint(0,nn.XSIZE-1),rand.randint(0,nn.YSIZE-1)]
    while (loc[0] == food[0] and loc[1] == food[1]):
        food = [rand.randint(0,nn.XSIZE-1),rand.randint(0,nn.YSIZE-1)]
    return food