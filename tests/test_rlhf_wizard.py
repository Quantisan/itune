import rlhf_wizard as rlhf


def test_instantiate_model():
    rlhf_model = rlhf.Model()
    assert isinstance(rlhf_model, rlhf.Model)


def test_experiment():
    model = rlhf.Model()

    @model.experiment(variations=[3])
    def three(model) -> int:
        return model.get_variation()

    assert three(model) == 3
