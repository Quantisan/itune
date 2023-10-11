from typing import Any

from .choose import MultiArmedBandit


class Model:
    def __init__(self):
        self._current_selections: dict[str, Any] = {}

    def _validate_parameter_argument(self, kwargs):
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

    def _choose_parameter(self, k, value_list):
        # note that keys are saved as strings

        mab = MultiArmedBandit()
        return mab.choose(k, value_list)

    def parameter(self, **kwargs):
        self._validate_parameter_argument(kwargs)
        parameter, value_list = list(kwargs.items())[0]

        choice = self._choose_parameter(parameter, value_list)
        self._track_choice(parameter, choice)
        return choice

    def _reset_current_selections(self):
        self._current_selections = {}

    def register_outcome(self, is_success: bool):
        for (
            self._current_selections_key,
            self._current_selections_value,
        ) in self._current_selections.items():
            if is_success:
                self._model[self._current_selections_key]["successes"][
                    str(self._current_selections_value)
                ] += 1
            else:
                self._model[self._current_selections_key]["failures"][
                    str(self._current_selections_value)
                ] += 1

        self._reset_current_selections()
