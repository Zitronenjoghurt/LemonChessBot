from src.api.api_controller import ApiController
from src.constants.rendering_style import RenderingStyle
from src.error import ExpectedApiError, UnexpectedApiError

API = ApiController.get_instance()

async def render_board(file_path: str, session_id: str, api_key: str, style: RenderingStyle):
    """Renders the board and saves it at a designated path.

    Args:
        file_path (str): The path where the image is to be saved.
        session_id (str): The chess game session id.
        api_key (str): The API key that is to be used to generate the image.
        style (RenderingStyle): The style the image should be rendered in.

    Raises:
        UnexpectedApiError: On an unexpected api response.
        ApiConnectionError: On error while connecting to API.
    """
    await API.get_image(endpoint_path=["session", "render"], file_path=file_path, api_key=api_key, headers={"session-id": session_id}, style=style.value)

async def move(api_key: str, session_id: str, move_query: dict):
    response = await API.post(["session", "move"], api_key=api_key, headers={"session-id": session_id}, **move_query)
    match response.status:
        case 200:
            return
        case 400:
            raise ExpectedApiError(title="Invalid move", message="You can't play this move.")
        case _:
            raise UnexpectedApiError(response)