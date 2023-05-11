# 50.042 FCS Lab 6 template
# Year 2021

import math
import primes
import random
import time

def baby_step(alpha, beta, p, fname):
    result = []
    for i in range(m):
        result.append(f"{(beta * primes.square_multiply(alpha, i, p)) % p}\n")
    with open(fname, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.writelines(result)

def giant_step(alpha, p, fname):
    result = []
    for i in range(m):
        result.append(f"{primes.square_multiply(alpha, i*m, p)}\n")
    with open(fname, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.writelines(result)

def baby_giant(alpha, beta, p):
    global m
    m = math.ceil((p-1)**0.5)
    bfile = "baby_step.txt"
    gfile = "giant_step.txt"
    baby_step(alpha, beta, p, bfile)
    giant_step(alpha, p, gfile)
    
    with open(bfile, mode="r", encoding="utf-8", newline="\n") as baby:
        with open(gfile, mode="r", encoding="utf-8", newline="\n") as giant:
            bsteps = baby.readlines()
            gsteps = giant.readlines()
            for i in range(m):
                for j in range(m):
                    if int(bsteps[i].strip()) == int(gsteps[j].strip()):
                        return j*m-i
            return -1

def test(p):
    start_time = time.time()
    random.seed(100)
    alpha = p-2
    private = random.randint(0, p-1)
    A = primes.square_multiply(alpha, private, p)
    B = primes.square_multiply(alpha, random.randint(0, p-1), p)
    sharedkey = primes.square_multiply(B, private, p)
    a = baby_giant(alpha, A, p)
    b = baby_giant(alpha, B, p)
    guesskey1 = primes.square_multiply(A, b, p)
    guesskey2 = primes.square_multiply(B, a, p)
    print("Guess key 1:", guesskey1)
    print("Guess key 2:", guesskey2)
    print("Actual shared key :", sharedkey)
    print(f"{time.time() - start_time} sec")

if __name__ == "__main__":
    start_time = time.time()
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    """
    p = 17851
    alpha = 17511
    A = 2945
    B = 11844
    sharedkey = 1671
    a = baby_giant(alpha, A, p)
    b = baby_giant(alpha, B, p)
    guesskey1 = primes.square_multiply(A, b, p)
    guesskey2 = primes.square_multiply(B, a, p)
    print("Guess key 1:", guesskey1)
    print("Guess key 2:", guesskey2)
    print("Actual shared key :", sharedkey)
    print(f"{time.time() - start_time} sec")

    # Test 2 (17 bits)
    test(131071)

    # Test 3 (20 bits)
    test(1048573)

    # Test 4 (32 bits)
    test(4294967291)