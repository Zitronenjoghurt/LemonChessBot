import asyncio
import discord
from discord.ui import Button, View
from typing import Optional
from src.scrollables.abstract_scrollable import AbstractScrollable

async def send_paginated(interaction: discord.Interaction, embed: 'PaginatedEmbed', timeout_after: int = 180):
    """Always sends the scrollable as a followup.
    """
    if embed.scrollable.is_scrollable():
        paginated_view = PaginatedView(embed=embed, user_id=interaction.user.id)
        await interaction.followup.send(embed=embed, view=paginated_view)
        paginated_view.message = await interaction.original_response()
        await paginated_view.timeout_after(timeout_after)
    else:
        await interaction.followup.send(embed=embed)

class PaginatedEmbed(discord.Embed):
    def __init__(
            self,
            scrollable,
            title: Optional[str] = None,
            color: Optional[discord.Colour] = None,
            author: Optional[str] = None,
            icon_url: Optional[str] = None
        ) -> None:
        if not isinstance(scrollable, AbstractScrollable):
            raise RuntimeError(f"Tried to initialize scrollable embed but given scrollable is invalid.")
        super().__init__(title=title, color=color)
        
        self.scrollable = scrollable
        if author:
            self.set_author(name=author, icon_url=icon_url)

    def is_scrollable(self) -> bool:
        return self.scrollable.is_scrollable()
    
    def time_out(self) -> None:
        self.color = discord.Color.dark_grey()
        self.set_footer(text="This interaction has timed out.")

    async def initialize(self) -> None:
        self.description = await self.scrollable.output()
        self.set_footer(text=self.scrollable.get_footer())

    async def next(self) -> None:
        self.description = await self.scrollable.next()
        self.set_footer(text=self.scrollable.get_footer())

    async def previous(self) -> None:
        self.description = await self.scrollable.previous()
        self.set_footer(text=self.scrollable.get_footer())

class PaginatedView(View):
    def __init__(self, embed: PaginatedEmbed, user_id: int, timeout: float = 300, **kwargs):
        super().__init__(timeout=timeout, **kwargs)
        self.embed = embed
        self.user_id = user_id

        if not embed.is_scrollable():
            self.disable_buttons()
            self.stop()

        # Appending the message this view was attached to 
        # makes it possible to disable the buttons on timeout
        self.message: Optional[discord.InteractionMessage] = None

    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
    async def previous_callback(self, interaction: discord.Interaction, button: Button):
        await self.embed.previous()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
    async def next_callback(self, interaction: discord.Interaction, button: Button):
        await self.embed.next()
        await interaction.response.edit_message(embed=self.embed)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id

    async def on_timeout(self) -> None:
        self.embed.time_out()
        self.disable_buttons()
        if isinstance(self.message, discord.InteractionMessage):
            await self.message.edit(embed=self.embed, view=self)

    def disable_buttons(self) -> None:
        for child in self.children:
            if isinstance(child, Button):
                child.disabled = True

    async def timeout_after(self, seconds: int):
        await asyncio.sleep(seconds)
        self.stop()
        await self.on_timeout()