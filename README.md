# i tune your parameters so you don't have to

itune is a Python package for optimizing parameters using reinforcement learning with human feedback (RLHF).

## Example: Favourite number

Find everyone's favorite number from 1 to 100 (inclusive).

```Python
from itune import Tune, MultiArmedBandit

itune = Tune(strategy=MultiArmedBandit())
print(f"Everyone's favourite number from 1 to 100 (inclusive) is {itune.choose(fav_num=range(1,101))}")


user_input = input("Agree (y) / Disagree (n)?")
######################
# reward function
itune.register_outcome(user_input == "y")
######################
```

TODO: show output and step through some iterations

## Example: Retrieval Augmented Generation (RAG) application

Let's dive into an example from LlamaIndex's Getting Started guide. In this scenario, we have a procedure with several parameters to fine-tune. For simplicity, we'll focus on just two of them: `chunk_size` and `llm`. We can harness the power of RLHF to discover the most effective combination of these parameters.

```Python
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI, PaLM

from itune import Tune, MultiArmedBandit

documents = SimpleDirectoryReader("data").load_data()

itune = Tune(strategy=MultiArmedBandit())


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

TODO: show output and step through some iterations

This example demonstrates how `itune` can be used to optimize procedure parameters by using user feedback to improve outcomes.

