import pytest

import itune as itune


@pytest.fixture(autouse=True)
def with_model(request):
    request.cls.model = itune.Tune(strategy=itune.MultiArmedBandit())


class TestApp:
    def test_instantiate_model(self):
        assert isinstance(itune.Tune(itune.MultiArmedBandit), itune.Tune)


class TestChoose:
    def test_choose(self):
        result = self.model.choose(x=[1, 2, 3])
        assert result in [1, 2, 3]

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
