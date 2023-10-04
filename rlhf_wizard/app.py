import random
from typing import Any


class Model:
    _model: dict[str, list] = {}
    _current_selections: dict[str, Any] = {}

    def _validate_parameter_variations(self, kwargs):
        if (
            len(kwargs) != 1
            or not isinstance(kwargs.get(list(kwargs.keys())[0]), list)
            or not kwargs.get(list(kwargs.keys())[0])
        ):
            raise ValueError("Argument must have exactly one non-empty list value")

    def _track_choice(self, key, choice):
        self._current_selections[key] = choice

    def parameter(self, **kwargs):
        self._validate_parameter_variations(kwargs)

        k, value_list = list(kwargs.items())[0]
        choice = random.choice(value_list)
        self._track_choice(k, choice)
        return choice
