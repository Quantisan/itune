import pytest

import itune as itune


@pytest.fixture(autouse=True)
def with_model(request):
    request.cls.model = itune.Model(strategy=itune.MultiArmedBandit())


class TestApp:
    def test_instantiate_model(self):
        assert isinstance(itune.Model(itune.MultiArmedBandit), itune.Model)


class TestParameter:
    def test_model_parameter(self):
        result = self.model.parameter(x=[1, 2, 3])
        assert result in [1, 2, 3]

        # check that the current choices is tracked
        assert self.model._current_choices == {"x": result}

        # check that we cannot call the same parameter again
        with pytest.raises(Exception):
            self.model.parameter(x=[1, 2, 3])

    def test_model_parameter_multiple_variations(self):
        with pytest.raises(ValueError):
            self.model.parameter(x=[1, 2, 3], y=[4, 5, 6])

    def test_model_parameter_empty_variation(self):
        with pytest.raises(ValueError):
            self.model.parameter(x=[])

    def test_model_parameter_non_list_variation(self):
        with pytest.raises(ValueError):
            self.model.parameter(x=1)


class TestOutcome:
    def test_model_register_outcome(self):
        assert self.model.parameter(x=[1, 2])
        assert self.model.register_outcome(False) is None
        assert self.model._current_choices == {}

        assert self.model.parameter(x=[1, 2])
        assert self.model.register_outcome(True) is None
        assert self.model._current_choices == {}
