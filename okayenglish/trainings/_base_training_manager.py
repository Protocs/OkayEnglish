from abc import ABC, abstractmethod


class TrainingManager(ABC):
    _PHRASES = {
        "right_answer": "Это правильный ответ.\n",
        "wrong_answer": "Это неправильный ответ.\n"
                        "Если не знаете перевода, просто скажите «не знаю».\n",
        "idk_answer": "Ничего страшного.\nПравильный ответ - {}\n",
    }
    ITEMS_PER_TRAINING = 5

    def __init__(self):
        self.item_to_translate = None
        self.answer = None
        self._translated_so_far = 0

        self.next_item()

    @property
    def should_continue_training(self):
        return self._translated_so_far < self.ITEMS_PER_TRAINING

    @abstractmethod
    def check_input(self, inp, answer):
        pass

    def check_answer(self, inp):
        if self.check_input(inp, self.answer):
            self.next_item()
            self._translated_so_far += 1
            return self._PHRASES["right_answer"]
        elif any(word in inp.lower() for word in ("хз", "не знаю", "понятия")):
            self.next_item()
            return self._PHRASES["idk_answer"].format(self.answer)
        return self._PHRASES["wrong_answer"]

    @abstractmethod
    def next_item(self):
        pass
