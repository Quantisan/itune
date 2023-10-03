import random
from typing import List


def _validate_variations(variations, func):
    if not isinstance(variations, list):
        raise TypeError("variations must be a list")
    func_return_type = func.__annotations__.get("return")
    if func_return_type:
        if not all(isinstance(x, func_return_type) for x in variations):
            raise TypeError(
                "all variations must have the same type as the function return type"
            )


class Model:
    _model: dict[str, List] = {}

    def parameter(self, **kwargs):
        assert len(kwargs) == 1
        assert list(kwargs.values())
        assert isinstance(list(kwargs.values())[0], list)
        self._model.update(kwargs)
        return random.choice(list(kwargs.values())[0])

    def experiment(self, variations):
        def decorator(func):
            _validate_variations(variations, func)

            self._model[func.__name__] = variations

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def get_variation(self):
        ## TODO: get the calling function name
        return self._model.get("three")[0]
