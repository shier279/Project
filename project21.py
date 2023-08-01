from hashlib import sha256
from random import randint
import time

def generate_keypair():
    private_key = randint(1, pow(2, 256))
    public_key = pow(2, private_key, pow(2, 256) + 1)
    return private_key, public_key


def sign(private_key, message):
    hashed_message = int.from_bytes(sha256(message.encode()).digest(), 'big')
    nonce = randint(1, pow(2, 256))
    R = pow(2, nonce, pow(2, 256) + 1)
    commitment = pow(pow(2, private_key, pow(2, 256) + 1), R, pow(2, 256) + 1)
    challenge = int.from_bytes(sha256(commitment.to_bytes(32, 'big') + message.encode()).digest(), 'big') % pow(2, 256)
    response = (nonce - private_key * challenge) % (pow(2, 256) + 1)
    return commitment, response


def verify(public_key, message, commitment, response):
    challenge = int.from_bytes(sha256(commitment.to_bytes(32, 'big') + message.encode()).digest(), 'big') % pow(2, 256)
    verification_eq = pow(pow(2, public_key, pow(2, 256) + 1), commitment, pow(2, 256) + 1) * pow(commitment, challenge,
                                                                                                  pow(2, 256) + 1)
    verification_eq %= pow(2, 256) + 1
    return verification_eq == pow(2, response, pow(2, 256) + 1)


start = time.perf_counter()
private_key, public_key = generate_keypair()
message = "Hello, world!"
commitment, response = sign(private_key, message)
is_valid = verify(public_key, message, commitment, response)
print("Signature is valid:", is_valid)
end = time.perf_counter()
print(end - start)
