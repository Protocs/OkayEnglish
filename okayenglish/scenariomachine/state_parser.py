"""Парсер файла сценариев."""

import yaml
# noinspection PyUnresolvedReferences
from okayenglish.scenariomachine.states import *
# noinspection PyUnresolvedReferences
from okayenglish.scenariomachine.choice import Choice
from okayenglish.config import SCENARIO_FILE

__all__ = ["parse_file", "find_state_by_name"]

states = []


class ScenarioParsingError(Exception):
    pass


def find_state_by_name(name):
    return next(s for s in states if s.name == name)


def parse_file(fp):
    states.extend(load_states_from_file(fp))
    check_start_state_exists()


def load_states_from_file(fp):
    with open(fp, encoding="utf-8") as f:
        return yaml.load_all(f)


def check_start_state_exists():
    try:
        find_state_by_name("START")
    except StopIteration:
        raise ScenarioParsingError("состояние START не найдено.")


load_states_from_file(SCENARIO_FILE)
