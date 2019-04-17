from okayenglish.scenariomachine.utils import *


class WordTranslationTrainingManager:
    PHRASES = {
        "right_answer": "Это правильный ответ.\n",
        "wrong_answer": "Это неправильный ответ.\n"
    }

    def __init__(self, counter_max):
        self._current_word = None
        self._right_answer = None

        self._counter_max = counter_max
        self._count = 0

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
        return self.PHRASES["wrong_answer"]

    def change_current_word(self):
        current_language = random.choice(["ru", "en"])

        random_word = get_random_word()
        translate = get_word_translate(random_word, _from="ru", to="en")
        while not translate:
            random_word = get_random_word()
            translate = get_word_translate(random_word, _from="ru", to="en")
        if current_language == "ru":
            self._current_word = word(translate, "ru")
            self._right_answer = word(random_word, "en")
            return
        self._current_word = word(random_word, "en")
        self._right_answer = word(translate, "ru")
