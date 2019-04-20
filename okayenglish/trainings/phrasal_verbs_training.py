from okayenglish.utils import translate_word, Word, get_random_phrasal_verb

PHRASAL_PER_TRAINING = 5


class PhrasalVerbsTrainingManager:
    PHRASES = {
        "right_answer": "Это правильный ответ.\n",
        "wrong_answer": "Это неправильный ответ.\n"
                        "Если не знаете перевода, просто скажите «не знаю».\n",
        "idk_answer": "Ничего страшного.\nПравильный ответ - {}\n",
    }

    def __init__(self):
        self.phrase = None
        self.answer = None
        self._translated_so_far = 0

        self.next_phrase()

    @property
    def should_continue_training(self):
        return self._translated_so_far < PHRASAL_PER_TRAINING

    def check_right_answer(self, inp):
        if inp == self.answer.word:
            self.next_phrase()
            self._translated_so_far += 1
            return self.PHRASES["right_answer"]
        elif any(word in inp.lower() for word in ("хз", "не знаю", "понятия")):
            phrase = self.PHRASES["idk_answer"].format(self.answer.word)
            self.next_phrase()
            return phrase
        return self.PHRASES["wrong_answer"]

    def next_phrase(self):
        random_phrase = get_random_phrasal_verb()
        translate = translate_word(random_phrase, from_lang="en", to_lang="ru")
        while not translate:
            random_phrase = get_random_phrasal_verb()
            translate = translate_word(random_phrase, from_lang="en", to_lang="ru")

        self.phrase = Word(random_phrase, "en")
        self.answer = Word(translate, "ru")
