import re

from okayenglish.states import *
from okayenglish.texts import GREETING as GREETING_TEXT
from okayenglish.trainings.word_training import WordTranslationTrainingManager
from okayenglish.utils import hide_word_letters, LANGUAGE_NAMES


class Session:
    def __init__(self, user):
        self._user = user
        self._current_state = GREETING
        self._training_manager = None

    def handle_state(self, req_parser, resp_parser):
        if self._current_state == GREETING:
            resp_parser.reply_text = GREETING_TEXT
            self._current_state = TRAINING_SELECT
        elif self._current_state == TRAINING_SELECT:
            self.select_training(req_parser, resp_parser)
        elif self._current_state == WORD_TRAINING:
            self.handle_word_training_question(req_parser, resp_parser)
        elif self._current_state == SENTENCE_TRAINING:
            ...  # TODO
        elif self._current_state == TEXT_TRAINING:
            ...  # TODO

    def select_training(self, req_parser, resp_parser):
        if re.findall("1|слов", req_parser.text, re.IGNORECASE):
            self.begin_word_training(resp_parser)
        if re.findall("2|предложени", req_parser.text, re.IGNORECASE):
            self._current_state = SENTENCE_TRAINING
            self._training_manager = ...
            ...  # TODO
        if re.findall("3|текст", req_parser.text, re.IGNORECASE):
            self._current_state = TEXT_TRAINING
            self._training_manager = ...
            ...  # TODO

    def begin_word_training(self, resp_parser):
        self._current_state = WORD_TRAINING
        training = self._training_manager = WordTranslationTrainingManager()
        word_with_hidden_letters = hide_word_letters(training.answer.word)
        text = (
            f'Переведите слово "{training.word.word}" '
            f"на {LANGUAGE_NAMES[training.answer.language]}\n"
        )
        text += f"Подсказка: {word_with_hidden_letters}\n"
        resp_parser.reply_text = text

    def handle_word_training_question(self, req_parser, resp_parser):
        training = self._training_manager
        text = training.check_right_answer(req_parser.text)
        # Если количество отработанных слов равняется ``counter_max``,
        # значит тренировка окончена
        if not training.should_continue_training:
            text += "Тренировка окончена."
            self._training_manager = None
            # Состояние после
            # последнего отработанного слова - состояние выбора тренировки
            self._current_state = TRAINING_SELECT
            text += "\nВыбирайте новую тренировку"
        else:
            word_with_hidden_letters = hide_word_letters(training.answer.word)
            text += (
                f'Переведите слово "{training.word.word}" '
                f"на {LANGUAGE_NAMES[training.answer.language]}\n"
            )
            text += f"Подсказка: {word_with_hidden_letters}\n"
        resp_parser.reply_text = text
