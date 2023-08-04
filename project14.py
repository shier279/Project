from gmssl.sm2 import CryptSM2, SM2PrivateKey, SM2PublicKey
import time

def generate_key_pair():
    private_key = SM2PrivateKey()
    private_key.generate()
    public_key = private_key.public_key
    return private_key, public_key

def encrypt(message, public_key):
    cipher = CryptSM2(public_key=public_key)
    encrypted_data = cipher.encrypt(message.encode())
    return encrypted_data

def decrypt(encrypted_data, private_key):
    cipher = CryptSM2(private_key=private_key)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data.decode()

def sign(message, private_key):
    signer = CryptSM2(private_key=private_key)
    signature = signer.sign(message.encode())
    return signature

def verify(message, signature, public_key):
    verifier = CryptSM2(public_key=public_key)
    is_valid = verifier.verify(message.encode(), signature)
    return is_valid

start = time.perf_counter()
message = "Hello, World!"
private_key, public_key = generate_key_pair()
encrypted_data = encrypt(message, public_key)
decrypted_data = decrypt(encrypted_data, private_key)
signature = sign(message, private_key)
is_valid = verify(message, signature, public_key)

print("加密后的数据：", encrypted_data)
print("解密后的数据：", decrypted_data)
print("数字签名：", signature)
print("签名验证结果：", is_valid)
end = time.perf_counter()
print(end - start)
