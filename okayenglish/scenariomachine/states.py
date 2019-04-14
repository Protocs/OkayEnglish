import re
import logging
from abc import ABC, abstractmethod

from okayenglish.scenariomachine.training_manager import WordTranslationTrainingManager
from . import TEXTS
from .choice import Choice
from .utils import LANGUAGES

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


def generate_word_translating_state(storage, inp):
    text = ""
    if storage.get("training") is None:
        training = WordTranslationTrainingManager(counter_max=5)
        storage["training"] = training
        training.change_current_word()
    else:
        training = storage.get("training")
        text += training.check_right_answer(inp)

    if not training.training_continues:
        text += "Тренировка окончена."
        storage["training"] = None
        training_choice_state("word_translating_state",
                              text + "\nВыберите новую тренировку")
    else:
        next_state = generate_word_translating_state
        text += f"Переведите слово \"{training.word.word}\" " \
            f"на {LANGUAGES[training.right_answer.language]}\n"
        text += f"Подсказка: {training._right_answer.word}"

        InputState(
            name="word_translating_state",
            text=text,
            next=next_state
        )

    return "word_translating_state"


InputState(
    name="START",
    text="",
    next="TRAINING_CHOICE"
)

training_choice_state = lambda name, text: ChoiceState(
    name=name,
    text=text,
    choices=[
        Choice(
            hint="Перевод слов",
            match="слова",
            next=generate_word_translating_state
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

training_choice_state("TRAINING_CHOICE", TEXTS["TRAINING_CHOICE"])
