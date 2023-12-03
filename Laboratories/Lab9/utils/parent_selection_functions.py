
import random
import numpy as np

def roulette(parents, parents_evals):
    if (max(parents_evals)-min(parents_evals)) > 1e-5:
        probabilities = [(score-min(parents_evals)) / (max(parents_evals)-min(parents_evals)) for score in parents_evals]
    else:
        probabilities = [1 for score in parents_evals]
    probabilities = np.array(probabilities)/sum(probabilities)
    p1 = random.choices(parents, k=1, weights=probabilities)[0]
    p2 = random.choices(parents, k=1, weights=probabilities)[0]
            
    return p1, p2

# tournament method to select parents
def tournament(parents, parents_evals, n = 2):
    participants = n*2

    parents_indexes = np.random.choice(list(range(len(parents))), replace=False, size=participants)
    parents_sample = [parents[index] for index in parents_indexes]
    parents_evals_sample = [parents_evals[index] for index in parents_indexes]

    # generate two groups of n parents
    group1 = parents_sample[:n]
    group2 = parents_sample[n:]

    # select the best parent from each group
    p1 = group1[np.argmax(parents_evals_sample[:n])]
    p2 = group2[np.argmax(parents_evals_sample[n:])]

    return p1, p2

