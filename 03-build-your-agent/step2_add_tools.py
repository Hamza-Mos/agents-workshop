"""
Track B - Step 2: Add Tools

Same agent, more tools: calculator and web search.
Notice the agent loop doesn't change at all - you just add definitions and functions.

YOUR TASK: Fill in the two TODOs below to add calculator and web search tools.
Check your work against solutions/step2_add_tools.py
"""

import json
import math
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
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
    # Tool A: "calculate"
    #   - description: "Evaluate a math expression like '2**10', 'sqrt(144)', or '15 * 0.18'"
    #   - parameters: one required string called "expression"
    #     Example structure:
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "expression": {"type": "string", "description": "Math expression"}
    #         },
    #         "required": ["expression"],
    #     }
    #
    # Tool B: "web_search"
    #   - description: "Search the web for information"
    #   - parameters: one required string called "query"
    #     (same structure as calculate, but with "query" instead)
    # ==========================================================
]

# Safe math functions that eval() is allowed to use (no builtins = no dangerous code)
SAFE_MATH = {
    "__builtins__": {},
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
    "log": math.log, "pi": math.pi, "e": math.e,
    "abs": abs, "round": round, "pow": pow,
}


def web_search(query):
    """Search DuckDuckGo and return text snippets. No API key needed."""
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
        return f"Search failed: {e}"


def run_tool(name, args):
    """Execute a tool by name and return the result as a string."""
    if name == "get_current_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ==========================================================
    # TODO 2: Add the "calculate" and "web_search" branches.
    #
    # calculate:
    #   - Evaluate: result = eval(args["expression"], SAFE_MATH)
    #   - Return str(result)
    #   - Wrap in try/except, return f"Error: {e}" on failure
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
    print("Tools: time, calculator, web search | Press Ctrl+C to exit\n")

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
