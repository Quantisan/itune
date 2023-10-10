import random


def calculate_expected_reward(successes, failures):
    if (successes + failures) > 0:
        return successes / (successes + failures)
    else:
        return 0


class MultiArmedBandit:
    def __init__(self, epsilon=0.05):
        self.epsilon = epsilon
        # trial_counts should have a schema, or it could be a class
        self.trial_counts = {}

    def _arms(self, parameter):
        return list(self.trial_counts[parameter]["successes"].keys())

    def _successes(self, parameter, arm):
        return self.trial_counts[parameter]["successes"][arm]

    def _failures(self, parameter, arm):
        return self.trial_counts[parameter]["failures"][arm]

    def _ensure_chosen_type(self, choice_str, value_list):
        return value_list[value_list.index(eval(choice_str))]

    def _seed_trial_counts(self, parameter, arms):
        self.trial_counts[parameter] = {
            "successes": {str(arm): 0 for arm in arms},
            "failures": {str(arm): 0 for arm in arms},
        }

    def choose(self, parameter, value_list):
        if parameter not in self.trial_counts:
            self._seed_trial_counts(parameter, value_list)

        expected_rewards = [
            calculate_expected_reward(
                self._successes(parameter, arm), self._failures(parameter, arm)
            )
            for arm in self._arms(parameter)
        ]
        # epsilon-greedy
        if random.random() > self.epsilon:
            return self._ensure_chosen_type(
                list(self._arms(parameter))[
                    expected_rewards.index(max(expected_rewards))
                ],
                value_list,
            )
        else:
            return (
                self._ensure_chosen_type(
                    random.choice(list(self._arms(parameter))),
                    value_list,
                ),
            )
