from Crypto.PublicKey import RSA
from ex2 import encrypt, decrypt
from primes import square_multiply

if __name__=="__main__":
    # public key
    key_pub = open('mykey.pem.pub','r').read()
    rsakey_pub = RSA.importKey(key_pub)
    n = int(rsakey_pub.n)
    e = int(rsakey_pub.e)
    #print(n)
    #print(e)

    # private key
    key_priv = open('mykey.pem.priv','r').read()
    rsakey_priv = RSA.importKey(key_priv)
    n_priv = int(rsakey_priv.n)
    d = int(rsakey_priv.d)
    #print(n_priv)
    #print(d)

    y = 100
    print(f"Encrypting: {y}\n")

    encrypted = encrypt(y, e, n)
    print(f"Result (as int): {encrypted}\n")

    ys = square_multiply(2, e, n)
    m = (encrypted * ys) % n
    print(f"Modified to (as int): {m}\n")

    decrypted = decrypt(m, d, n)
    print(f"Decrypted: {decrypted}")