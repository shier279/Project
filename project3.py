import hashlib
import time


message = b"Hello world"
hash_obj = hashlib.sha256(message)
digest = hash_obj.digest()


fake_message = b"Hello_world"
fake_digest = hashlib.sha256(fake_message).digest()
fake_digest_extended = hashlib.sha256(fake_message + digest).hexdigest()


start = time.perf_counter()
print("Original message: ", message)
print("Original digest: ", digest.hex())
print("Fake message: ", fake_message)
print("Fake digest: ", fake_digest.hex())
print("Fake extended digest: ", fake_digest_extended)
end = time.perf_counter()
print(end - start)
