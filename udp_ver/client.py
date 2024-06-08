import socket
import threading

class ChatClient:
    def __init__(self, nickname, host='127.0.0.1', port=5000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (host, port)
        self.nickname = nickname

        self.client.sendto(f'{nickname} has connected!'.encode('utf-8'), self.server_address)

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send)
        send_thread.start()

    def receive(self):
        while True:
            try:
                message, _ = self.client.recvfrom(1024)
                print(message.decode('utf-8'))
            except:
                continue

    def send(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.sendto(message.encode('utf-8'), self.server_address)

if __name__ == "__main__":
    nickname = input("Choose your nickname: ")
    client = ChatClient(nickname)