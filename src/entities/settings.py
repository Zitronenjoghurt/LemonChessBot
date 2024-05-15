from typing import Optional
from pydantic import BaseModel, Field

class Settings(BaseModel):
    notify_new_session: bool = Field(default = False) # Notify when someone joins your room
    notify_move: bool = Field(default = False)        # Notify when opponent moves

    def update(self, notify_new_session: Optional[bool], notify_move: Optional[bool]) -> bool:
        updated = False

        if isinstance(notify_new_session, bool):
            self.notify_new_session = notify_new_session
            updated = True
        if isinstance(notify_move, bool):
            self.notify_move = notify_move
            updated = True

        return updated
    
    def get_fields(self) -> list[tuple[str, str]]:
        return [
            ("Notify on game start", on_off(self.notify_new_session)),
            ("Notify on opponent move", on_off(self.notify_move))
        ]

def on_off(value: bool) -> str:
    return "On" if value else "Off"