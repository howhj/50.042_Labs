from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from base64 import b64encode, b64decode
from math import ceil
from primes import square_multiply
from random import randint

def generate_RSA(bits=1024):
    key = RSA.generate(bits)
    priv_key = key.export_key()
    fout_priv = open("key.pem", "wb").write(priv_key)
    pub_key = key.publickey().export_key()
    fout_pub = open("key.pem.pub", "wb").write(pub_key)

def encrypt_RSA(pub_key_file, message):
    key = open(pub_key_file, "rb").read()
    rsakey = RSA.importKey(key)
    oaep_obj = PKCS1_OAEP.new(rsakey)
    cipher = oaep_obj.encrypt(message.encode())
    return b64encode(cipher)

def decrypt_RSA(priv_key_file, cipher):
    key = open(priv_key_file, "rb").read()
    rsakey = RSA.importKey(key)
    cipher_decoded = b64decode(cipher)
    oaep_obj = PKCS1_OAEP.new(rsakey)
    data = oaep_obj.decrypt(cipher_decoded)
    return data.decode()

def sign_data(priv_key_file, data):
    key = open(priv_key_file, "rb").read()
    rsakey = RSA.importKey(key)
    hashed_data = SHA256.new(data.encode())
    signature = PKCS1_PSS.new(rsakey).sign(hashed_data)
    return b64encode(signature)

def verify_sign(pub_key_file, sign, data):
    key = open(pub_key_file, "rb").read()
    rsakey = RSA.importKey(key)
    hashed_data = SHA256.new(data.encode())
    verifier = PKCS1_PSS.new(rsakey)
    try:
        verifier.verify(hashed_data, b64decode(sign))
        return True
    except(ValueError, TypeError):
        return False

if __name__=="__main__":
    generate_RSA()
    plaintext = open("mydata.txt", "r").read()
    print(f"Plaintext: {plaintext}\n")

    cipher = encrypt_RSA("key.pem.pub", plaintext)
    decrypted = decrypt_RSA("key.pem", cipher)
    print(f"Decrypted plaintext: {decrypted}\n")
    print(f"Original and decrypted plaintext match? {plaintext == decrypted}\n")

    signature = sign_data("key.pem", plaintext)
    verification = verify_sign("key.pem.pub", signature, plaintext)
    print(f"Signature verified? {verification}\n")

    print("------------------------------------------------------------\n")

    print("Protocol attack on encryption:\n")
    key_pub = open('key.pem.pub','r').read()
    rsakey_pub = RSA.importKey(key_pub)
    n = int(rsakey_pub.n)
    e = int(rsakey_pub.e)
    y = 100
    print(f"Encrypting: {y}\n")

    encrypted = encrypt_RSA("key.pem.pub", str(y))
    print(f"Result (in base64): {encrypted}\n")

    ys = square_multiply(2, e, n)
    m = (int.from_bytes(b64decode(encrypted), "little") * ys) % n
    m_str = b64encode(m.to_bytes(ceil(m.bit_length()/8), "little"))
    print(f"Modified to (in base64): {m_str}\n")

    try:
        decrypted2 = decrypt_RSA("key.pem", m_str)
        print(f"Decrypted: {decrypted2}")
        print("The protocol attack succeeded.")
    except(ValueError):
        print("Ciphertext could not be decrypted.")
        print("The protocol attack failed.\n")

    print("------------------------------------------------------------\n")

    print("Protocol attack on signature:\n")
    s = randint(0, 2**256-1) # Using 256 bits to allow for padding
    x = encrypt_RSA("key.pem.pub", str(s))
    print("As 'Alice',")
    print(f"s: {s}")
    print(f"x: {x}\n")

    check = verify_sign("key.pem.pub", str(s), str(x))
    print("As Bob,")
    print(f"x'==x? {check}")
    if check:
        print("s is a valid signature for x. (x,s) accepted.")
        print("The protocol attack succeeded.")
    else:
        print("s is an invalid signature for x. (x,s) rejected.")
        print("The protocol attack failed.")