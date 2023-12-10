import random
import numpy as np

### WHEN TO SWAP
def fixed_generations(generation, every):
    return (generation + 1) % every == 0
