from typing import Optional
from src.api.api_controller import ApiController
from src.api.models.response_models import RoomInfo
from src.error import UnexpectedApiError, ExpectedApiError

API = ApiController.get_instance()

async def create_room(api_key: str, name: Optional[str], public: Optional[bool]) -> RoomInfo:
    """Creates a new multiplayer room.

    Args:
        api_key (str): The api key of the user who is trying to create the room.
        name (Optional[str]): The name of the room.
        public (Optional[bool]): If the room should be public.

    Raises:
        ExpectedApiError: When the session limit is reached and the user can't create any more rooms.
        UnexpectedApiError: On an unexpected api response.

    Returns:
        RoomInfo: All important information about the newly created room.
    """
    if isinstance(name, str):
        response = await API.post(["room"], api_key=api_key, name=name, public=str(public).lower())
    else:
        response = await API.post(["room"], api_key=api_key, public=str(public).lower())
    match response.status:
        case 200:
            return RoomInfo.model_validate_json(response.content)
        case 400:
            raise ExpectedApiError(title="Session limit reached", message="You have reached your session limit and can't create another room yet.")
        case _:
            raise UnexpectedApiError(response)