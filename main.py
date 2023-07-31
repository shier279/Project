import hashlib
import itertools
import time

def sm3(message):
    return hashlib.new('sm3', bytes(message, 'utf-8')).hexdigest()[:5]

def rho_algorithm():
    target_bits = 5
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    current_length = 1

    while True:
        message_combinations = itertools.product(characters, repeat=current_length)

        for combination in message_combinations:
            message = ''.join(combination)
            hash_value = sm3(message)
            prefix = hash_value[:target_bits]

            if prefix == '0' * target_bits:
                print("Collision found!")
                print("Message:", message)
                print("Hash Value:", hash_value)
                return

        current_length += 1

start = time.perf_counter()
rho_algorithm()
end = time.perf_counter()
print(end - start)