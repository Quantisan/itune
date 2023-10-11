from itune import MultiArmedBandit, Tune

MAX_VALUE = 5
itune = Tune(strategy=MultiArmedBandit())

for _ in range(10):
    print(
        f"Everyone's favourite number from 1 to {MAX_VALUE} (inclusive) is {itune.choose(fav_num=list(range(1,5+1)))}"
    )

    user_input = input("Agree (y) / Disagree (n)?")
    ######################
    # reward function
    itune.register_outcome(user_input == "y")
    ######################
