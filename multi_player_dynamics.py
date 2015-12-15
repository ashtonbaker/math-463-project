import random
import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
import csv

def d(p, q, f):
    M = [   [-1 + p[0]*q[0], -1 + p[0], -1 + q[0], f[0]],
            [     p[1]*q[2], -1 + p[1],      q[2], f[1]],
            [     p[2]*q[1],      p[2], -1 + q[1], f[2]],
            [     p[3]*q[3],      p[3],      q[3], f[3]]];

    return np.linalg.det(M)

def get_score(p, q):
    T = 5
    R = 3
    P = 1
    S = 0
    
    Sx = [R, S, T, P]
    Sy = [R, T, S, P]
    
    M =    [[p[0]*q[0], p[0]*(1 - q[0]), (1 - p[0])*q[0], (1 - p[0])*(1 - q[0])],
            [p[1]*q[2], p[1]*(1 - q[2]), (1 - p[1])*q[2], (1 - p[1])*(1 - q[2])],
            [p[2]*q[1], p[2]*(1 - q[1]), (1 - p[2])*q[1], (1 - p[2])*(1 - q[1])],
            [p[3]*q[3], p[3]*(1 - q[2]), (1 - p[3])*q[3], (1 - p[3])*(1 - q[3])]]
    
    sx = d(p, q, Sx) / d(p, q, [1, 1, 1, 1])
    sy = d(p, q, Sy) / d(p, q, [1, 1, 1, 1])
    
    return sx

def main():
    # Input the strategies you would like to simulate, along with the initial populations,
    # and number of trials.
    
    p = [0, 0, 0, 0] # Always defect
    q = [1, 0, 1, 0] # Tit-for-Tat
    r = [1, 1, 1, 1] # Always cooperate
    
    initial_p = 0.33
    initial_q = 0.33
    initial_r = 0.33
    
    number_of_trials = 400



    # Here, we organize the inputs into a ``players'' vector and an ``initial populations''
    # vector. Be sure to add any extra players here if you want to simulate more than 3 players.
    players = [p, q, r]
    initial_populations = [initial_p, initial_q, initial_r]
    
    # Define an error, and apply it to the strategies. This really only works for strategies
    # containing 0's and 1's, otherwise you might have to calculate the error by hand
    error = 0.000001
    players = [[abs(x - error) for x in a] for a in players]
    
    
    # s is going to be our matrix of scores, so that s[i][j] gives the expected score for strategy
    # i against strategy j. The following lines compute s for any number of players, so this code
    # never needs to be modified.
    s = []

    for a in players:
        newline = []
        for b in players:
            newline.append(get_score(a, b))
        s.append(newline)
        
    
    # x will hold our populations at each generation. We initialize it with the initial populations
    x = [initial_populations]
    
    
    # Simulate the system. For every step, we use x[-1][i] as the population of strategy i from
    # the previous step.
    for i in xrange(number_of_trials):
        totals = [] # This will hold the total scores for each strategy this generation
        
        for i in range(len(x[-1])):
            # Calculate the expected value of the total scores amassed by strategy i.
            i_score = x[-1][i] * sum( [x[-1][j]*s[i][j] for j in range(len(s[i]))] )
            totals.append(i_score)

        # Calculate the proportional scores, and don't let any individual population drop below
        # 0.01% of the total population. These proportional scores become the new populations,
        # so we directly add them to the list of results.
        x.append([max(totals[i]/sum(totals), 0.0001) for i in range(len(totals))])
    
    
    
    # Graph the results!
    plt.figure(figsize=(8, 6))

    for i in range(len(x[-1])):
        plt.plot(range(len(x)), [row[i] for row in x])
        
    plt.ylim([0.0, 1.0])
    plt.xlabel('Generation')
    plt.ylabel('Portion of population')
    plt.ylim([0.0, 1.0])
    plt.show()

    print x[-1]
    
main()
