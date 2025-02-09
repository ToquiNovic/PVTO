import datetime
import os

def read_output(opensim):
    log_created = False  
    log_file = os.path.join(os.getcwd(), "region_log.txt") 

    while True:
        output = opensim.process.stdout.readline()
        if output == '' and opensim.process.poll() is not None:
            break
        if output:
            opensim.console_buffer.append(output.strip())
            print(output.strip())
            opensim.console_event.set()

            if 'Region' in output and not opensim.region_found:
                opensim.region_found = True
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Crear el archivo solo si no ha sido creado antes
                if not log_created and not os.path.exists(log_file):
                    with open(log_file, 'w') as file:
                        file.write(f"{timestamp} Servidor Iniciado\n")
                    log_created = True 
                    print(f"Found region, logged at {timestamp}")

                opensim.process.stdin.write("alert hola\n")
                opensim.process.stdin.flush()
