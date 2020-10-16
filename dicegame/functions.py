from math import isnan
from math import e

# Returns the sigmoid function 
def sigmoid(x):
    ret = 1/(1+e**(-x))
    if isnan(ret):
        return 0
    return ret