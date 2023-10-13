import logging as log
import pickle

DEFAULT_FILEPATH = "./.itune_strategy.pkl"


class Tune:
    """
    The tune object implements a reinforcement learning with human feedback strategy for
    parameter tuning. It is initialized with a reinforcement learning strategy and
    provides methods for choosing parameters and registering the success or failure of
    the chosen parameters.

    Args:
        strategy (object): An object that defines the reinforcement learning strategy to
                           be used.
        only_choose_winning_params (bool, optional): Whether to only choose the current
                                                     winning parameters. This is useful
                                                     in production to ensure determinism
                                                     of your parameters. Defaults to
                                                     `False`.
    """

    def __init__(self, strategy, only_choose_winning_params=False):
        self._current_choices = {}
        self.only_choose_winning_params = only_choose_winning_params
        self.strategy = strategy
        self._load()

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
        """
        Choose a value for a given parameter based on the current strategy.

        :param kwargs: A dictionary with a single key-value pair representing the parameter and its possible values.
        :return: The chosen value for the parameter.
        """
        self._validate_choose_argument(kwargs)
        parameter, value_list = list(kwargs.items())[0]

        choice = self.strategy.choose(
            parameter, value_list, self.only_choose_winning_params
        )
        self._track_choice(parameter, choice)
        if self.only_choose_winning_params:
            log.info(
                f"Chose current winner {choice} for parameter {parameter} (only_choose_winning_params is True)"
            )
        else:
            log.info(f"Chose {choice} for parameter {parameter}")

        return choice

    def _reset_current_choices(self):
        self._current_choices = {}

    def register_outcome(self, is_success: bool):
        """
        Registers the outcome of the current played choices made by the current strategy.

        Args:
            is_success (bool): A boolean value indicating whether the played choices were
                               successful or not.
        """
        self.strategy.register_outcome(self._current_choices, is_success)
        self._reset_current_choices()
        self._save()

    def _save(self):
        if not self.only_choose_winning_params:
            with open(DEFAULT_FILEPATH, "wb") as f:
                pickle.dump(self.strategy, f)
            log.info(f"Saved itune model with strategy {self.strategy}")
        else:
            log.info(
                "Not saving itune model because only_choose_winning_params is True"
            )

    def _load(self):
        # TODO: check that loaded model is same as instance initialized model
        try:
            with open(DEFAULT_FILEPATH, "rb") as f:
                self.strategy = pickle.load(f)
            log.info(f"Loaded saved itune model with strategy {self.strategy}")

        except FileNotFoundError:
            log.info("No saved itune model found. Continuing gracefully.")
