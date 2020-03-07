import datetime
import http.client, urllib

from configuration import STINKYSOCKS_SCHEDULE_URL
from credentials import pushover_token, pushover_user
from email_notifier import EmailNotifier
from game_status import GameStatus
from notifier import Notifier


class PushoverNotifier(Notifier):
    """ Uses the Push Over platform to send a notification to the Push Over mobile app """

    def send_game_status_update(self, game_statuses):
        """ Send a push notification with the game availability information """
        message = self.get_game_status_message(game_statuses)

        conn = http.client.HTTPSConnection("api.pushover.net:443")

        conn.request("POST", "/1/messages.json",
          urllib.parse.urlencode({
            "token": pushover_token,
            "user": pushover_user,
            "html": 1,
            "message": message
          }), { "Content-type": "application/x-www-form-urlencoded" })

        resp = conn.getresponse()

        # If we failed to submit the push notification, send an error email out.
        if resp.status != 200:
            error_message = f"Error trying to send push notification via Pushover, response code: {resp.status}"
            self.send_error_email(error_message)
            raise Exception(error_message)

    def send_error_email(self, error_message):
        email_notifier = EmailNotifier()
        email_notifier.send_error_email(error_message)

    def get_game_status_message(self, game_statuses):
        """ Get a message with all of the game's statuses, which ones have recently become available, and a link to the
            current scheudle """
        message = ""

        # Get the game statuses organized by week (see function for dict formatting)
        games_statuses_weekly = GameStatus.get_game_statuses_by_week(game_statuses)
        current_week = int(datetime.datetime.now().strftime("%W"))

        # For each week, print out the games and whether or not they've recently become available.
        for week in sorted (games_statuses_weekly.keys()):
            is_this_week = int(week) == current_week
            is_next_week = int(week) == current_week + 1

            # Print which week the games belong to relative to the current week
            if is_this_week:
                message += "<b>This Week:</b>\n"
            elif is_next_week:
                message += "<b>Next Week:</b>\n"
            else:
                message += "<b>Future Week:</b>\n"

            # Go through each game in the week and print out its availability, date, and a badge if it's recently become available
            for game in games_statuses_weekly[week]['game_statuses']:
                message += "    "
                if game.did_game_become_available():
                    message += '<b><font color="#00FF00">[NOW AVAILABLE!]</font></b> '

                if game.is_game_sold_out:
                    message += '<font color="#FF0000">Unavailable</font> - '
                else:
                    message += '<font color="#00FF00">Available</font> - '

                message += f'<a href="{game.url}"> {game.get_readable_date()}</a>'
                message += "\n"

            message += "\n"

        # Add the schedule at the bottom of the message
        message += "\n"
        message += f'<a href="{STINKYSOCKS_SCHEDULE_URL}">Schedule</a>'

        return message
