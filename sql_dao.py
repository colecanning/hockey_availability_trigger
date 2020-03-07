import sqlite3
from sqlite3 import Error

from credentials import sqlite_db_file


class SQLDao(object):
    SQL_INSERT_HOCKEY_GAMES_TABLE = """
        CREATE TABLE IF NOT EXISTS hockey_game_tested_new (
            id integer PRIMARY KEY,
            game_date text NOT NULL,
            is_available integer,
            CONSTRAINT u_game_date UNIQUE (game_date)
        );
    """

    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        """ create a database connection to a SQLite database """
        return sqlite3.connect(sqlite_db_file)

    def build_hockey_games_table(self):
        cursor = self.connection.cursor()
        cursor.execute(self.SQL_INSERT_HOCKEY_GAMES_TABLE)
        self.connection.commit()

    def insert_hockey_game(self, project):
        sql = '''
            INSERT INTO hockey_game_tested_new(game_date, is_available)
            VALUES
            (?, ?)
        '''
        cursor = self.connection.cursor()
        cursor.execute(sql, project)
        self.connection.commit()
        return cursor.lastrowid

    def get_hockey_game(self, game_date):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT is_available
            FROM hockey_game_tested_new
            WHERE game_date = ?
        """, [(game_date)])

        return cursor.fetchall()

    def get_hockey_games(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT game_date, CASE WHEN is_available THEN 'Available' ELSE 'Not Available' END
            FROM hockey_game_tested_new
        """)

        return cursor.fetchall()
