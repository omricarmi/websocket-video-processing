from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from cv2 import cv2
import logging
import utils
from websocket_connection_manager import ConnectionManager

# FastAPI App
app = FastAPI()

# Read client html
with open('index.html') as f:
    html = f.read()


@app.get("/")
async def get():
    return HTMLResponse(html)


# Websocket Connection Manager
manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.broadcast({'type': "message", 'data': f"Client '{client_id}' joined"})
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            img = utils.base64_url_data_to_cv2_image(data)
            img = cv2.Canny(img,100,200)
            img = cv2.putText(img, f"server from client: {client_id}", (20, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))
            data_with_overlay = utils.cv2_image_to_base64_url_data(img)
            await manager.broadcast({'type': "image", 'data': data_with_overlay})
            # await manager.send_personal_message(data_with_overlay,websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({'type': "message", 'data': f"Client '{client_id}' left"})
        cv2.destroyAllWindows()
    except:
        logging.error(f'unexcpected error')
