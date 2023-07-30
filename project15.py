import socket
import time
from gmssl import sm2, func


def generate_key_pair():
    private_key = sm2.CryptSM2(public_key_format='uncompressed').generate_key()
    public_key = private_key[1]
    return private_key, public_key

def send_public_key(socket, public_key):
    socket.sendall(public_key)

def receive_public_key(socket):
    public_key = socket.recv(1024)
    return public_key

def sign_message(private_key, message):
    signer = sm2.CryptSM2(private_key=private_key)
    signature = signer.sign(func.bytes_to_list(message))
    return signature


def verify_signature(public_key, signature, message):
    verifier = sm2.CryptSM2(public_key=public_key)
    try:
        verifier.verify(func.bytes_to_list(signature), func.bytes_to_list(message))
        return True
    except Exception:
        return False


def client():
    host = '127.0.0.1'
    port = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    private_key, public_key = generate_key_pair()
    send_public_key(client_socket, public_key)
    server_public_key = receive_public_key(client_socket)
    message = b'Hello, World!'
    signature = sign_message(private_key, message)
    client_socket.sendall(message)
    client_socket.sendall(signature)
    result = client_socket.recv(1024)

    if result == b'Success':
        print("Signature verification succeeded.")
    else:
        print("Signature verification failed.")
    client_socket.close()

# 服务器端代码
def server():
    host = '127.0.0.1'
    port = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()
    client_public_key = receive_public_key(client_socket)
    private_key, public_key = generate_key_pair()
    send_public_key(client_socket, public_key)
    message = client_socket.recv(1024)
    signature = client_socket.recv(1024)


    if verify_signature(client_public_key, signature, message):
        client_socket.sendall(b'Success')
    else:
        client_socket.sendall(b'Failure')

    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    start = time.perf_counter()
    server()
    client()
    end = time.perf_counter()
    print(end - start)
