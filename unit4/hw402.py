#
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the absolute value of the difference
# between each element in L and x: SUM_{i=0}^{n-1} |L[i] - x|
# 
# Your code should run in Theta(n) time
#

import random

def partition(L, v):
    smaller = []
    bigger = []
    for val in L:
        if val < v: smaller += [val]
        if val > v: bigger += [val]
    return (smaller, [v], bigger)

def top_k(L, k):
    v = L[random.randrange(len(L))]
    (left, middle, right) = partition(L, v)
    # middle used below (in place of [v]) for clarity
    if len(left) == k:   return left
    if len(left)+1 == k: return left + middle
    if len(left) > k:    return top_k(left, k)
    return left + middle + top_k(right, k - len(left) - len(middle))


def minimize_absolute(L):
    ll = len(L)
    x = None
    # your code here
    if ll%2 == 1:
        list = top_k(L, ll/2 +1)
        x = max(list)
    else:
        list = top_k(L, ll/2 + 1)
        print list
        x1 = max(list)
        list.remove(x1)
        x2 = max(list)
        x = (x1 + x2)  / 2
    return x

L = [ 6, 5, 4, 5]

print minimize_absolute(L)