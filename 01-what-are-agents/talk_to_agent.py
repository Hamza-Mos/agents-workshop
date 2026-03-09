"""
Talk to a Real AI Agent

This agent has three tools:
  - get_current_time: Check the time in any timezone
  - calculate: Do math
  - web_search: Search the internet

Try asking:
  "What time is it in Tokyo?"
  "What's the square root of 2048?"
  "Search the web for AI agent frameworks"
  "What time is it, and what's 15% of 847?"  (watch it chain two tools!)

Press Ctrl+C to exit.
"""

import json
import math
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
            "name": "calculate",
            "description": "Evaluate a math expression. Supports standard math: +, -, *, /, **, sqrt(), sin(), cos(), log(), pi, e.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression, e.g. 'sqrt(144)' or '2**10 + 5'",
                    }
                },
                "required": ["expression"],
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

SAFE_MATH_GLOBALS = {
    "__builtins__": {},
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log2": math.log2,
    "log10": math.log10,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
    "round": round,
    "pow": pow,
    "min": min,
    "max": max,
}


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


def calculate(expression):
    try:
        result = eval(expression, SAFE_MATH_GLOBALS)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def web_search(query):
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8")
        results = []
        for chunk in html.split('class="result__snippet"')[1:4]:
            end = chunk.find("</")
            if end > 0:
                text = chunk[1:end]
                # Strip HTML tags
                clean = ""
                in_tag = False
                for ch in text:
                    if ch == "<":
                        in_tag = True
                    elif ch == ">":
                        in_tag = False
                    elif not in_tag:
                        clean += ch
                clean = clean.replace("&amp;", "&").replace("&quot;", '"').replace("&#x27;", "'").strip()
                if clean:
                    results.append(clean)
        return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search failed ({e}). Try a different query."


TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "web_search": web_search,
}


# ---------------------------------------------------------------------------
# The agent loop
# ---------------------------------------------------------------------------

def chat():
    print("=" * 55)
    print("  AI Agent Demo - type a message and watch it think")
    print("  Tools: time, calculator, web search")
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
