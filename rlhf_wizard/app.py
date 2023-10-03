import random
from typing import List


def _validate_variations(kwargs):
    if (
        len(kwargs) != 1
        or not isinstance(kwargs.get(list(kwargs.keys())[0]), list)
        or not kwargs.get(list(kwargs.keys())[0])
    ):
        raise ValueError("Argument must have exactly one non-empty list value")


class Model:
    _model: dict[str, List] = {}

    def parameter(self, **kwargs):
        _validate_variations(kwargs)

        self._model.update(kwargs)
        return random.choice(list(kwargs.values())[0])
