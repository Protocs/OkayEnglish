from okayenglish.trainings._base_training_manager import TrainingManager

from okayenglish.utils import translate_word, Word, get_random_phrasal_verb


class PhrasalVerbsTrainingManager(TrainingManager):
    def check_input(self, inp, answer):
        return inp.lower().strip() == self.answer.word

    def next_item(self):
        random_phrase = get_random_phrasal_verb()
        translate = translate_word(random_phrase, from_lang="en", to_lang="ru")
        while not translate:
            random_phrase = get_random_phrasal_verb()
            translate = translate_word(random_phrase, from_lang="en", to_lang="ru")

        self.item_to_translate = Word(random_phrase, "en")
        self.answer = Word(translate, "ru")
