class GameStatus(object):
    def __init__(self, datetime, url, is_game_sold_out):
        self.datetime = datetime
        self.url = url
        self.is_game_sold_out = is_game_sold_out

    def __str__(self):
        return str(self.datetime)
