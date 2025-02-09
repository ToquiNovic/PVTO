import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables del entorno
OPEN_SIM_DIR = os.getenv("OPEN_SIM_DIR")
OPEN_SIM_EXECUTABLE = os.getenv("OPEN_SIM_EXECUTABLE", "OpenSim.exe") 
OPEN_SIM_PATH = os.path.join(OPEN_SIM_DIR, OPEN_SIM_EXECUTABLE) if OPEN_SIM_DIR else None

# Configuración de FastAPI
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 5000))
