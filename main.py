import hmac
import hashlib
import time
from ecdsa import SigningKey, NIST384p

def sha256(msg):
    return hashlib.sha256(msg).digest()

def hmac_sha256(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()

def bits2int(bits):
    return int.from_bytes(bits, 'big')

def int2octets(num):
    length = (num.bit_length() + 7) // 8
    return num.to_bytes(length, 'big')

def generate_k(hash_msg, private_key):
    order = NIST384p.order
    d = private_key.privkey.secret_multiplier
    k = 0
    v = b'\x01' * 48
    k = hmac_sha256(v + b'\x00' + int2octets(d) + hash_msg, v)
    v = hmac_sha256(v, k)
    k = hmac_sha256(v + b'\x01' + int2octets(d) + hash_msg, v)
    v = hmac_sha256(v, k)
    while True:
        t = b''
        while len(t) < 48:
            v = hmac_sha256(v, b'')
            t += v
        k = bits2int(t)
        if k >= 1 and k < order:
            break
        v = hmac_sha256(v, b'\x00')
    return k

def sm2_sign(private_key, msg):
    curve = NIST384p.curve
    hash_msg = sha256(msg)
    k = generate_k(hash_msg, private_key)
    r = 0
    s = 0
    while r == 0 or s == 0:
        R = k * curve.generator
        r = R.x() % curve.order()
        s = (hash_msg + r * private_key.privkey.secret_multiplier) % curve.order()
    return r, s


start = time.perf_counter()
private_key = SigningKey.generate(curve=NIST384p)
msg = b"Hello, World"
r, s = sm2_sign(private_key, msg)
print("Signature (r, s):", r, s)
end = time.perf_counter()
print(end - start)
