import json
import random
from collections import namedtuple
import requests

from ..local_settings import DICTIONARY_API_KEY

DICTIONARY_API_SERVER = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"

LANGUAGES = {
    "ru": "русский язык",
    "en": "английский язык"
}


def get_random_word():
    with open("okayenglish/static/english_words.txt", encoding="utf-8") as file:
        words = file.readlines()
        return random.choice(words).strip()


def get_word_translate(word, _from, to):
    params = {
        "key": DICTIONARY_API_KEY,
        "text": word,
        "lang": "-".join([_from, to])
    }
    response = requests.get(DICTIONARY_API_SERVER, params).content
    return json.loads(response)["def"][0]["tr"][0]["text"]


def hide_word_letters(word):
    letters = list(word)
    for _ in range(len(word) // 2 + 1):
        random_index = random.randint(0, len(word) - 1)
        while not letters[random_index]:
            random_index = random.randint(0, len(word) - 1)
        letters[random_index] = None
    return " ".join(map(lambda l: "_" if not l else l, letters))


word = namedtuple("word", "word language")
