# 50.042 FCS Lab 6 template
# Year 2021

import random
def square_multiply(a,x,n):
    # Find number of bits of x
    p = x
    counter = 0
    while p > 0:
        p >>= 1
        counter += 1

    # Algorithm
    y = 1
    for i in range(counter-1, -1, -1):
        y = y**2 % n
        z = x >> i
        x -= z << i
        if z == 1:
            y = a * y % n
    return y

def miller_rabin(n, a):
    pass

def gen_prime_nbits(n):
    pass

if __name__=="__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561,2))
    print('Is 27 a prime?')
    print(miller_rabin(27,2))
    print('Is 61 a prime?')
    print(miller_rabin(61,2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (80 bits):')
    print(gen_prime_nbits(80))
