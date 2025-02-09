# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opensim import start_opensim
from command_handler import log_region_found
import uvicorn
from threading import Thread

app = FastAPI()
process = start_opensim()

class CommandRequest(BaseModel):
    command: str

@app.post("/send_command")
async def send_command(command_request: CommandRequest):
    command = command_request.command
    if not command:
        raise HTTPException(status_code=400, detail="No command provided")
    process.stdin.write(command + "\n")
    process.stdin.flush()
    return {"message": f"Command '{command}' sent to OpenSimulator"}

def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=5000)
fastapi_thread = Thread(target=start_fastapi)
fastapi_thread.start()