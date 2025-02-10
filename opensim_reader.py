# opensim_reader.py
import datetime
import os
import asyncio
from UA3DAPI.external_service import ExternalService

async def fetch_server_status(server_status: str):
    """Hace la petición a la ruta '/server-status' para obtener el estado del servidor"""
    try:
        # Llama al servicio externo para obtener el estado
        status = await ExternalService.get_server_status(server_status)

        # Imprime la respuesta en la consola
        print(f"Respuesta de la API para el estado del servidor: {status}")

        return status
    except Exception as e:
        print(f"Error al obtener el estado del servidor: {e}")
        return None

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

                # Crea un nuevo loop de eventos en este hilo
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                # Llama a la API para obtener el estado del servidor
                server_status = "RUNNING_SERVER" 
                loop.run_until_complete(fetch_server_status(server_status))
