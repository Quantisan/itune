import logging

import pytest

import itune as itune


def wipe_persisted_model():
    import os

    try:
        os.remove(itune.app.FILENAME)
    except FileNotFoundError:
        pass


@pytest.fixture(autouse=True)
def with_model(request):
    request.cls.model = itune.Tune(strategy=itune.MultiArmedBandit())

    yield

    wipe_persisted_model()


class TestApp:
    def test_instantiate_model(self):
        assert isinstance(itune.Tune(itune.MultiArmedBandit), itune.Tune)

    def test_load_nonexistent_model(self, caplog):
        with caplog.at_level(logging.INFO):
            assert self.model._load() is None
        for record in caplog.records:
            assert record.levelname == "INFO"
        assert "No saved itune model found" in caplog.text

        assert isinstance(self.model.strategy, itune.MultiArmedBandit)

    def test_save_and_load(self):
        self.model.choose(x=[1, 2])
        self.model.register_outcome(False)
        # model is implicitly saved after register_outcome
        assert sum(self.model.strategy.trial_counts["x"]["successes"].values()) == 0
        assert sum(self.model.strategy.trial_counts["x"]["failures"].values()) == 1

        fresh_model = itune.Tune(itune.MultiArmedBandit())
        # model is implicitly loaded on instantiation
        assert isinstance(fresh_model.strategy, itune.MultiArmedBandit)
        assert fresh_model.strategy.trial_counts == self.model.strategy.trial_counts


class TestChoose:
    def test_choose(self, caplog):
        with caplog.at_level(logging.INFO):
            result = self.model.choose(x=[1, 2, 3])
        # assert that it works
        assert result in [1, 2, 3]
        # assert that it logged
        for record in caplog.records:
            assert record.levelname == "INFO"
        assert "Chose" in caplog.text

        # check that the current choices is tracked
        assert self.model._current_choices == {"x": result}

        # check that we cannot call the same parameter again
        with pytest.raises(Exception):
            self.model.choose(x=[1, 2, 3])

    def test_model_choose_multiple_variations(self):
        with pytest.raises(ValueError):
            self.model.choose(x=[1, 2, 3], y=[4, 5, 6])

    def test_model_choose_empty_variation(self):
        with pytest.raises(ValueError):
            self.model.choose(x=[])

    def test_model_choose_non_list_variation(self):
        with pytest.raises(ValueError):
            self.model.choose(x=1)


class TestOutcome:
    def test_model_register_outcome(self):
        assert self.model.choose(x=[1, 2])
        assert self.model.register_outcome(False) is None
        assert self.model._current_choices == {}

        assert self.model.choose(x=[1, 2])
        assert self.model.register_outcome(True) is None
        assert self.model._current_choices == {}


class TestOnlyChooseWinningParams:
    def test_choose_winner(self, caplog):
        arms = list(range(1, 100))
        chosen = self.model.choose(x=arms)
        self.model.register_outcome(True)

        # only_choose_winning_params doesn't initialize states by design,
        # so we had to run it a cycle (above) first before we can test it
        self.model.only_choose_winning_params = True

        with caplog.at_level(logging.INFO):
            assert self.model.choose(x=arms) == chosen
        assert "only_choose_winning_params is True" in caplog.text

    def test_load_still_works(self):
        self.model.only_choose_winning_params = True
        assert self.model._load() is None
        assert isinstance(self.model.strategy, itune.MultiArmedBandit)

    def test_save_is_skipped(self, caplog):
        self.model.only_choose_winning_params = True
        with caplog.at_level(logging.INFO):
            assert self.model._save() is None
        assert "Not saving" in caplog.text
