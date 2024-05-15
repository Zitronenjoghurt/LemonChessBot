import discord
from typing import Optional
from src.entities.discord_user import DiscordUser
from src.ui.custom_embeds import ErrorEmbed

async def retrieve_discord_user(interaction: discord.Interaction) -> Optional[DiscordUser]:
    """Retrieves a discord user and executes important procedures such as checking if the user is banned.

    Args:
        interaction (discord.Interaction): The current interaction as context.

    Returns:
        Optional[DiscordUser]: The discord user, returns None if the user is banned.
    """
    user = await DiscordUser.load(user_id=str(interaction.user.id))

    if user.banned:
        await interaction.response.send_message(embed=ErrorEmbed(title="Account deactivated", message=f"**Your LemonChess account was deactivated by an Administrator.**\n\nReason: **`{user.ban_reason}`**"), ephemeral=True)
        return
    
    return user