#
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the square of the difference
# between each element in L and x: SUM_{i=0}^{n-1} (L[i] - x)^2
# 
# Your code should run in Theta(n) time
# 

def minimize_square(L):
    x = 0
    # your code here
    for item in L:
        x += item    
    if len(L) == 0:
        return 0
    else:
        return x* 1.0/len(L)
    
L = [2,2,3,4]
print minimize_square(L)