from okayenglish.trainings._base_training_manager import TrainingManager

from okayenglish.utils import (
    checkable_sentence,
    get_random_sentence,
    translate_sentence,
)


class SentenceTrainingManager(TrainingManager):
    def check_input(self, inp, answer):
        return checkable_sentence(inp) == checkable_sentence(self.answer)

    def next_item(self):
        sentence = get_random_sentence()
        self.answer = sentence[0]
        self.item_to_translate = sentence[1]
