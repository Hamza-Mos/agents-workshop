"""
Exercise 3: Memory Agent

This agent remembers things between conversations.

Try this:
  1. Run the script
  2. Tell it: "My name is Alice and I study computer science"
  3. Ask: "What's my name?"  (it knows!)
  4. Press Ctrl+C to exit
  5. Run the script AGAIN
  6. Ask: "What do you know about me?"

It remembers because it saves facts to memory.json.
That file IS the long-term memory. Open it and look.
"""

import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
client = OpenAI()

MEMORY_FILE = Path(__file__).parent / "memory.json"


def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {}


def save_memory(data):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))


memory = load_memory()

# -- Tools ------------------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": "Save a fact to long-term memory. Use this whenever the user shares something worth remembering (name, preferences, facts about themselves).",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "Short label, e.g. 'name', 'major', 'favorite_color'",
                    },
                    "value": {
                        "type": "string",
                        "description": "The fact to store",
                    },
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall",
            "description": "Retrieve all stored memories. Use this when the user asks about something you might have saved before.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def run_tool(name, args):
    if name == "remember":
        memory[args["key"]] = args["value"]
        save_memory(memory)
        return f"Saved: {args['key']} = {args['value']}"
    if name == "recall":
        return json.dumps(memory, indent=2) if memory else "No memories stored yet."
    if name == "get_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Unknown tool: {name}"


# -- Agent loop (same pattern as exercise 2) --------------------------------


def agent(user_input, messages):
    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="gpt-5-mini", messages=messages, tools=tools
        )
        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content

        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            print(f"  [tool call]  {tc.function.name}({json.dumps(args)})")
            result = run_tool(tc.function.name, args)
            print(f"  [result]     {result}")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})


# -- Main -------------------------------------------------------------------

if __name__ == "__main__":
    print("Memory Agent")
    print("This agent remembers things between conversations.")
    if memory:
        print(f"Loaded {len(memory)} memories from {MEMORY_FILE.name}")
    print("Press Ctrl+C to exit.\n")

    existing = json.dumps(memory, indent=2) if memory else "None yet."
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant with persistent memory. "
                "When the user shares personal info (name, preferences, facts), "
                "use the 'remember' tool to save it. When they ask about something "
                "you might have stored, use 'recall' first.\n\n"
                f"Current memories:\n{existing}"
            ),
        }
    ]

    while True:
        try:
            q = input("You: ").strip()
            if q:
                answer = agent(q, messages)
                print(f"\nAgent: {answer}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break
