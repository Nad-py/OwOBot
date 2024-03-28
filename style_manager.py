from json import load
import os
import logging
import discord


def load_style(style: str) -> dict:
    """
    Load a style from a JSON file.

    Args:
        style (str): The name of the style file.

    Returns:
        dict: The style information loaded from the JSON file.

    Raises:
        FileNotFoundError: If the specified style file is not found.
        Exception: If an error occurs while loading the style file.
    """
    style_path = f"./styles/{style}"
    try:
        with open(style_path, encoding="utf8") as json_data:
            style_dict = load(json_data)
            return style_dict
    except FileNotFoundError:
        logging.error(f"Style file not found: {style_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading style {style}: {e}")
        raise


async def send_error_embed(interaction: discord.Interaction, error_message: str) -> None:
    """
    Utility function to send an error message with a fallback embed.

    Args:
        interaction (discord.Interaction): The interaction context.
        error_message (str): The error message to display.
    """
    logging.error(error_message)
    error_embed = discord.Embed(title="Error", description=error_message, color=discord.Color.red())
    await interaction.response.send_message(embed=error_embed, ephemeral=True)


def create_give_embed(points_given: int, author: discord.User) -> discord.Embed:
    """
        Create an embed for the points given.

        Args:
            points_given (int): The number of points given.
            author (discord.User): The author of the points.

        Returns:
            discord.Embed: The created embed.
        """
    try:
        embed_dict = load_style("points_given.json")

        embed_dict['description'] = embed_dict['description'].format(points=points_given)
        embed_dict["author"]["name"] = author.display_name
        embed_dict["author"]["icon_url"] = author.avatar.url

        return discord.Embed().from_dict(embed_dict)

    except Exception as ex:
        logging.error(f"Error in create_give_embed: {ex}")


def create_view_embed(points: int, author: discord.User) -> discord.Embed:
    """
        Create an embed for viewing points.

        Args:
            points (int): The number of points to display.
            author (discord.User): The author of the points.

        Returns:
            discord.Embed: The created embed.
        """
    try:
        embed_dict = load_style("point_view.json")
        embed_dict["description"] = embed_dict["description"].format(points=points)
        embed_dict["author"]["name"] = author.display_name
        embed_dict["author"]["icon_url"] = author.avatar.url
        return discord.Embed().from_dict(embed_dict)

    except Exception as ex:
        logging.error(f"Error in create_view_embed: {ex}")


def create_leaderboard_embed(leaderboard_data: list, author: discord.User) -> discord.Embed:
    """
    Create an embed for the cute leaderboard.

    Args:
        leaderboard_data (list): The list of tuples containing name and points.
        author (discord.User): The author of the leaderboard.

    Returns:
        discord.Embed: The created embed.
    """
    try:
        embed_dict = load_style("leaderboard.json")
        embed_dict["author"]["name"] = author.display_name
        embed_dict["author"]["icon_url"] = author.avatar.url

        for i, (name, points) in enumerate(leaderboard_data, start=1):
            embed_dict["fields"][1]["value"] += f"{name}\nㅤㅤㅤ" if i < len(leaderboard_data) else f"{name}"
            embed_dict["fields"][2]["value"] += f"{points}\nㅤㅤㅤㅤ" if i < len(leaderboard_data) else f"{points}"

        return discord.Embed().from_dict(embed_dict)

    except Exception as ex:
        logging.error(f"Error in create_leaderboard_embed: {ex}")


def create_profession_embed(name: str, service_description: str, service_requirements: str,
                            author: discord.User) -> discord.Embed:
    """
    Create an embed for the profession message.

    Args:
        name (str): The title of the profession message.
        service_description (str): The first row of the service description.
        service_requirements (str): The service requirements.
        author (discord.User): The author of the profession message.

    Returns:
        discord.Embed: The created embed.
    """
    embed_dict = load_style("professions.json")
    service_requirements = service_requirements.replace(",", "\n")
    embed_dict["author"]["name"] = author.display_name
    embed_dict["author"]["icon_url"] = author.avatar.url
    embed_dict["description"] = embed_dict["description"].format(service_name=name)
    embed_dict["fields"][0]["value"] = embed_dict["fields"][0]["value"].format(
        service_description=service_description)
    embed_dict["fields"][1]["value"] = embed_dict["fields"][1]["value"].format(
        service_requirements=service_requirements)

    return discord.Embed().from_dict(embed_dict)