import discord
import sqlite3
from typing import Optional, Type, Any, List, Tuple
import logging


class DatabaseManager:
    """
    TODO: describe this
    """

    def __init__(self, db_file: str = 'owodb.db'):
        """
        Initialize the DatabaseManager with the specified database file.

        Args:
            db_file (str): The filename of the SQLite database file. Default is 'owodb.db'.
        """
        self.db_file = db_file
        self.conn = None

    def connect(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.db_file)
        return self.conn

    def disconnect(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None  # Set to None after closing to avoid potential issues

    def setup_database(self) -> None:
        """
        Creates the 'cutePoints' table if it doesn't exist.

        The 'cutePoints' table has columns: 'id', 'name', 'points', and 'userid'.
        """
        with self.connect() as conn:
            cur = conn.cursor()

            cur.execute('''
                CREATE TABLE IF NOT EXISTS cutePoints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    points INTEGER,
                    userid INTEGER NOT NULL UNIQUE
                )
            ''')

            conn.commit()

    def get_leaderboard_data(self) -> List[Tuple[str, int]]:
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name, points FROM cutePoints ORDER BY points DESC LIMIT 10")
            leaderboard_data = cur.fetchall()
        return leaderboard_data

    async def get_or_create_user(self, user: discord.User) -> tuple:
        """
        Retrieve an existing user's data or create a new user if not found.

        Args:
            user (discord.User): The Discord user.

        Returns:
            tuple: User information (or None if a new user was created).
        """
        try:
            with self.connect() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM cutePoints WHERE userid = ?", (user.id,))
                existing_user = cur.fetchone()
                if existing_user:
                    return existing_user
                else:
                    cur.execute("INSERT INTO cutePoints (name, points, userid) VALUES (?, ?, ?)",
                                (user.display_name, 0.0, user.id))
                    conn.commit()
                    return None, user.display_name, 0.0, user.id
        except Exception as ex:
            logging.error(f"Error in get_or_create_user: {ex}")
            raise

    async def give_points(self, user: discord.User, points: int) -> None:
        user_info = await self.get_or_create_user(user)
        with self.connect() as conn:
            cur = conn.cursor()
            new_points = user_info[2] + points
            cur.execute("UPDATE cutePoints SET points = ? WHERE userid = ?", (new_points, user.id))
            conn.commit()

    def __enter__(self) -> sqlite3.Connection:
        """
        Allows the DatabaseManager to be used as a context manager.

        Returns:
            sqlite3.Connection: The SQLite database connection.
        """
        return self.connect()

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[Any]) -> None:
        """
        Ensure the database connection is closed when exiting the context.

        Args:
            exc_type: The type of the exception.
            exc_value: The exception instance.
            traceback: The traceback information.
        """
        self.disconnect()
