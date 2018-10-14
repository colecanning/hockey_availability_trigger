from availability_checker import AvailabilityChecker
from time import sleep

SLEEP_TIME = 2 * 60

availability_checker = AvailabilityChecker()

while(True):
    availability_checker.check_game_availability()
    print("Sleeping for {} seconds...".format(SLEEP_TIME))
    sleep(SLEEP_TIME)
