from gmssl import sm4
import base64
import time

def sm4_encrypt(plaintext, key):
    cipher = sm4.CryptSM4()
    cipher.set_key(key, sm4.SM4_ENCRYPT)
    ciphertext = cipher.crypt_ecb(plaintext)
    return base64.b64encode(ciphertext)

def sm4_decrypt(ciphertext, key):
    cipher = sm4.CryptSM4()
    cipher.set_key(key, sm4.SM4_DECRYPT)
    decrypted_bytes = cipher.crypt_ecb(base64.b64decode(ciphertext))
    return decrypted_bytes.decode('utf-8')


start = time.perf_counter()
plaintext = b"Hello, World!"
key = b"0123456789abcdef"
encrypted = sm4_encrypt(plaintext, key)
print("Encrypted:", encrypted)
decrypted = sm4_decrypt(encrypted, key)
print("Decrypted:", decrypted)
end = time.perf_counter()
print(end - start)
