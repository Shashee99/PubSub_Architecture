import socket
import sys
import threading

topic_subscribers = {}

def handle_client(client_socket, address):
    client_type = client_socket.recv(1024).decode()
   
    client_type,topic = client_type.split(',')
    # print(ct,topic)
    if client_type == "SUBSCRIBER":
       
        if topic not in topic_subscribers:
            topic_subscribers[topic] = []
        topic_subscribers[topic].append(client_socket)
       
        print("Subscriber connected:", address, "Topic:", topic)

    elif client_type == "PUBLISHER":
        if topic not in topic_subscribers:
            topic_subscribers[topic] = []
        topic_subscribers[topic].append(client_socket)
     
        print("Publisher connected:", address, "Topic:", topic)

    while True:
        # print(topic_subscribers)
        data = client_socket.recv(1024)
        if not data:
            break
        incoming = data.decode()
        topic,message = incoming.split(':')
        print("Received from Publisher ", address, ":", message, "| Topic : ", topic)
        if data.decode() == "terminate":
            break

        if client_type == "PUBLISHER":
           
            data = message.encode()
            print(topic)
            if topic in topic_subscribers:
                print('topic')
                subscribers = topic_subscribers[topic]
                print('ss',subscribers)
                for subscriber in subscribers:
                    subscriber.sendall(data)

    if client_type == "SUBSCRIBER":
        topic = client_socket.recv(1024).decode()
        if topic in topic_subscribers:
            topic_subscribers[topic].remove(client_socket)
            print("Subscriber disconnected:", address)
    elif client_type == "PUBLISHER":
        print("Publisher disconnected:", address)
    # print(topic_subscribers)


    client_socket.close()

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print("Server listening on port", port)

    while True:
        client_socket, address = server_socket.accept()
        print("Client connected:", address)
        # threading.Thread(target=print(topic_subscribers),).start()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
