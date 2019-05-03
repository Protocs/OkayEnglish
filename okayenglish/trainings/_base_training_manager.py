import random

from abc import ABC, abstractmethod

from okayenglish.states import TRAINING_SELECT
from okayenglish.texts import TRAINING_HELP
from okayenglish.utils import TRAINING_NAMES


class TrainingManager(ABC):
    _PHRASES = {
        "right_answer": [
            "Это правильный ответ.",
            "В точку!",
            "Да, правильно.",
            "Верно!",
            "Абсолютно правильно!",
        ],
        "wrong_answer": [
            "Это неправильный ответ.",
            "Нет, неправильно.",
            "Увы, но нет.",
            "К сожалению, это неправильно.",
            "Неверно.",
        ],
        "if_idk": "Если не знаете перевода, просто скажите «не знаю».\n",
        "idk_answer": "Ничего страшного.\nПравильный ответ - {}\n",
        "stop": ["Хорошо, хватит так хватит. ", "Как скажете. ", "Так и быть. "],
        "tip": "С использованием подсказки правильный ответ будет засчитан как "
        "половина правильного ответа.\n",
        "already_tip": "Вы уже использовали подсказку.\n",
    }

    ITEMS_PER_TRAINING = 5

    def __init__(self, session):
        self._session = session
        self.item_to_translate = None
        self.answer = None
        self._translated_so_far = 0
        self._wrong_answers = 0

        self.training_interrupt = False

        self.tip = None
        self.tips = 0

        self.next_item()

    @property
    def should_continue_training(self):
        return (
            self._translated_so_far < self.ITEMS_PER_TRAINING
            and not self.training_interrupt
        )

    @abstractmethod
    def check_input(self, inp, answer):
        pass

    def check_answer(self, inp):
        if self.check_input(inp, self.answer):
            self.next_item()
            self.tip = False
            self._translated_so_far += 1
            return random.choice(self._PHRASES["right_answer"]) + "\n"
        elif any(word in inp.lower() for word in ("хз", "не знаю", "понятия")):
            phrase = self._PHRASES["idk_answer"].format(self.answer)
            self.next_item()
            self.tip = False
            self._wrong_answers += 1
            return phrase
        elif any(word in inp.lower() for word in ("хватит", "достаточно")):
            self._session._current_state = TRAINING_SELECT
            self._session._training_manager = None
            self.training_interrupt = True
            return random.choice(self._PHRASES["stop"])
        elif any(word in inp.lower() for word in ("подскажи", "подсказка")):
            if self.tip:
                return self._PHRASES["already_tip"]
            self.tip = True
            self.tips += 1
            return self._PHRASES["tip"]
        elif any(word in inp.lower() for word in ("помощь", "что ты умеешь")):
            return TRAINING_HELP.format(
                training_name=TRAINING_NAMES[self._session._current_state]
            )
        self._wrong_answers += 1
        return (
            random.choice(self._PHRASES["wrong_answer"])
            + "\n"
            + self._PHRASES["if_idk"]
        )

    @abstractmethod
    def next_item(self):
        pass

    def get_stats(self):
        return self._translated_so_far - self.tips / 2, self._wrong_answers, self.tips
