from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import time

def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext, AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_plaintext)
    encrypted_text = base64.b64encode(encrypted_bytes)
    return encrypted_text

def aes_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(base64.b64decode(ciphertext))
    decrypted_text = unpad(decrypted_bytes, AES.block_size).decode('utf-8')
    return decrypted_text

start = time.perf_counter()
plaintext = b"Hello, World!"
key = b"0123456789abcdef"
encrypted = aes_encrypt(plaintext, key)
print("Encrypted:", encrypted)
decrypted = aes_decrypt(encrypted, key)
print("Decrypted:", decrypted)
end = time.perf_counter()
print(end - start)
