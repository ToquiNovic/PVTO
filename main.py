# main.py
from threading import Thread
from opensim import start_opensim
from server import start_fastapi

process = start_opensim()
fastapi_thread = Thread(target=start_fastapi)
fastapi_thread.start()
fastapi_thread.join()