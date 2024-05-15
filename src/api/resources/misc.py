from src.api.api_controller import ApiController
from src.constants.config import Config
from src.error import ApiConnectionError

API = ApiController.get_instance()
CONFIG = Config.get_instance()

async def ping() -> bool:
    try:
        response = await API.get(endpoint_path=[""], api_key=CONFIG.API_KEY)
    except ApiConnectionError:
        return False
    return response.status == 200