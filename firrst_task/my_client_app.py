import socket
import sys

def start_client(server_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print("Connected to server")

    while True:
        message = input("Enter message ('terminate' to exit): ")
        client_socket.sendall(message.encode())
        if message == "terminate":
            break

    client_socket.close()
    print("Disconnected from server")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python my_client_app.py <server_ip> <port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    start_client(server_ip, port)
