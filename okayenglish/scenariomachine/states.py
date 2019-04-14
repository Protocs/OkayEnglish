import re
import random
import logging
from abc import ABC, abstractmethod

from yaml import YAMLObject, add_constructor

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
