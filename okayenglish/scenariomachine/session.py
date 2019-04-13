from okayenglish.scenariomachine.session_storage import SessionStorage
from okayenglish.scenariomachine.state_parser import find_state_by_name


class Session:
    def __init__(self, user):
        self._user = user
        self._current_state = None
        self._storage = SessionStorage()
        self._text_prepend = None

    def advance(self):
        self._advance_state()
        # TODO: Отправить сообщение с помощью _send()
        ...

    def _send(self):
        ...

    # TODO: Обработать FinalState
    def _advance_state(self):
        if self._current_state is None:
            self._current_state = find_state_by_name("START")
        else:
            self._current_state = self._current_state.next_state()
