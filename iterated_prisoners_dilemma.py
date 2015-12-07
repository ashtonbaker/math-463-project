import random
import math

def play(player, previous_play):
    probability_of_cooperating = player[previous_play]
    if random.random() < probability_of_cooperating:
        return 'C'
    else:
        return 'D'


random.seed()

scoring_matrix = {  ('C', 'C'): [200, 200],
                    ('C', 'D'): [-100, 300],
                    ('D', 'C'): [300, -100],
                    ('D', 'D'): [0, 0]}

# Always Cooperate
player_1 = {('C', 'C'): 1,
            ('C', 'D'): 1,
            ('D', 'C'): 1,
            ('D', 'D'): 1}

# Always Defect
player_2 = {('C', 'C'): 0,
            ('C', 'D'): 0,
            ('D', 'C'): 0,
            ('D', 'D'): 0}

print player_1
print player_2

plays = [('C', 'C')]
scores = [ scoring_matrix[plays[0]] ]

for i in xrange(1000):
    current_play = (play(player_1, plays[-1]), play(player_2, plays[-1]))
    current_score = scoring_matrix[current_play]

    plays.append(current_play)
    scores.append([x + y for x, y in zip(current_score, scores[-1])])

for x in scores:
    print "%i, %i" % (x[0], x[1])
