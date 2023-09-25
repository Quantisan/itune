from typing import List


class Model:
    _model: dict[str, List] = {}

    def experiment(self, variations):
        def decorator(func):
            assert isinstance(variations, list)
            assert all(
                isinstance(x, func.__annotations__["return"]) for x in variations
            )
   
            self._model[func.__name__] = variations

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def get_variation(self):
        ## TODO: get the calling function name
        return self._model.get("three")[0]
