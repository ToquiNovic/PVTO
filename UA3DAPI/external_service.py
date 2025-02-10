# external_service.py
import time
from UA3DAPI.external_api import ExternalAPIClient
from config.config import UA3D_USER, UA3D_PASS, UA3D_BACK

# Crea una instancia del cliente API externa
external_api_client = ExternalAPIClient(base_url=UA3D_BACK)

class ExternalService:
    access_token = None
    refresh_token = None
    access_token_expiry = None

    @staticmethod
    async def authenticate():
        login_payload = {
            "username": UA3D_USER,
            "password": UA3D_PASS
        }
        response = await external_api_client.post("/auth/signin", json_data=login_payload)

        # Almacena los tokens y la expiración del accessToken
        if response.get("accessToken"):
            ExternalService.access_token = response["accessToken"]
            ExternalService.refresh_token = response["refreshToken"]
            ExternalService.access_token_expiry = time.time() + 3600  # El token expira en 1 hora
        else:
            raise Exception("Error al autenticar: No se recibió el accessToken.")

    @staticmethod
    async def ensure_access_token():
        """Verifica si el token está expirado y lo obtiene de nuevo si es necesario"""
        if ExternalService.access_token is None or time.time() > ExternalService.access_token_expiry:
            if ExternalService.refresh_token:  # Si ya existe un refresh token
                await ExternalService.refresh_access_token()
            else:  # Si no, realiza una nueva autenticación
                await ExternalService.authenticate()

    @staticmethod
    async def refresh_access_token():
        """Renueva el access token usando el refresh token"""
        if not ExternalService.refresh_token:
            raise Exception("No refresh token disponible. No se puede refrescar el access token.")
        
        refresh_payload = {
            "refreshToken": ExternalService.refresh_token
        }
        response = await external_api_client.post("/auth/refresh", json_data=refresh_payload)

        if response.get("accessToken"):
            ExternalService.access_token = response["accessToken"]
            ExternalService.access_token_expiry = time.time() + 3600  # El token expira en 1 hora
        else:
            raise Exception("Error al refrescar el token: No se recibió el accessToken.")

    @staticmethod
    async def get_server_status(server_name: str):
        """Obtiene el estado del servidor después de asegurarse de que el access token esté vigente"""
        await ExternalService.ensure_access_token()  # Asegura que el token sea válido

        headers = {
            "Authorization": f"Bearer {ExternalService.access_token}"
        }

        # Realiza la petición PATCH para obtener el estado del servidor
        response = await external_api_client.patch_data("/server-status", json_data={"name": server_name}, headers=headers)

        if "error" in response:
            raise Exception(f"Error al obtener el estado del servidor: {response['error']}")

        return response
