# opensim_process.py
import subprocess
import asyncio
import threading
from command_logger import CommandLogger
from message_manager import send_pretty_message

class OpenSimProcess:
    def __init__(self, executable_path, working_dir, websocket_manager=None):
        self.executable_path = executable_path
        self.working_dir = working_dir
        self.console_buffer = []
        self.console_event = asyncio.Event()
        self.region_found = False
        self.process = None  
        self.running = False
        self.lock = threading.Lock()
        self.logger = CommandLogger()
        self.websocket_manager = websocket_manager

    def start_process(self):
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
        with self.lock:
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait()
                self.process = None
                self.running = False
                print("🛑 OpenSimulator detenido correctamente.")
            else:
                print("⚠️ OpenSimulator no estaba en ejecución.")

    async def send_command(self, command):
        with self.lock:
            if not self.running:
                error_msg = "❌ No se puede enviar comandos. OpenSimulator no está en ejecución."
                print(error_msg)
                return error_msg

            if not self.region_found:
                error_msg = "⏳ No se pueden enviar comandos hasta que la región esté completamente cargada."
                print(error_msg)
                return error_msg

            if self.process and self.process.stdin:
                # Usar la función send_pretty_message para enviar el mensaje bonito
                send_pretty_message(self.console_buffer, self.websocket_manager, "success", "Comando enviado con éxito.")
                send_pretty_message(self.console_buffer, self.websocket_manager, "info", f"📩 Comando: {command}")
                
                # Ahora envía el comando a OpenSimulator
                self.process.stdin.write(command + "\n")
                self.process.stdin.flush()


                self.logger.log_command(command)

                return f"Comando enviado: {command}"
