from fastapi import WebSocket
from pydantic import EmailStr

class ConnectionManager:

    def __init__(self):
        self.active_connections: dict ={}

    def connect(self,email : str, websocket: WebSocket):
        if email not in self.active_connections:
            self.active_connections[email] = []
        self.active_connections[email].append(websocket)
    def disconnect(self, email: str, websocket: WebSocket):
        self.active_connections[email].remove(websocket)

    async def broadcast(self, email: str, message: str):
        for connection in self.active_connections.get(email, []):
            await connection.send_text(message)    


manager=ConnectionManager()
