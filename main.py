import os
from threading import Thread
import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.routing import APIRouter

from config.config import OPEN_SIM_DIR, OPEN_SIM_PATH, FASTAPI_HOST, FASTAPI_PORT
from opensim.opensim_process import OpenSimProcess
from utils.websocket_handler import websocket_endpoint
from routes.fastapi_routes import setup_routes
from opensim.opensim_reader import read_output
from UA3DAPI.controllers.external_controller import ua3d_update_server_status, get_opensim_mode

# Instancia de OpenSimProcess
opensim = OpenSimProcess(OPEN_SIM_PATH, OPEN_SIM_DIR)
COMMAND_HISTORY_PATH = os.path.join(os.getcwd(), "logs", "CommandHistory.txt")

# Crear la aplicación FastAPI
app = FastAPI()

# Habilitar CORS para permitir todas las fuentes (*)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

setup_routes(app, opensim)

# Configurar WebSocket
router = APIRouter()

@router.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket, opensim)

app.include_router(router)

# 🔹 Ruta para iniciar OpenSimulator manualmente
@app.get("/start")
async def start_opensim():
    try:
        mode = await get_opensim_mode()
        print(f"🔵 Intentando iniciar OpenSimulator con modo: {mode}")

        if opensim.running:
            print("⚠️ OpenSimulator ya estaba en ejecución.")
            return {"error": "OpenSimulator ya está en ejecución."}

        opensim.start_process()
        await asyncio.sleep(2) 

        print(f"📌 Estado de opensim.running después de iniciar: {opensim.running}")
        if not opensim.running:
            raise HTTPException(status_code=500, detail="Error: OpenSimulator no se inició correctamente.")

        print("✅ OpenSimulator iniciado correctamente.")

        asyncio.create_task(read_output(opensim, mode))

    except Exception as e:
        print(f"🚨 Error en start_opensim: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al iniciar OpenSimulator: {str(e)}")

    return {"message": f"OpenSimulator iniciado en modo '{mode}'"}

# 🔹 Ruta para detener OpenSimulator manualmente
@app.get("/stop")
async def stop_opensim():
    if not opensim.running:
        return {"error": "OpenSimulator no está en ejecución."}
    try:
        # Primero, actualizar el estado a "SHUTDOWN_SERVER"
        await ua3d_update_server_status("SHUTDOWN_SERVER")  
        print("🔴 Estado del Servidor actualizado a SHUTDOWN_SERVER.")

        # Detener OpenSimulator
        opensim.stop_process()

        # Esperar a que el proceso realmente se detenga
        while opensim.running:
            await asyncio.sleep(1)

        # Luego, actualizar el estado a "OFFLINE"
        await ua3d_update_server_status("OFFLINE")
        print("🟢 Estado del Servidor actualizado a OFFLINE.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al detener el servidor: {str(e)}")

    return {"message": "OpenSimulator detenido correctamente"}

# 🔹 Ruta para obtener el historial de comandos
@app.get("/history")
async def get_command_history():
    try:
        if not os.path.exists(COMMAND_HISTORY_PATH):
            raise HTTPException(status_code=404, detail="El archivo de historial no existe.")

        with open(COMMAND_HISTORY_PATH, "r", encoding="utf-8") as file:
            lines = file.readlines()

        history_entries = [
            line.strip() for line in lines if line.strip() and not line.startswith("===== OpenSimulator Command History =====")
        ]

        return {"history": history_entries}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el historial: {str(e)}")
    
@app.get("/kill")
async def kill_server():
    try:
        print("🛑 Apagando el servidor...")
        os._exit(0)
    except Exception as e:
        return {"error": f"Error al apagar el servidor: {str(e)}"}

# 🔹 Iniciar el servidor FastAPI
if __name__ == "__main__":
   uvicorn.run(app, host=FASTAPI_HOST, port=FASTAPI_PORT)
