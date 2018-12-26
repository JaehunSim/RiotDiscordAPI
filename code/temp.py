# -*- coding: utf-8 -*-

#partition list a into k partitions
def partition_list(a, k):
    if k <= 1: return [a]
    if k >= len(a): return [[x] for x in a]
    partition_between = [(i+1)*len(a) // k for i in range(k-1)]
    average_height = float(sum(a))/k
    best_score = None
    best_partitions = None
    count = 0

    while True:
        starts = [0] + partition_between
        ends = partition_between + [len(a)]
        partitions = [a[starts[i]:ends[i]] for i in range(k)]
        heights = list(map(sum, partitions))

        abs_height_diffs = list(map(lambda x: abs(average_height - x), heights))
        worst_partition_index = abs_height_diffs.index(max(abs_height_diffs))
        worst_height_diff = average_height - heights[worst_partition_index]

        if best_score is None or abs(worst_height_diff) < best_score:
            best_score = abs(worst_height_diff)
            best_partitions = partitions
            no_improvements_count = 0
        else:
            no_improvements_count += 1

        if worst_height_diff == 0 or no_improvements_count > 5 or count > 100:
            return best_partitions
        count += 1

        move = -1 if worst_height_diff < 0 else 1
        bound_to_move = 0 if worst_partition_index == 0\
                        else k-2 if worst_partition_index == k-1\
                        else worst_partition_index-1 if (worst_height_diff < 0) ^ (heights[worst_partition_index-1] > heights[worst_partition_index+1])\
                        else worst_partition_index
        direction = -1 if bound_to_move < worst_partition_index else 1
        partition_between[bound_to_move] += move * direction

def print_best_partition(a, k):
    print('Partitioning {0} into {1} partitions'.format(a, k))
    p = partition_list(a, k)
    print('The best partitioning is {0}\n    With heights {1}\n'.format(p, list(map(sum, p))))

#tests
a = [1, 6, 2, 3, 4, 1, 7, 6, 4]
print_best_partition(a, 1)
print_best_partition(a, 2) 
print_best_partition(a, 3)
print_best_partition(a, 4)
print_best_partition(a, 5)

b = [1, 10, 10, 1]
print_best_partition(b, 2)

import random
c = [random.randint(0,20) for x in range(100)]
print_best_partition(c, 10)

d = [95, 15, 75, 25, 85, 5]
print_best_partition(d, 3)