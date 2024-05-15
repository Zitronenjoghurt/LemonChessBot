import discord
from discord import ui
from typing import Optional
from src.api.models.response_models import ApiKeyResponse
from src.api.resources.user import register
from src.entities.chess_user import ChessUser
from src.error import UnexpectedApiError
from src.ui.custom_embeds import ErrorEmbed, SuccessEmbed

async def retrieve_chess_user(interaction: discord.Interaction) -> Optional[ChessUser]:
    """Checks if the user is already registered for LemonChess.

    Args:
        interaction (discord.Interaction): The current interaction as context.

    Returns:
        Optional[ChessUser]: The LemonChess user. Returns None if the user was not registered yet.
    """
    user = await ChessUser.find_one(discord_id=str(interaction.user.id))
    if isinstance(user, ChessUser):
        return user
    
    embed = RegistrationEmbed()
    confirm_view = RegistrationConfirmView(interaction.user.id, timeout=120)
    await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=True)
    confirm_view.message = await interaction.original_response()
    timed_out = await confirm_view.wait()

    if confirm_view.confirmed:
        embed.title = "REGISTRATION ACCEPTED"
        embed.color = discord.Color.green()
    elif timed_out:
        embed.title = "REGISTRATION TIMED OUT"
        embed.color = discord.Color.dark_gray()
    else:
        embed.title = "REGISTRATION CANCELLED"
        embed.color = discord.Color.red()
    await interaction.edit_original_response(embed=embed)

class RegistrationEmbed(discord.Embed):
    def __init__(self) -> None:
        description = "**If you accept, your discord user name and id will be used to identify you as a LemonChess player.\nAny misuse of the bot or its features, including profanity or bad sportsmanship, will lead to a permanent ban from all bot features.\n\nClicking on the confirm button will lead you to a pop-up, where you can type in your desired display name.\nIf you got an Api-Key for LemonChess, you can also input it there to link your account with your discord user id.**"
        super().__init__(color=discord.Color.from_str("#FCD056"), title="INITIAL REGISTRATION", description=description)
        self.set_author(name="LemonChess")

import discord
from discord.ui import Button, View
from typing import Optional

class RegistrationConfirmView(View):
    def __init__(self, user_id: int, timeout: float = 180, **kwargs):
        super().__init__(timeout=timeout, **kwargs)
        self.user_id = user_id
        self.confirmed = False

        # Appending the message this view was attached to 
        # makes it possible to disable the buttons on timeout
        self.message: Optional[discord.InteractionMessage] = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        self.confirmed = True
        self.disable_buttons()
        if isinstance(self.message, discord.InteractionMessage):
            await self.message.edit(view=self)
        self.stop()
        modal = RegistrationModal(interaction.user)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        self.confirmed = False
        self.disable_buttons()
        await interaction.response.edit_message(view=self)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id

    async def on_timeout(self) -> None:
        self.confirmed = False
        self.disable_buttons()
        if isinstance(self.message, discord.InteractionMessage):
            await self.message.edit(view=self)

    def disable_buttons(self) -> None:
        for child in self.children:
            if isinstance(child, Button):
                child.disabled = True

class RegistrationModal(ui.Modal):
    def __init__(self, user: discord.User | discord.Member) -> None:
        super().__init__(
            title="Finish registration"
        )
        self.user = user

        self.display_name = ui.TextInput(label="Display name", placeholder="The name other players will see.", required=True, min_length=3, max_length=64, style=discord.TextStyle.short)
        self.add_item(self.display_name)

        self.api_key = ui.TextInput(label="Api Key", placeholder="If you already have an API key, you can link your account by putting it in here.", required=False, min_length=32, max_length=32, style=discord.TextStyle.short)
        self.add_item(self.api_key)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            response = await register(id=str(self.user.id), name=self.user.name, display_name=self.display_name.value)
            if not isinstance(response, ApiKeyResponse):
                await interaction.response.send_message(embed=ErrorEmbed(title="Already registered", message="Your discord user id is already linked to a LemonChess account."), ephemeral=True)
                return
            
            await interaction.response.send_message(embed=SuccessEmbed(title="Successfully registered", message="Your discord account was successfully linked to a LemonChess account.\nYou can now use all bot features."), ephemeral=True)

        except UnexpectedApiError:
            await interaction.response.send_message(embed=ErrorEmbed.unexpected_api_error(), ephemeral=True)