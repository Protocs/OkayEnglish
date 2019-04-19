import random

from okayenglish.utils import get_word_translate, word, get_random_word


class WordTranslationTrainingManager:
    PHRASES = {
        "right_answer": "Это правильный ответ.\n",
        "wrong_answer": "Это неправильный ответ.\n"
                        "Если не знаете перевода, просто скажите «не знаю».\n",
        "idk_answer": "Ничего страшного.\nПравильный ответ - {}\n"
    }

    def __init__(self, counter_max):
        self._current_word = None
        self._right_answer = None

        self._counter_max = counter_max
        self._count = 0

        self.change_current_word()

    @property
    def training_continues(self):
        return self._count < self._counter_max

    @property
    def word(self):
        return self._current_word

    @property
    def right_answer(self):
        return self._right_answer

    def check_right_answer(self, inp):
        if inp == self._right_answer.word:
            self.change_current_word()
            self._count += 1
            return self.PHRASES["right_answer"]
        elif any(word in inp.lower() for word in ("хз", "не знаю", "понятия")):
            phrase = self.PHRASES["idk_answer"].format(self._right_answer.word)
            self.change_current_word()
            return phrase
        return self.PHRASES["wrong_answer"]

    def change_current_word(self):
        current_language = random.choice(["ru", "en"])

        random_word = get_random_word()
        translate = get_word_translate(random_word, _from="ru", to="en")
        while not translate:
            random_word = get_random_word()
            translate = get_word_translate(random_word, _from="ru", to="en")
        if current_language == "ru":
            self._current_word = word(translate, "en")
            self._right_answer = word(random_word, "ru")
            return
        self._current_word = word(random_word, "ru")
        self._right_answer = word(translate, "en")
