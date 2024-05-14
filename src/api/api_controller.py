import aiohttp
from typing import Optional
from src.constants.config import Config

CONFIG = Config.get_instance()

class ApiResponse():
    def __init__(self, status: int, content: str) -> None:
        self.status = status
        self.content = content

class ApiController():
    _instance = None

    def __init__(self) -> None:
        if ApiController._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of ApiController.")

    @staticmethod
    def get_instance() -> 'ApiController':
        if ApiController._instance is None:
            ApiController._instance = ApiController()
        return ApiController._instance
    
    def generate_url(self, endpoint_path: list[str], **kwargs) -> str:
        endpoint = "/".join(endpoint_path)
        arguments = "&".join([f"{key}={value}" for key, value in kwargs.items()])
        if len(kwargs) > 0:
            return f"{CONFIG.API_URL}/{endpoint}?{arguments}"
        return f"{CONFIG.API_URL}/{endpoint}"
    
    def build_headers(self, additional_data: Optional[dict] = None) -> dict:
        headers = {
            'x-api-key': CONFIG.API_KEY
        }

        if isinstance(additional_data, dict):
            headers.update(additional_data)

        return headers

    async def get(self, endpoint_path: list[str], headers: Optional[dict] = None, **params) -> ApiResponse:
        url = self.generate_url(endpoint_path, **params)

        async with aiohttp.ClientSession(headers=self.build_headers(headers)) as session:
            async with session.get(url) as response:
                content = await response.text()
                return ApiResponse(response.status, content)
            
    async def post(self, endpoint_path: list[str], headers: Optional[dict] = None, **params) -> ApiResponse:
        url = self.generate_url(endpoint_path, **params)

        async with aiohttp.ClientSession(headers=self.build_headers(headers)) as session:
            async with session.post(url) as response:
                content = await response.text()
                return ApiResponse(response.status, content)