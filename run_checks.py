import argparse

from availability_checker import AvailabilityChecker
from config.configuration import SLEEP_TIME
from random import randint
from time import sleep

parser = argparse.ArgumentParser("availability_checker")
parser.add_argument("--clear", help="boolean whether or not to clear the db file before checking status", type=bool)
parser.set_defaults(clear=False)
args = parser.parse_args()

availability_checker = AvailabilityChecker()
availability_checker.initialize(clear=args.clear)

while(True):
    # Add a jitter to the sleep time, between 1 second and 30 seconds (or the sleep time if its less than 30 seconds)
    sleep_delta = randint(1, min(30, SLEEP_TIME))
    sleep_time = SLEEP_TIME + sleep_delta

    availability_checker.check_game_availability()
    print("Sleeping for {} seconds...".format(sleep_time))
    sleep(sleep_time)
