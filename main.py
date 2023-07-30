import socket
from gmssl import sm2

def receive_data(conn):
    data = b''
    while True:
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk
    return data

def send_data(conn, data):
    conn.sendall(data)

def sm2_2p_decrypt(private_key, ciphertext):
    sm2_crypt = sm2.CryptSM2(private_key, b'')
    plaintext = sm2_crypt.decrypt(ciphertext)
    return plaintext

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 1234
REMOTE_HOST = '127.0.0.1'
REMOTE_PORT = 5678

file_path_private = "C:/Users/27968/Desktop/local_private_key.pem"
password_private = "123456"

file_path_shared = "C:/Users/27968/Desktop/local_shared_key.pem"
password_shared = "123456"

local_private_key, local_public_key = sm2.CryptSM2().generate_key_pair()
with open(file_path_private, "wb") as key_file:
    key_file.write(local_private_key.export_key(format="PEM", cipher="sm4_cbc", password=password_private.encode()))

local_shared_key, _ = sm2.CryptSM2().generate_key_pair()
with open(file_path_shared, "wb") as key_file:
    key_file.write(local_shared_key.export_key(format="PEM", cipher="sm4_cbc", password=password_shared.encode()))


local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_socket.bind((LOCAL_HOST, LOCAL_PORT))
local_socket.listen(1)
print("等待本地客户端连接...")

local_conn, local_addr = local_socket.accept()
print("本地客户端已连接：", local_addr)

remote_public_key = receive_data(local_conn)
decrypted_remote_public_key = sm2_2p_decrypt(local_private_key, remote_public_key)

ciphertext = receive_data(local_conn)
plaintext = sm2_2p_decrypt(local_shared_key, ciphertext)
send_data(local_conn, plaintext)

local_conn.close()
local_socket.close()