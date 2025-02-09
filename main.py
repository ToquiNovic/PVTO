# main.py
import os
from threading import Thread
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.routing import APIRouter

from config.config import OPEN_SIM_DIR, OPEN_SIM_PATH, FASTAPI_HOST, FASTAPI_PORT
from opensim_process import OpenSimProcess
from utils.websocket_handler import websocket_endpoint
from routes.fastapi_routes import setup_routes
from opensim_reader import read_output 
from UA3DAPI.controllers.external_controller import ua3d_update_server_status

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
    if opensim.running:
        return {"error": "OpenSimulator ya está en ejecución."}
    
    try:
        server_status = await ua3d_update_server_status("ONLINE")
        print(f"Estado del servidor: {server_status}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el estado del servidor: {str(e)}")

    opensim.start_process()

    output_thread = Thread(target=read_output, args=(opensim,))
    output_thread.start()

    return {"message": "OpenSimulator iniciado correctamente"}

# Ruta para detener OpenSimulator manualmente
@app.get("/stop")
async def stop_opensim():
    if not opensim.running:
        return {"error": "OpenSimulator no está en ejecución."}

    opensim.stop_process()

    try:
        server_status = await ua3d_update_server_status("OFFLINE")
        print(f"Estado del Servidor actualizado en la BD: {server_status}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el estado del servidor: {str(e)}")

    return {"message": "OpenSimulator detenido correctamente"}

# Iniciar el servidor FastAPI
if __name__ == "__main__":
   uvicorn.run(app, host=FASTAPI_HOST, port=FASTAPI_PORT)
