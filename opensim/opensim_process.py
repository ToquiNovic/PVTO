import subprocess
import asyncio
import threading
from utils.command_logger import CommandLogger
from utils.message_manager import send_pretty_message
from UA3DAPI.controllers.external_controller import ua3d_get_server_status

async def is_server_online():
    try:
        server_data = await ua3d_get_server_status()
        if not isinstance(server_data, dict):
            print("⚠️ Respuesta inválida del servidor.")
            return False
        return server_data.get("status", {}).get("name", "") == "ONLINE"
    except Exception as e:
        print(f"🚨 Error al verificar el estado del servidor: {e}")
        return False

class OpenSimProcess:
    def __init__(self, executable_path, working_dir, websocket_manager=None):
        self.executable_path = executable_path
        self.working_dir = working_dir
        self.console_buffer = []
        self.console_event = asyncio.Event()
        self.region_found = False
        self.process = None  
        self.running = False
        self.logger = CommandLogger()
        self.websocket_manager = websocket_manager

    def start_process(self):
        if self.running:
            send_pretty_message(self.console_buffer, self.websocket_manager, "warning", "❌ OpenSimulator ya está en ejecución.")
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
        send_pretty_message(self.console_buffer, self.websocket_manager, "success", "✅ OpenSimulator iniciado correctamente.")
        print("✅ OpenSimulator iniciado correctamente.")

    def stop_process(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            self.process = None
            self.running = False
            send_pretty_message(self.console_buffer, self.websocket_manager, "success", "🛑 OpenSimulator detenido correctamente")
            print("🛑 OpenSimulator detenido correctamente.")
        else:
            send_pretty_message(self.console_buffer, self.websocket_manager, "warning", "⚠️ OpenSimulator no estaba en ejecución.")
            print("⚠️ OpenSimulator no estaba en ejecución.")
    
    async def send_command(self, command):
        if not self.running:
            error_msg = "❌ OpenSimulator no está en ejecución."
            send_pretty_message(self.console_buffer, self.websocket_manager, "error", error_msg)
            print(error_msg)
            return error_msg

        if not await is_server_online():
            error_msg = "🚫 No se pueden enviar comandos hasta que el servidor esté ONLINE."
            send_pretty_message(self.console_buffer, self.websocket_manager, "warning", error_msg)
            print(error_msg)
            return error_msg

        if self.process and self.process.stdin:
            send_pretty_message(self.console_buffer, self.websocket_manager, "success", "Comando enviado con éxito.")
            send_pretty_message(self.console_buffer, self.websocket_manager, "info", f"📩 Comando: {command}")
            
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
            print(f"📩 Comando enviado: {command}")
            
            self.logger.log_command(command)
            return f"Comando enviado: {command}"
