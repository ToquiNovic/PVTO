# main.py
import os
from threading import Thread
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.routing import APIRouter

from opensim_process import OpenSimProcess
from websocket_handler import websocket_endpoint
from fastapi_routes import setup_routes

# Configuración del directorio de OpenSimulator
OPEN_SIM_DIR = r"C:\Users\Administrador\Desktop\Opcion de Grado Daniel\servers\UA3D-1\bin"
OPEN_SIM_PATH = os.path.join(OPEN_SIM_DIR, "OpenSim.exe")

# Instancia de OpenSimProcess para manejar el proceso
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

# Iniciar el servidor FastAPI en un hilo separado
def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=5000)

fastapi_thread = Thread(target=start_fastapi)
fastapi_thread.start()

# Iniciar la lectura del proceso OpenSimulator en un hilo separado
output_thread = Thread(target=opensim.read_output)
output_thread.start()

# Espera indefinida para que los hilos sigan funcionando
output_thread.join()
fastapi_thread.join()
