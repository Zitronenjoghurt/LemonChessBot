import asyncio
from typing import Optional
from bson import ObjectId
from src.api.resources.session import render_board
from src.constants.rendering_style import RenderingStyle
from src.entities.chess_session import ChessSession
from src.utils.file_operations import get_image_api_path, file_exists, delete_file_if_exists

IMAGE_NAME = "{session_id}-{color}-{tick}-{style}.png"
IMAGE_API_URL = "https://image.lemon.industries/{file_name}"
    
async def retrieve_image_url(session_id: str, key: str, style: RenderingStyle = RenderingStyle.MODERN) -> Optional[str]:
    oid = ObjectId(session_id)
    session = await ChessSession.find_one(_id=oid)
    if not session: 
        return None
    
    color = session.get_color_by_key(key=key).value
    file_name = IMAGE_NAME.format(session_id=session_id, color=color, tick=session.game_state.tick, style=style.value)
    file_path = get_image_api_path(file_name=file_name)

    image_url = IMAGE_API_URL.format(file_name=file_name)

    if file_exists(file_path=file_path):
        return image_url
    
    await render_board(file_path=file_path, session_id=session_id, api_key=key, style=style)

    # Delete the previous image if it exists, it's not needed anymore
    asyncio.create_task(delete_old_images(session_id=session_id, color=color, tick=session.game_state.tick, style=style.value))

    return image_url

async def delete_old_images(session_id: str, color: int, tick: int, style: str):
    for i in range(tick - 1, -1, -1):
        file_name = IMAGE_NAME.format(session_id=session_id, color=color, tick=i, style=style)
        file_path = get_image_api_path(file_name=file_name)
        success = delete_file_if_exists(file_path=file_path)
        if success:
            break # It only has to delete once, but the last file can be of any previous tick