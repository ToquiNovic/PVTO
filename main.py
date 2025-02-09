# main.py
import os
from threading import Thread
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.routing import APIRouter

from config import OPEN_SIM_DIR, OPEN_SIM_PATH, FASTAPI_HOST, FASTAPI_PORT
from opensim_process import OpenSimProcess
from websocket_handler import websocket_endpoint
from fastapi_routes import setup_routes
from opensim_reader import read_output 

# Instancia de OpenSimProcess
opensim = OpenSimProcess(OPEN_SIM_PATH, OPEN_SIM_DIR)

# Crear la aplicación FastAPI
app = FastAPI()
setup_routes(app, opensim)

# Configurar WebSocket
router = APIRouter()

@router.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket, opensim)


app.include_router(router)

# Ruta para iniciar OpenSimulator manualmente
@app.get("/start")
async def start_opensim():
    opensim.start_process()
    
    # Iniciar la lectura del proceso en un hilo separado
    output_thread = Thread(target=read_output, args=(opensim,))
    output_thread.start()

    return {"message": "OpenSimulator iniciado correctamente"}

# Iniciar el servidor FastAPI
if __name__ == "__main__":
   uvicorn.run(app, host=FASTAPI_HOST, port=FASTAPI_PORT)
