import pytest

from itune import MultiArmedBandit


@pytest.fixture(autouse=True)
def with_model(request):
    request.cls.mab = MultiArmedBandit()


class TestMultiArmedBandit:
    def test_ensure_chosen_type(self):
        choice = self.mab._ensure_chosen_type("1", [1, 2])
        assert choice == 1

    def test_mab_choose(self):
        choice = self.mab.choose("x", [1, 2])
        assert choice in [1, 2]

    def test_model_parameter_values_list_changed(self):
        self.mab.choose("x", [1, 2, 3])
        with pytest.raises(NotImplementedError):
            self.mab.choose("x", [1, 2])

    def test_model_parameter_unexpected_parameter_given(self):
        self.mab.choose("x", [1, 2, 3])
        with pytest.raises(NotImplementedError):
            self.mab.choose("y", [4, 5, 6])
