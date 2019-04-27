from okayenglish.trainings._base_training_manager import TrainingManager

from okayenglish.utils import (
    get_random_phrasal_verb,
    get_tip_letters,
)


class PhrasalVerbsTrainingManager(TrainingManager):
    @property
    def symbols_to_hide(self):
        tip_letters = 0
        if self.tip:
            tip_letters = get_tip_letters(len(self.answer))
        return len(self.answer) // 2 + 1 - tip_letters

    def check_input(self, inp, answer):
        return inp.lower().strip() == self.answer.lower()

    def next_item(self):
        random_phrase = get_random_phrasal_verb()

        self.item_to_translate = random_phrase[1]
        self.answer = random_phrase[0]
