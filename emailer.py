import smtplib
import textwrap

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer(object):
    def __init__(self, user_email_address, password):
        self.user_email_address = user_email_address
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()
        self.server.login(user_email_address, password)

    def close(self):
        if self.server:
            self.server.close()

    def send_email(self, body):
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Hockey Game Available!'
        message['From'] = self.user_email_address
        message['To'] = self.user_email_address

        part2 = MIMEText(body, 'html')
        message.attach(part2)
        self.server.sendmail(self.user_email_address, self.user_email_address, message.as_string())

    @staticmethod
    def get_game_availability_copy(is_game_sold_out):
        if is_game_sold_out is None:
            return 'Error getting game status'
        elif is_game_sold_out:
            return 'sold out'
        else:
            return 'available'

    def send_game_status_emails(self, game_statuses):
        if any([g.is_game_sold_out for g in game_statuses]):
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
