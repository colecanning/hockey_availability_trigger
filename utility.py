from credentials import debug as debug_flag


def debug(message):
    if debug_flag:
        print(message)
