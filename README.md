# i tune your parameters so you don't have to

itune is a Python package for optimizing parameters using reinforcement learning with human feedback (RLHF).

## Example: Favourite number guessing game

This code example demonstrates a simple guessing game using `itune`. The algorithm will randomly choose a number from 1 to 5 (inclusive) and ask the user if that is their favourite number. If the user says yes, the algorithm will learn to choose that number more often in the future. If the user says no, the algorithm will continue to explore different numbers.

```Python
from itune import MultiArmedBandit, Tune

MAX_VALUE = 5
ITERATIONS = 5
itune = Tune(strategy=MultiArmedBandit())

for _ in range(ITERATIONS):
    print(
        f"Your favourite number from 1 to {MAX_VALUE} (inclusive) is {itune.choose(fav_num=list(range(1,5+1)))}"
    )

    user_input = input("Yes (y) / No (n)?")
    ######################
    # reward function
    itune.register_outcome(user_input == "y")
    ######################

```

### Output

Suppose your favorite number is 5. The output of the code might look like this:

```
Your favourite number from 1 to 5 (inclusive) is 3
Yes (y) / No (n)?n
Your favourite number from 1 to 5 (inclusive) is 4
Yes (y) / No (n)?n
Your favourite number from 1 to 5 (inclusive) is 2
Yes (y) / No (n)?n
Your favourite number from 1 to 5 (inclusive) is 5
Yes (y) / No (n)?y
Your favourite number from 1 to 5 (inclusive) is 5
Yes (y) / No (n)?y
```

It's worth noting that `itune` retains its progress by loading and saving its state implicitly, enabling seamless continuation from previous sessions.

```
Your favourite number from 1 to 5 (inclusive) is 1
Yes (y) / No (n)?n
Your favourite number from 1 to 5 (inclusive) is 5
Yes (y) / No (n)?y
Your favourite number from 1 to 5 (inclusive) is 5
Yes (y) / No (n)?y
Your favourite number from 1 to 5 (inclusive) is 5
Yes (y) / No (n)?y
Your favourite number from 1 to 5 (inclusive) is 5
Yes (y) / No (n)?y
```

During subsequent runs, `itune` tends to favour the previously successful choice.

## Example: Retrieval Augmented Generation (RAG) application

This example requires features not yet available in `itune v0.1`. It demonstrates where the library is headed.

### Problem

Optimizing a user-facing program with multiple parameters can be tedious, especially when the parameters are correlated.

### Solution

Use the `itune` library to discover the most effective combination of parameters. `itune` is a parameter optimizer for user-facing programs.

### Example

The following code shows how to use `itune` to optimize the `chunk_size` and `llm` parameters of a RAG model:

```Python
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI, PaLM

from itune import Tune, ContextualBandit

documents = SimpleDirectoryReader("data").load_data()

itune = Tune(strategy=ContextualBandit())


service_context = ServiceContext.from_defaults(
    #######################################################################
    # pass in acceptable list of values to these parameters and use RLHF to
    # optimize over combinations of them
    chunk_size=itune.choose(chunk_size=[250, 500, 1000, 2000])
    llm=itune.choose(llm=[PaLM(), OpenAI()])
    #######################################################################
)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)

user_input = input("Good response?")
# reward function
itune.register_outcome(user_input == "y")
```

### Benefits

Using `itune` can save you time and effort when writing programs with multiple parameters. It also allows you to focus on developing your end-to-end solution while `itune` figures out the best combination of parameters.

## Installing

Install and update using `pip`:

```
$ pip install itune
```

