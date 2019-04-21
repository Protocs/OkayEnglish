import re

from okayenglish.states import *
from okayenglish.texts import GREETING as GREETING_TEXT, TRAININGS as TRAININGS_TEXT
from okayenglish.trainings.word_training import WordTrainingManager
from okayenglish.trainings.sentence_training import SentenceTrainingManager
from okayenglish.trainings.phrasal_verbs_training import PhrasalVerbsTrainingManager
from okayenglish.utils import hide_word_letters, LANGUAGE_NAMES, get_sentence_hints


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
            self.handle_sentence_training_question(req_parser, resp_parser)
        elif self._current_state == PHRASAL_VERBS_TRAINING:
            self.handle_phrasal_verb_training_question(req_parser, resp_parser)
        elif self._current_state == TEXT_TRAINING:
            ...  # TODO

    def select_training(self, req_parser, resp_parser):
        if re.findall("1|слов", req_parser.text, re.IGNORECASE):
            self.begin_word_training(resp_parser)
        if re.findall("2|предложени", req_parser.text, re.IGNORECASE):
            self.begin_sentence_training(resp_parser)
        if re.findall("3|текст", req_parser.text, re.IGNORECASE):
            self._current_state = TEXT_TRAINING
            self._training_manager = ...
            ...  # TODO
        if re.findall("4|фраз", req_parser.text, re.IGNORECASE):
            self.begin_phrasal_verbs_training(resp_parser)

    def begin_word_training(self, resp_parser):
        self._current_state = WORD_TRAINING
        training = self._training_manager = WordTrainingManager(self)
        word_with_hidden_letters = hide_word_letters(training.answer.word)
        text = (
            f'Переведите слово «{training.item_to_translate.word}» '
            f"на {LANGUAGE_NAMES[training.answer.language]}\n"
        )
        text += f"Подсказка: {word_with_hidden_letters}\n"
        resp_parser.reply_text = text

    def begin_sentence_training(self, resp_parser):
        self._current_state = SENTENCE_TRAINING
        training = self._training_manager = SentenceTrainingManager(self)
        hints = get_sentence_hints(training.answer)
        text = (
            f'Переведите предложение "{training.item_to_translate.strip()}" '
            f"на английский\n"
        )
        text += f"Подсказки: {', '.join(hints)}\n"
        resp_parser.reply_text = text

    def begin_phrasal_verbs_training(self, resp_parser):
        self._current_state = PHRASAL_VERBS_TRAINING
        training = self._training_manager = PhrasalVerbsTrainingManager(self)
        phrase_with_hidden_letters = hide_word_letters(training.answer.word)
        text = f"Переведите фразу «{training.item_to_translate.word}» на русский язык\n"
        text += f"Подсказка: {phrase_with_hidden_letters}\n"
        resp_parser.reply_text = text

    def handle_phrasal_verb_training_question(self, req_parser, resp_parser):
        training = self._training_manager
        text = training.check_answer(req_parser.text)
        if not training.should_continue_training:
            text += "Тренировка окончена."
            self._training_manager = None
            self._current_state = TRAINING_SELECT
            text += "\nВыбирайте новую тренировку" + TRAININGS_TEXT
        else:
            phrase_with_hidden_letters = hide_word_letters(training.answer.word)
            text += f"Переведите фразу «{training.item_to_translate.word}» на русский язык\n"
            text += f"Подсказка: {phrase_with_hidden_letters}\n"
        resp_parser.reply_text = text

    def handle_word_training_question(self, req_parser, resp_parser):
        training = self._training_manager
        text = training.check_answer(req_parser.text)
        # Если количество отработанных слов равняется ``counter_max``,
        # значит тренировка окончена
        if not training.should_continue_training:
            text += "Тренировка окончена."
            self._training_manager = None
            # Состояние после
            # последнего отработанного слова - состояние выбора тренировки
            self._current_state = TRAINING_SELECT
            text += "\nВыбирайте новую тренировку" + TRAININGS_TEXT
        else:
            word_with_hidden_letters = hide_word_letters(training.answer.word)
            text += (
                f'Переведите слово «{training.item_to_translate.word}» '
                f"на {LANGUAGE_NAMES[training.answer.language]}\n"
            )
            text += f"Подсказка: {word_with_hidden_letters}\n"
        resp_parser.reply_text = text

    def handle_sentence_training_question(self, req_parser, resp_parser):
        training = self._training_manager
        text = training.check_answer(req_parser.text)
        # Если количество отработанных предложений равняется ``counter_max``,
        # значит тренировка окончена
        if not training.should_continue_training:
            text += "Тренировка окончена."
            self._training_manager = None
            # Состояние после
            # последнего отработанного предложения - состояние выбора тренировки
            self._current_state = TRAINING_SELECT
            text += "\nВыбирайте новую тренировку" + TRAININGS_TEXT
        else:
            hints = get_sentence_hints(training.answer)
            text += (
                f'Переведите предложение "{training.item_to_translate.strip()}" '
                f"на английский\n"
            )
            text += f"Подсказки: {', '.join(hints)}\n"
        resp_parser.reply_text = text
