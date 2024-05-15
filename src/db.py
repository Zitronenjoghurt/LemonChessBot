from enum import Enum
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from src.constants.config import Config

CONFIG = Config.get_instance()

class Collection(Enum):
    NONE = ""
    CHESS_USERS = "users"
    CHESS_ROOMS = "rooms"
    CHESS_SESSIONS = "sessions"
    DISCORD_USERS = "discord_users"

class Database():
    _instance = None

    def __init__(self) -> None:
        if Database._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of Database.")
        self.client = AsyncIOMotorClient(CONFIG.DB_URL)
        self.db = self.client["LemonChess"]

    @staticmethod
    def get_instance() -> 'Database':
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance
    
    async def find_one(self, collection: Collection, **kwargs):
        return await self.db[collection.value].find_one(kwargs)
    
    async def find(self, collection: Collection, sort_key: Optional[str] = None, descending: bool = True, **kwargs):
        if isinstance(sort_key, str):
            designator = DESCENDING if descending else ASCENDING
            cursor = self.db[collection.value].find(kwargs).sort(sort_key, designator)
        else:
            cursor = self.db[collection.value].find(kwargs)
        return [document async for document in cursor]

    async def delete_one(self, collection: Collection, **kwargs) -> int:
        result = await self.db[collection.value].delete_one(kwargs)
        return result.deleted_count
    
    async def save(self, collection: Collection, document: dict) -> int:
        filter = {"_id": document["_id"]} if "_id" in document else {}
        result = await self.db[collection.value].replace_one(filter, document, upsert=True)
        return result.upserted_id if result.upserted_id is not None else result.modified_count