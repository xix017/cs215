#
# List of distinct two-digit values.
# Where will 84 be located in the sorted version?
#
import random

L = [31, 45, 91, 51, 66, 82, 28, 33, 11, 89, 27, 36]

def partition(L, v):
    smaller = []
    bigger = []
    for val in L:
        if val < v: smaller += [val]
        if val > v: bigger += [val]
    return (smaller, [v], bigger)

print partition(L, 84)
# >>>[31, 45, 51, 66, 82, 28, 33, 11, 27, 36, 84, 91, 89]

def top_k(L, k):
    v = L[random.randrange(len(L))] # select a random item in L
    (left, middle, right) = partition(L, v)
    # middle used below (in place of [v]) for clarity
    if len(left) == k:   return left
    if len(left)+1 == k: return left + middle
    if len(left) > k:    return top_k(left, k)
    return left + middle + top_k(right, k - len(left) - len(middle))

print top_k(L, 5)
# >>> [31, 28, 33, 11, 27]
# list order may vary due to random selection of v