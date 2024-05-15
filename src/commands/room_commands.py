import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from src.entities.discord_user import DiscordUser
from src.ui.registration import retrieve_chess_user
from src.utils.user_operations import retrieve_discord_user

class RoomCommands(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    room_group = app_commands.Group(name="room", description="All commands about multiplayer rooms")

    @room_group.command(name="create", description="Create a multiplayer room")
    @app_commands.describe(name="The name you want to give your room")
    @app_commands.describe(public="If the room is supposed to be public or not. Defaults to true.")
    async def room_create(self, interaction: discord.Interaction, name: Optional[str] = None, public: bool = True):
        if not (chess_user := await retrieve_chess_user(interaction=interaction)):
            return
        if not (discord_user := await retrieve_discord_user(interaction=interaction)):
            return
        await discord_user.save()

async def setup(bot):
    await bot.add_cog(RoomCommands(bot))