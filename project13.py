from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import time


SECP256R1_p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
SECP256R1_a = -3
SECP256R1_b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
SECP256R1_order = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
SECP256R1_generator = (
    0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
)


def ecmh_curve_hash(data, private_key):
    public_key = private_key.public_key()
    peer_private_key = ec.generate_private_key(ec.SECP256R1())
    peer_public_key = peer_private_key.public_key()
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    hasher = hashes.Hash(hashes.SHA256())
    hasher.update(shared_secret)
    h = hasher.finalize()
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=64,
        salt=None,
        info=b"ecmh",
    ).derive(h)
    key = derived_key[:32]
    hasher = hashes.Hash(hashes.SHA256())
    hasher.update(data)
    hmac_hash = hasher.finalize()
    s = int.from_bytes(hmac_hash, 'big') * int.from_bytes(key, 'big') % SECP256R1_order
    return public_key, hmac_hash, s


def ecmh_curve_verify(data, public_key, hmac_hash, s):
    encoded_public_key = public_key.public_numbers().public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    hasher = hashes.Hash(hashes.SHA256())
    hasher.update(encoded_public_key)
    h = hasher.finalize()
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=64,
        salt=None,
        info=b"ecmh",
    ).derive(h)
    key = derived_key[:32]
    hasher = hashes.Hash(hashes.SHA256())
    hasher.update(data)
    hmac_hash2 = hasher.finalize()
    s2 = int.from_bytes(hmac_hash2, 'big') * int.from_bytes(key, 'big') % SECP256R1_order
    return s == s2


start = time.perf_counter()
private_key = ec.generate_private_key(ec.SECP256R1())
data = b"Hello, world!"
public_key, hmac_hash, s = ecmh_curve_hash(data, private_key)
verification_result = ecmh_curve_verify(data, public_key, hmac_hash, s)
print("Verification Result: ", verification_result)
end = time.perf_counter()
print(end -start)
