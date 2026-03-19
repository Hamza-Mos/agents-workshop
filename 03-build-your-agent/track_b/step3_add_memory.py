"""
Track B - Step 3: Add Memory

Same agent, now with persistent memory. Tell it your name, restart, ask again.
Memory is stored in agent_memory.json - just a JSON file.

YOUR TASK: Fill in the four TODOs below to add persistent memory.
Check your work against solutions/step3_add_memory.py
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

MEMORY_FILE = Path(__file__).parent / "agent_memory.json"


# ==========================================================
# TODO 1: Implement load_memory() and save_memory()
#
# load_memory():
#   - If MEMORY_FILE exists, read and parse the JSON
#   - Otherwise return an empty dict {}
#   - Hint: MEMORY_FILE.exists(), MEMORY_FILE.read_text(), json.loads()
#
# save_memory(data):
#   - Write the dict as JSON to MEMORY_FILE
#   - Hint: MEMORY_FILE.write_text(json.dumps(data, indent=2))
# ==========================================================

def load_memory():
    pass  # <-- Replace with your implementation


def save_memory(data):
    pass  # <-- Replace with your implementation


memory = load_memory() or {}

# ==========================================================
# TODO 2: Write the system prompt.
#
# The model needs to know it has memory capabilities.
# Include:
#   1. Tell it it's a personal assistant with persistent memory
#   2. Tell it to use 'remember' when the user shares personal info
#   3. Tell it to use 'recall' when the user asks about stored info
#   4. Include the current memories so the model starts with context:
#      "Current memories:\n" + (json.dumps(memory, indent=2) if memory else "None yet.")
# ==========================================================
SYSTEM_PROMPT = ""  # <-- Replace with your system prompt

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
            "name": "web_search",
            "description": "Search the web",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        # ==========================================================
        # TODO 3: Define the "remember" tool schema.
        #
        # It needs two required string parameters:
        #   "key" - short label like 'name', 'major', 'favorite_color'
        #   "value" - the fact to save
        #
        # Pattern (same as calculate/web_search above):
        #   "parameters": {
        #       "type": "object",
        #       "properties": {
        #           "key": {"type": "string", "description": "..."},
        #           "value": {"type": "string", "description": "..."},
        #       },
        #       "required": ["key", "value"],
        #   }
        # ==========================================================
        "type": "function",
        "function": {
            "name": "remember",
            "description": "Save a fact to persistent memory",
            "parameters": {
                "type": "object",
                "properties": {},  # <-- Add "key" and "value" properties
                "required": [],  # <-- List required parameter names
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
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
    "log": math.log, "pi": math.pi, "e": math.e,
    "abs": abs, "round": round,
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
    if name == "calculate":
        try:
            return str(eval(args["expression"], SAFE_MATH))
        except Exception as e:
            return f"Error: {e}"
    if name == "web_search":
        return web_search(args["query"])
    # ==========================================================
    # TODO 4: Add the "remember" and "recall" branches.
    #
    # remember:
    #   1. Store: memory[args["key"]] = args["value"]
    #   2. Persist: save_memory(memory)
    #   3. Return: f"Saved: {args['key']} = {args['value']}"
    #
    # recall:
    #   - If memory has data: return json.dumps(memory, indent=2)
    #   - Otherwise: return "No memories yet."
    # ==========================================================
    if name == "remember":
        pass  # <-- Replace with your implementation
    if name == "recall":
        pass  # <-- Replace with your implementation
    return f"Unknown tool: {name}"


def agent_loop(messages):
    """The agent loop - same as before, unchanged."""
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
    print("Agent with Memory (Step 3)")
    if memory:
        print(f"Loaded {len(memory)} memories from {MEMORY_FILE.name}")
    print("Tools: time, calculator, web search, remember, recall")
    print("Press Ctrl+C to exit\n")

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
