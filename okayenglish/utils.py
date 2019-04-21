import json
import random
import requests
import re

from okayenglish.local_settings import DICTIONARY_API_KEY, TRANSLATE_API_KEY

TRANSLATE_API_SERVER = "https://translate.yandex.net/api/v1.5/tr.json/translate"
DICTIONARY_API_SERVER = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"

LANGUAGE_NAMES = {
    "ru": "русский язык",
    "en": "английский язык"
}


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
        return random.choice(f.readlines())


def get_random_phrasal_verb():
    with open("okayenglish/static/phrasal_verbs.txt", encoding="utf-8") as file:
        phrases = file.readlines()
        return random.choice(phrases).strip()


def translate_word(word, from_lang, to_lang):
    params = {
        "key": DICTIONARY_API_KEY,
        "text": word,
        "lang": from_lang + "-" + to_lang
    }
    response = requests.get(DICTIONARY_API_SERVER, params).content
    try:
        return json.loads(response)["def"][0]["tr"][0]["text"]
    except IndexError:
        return False


def translate_sentence(sentence):
    params = {
        "key": TRANSLATE_API_KEY,
        "text": sentence,
        "lang": "en-ru"
    }
    response = requests.get(TRANSLATE_API_SERVER, params)
    try:
        return response.json()["text"][0]
    except IndexError:
        return False


def checkable_sentence(sentence):
    return re.sub(r"[.?]", "", sentence.lower().strip())


def hide_word_letters(word):
    letters = list(word.replace(" ", "_"))
    for _ in range(len(word) // 2 + 1):
        random_index = random.randint(0, len(word) - 1)
        while letters[random_index] in ("*", "_"):
            random_index = random.randint(0, len(word) - 1)
        letters[random_index] = "*"
    return " ".join(letters)


def get_sentence_hints(translated_sentence):
    hints = checkable_sentence(translated_sentence).split()
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

