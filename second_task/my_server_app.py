import socket
import sys
import threading

subscribers = []
publishers = []

def handle_client(client_socket, address):
    client_type = client_socket.recv(1024).decode()

    if client_type == "SUBSCRIBER":
        subscribers.append(client_socket)
        print("Subscriber connected:", address)
    elif client_type == "PUBLISHER":
        publishers.append(client_socket)
        print("Publisher connected:", address)

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        print("Received from client", address, ":", data.decode())
        if data.decode() == "terminate":
            break

        if client_type == "PUBLISHER":
            for subscriber in subscribers:
                subscriber.sendall(data)

    if client_type == "SUBSCRIBER":
        subscribers.remove(client_socket)
        print("Subscriber disconnected:", address)
    elif client_type == "PUBLISHER":
        publishers.remove(client_socket)
        print("Publisher disconnected:", address)

    client_socket.close()



def print_subsandpubs():
    print("subs : ",subscribers)
    print("pubsubs : ",publishers)



def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print("Server listening on port", port)

    while True:
        client_socket, address = server_socket.accept()
        print("Client connected:", address)
        threading.Thread(target=handle_client, args=(client_socket, address)).start()
        threading.Thread(target=print_subsandpubs, ).start()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
