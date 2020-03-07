import datetime
import http.client, urllib

from credentials import pushover_token, pushover_user
from email_notifier import EmailNotifier
from game_status import GameStatus
from notifier import Notifier


class PushoverNotifier(Notifier):
    """ Uses the Push Over platform to send a notification to the Push Over mobile app """

    def send_game_status_emails(self, game_statuses):
        """ Send a push notification with the game availability information """
        message = self.get_message(game_statuses)

        conn = http.client.HTTPSConnection("api.pushover.net:443")

        conn.request("POST", "/1/messages.json",
          urllib.parse.urlencode({
            "token": pushover_token,
            "user": pushover_user,
            "html": 1,
            "message": message
          }), { "Content-type": "application/x-www-form-urlencoded" })

        resp = conn.getresponse()
        if resp.status != 200:
            error_message = f"Error trying to send push notification via Pushover, response code: {resp.status}"
            self.send_error_email(error_message)
            raise Exception(error_message)

    def send_error_email(self, error_message):
        email_notifier = EmailNotifier()
        email_notifier.send_error_email(error_message)


    def get_message(self, game_statuses):
        message = ""

        games_statuses_weekly = GameStatus.get_game_statuses_by_week(game_statuses)
        current_week = int(datetime.datetime.now().strftime("%W"))

        # for game_statuses_week in games_statuses_weekly:
        for week in sorted (games_statuses_weekly.keys()):
            is_this_week = int(week) == current_week
            is_next_week = int(week) == current_week + 1

            if is_this_week:
                message += "This Week:\n"
            elif is_next_week:
                message += "Next Week:\n"
            else:
                message += "Future Week:\n"

            for game in games_statuses_weekly[week]['game_statuses']:
                message += "    "
                if game.did_game_become_available():
                    message += "<b> NOW AVAILABLE! </b>"
                message += f'<a href="{game.url}"> {game.get_readable_date()}</a>'
                message += "\n"

            message += "\n"

        return message
