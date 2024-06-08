import asyncio

class ChatClient:
    def __init__(self, nickname, host='127.0.0.1', port=5000):
        self.nickname = nickname
        self.host = host
        self.port = port

    async def send_messages(self, writer):
        while True:
            message = f'{self.nickname}: {input()}'
            writer.write(message.encode('utf-8'))
            await writer.drain()

    async def receive_messages(self, reader):
        while True:
            message = await reader.read(100)
            print(message.decode('utf-8'))

    async def run(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)

        # Send initial message to the server
        initial_message = f'{self.nickname} has connected!'
        writer.write(initial_message.encode('utf-8'))
        await writer.drain()

        # Start two tasks: one for sending and one for receiving messages
        send_task = asyncio.create_task(self.send_messages(writer))
        receive_task = asyncio.create_task(self.receive_messages(reader))

        # Wait for both tasks to complete
        await asyncio.gather(send_task, receive_task)

if __name__ == "__main__":
    nickname = input("Choose your nickname: ")
    client = ChatClient(nickname)
    asyncio.run(client.run())