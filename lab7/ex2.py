from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from primes import square_multiply

def encrypt(x, e, n):
    return square_multiply(x, e, n)

def decrypt(x, d, n):
    return square_multiply(x, d, n)

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

    plaintext = open("message.txt", "rb").read()
    plaintext_as_int = int.from_bytes(plaintext, "big")
    print(f"Original message (as integer) is: {plaintext_as_int}\n")

    encrypted_message = encrypt(plaintext_as_int, e, n)
    print(f"Encrypted message (as integer) is: {encrypted_message}\n")

    decrypted_message = decrypt(encrypted_message, d, n)
    print(f"Decrypted message (as integer) is: {decrypted_message}\n")
    print(f"Do decrypted and original messages match? {plaintext_as_int == decrypted_message}\n")

    hashed_message = SHA256.new(plaintext)
    hash_as_int = int(hashed_message.hexdigest(), 16)
    print(f"Hashed message (as integer) is: {hash_as_int}\n")

    signature = encrypt(hash_as_int, d, n_priv)
    print(f"RSA signature is: {signature}\n")

    verification = decrypt(signature, e, n)
    print(f"Verification with public key: {verification}\n")
    print(f"Do hashes match? {hash_as_int == verification}")