# 50.042 FCS Lab 6 template
# Year 2021

import primes
import random
import present

def dhke_setup(nb):
    p = 1208925819614629174706189
    alpha = 1208925819614629174706187
    return p, alpha

def gen_priv_key(p):
    return random.randint(2, p-2)

def get_pub_key(alpha, a, p):
    return primes.square_multiply(alpha, a, p)

def get_shared_key(keypub, keypriv, p):
    return primes.square_multiply(keypub, keypriv, p)


if __name__ == "__main__":
    p, alpha = dhke_setup(80)
    print("Generate P and alpha:")
    print("P:", p)
    print("alpha:", alpha)
    print()
    a = gen_priv_key(p)
    b = gen_priv_key(p)
    print("My private key is: ", a)
    print("Test other private key is: ", b)
    print()
    A = get_pub_key(alpha, a, p)
    B = get_pub_key(alpha, b, p)
    print("My public key is: ", A)
    print("Test other public key is: ", B)
    print()
    sharedKeyA = get_shared_key(B, a, p)
    sharedKeyB = get_shared_key(A, b, p)
    print("My shared key is: ", sharedKeyA)
    print("Test other shared key is: ", sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())

    # My lab 4 ecb.py was coded to be very specific to pbm files.
    # For convenience, I will only use an 8 character string
    # so that I can encrypt it as a single block using present.py directly.
    # The plaintext I chose is "12345678" (without the quotes).
    # In hexadecimal, the plaintext is 0x3132333435363738
    plain = 0x3132333435363738
    cipher = present.present(plain, sharedKeyA)
    decrypted = present.present_inv(cipher, sharedKeyB)
    assert plain == decrypted
