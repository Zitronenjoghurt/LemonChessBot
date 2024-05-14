from src.db import Collection
from src.entities.database_entity import DatabaseEntity

class DiscordUser(DatabaseEntity):
    COLLECTION = Collection.DISCORD_USERS
    user_id: str