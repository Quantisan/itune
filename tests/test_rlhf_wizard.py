import pytest

import rlhf_wizard as rlhf


def setup_function():
    rlhf.model = rlhf.Model()


def test_instantiate_model():
    assert isinstance(rlhf.model, rlhf.Model)


## parameter()


def test_model_parameter():
    result = rlhf.model.parameter(x=[1, 2, 3])
    assert result in [1, 2, 3]

    # check that the current selection is tracked
    assert rlhf.model._current_selections == {"x": result}
    # check that model is intialized with all the possible values
    assert rlhf.model._model == {
        "x": {
            "successes": {"1": 0, "2": 0, "3": 0},
            "failures": {"1": 0, "2": 0, "3": 0},
        }
    }

    # check that we cannot call the same parameter again
    with pytest.raises(Exception):
        rlhf.model.parameter(x=[1, 2, 3])


def test_model_parameter_multiple_variations():
    with pytest.raises(ValueError):
        rlhf.model.parameter(variation=[1, 2, 3], variation2=[4, 5, 6])


def test_model_parameter_empty_variation():
    with pytest.raises(ValueError):
        rlhf.model.parameter(variation=[])


def test_model_parameter_non_list_variation():
    with pytest.raises(ValueError):
        rlhf.model.parameter(variation=1)


def test_model_parameter_values_list_changed():
    rlhf.model.parameter(variation=[1, 2, 3])
    with pytest.raises(Exception):
        rlhf.model.parameter(variation=[1, 2])
