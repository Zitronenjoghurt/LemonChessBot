from typing import Optional
from src.api.api_controller import ApiController
from src.api.models.response_models import ApiKeyResponse
from src.constants.config import Config
from src.error import UnexpectedApiError, ExpectedApiError

API = ApiController.get_instance()
CONFIG = Config.get_instance()

async def register(id: str, name: str, display_name: str) -> ApiKeyResponse:
    """Registers a user.

    Args:
        id (str): The discord user id of the user to register
        name (str): The discord user name of the user

    Raises:
        UnecpectedApiError: On unexpected API response
        ValidationError: On invalid API response
        ApiConnectionError: On error while connecting to API.

    Returns:
        Optional[ApiKeyResponse]: Api key, if the user was registered, else None
    """
    response = await API.post(["user", "discord"], api_key=CONFIG.API_KEY, id=id, name=name, display_name=display_name)
    match response.status:
        case 200:
            return ApiKeyResponse.model_validate_json(response.content)
        case 400:
            raise ExpectedApiError(title="Already registered", message="Your discord user id is already linked to a LemonChess account.")
        case _:
            raise UnexpectedApiError(response)