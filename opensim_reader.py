# opensim_reader.py
import re
import asyncio
from UA3DAPI.controllers.external_controller import ua3d_update_server_status
from config.config import OPENSIM_UUID, OPENSIM_PASS

async def noob_mode(opensim):
    try:
        print("🔧 Configurando el servidor OpenSimulator...")

        config_steps = {
            r"New estate name \[My Estate\]:": "UA3D\n",
            r"Estate owner first name \[Test\]:": "\n",
            r"Estate owner last name \[User\]:": "\n",
            r"Password:": f"{OPENSIM_PASS}\n", 
            r"Email:": "\n",
            r"User ID \[UUID\]:": f"{OPENSIM_UUID}\n"
        }

        while opensim.running:
            output = await asyncio.to_thread(opensim.process.stdout.readline)
            if not output:
                break

            output = output.strip()
            print(f"⚙️ OpenSimulator Output: {output}")

            for pattern, response in config_steps.items():
                if re.search(pattern, output):
                    print(f"📝 Respondiendo: {response.strip()}")
                    await send_console_command(opensim, response)

    except Exception as e:
        print(f"🚨 Error en noob_mode: {e}")

async def read_output(opensim, mode="default"):
    while opensim.running:
        output = await asyncio.to_thread(opensim.process.stdout.readline)
        if not output:
            break

        output = output.strip()
        print(f"🔹 OpenSimulator Output [{mode}]: {output}") 
        opensim.console_buffer.append(output)
        opensim.console_event.set()
        
        if mode == "nood":
            await noob_mode(opensim)
        else:
            if 'Region' in output and not opensim.region_found:
                opensim.region_found = True
                await send_console_command(opensim, "alert hola\n")
                await ua3d_update_server_status("ONLINE")

async def send_console_command(opensim, command):
    await asyncio.to_thread(opensim.process.stdin.write, command)  
    await asyncio.to_thread(opensim.process.stdin.flush)
