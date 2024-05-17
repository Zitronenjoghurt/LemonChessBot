from enum import Enum
from typing import Optional
from bson import ObjectId
from src.api.resources.session import render_board
from src.constants.rendering_style import RenderingStyle
from src.entities.chess_session import ChessSession
from src.utils.file_operations import get_image_api_path, file_exists

IMAGE_NAME = "{session_id}-{color}-{tick}-{style}.png"
IMAGE_API_URL = "https://image.lemon.industries/{file_name}"
    
async def retrieve_image_url(session_id: str, key: str, style: RenderingStyle = RenderingStyle.MODERN) -> Optional[str]:
    oid = ObjectId(session_id)
    session = await ChessSession.find_one(_id=oid)
    if not session:
        return None
    
    file_name = IMAGE_NAME.format(session_id=session_id, color=session.get_color_by_key(key=key).value, tick=session.game_state.tick, style=style.value)
    file_path = get_image_api_path(file_name=file_name)

    image_url = IMAGE_API_URL.format(file_name=file_name)

    if file_exists(file_path=file_path):
        return image_url
    
    await render_board(file_path=file_path, session_id=session_id, api_key=key, style=style)
    return image_url