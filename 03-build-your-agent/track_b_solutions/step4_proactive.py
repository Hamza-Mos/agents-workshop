"""
Track B - Step 4: Proactive Scheduling

Same agent, now with a background thread that triggers the agent on a timer.
The agent will periodically print a message without you asking.

This is the terminal equivalent of getting an unprompted Telegram message
from your agent.
"""

import json
import os
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
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
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
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
    if name == "get_current_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if name == "get_weather":
        return get_weather(args["city"])
    if name == "web_search":
        return web_search(args["query"])
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

PROACTIVE_INTERVAL = 60  # seconds
PROACTIVE_PROMPT = (
    "You are checking in proactively. The current time is {time}. "
    "Share a brief, useful observation - a fun fact, a productivity tip, "
    "or a reminder to take a break. Keep it to 1-2 sentences."
)


def proactive_loop(system_prompt):
    """Background thread that triggers the agent periodically."""
    while True:
        time.sleep(PROACTIVE_INTERVAL)
        try:
            prompt = PROACTIVE_PROMPT.format(time=datetime.now().strftime("%H:%M"))
            response = run_agent(prompt, system_prompt)
            print(f"\n  [proactive] {response}\n")
            print("You: ", end="", flush=True)  # re-show the prompt
        except Exception as e:
            pass  # Don't crash the background thread on errors


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

    # Start the proactive background thread
    scheduler = threading.Thread(target=proactive_loop, args=(system_prompt,), daemon=True)
    scheduler.start()

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
