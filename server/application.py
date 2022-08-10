import json

from fastapi import FastAPI, WebSocket
from server.connection_manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    print(f"Accepting connection for client {client_id} ...")
    await manager.connect(websocket)
    print("Connected")
    while True:
        data = await websocket.receive_json()
        await manager.broadcast(data)
