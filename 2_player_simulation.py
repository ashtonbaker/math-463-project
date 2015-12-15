import random
import math
import numpy as np
import matplotlib.pyplot as plt

def play(player, previous_play):
    # Given a player's strategy, and the previous play, either return a 'C' or a 'D'.
    # This is done by generating a random number, and comparing it to the player's conditional
    # probability of cooperating given the previous play.
    probability_of_cooperating = player[previous_play]
    if random.random() < probability_of_cooperating:
        return 'C'
    else:
        return 'D'

def firstplay(p1, p2):
    # Return a tuple of 'C' and 'D', according to each player's probability of cooperating in the
    # initial round. This is done by generating a random number in [0, 1], and comparing it to each
    # player's conditional probability of cooperating on the initial play.
    if random.random() < p1['initial']:
        p1_move = 'C'
    else:
        p1_move = 'D'

    if random.random() < p2['initial']:
        p2_move = 'C'
    else:
        p2_move = 'D'

    return (p1_move, p2_move)

# Define how many rounds to simulate play
number_of_plays = 2000

# Define the possible scores for the game
T = 5 # Temptation to defect (reward for DC). Default = 5
R = 3 # Reward for mutual cooperation (CC). Default = 3
P = 1 # Punishment for mutual defection (DD). Default = 1
S = 0 # Sucker's payoff (reward for CD). Default = 0

# Create a scoring matrix as a dictionary that will give the scores for each player
# given the plays that they made.
scoring_matrix = {  ('C', 'C'): [R, R],
                    ('C', 'D'): [S, T],
                    ('D', 'C'): [T, S],
                    ('D', 'D'): [P, P]}

# Define the two strategies, p and q in terms of probability to cooperate given that the
# previous rounds were cc, cd, dc, or dd, seen from their perspective.
p = [0.5, 0.5, 0.5, 0.5]
q = [0.5, 0.5, 0.5, 0.5]


# Define the two players using dictionaries. Given a tuple representing the previous scores,
# the players will output their probability to cooperate.
player_1 = {'initial': 1,
            ('C', 'C'): p[0],
            ('C', 'D'): p[1],
            ('D', 'C'): p[2],
            ('D', 'D'): p[3]}

player_2 = {'initial': 1,
            ('C', 'C'): q[0],
            ('C', 'D'): q[2],
            ('D', 'C'): q[1],
            ('D', 'D'): q[3]}

plays = [firstplay(player_1, player_2)] # Initialize plays according to initial probs
scores = [ scoring_matrix[plays[0]] ] # Initialize the score list accordingly


# Continue play for the specified duration. At each step, calculate a play for each player
# using the previous play, then calculate the score for each player based on that. Then,
# append the scores with the cumulative scores up to this point.
for i in xrange(number_of_plays):
    current_play = (play(player_1, plays[-1]), play(player_2, plays[-1]))
    current_score = scoring_matrix[current_play]

    plays.append(current_play)
    scores.append([x + y for x, y in zip(current_score, scores[-1])])


# Normalize the scores to give the cumulatave average points-per-round for each round.
y1 = [scores[i][0]/float(i + 1) for i in range(len(scores))]
y2 = [scores[i][1]/float(i + 1) for i in range(len(scores))]


# Plot the points-per-round for each player against the round numbers.
plt.figure(figsize=(8, 6))
plt.plot(range(len(y1)), y1)
plt.plot(range(len(y2)), y2)
plt.xlabel('Plays')
plt.ylabel('Points per play')
plt.show()

# Print the final scores, so that we know what the system is approaching.
print scores[-1][0]/float(len(scores)), scores[-1][1]/float(len(scores))

