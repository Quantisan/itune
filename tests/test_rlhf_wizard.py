import pytest

import rlhf_wizard as rlhf


def test_instantiate_model():
    rlhf_model = rlhf.Model()
    assert isinstance(rlhf_model, rlhf.Model)

