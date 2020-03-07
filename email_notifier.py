import smtplib
import textwrap

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from credentials import gmail_password, gmail_user
from notifier import Notifier


class EmailNotifier(Notifier):
    def __init__(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()
        self.server.login(gmail_user, gmail_password)

    def close(self):
        if self.server:
            self.server.close()

    def send_email(self, body):
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Hockey Game Available!'
        message['From'] = gmail_user
        message['To'] = gmail_user

        part2 = MIMEText(body, 'html')
        message.attach(part2)
        self.server.sendmail(gmail_user, gmail_user, message.as_string())

    @staticmethod
    def get_game_availability_copy(is_game_sold_out):
        if is_game_sold_out is None:
            return 'Error getting game status'
        elif is_game_sold_out:
            return 'sold out'
        else:
            return 'available'

    def send_game_status_emails(self, game_statuses):
        body = textwrap.dedent("""
        <table>
            <thead>
                <tr>
                    <th> Date </th>
                    <th> Availability </th>
                </tr>
            </thead>
            <tbody>
        """)
        for game_status in game_statuses:
            print(game_status)
            body += textwrap.dedent("""
                <tr>
                    <td> {} </td> <td> {} </td> <td> <a href="{}"> link </a> </td>
                </tr>
            """).format(game_status.datetime, self.get_game_availability_copy(game_status.is_game_sold_out),
                        game_status.url)
        body += textwrap.dedent("""
            </tbody>
        </table>
        """)
        self.send_email(body)

    def send_error_email(self):
        self.send_email('There was an issue getting game availability!')
