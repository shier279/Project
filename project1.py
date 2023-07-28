import random
import hashlib

def sm3(text):
    h = hashlib.new('sm3')
    h.update(text.encode('utf-8'))
    return h.hexdigest()

def random_message(n):
    r = random.randint(0,n)
    return(str(random.getrandbits(r)))

def brithdayattack():
    H = {}
    while True:
        M = random_message(32)
        h_m = sm3(M)
        H_M = h_m[:10]
        if H_M in H:
            M1 = M
            M2 = H[H_M]
            if M1 != M2:
                return (M1, M2)
        else:
            H[H_M] = M


M1,M2 = brithdayattack()
print(M1,M2)
