import random
from typing import Any


def _validate_variations(kwargs):
    if (
        len(kwargs) != 1
        or not isinstance(kwargs.get(list(kwargs.keys())[0]), list)
        or not kwargs.get(list(kwargs.keys())[0])
    ):
        raise ValueError("Argument must have exactly one non-empty list value")


class Model:
    _model: dict[str, list] = {}
    _current_selections: dict[str, Any] = {}

    def parameter(self, **kwargs):
        _validate_variations(kwargs)

        k, value_list = list(kwargs.items())[0]
        choice = random.choice(value_list)
        self._current_selections[k] = choice
        return choice
