from abc import ABC, abstractmethod

from okayenglish.states import TRAINING_SELECT


class TrainingManager(ABC):
    _PHRASES = {
        "right_answer": "Это правильный ответ.\n",
        "wrong_answer": "Это неправильный ответ.\n"
                        "Если не знаете перевода, просто скажите «не знаю».\n",
        "idk_answer": "Ничего страшного.\nПравильный ответ - {}\n",
        "stop": "Хорошо, хватит так хватит. "
    }
    ITEMS_PER_TRAINING = 5

    def __init__(self, session):
        self._session = session
        self.item_to_translate = None
        self.answer = None
        self._translated_so_far = 0

        self._training_interrupt = False

        self.next_item()

    @property
    def should_continue_training(self):
        return self._translated_so_far < self.ITEMS_PER_TRAINING \
               and not self._training_interrupt

    @abstractmethod
    def check_input(self, inp, answer):
        pass

    def check_answer(self, inp):
        if self.check_input(inp, self.answer):
            self.next_item()
            self._translated_so_far += 1
            return self._PHRASES["right_answer"]
        elif any(word in inp.lower() for word in ("хз", "не знаю", "понятия")):
            phrase = self._PHRASES["idk_answer"].format(self.answer)
            self.next_item()
            return phrase
        elif any(word in inp.lower() for word in ("хватит", "достаточно")):
            self._session._current_state = TRAINING_SELECT
            self._session._training_manager = None
            self._training_interrupt = True
            return self._PHRASES["stop"]
        return self._PHRASES["wrong_answer"]

    @abstractmethod
    def next_item(self):
        pass
