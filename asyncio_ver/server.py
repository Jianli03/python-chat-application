import asyncio

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.server = None
        self.clients = []

    async def handle_client(self, reader, writer):
        client_info = writer.get_extra_info('peername')
        self.clients.append(writer)
        print(f"New connection from {client_info}")

        try:
            while True:
                data = await reader.read(100)
                message = data.decode('utf-8')
                if not message:
                    break
                self.broadcast(message, writer)
        except asyncio.CancelledError:
            pass
        finally:
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()
            print(f"Connection from {client_info} closed")

    def broadcast(self, message, sender_writer):
        for client in self.clients:
            if client != sender_writer:
                client.write(message.encode('utf-8'))
                asyncio.create_task(client.drain())

    async def start_server(self):
        self.server = await asyncio.start_server(self.handle_client, '127.0.0.1', 5000)
        addr = self.server.sockets[0].getsockname()
        print(f"Serving on {addr}")

        async with self.server:
            await self.server.serve_forever()

if __name__ == "__main__":
    server = ChatServer()
    asyncio.run(server.start_server())