import discord

class SuccessEmbed(discord.Embed):
    def __init__(self, title: str, message: str) -> None:
        super().__init__(title=title, description=message, color=discord.Color.green())

class ErrorEmbed(discord.Embed):
    def __init__(self, title: str, message: str) -> None:
        super().__init__(title=title, description=message, color=discord.Color.red())