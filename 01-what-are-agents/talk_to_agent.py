"""
Talk to a Real AI Agent

This agent has three tools:
  - get_current_time: Check the time in any timezone
  - get_weather: Get real-time weather for any city
  - web_search: Search the internet

Try asking:
  "What time is it in Tokyo?"
  "What's the weather in Waterloo?"
  "What time is it in London and what's the weather there?"  (chains two tools!)
  "Search the web for the latest AI news"

Press Ctrl+C to exit.
"""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file (in the repo root)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()

MODEL = "gpt-5-mini"

# ---------------------------------------------------------------------------
# Tool definitions (this is what the model sees)
# ---------------------------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time, optionally in a specific timezone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone like 'America/New_York' or 'Asia/Tokyo'. Leave empty for local time.",
                    }
                },
            },
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
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web and return the top results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for",
                    }
                },
                "required": ["query"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Tool implementations (this is what actually runs on your machine)
# ---------------------------------------------------------------------------

def get_current_time(timezone=None):
    try:
        if timezone:
            from zoneinfo import ZoneInfo
            now = datetime.now(ZoneInfo(timezone))
        else:
            now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S %Z").strip()
    except Exception as e:
        return f"Error: {e}"


def get_weather(city):
    """Get real-time weather from wttr.in (no API key needed)."""
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        # wttr.in wraps everything under "data" key
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


TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "get_weather": get_weather,
    "web_search": web_search,
}


# ---------------------------------------------------------------------------
# The agent loop
# ---------------------------------------------------------------------------

def chat():
    print("=" * 55)
    print("  AI Agent Demo - type a message and watch it think")
    print("  Tools: time, weather, web search")
    print("  Press Ctrl+C to exit")
    print("=" * 55)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant with access to tools. "
                "Use them whenever they would help answer the user's question. "
                "Be concise."
            ),
        }
    ]

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        # The agent loop: keep going until the model gives a final text response
        while True:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
            )
            msg = response.choices[0].message
            messages.append(msg)

            # No tool calls? We have our final answer.
            if not msg.tool_calls:
                print(f"\nAgent: {msg.content}")
                break

            # Execute each tool the model wants to call
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"\n  [tool call]  {name}({json.dumps(args)})")
                func = TOOL_FUNCTIONS.get(name)
                if func is None:
                    result = f"Unknown tool: {name}"
                else:
                    result = func(**args)
                print(f"  [result]     {result[:200]}")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )


if __name__ == "__main__":
    chat()
