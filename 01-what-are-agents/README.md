# 01 - What Are Agents?

An AI agent is an LLM that can **do things** — call functions, search the web, check the weather, remember facts. The gap between a chatbot and an agent is one loop: **Think, Act, Observe, Repeat.**

## The ReAct pattern

This is how every modern agent thinks (from [Yao et al., ICLR 2023](https://arxiv.org/abs/2210.03629)):

```
Think   ->  "The user wants the weather in Tokyo. I should use the weather tool."
  |
Act     ->  call get_weather(city="Tokyo")
  |
Observe ->  "Tokyo: 14°C, Light rain, Humidity: 86%"
  |
Think   ->  "I have the answer. Let me respond."
  |
Respond ->  "It's 14°C in Tokyo with light rain showers."
```

The model decides when to use tools and when to stop. Your code just runs the loop.

## The four layers

Every agent has the same anatomy:

| Layer | What it does |
|-------|-------------|
| **Planning** | The reasoning loop — when to act, when to stop |
| **Memory** | Conversation history + facts saved to disk |
| **Tools** | APIs, web search, weather, file access |
| **Brain** | The LLM (GPT, Claude, etc.) |

One way to think about it: **an agent is an LLM with a while-loop and access to the real world.**

## Exercise: talk to a real agent

```bash
uv run 01-what-are-agents/talk_to_agent.py
```

This agent has three tools: **current time**, **weather**, and **web search**. Try these:

- `What time is it in Tokyo?`
- `What's the weather in Waterloo?`
- `Search the web for the latest AI news`
- `What time is it in London and what's the weather there?` (chains two tools!)

Watch the `[tool call]` and `[result]` lines — that's the ReAct pattern happening in real time.

**Early finisher?** Open `talk_to_agent.py` and find the `while True` loop. That's the entire agent.

---

Next: [02 - Building Blocks](../02-building-blocks/)
