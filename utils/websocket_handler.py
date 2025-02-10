# websocket_handler.py
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

async def websocket_endpoint(websocket: WebSocket, opensim):
    await websocket.accept()

    try:
        while True:
            if opensim.process is None or opensim.process.poll() is not None:
                await websocket.send_text("OpenSimulator no está en ejecución. Usa /start para iniciarlo.")
                await asyncio.sleep(3)
                continue

            try:
                await asyncio.wait_for(opensim.console_event.wait(), timeout=5)
                opensim.console_event.clear()
            except asyncio.TimeoutError:
                continue

            while opensim.console_buffer:
                line = opensim.console_buffer.pop(0)
                await websocket.send_text(line)

    except WebSocketDisconnect:
        print("Cliente desconectado del WebSocket")

