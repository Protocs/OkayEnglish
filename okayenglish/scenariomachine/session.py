import random

from okayenglish.scenariomachine.session_storage import SessionStorage
from okayenglish.scenariomachine.state_parser import find_state_by_name


class Session:
    def __init__(self, user):
        self._user = user
        self._current_state = find_state_by_name("START")
        self._storage = SessionStorage()
        self._text_prepend = None
        self._user_text = None
        self._first_message = True

    def receive(self, req_parser):
        if self._first_message:
            self._user_text = ""
            self._first_message = False
        else:
            self._user_text = req_parser.text

    def respond(self, resp_parser):
        """Возвращает текст для сообщения."""
        if self._text_prepend is not None:
            random_prepend = random.choice(self._text_prepend) + "\n"
        else:
            random_prepend = ""
        self._text_prepend = None
        resp_parser.reply_text = random_prepend + self._current_state.get_text(
            self._storage
        )
        self._advance_state(self._user_text)

    # TODO: Обработать FinalState
    def _advance_state(self, inp):
        self._current_state = self._current_state.next_state(self._storage, inp)
