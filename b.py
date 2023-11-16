import numpy as np

def f(n):
    c = 0
    i = 0
    while n>=0:
        i += 1
        n = n-2
        c = c + n - 2 
    
    r = i == (np.ceil(n/2))

    return c,i
print(f(7))