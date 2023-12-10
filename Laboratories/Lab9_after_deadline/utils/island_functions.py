import random
import numpy as np

### HOW TO SWAP
def random_swap(islands):
    island_indices = list(range(len(islands)))
    random.shuffle(island_indices)  # Shuffle island indices to randomize swapping order

    for i in range(0, len(islands) - 1):
        island1_index, island2_index = island_indices[i], island_indices[i + 1]
        individual_index_island1 = random.randint(0, len(islands[island1_index]) - 1)
        individual_index_island2 = random.randint(0, len(islands[island2_index]) - 1)
        
        # Swap individuals between islands
        islands[island1_index][individual_index_island1], islands[island2_index][individual_index_island2] = (
            islands[island2_index][individual_index_island2],
            islands[island1_index][individual_index_island1],
        )

def ring_topology_migration(islands, migration_rate = 0.3):
    num_islands = len(islands)
    migration_count = int(migration_rate * len(islands[0]))
    
    for i in range(num_islands):
        sender_idx = i
        receiver_idx = (i + 1) % num_islands
        
        # Select individuals for migration
        migrants = islands[sender_idx][-migration_count:]
        
        # Exchange migrants
        islands[receiver_idx][:migration_count] = migrants

def fitness_based_migration(islands, fitness_values, migration_rate = 0.3):
    num_islands = len(islands)
    migration_count = int(migration_rate * len(islands[0]))
    
    # Sort populations by fitness
    sorted_populations = [x for _, x in sorted(zip(fitness_values, islands), key=lambda pair: pair[0])]
    
    for i in range(num_islands):
        sender_idx = i
        receiver_idx = (i + 1) % num_islands
        
        # Select individuals for migration based on fitness
        migrants = sorted_populations[sender_idx][-migration_count:]
        
        # Exchange migrants
        sorted_populations[receiver_idx][:migration_count] = migrants
        
    # Update original population order
    for i in range(num_islands):
        islands[i] = sorted_populations[i]


### WHEN TO SWAP
def fixed_generations(generation, every):
    return (generation + 1) % every == 0

def fitness_based(fitness_values, threshold = 0.1):
    means = np.array([np.mean(x) for x in fitness_values])
    means = np.reshape(means, (len(means), 1))
    diff_mat = means - means.transpose()
    return (diff_mat >= threshold).any()