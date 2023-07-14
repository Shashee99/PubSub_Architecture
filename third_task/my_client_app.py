import socket
import sys

def start_client(server_ip, port, mode, topic=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print("Connected to server")

    client_socket.sendall(mode.encode())

    if mode == "SUBSCRIBER":
        if topic:
            topic = f',{topic}'
            client_socket.sendall(topic.encode())
        else:
            print("Please provide a topic for the subscriber.")
            client_socket.close()
            return

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Received message:", data.decode())

    elif mode == "PUBLISHER":
        if topic:
            topicTobesend = f',{topic}'
            client_socket.sendall(topicTobesend.encode())
        else:
            print("Please provide a topic for the publisher.")
            client_socket.close()
            return

        while True:
            message = input("Enter message ('terminate' to exit): ")
            prepareforsend = f'{topic}:{message}'
            client_socket.sendall(prepareforsend.encode())
            if message == "terminate":
                break

    client_socket.close()
    print("Disconnected from server")

if __name__ == '__main__':
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python my_client_app.py <server_ip> <port> <mode (PUBLISHER or SUBSCRIBER)> [<topic>]")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    mode = sys.argv[3]
    topic = sys.argv[4] if len(sys.argv) == 5 else None

    start_client(server_ip, port, mode, topic)
