import datetime


class GameStatus(object):
    def __init__(self, datetime, url, is_game_sold_out, sql_dao):
        self.datetime = datetime
        self.url = url
        self.is_game_sold_out = is_game_sold_out
        self.was_game_sold_out = None
        self.sql_dao = sql_dao

    def was_game_found(self):
        return self.is_game_sold_out is not None

    def did_game_become_available(self):
        """
        Is the game a new game, or did it change statuses to available?
        TODO: checking "self.is_game_sold_out is not None" is a hack - both of these values are None if we fail to find it
            when querying the site. Instead, we just shouldn't insert into the DB, or should handle the exceptional state of
            the game better so that this is more explicit.
        """
        return (self.was_game_sold_out is None and self.was_game_found()) or (self.was_game_sold_out and self.is_game_sold_out is False)

    def set_prior_game_availability(self):
        game_info = self.sql_dao.get_hockey_game(str(self.datetime))
        self.was_game_sold_out = not game_info[0][0] if game_info else None

    def insert_game(self):
        self.sql_dao.insert_hockey_game((str(self.datetime), not self.is_game_sold_out))

    def get_readable_date(self):
        return self.datetime.strftime("%m/%d/%Y, %I:%M %p")

    def is_next_game(self):
        return (self.datetime - datetime.datetime.now()).days <= 7

    def __repr__(self):
        return f"{{datetime: {self.datetime}, is_game_sold_out: {self.is_game_sold_out}, was_game_sold_out: {self.was_game_sold_out}}}"

    @staticmethod
    def get_game_statuses_by_week(game_statuses):
        """
        Get the game statuses in a dictionary where each key is the week of the year.
        Example:
        {
            '10':
                {
                    'datetime': datetime,
                    'game_statuses': [GameStatus, ...]
                },
            ...
        }
        """
        games_by_week = {}
        for game in game_statuses:
            week = game.datetime.strftime("%W")
            if week not in games_by_week:
                games_by_week[week] = {"datetime":game.datetime, "game_statuses": [game]}
            else:
                games_by_week[week]["game_statuses"].append(game)
        return games_by_week
