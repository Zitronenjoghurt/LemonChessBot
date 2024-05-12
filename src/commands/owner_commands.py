from discord.ext import commands
from src.constants.config import Config
from src.logging.logger import LOGGER

CONFIG = Config.get_instance()

class OwnerCommands(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx: commands.Context):
        if str(ctx.author.id) != CONFIG.OWNER_ID:
            return
        await self.bot.tree.sync()
        await ctx.send("Application commands synced.")
        LOGGER.info("Synced application commands")

async def setup(bot):
    await bot.add_cog(OwnerCommands(bot))