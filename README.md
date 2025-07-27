# AI Agent in Python

## Tokens 

- think of tokens as the currency of LLMs.
- are the way that LLMs measure how much text they have to process.
- Tokens are roughly 4 characters for most models
- It's important when working with LLM APIs to understand how many tokens you're using.

# Messages

LLM APIs aren't typically used in a "one-shot" manner, for example:

* Prompt: "What is the meaning of life?" <br />
* Response: "42" <br />

They work the same way ChatGPT works: in a conversation. The conversation has a history, and if we keep track of that history, then with each new prompt, the model can see the entire conversation and respond within the larger context of the conversation.

# Roles

Importantly, each message in the conversation has a "role". In the context of a chat app like ChatGPT, your conversations would look like this: