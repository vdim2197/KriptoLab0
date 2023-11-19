import socket
from folyamtitkosito import solitaire
from folyamtitkosito import blum_blum_shub
from folyamtitkosito import generate_one_time_key
from folyamtitkosito import stream_encrypt
from folyamtitkosito import stream_decrypt
from read_configuration import read

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    encryption_algorithm, key = read()

    try:
        while True:
            message = input("Enter your message: ")
            encrypted_message = stream_encrypt(message.encode(), key)
            client_socket.send(encrypted_message)

            data = client_socket.recv(1024)
            decrypted_data = stream_decrypt(data, key)
            print(f"Received from server: {decrypted_data.decode()}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()