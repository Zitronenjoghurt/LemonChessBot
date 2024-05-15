import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from src.api.resources.misc import ping
from src.ui.registration import retrieve_chess_user
from src.utils.user_operations import retrieve_discord_user

class MiscCommands(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        latency_ms = round(self.bot.latency * 1000)
        ping_success = await ping()
        api_availability = "Online" if ping_success else "Offline"
        embed = discord.Embed(
            title="PONG",
            color=discord.Color.green() if ping_success else discord.Color.red()
        )
        embed.add_field(name="Bot Latency", value=f"**`{latency_ms}ms`**", inline=False)
        embed.add_field(name="LemonChess API", value=f"**`{api_availability}`**", inline=False)
        await ctx.send(embed=embed)
    
    @app_commands.command(name="settings", description="Adjust different bot settings")
    @app_commands.describe(nofity_new_session="If you should be notified when someone joins one of your rooms.")
    @app_commands.describe(notify_move="If you should be notified when an opponent plays a move.")
    async def settings(self, interaction: discord.Interaction, nofity_new_session: Optional[bool] = None, notify_move: Optional[bool] = None):
        if not await retrieve_chess_user(interaction=interaction):
            return
        if not (discord_user := await retrieve_discord_user(interaction=interaction)):
            return
        
        await interaction.response.defer(ephemeral=True)

        updated = discord_user.settings.update(notify_new_session=nofity_new_session, notify_move=notify_move)
        if updated:
            await discord_user.save()

        embed = discord.Embed(
            title="SETTINGS UPDATED" if updated else "SETTINGS",
            color=discord.Color.green() if updated else discord.Color.light_gray()
        )

        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        for name, value in discord_user.settings.get_fields():
            embed.add_field(name=name, value=f"**`{value}`**", inline=False)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MiscCommands(bot))