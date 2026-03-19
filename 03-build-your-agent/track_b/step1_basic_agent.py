"""
Track B - Step 1: Basic Agent

The simplest possible agent. One tool (time), one loop.
This is the foundation everything else builds on.

YOUR TASK: Implement the agent_loop() function below.
This is the same pattern from Exercise 2 in Building Blocks.
Check your work against solutions/step1_basic_agent.py
"""

import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from the .env file in the repo root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()

# The system prompt tells the model how to behave
SYSTEM_PROMPT = "You are a friendly personal assistant. Use your tools when they'd help."

# One simple tool: get the current time
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def run_tool(name, args):
    """Execute a tool by name and return the result as a string."""
    if name == "get_current_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Unknown tool: {name}"


def agent_loop(messages):
    """Run the agent loop until the model produces a text response.

    This is the core pattern:
      while True -> call model -> check for tool calls -> execute -> repeat
    """
    # ==========================================================
    # TODO: Implement the agent loop.
    #
    # while True:
    #   1. Call the model:
    #        response = client.chat.completions.create(
    #            model="gpt-5-mini", messages=messages, tools=tools
    #        )
    #   2. Get the response message and add to history:
    #        msg = response.choices[0].message
    #        messages.append(msg)
    #   3. If no tool calls, return the text:
    #        if not msg.tool_calls:
    #            return msg.content
    #   4. For each tool call:
    #        - Parse: args = json.loads(tc.function.arguments)
    #        - Print: print(f"  [tool]  {tc.function.name}({json.dumps(args)})")
    #        - Run:   result = run_tool(tc.function.name, args)
    #        - Print: print(f"  [result] {result}")
    #        - Add result to messages:
    #            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    # ==========================================================
    pass  # <-- Remove this and write your loop here


def main():
    print("Basic Agent (Step 1)")
    print("Tools: time | Press Ctrl+C to exit\n")

    # Start the conversation with the system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            messages.append({"role": "user", "content": user_input})
            answer = agent_loop(messages)
            print(f"\nAgent: {answer}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break


if __name__ == "__main__":
    main()
