# 02 - Building Blocks

In Part 1 you talked to an agent. Now you'll understand how it works by building each piece yourself.

There are three exercises (plus a stretch goal):

1. **Tool calling basics** - See the exact mechanics of a single tool call
2. **The agent loop** - Build a complete agent in ~40 lines of Python
3. **Memory** - Give your agent persistent memory that survives restarts
4. **MCP server** (stretch) - Build a tool server using the new open standard

## How tool calling works

The model doesn't run your code. It can't. It's a language model - it produces text. So tool calling works as a conversation:

```
You:    "What time is it?"                --> send to model (with tool definitions)
Model:  "I want to call get_time()"       --> returns a tool_call, NOT text
You:    *actually run get_time()*          --> your code executes the function
You:    "The result was 2:30 PM"           --> send result back to model
Model:  "It's 2:30 PM!"                   --> now it responds with text
```

The model outputs a structured JSON object saying "call this function with these arguments." Your code does the real work. This back-and-forth is the fundamental primitive behind every AI agent, and it works the same way across OpenAI, Anthropic, and Google's APIs.

A tool definition is just a JSON schema - a function signature the model can read:

```json
{
  "name": "get_current_time",
  "description": "Get the current date and time",
  "parameters": {
    "type": "object",
    "properties": {
      "timezone": {
        "type": "string",
        "description": "e.g. 'America/New_York'"
      }
    }
  }
}
```

Nothing magical. The model reads the name and description, decides if the tool is relevant, and outputs the right arguments.

## Exercise 1: Tool calling basics (5 min)

```bash
python3 02-building-blocks/1_tool_calling_basics.py
```

This script walks you through a single tool call, step by step. Read the output carefully - it shows exactly what happens at each stage.

## The agent loop

Exercise 1 showed one tool call. But what if the model needs to call multiple tools? Or call a tool, read the result, then decide to call another?

That's the agent loop:

```python
while True:
    response = call_model(messages)

    if response has no tool calls:
        return response.text       # done - model has a final answer

    for each tool_call in response:
        result = execute(tool_call)
        messages.append(result)    # feed it back and loop
```

That's it. The model decides what to do. Your code just executes tools and feeds results back. The model decides when to stop. This `while True` loop IS the ReAct pattern from Part 1.

## Exercise 2: The agent loop (5 min)

```bash
python3 02-building-blocks/2_agent_loop.py
```

This is a complete working agent in about 40 lines. Try multi-step queries:
- `What time is it, and what's 2 to the power of 10?` (chains two tools)
- `What's the square root of the number of seconds in a day?` (needs to calculate 86400, then sqrt it)

## Memory

Without memory, every conversation starts from zero. There are two kinds:

**Short-term memory** is the conversation history you send with each API call. The model sees all previous messages and can refer back to them. It's limited by the context window (the model's maximum input size).

**Long-term memory** is facts saved to a file or database that survive across conversations and restarts. For a personal agent, this can be as simple as a JSON file.

```
Short-term:  "What did I just say?"     -> stored in the messages array
Long-term:   "What's my favorite color?" -> stored in memory.json
```

You don't need a vector database. You don't need RAG. For a personal agent, a simple file works.

## Exercise 3: Memory (5 min)

```bash
python3 02-building-blocks/3_memory_agent.py
```

Try this:
1. Tell it: `My name is Alice and I study computer science`
2. Ask: `What's my name?` (it knows - short-term memory)
3. Press Ctrl+C to exit
4. Run the script again
5. Ask: `What do you know about me?` (it still knows - long-term memory!)

Check `02-building-blocks/memory.json` after using it. That's the memory file.

## Stretch: MCP server

MCP (Model Context Protocol) is a standard created by Anthropic for connecting AI agents to tools. Think of it as USB for AI: build one MCP server, and any MCP client (Claude Desktop, Cursor, VS Code, etc.) can use it. OpenAI, Google, and Microsoft have all adopted it.

```bash
pip install mcp
python3 02-building-blocks/4_mcp_server.py
```

This creates a minimal MCP server with two tools. You can connect it to Claude Desktop or any MCP-compatible client.

---

Next: [03 - Build Your Agent](../03-build-your-agent/) - build a complete personal AI agent.
