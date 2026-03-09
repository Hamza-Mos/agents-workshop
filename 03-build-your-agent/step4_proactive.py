"""
Track B - Step 4: Proactive Scheduling

Same agent, now with a background thread that triggers the agent on a timer.
The agent will periodically print a message without you asking.

This is the terminal equivalent of getting an unprompted Telegram message
from your agent.

YOUR TASK: Fill in the three TODOs below to add proactive scheduling.
Check your work against solutions/step4_proactive.py
"""

import json
import math
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()

MEMORY_FILE = Path(__file__).parent / "agent_memory.json"


def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {}


def save_memory(data):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))


memory = load_memory()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": "Save a fact to persistent memory",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall",
            "description": "Retrieve all stored memories",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

SAFE_MATH = {
    "__builtins__": {},
    "sqrt": math.sqrt, "pi": math.pi, "e": math.e,
    "abs": abs, "round": round,
}


def run_tool(name, args):
    if name == "get_current_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if name == "calculate":
        try:
            return str(eval(args["expression"], SAFE_MATH))
        except Exception as e:
            return f"Error: {e}"
    if name == "remember":
        memory[args["key"]] = args["value"]
        save_memory(memory)
        return f"Saved: {args['key']} = {args['value']}"
    if name == "recall":
        return json.dumps(memory, indent=2) if memory else "No memories yet."
    return f"Unknown tool: {name}"


def run_agent(prompt, system_prompt):
    """Run the agent with a given prompt and return the response."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

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
            result = run_tool(tc.function.name, args)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})


# -- Proactive scheduler ----------------------------------------------------

PROACTIVE_INTERVAL = 60  # seconds between proactive messages

# ==========================================================
# TODO 1: Write the proactive prompt.
#
# This is what gets sent to the agent on each timer tick.
# Include a {time} placeholder for the current time.
# Tell the agent to share something brief and useful:
#   a fun fact, productivity tip, or reminder to take a break.
# Keep it to 1-2 sentences.
#
# Example:
#   "You are checking in proactively. The current time is {time}. "
#   "Share a brief, useful observation..."
# ==========================================================
PROACTIVE_PROMPT = ""  # <-- Write your proactive prompt here


def proactive_loop(system_prompt):
    """Background thread that triggers the agent periodically."""
    # ==========================================================
    # TODO 2: Implement the proactive scheduler.
    #
    # while True:
    #   1. time.sleep(PROACTIVE_INTERVAL)  -- wait for the interval
    #   2. Build the prompt:
    #        prompt = PROACTIVE_PROMPT.format(time=datetime.now().strftime("%H:%M"))
    #   3. Call the agent:
    #        response = run_agent(prompt, system_prompt)
    #   4. Print the response:
    #        print(f"\n  [proactive] {response}\n")
    #   5. Re-show the input prompt:
    #        print("You: ", end="", flush=True)
    #   6. Wrap everything (except sleep) in try/except
    #      to avoid crashing the background thread on errors
    # ==========================================================
    pass  # <-- Replace with your implementation


# -- Main -------------------------------------------------------------------

def main():
    existing = json.dumps(memory, indent=2) if memory else "None yet."
    system_prompt = (
        "You are a friendly personal assistant with persistent memory. "
        "When the user shares personal info, use 'remember' to save it. "
        "When they ask about something you might have saved, use 'recall' first.\n\n"
        f"Current memories:\n{existing}"
    )

    print("Proactive Agent (Step 4)")
    print(f"The agent will check in every {PROACTIVE_INTERVAL} seconds.")
    if memory:
        print(f"Loaded {len(memory)} memories from {MEMORY_FILE.name}")
    print("Press Ctrl+C to exit\n")

    # ==========================================================
    # TODO 3: Start the proactive loop in a background thread.
    #
    # Use threading.Thread:
    #   - target: proactive_loop
    #   - args: (system_prompt,)
    #   - daemon: True  (so it stops when main thread exits)
    # Don't forget to call .start()
    # ==========================================================
    # <-- Start the background thread here

    # Interactive chat (same as before)
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            messages.append({"role": "user", "content": user_input})

            while True:
                response = client.chat.completions.create(
                    model="gpt-5-mini", messages=messages, tools=tools
                )
                msg = response.choices[0].message
                messages.append(msg)

                if not msg.tool_calls:
                    print(f"\nAgent: {msg.content}\n")
                    break

                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    print(f"  [tool]   {tc.function.name}({json.dumps(args)})")
                    result = run_tool(tc.function.name, args)
                    print(f"  [result] {result[:150]}")
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break


if __name__ == "__main__":
    main()
