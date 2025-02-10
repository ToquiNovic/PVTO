# command_logger.py
import os
import datetime

class CommandLogger:
    def __init__(self, log_dir="logs", log_file="CommandHistory.txt"):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)

        # Crear la carpeta 'logs' si no existe
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Crear el archivo si no existe
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as file:
                file.write("===== OpenSimulator Command History =====\n")

    def log_command(self, command):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {command}\n"

        with open(self.log_file, "a") as file:
            file.write(log_entry)

        print(f"📝 Comando registrado en {self.log_file}")
