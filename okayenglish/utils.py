import json
import random
import requests
import re

from okayenglish.local_settings import DICTIONARY_API_KEY
from okayenglish.texts import TRAININGS
from okayenglish.states import WORD_TRAINING, PHRASAL_VERBS_TRAINING, SENTENCE_TRAINING

TRANSLATE_API_SERVER = "https://translate.yandex.net/api/v1.5/tr.json/translate"
DICTIONARY_API_SERVER = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"

LANGUAGE_NAMES = {"ru": "русский язык", "en": "английский язык"}

TRAINING_NAMES = {
    WORD_TRAINING: "Перевод слов",
    PHRASAL_VERBS_TRAINING: "Перевод фразовых глаголов",
    SENTENCE_TRAINING: "Перевод предложений",
}

TRAINING_SUGGESTS = [
    {"title": TRAINING_NAMES[training], "hide": True} for training in TRAINING_NAMES
] + [{"title": "Статистика", "hide": True}]

TRAINING_PROCESS_SUGGESTS = [
                {"title": "Подсказка", "hide": True},
                {"title": "Не знаю", "hide": True},
                {"title": "Хватит", "hide": True},
            ]

def get_random_russian_word():
    with open("okayenglish/static/russian_words.txt", encoding="utf-8") as file:
        words = file.readlines()
        return random.choice(words).strip()


def get_random_english_word():
    with open("okayenglish/static/english_words.txt", encoding="utf-8") as file:
        words = file.readlines()
        return random.choice(words).strip()


def get_random_sentence():
    with open("okayenglish/static/sentences.txt", encoding="utf-8") as f:
        sentence = random.choice(f.readlines()).split("|")
        return sentence[0].strip(), sentence[1].strip()


def get_random_phrasal_verb():
    with open("okayenglish/static/phrasal_verbs.txt", encoding="utf-8") as f:
        phrases = random.choice(f.readlines()).split("|")
        return phrases[0].strip(), phrases[1].strip()


def translate_word(word, from_lang, to_lang):
    params = {
        "key": DICTIONARY_API_KEY,
        "text": word,
        "lang": from_lang + "-" + to_lang,
    }
    response = requests.get(DICTIONARY_API_SERVER, params).content
    try:
        return json.loads(response)["def"][0]["tr"][0]["text"]
    except IndexError:
        return False


def checkable_sentence(sentence):
    return re.sub(r"[.?]", "", sentence.lower().strip())


def get_tip_letters(word_length):
    if word_length <= 6:
        tip_letters = 1
    elif 6 < word_length <= 12:
        tip_letters = 2
    else:
        tip_letters = 3
    return tip_letters


def hide_word_letters(word, to_hide=None):
    letters = list(word.replace(" ", "_"))
    for _ in range(len(word) // 2 + 1 if to_hide is None else to_hide):
        random_index = random.randint(0, len(word) - 1)
        while letters[random_index] in ("*", "_"):
            random_index = random.randint(0, len(word) - 1)
        letters[random_index] = "*"
    return " ".join(letters)


def get_sentence_hints(translated_sentence, duds=True):
    hints = checkable_sentence(translated_sentence).split()
    if duds:
        duds_to_add = len(hints)
        hints += [get_random_english_word() for _ in range(duds_to_add)]
    random.shuffle(hints)
    return hints


class Word:
    def __init__(self, word, language):
        self.word = word
        self.language = language

    def __str__(self):
        return self.word
