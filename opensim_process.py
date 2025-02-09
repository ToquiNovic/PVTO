# opensim_process.py
import subprocess
import asyncio
import threading  # 🔒 Importamos threading para el Lock

class OpenSimProcess:
    def __init__(self, executable_path, working_dir):
        self.executable_path = executable_path
        self.working_dir = working_dir
        self.console_buffer = []
        self.console_event = asyncio.Event()
        self.region_found = False
        self.process = None  
        self.running = False
        self.lock = threading.Lock()

    def start_process(self):
        """ Inicia OpenSimulator solo si no está en ejecución. """
        with self.lock:
            if self.running:
                print("❌ OpenSimulator ya está en ejecución.")
                return

            self.process = subprocess.Popen(
                [self.executable_path, "-console=basic"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=self.working_dir
            )
            self.running = True
            print("✅ OpenSimulator iniciado correctamente.")

    def stop_process(self):
        """ Detiene OpenSimulator si está en ejecución. """
        with self.lock:
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait()
                self.process = None
                self.running = False
                print("🛑 OpenSimulator detenido correctamente.")
            else:
                print("⚠️ OpenSimulator no estaba en ejecución.")

    def send_command(self, command):
        """ Envía un comando a la consola de OpenSimulator. """
        if self.process and self.process.stdin:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()

