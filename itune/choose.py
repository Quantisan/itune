import random


class MultiArmedBandit:
    def __init__(self):
        self.epsilon = 0.05

    def choose(self, current_states):
        successes = current_states["successes"]
        failures = current_states["failures"]
        values = [
            successes[arm] / (successes[arm] + failures[arm])
            if successes[arm] + failures[arm] > 0
            else 0
            for arm in successes.keys()
        ]
        if random.random() > self.epsilon:
            return list(successes.keys())[values.index(max(values))]
        else:
            return random.choice(list(successes.keys()))
