# fastapi_routes.py
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

        # Espera correctamente la corutina
        result = await opensim.send_command(command)

        # Verifica si hay un error en el resultado
        if "Error" in result:
            raise HTTPException(status_code=400, detail=result)

        return {"message": result}
