# command_handler.py
from config import LOG_FILE

def log_region_found():
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as file:
        file.write(f"Servidor Iniciado at {timestamp}\n")

# websocket_handler.py
import asyncio
from fastapi import WebSocket, WebSocketDisconnect

console_buffer = []
console_event = asyncio.Event()

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        for line in console_buffer:
            await websocket.send_text(line)
        while True:
            await console_event.wait()
            console_event.clear()
            for line in console_buffer:
                await websocket.send_text(line)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")