import datetime
import smtplib
import urllib2
import textwrap
from collections import OrderedDict

from bs4 import BeautifulSoup

from credentials import gmail_password, gmail_user
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SOLD_OUT = 'SOLD OUT'


HTML = textwrap.dedent("""\
            <html>
              <head></head>
              <body>
                <p>Hi!<br>
                   How are you?<br>
                   Here is the <a href="https://www.python.org">link</a> you wanted.
                </p>
              </body>
            </html>
""")


def get_game_statuses():
    urls = build_urls()

    game_statuses = {}
    for day, url in urls.iteritems():
        print('Checking {} ...'.format(day))
        try:
            request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
            connection = urllib2.urlopen(request)

            soup = BeautifulSoup(connection, 'html.parser')
            game_status_button = soup.find('a', attrs={'class': 'more-info'})

            is_game_sold_out = bool(game_status_button and SOLD_OUT in game_status_button.text)
            game_statuses[day] = is_game_sold_out

        except Exception as e:
            print('Exception when trying to check status of game: {}'.format(e))
            # send_failure_email()

    return game_statuses


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

    def send_game_status_emails(self, game_statuses):
        if any(game_statuses.items()):
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
            for day, is_game_sold_out in game_statuses.iteritems():
                body += '<tr> <td>{}</td> <td>{}</td> </tr>'.format(day, 'sold out' if is_game_sold_out else 'available')
            body += textwrap.dedent("""
                </tbody>
            </table>
            """)
        self.send_email(body)


def build_urls():
    base_url = 'https://secure.stinkysocks.net/NCH/NCH-'
    hours = [21, 22]
    weeks_ahead = 3

    urls = OrderedDict()
    today = datetime.date.today()
    for week_ahead in range(weeks_ahead):
        tuesday = today + datetime.timedelta(((1-today.weekday()) % 7) + week_ahead * 7)
        for hour in hours:
            tuesday_dt = datetime.datetime.combine(tuesday, datetime.datetime.min.time())
            tuesday_dt = tuesday_dt.replace(hour=hour, minute=0)
            urls[tuesday_dt] = base_url + tuesday_dt.strftime('%Y%m%d%H%S') + 'SOM.html'

    return urls


try :
    emailer = Emailer(gmail_user, gmail_password)
    game_statuses = get_game_statuses()
    print(game_statuses)
    emailer.send_game_status_emails(game_statuses)
except Exception as e:
    print('Exception while starting emailer: {}'.format(e))
    if emailer:
        print('Closing SMTP Connection')
        emailer.close()

