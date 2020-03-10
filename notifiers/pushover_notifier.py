import datetime
import http.client, urllib
import imgkit
import requests

from config.configuration import STINKYSOCKS_SCHEDULE_URL
from config.credentials import pushover_token, pushover_user
from models.game_status import GameStatus
from notifiers.email_notifier import EmailNotifier
from notifiers.notifier import Notifier


class PushoverNotifier(Notifier):
    """ Uses the Push Over platform to send a notification to the Push Over mobile app """

    def send_game_status_update(self, game_statuses):
        """ Send a push notification with the game availability information """
        message = self.get_game_status_message(game_statuses)
        imgkit.from_string(self.get_game_status_message(game_statuses, for_image=True, max_game_statuses=None), 'message.jpg')
        self.send_notification(message, "Hockey Notifier - Availability Changed!", 'message.jpg')

    def send_notification(self, message, title, image_path):
        conn = http.client.HTTPSConnection("api.pushover.net:443")

        resp = requests.post(
            "https://api.pushover.net/1/messages.json",
            data = {
                "token": pushover_token,
                "user": pushover_user,
                "html": 1,
                "title": title,
                "message": message
            },
            files = {
                "attachment": ("message.jpg", open(image_path, "rb"), "image/jpeg")
            }
        )

        # If we failed to submit the push notification, send an error email out.
        if resp.status_code != 200:
            error_message = f"Error trying to send push notification via Pushover, response code: {resp.status_code}"
            self.send_error_email(error_message)
            raise Exception(error_message)

    def send_error_email(self, error_message):
        email_notifier = EmailNotifier()
        email_notifier.send_error_email(error_message)

    def send_all_game_status_update(self, game_statuses):
        message = self.get_game_status_message(game_statuses, skip_now_available=True)
        imgkit.from_string(self.get_game_status_message(game_statuses, for_image=True, max_game_statuses=None), 'message.jpg')
        self.send_notification(message, "Hockey Notifier - Status Report", 'message.jpg')

    def get_game_status_message(self, game_statuses, skip_now_available=False, max_game_statuses=4, for_image=False):
        """ Get a message with all of the game's statuses, which ones have recently become available, and a link to the
            current scheudle """
        line_separator = '\n' if not for_image else '<br>'

        message = ""

        # Get the game statuses organized by week (see function for dict formatting)
        games_statuses_weekly = GameStatus.get_game_statuses_by_week(game_statuses)
        current_week = int(datetime.datetime.now().strftime("%W"))

        # For each week, print out the games and whether or not they've recently become available.
        game_index = 0
        for week in sorted (games_statuses_weekly.keys()):
            if max_game_statuses and (game_index >= max_game_statuses):
                break
            is_this_week = int(week) == current_week
            is_next_week = int(week) == current_week + 1

            # Print which week the games belong to relative to the current week
            if is_this_week:
                message += f"<b>This Week:</b>{line_separator}"
            elif is_next_week:
                message += f"<b>Next Week:</b>{line_separator}"
            else:
                message += f"<b>Future Week:</b>{line_separator}"

            # Go through each game in the week and print out its availability, date, and a badge if it's recently become available
            for game in games_statuses_weekly[week]['game_statuses']:
                game_index += 1
                if max_game_statuses and (game_index > max_game_statuses):
                    break

                message += "    "
                if not skip_now_available and game.did_game_become_available():
                    message += '<b><font color="#00FF00">[NOW AVAILABLE!]</font></b> '

                if game.is_game_sold_out:
                    message += '<font color="#FF0000">Unavailable</font> - '
                else:
                    message += '<font color="#00FF00">Available</font> - '

                message += f'<a href="{game.url}"> {game.get_readable_date()}</a>'
                message += f"{line_separator}"

            message += line_separator

        if not for_image:
            # Add the schedule at the bottom of the message
            message += line_separator
            message += f'<a href="{STINKYSOCKS_SCHEDULE_URL}">Schedule</a>'

        return message
