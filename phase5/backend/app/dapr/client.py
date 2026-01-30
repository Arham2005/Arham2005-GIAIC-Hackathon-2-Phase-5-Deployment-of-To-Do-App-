import aiohttp
import json
from typing import Dict, Any, Optional
import os


class DaprClient:
    def __init__(self):
        self.dapr_http_port = os.getenv("DAPR_HTTP_PORT", "3500")
        self.dapr_grpc_port = os.getenv("DAPR_GRPC_PORT", "50001")
        self.base_url = f"http://localhost:{self.dapr_http_port}"

    async def publish_event(self, pubsub_name: str, topic_name: str, data: Dict[str, Any]):
        """Publish an event to Dapr pub/sub"""
        url = f"{self.base_url}/v1.0/publish/{pubsub_name}/{topic_name}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        print(f"Event published to {pubsub_name}/{topic_name}: {data}")
                        return True
                    else:
                        print(f"Failed to publish event: {response.status}")
                        return False
            except Exception as e:
                print(f"Error publishing event: {e}")
                return False

    async def save_state(self, store_name: str, key: str, value: Any):
        """Save state using Dapr state management"""
        url = f"{self.base_url}/v1.0/state/{store_name}"

        state_item = {
            "key": key,
            "value": value
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=[state_item]) as response:
                    if response.status == 200:
                        print(f"State saved: {store_name}/{key}")
                        return True
                    else:
                        print(f"Failed to save state: {response.status}")
                        return False
            except Exception as e:
                print(f"Error saving state: {e}")
                return False

    async def get_state(self, store_name: str, key: str) -> Optional[Any]:
        """Get state using Dapr state management"""
        url = f"{self.base_url}/v1.0/state/{store_name}/{key}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"State retrieved: {store_name}/{key}")
                        return data
                    elif response.status == 404:
                        print(f"State not found: {store_name}/{key}")
                        return None
                    else:
                        print(f"Failed to get state: {response.status}")
                        return None
            except Exception as e:
                print(f"Error getting state: {e}")
                return None

    async def invoke_binding(self, binding_name: str, operation: str, data: Dict[str, Any] = None):
        """Invoke a Dapr binding"""
        url = f"{self.base_url}/v1.0/bindings/{binding_name}"

        payload = {
            "operation": operation
        }

        if data:
            payload["data"] = data

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        print(f"Binding invoked: {binding_name} ({operation})")
                        result = await response.json()
                        return result
                    else:
                        print(f"Failed to invoke binding: {response.status}")
                        return None
            except Exception as e:
                print(f"Error invoking binding: {e}")
                return None


# Global Dapr client instance
dapr_client = DaprClient()