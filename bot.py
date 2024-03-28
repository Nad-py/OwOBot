import discord
import asyncio
import os
import logging
from discord.ext import commands
from db_manager import DatabaseManager
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    logging.error("Discord token not found. Please set the DISCORD_TOKEN environment variable.")
    exit(1)

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='!')

db = DatabaseManager()


async def setup_cogs() -> None:
    """
    Loads all cogs in the 'cogs' directory.
    """
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logging.info(f"Cog {filename} loaded successfully.")
            except commands.ExtensionError as e:
                logging.error(f"Error loading cog {filename}: {e}")


def check_if_owner(ctx: commands.Context) -> bool:
    """
    Checks whether the user invoking the command is the owner specified in BOT_OWNER_ID.

    Args:
        ctx (commands.Context): The context object provided by Discord.py.

    Returns:
        bool: True if the invoking user matches the BOT_OWNER_ID, False otherwise.
    """

    return ctx.message.author.id == int(os.environ.get("BOT_OWNER_ID"))

@bot.command()
@commands.check(check_if_owner)
async def sync(ctx: commands.Context) -> None:
    """
    Command to synchronize commands within the bot's command tree for the guild from which it was executed.

    Args:
        ctx (commands.Context): Required while using the @bot.command() decorator
    """
    try:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        logging.info(f"Synced {len(fmt)} commands.")
        await ctx.send(f"Synced {len(fmt)} commands", delete_after=3)
        await ctx.message.delete()

    except commands.CommandError as e:
        logging.error(f"Error in sync command: {e}")


async def main() -> None:
    """
    Main function to set up the database, load cogs, and start the bot.

    This function sets up the database, loads cogs (extensions), and starts the bot using the provided TOKEN.
    """
    try:
        db.setup_database()
        await setup_cogs()
        await bot.start(TOKEN)
    except commands.CommandError as e:
        logging.error(f"Error in main function: {e}")


asyncio.run(main())
