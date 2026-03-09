# 01 - What Are Agents?

When people hear "AI agent," they picture Jarvis from Iron Man. The reality is more like this: a Telegram chat where the AI checks your calendar, finds a conflict, and drafts a reschedule email. Less cinematic. Way more useful.

An AI agent is just an LLM that can **do things** - call functions, read files, search the web, remember facts. That's it. The gap between a chatbot and an agent is one idea: **tool calling**.

## The evolution

Think of it as a staircase:

```
Level 5:  Multi-agent systems         (agents coordinating with other agents)
Level 4:  Tools + memory + planning   <-- this is what we're building today
Level 3:  LLM + tool calling          (can take actions)
Level 2:  LLM chatbot                 (ChatGPT, can talk)
Level 1:  Rule-based chatbot          (if/else, no intelligence)
```

The biggest jump is from Level 2 to Level 3. That's the difference between an AI that **talks** and an AI that **does things**.

## The four layers

Every agent has the same anatomy:

```
┌──────────────────────────────┐
│  Planning  (the reasoning    │
│            loop - when to    │
│            act, when to stop)│
├──────────────────────────────┤
│  Memory    (conversation     │
│            history + facts   │
│            saved to disk)    │
├──────────────────────────────┤
│  Tools     (APIs, web search,│
│            file access, etc) │
├──────────────────────────────┤
│  Brain     (the LLM - GPT,  │
│            Claude, etc)      │
└──────────────────────────────┘
```

One way to think about it: **an agent is an LLM with a while-loop and access to the real world.**

## The ReAct pattern

This is how agents think. It comes from a research paper (Yao et al., ICLR 2023) and every modern agent uses it:

```
Think  ->  "The user wants to know what's on their calendar today.
            I should use the calendar tool."
  |
Act    ->  call get_calendar(date="2026-03-20")
  |
Observe -> [Meeting with Prof. K at 2pm, Workshop prep at 4pm]
  |
Think  ->  "I have the calendar. Let me format a response."
  |
Respond -> "You have two things today: meeting with Prof. K at 2pm
            and workshop prep at 4pm."
```

Think, Act, Observe, repeat. The model decides when to use tools and when to stop. Your code just runs the loop.

## Exercise: talk to a real agent

Run the pre-built agent:

```bash
python3 01-what-are-agents/talk_to_agent.py
```

This agent has three tools: current time, calculator, and web search. Try these:

- `What time is it in Tokyo?`
- `What's the square root of 2048?`
- `Search the web for AI agent frameworks`
- `What time is it here, and what's 15% of 847?` (watch it chain two tool calls)

Watch the output. You'll see `[tool call]` and `[result]` lines showing exactly what the agent does and why. That's the ReAct pattern happening in real time.

**For early finishers:** Open `talk_to_agent.py` and read the code. Find the `while True` loop - that's the entire agent. Find the tool definitions - that's how the model knows what tools exist.

---

Next: [02 - Building Blocks](../02-building-blocks/) - you'll build this from scratch.
