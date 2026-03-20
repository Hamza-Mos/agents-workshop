"""
Track B - Step 2: Add Tools

Same agent, more tools: weather and web search.
Notice the agent loop doesn't change at all - you just add definitions and functions.

YOUR TASK: Fill in the two TODOs below to add weather and web search tools.
Check your work against solutions/step2_add_tools.py
"""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
client = OpenAI()

SYSTEM_PROMPT = "You are a friendly personal assistant. Use your tools when they'd help."

# The time tool is already defined for you. Add the new ones below.
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    # ==========================================================
    # TODO 1: Add two more tool definitions.
    #
    # Tool A: "get_weather"
    #   - description: "Get the current weather for any city in the world. Returns temperature, conditions, humidity, and wind."
    #   - parameters: one required string called "city"
    #     Example structure:
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "city": {"type": "string", "description": "City name, e.g. 'Toronto', 'London', 'Tokyo'"}
    #         },
    #         "required": ["city"],
    #     }
    #
    # Tool B: "web_search"
    #   - description: "Search the web for information"
    #   - parameters: one required string called "query"
    #     (same structure as get_weather, but with "query" instead)
    # ==========================================================
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
            f"{city}: {c['temp_C']}\u00b0C ({c['temp_F']}\u00b0F), "
            f"{c['weatherDesc'][0]['value']}, "
            f"Humidity: {c['humidity']}%, "
            f"Wind: {c['windspeedKmph']} km/h"
        )
    except Exception as e:
        return f"Could not get weather for {city}: {e}"


def web_search(query):
    """Search the web via Brave Search API."""
    api_key = os.environ.get("BRAVE_SEARCH_API_KEY", "")
    url = "https://api.search.brave.com/res/v1/web/search?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        results = []
        for i, r in enumerate(data.get("web", {}).get("results", [])[:5]):
            title = r.get("title", "")
            desc = r.get("description", "")
            results.append(f"{i+1}. {title}\n   {desc}")
        return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search failed: {e}"


def run_tool(name, args):
    """Execute a tool by name and return the result as a string."""
    if name == "get_current_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ==========================================================
    # TODO 2: Add the "get_weather" and "web_search" branches.
    #
    # get_weather:
    #   - Call: get_weather(args["city"])
    #   - Return the result
    #
    # web_search:
    #   - Call: web_search(args["query"])
    #   - Return the result
    # ==========================================================
    return f"Unknown tool: {name}"


def agent_loop(messages):
    """The agent loop - same as Step 1, unchanged."""
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
            print(f"  [tool]   {tc.function.name}({json.dumps(args)})")
            result = run_tool(tc.function.name, args)
            print(f"  [result] {result[:150]}")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})


def main():
    print("Agent with Tools (Step 2)")
    print("Tools: time, weather, web search | Press Ctrl+C to exit\n")

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
