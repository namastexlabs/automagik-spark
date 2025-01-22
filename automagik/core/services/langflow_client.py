import httpx
from typing import Dict, Any, Optional, List

class LangflowClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}' if api_key else None
        }

    async def get_flows(self) -> List[Dict[str, Any]]:
        """Get all flows from Langflow server"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/api/v1/flows",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_flow(self, flow_id: str) -> Dict[str, Any]:
        """Get flow details by ID"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/api/v1/flows/{flow_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def run_flow(self, flow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run a flow with given inputs"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/api/v1/flows/{flow_id}/run",
                headers=self.headers,
                json=inputs
            )
            response.raise_for_status()
            return response.json()
