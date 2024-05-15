import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from src.ui.registration import check_registration

class RoomCommands(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    room_group = app_commands.Group(name="room", description="All commands about multiplayer rooms")

    @room_group.command(name="create", description="Create a multiplayer room")
    @app_commands.describe(name="The name you want to give your room")
    @app_commands.describe(public="If the room is supposed to be public or not. Defaults to true.")
    async def room_create(self, interaction: discord.Interaction, name: Optional[str] = None, public: bool = True):
        if not await check_registration(interaction=interaction):
            return

async def setup(bot):
    await bot.add_cog(RoomCommands(bot))