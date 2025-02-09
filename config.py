# config.py
import os

# Configuración del servidor OpenSimulator
OPENSIM_DIR = r"C:\Users\Administrador\Desktop\Opcion de Grado Daniel\servers\UA3D-1\bin"
OPENSIM_PATH = os.path.join(OPENSIM_DIR, "OpenSim.exe")
LOG_FILE = r"C:\Users\Administrador\Desktop\Opcion de Grado Daniel\prueba\region_log.txt"

# Configuración del servidor FastAPI
HOST = "0.0.0.0"
PORT = 5000