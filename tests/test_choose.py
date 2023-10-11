from itune import MultiArmedBandit


def test_ensure_chosen_type():
    mab = MultiArmedBandit()
    choice = mab._ensure_chosen_type("1", [1, 2])
    assert choice == 1


def test_mab_choose():
    mab = MultiArmedBandit()
    choice = mab.choose("x", [1, 2])
    assert choice in [1, 2]
