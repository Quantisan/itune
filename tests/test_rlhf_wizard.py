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


def test_experiment_without_output_type_hint():
    model = rlhf.Model()

    @model.experiment(variations=[3])
    def three(model):
        return model.get_variation()

    assert three(model) == 3


def test_experiment_variation_validation_fail():
    model = rlhf.Model()

    try:

        @model.experiment(variations=[3])
        def three(model) -> str:
            return model.get_variation()

        three(model)
    except TypeError as e:
        assert (
            str(e)
            == "all variations must have the same type as the function return type"
        )
    else:
        assert False, "TypeError not raised"
