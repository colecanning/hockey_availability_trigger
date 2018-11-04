from email_notifier import EmailNotifier
from terminal_notifier import TerminalNotifier

class NotifierFactory(object):

	@staticmethod
	def get_notifier(gmail_user, gmail_password):
		notifier = None
		try:
			notifier = EmailNotifier(gmail_user, gmail_password)
		except Exception as e:
			print('Failed to make EmailNotifier, proceeding with TerminalNotifier. Exception: {}'.format(e))
			notifier = TerminalNotifier()
		return notifier
