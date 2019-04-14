import json
import random
from collections import namedtuple
import requests

from ..local_settings import TRANSLATOR_API_KEY

TRANSLATOR_API_SERVER = "https://translate.yandex.net/api/v1.5/tr.json/translate"

LANGUAGES = {
    "ru": "русский язык",
    "en": "английский язык"
}


def get_random_word():
    with open("static/english_words.txt", encoding="utf-8") as file:
        words = file.readlines()
        return random.choice(words).strip()


def get_word_translate(word, _from, to):
    params = {
        "key": TRANSLATOR_API_KEY,
        "text": word,
        "lang": "-".join([_from, to])
    }
    response = requests.get(TRANSLATOR_API_SERVER, params).content
    return json.loads(response)["text"][0]


word = namedtuple("word", "word language")
