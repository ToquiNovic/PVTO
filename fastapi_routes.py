from fastapi import HTTPException
from pydantic import BaseModel

class CommandRequest(BaseModel):
    command: str

def setup_routes(app, opensim):
    @app.post("/send_command")
    async def send_command(command_request: CommandRequest):
        command = command_request.command
        if not command:
            raise HTTPException(status_code=400, detail="No command provided")

        opensim.send_command(command)
        return {"message": f"Command '{command}' sent to OpenSimulator"}
