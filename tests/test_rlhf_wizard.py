import pytest
import rlhf_wizard as rlhf


@pytest.fixture(autouse=True)
def new_model():
    rlhf.model = rlhf.Model()


def test_instantiate_model():
    assert isinstance(rlhf.model, rlhf.Model)


def test_experiment():
    @rlhf.model.experiment(variations=[3])
    def three(model) -> int:
        return model.get_variation()

    assert three(rlhf.model) == 3


def test_experiment_without_output_type_hint():
    @rlhf.model.experiment(variations=[3])
    def three(model):
        return model.get_variation()

    assert three(rlhf.model) == 3


def test_experiment_variation_validation_fail():
    with pytest.raises(TypeError) as e:

        @rlhf.model.experiment(variations=[3])
        def three(model) -> str:
            return model.get_variation()

        three(rlhf.model)

    assert (
        str(e.value)
        == "all variations must have the same type as the function return type"
    )
