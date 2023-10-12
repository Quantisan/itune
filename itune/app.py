import pickle

FILENAME = "itune_strategy.pkl"


class Tune:
    def __init__(self, strategy):
        self._current_choices = {}
        self.strategy = strategy

    def _validate_choose_argument(self, kwargs):
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

    def choose(self, **kwargs):
        self._validate_choose_argument(kwargs)
        parameter, value_list = list(kwargs.items())[0]

        choice = self.strategy.choose(parameter, value_list)
        self._track_choice(parameter, choice)
        return choice

    def _reset_current_choices(self):
        self._current_choices = {}

    def register_outcome(self, is_success: bool):
        self.strategy.register_outcome(self._current_choices, is_success)
        self._reset_current_choices()

    def save(self):
        with open(FILENAME, "wb") as f:
            pickle.dump(self.strategy, f)

    def load(self):
        try:
            with open(FILENAME, "rb") as f:
                self.strategy = pickle.load(f)
        except FileNotFoundError:
            print("No saved model found. Continuing gracefully.")
