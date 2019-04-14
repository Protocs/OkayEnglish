"""Парсер файла сценариев."""

import yaml
# noinspection PyUnresolvedReferences
from okayenglish.scenariomachine.states import *
# noinspection PyUnresolvedReferences
from okayenglish.scenariomachine.choice import Choice
from okayenglish.config import SCENARIO_FILE

__all__ = ["parse_file", "find_state_by_name"]

scenario_file = open(SCENARIO_FILE, encoding="utf-8")
states = []


class ScenarioParsingError(Exception):
    pass


def find_state_by_name(name):
    try:
        return next(s for s in states if s.name == name)
    except StopIteration:
        raise ValueError(f"состояние {name!r} не найдено")


def parse_file(fp):
    states.extend(yaml.load_all(scenario_file))


parse_file(SCENARIO_FILE)
