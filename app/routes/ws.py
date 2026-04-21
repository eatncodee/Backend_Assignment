from fastapi import status,HTTPException,APIRouter,WebSocket,WebSocketDisconnect
from app.SocketManager import manager
from app.Oauth2 import verify_access_token

ws=APIRouter()


@ws.websocket("/ws")
async def connect(websocket: WebSocket, token: str):
    await websocket.accept()
    email = None
    try:
        Credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentials")
        result = await verify_access_token(token, Credentials_exception)
        email = result.email
        manager.connect(email=email, websocket=websocket)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if email:
            manager.disconnect(email=email, websocket=websocket)
    except HTTPException:
        await websocket.close(code=1008)



