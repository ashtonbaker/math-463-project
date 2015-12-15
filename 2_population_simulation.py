import random
import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
import csv


def d(p, q, f):
    # This is the determinant defined in the paper for an arbitrary vector f.
    M = [   [-1 + p[0]*q[0], -1 + p[0], -1 + q[0], f[0]],
            [     p[1]*q[2], -1 + p[1],      q[2], f[1]],
            [     p[2]*q[1],      p[2], -1 + q[1], f[2]],
            [     p[3]*q[3],      p[3],      q[3], f[3]]];

    return np.linalg.det(M)

def get_score(p, q):
    # This gives the expected score for p in a game of p vs q. This method is equivalent to the 
    # equations given by the Press/Dyson paper, and so some pairs will return (nan, nan) if there
    # is no error introduced.
    
    T = 5 # Temptation to defect (reward for DC). Default = 5
    R = 3 # Reward for mutual cooperation (CC). Default = 3
    P = 1 # Punishment for mutual defection (DD). Default = 1
    S = 0 # Sucker's payoff (reward for CD). Default = 0
    
    # Score matrices for both players
    Sx = [R, S, T, P]
    Sy = [R, T, S, P]
    
    # Transition matrix as defined in the text
    M =    [[p[0]*q[0], p[0]*(1 - q[0]), (1 - p[0])*q[0], (1 - p[0])*(1 - q[0])],
            [p[1]*q[2], p[1]*(1 - q[2]), (1 - p[1])*q[2], (1 - p[1])*(1 - q[2])],
            [p[2]*q[1], p[2]*(1 - q[1]), (1 - p[2])*q[1], (1 - p[2])*(1 - q[1])],
            [p[3]*q[3], p[3]*(1 - q[2]), (1 - p[3])*q[3], (1 - p[3])*(1 - q[3])]]
    
    # Expected scores for each player
    sx = d(p, q, Sx) / d(p, q, [1, 1, 1, 1])
    sy = d(p, q, Sy) / d(p, q, [1, 1, 1, 1])
    
    # Return the score for the first player.
    return sx


# We're going to make an array where results[i][j] is the expected long-term population of
# strategy i against strategy j, where the strategies are those composed of 0's and 1's, in
# lexicographical order. That is, strategy 0 is (0, 0, 0, 0), strategy 1 is (0, 0, 0, 1),
# strategy 2 is (0, 0, 1, 0), and so on.

results = []

# We will actually use numbers very close to 0 and very close to 1, to avoid divide-by-zero errors.
for p in itertools.product([0.0000001, 0.9999999], repeat=4):
    newline = []
    for q in itertools.product([0.0000001, 0.9999999], repeat=4):

        # m[i][j] is the expected score for strategy i against strategy j.
        m = [[get_score(p, p), get_score(p, q)], [get_score(q, p), get_score(q, q)]]
        
        # x and y will hold the populations of p and q in each generation. We initialize them
        # with p as the minority.
        x = [0.01]
        y = [0.99]
        
        # Simulate play between the two populations
        for i in xrange(10000):
            x_total = x[-1] * (x[-1] * m[0][0] + y[-1] * m[0][1])
            y_total = y[-1] * (y[-1] * m[1][1] + x[-1] * m[1][0])
            
            x.append( x_total / (x_total + y_total) )
            y.append( y_total / (x_total + y_total) )
        
        newline.append(x[-1])
    results.append(newline)

# Write the results to a csv file
with open("2_population_simulation_output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(results)
