import logging

import pytest

import itune as itune


@pytest.fixture(autouse=True)
def with_model(request):
    request.cls.model = itune.Tune(strategy=itune.MultiArmedBandit())


class TestApp:
    def test_instantiate_model(self):
        assert isinstance(itune.Tune(itune.MultiArmedBandit), itune.Tune)

    def test_load_nonexistent_model(self, caplog):
        with caplog.at_level(logging.INFO):
            assert self.model.load() is None
        for record in caplog.records:
            assert record.levelname == "INFO"
        assert "No saved" in caplog.text

        assert isinstance(self.model.strategy, itune.MultiArmedBandit)

    def test_save_and_load(self):
        self.model.choose(x=[1, 2])
        self.model.register_outcome(False)
        assert sum(self.model.strategy.trial_counts["x"]["successes"].values()) == 0
        assert sum(self.model.strategy.trial_counts["x"]["failures"].values()) == 1
        assert self.model.save() is None

        fresh_model = itune.Tune(itune.MultiArmedBandit())
        assert fresh_model.load() is None
        assert isinstance(fresh_model.strategy, itune.MultiArmedBandit)
        assert sum(fresh_model.strategy.trial_counts["x"]["successes"].values()) == 0
        assert sum(fresh_model.strategy.trial_counts["x"]["failures"].values()) == 1

        # remove the saved file
        import os

        os.remove(itune.app.FILENAME)


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
