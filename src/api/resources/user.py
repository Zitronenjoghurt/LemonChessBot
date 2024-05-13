from typing import Optional
from src.api.api_controller import ApiController
from src.api.models.response_models import ApiKeyResponse
from src.error import UnecpectedApiError

API = ApiController.get_instance()

async def register(id: str, name: str) -> Optional[ApiKeyResponse]:
    """Registers a user.

    Args:
        id (str): The discord user id of the user to register
        name (str): The discord user name of the user

    Raises:
        UnecpectedApiError: On unexpected API response
        ValidationError: On invalid API response

    Returns:
        Optional[ApiKeyResponse]: Api key, if the user was registered, else None
    """
    response = await API.post(["user", "discord"], id=id, name=name)
    match response.status:
        case 200:
            return ApiKeyResponse.model_validate_json(response.content)
        case 400:
            return None
        case _:
            raise UnecpectedApiError(response)