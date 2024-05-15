import discord

class SuccessEmbed(discord.Embed):
    def __init__(self, title: str, message: str) -> None:
        super().__init__(title=title, description=message, color=discord.Color.from_str("#48c744"))

class ErrorEmbed(discord.Embed):
    def __init__(self, title: str, message: str) -> None:
        super().__init__(title=title, description=message, color=discord.Color.from_str("#c9042f"))

    @staticmethod
    def unexpected_api_error() -> 'ErrorEmbed':
        return ErrorEmbed(title="API Error", message="An unexpected error occured while trying to request the LemonChess API. Please be patient and/or contact the developer.")