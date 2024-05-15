import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from src.api.resources.room import create_room
from src.error import ApiError
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
        if not await retrieve_discord_user(interaction=interaction):
            return
        await interaction.response.defer(ephemeral=not public)
        try:
            room = await create_room(api_key=chess_user.key, name=name, public=public)
        except ApiError as err:
            return await interaction.followup.send(embed=err.get_embed())
        
        public_text = " (or wait for someone to find your room with `/room list`)" if public else ""
        embed = discord.Embed(
            title="ROOM CREATED",
            description=f"*You can give this code to your friend{public_text}.\n\nThey can join you using `/room join`.*",
            color=discord.Color.green()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="NAME", value=f"**`{room.name}`**", inline=False)
        embed.add_field(name="CODE", value=f"**`{room.code}`**", inline=False)
        embed.add_field(name="PUBLIC", value=f"**`{room.public}`**")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RoomCommands(bot))