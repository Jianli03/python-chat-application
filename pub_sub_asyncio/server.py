import asyncio

class PubSub:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, client):
        self.subscribers[client] = asyncio.Queue()

    def unsubscribe(self, client):
        if client in self.subscribers:
            del self.subscribers[client]

    async def publish(self, message, sender_client):
        for client, q in self.subscribers.items():
            if client != sender_client:
                await q.put(message)

    async def get_message(self, client):
        return await self.subscribers[client].get()

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.pubsub = PubSub()

    async def handle_client(self, reader, writer):
        client = writer.get_extra_info('peername')
        self.pubsub.subscribe(client)
        try:
            while True:
                data = await reader.read(100)
                message = data.decode('utf-8')
                if not message:
                    break
                await self.pubsub.publish(message, client)
                while not self.pubsub.subscribers[client].empty():
                    message = await self.pubsub.get_message(client)
                    writer.write(message.encode('utf-8'))
                    await writer.drain()
        except:
            pass
        finally:
            self.pubsub.unsubscribe(client)
            writer.close()
            await writer.wait_closed()

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    server = ChatServer()
    asyncio.run(server.start_server())