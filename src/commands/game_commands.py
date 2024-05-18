from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
from src.api.resources.session import move
from src.board_image_handler import retrieve_image_url
from src.constants.color import ChessColor
from src.entities.chess_session import ChessSession
from src.entities.chess_user import ChessUser
from src.error import ApiError
from src.ui.custom_embeds import ErrorEmbed
from src.ui.registration import retrieve_chess_user
from src.utils.chess import is_valid_chess_cell
from src.utils.user_operations import retrieve_discord_user

class GameCommands(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @app_commands.command(name="game", description="Shows you the board and information about a game.")
    @app_commands.describe(name="The name of the game.")
    async def game(self, interaction: discord.Interaction, name: str):
        if not (chess_user := await retrieve_chess_user(interaction=interaction)):
            return
        if not await retrieve_discord_user(interaction=interaction):
            return
        
        await interaction.response.defer()

        session = await ChessSession.find_by_name(name=name)
        if not session:
            return await interaction.followup.send(embed=ErrorEmbed(title="Game not found", message="The provided name doesn't fit to any of your games."))
        
        image_url = await retrieve_image_url(session_id=str(session.id), key=chess_user.key)

        embed = discord.Embed(
            title=session.name,
            color=discord.Color.from_str("#FAAF4D")
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.set_image(url=image_url)

        if chess_user.key in session.keys:
            index = session.keys.index(chess_user.key)
            color = ChessColor(index)
            embed.add_field(name="YOUR COLOR", value=f"**`{color.name}`**", inline=False)
        
        embed.add_field(name="STATUS", value=session.get_status(key=chess_user.key), inline=False)
        embed.add_field(name="LAST MOVE", value=session.get_last_move(), inline=False)

        embed.set_footer(text="Use /move to play")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="move", description="Move in a game.")
    @app_commands.describe(name="The name of the game you want to move in.")
    @app_commands.describe(source="The cell the piece you want to move is placed.")
    @app_commands.describe(target="The target cell you want to move your piece to.")
    @app_commands.describe(castle_kingside="If you want to castle king-side.")
    @app_commands.describe(castle_queenside="If you want to castle queen-side.")
    async def move(self, interaction: discord.Interaction, name: str, source: Optional[str] = None, target: Optional[str] = None, castle_kingside: bool = False, castle_queenside: bool = False):
        if not (chess_user := await retrieve_chess_user(interaction=interaction)):
            return
        if not await retrieve_discord_user(interaction=interaction):
            return
        
        await interaction.response.defer()
        
        session = await ChessSession.find_by_name(name=name)
        if not session:
            return await interaction.followup.send(embed=ErrorEmbed(title="Game not found", message="The provided name doesn't fit to any of your games."))
        
        if chess_user.key not in session.keys:
            return await interaction.followup.send(embed=ErrorEmbed(title="Not a participant", message="You are not a participant of this game."))
        
        if chess_user.key != session.keys[session.game_state.next_to_move]:
            return await interaction.followup.send(embed=ErrorEmbed(title="Please wait", message="It's not your turn."))
        
        if (not source or not target) and (not castle_kingside and not castle_queenside):
            return await interaction.followup.send(embed=ErrorEmbed(title="Invalid move", message="You did not provide enough move information. Make sure you either provide source and target cell of your move OR castle kingside/queenside."))

        if castle_kingside and castle_queenside:
            return await interaction.followup.send(embed=ErrorEmbed(title="Invalid move", message="You can't castle king and queenside at the same time."))

        if isinstance(source, str) and not is_valid_chess_cell(source.lower()):
            return await interaction.followup.send(embed=ErrorEmbed(title="Invalid move", message="The provided source cell is invalid, valid cells look like `e2`, `A6`, `b3`..."))
        
        if isinstance(target, str) and not is_valid_chess_cell(target.lower()):
            return await interaction.followup.send(embed=ErrorEmbed(title="Invalid move", message="The provided target cell is invalid, valid cells look like `e2`, `A6`, `b3`..."))
        
        query: dict = {
            "castle_kingside": str(castle_kingside).lower(),
            "castle_queenside": str(castle_queenside).lower()
        }

        if isinstance(source, str) or isinstance(target, str):
            query["from"] = source
            query["to"] = target

        try:
            await move(api_key=chess_user.key, session_id=str(session.id), move_query=query)
        except ApiError as err:
            return await interaction.followup.send(embed=err.get_embed())
        
        embed = discord.Embed(
            title="MOVE PLAYED",
            description="*You can view the board using `/game`*",
            color=discord.Color.green()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        await interaction.followup.send(embed=embed)

    @game.autocomplete("name")
    @move.autocomplete("name")
    async def game_names_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        user = await ChessUser.find_one(discord_id=str(interaction.user.id))
        if not user:
            return []
        sessions = await ChessSession.find_running(user.key)
        return [
            app_commands.Choice(name=name, value=name)
            for name in [session.name for session in sessions]
            if current.lower() in name.lower()
        ]

async def setup(bot):
    await bot.add_cog(GameCommands(bot))