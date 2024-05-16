from pydantic import Field
from src.db import Collection
from src.entities.database_entity import DatabaseEntity
from src.entities.settings import Settings

class DiscordUser(DatabaseEntity):
    COLLECTION = Collection.DISCORD_USERS
    user_id: str
    banned: bool = Field(default=False)
    ban_reason: str = Field(default="")
    settings: Settings = Field(default_factory=Settings)
    has_played_once: bool = Field(default=False) # Is false if the user never joined a sessioni