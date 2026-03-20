"""
Exercise 2: The Agent Loop

A complete AI agent in about 40 lines of Python.
This is the most important code in the workshop.

The while True loop IS the agent. The model decides what to do.
Your code just executes tools and feeds results back.

YOUR TASK: Implement the agent() function below, then run this script.
Check your work against solutions/2_agent_loop.py

Try:
  "What time is it and what's the weather in Toronto?"
  "Compare the weather in Tokyo and London right now."

Watch it chain multiple tool calls automatically.
"""

import json
import urllib.parse
import urllib.request
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
            "name": "get_weather",
            "description": "Get the current weather for any city in the world. Returns temperature, conditions, humidity, and wind.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g. 'Toronto', 'London', 'Tokyo'",
                    }
                },
                "required": ["city"],
            },
        },
    },
]


def get_weather(city):
    """Get real-time weather from wttr.in (no API key needed)."""
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        if "data" in data:
            data = data["data"]
        c = data["current_condition"][0]
        return (
            f"{city}: {c['temp_C']}°C ({c['temp_F']}°F), "
            f"{c['weatherDesc'][0]['value']}, "
            f"Humidity: {c['humidity']}%, "
            f"Wind: {c['windspeedKmph']} km/h"
        )
    except Exception as e:
        return f"Could not get weather for {city}: {e}"


def run_tool(name, args):
    if name == "get_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if name == "get_weather":
        return get_weather(args["city"])
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
    #
    # Try: "What's the weather in Tokyo?" to see the weather tool in action.
    # ==========================================================
    
    while True:
        response = client.chat.completions.create(
               model="gpt-5-mini", messages=messages, tools=tools
           )
        
        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content

        for tool_call in msg.tool_calls:
            tool_args = json.loads(tool_call.function.arguments)
            print(f"  [tool call]  {tool_call.function.name}({json.dumps(tool_args)})")
            result = run_tool(tool_call.function.name, tool_args)
            print(f"  [result]     {result}")
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})




# -- Try it -----------------------------------------------------------------

if __name__ == "__main__":
    print("Agent Loop Demo")
    print("This agent has two tools: time and weather.")
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
