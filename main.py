import pyarm
import time


def encrypt(key, plaintext):
    ciphertext = pyarm.aes_encrypt(key, plaintext)
    return ciphertext


def decrypt(key, ciphertext):
    plaintext = pyarm.aes_decrypt(key, ciphertext)
    return plaintext


start = time.perf_counter()
key = b"\x00" * 16
plaintext = b"Hello, world!"
ciphertext = encrypt(key, plaintext)
decrypted_plaintext = decrypt(key, ciphertext)
print(decrypted_plaintext == plaintext)
end = time.perf_counter()
print(end - start)

