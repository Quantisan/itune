import logging
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

    def __str__(self) -> str:
        return f"MultiArmedBandit(epsilon={self.epsilon}, trial_counts={self.trial_counts})"

    def __repr__(self) -> str:
        return self.__str__()

    def _arms(self, parameter):
        return list(self.trial_counts[parameter]["successes"].keys())

    def _successes(self, parameter, arm):
        return self.trial_counts[parameter]["successes"][arm]

    def _failures(self, parameter, arm):
        return self.trial_counts[parameter]["failures"][arm]

    def _seed_trial_counts(self, parameter, arms):
        self.trial_counts[parameter] = {
            "successes": {arm: 0 for arm in arms},
            "failures": {arm: 0 for arm in arms},
        }

    def _validate_parameter(self, parameter, value_list):
        if parameter not in self.trial_counts and self.trial_counts:
            raise NotImplementedError(
                f"Parameter `{parameter}` is not in the model. Only one parameter can be in play at a time."
            )

        if parameter in self.trial_counts:
            existing_arms = set(map(str, self._arms(parameter)))
            new_arms = set(map(str, value_list))
            if existing_arms != new_arms:
                raise NotImplementedError(
                    f"Parameter `{parameter}` possible values appear to have changed since the "
                    f"model was initialized. Original [{', '.join(existing_arms)}], current values [{', '.join(new_arms)}]."
                )

    def _current_winners(self, parameter):
        expected_rewards = [
            calculate_expected_reward(
                self._successes(parameter, arm), self._failures(parameter, arm)
            )
            for arm in self._arms(parameter)
        ]
        max_reward = max(expected_rewards)
        max_indices = [
            i for i, reward in enumerate(expected_rewards) if reward == max_reward
        ]
        return [list(self._arms(parameter))[i] for i in max_indices], max_reward

    def choose_winning(self, parameter):
        current_winners, _ = self._current_winners(parameter)
        chosen = current_winners[0]
        if len(current_winners) > 1:
            logging.info(
                "MultiArmedBandit found more than one winner for parameter "
                f"{parameter} even though only_choose_winning_params is `True`."
                f"Arbitrarily choosing the first winner that came up, {chosen}."
            )
        return chosen

    def _choose_with_epsilon_greedy(self, parameter):
        if random.random() > self.epsilon:
            current_winners, winning_reward = self._current_winners(parameter)
            chosen = random.choice(current_winners)
            logging.debug(
                f"MultiArmedBandit chose {chosen} for parameter {parameter}, because it has a max reward of {winning_reward}"
            )
        else:
            chosen = random.choice(list(self._arms(parameter)))
            logging.debug(
                f"MultiArmedBandit chose {chosen} for parameter {parameter} randomly"
            )
        return chosen

    def choose(self, parameter, value_list, only_choose_winning=False):
        if only_choose_winning:
            return self.choose_winning(parameter)

        self._validate_parameter(parameter, value_list)

        if parameter not in self.trial_counts and not self.trial_counts:
            self._seed_trial_counts(parameter, value_list)

        return self._choose_with_epsilon_greedy(parameter)

    def register_outcome(self, current_selections, is_success):
        for (
            this_parameter,
            this_arm,
        ) in current_selections.items():
            if is_success:
                self.trial_counts[this_parameter]["successes"][this_arm] += 1
            else:
                self.trial_counts[this_parameter]["failures"][this_arm] += 1
