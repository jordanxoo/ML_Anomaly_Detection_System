from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

class ConnectionManager:

    def __init__(self):
        self.active_connections = []


    async def connect(self,websocket):
        self.active_connections.append(websocket)

    async def broadcast(self,message):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def disconnect(self,websocket):
        self.active_connections.remove(websocket)



manager = ConnectionManager()
router = APIRouter()

@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    
    await websocket.accept()
    await manager.connect(websocket)

    while True:
        try:
            await websocket.receive_text()
        except WebSocketDisconnect:
            await manager.disconnect(websocket)
            break 

