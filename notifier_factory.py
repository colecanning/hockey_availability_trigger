from email_notifier import EmailNotifier
from pushover_notifier import PushoverNotifier
from push_safer_notifier import PushSaferNotifier
from terminal_notifier import TerminalNotifier


EMAIL_NOTIFIER = 0
PUSH_SAFER_NOTIFIER = 1
TERMINAL_NOTIFIER = 2
PUSH_OVER_NOTIFIER = 3

NOTIFIERS = {
    EMAIL_NOTIFIER: EmailNotifier,
    PUSH_SAFER_NOTIFIER: PushSaferNotifier,
    TERMINAL_NOTIFIER: TerminalNotifier,
    PUSH_OVER_NOTIFIER: PushoverNotifier
}

class NotifierFactory(object):

    @staticmethod
    def get_notifier(notifier_type=1):
        notifier = None
        try:
            notifier_class = NOTIFIERS[notifier_type]
            notifier = notifier_class()
        except Exception as e:
            print('Failed to make EmailNotifier, proceeding with TerminalNotifier. Exception: {}'.format(e))
            notifier = TerminalNotifier()
        return notifier
