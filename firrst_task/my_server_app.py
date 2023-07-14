import socket
import sys

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print("Server listening on port", port)

    while True:
        client_socket, address = server_socket.accept()
        print("Client connected:", address)

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Received from client:", data.decode())

            if data.decode() == "terminate":
                break

        client_socket.close()
        print("Client disconnected")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
