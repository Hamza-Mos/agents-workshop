# 02 - Building Blocks

You talked to an agent. Now build each piece yourself.

## How tool calling works

The model doesn't run your code. It can't. So tool calling works as a conversation:

```
You:    "What's the weather in Tokyo?"     --> send to model (with tool definitions)
Model:  "I want to call get_weather()"     --> returns a tool_call, NOT text
You:    *actually run get_weather()*        --> your code executes the function
You:    "The result was 14°C, rain"         --> send result back to model
Model:  "It's 14°C in Tokyo with rain!"    --> now it responds with text
```

The model outputs structured JSON saying "call this function with these arguments." Your code does the real work. This pattern is the same across OpenAI, Anthropic, and Google's APIs.

## Exercise 1: Tool calling basics

```bash
uv run 02-building-blocks/1_tool_calling_basics.py
```

Fill in the two TODOs. Read the step-by-step output — it shows exactly how a single tool call works.

## The agent loop

What if the model needs multiple tools? That's the agent loop:

```python
while True:
    response = call_model(messages)

    if response has no tool calls:
        return response.text       # done

    for each tool_call in response:
        result = execute(tool_call)
        messages.append(result)    # feed it back and loop
```

That's the entire secret. Claude Code, Cursor, Devin — every AI agent runs this exact loop. The model thinks, acts, observes, and decides when it's done. You just gave an LLM hands.

## Exercise 2: The agent loop

```bash
uv run 02-building-blocks/2_agent_loop.py
```

Fill in the TODO to build the `while True` loop. When it works, try:
- `What time is it in Tokyo and what's the weather there?` (chains both tools)

## Memory

Without memory, every conversation starts from zero:

- **Short-term memory** = the messages array you send each API call
- **Long-term memory** = facts saved to a JSON file that survive restarts

You don't need a vector database. For a personal agent, a simple file works.

## Exercise 3: Memory

```bash
uv run 02-building-blocks/3_memory_agent.py
```

Fill in the TODOs for `load_memory()`, `save_memory()`, and the remember/recall tools. Then:
1. Tell it: `My name is Alice and I study computer science`
2. Press Ctrl+C to exit
3. Run it again
4. Ask: `What do you know about me?` — it still knows!

Check `memory.json` — that's the entire memory system.

---

Next: [03 - Build Your Agent](../03-build-your-agent/)
