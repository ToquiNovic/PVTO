# UA3DAPI/external_api.py
import httpx

class ExternalAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def post_data(self, endpoint: str, json_data: dict) -> dict:
        try:
            response = await self.client.post(endpoint, json=json_data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error occurred: {e}"}
        except httpx.RequestError as e:
            return {"error": f"Error making request: {e}"}
        
    async def patch_data(self, endpoint: str, json_data: dict, headers: dict) -> dict:
        try:
            response = await self.client.patch(endpoint, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error occurred: {e}"}
        except httpx.RequestError as e:
            return {"error": f"Error making request: {e}"}

    async def close(self):
        await self.client.aclose()
