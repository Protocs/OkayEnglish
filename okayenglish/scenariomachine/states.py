import re
import random
import logging

from yaml import YAMLObject, add_constructor

logging.basicConfig(level=logging.DEBUG)


def _indent(func_code):
    """Добавляет отступы в тело функции.

    >>> func = '''def func():
    ... if True:
    ...     return True
    ... '''
    >>> print(_indent(func))
    def func():
        if True:
            return True
    """
    lines = func_code.split("\n")
    for i in range(1, len(lines)):
        lines[i] = "    " + lines[i]
    return "\n".join(lines)


def _create_dynamic_text_function(text):
    """Создает функцию, возвращающую текст сообщения.

    Варианты:

        - text - одно сообщение: возвращает функцию, возвращающую это сообщение.
        - text - список из нескольких сообщений: возвращает функцию,
          возвращающую случайное сообщение из этого списка.
        - text - тело функции Python, начинающееся с ``code``:
          создает функцию с указанным телом, которая должна принять аргумент
          ``storage`` (хранилище сессии) и вернуть текст сообщения.
    """

    if isinstance(text, str):
        # Одна строка
        if "code" not in text:
            return lambda _: text
        else:  # Пользовательская функция
            func = text.replace("code", "def text_func(storage):")
            func = _indent(func)
            logging.error(repr(func))
            exec(func)
            logging.error(locals())
            return locals()["text_func"]
    # Несколько строк в списке
    if isinstance(text, list):
        return lambda _: random.choice(text)


def create_dynamic_next_state_function(text):
    """Создает функцию, возвращающую название следующего состояния.

    Варианты:

        - next - название состояния: возвращает функцию, возвращающую это название.
        - next - тело функции Python, начинающееся с ``code``:
          создает функцию с указанным телом, которая должна принять аргументы
          ``storage`` (хранилище сессии) и ``inp`` (текст ответа пользователя)
          и вернуть название следующего состояния.
    """

    # Одна строка
    if "code" not in text:
        return lambda _, __: text
    else:  # Пользовательская функция
        func = text.replace("code", "def next_func(inp, storage):")
        func = _indent(func)
        logging.error(repr(func))
        exec(func)
        logging.error(locals())
        return locals()["next_func"]


def get_text_and_tts(text_and_tts):
    """
    Раскладывает текст сообщения,
    возможно содержащую данные о произношении, на собственно текст и tts-строку.
    """
    match = re.search(tts_pattern, text_and_tts)
    # Если произношение не задано, произносим как пишем
    if match is None:
        return text_and_tts, text_and_tts
    # Убираем &(...) из текста
    just_text = re.sub(tts_pattern, "", text_and_tts).strip()
    tts = match.group(0)
    return just_text, tts


class AbstractState:
    def __init__(self, name, text):
        logging.info("AbstractState constructor")
        self.name = name
        self.get_text = _create_dynamic_text_function(text)

    def next_state(self, storage, inp):
        """Возвращает следующее состояние, определяемое :func:`get_next_state_name`.

        :param SessionStorage storage: хранилище данных этой сессии.
        :param str inp: ответ пользователя на сообщение этого состояния.
        :rtype: AbstractState
        """
        from okayenglish.scenariomachine.state_parser import find_state_by_name

        return find_state_by_name(self.get_next_state_name(storage, inp))

    def get_next_state_name(self, storage, inp):
        pass


# Регулярное выражения измененного произношения.
# Пример:
#
# Здравствуйте! Это мы, хороводоведы. &(Здравствуйте! Это мы, хоров+одо в+еды.)
tts_pattern = re.compile(r"&\((.*)\)")


class ChoiceState(AbstractState):
    def __init__(self, name, text, choices):
        super().__init__(name, text)
        logging.info("ChoiceState constructor")
        self.choices = choices

    def get_next_state_name(self, storage, inp):
        for choice in self.choices:
            if choice.fits_under(inp):
                return choice.next(storage, inp)
        raise ValueError(
            "ни один выбор не подошёл под ответ.\n"
            'Добавьте Choice с "match: .*", '
            'чтобы задать выбор "Не поняла".'
        )


class InputState(AbstractState):
    def __init__(self, name, text, next):
        super().__init__(name, text)
        self.next = create_dynamic_next_state_function(next)

    def get_next_state_name(self, storage, inp):
        return self.next(storage, inp)


class FinalState(AbstractState):
    def get_next_state_name(self, storage, inp):
        return None


def choices_constructor(loader, node):
    value = loader.construct_mapping(node)
    return ChoiceState(value["name"], value["text"], value["choices"])


def input_constructor(loader, node):
    value = loader.construct_mapping(node)
    return InputState(value["name"], value["text"], value["next"])


def final_constructor(loader, node):
    value = loader.construct_mapping(node)
    return FinalState(value["name"], value["text"])


add_constructor("!Choices", choices_constructor)
add_constructor("!Input", input_constructor)
add_constructor("!Exit", final_constructor)
