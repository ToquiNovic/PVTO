# UA3DAPI/controllers/external_controller.py
from fastapi import HTTPException
from UA3DAPI.services.external_service import ExternalService
from UA3DAPI.external_api import ExternalAPIClient
from config.config import UA3D_BACK

external_api_client = ExternalAPIClient(base_url=UA3D_BACK)

async def ua3d_update_server_status(name: str):
    token = await ExternalService.get_authenticated_token()

    headers = {"Authorization": f"Bearer {token}"}
    body = {"name": name}
    response = await external_api_client.patch_data("/server-status", json_data=body, headers=headers)

    if response.get("error"):
        raise HTTPException(status_code=500, detail=response["error"])

    return response
