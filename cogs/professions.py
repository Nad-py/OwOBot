import discord
from discord import app_commands
from discord.ext import commands
import style_manager
import logging
import os
from typing import Optional

class ProfessionButtons(discord.ui.View):
    def __init__(self, owner_id: int, *, timeout: Optional[float] = None) -> None:
        """
        Initializes an instance of the ProfessionButtons view.

        Args:
            owner_id (int): The ID of the user who owns the profession-related action.
            timeout (Optional[float]): The timeout for the view, in seconds.
        """
        self.owner_id = owner_id
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.gray)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """
        A button callback for deleting a profession message. It ensures that only the user that created the message is
        able to delete it.

        Args:
            interaction (discord.Interaction): The interaction context.
            button (discord.ui.Button): The button that triggered the interaction.
        """
        try:
            if self.owner_id == interaction.user.id:
                await interaction.message.delete()
        except Exception as ex:
            logging.error(f"Error in profession command: {ex}")
            await style_manager.send_error_embed(interaction, "An error occurred while processing your request.")


class Professions(commands.Cog):
    """
    A Discord Cog for managing user professions.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """
        Initializes an instance of the Professions cog.

        Args:
            bot (commands.Bot): The Discord bot instance.
        """
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """
        Listener function called when the bot is ready.

        This function logs a message indicating successful loading of the Professions cog.
        """
        logging.info("Professions cog loaded successfully.")

    @app_commands.command(name="profession", description="meowfession descwiption")
    async def profession(self, interaction: discord.Interaction, name: str, description: str,
                         requirements: str) -> None:
        """
        Command for users to create and send messages, allowing them to upload information about their services.

        Args:
            interaction (discord.Interaction): The interaction context.
            name (str): The title of the profession.
            description (str): The description of the service.
            requirements (str): Requirements for the service, separated by commas.
        """
        try:
            embed = style_manager.create_profession_embed(name, description, requirements, interaction.user)
            await interaction.response.send_message(embed=embed, view=ProfessionButtons(interaction.user.id))
        except Exception as ex:
            logging.error(f"Error in profession command: {ex}")
            await style_manager.send_error_embed(interaction, "An error occurred while processing your request.")


async def setup(bot: commands.Bot) -> None:
    """
    Set up the Professions cog.

    Args:
        bot (commands.Bot): The Discord bot.
    """
    # specifying a guild is essential, it doesnt register slash commands otherwise
    await bot.add_cog(Professions(bot), guilds=[discord.Object(id=int(os.environ.get("GUILD_ID")))])


"""
TODO:
    Preview of the profession message before sending, needs a confirmation button
    Maybe limit the length of some strings, for example, "title"
    Deletion/editing of post
"""
