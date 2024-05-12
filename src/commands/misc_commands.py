from discord.ext import commands

class MiscCommands(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        latency_ms = round(self.bot.latency * 1000)
        await ctx.send(f"**Pong!** {latency_ms}ms\n")

async def setup(bot):
    await bot.add_cog(MiscCommands(bot))