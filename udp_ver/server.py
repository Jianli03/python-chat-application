import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((host, port))
        self.clients = []

    def broadcast(self, message, sender_address):
        for client in self.clients:
            if client != sender_address:
                self.server.sendto(message, client)

    def handle_messages(self):
        while True:
            try:
                message, client_address = self.server.recvfrom(1024)
                if client_address not in self.clients:
                    self.clients.append(client_address)
                    self.broadcast(f"{client_address} joined the chat!".encode('utf-8'), client_address)
                self.broadcast(message, client_address)
            except:
                continue

if __name__ == "__main__":
    server = ChatServer()
    print('Server is running...')
    server.handle_messages()