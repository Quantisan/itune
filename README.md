Wizard is a Python package for optimizing procedures using reinforcement learning with human feedback (RLHF).

## Example: Favourite number

Find everyone's favorite number from 1 to 100 (inclusive).

```Python
import rlhf_wizard as rlhf

rlhf_model = rlhf.Model()
print(f"Everyone's favourite number from 1 to 100 (inclusive) is {rlhf_model.parameter(fav_num=range(1,101))}")


user_input = input("Agree (y) / Disagree (n)?")
######################
# RLHF reward function
rlhf_model.register_outcome(user_input == "y")
######################
```

TODO: show output and step through some iterations

## Example: Retrieval Augmented Generation (RAG) application

Let's dive into an example from LlamaIndex's Getting Started guide. In this scenario, we have a procedure with several parameters to fine-tune. For simplicity, we'll focus on just two of them: `chunk_size` and `llm`. We can harness the power of RLHF to discover the most effective combination of these parameters.

```Python
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI, PaLM

import rlhf_wizard as rlhf

documents = SimpleDirectoryReader("data").load_data()

model = rlhf.Model()


service_context = ServiceContext.from_defaults(
    #######################################################################
    # pass in acceptable list of values to these parameters and use RLHF to
    # optimize over combinations of them
    chunk_size=model.parameter(chunk_size=[250, 500, 1000, 2000])
    llm=model.parameter(llm=[PaLM(), OpenAI()])
    #######################################################################
)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)

user_input = input("Good response?")
# RLHF reward function
model.register_outcome(user_input == "y")
```

TODO: show output and step through some iterations

This example demonstrates how Wizard can be used to optimize procedure parameters by using user feedback to improve outcomes.

