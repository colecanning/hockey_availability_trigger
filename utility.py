from credentials import gmail_password, gmail_user, debug as debug_flag


def debug(message):
    if debug_flag:
        print(message)