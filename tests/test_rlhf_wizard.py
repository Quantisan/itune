import pytest

import rlhf_wizard as rlhf


@pytest.fixture(autouse=True)
def new_model():
    rlhf.model = rlhf.Model()


def test_instantiate_model():
    assert isinstance(rlhf.model, rlhf.Model)


def test_parameter():
    assert rlhf.model.parameter(x=[3]) == 3
