import socket
from folyamtitkosito import solitaire
from folyamtitkosito import blum_blum_shub
from folyamtitkosito import generate_one_time_key
from folyamtitkosito import stream_encrypt
from folyamtitkosito import stream_decrypt
from read_configuration import read


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(2)

    print("Waiting for clients to connect...")
    client1, addr1 = server_socket.accept()
    print(f"Client 1 connected: {addr1}")
    client2, addr2 = server_socket.accept()
    print(f"Client 2 connected: {addr2}")

    encryption_algorithm, key = read()
    try:
        while True:
            data = client1.recv(1024)
            if not data:
                break
            decrypted_data = stream_decrypt(data, key)
            print(f"Received from Client 1: {decrypted_data.decode()}")

            client2.send(stream_encrypt(decrypted_data, key))

            data = client2.recv(1024)
            if not data:
                break
            decrypted_data = stream_decrypt(data, key)
            print(f"Received from Client 2: {decrypted_data.decode()}")

            client1.send(stream_encrypt(decrypted_data, key))
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
