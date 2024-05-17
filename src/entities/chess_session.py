from typing import Optional
from bson import ObjectId
from pydantic import Field
from src.constants.color import ChessColor
from src.db import Collection, Database
from src.entities.database_entity import DatabaseEntity
from src.entities.game_state import GameState

DB = Database.get_instance()

class ChessSession(DatabaseEntity):
    COLLECTION = Collection.CHESS_SESSIONS
    id: ObjectId = Field(..., alias='_id')
    name: str
    keys: list[str]
    created_stamp: int
    game_state: GameState

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed=True

    @staticmethod
    async def find_by_name(name: str) -> Optional['ChessSession']:
        cursor = DB.db[ChessSession.COLLECTION.value].find(
            { "$text": { "$search": name } },
            { "score": { "$meta": "textScore" } }
        ).sort([("score", {"$meta": "textScore"})])
        results = [document async for document in cursor]
        if not results:
            return None
        return ChessSession.model_validate(results[0])

    @staticmethod
    async def find_running(key: str) -> list['ChessSession']:
        filter = {"keys": key, "game_state.winner": 2, "game_state.draw": False}
        return await ChessSession.find(filter=filter)
    
    def get_color_by_key(self, key: str) -> ChessColor:
        try:
            index = self.keys.index(key)
        except IndexError:
            index = 0
        if index == 1:
            return ChessColor.BLACK
        return ChessColor.WHITE