from typing import Optional
from src.constants.config import Config
from src.entities.chess_room import ChessRoom
from src.scrollables.abstract_query_scrollable import AbstractQueryScrollable

CONFIG = Config.get_instance()
PAGE_SIZE = 25

class ChessRoomScrollable(AbstractQueryScrollable):
    def __init__(self, page_size: int, starting_page: int = 1) -> None:
        super().__init__(page_size, starting_page)
        self.user_is_owner = False

    @staticmethod
    async def create(key: Optional[str] = None) -> 'ChessRoomScrollable':
        if isinstance(key, str):
            scrollable = await ChessRoomScrollable.create_from_find(
                entity_cls=ChessRoom,
                page_size=PAGE_SIZE,
                sort_key="created_stamp",
                descending=False,
                key=key
            )
            scrollable.user_is_owner = True
        else:
            scrollable = await ChessRoomScrollable.create_from_find(
                entity_cls=ChessRoom,
                page_size=PAGE_SIZE,
                sort_key="created_stamp",
                descending=False
            )
        return scrollable
    
    async def output(self) -> str:
        rooms: list[ChessRoom] = self.get_current_entities()
        if len(rooms) == 0:
            return "*no rooms*"
        
        strings = []
        for room in rooms:
            user_name = await room.get_owner_display_name()
            if self.user_is_owner:
                string = f"**`{room.code}`** | *{room.name}*"
            else:
                string = f"**`{room.code}`** | **{user_name}** | *{room.name}*"
            strings.append(string)
        return "\n".join(strings)