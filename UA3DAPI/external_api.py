# UA3DAPI/external_api.py
import httpx

class ExternalAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def post_data(self, endpoint: str, json_data: dict) -> dict:
        url = f"{self.base_url}{endpoint}"
        print(f"POST {url} con datos: {json_data}")
        try:
            response = await self.client.post(endpoint, json=json_data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"⚠️ HTTP Status Error en {url}: {e.response.status_code} - {e.response.text}")
            return {"error": f"HTTP error: {e.response.status_code}"}
        except httpx.RequestError as e:
            print(f"⚠️ Error de conexión en {url}: {e}")
            return {"error": f"Request error: {e}"}
        except Exception as e:
            print(f"⚠️ Error inesperado en {url}: {e}")
            return {"error": f"Unexpected error: {e}"}

    async def patch_data(self, endpoint: str, json_data: dict, headers: dict) -> dict:
        url = f"{self.base_url}{endpoint}"
        print(f"PATCH {url} con datos: {json_data} y headers: {headers}")
        try:
            response = await self.client.patch(endpoint, json=json_data, headers=headers)
            response.raise_for_status()
            print(f"✅ PATCH Response ({response.status_code}): {response.text}")
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"⚠️ HTTP Status Error en {url}: {e.response.status_code} - {e.response.text}")
            return {"error": f"HTTP error: {e.response.status_code}"}
        except httpx.RequestError as e:
            print(f"⚠️ Error de conexión en {url}: {e}")
            return {"error": f"Request error: {e}"}
        except Exception as e:
            print(f"⚠️ Error inesperado en {url}: {e}")
            return {"error": f"Unexpected error: {e}"}

    async def put_data(self, endpoint: str, json_data: dict, headers: dict = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        print(f"PUT {url} con datos: {json_data} y headers: {headers}")
        try:
            response = await self.client.put(endpoint, json=json_data, headers=headers)
            response.raise_for_status()
            print(f"✅ PUT Response ({response.status_code}): {response.text}")
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"⚠️ HTTP Status Error en {url}: {e.response.status_code} - {e.response.text}")
            return {"error": f"HTTP error: {e.response.status_code}"}
        except httpx.RequestError as e:
            print(f"⚠️ Error de conexión en {url}: {e}")
            return {"error": f"Request error: {e}"}
        except Exception as e:
            print(f"⚠️ Error inesperado en {url}: {e}")
            return {"error": f"Unexpected error: {e}"}

    async def close(self):
        await self.client.aclose()

    async def get_data(self, endpoint: str, headers: dict = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        print(f"GET {url} con headers: {headers}")
        try:
            response = await self.client.get(endpoint, headers=headers)
            response.raise_for_status()
            print(f"✅ GET Response ({response.status_code}): {response.text}")
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"⚠️ HTTP Status Error en {url}: {e.response.status_code} - {e.response.text}")
            return {"error": f"HTTP error: {e.response.status_code}"}
        except httpx.RequestError as e:
            print(f"⚠️ Error de conexión en {url}: {e}")
            return {"error": f"Request error: {e}"}
        except Exception as e:
            print(f"⚠️ Error inesperado en {url}: {e}")
            return {"error": f"Unexpected error: {e}"}
