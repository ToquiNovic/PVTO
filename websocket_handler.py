from fastapi import WebSocket, WebSocketDisconnect

async def websocket_endpoint(websocket: WebSocket, opensim):
    await websocket.accept()

    try:
        for line in opensim.console_buffer:
            await websocket.send_text(line)

        while True:
            await opensim.console_event.wait()
            opensim.console_event.clear()

            for line in opensim.console_buffer:
                await websocket.send_text(line)

    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")
