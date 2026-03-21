"""
Track B - Step 1: Basic Agent

The simplest possible agent. One tool (time), one loop.
This is the foundation everything else builds on.
"""

import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
client = OpenAI()

SYSTEM_PROMPT = "You are a friendly personal assistant. Use your tools when they'd help."

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
    if name == "get_current_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Unknown tool: {name}"


def agent_loop(messages):
    """Run the agent loop until the model produces a text response."""
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
            print(f"  [tool]  {tc.function.name}({json.dumps(args)})")
            result = run_tool(tc.function.name, args)
            print(f"  [result] {result}")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})


def main():
    print("Basic Agent (Step 1)")
    print("Tools: time | Press Ctrl+C to exit\n")

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
