import calendar
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from credentials import push_safer_private_key
from notifier import Notifier


class PushSaferNotifier(Notifier):

    PUSH_SAFER_URL = 'https://www.pushsafer.com/api'
    DEFAULT_POST_FIELDS = {
        't' : 'Game Available',
        'm' : ' ',
        'ut' : 'Game URL',
        'k' : push_safer_private_key
    }

    def send_game_status_emails(self, game_statuses):
        for game_status in [g for g in game_statuses if g.did_game_become_available()]:
            post_fields = self.DEFAULT_POST_FIELDS
            post_fields['u'] = game_status.url

            day = calendar.day_name[game_status.datetime.weekday()]
            date = '{} {}'.format(day, game_status.datetime.strftime('%m/%d %I:%M%p'))

            post_fields['t'] = 'Game Available - {}'.format(date)

            request = Request(self.PUSH_SAFER_URL, urlencode(post_fields).encode())
            json = urlopen(request).read().decode()

    def send_error_email(self):
        print('Error pushing notification')
        pass
