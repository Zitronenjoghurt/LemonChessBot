from pydantic import Field
from src.db import Collection
from src.entities.database_entity import DatabaseEntity

class ChessRoom(DatabaseEntity):
    COLLECTION = Collection.CHESS_ROOMS
    key: str
    name: str
    code: str
    created_stamp: int
    public: bool