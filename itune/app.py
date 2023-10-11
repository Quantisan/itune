from .choose import MultiArmedBandit


class Model:
    def __init__(self):
        self._current_choices = {}
        self.strategy = MultiArmedBandit()

    def _validate_parameter_argument(self, kwargs):
        if (
            len(kwargs) != 1
            or not isinstance(kwargs.get(list(kwargs.keys())[0]), list)
            or not kwargs.get(list(kwargs.keys())[0])
        ):
            raise ValueError("Argument must have exactly one non-empty list value")

    def _track_choice(self, parameter, choice):
        if parameter not in self._current_choices:
            self._current_choices[str(parameter)] = choice
        else:
            raise Exception(f"Parameter `{parameter}` has already been selected")

    def parameter(self, **kwargs):
        self._validate_parameter_argument(kwargs)
        parameter, value_list = list(kwargs.items())[0]

        choice = self.strategy.choose(parameter, value_list)
        self._track_choice(parameter, choice)
        return choice

    def _reset_current_choices(self):
        self._current_choices = {}

    def register_outcome(self, is_success: bool):
        self.strategy.register_outcome(self._current_choices, is_success)
        self._reset_current_choices()
