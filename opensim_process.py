# opensim_process.py
import subprocess
import asyncio

class OpenSimProcess:
    def __init__(self, executable_path, working_dir):
        self.executable_path = executable_path
        self.working_dir = working_dir
        self.console_buffer = []
        self.console_event = asyncio.Event()
        self.region_found = False
        self.process = None  

    def start_process(self):
        """ Inicia el proceso de OpenSimulator si no está en ejecución. """
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(
                [self.executable_path, "-console=basic"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=self.working_dir
            )
            print("OpenSimulator iniciado correctamente.")

    def send_command(self, command):
        if self.process and self.process.stdin:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
