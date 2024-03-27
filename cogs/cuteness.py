import logging
import discord
from discord import app_commands
from discord.ext import commands
from db_manager import DatabaseManager
import style_manager
import os


class Cuteness(commands.Cog):
    """
    A Discord Cog for managing cute points.
    """

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: DatabaseManager = DatabaseManager()
        self.log_channel = int(os.environ.get("CUTE_CHANNEL"))

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("Cuteness cog loaded successfully.")

    @app_commands.command(name="cute_give", description="Give cute points to a member (or take em away >:3)")
    @app_commands.checks.has_role(int(os.environ.get("CUTE_ROLE_ID")))
    async def cute_give(self, interaction: discord.Interaction, points: int, user: discord.User) -> None:
        """
        Command to give cute points to a member.

        Args:
            interaction (discord.Interaction): The interaction context.
            points (int): The number of cute points to give.
            user (discord.User): The target user.
        """
        try:
            await self.db.give_points(user, points)
            embed = style_manager.create_give_embed(points, interaction.user)

            await interaction.response.send_message(embed=embed, ephemeral=True)
            await self.bot.get_channel(self.log_channel).send(f"{interaction.user} gave {user} {points} point(s)")
        except Exception as ex:
            logging.error(f"Error in cute_give: {ex}")
            await style_manager.send_error_embed(interaction, "Failed to give cute points")

    @app_commands.command(name="cute_points", description="Look at your own points:3")
    async def cute_points(self, interaction: discord.Interaction) -> None:
        """
        Command to check the cute points of the invoking user.
        """
        try:
            user_info = await self.get_or_create_user(interaction.user)
            embed = style_manager.create_view_embed(user_info[2], interaction.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as ex:
            logging.error(f"Error in point_view command: {ex}")
            await style_manager.send_error_embed(interaction, "Failed to retrieve your cute points")

    @app_commands.command(name="cute_leaderboard", description="Look at the cute leaderboard :3")
    async def cute_leaderboard(self, interaction: discord.Interaction) -> None:
        """
        Retrieves the top 10 members with the highest cute points from the database
        and displays their rankings and points in descending order.
        """
        try:
            with self.db.connect() as conn:
                cur = conn.cursor()
                cur.execute("SELECT name, points FROM cutePoints ORDER BY points DESC LIMIT 10")
                leaderboard_data = cur.fetchall()

            embed = style_manager.create_leaderboard_embed(leaderboard_data, interaction.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as ex:
            logging.error(f"Error in cute_leaderboard: {ex}")
            await style_manager.send_error_embed(interaction, "Failed to retrieve leaderboard data")


async def setup(bot: commands.Bot) -> None:
    """
    Set up the Cuteness cog.

    Args:
        bot (commands.Bot): The Discord bot.
    """
    # specifying a guild is essential, it doesnt register slash commands otherwise
    await bot.add_cog(Cuteness(bot), guilds=[discord.Object(id=int(os.environ.get("GUILD_ID")))])
