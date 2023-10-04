import pytest

import rlhf_wizard as rlhf


@pytest.fixture(autouse=True)
def new_model():
    rlhf.model = rlhf.Model()


def test_instantiate_model():
    assert isinstance(rlhf.model, rlhf.Model)


def test_model_parameter():
    result = rlhf.model.parameter(x=[1, 2, 3])
    assert result in [1, 2, 3]


def test_model_parameter_multiple_variations():
    with pytest.raises(ValueError):
        rlhf.model.parameter(variation=[1, 2, 3], variation2=[4, 5, 6])


def test_model_parameter_empty_variation():
    with pytest.raises(ValueError):
        rlhf.model.parameter(variation=[])


def test_model_parameter_non_list_variation():
    with pytest.raises(ValueError):
        rlhf.model.parameter(variation=1)
