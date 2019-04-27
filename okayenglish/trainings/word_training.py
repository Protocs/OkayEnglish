import random

from okayenglish.trainings._base_training_manager import TrainingManager
from okayenglish.utils import (
    translate_word,
    Word,
    get_random_russian_word,
    get_tip_letters,
)


class WordTrainingManager(TrainingManager):
    @property
    def symbols_to_hide(self):
        tip_letters = 0
        if self.tip:
            tip_letters = get_tip_letters(len(self.answer.word))
        return len(self.answer.word) // 2 + 1 - tip_letters

    def check_input(self, inp, answer):
        return inp.lower().strip() == answer.word.lower()

    def next_item(self):
        current_language = random.choice(["ru", "en"])
        random_word = get_random_russian_word()
        translate = translate_word(random_word, from_lang="ru", to_lang="en")
        while not translate:
            random_word = get_random_russian_word()
            translate = translate_word(random_word, from_lang="ru", to_lang="en")
        if current_language == "ru":
            self.item_to_translate = Word(translate, "en")
            self.answer = Word(random_word, "ru")
            return
        self.item_to_translate = Word(random_word, "ru")
        self.answer = Word(translate, "en")
