import random


def calculate_expected_reward(successes, failures):
    if (successes + failures) > 0:
        return successes / (successes + failures)
    else:
        return 0


class MultiArmedBandit:
    def __init__(self, epsilon=0.10):
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

    def _validate_parameter(self, parameter, value_list):
        if parameter not in self.trial_counts and self.trial_counts:
            raise NotImplementedError(
                f"Parameter `{parameter}` is not in the model. Only one parameter can be in play at a time."
            )

        if parameter in self.trial_counts:
            existing_arms = set(self._arms(parameter))
            new_arms = set(map(str, value_list))
            if existing_arms != new_arms:
                raise NotImplementedError(
                    f"Parameter `{parameter}` possible values appear to have changed since the "
                    f"model was initialized. Original [{', '.join(existing_arms)}], current values [{', '.join(new_arms)}]."
                )

    def choose(self, parameter, value_list):
        self._validate_parameter(parameter, value_list)

        if parameter not in self.trial_counts and not self.trial_counts:
            self._seed_trial_counts(parameter, value_list)

        expected_rewards = [
            calculate_expected_reward(
                self._successes(parameter, arm), self._failures(parameter, arm)
            )
            for arm in self._arms(parameter)
        ]
        # epsilon-greedy
        if random.random() > self.epsilon:
            max_reward = max(expected_rewards)
            max_indices = [
                i for i, reward in enumerate(expected_rewards) if reward == max_reward
            ]
            chosen_index = random.choice(max_indices)
            return self._ensure_chosen_type(
                list(self._arms(parameter))[chosen_index],
                value_list,
            )
        else:
            return self._ensure_chosen_type(
                random.choice(list(self._arms(parameter))),
                value_list,
            )

    def register_outcome(self, current_selections, is_success):
        for (
            this_parameter,
            this_arm,
        ) in current_selections.items():
            if is_success:
                self.trial_counts[this_parameter]["successes"][str(this_arm)] += 1
            else:
                self.trial_counts[this_parameter]["failures"][str(this_arm)] += 1
