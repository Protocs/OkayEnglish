import re

from okayenglish.states import *
from okayenglish.texts import (
    GREETING as GREETING_TEXT,
    TRAININGS as TRAININGS_TEXT,
    MAIN_MENU_HELP,
    UNKNOWN_REQUEST,
)
from okayenglish.trainings.word_training import WordTrainingManager
from okayenglish.trainings.sentence_training import SentenceTrainingManager
from okayenglish.trainings.phrasal_verbs_training import PhrasalVerbsTrainingManager
from okayenglish.trainings._base_training_manager import TrainingManager
from okayenglish.utils import (
    hide_word_letters,
    LANGUAGE_NAMES,
    get_sentence_hints,
    TRAINING_SUGGESTS,
    TRAINING_NAMES,
)


class Session:
    def __init__(self, user):
        self._user = user
        self._current_state = GREETING
        self._training_manager = None

    def handle_state(self, req_parser, resp_parser):
        if self._current_state == GREETING:
            resp_parser.reply_text = GREETING_TEXT
            self.change_current_state(TRAINING_SELECT, resp_parser)
        elif self._current_state == TRAINING_SELECT:
            self.select_training(req_parser, resp_parser)
        elif self._current_state == WORD_TRAINING:
            self.handle_word_training_question(req_parser, resp_parser)
        elif self._current_state == SENTENCE_TRAINING:
            self.handle_sentence_training_question(req_parser, resp_parser)
        elif self._current_state == PHRASAL_VERBS_TRAINING:
            self.handle_phrasal_verb_training_question(req_parser, resp_parser)

    def select_training(self, req_parser, resp_parser):
        if re.findall("помощь|что ты умеешь", req_parser.text, re.IGNORECASE):
            resp_parser.reply_text = MAIN_MENU_HELP
        elif re.findall("1|слов", req_parser.text, re.IGNORECASE):
            self.begin_word_training(resp_parser)
        elif re.findall("2|предложени", req_parser.text, re.IGNORECASE):
            self.begin_sentence_training(resp_parser)
        elif re.findall("3|фраз", req_parser.text, re.IGNORECASE):
            self.begin_phrasal_verbs_training(resp_parser)
        elif re.findall("статистика", req_parser.text, re.IGNORECASE):
            self.handle_stats(req_parser, resp_parser)
        else:
            resp_parser.reply_text = UNKNOWN_REQUEST

    def begin_word_training(self, resp_parser):
        self.change_current_state(WORD_TRAINING, resp_parser)
        training = self._training_manager = WordTrainingManager(self)
        word_with_hidden_letters = hide_word_letters(training.answer.word)
        text = (
            f"Переведите слово «{training.item_to_translate.word}» "
            f"на {LANGUAGE_NAMES[training.answer.language]}\n"
        )
        text += f"Подсказка: {word_with_hidden_letters}\n"
        resp_parser.reply_text = text

    def begin_sentence_training(self, resp_parser):
        self.change_current_state(SENTENCE_TRAINING, resp_parser)
        training = self._training_manager = SentenceTrainingManager(self)
        hints = get_sentence_hints(training.answer)
        text = (
            f'Переведите предложение "{training.item_to_translate.strip()}" '
            f"на английский\n"
        )
        text += f"Подсказки: {', '.join(hints)}\n"
        resp_parser.reply_text = text

    def begin_phrasal_verbs_training(self, resp_parser):
        self.change_current_state(PHRASAL_VERBS_TRAINING, resp_parser)
        training = self._training_manager = PhrasalVerbsTrainingManager(self)
        phrase_with_hidden_letters = hide_word_letters(training.answer)
        text = f"Переведите фразу «{training.item_to_translate}» на русский язык\n"
        text += f"Подсказка: {phrase_with_hidden_letters}\n"
        resp_parser.reply_text = text

    def handle_phrasal_verb_training_question(self, req_parser, resp_parser):
        training = self._training_manager
        text = training.check_answer(req_parser.text)
        if not training.should_continue_training:
            text += "Тренировка окончена."
            if not training.training_interrupt:
                self.save_stats(req_parser)
                text += self.show_stats()
            self._training_manager = None
            self.change_current_state(TRAINING_SELECT, resp_parser)
            text += "\nВыбирайте новую тренировку" + TRAININGS_TEXT
        else:
            phrase_with_hidden_letters = hide_word_letters(
                training.answer, training.symbols_to_hide
            )
            text += f"Переведите фразу «{training.item_to_translate}» на русский язык\n"
            text += f"Подсказка: {phrase_with_hidden_letters}\n"
        resp_parser.reply_text = text

    def handle_word_training_question(self, req_parser, resp_parser):
        training = self._training_manager
        text = training.check_answer(req_parser.text)
        # Если количество отработанных слов равняется ``counter_max``,
        # значит тренировка окончена
        if not training.should_continue_training:
            text += "Тренировка окончена."
            if not training.training_interrupt:
                self.save_stats(req_parser)
                text += self.show_stats()
            self._training_manager = None
            # Состояние после
            # последнего отработанного слова - состояние выбора тренировки
            self.change_current_state(TRAINING_SELECT, resp_parser)
            text += "\nВыбирайте новую тренировку" + TRAININGS_TEXT
        else:
            word_with_hidden_letters = hide_word_letters(
                training.answer.word, training.symbols_to_hide
            )
            text += (
                f"Переведите слово «{training.item_to_translate.word}» "
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
            if not training.training_interrupt:
                self.save_stats(req_parser)
                text += self.show_stats()

            self._training_manager = None
            # Состояние после
            # последнего отработанного предложения - состояние выбора тренировки
            self.change_current_state(TRAINING_SELECT, resp_parser)
            text += "\nВыбирайте новую тренировку" + TRAININGS_TEXT
        else:
            hints = get_sentence_hints(training.answer, not training.tip)
            text += (
                f'Переведите предложение "{training.item_to_translate.strip()}" '
                f"на английский\n"
            )
            text += f"Подсказки: {', '.join(hints)}\n"
        resp_parser.reply_text = text

    def handle_stats(self, req_parser, resp_parser):
        from okayenglish.db import get_user_stats

        self.change_current_state(STATS, resp_parser)
        text = "Ваша статистика:\n"
        for training in (WORD_TRAINING, PHRASAL_VERBS_TRAINING, SENTENCE_TRAINING):
            stats = get_user_stats(req_parser.user_id, training)
            if not stats:
                continue
            training_count = len(stats)
            right_answers_percent = round(
                sum(tr.right_answers for tr in stats)
                / sum([tr.right_answers + tr.wrong_answers for tr in stats])
                * 100,
                2,
            )
            text += (
                f"{TRAINING_NAMES[training]}: "
                f"количество тренировок - {training_count}, "
                f"процент правильных ответов - {right_answers_percent}%\n"
            )
        self.change_current_state(TRAINING_SELECT, resp_parser)
        resp_parser.reply_text = text

    def save_stats(self, req_parser):
        from okayenglish.db import db, TrainingStats

        stats = self._training_manager.get_stats()
        db.session.add(
            TrainingStats(
                user_id=req_parser.user_id,
                right_answers=stats[0],
                wrong_answers=stats[1] + stats[2] / 2,
                training_type=self._current_state,
            )
        )
        db.session.commit()

    def show_stats(self):
        stats = self._training_manager.get_stats()
        text = "\nРезультат тренировки: "
        right_answers_percent = round(
            stats[0] / (TrainingManager.ITEMS_PER_TRAINING + stats[1]) * 100, 2
        )
        text += f"процент правильных ответов: {right_answers_percent}%"

        return text

    def change_current_state(self, new_state, resp_parser):
        resp_parser["response"]["buttons"] = []
        if new_state == TRAINING_SELECT:
            resp_parser["response"]["buttons"] = TRAINING_SUGGESTS
        elif new_state.endswith("training"):
            resp_parser["response"]["buttons"] = [
                {"title": "Подсказка", "hide": True},
                {"title": "Не знаю", "hide": True},
                {"title": "Хватит", "hide": True},
            ]

        self._current_state = new_state
