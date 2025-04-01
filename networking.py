import asyncio
import websockets
import queue
import threading

class WebSocketConnection:
    def __init__(self, host="", port="8001"):
        print("init")
        self.host = host 
        self.port = port
        self.clients = set()
        self.message_queue = queue.Queue()

    async def handler(self, websocket):
        """Handles new client connections and messages."""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                self.message_queue.put(message)  # Store message for main app
                #print(self.message_queue.get())
                # This is where ja message will send itself when you can fix the code
                # await self.broadcast(message, sender=websocket)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)

    async def start_server(self):
        """Starts the WebSocket server."""
        print('server starting')
        self.server = await websockets.serve(self.handler, self.host, self.port)
        await self.server.wait_closed()

    def run(self):
        asyncio.run(self.start_server())

    def start_as_thread(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    async def is_message(self):
        "reads messages from the queue then if it is not empty"
        if not self.message_queue.empty():
            return self.message_queue.get()
        return False


#serv = WebSocketConnection()
#asyncio.run(serv.start_as_thread())



