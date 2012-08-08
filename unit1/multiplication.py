# naive multiplication algorithm

def naive(a, b):
    x = a; y = b;
    z = 0;
    while x>0:
        z = z + y
        x = x-1
    return z

# recursive naive multiplication algorithm

def rec_naive(a, b):
    if a==0:
        return 0
    return b + rec_naive(a-1, b)
    
# russian multiplication algorithm

def russian(a, b):
    x = a; y = b;
    z = 0;
    while x>0:
        if x%2 == 1:
            z = z + y
        y = y<<1
        x = x>>1
    return z

# russian, in recursive

def rec_russian(a, b):
    if a == 0:
        return 0
    if a %2 == 0:
        return 2*rec_russian(a>>1, b)
    else:
        return b + 2*rec_russian(a>>1, b)
    

a = 7; b = 4;
print naive(a, b) == rec_naive(a, b) \
        and naive(a,b) == russian(a,b) \
        and naive(a,b) == rec_russian(a,b)