import pytest

import rlhf_wizard as rlhf


@pytest.fixture(autouse=True)
def with_model(request):
    request.cls.model = rlhf.Model()


class TestApp:
    def test_instantiate_model(self):
        assert isinstance(rlhf.Model(), rlhf.Model)


class TestParameter:
    def test_model_parameter(self):
        result = self.model.parameter(x=[1, 2, 3])
        assert result in [1, 2, 3]

        # check that the current selection is tracked
        assert self.model._current_selections == {"x": result}
        # check that model is intialized with all the possible values
        assert self.model._model == {
            "x": {
                "successes": {"1": 0, "2": 0, "3": 0},
                "failures": {"1": 0, "2": 0, "3": 0},
            }
        }

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

    def test_model_parameter_values_list_changed(self):
        self.model.parameter(x=[1, 2, 3])
        self.model._reset_current_selections()
        with pytest.raises(Exception):
            self.model.parameter(x=[1, 2])
