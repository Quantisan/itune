from itune import MultiArmedBandit


def test_mab_choose():
    mab = MultiArmedBandit()
    choice = mab.choose({"successes": {"1": 0, "2": 0}, "failures": {"1": 0, "2": 1}})
    assert choice in ["1", "2"]


def test_ensure_chosen_type():
    mab = MultiArmedBandit()
    choice = mab.ensure_chosen_type("1", [1, 2])
    assert choice == 1
