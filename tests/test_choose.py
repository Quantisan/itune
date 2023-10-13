import logging

import pytest

from itune import MultiArmedBandit


@pytest.fixture(autouse=True)
def with_model(request):
    request.cls.mab = MultiArmedBandit()


class TestMultiArmedBandit:
    def test_instantiate_model(self):
        assert isinstance(MultiArmedBandit(), MultiArmedBandit)

    def test_seed_trial_counts(self):
        assert self.mab.trial_counts == {}
        self.mab.choose("x", [1, 2, 3])
        # check that model is intialized with all the possible values
        assert self.mab.trial_counts == {
            "x": {
                "successes": {"1": 0, "2": 0, "3": 0},
                "failures": {"1": 0, "2": 0, "3": 0},
            }
        }

    def test_ensure_chosen_type(self):
        choice = self.mab._ensure_chosen_type("1", [1, 2])
        assert choice == 1

    def test_mab_choose(self, caplog):
        with caplog.at_level(logging.DEBUG):
            choice = self.mab.choose("x", [1, 2])
        # assert that it works
        assert choice in [1, 2]

        # assert that it logged
        for record in caplog.records:
            assert record.levelname == "DEBUG"
        assert "chose" in caplog.text

    def test_model_parameter_values_list_changed(self):
        self.mab.choose("x", [1, 2, 3])
        with pytest.raises(NotImplementedError):
            self.mab.choose("x", [1, 2])

    def test_model_parameter_unexpected_parameter_given(self):
        self.mab.choose("x", [1, 2, 3])
        with pytest.raises(NotImplementedError):
            self.mab.choose("y", [4, 5, 6])

    def test_choose_winning(self, caplog):
        arms = list(range(1, 100))
        self.mab.choose("x", arms)
        fixed_choice = 77
        self.mab.register_outcome({"x": fixed_choice}, True)
        with caplog.at_level(logging.INFO):
            assert self.mab.choose_winning("x") == str(fixed_choice)
        assert caplog.text == ""

    def test_choose_winning_multi_winners(self, caplog):
        arms = list(range(1, 100))
        self.mab.choose("x", arms)
        fixed_choice = 77
        self.mab.register_outcome({"x": fixed_choice}, True)
        self.mab.register_outcome({"x": fixed_choice + 1}, True)
        self.mab.register_outcome({"x": fixed_choice + 2}, True)
        with caplog.at_level(logging.INFO):
            assert self.mab.choose_winning("x") == str(fixed_choice)
        assert "found more than one winner" in caplog.text

    def test_register_outcome_success(self):
        assert self.mab.choose("x", [1, 2])
        assert self.mab.register_outcome({"x": 1}, True) is None
        assert self.mab.trial_counts == {
            "x": {"successes": {"1": 1, "2": 0}, "failures": {"1": 0, "2": 0}},
        }

    def test_register_outcome_failure(self):
        assert self.mab.choose("x", [1, 2])
        assert self.mab.register_outcome({"x": 1}, False) is None
        assert self.mab.trial_counts == {
            "x": {"successes": {"1": 0, "2": 0}, "failures": {"1": 1, "2": 0}},
        }
