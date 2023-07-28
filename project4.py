import struct
import threading
from concurrent.futures import ThreadPoolExecutor

def sm3_hash(message):
    IV = (0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
          0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E)
    Tj = [0x79CC4519, 0x7A879D8A] * 16
    W = [0] * 68
    W_ = [0] * 64
    length_in_bits = len(message) * 8
    message += b'\x80'
    while len(message) % 64 != 56:
        message += b'\x00'
    message += struct.pack('>Q', length_in_bits)

    n = len(message) // 64
    blocks = [message[i*64 : (i+1)*64] for i in range(n)]

    V = list(IV)

    def compress(block):
        for j in range(16):
            W[j] = struct.unpack('>I', block[j*4 : (j+1)*4])[0]
        for j in range(16, 68):
            W[j] = P1(W[j-16] ^ W[j-9] ^ (W[j-3] << 15 | W[j-3] >> 17)) ^ (W[j-13] << 7 | W[j-13] >> 25) ^ W[j-6]

        for j in range(64):
            W_[j] = W[j] ^ W[j+4]

        A, B, C, D, E, F, G, H = V
        for j in range(64):
            A, B, C, D, E, F, G, H = (
                P1((B << 9 | B >> 23) ^ (B << 17 | B >> 15) ^ (B << 23 | B >> 9) ^ Tj[j // 8] ^ W_[j]),
                A,
                (C << 19 | C >> 13),
                D,
                P1((F << 9 | F >> 23) ^ (F << 17 | F >> 15) ^ (F << 23 | F >> 9) ^ Tj[j // 8 + 1] ^ W[j]),
                E,
                (G << 19 | G >> 13),
                H
            )

        return [(V[i] ^ x) & 0xFFFFFFFF for i, x in enumerate([A, B, C, D, E, F, G, H])]

    with ThreadPoolExecutor() as executor:
        results = executor.map(compress, blocks)

    V = [0] * 8
    for result in results:
        V = [(V[i] ^ x) & 0xFFFFFFFF for i, x in enumerate(result)]

    return struct.pack('>8I', *V)

def P1(x):
    return x ^ (x << 15 | x >> 17) ^ (x << 23 | x >> 9)

message = b"Hello World"
hash_value = sm3_hash(message)
print("Hash value:", hash_value.hex())
