import argparse
import sched
from datetime import datetime, timedelta
from random import randint
from time import sleep, time

from availability_checker import AvailabilityChecker
from config.configuration import SLEEP_TIME, REPORT_HOUR


def when_to_generate_report(now):
    tomorrow = now + timedelta(1)
    return datetime(year=tomorrow.year, month=tomorrow.month,
                        day=tomorrow.day, hour=9, minute=0, second=0)

def seconds_until_next_report(now):
    """Get the number of seconds until the specified hour of the day, tomorrow. """
    return (when_to_generate_report(now) - now).seconds

parser = argparse.ArgumentParser("availability_checker")
parser.add_argument("--clear", help="boolean whether or not to clear the db file before checking status", type=bool)
parser.set_defaults(clear=False)
args = parser.parse_args()

availability_checker = AvailabilityChecker()
availability_checker.initialize(clear=args.clear)

# Add a jitter to the sleep time, between 1 second and 30 seconds (or the sleep time if its less than 30 seconds)
sleep_delta = randint(1, min(30, SLEEP_TIME))
sleep_time = SLEEP_TIME + sleep_delta

scheduler = sched.scheduler(time, sleep)
def check_availability(sc):
    availability_checker.check_game_availability()
    print("Sleeping for {} seconds... \n\n".format(sleep_time))
    scheduler.enter(sleep_time, 1, check_availability, (sc,))

def get_status_report(sc):
    availability_checker.send_game_status_notification()
    now = datetime.now()
    time_of_next_report = when_to_generate_report(now)
    print("Sleeping until next daily report at {} ... \n\n".format(time_of_next_report))
    scheduler.enter(seconds_until_next_report(now), 1, get_status_report, (sc,))

scheduler.enter(0, 1, check_availability, (scheduler,))
scheduler.enter(0, 1, get_status_report, (scheduler,))
scheduler.run()
