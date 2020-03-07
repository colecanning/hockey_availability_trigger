import argparse

from availability_checker import AvailabilityChecker
from configuration import SLEEP_TIME
from time import sleep

parser = argparse.ArgumentParser("availability_checker")
parser.add_argument("--clear", help="boolean whether or not to clear the db file before checking status", type=bool)
parser.set_defaults(clear=False)
args = parser.parse_args()

availability_checker = AvailabilityChecker()
availability_checker.initialize(clear=args.clear)

while(True):
    availability_checker.check_game_availability()
    print("Sleeping for {} seconds...".format(SLEEP_TIME))
    sleep(SLEEP_TIME)
