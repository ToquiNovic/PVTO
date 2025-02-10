# fastapi_routes.py
from fastapi import HTTPException
from pydantic import BaseModel
from UA3DAPI.external_service import ExternalService 

class CommandRequest(BaseModel):
    command: str

class ServerStatusRequest(BaseModel):
    name: str

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

    @app.patch("/server-status")
    async def update_server_status(server_status_request: ServerStatusRequest):
        name = server_status_request.name

        if not name:
            raise HTTPException(status_code=400, detail="No server name provided")

        # Llama a ExternalService para obtener el estado del servidor
        try:
            status = await ExternalService.get_server_status(name)
            
            if not status:
                raise HTTPException(status_code=404, detail="Server not found or status unavailable")
            
            # Si el servidor tiene un estado válido, retornamos el estado
            return {"server_name": name, "status": status}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching server status: {str(e)}")
