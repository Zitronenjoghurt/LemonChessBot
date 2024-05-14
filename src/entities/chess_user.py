from pydantic import Field
from src.db import Collection
from src.entities.database_entity import DatabaseEntity

class ChessUser(DatabaseEntity):
    COLLECTION = Collection.CHESS_USERS
    key: str
    name: str
    display_name: str
    created_stamp: int
    last_access_stamp: int
    permission: str
    discord_id: str
    endpoint_usage: dict[str, int]
    rate_limiting: dict[str, int]