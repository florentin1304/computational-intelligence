import numpy as np
import random

def one_bit_flip(ind, size=1, mutation_probability=1):
    if random.random() < mutation_probability:
        index = np.random.choice(list(range(len(ind))), size=size, replace=False)
        ind[index] = 1 - ind[index]
    return ind

def three_bit_flip(ind, size=3, mutation_probability=1):
    if random.random() < mutation_probability:
        index = np.random.choice(list(range(len(ind))), size=size, replace=False)
        ind[index] = 1 - ind[index]
    return ind