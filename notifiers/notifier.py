from abc import ABC, abstractmethod


class Notifier(ABC):

    @abstractmethod
    def send_game_status_update(self):
        pass

    @abstractmethod
    def send_error_email(self):
        pass
