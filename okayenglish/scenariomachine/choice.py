import re

from yaml import add_constructor

from okayenglish.scenariomachine.states import create_dynamic_next_state_function


class Choice:
    yaml_tag = "!Choice"

    def __init__(self, match, next, hint, prepend_next_text):
        self.hint = hint
        self.match = match
        self.next = create_dynamic_next_state_function(next)
        self.prepend_next_text = prepend_next_text
        if isinstance(prepend_next_text, str):
            self.prepend_next_text = (prepend_next_text,)

    def fits_under(self, response):
        """
        Возвращает ``True``,
        если ``response`` подходит под этот вариант,
        иначе ``False``.
        """
        return re.match(self.match, response) is not None


def choice_constructor(loader, node):
    value = loader.construct_mapping(node)
    return Choice(
        value["match"],
        value["next"],
        value.get("hint"),
        value.get("prepend_next_text", ()),
    )


add_constructor("!Choice", choice_constructor)
