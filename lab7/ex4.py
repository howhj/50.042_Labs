from Crypto.PublicKey import RSA
from ex2 import encrypt, decrypt
from random import randint

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

    s = random.randint(0, 2^1024-1)
    x = encrypt(s, e, n)
    print("As 'Alice',")
    print(f"s: {s}")
    print(f"x: {x}\n")

    new_x = decrypt(s, e, n)
    check = new_x == x
    print("As Bob,")
    print(f"x': {new_x}")
    print(f"x'==x? {check}")
    if check:
        print("s is a valid signature for x. (x,s) accepted.")
    else:
        print("s is an invalid signature for x. (x,s) rejected.")