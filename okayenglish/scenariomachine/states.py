import re
import logging
from abc import ABC, abstractmethod

from . import TEXTS
from .choice import Choice

__all__ = ["ChoiceState", "InputState", "FinalState"]

logging.basicConfig(level=logging.DEBUG)


def get_text_and_tts(text_and_tts):
    """
    Раскладывает текст сообщения,
    возможно содержащую данные о произношении, на собственно текст и tts-строку.
    """
    match = re.search(tts_pattern, text_and_tts)
    # Если произношение не задано, произносим как пишем
    if match is None:
        return text_and_tts, text_and_tts
    # Убираем &(...) из текста
    just_text = re.sub(tts_pattern, "", text_and_tts).strip()
    tts = match.group(0)
    return just_text, tts


class AbstractState(ABC):
    def __init__(self, name, text):
        self.text = text
        self.name = name
        state_objects[name] = self

    def get_text(self, storage):
        if isinstance(self.text, str):
            return self.text
        if callable(self.text):
            return self.text(storage)

    @abstractmethod
    def get_next_state(self, storage, inp):
        pass


# Регулярное выражения измененного произношения.
# Пример:
#
# Здравствуйте! Это мы, хороводоведы. &(Здравствуйте! Это мы, хоров+одо в+еды.)
tts_pattern = re.compile(r"&\((.*)\)")

state_objects = {}


class ChoiceState(AbstractState):
    def __init__(self, name, text, choices):
        super().__init__(name, text)
        self.choices = choices

    def get_next_state(self, storage, inp):
        for choice in self.choices:
            if choice.fits_under(inp):
                if isinstance(choice.next, str):
                    return state_objects[choice.next]
                if callable(choice.next):
                    return state_objects[choice.next(storage, inp)]
        raise ValueError(
            f"ни один выбор не подошёл под ответ {inp!r}.\n"
            'Добавьте Choice с "match: .*", '
            'чтобы задать выбор "Не поняла".'
        )


class InputState(AbstractState):
    def __init__(self, name, text, next):
        super().__init__(name, text)
        self.text = text
        self.next = next

    def get_next_state(self, storage, inp):
        if isinstance(self.next, str):
            return state_objects[self.next]
        if callable(self.next):
            return state_objects[self.next(storage, inp)]


class FinalState(AbstractState):
    def get_next_state(self, storage, inp):
        return None


InputState(
    name="START",
    text=TEXTS["START"],
    next="TRAINING_CHOICE"
)

ChoiceState(
    name="TRAINING_CHOICE",
    text=TEXTS["TRAINING_CHOICE"],
    choices=[
        Choice(
            hint="Перевод слов",
            match="слова",
            next="word_translating_state"
        ),
        Choice(
            hint="Перевод предложений",
            match="предложения",
            next="sentences_translating_state"
        ),
        Choice(
            hint="Чтение текста",
            match="текст",
            next="text_reading_state"
        )
    ],
)

# Временные состояния тренировок
# TODO: Генерация состояния для текущей тренировки
InputState(
    name="word_translating_state",
    text="Тут будет перевод слов",
    next="START"
)

InputState(
    name="sentences_translating_state",
    text="Тут будет перевод предложений",
    next="START"
)

InputState(
    name="text_reading_state",
    text="Тут будет чтение текста",
    next="START"
)
