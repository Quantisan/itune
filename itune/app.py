import random
from typing import Any


class Model:
    def __init__(self):
        self._model: dict[str, dict] = {}
        self._current_selections: dict[str, Any] = {}

    def _validate_parameter_variations(self, kwargs):
        if (
            len(kwargs) != 1
            or not isinstance(kwargs.get(list(kwargs.keys())[0]), list)
            or not kwargs.get(list(kwargs.keys())[0])
        ):
            raise ValueError("Argument must have exactly one non-empty list value")

    def _track_choice(self, key, choice):
        if key not in self._current_selections:
            self._current_selections[str(key)] = choice
        else:
            raise Exception(f"Parameter `{key}` has already been selected")

    def _seed_model(self, k, value_list):
        self._model[k] = {
            "successes": {str(value): 0 for value in value_list},
            "failures": {str(value): 0 for value in value_list},
        }

    def _choose_parameter(self, k, value_list):
        if k not in self._model:
            raise Exception(f"Parameter `{k}` is not in the model")

        # note that keys are saved as strings
        original_value_list = list(self._model[k]["successes"].keys())
        new_value_list = [str(v) for v in value_list]
        if set(original_value_list) != set(new_value_list):
            raise Exception(
                f"Parameter `{k}` possible values list appear to have changed since the "
                # note that printing out the whole list can overrun the log if they get long
                f"model was initialized. Original [{', '.join(original_value_list)}], current values [{', '.join(new_value_list)}]."
            )

        # TODO: implement RL
        return random.choice(value_list)

    def parameter(self, **kwargs):
        self._validate_parameter_variations(kwargs)

        k, value_list = list(kwargs.items())[0]

        if k not in self._model:
            self._seed_model(k, value_list)

        choice = self._choose_parameter(k, value_list)
        self._track_choice(k, choice)
        return choice

    def _reset_current_selections(self):
        self._current_selections = {}

    def register_outcome(self, is_success: bool):
        # TODO: update model

        self._reset_current_selections()
