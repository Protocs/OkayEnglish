from okayenglish.trainings._base_training_manager import TrainingManager

from okayenglish.utils import translate_word, Word, get_random_phrasal_verb


class PhrasalVerbsTrainingManager(TrainingManager):
    def check_input(self, inp, answer):
        return inp.lower().strip() == self.answer.lower()

    def next_item(self):
        random_phrase = get_random_phrasal_verb()

        self.item_to_translate = random_phrase[1]
        self.answer = random_phrase[0]
