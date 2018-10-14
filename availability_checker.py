import datetime
import smtplib
import textwrap
from collections import OrderedDict
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from credentials import gmail_password, gmail_user
from emailer import Emailer


SOLD_OUT = 'SOLD OUT'


def get_game_statuses():
    urls = build_urls()

    game_statuses = []
    for day, url in urls.items():
        print('Checking {} ...'.format(day))
        try:
            request = Request(url, headers={'User-Agent' : "Magic Browser"})
            connection = urlopen(request)

            soup = BeautifulSoup(connection, 'html.parser')
            game_status_button = soup.find('a', attrs={'class': 'more-info'})

            is_game_sold_out = bool(game_status_button and SOLD_OUT in game_status_button.text)
            game_status = GameStatus(day, url, is_game_sold_out)
            game_statuses.append(game_status)

        except Exception as e:
            game_status = GameStatus(day, url, None)
            game_statuses.append(game_status)

    return game_statuses





class GameStatus(object):
    def __init__(self, datetime, url, is_game_sold_out):
        self.datetime = datetime
        self.url = url
        self.is_game_sold_out = is_game_sold_out

    def __str__(self):
        return str(self.datetime)


def build_urls():
    base_url = 'https://secure.stinkysocks.net/NCH/NCH-'
    hours = [21, 22]
    weeks_ahead = 1

    urls = OrderedDict()
    today = datetime.date.today()
    for week_ahead in range(weeks_ahead):
        tuesday = today + datetime.timedelta(((1-today.weekday()) % 7) + week_ahead * 7)
        for hour in hours:
            tuesday_dt = datetime.datetime.combine(tuesday, datetime.datetime.min.time())
            tuesday_dt = tuesday_dt.replace(hour=hour, minute=0)
            urls[tuesday_dt] = base_url + tuesday_dt.strftime('%Y%m%d%H%S') + 'SOM.html'

    return urls


emailer = None
try :
    emailer = Emailer(gmail_user, gmail_password)
    game_statuses = get_game_statuses()
    print([str(g) for g in game_statuses])
    emailer.send_game_status_emails(game_statuses)

except Exception as e:
    print('Exception while starting emailer: {}'.format(e))

finally:
    if emailer:
        print('Closing SMTP Connection')
        emailer.close()


