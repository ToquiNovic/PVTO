# UA3DAPI/services/external_service.py
from fastapi import HTTPException
from UA3DAPI.external_api import ExternalAPIClient
from config.config import UA3D_USER, UA3D_PASS, UA3D_BACK

external_api_client = ExternalAPIClient(base_url=UA3D_BACK)

class ExternalService:
    access_token = None
    refresh_token = None

    @staticmethod
    async def authenticate():
        login_payload = {
            "username": UA3D_USER,
            "password": UA3D_PASS
        }
        response = await external_api_client.post_data("/auth/signin", json_data=login_payload)

        if response.get("accessToken"):
            ExternalService.access_token = response["accessToken"]
            ExternalService.refresh_token = response["refreshToken"]
            print(f"Autenticación exitosa. Access Token: {ExternalService.access_token}")
        else:
            raise HTTPException(status_code=400, detail="Error de autenticación: No se recibió el accessToken")

    @staticmethod
    async def get_authenticated_token():
        if ExternalService.access_token:
            return ExternalService.access_token
        else:
            await ExternalService.authenticate()
            return ExternalService.access_token
