from src.api.api_controller import ApiController
from src.constants.config import Config

API = ApiController.get_instance()
CONFIG = Config.get_instance()

async def ping() -> bool:
    response = await API.get(endpoint_path=[""], api_key=CONFIG.API_KEY)
    return response.status == 200