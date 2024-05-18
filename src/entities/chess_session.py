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
    
    def get_status(self, key: str) -> str:
        is_player = key in self.keys
        color = self.get_color_by_key(key=key)

        information = []
        if self.game_state.is_ongoing():
            if is_player and color.value == self.game_state.next_to_move:
                information.append("**`YOUR turn`**")
            else:
                information.append(f"**`{color.name} to move`**")

            if self.game_state.check_states[0]:
                if is_player and color == ChessColor.WHITE:
                    information.append("You are check")
                else:
                    information.append("White is check")

            if self.game_state.check_states[1]:
                if is_player and color == ChessColor.BLACK:
                    information.append("You are check")
                else:
                    information.append("Black is check")

        else:
            if self.game_state.draw:
                information.append("**`DRAW`**")
            else:
                win_color = ChessColor(self.game_state.winner)
                information.append(f"**`{win_color.name} WON`**")
            if self.game_state.checkmate:
                information.append("by **Checkmate**")
            elif self.game_state.resign:
                information.append("by **Resignation**")
            elif self.game_state.stalemate:
                information.append("by **Stalemate**")
            elif self.game_state.remis:
                information.append("by **50-Remis Rule**")

        return "\n".join(information)
    
    def get_last_move(self) -> str:
        return self.game_state.last_san_to_description()