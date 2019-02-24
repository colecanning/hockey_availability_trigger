from email_notifier import EmailNotifier
from push_safer_notifier import PushSaferNotifier
from terminal_notifier import TerminalNotifier

class NotifierFactory(object):

    NOTIFIERS = {
        0: EmailNotifier,
        1: PushSaferNotifier,
        2: TerminalNotifier
    }

    @staticmethod
    def get_notifier(notifier_type=1):
        notifier = None
        try:
            notifier_class = NotifierFactory.NOTIFIERS[notifier_type]
            notifier = notifier_class()
        except Exception as e:
            print('Failed to make EmailNotifier, proceeding with TerminalNotifier. Exception: {}'.format(e))
            notifier = TerminalNotifier()
        return notifier
