Wizard is a Python package for optimizing procedures using reinforcement learning with human feedback (RLHF).

## Example: Retrieval Augmented Generation (RAG) application

Let's dive into an example from LlamaIndex's Getting Started guide. In this scenario, we have a procedure with several parameters to fine-tune. For simplicity, we'll focus on just two of them: `chunk_size` and `llm`. We can harness the power of RLHF to discover the most effective combination of these parameters.

```Python
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import ServiceContext
from llama_index.llms import PaLM, OpenAI

documents = SimpleDirectoryReader('data').load_data()

service_context = ServiceContext.from_defaults(

  #######################################################################
  # pass in acceptable list of values to these parameters and use RLHF to
  # optimize over combinations of them
  chunk_size=@rlhf.parameter.list(250, 500, 1000, 2000),
  llm=@rlhf.parameter.list(lambda:PaLM(), lambda:OpenAI()),
  #######################################################################

)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)

user_input = input("Good response?")
if user_input == "y":

  ######################
  # RLHF reward function
  @rlhf.reward(1)
  ######################

```

This example demonstrates how Wizard can be used to optimize procedure parameters by using user feedback to improve outcomes.

