import random


class MultiArmedBandit:
    def __init__(self, successes, failures, epsilon=0.05):
        self.successes = successes
        self.failures = failures
        self.epsilon = epsilon

    def _ensure_chosen_type(self, choice_str, value_list):
        return value_list[value_list.index(eval(choice_str))]

    def choose(self, value_list):
        values = [
            self.successes[arm] / (self.successes[arm] + self.failures[arm])
            if self.successes[arm] + self.failures[arm] > 0
            else 0
            for arm in self.successes.keys()
        ]
        if random.random() > self.epsilon:
            return self._ensure_chosen_type(
                list(self.successes.keys())[values.index(max(values))], value_list
            )
        else:
            return (
                self._ensure_chosen_type(
                    random.choice(list(self.successes.keys())),
                    value_list,
                ),
            )
