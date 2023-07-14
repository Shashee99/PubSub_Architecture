import socket
import sys

def start_client(server_ip, port, mode):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print("Connected to server")

    client_socket.sendall(mode.encode())

    if mode == "SUBSCRIBER":
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Received message:", data.decode())

    elif mode == "PUBLISHER":
        while True:
            message = input("Enter message ('terminate' to exit): ")
            client_socket.sendall(message.encode())
            if message == "terminate":
                break

    client_socket.close()
    print("Disconnected from server")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python my_client_app.py <server_ip> <port> <mode (PUBLISHER or SUBSCRIBER)>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    mode = sys.argv[3]

    start_client(server_ip, port, mode)