# Track B: Python from Scratch (Post-Workshop / Self-Guided)

Build a personal AI agent from scratch using just the OpenAI API. No frameworks, no magic - you'll understand every line.

This track is designed to be done **after the workshop** at your own pace, or during the workshop if you prefer building from scratch over using OpenClaw.

## What you'll build

A terminal-based agent that can:
- Chat naturally
- Use tools (time, calculator, web search)
- Remember facts across conversations
- Run tasks on a schedule

Each step builds on the previous one. By Step 4, you have a complete agent.

## Step 1: Basic agent with one tool (~8 min)

The simplest possible agent. One tool (get the time), one loop.

```bash
python3 03-build-your-agent/step1_basic_agent.py
```

Read the code. It's the same `while True` loop from Exercise 2, but packaged as a proper chat agent.

## Step 2: Add more tools (~5 min)

Add a calculator and web search. Notice how easy it is - you just add a tool definition and a function. The agent loop doesn't change at all.

```bash
python3 03-build-your-agent/step2_add_tools.py
```

Try: `Search the web for the weather in Waterloo, Ontario`

## Step 3: Add persistent memory (~8 min)

Add `remember` and `recall` tools. Facts get saved to `agent_memory.json` and survive restarts.

```bash
python3 03-build-your-agent/step3_add_memory.py
```

Try: Tell it your name, restart the script, ask what your name is.

## Step 4: Add proactive scheduling (~8 min)

Add a background thread that triggers the agent on a schedule. The agent runs independently and prints to the console.

```bash
python3 03-build-your-agent/step4_proactive.py
```

The agent will print a proactive message every 60 seconds while you're chatting.

## Going further

After completing this track, you could:
- Connect it to Telegram using [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- Add more tools (file operations, calendar, email)
- Build an MCP server (see Exercise 4 in Building Blocks)
- Add a system prompt loaded from a SOUL.md file
