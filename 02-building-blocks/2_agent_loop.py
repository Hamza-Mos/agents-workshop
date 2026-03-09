"""
Exercise 2: The Agent Loop

A complete AI agent in about 40 lines of Python.
This is the most important code in the workshop.

The while True loop IS the agent. The model decides what to do.
Your code just executes tools and feeds results back.

YOUR TASK: Implement the agent() function below, then run this script.
Check your work against solutions/2_agent_loop.py

Try:
  "What time is it, and what's 2 to the power of 10?"
  "What's the square root of the number of seconds in a day?"

Watch it chain multiple tool calls automatically.
"""

import json
import math
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()


# -- Tools the agent can use ------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression like '2**10' or 'sqrt(86400)'",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]

SAFE_MATH = {"__builtins__": {}, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}


def run_tool(name, args):
    if name == "get_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if name == "calculate":
        return str(eval(args["expression"], SAFE_MATH))
    return f"Unknown tool: {name}"


# -- The agent (this is the whole thing) ------------------------------------


def agent(user_input):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use your tools when needed."},
        {"role": "user", "content": user_input},
    ]

    # ==========================================================
    # TODO: Implement the agent loop.
    #
    # This is a while True loop that repeats:
    #
    #   1. Call the model:
    #        response = client.chat.completions.create(
    #            model="gpt-5-mini", messages=messages, tools=tools
    #        )
    #
    #   2. Get the message and add it to history:
    #        msg = response.choices[0].message
    #        messages.append(msg)
    #
    #   3. If no tool calls -> the model is done:
    #        if not msg.tool_calls:
    #            return msg.content
    #
    #   4. Otherwise, for each tool call (tc) in msg.tool_calls:
    #        - Parse args: args = json.loads(tc.function.arguments)
    #        - Print:      print(f"  [tool call]  {tc.function.name}({json.dumps(args)})")
    #        - Execute:    result = run_tool(tc.function.name, args)
    #        - Print:      print(f"  [result]     {result}")
    #        - Append:     messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    #
    #   5. Loop back to step 1. The model sees the results and decides next.
    # ==========================================================
    pass  # <-- Remove this and write your loop here


# -- Try it -----------------------------------------------------------------

if __name__ == "__main__":
    print("Agent Loop Demo")
    print("This agent has two tools: time and calculator.")
    print("Press Ctrl+C to exit.\n")

    while True:
        try:
            q = input("You: ").strip()
            if q:
                answer = agent(q)
                print(f"\nAgent: {answer}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break
