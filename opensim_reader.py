# opensim_reader.py
import datetime
import os
import asyncio
from UA3DAPI.controllers.external_controller import ua3d_update_server_status

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

                if not log_created and not os.path.exists(log_file):
                    with open(log_file, 'w') as file:
                        file.write(f"{timestamp} Servidor Iniciado\n")
                    log_created = True 
                    print(f"Found region, logged at {timestamp}")

                opensim.process.stdin.write("alert hola\n")
                opensim.process.stdin.flush()

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    status = loop.run_until_complete(ua3d_update_server_status("CREATING_SERVER"))
                    if status:
                        print(f"Estado del servidor actualizado en la BD: {status}")
                except Exception as e:
                    print(f"Error al actualizar el estado del servidor: {e}")
                finally:
                    loop.close()

    print("🛑 OpenSimulator se ha detenido. Actualizando estado en la BD...")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        status = loop.run_until_complete(ua3d_update_server_status("OFFLINE"))
        if status:
            print(f"Estado del servidor actualizado a OFFLINE en la BD: {status}")
    except Exception as e:
        print(f"Error al actualizar el estado del servidor a OFFLINE: {e}")
    finally:
        loop.close()
