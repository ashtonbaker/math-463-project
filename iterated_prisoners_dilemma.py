import random
import math

def play(player, previous_play):
    probability_of_cooperating = player[previous_play]
    if random.random() < probability_of_cooperating:
        return 'C'
    else:
        return 'D'

def firstplay(p1, p2):
    if random.random() < p1('initial'):
        p1_move = 'C'
    else:
        p1_move = 'D'

    if random.random() < p2('initial'):
        p2_move = 'C'
    else:
        p2_move = 'D'

    return (p1_move, p2_move)

random.seed()

scoring_matrix = {  ('C', 'C'): [3, 3],
                    ('C', 'D'): [0, 5],
                    ('D', 'C'): [5, 0],
                    ('D', 'D'): [1, 1]}

# Always Cooperate
player_1 = {'initial': 1,
            ('C', 'C'): 1,
            ('C', 'D'): 0,
            ('D', 'C'): 1,
            ('D', 'D'): 0}

# Always Defect
player_2 = {'initial': 0,
            ('C', 'C'): 1,
            ('C', 'D'): 1,
            ('D', 'C'): 0,
            ('D', 'D'): 0}

plays = [firstplay(player_1, player_2)] # Initialize according to initial probs
scores = [ scoring_matrix[plays[0]] ] # Initialize the score list accordingly

for i in xrange(10000):
    current_play = (play(player_1, plays[-1]), play(player_2, plays[-1]))
    current_score = scoring_matrix[current_play]

    plays.append(current_play)
    scores.append([x + y for x, y in zip(current_score, scores[-1])])

for i in range(len(scores)):
    print "%f, %f" % (scores[i][0]/float(i + 1), scores[i][1]/float(i + 1))
