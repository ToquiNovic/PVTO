# routes/fastapi_routes.py
from fastapi import HTTPException
from pydantic import BaseModel

class CommandRequest(BaseModel):
    command: str

def setup_routes(app, opensim):
    # Ruta para enviar comandos al servidor OpenSimulator
    @app.post("/send_command")
    async def send_command(command_request: CommandRequest):
        command = command_request.command
        
        # Validación de comando vacío
        if not command:
            raise HTTPException(status_code=400, detail="No command provided")
        
        # Enviar el comando a la instancia OpenSimulator
        result = await opensim.send_command(command)

        # Verifica si hay un error en el resultado
        if "Error" in result:
            raise HTTPException(status_code=400, detail=result)

        return {"message": result}