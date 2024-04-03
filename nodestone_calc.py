import pandas as pd
import numpy as np
from collections import Counter
import itertools
from copy import deepcopy
import sys

print("Reading ", sys.argv[1])
df = pd.read_csv(sys.argv[1])

labels = list(set(df.to_numpy().flatten()))
arrays = {label: [] for label in labels}


### PARAMETERS TO SET ###
specify_target = True
print("Finding solution for", sys.argv[2], "occurrences of each skill")
num_desired = int(sys.argv[2])

if specify_target:
    """target = {
        "strike": 3,
        "dragon": 3,
        "deaths": 3,
        "shaft": 2,
        "falling": 2,
        "scattering": 2,
        "chain": 2,
        "phantom": 2
    }"""

    target = {
        k: 1 for k in ['flurry', 'resonate', 'sweep', 'death', 'rush', 'blitz']
    }

    labels = [x for x in target.keys()]
else:
    target = {labels[i]: num_desired for i in range(len(labels))}
    
init_count = {labels[i]: 1 for i in range(len(labels))}

for i, row in df.iterrows():
    arr_idx = row["1"]

    if (row["2"], row["3"]) in arrays[arr_idx] or (row["3"], row["2"]) in arrays[arr_idx]:
        continue
    
    arrays[arr_idx].append((row["2"], row["3"]))




solutions = []
solution_counts = []
for arr in itertools.product(*[arrays[labels[i]] for i in range(len(labels))]):         
    counts = deepcopy(init_count)
    print("Printing counts")
    print(counts)
    for x in [*arr]:
        counts[x[0]] += 1
        counts[x[1]] += 1
    
    
    res = {label: counts[label] - target[label] for label in labels}
    if all(v >= 0 for v in res.values()):
        solutions.append([*arr])
        solution_counts.append(counts)

print(len(solutions))
print({labels[i]: solutions[0][i] for i in range(len(labels))})

def check_redundant_solution(solution_dict, solution_counts, target):
    for k in solution_dict.keys():
        counts = deepcopy(solution_counts)
        counts[k] -= 1
        counts[solution_dict[k][0]] -= 1
        counts[solution_dict[k][1]] -= 1
        
        res = {label: counts[label] - target[label] for label in counts.keys()}
        if all(v >= 0 for v in res.values()):
            del solution_dict[k]
            print(k)
            return True, solution_dict, counts, k
        
    return False, solution_dict, solution_counts, None

"""target = {labels[i]: num_desired-1 for i in range(len(labels))}"""
check_redundant_solution({labels[i]: solutions[0][i] for i in range(len(labels))}, solution_counts[0], target)

"""for i, solution in enumerate(solutions):
    solution_dict = {labels[i]: solutions[0][i] for i in range(len(labels))}
    
    n = 0

    found = True
    sol_dict = deepcopy(solution_dict)
    sol_count = deepcopy(solution_counts[i])
    
    remove_nodes = []
    while found:
        found, sol_dict, sol_count, k = check_redundant_solution(sol_dict, sol_count, target)
        remove_nodes.append(k)

        if found:
            n += 1
    
    if n >= 2:
        print(f"Removed {n} nodes, full solution: {solution_dict},  remove nodes: {remove_nodes}")"""
        
    


