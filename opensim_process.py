import subprocess
import os
import datetime
import asyncio

class OpenSimProcess:
    def __init__(self, executable_path, working_dir):
        self.executable_path = executable_path
        self.working_dir = working_dir
        self.console_buffer = []
        self.console_event = asyncio.Event()
        self.region_found = False
        self.process = subprocess.Popen(
            [self.executable_path, "-console=basic"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=self.working_dir
        )

    def read_output(self):
        while True:
            output = self.process.stdout.readline()
            if output == '' and self.process.poll() is not None:
                break
            if output:
                self.console_buffer.append(output.strip())
                print(output.strip())
                self.console_event.set()

                if 'Region' in output and not self.region_found:
                    self.region_found = True
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file = os.path.join(self.working_dir, "region_log.txt")
                    with open(log_file, 'a') as file:
                        file.write(f"Servidor Iniciado at {timestamp}\n")
                    print(f"Found region, logged at {timestamp}")

                    self.process.stdin.write("alert hola\n")
                    self.process.stdin.flush()

    def send_command(self, command):
        if self.process.stdin:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
