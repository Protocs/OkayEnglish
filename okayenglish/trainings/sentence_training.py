from okayenglish.utils import checkable_sentence, get_random_sentence, \
    translate_sentence

SENTENCES_PER_TRAINING = 5


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
        return self._translated_so_far < SENTENCES_PER_TRAINING

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
