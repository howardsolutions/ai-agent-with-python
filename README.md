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

# System Prompt

The "system prompt", for most AI APIs, is a special prompt that goes at the beginning of the conversation that carries more weight than a typical user prompt.

The system prompt sets the tone for the conversation, and can be used to:

* Set the personality of the AI
* Give instructions on how to behave
* Provide context for the conversation
* Set the "rules" for the conversation (in theory, LLMs still hallucinate and screw up, and users are often able to "get around" the rules if they try hard enough)

# Function Declaration

1. We're using the LLM as a decision-making engine, but we're still the ones running the code.
2. We tell the LLM which functions are available to it
3. We give it a prompt
4. It describes which function it wants to call, and what arguments to pass to it
5. We call that function with the arguments it provided
6. We return the result to the LLM