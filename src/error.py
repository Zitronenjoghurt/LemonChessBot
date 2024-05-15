import discord
from src.api.api_controller import ApiResponse
from src.ui.custom_embeds import ErrorEmbed

class ApiError(Exception):
    """Exception base class for api-related errors."""

    def get_embed(self) -> discord.Embed:
        return discord.Embed()

class UnexpectedApiError(ApiError):
    """Raised when the API returned an unexpected response."""
    
    def __init__(self, response: ApiResponse) -> None:
        super().__init__(f"Unexpected API response: [{response.status}] {response.content}")

    def get_embed(self) -> discord.Embed:
        return ErrorEmbed(title="API Error", message="An unexpected error occured while trying to request the LemonChess API. Please be patient and/or contact the developer.")

class ExpectedApiError(ApiError):
    """Raised when the API returned an expected response which still leads to a failed state."""

    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
        super().__init__(f"{title}: {message}")

    def get_embed(self) -> discord.Embed:
        return ErrorEmbed(title=self.title, message=self.message)