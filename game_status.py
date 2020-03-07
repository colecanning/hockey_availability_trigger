class GameStatus(object):
    def __init__(self, datetime, url, is_game_sold_out, sql_dao):
        self.datetime = datetime
        self.url = url
        self.is_game_sold_out = is_game_sold_out
        self.was_game_sold_out = None
        self.sql_dao = sql_dao

    # def __str__(self):
    #     return str(self.datetime)

    def did_game_become_available(self):
        """ Is the game a new game, or did it change statuses to available? """
        return (self.was_game_sold_out is None) or (self.was_game_sold_out and self.is_game_sold_out is False)

    def set_prior_game_availability(self):
        game_info = self.sql_dao.get_hockey_game(str(self.datetime))
        self.was_game_sold_out = game_info[0][0] if game_info else None

    def insert_game(self):
        self.sql_dao.insert_hockey_game((str(self.datetime), not self.is_game_sold_out))

    def __repr__(self):
        return f"{{datetime: {self.datetime}, is_game_sold_out: {self.is_game_sold_out}, was_game_sold_out: {self.was_game_sold_out}}}"


