import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from src.api.resources.room import create_room, join_room
from src.entities.chess_room import ChessRoom
from src.error import ApiError
from src.scrollables.chess_room_scrollable import ChessRoomScrollable
from src.ui.custom_embeds import ErrorEmbed
from src.ui.paginated_embed import PaginatedEmbed, send_paginated
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

    @room_group.command(name="list", description="List all public multiplayer rooms")
    async def room_list(self, interaction: discord.Interaction):
        if not await retrieve_chess_user(interaction=interaction):
            return
        if not await retrieve_discord_user(interaction=interaction):
            return
        
        await interaction.response.defer()

        scrollable = await ChessRoomScrollable.create()
        embed = PaginatedEmbed(
            scrollable=scrollable,
            title="PUBLIC ROOMS",
            color=discord.Color.from_str("#8857bd")
        )
        await embed.initialize()

        await send_paginated(interaction=interaction, embed=embed)

    @room_group.command(name="own", description="List all of your own rooms")
    async def room_own(self, interaction: discord.Interaction):
        if not (chess_user := await retrieve_chess_user(interaction=interaction)):
            return
        if not await retrieve_discord_user(interaction=interaction):
            return
        
        await interaction.response.defer(ephemeral=True)

        scrollable = await ChessRoomScrollable.create(key=chess_user.key)
        embed = PaginatedEmbed(
            scrollable=scrollable,
            title="PUBLIC ROOMS",
            color=discord.Color.from_str("#8857bd")
        )
        await embed.initialize()

        await send_paginated(interaction=interaction, embed=embed)

    @room_group.command(name="join", description="Join a room using a code")
    @app_commands.describe(code="The code of the room you want to join")
    async def room_join(self, interaction: discord.Interaction, code: str):
        if not (chess_user := await retrieve_chess_user(interaction=interaction)):
            return
        if not (discord_user := await retrieve_discord_user(interaction=interaction)):
            return
        
        await interaction.response.defer(ephemeral=True)

        room = await ChessRoom.find_one(code=code)
        if not room:
            return await interaction.followup.send(embed=ErrorEmbed(title="Room not found", message="There is no open room with the specified code."))

        try:
            await join_room(api_key=chess_user.key, code=code)
        except ApiError as err:
            return await interaction.followup.send(embed=err.get_embed())
        
        embed = discord.Embed(
            title="GAME STARTED",
            description="*You successfully joined the room and the game has started.\nYou can use `/move` to play your move.*",
            color=discord.Color.green()
        )
        embed.set_footer(text="If this is your first time, check out /help to learn how to play the game.")
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="Game", value=f"**`{room.name}`**", inline=False)
        embed.add_field(name="Opponent", value=f"**`{await room.get_owner_display_name()}`**", inline=False)

        await interaction.followup.send(embed=embed)

        if not discord_user.has_played_once:
            discord_user.has_played_once = True
            await discord_user.save()

async def setup(bot):
    await bot.add_cog(RoomCommands(bot))