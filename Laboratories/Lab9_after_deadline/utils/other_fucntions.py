import numpy as np

def generate_random_individual(length):
    ind = np.random.choice([0, 1], size=length)
    return ind

def get_parents_diversity(p1, p2):
    return np.sum( np.abs( p1-p2 ) )