import numpy as np
import random
from copy import deepcopy 

def uniform_crossover(ind1, ind2):
    new_ind = np.ndarray(shape=ind1.shape)
    for i in range(len(ind1)):
        gene_giver = random.choice([ind1, ind2])
        new_ind[i] = gene_giver[i]
    return new_ind

def one_cut_crossover(ind1, ind2):
    index = np.random.randint(1, len(ind1)-1)
    new_ind = deepcopy(ind1)
    new_ind[index:] = ind2[index:]
    return new_ind

def two_cuts_crossover(ind1, ind2):
    idx_1 = np.random.randint(1, len(ind1) - 2)
    idx_2 = np.random.randint(idx_1 + 1, len(ind1) - 1)
    return np.concatenate((ind1[idx_1:idx_2], ind2[:idx_1], ind1[idx_2:]))

def three_cuts_crossover(ind1, ind2):
    idx_1 = np.random.randint(1, len(ind1) / 2)
    idx_3 = np.random.randint(idx_1 + 1, len(ind1) - 1)
    idx_2 = np.random.randint(idx_1, idx_3)
    return np.concatenate((ind2[:idx_1], ind1[idx_1:idx_2], ind2[idx_2:idx_3], ind1[idx_3:]))        

def random_xover(ind1, ind2):
    flag = random.random()
    if flag < 0.25:
        return one_cut_crossover(ind1, ind2)
    elif 0.25 <= flag < 0.50:
        return uniform_crossover(ind1, ind2)
    elif 0.50 <= flag < 0.75:
        return two_cuts_crossover(ind1, ind2)
    elif 0.75 <= flag < 1.00:
        return three_cuts_crossover(ind1, ind2)