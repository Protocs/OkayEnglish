import random

from okayenglish.utils import translate_word, Word, \
    get_random_sentence, translate_sentence, get_random_russian_word, checkable_sentence

WORDS_PER_TRAINING = 5


class WordTranslationTrainingManager:
    PHRASES = {
        "right_answer": "Это правильный ответ.\n",
        "wrong_answer": "Это неправильный ответ.\n"
                        "Если не знаете перевода, просто скажите «не знаю».\n",
        "idk_answer": "Ничего страшного.\nПравильный ответ - {}\n",
    }

    def __init__(self):
        self.word = None
        self.answer = None
        self._translated_so_far = 0

        self.next_word()

    @property
    def should_continue_training(self):
        return self._translated_so_far < WORDS_PER_TRAINING

    def check_answer(self, inp):
        if inp == self.answer.word:
            self.next_word()
            self._translated_so_far += 1
            return self.PHRASES["right_answer"]
        elif any(word in inp.lower() for word in ("хз", "не знаю", "понятия")):
            phrase = self.PHRASES["idk_answer"].format(self.answer.word)
            self.next_word()
            return phrase
        return self.PHRASES["wrong_answer"]

    def next_word(self):
        current_language = random.choice(["ru", "en"])
        random_word = get_random_russian_word()
        translate = translate_word(random_word, from_lang="ru", to_lang="en")
        while not translate:
            random_word = get_random_russian_word()
            translate = translate_word(random_word, from_lang="ru", to_lang="en")
        if current_language == "ru":
            self.word = Word(translate, "en")
            self.answer = Word(random_word, "ru")
            return
        self.word = Word(random_word, "ru")
        self.answer = Word(translate, "en")


class SentenceTranslationTrainingManager:
    PHRASES = {
        "right_answer": "Это правильный ответ.\n",
        "wrong_answer": "Это неправильный ответ.\n"
                        "Если не знаете перевода, просто скажите «не знаю».\n",
        "idk_answer": "Ничего страшного.\nПравильный ответ - {}\n",
    }

    def __init__(self):
        self.sentence = None
        self.answer = None
        self._translated_so_far = 0

        self.next_sentence()

    @property
    def should_continue_training(self):
        return self._translated_so_far < WORDS_PER_TRAINING

    def check_answer(self, inp):
        if checkable_sentence(inp) == checkable_sentence(self.answer):
            self.next_sentence()
            self._translated_so_far += 1
            return self.PHRASES["right_answer"]
        elif any(word in inp.lower() for word in ("хз", "не знаю", "понятия")):
            phrase = self.PHRASES["idk_answer"].format(self.answer)
            self.next_sentence()
            return phrase
        return self.PHRASES["wrong_answer"]

    def next_sentence(self):
        self.answer = get_random_sentence()
        self.sentence = translate_sentence(self.answer)
