# UA3DAPI/controllers/external_controller.py
from fastapi import HTTPException
from UA3DAPI.services.external_service import ExternalService
from UA3DAPI.external_api import ExternalAPIClient
from config.config import UA3D_BACK, ID_SERVER

external_api_client = ExternalAPIClient(base_url=UA3D_BACK)

async def ua3d_update_server_status(name: str):
    try:
        print("🔄 Actualizando estado del servidor...")

        token = await ExternalService.get_authenticated_token()
        headers = {"Authorization": f"Bearer {token}"}
        status_body = {"name": name}

        # 🔹 Pedir el ID del nuevo estado
        status_response = await external_api_client.patch_data("/server-status", json_data=status_body, headers=headers)

        if not status_response or not isinstance(status_response, dict):
            raise HTTPException(status_code=500, detail="❌ Respuesta inesperada del servidor en /server-status")

        status_id = status_response.get("id")
        if not status_id:
            raise HTTPException(status_code=500, detail="❌ 'id' no encontrado en la respuesta de /server-status")

        print(f"✅ Estado obtenido: {status_response}")

        # 🔹 Actualizar el estado del servidor
        server_body = {
            "id": ID_SERVER,
            "statusId": status_id
        }

        server_response = await external_api_client.put_data("/servers", json_data=server_body, headers=headers)

        if not server_response or not isinstance(server_response, dict):
            raise HTTPException(status_code=500, detail="❌ Respuesta inesperada del servidor en /servers")

        print(f"✅ Estado del servidor actualizado: {server_response}")
        return server_response

    except Exception as e:
        print(f"🚨 Error en ua3d_update_server_status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def ua3d_get_server_status():
    try:
        print("📡 Obteniendo estado actual del servidor...")

        token = await ExternalService.get_authenticated_token()
        headers = {"Authorization": f"Bearer {token}"}

        server_response = await external_api_client.get_data(f"/servers/{ID_SERVER}", headers=headers)

        if not server_response or not isinstance(server_response, dict):
            raise HTTPException(status_code=500, detail="❌ Respuesta inesperada del servidor en /servers")

        print(f"🔍 Respuesta del servidor: {server_response}")

        return server_response 

    except Exception as e:
        print(f"🚨 Error en ua3d_get_server_status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_opensim_mode():
    try:
        server_data = await ua3d_get_server_status()

        if not isinstance(server_data, dict):
            print("⚠️ Advertencia: La respuesta del servidor no es válida.")
            return "default"

        # Extraer el estado del servidor
        server_status = server_data.get("status", {}).get("name", "")

        # Retornar el modo en función del estado
        return "noob" if server_status == "SERVER_CONFIGURATION_COMPLETED" else "default"

    except Exception as e:
        print(f"🚨 Error al verificar el estado del servidor: {e}")
        return "default"
