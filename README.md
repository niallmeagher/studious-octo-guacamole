# studious-octo-guacamole
Conversational AI that answers questions about movies based on MovieLens 100K dataset.

# How to use:
- Install requirements using requirements.txt
- Set question you would like to ask in main.py input field
- `python3 main.py`

# Implementation details
The chatbot is built on a Natural Language Query Parser, the results of which are passed to an LLM. When the user provides a question, the query parser infers the user's intent (searching for a recommendation, information, or filtering the database), as well as relevant features the user is looking for (year, genre, title). Once these have been identified, an SQL query is constructed filtering on these attributes.

The results of the query are passed to an LLM agent (currently GPT2) along with the user intent, the original user prompt, as well as a system prompt outlining the agent's role and providing an example of a desirable answer. 

# Further work
1. Current implementation uses a GPT2 model. Given that the system prompt is designed for more current models (Claude Haiku/GPT 4o), the chatbot is not able to provide cohesive answers.
2. As a proof of concept, the query parser follows a simple rule-based system. This could be expanded on by using another LLM to structure queries from the user prompt, and work as a RAG model instead.
3. I would like to implement the ability to ask follow up questions to the agent.
