import os
import psutil

def kill_related_processes():
    current_pid = os.getpid()
    current_process = psutil.Process(current_pid)
    print(f"🧑‍💻 Cerrando procesos relacionados con el PID {current_pid}...")

    # Encuentra y mata todos los procesos hijos
    for child in current_process.children(recursive=True):
        print(f"🛑 Matando proceso hijo PID: {child.pid} ({child.name()})")
        child.terminate()

    # Esperar a que los procesos terminen
    _, still_alive = psutil.wait_procs(current_process.children(recursive=True), timeout=5)
    for p in still_alive:
        print(f"⚠️ Fuerza bruta para matar PID: {p.pid}")
        p.kill()