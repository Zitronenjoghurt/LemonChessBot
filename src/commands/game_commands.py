import discord
from discord import app_commands
from discord.ext import commands
from src.entities.chess_session import ChessSession
from src.entities.chess_user import ChessUser
from src.ui.custom_embeds import ErrorEmbed
from src.ui.registration import retrieve_chess_user
from src.utils.user_operations import retrieve_discord_user

class GameCommands(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @app_commands.command(name="game", description="Shows you the board and information about a game")
    @app_commands.describe(name="The name of the game.")
    async def game(self, interaction: discord.Interaction, name: str):
        if not await retrieve_chess_user(interaction=interaction):
            return
        if not (discord_user := await retrieve_discord_user(interaction=interaction)):
            return
        
        await interaction.response.defer(ephemeral=True)

        session = await ChessSession.find_by_name(name=name)
        if not session:
            return await interaction.followup.send(embed=ErrorEmbed(title="Game not found", message="The provided name doesn't fit to any of your games."))
        
        # ToDo: Show game board and info

    @game.autocomplete("name")
    async def game_names(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
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