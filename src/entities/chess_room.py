from src.db import Collection
from src.entities.chess_user import ChessUser
from src.entities.database_entity import DatabaseEntity

class ChessRoom(DatabaseEntity):
    COLLECTION = Collection.CHESS_ROOMS
    key: str
    name: str
    code: str
    created_stamp: int
    public: bool

    async def get_owner_display_name(self) -> str:
        user = await ChessUser.find_one(key=self.key)
        if not user:
            return "DELETED USER"
        return user.display_name