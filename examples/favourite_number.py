from itune import MultiArmedBandit, Tune

MAX_VALUE = 5
ITERATIONS = 5
itune = Tune(strategy=MultiArmedBandit())

# pick up from where we left off, if possible. Otherwise, this continues gracefully.
itune.load()

for _ in range(ITERATIONS):
    print(
        f"Your favourite number from 1 to {MAX_VALUE} (inclusive) is {itune.choose(fav_num=list(range(1,5+1)))}"
    )

    user_input = input("Yes (y) / No (n)?")
    ######################
    # reward function
    itune.register_outcome(user_input == "y")
    ######################

# save the learned states for later use
itune.save()
