import random
import logging

from okayenglish.scenariomachine.session_storage import SessionStorage
from okayenglish.scenariomachine.states import FinalState, state_objects


class Session:
    def __init__(self, user):
        self._user = user
        self._current_state = state_objects["START"]
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
        logging.info(dir(self._current_state))
        resp_parser.reply_text = random_prepend + self._current_state.get_text(
            self._storage
        )
        if isinstance(self._current_state, FinalState):
            resp_parser.end_session = True
        self._advance_state(self._user_text)

    # TODO: Обработать FinalState
    def _advance_state(self, inp):
        self._current_state = self._current_state.get_next_state(self._storage, inp)
