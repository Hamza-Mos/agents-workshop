"""
Exercise 1: Tool Calling Basics

This shows the fundamental mechanic behind every AI agent:
the model doesn't run code - it asks YOU to run code for it.

Here's exactly what happens:
  1. You define a tool as a JSON schema
  2. You send a message to the model with the tool available
  3. The model responds with a tool_call (not text!)
  4. Your code runs the actual function
  5. You send the result back to the model
  6. The model writes a final response using the result

YOUR TASK: Fill in the two TODOs below, then run this script.
Check your work against solutions/1_tool_calling_basics.py
"""

import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()


# -- Step 1: Define the tool ------------------------------------------------
# This JSON schema tells the model what the tool does. The model never sees
# your Python function - it only reads this description.

tools = [
    {
        "type": "function",
        "function": {
            # ==========================================================
            # TODO 1: Define the tool schema the model will see.
            #
            # Replace the "___" placeholders:
            #   "name": should match the Python function name below
            #   "description": tell the model what this tool does
            #   "parameters": this tool takes no arguments, so use
            #                 {"type": "object", "properties": {}}
            # ==========================================================
            "name": "___",
            "description": "___",
            "parameters": {"type": "object", "properties": {}},
        },
    }
]


# This is the actual function that runs on YOUR machine:
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


print("=" * 60)
print("  TOOL CALLING: STEP BY STEP")
print("=" * 60)

# -- Step 2: Send a message with the tool available -------------------------
user_message = "What time is it right now?"
print(f'\n>> Step 2: Sending message to model: "{user_message}"')
print("   (The tool definition is sent alongside so the model knows it exists)\n")

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": user_message}],
    tools=tools,
)
assistant_message = response.choices[0].message


# -- Step 3: The model responds with a tool call ----------------------------
print(">> Step 3: Model's response:")
if assistant_message.tool_calls:
    tool_call = assistant_message.tool_calls[0]
    print(f"   Tool to call: {tool_call.function.name}")
    print(f"   Arguments:    {tool_call.function.arguments}")
    print("   (Notice: it returned a tool_call, NOT a text response!)\n")
else:
    print("   Unexpected: the model responded with text instead of a tool call.")
    print(f"   Response: {assistant_message.content}")
    exit()


# -- Step 4: Execute the function -------------------------------------------
print(">> Step 4: Running the actual function on YOUR machine:")
result = get_current_time()
print(f"   Result: {result}\n")


# -- Step 5: Send the result back to the model ------------------------------
print(">> Step 5: Sending the result back to the model...\n")
messages = [
    {"role": "user", "content": user_message},
    assistant_message,
    {
        # ==========================================================
        # TODO 2: Fill in the tool result message.
        #
        # Replace the "___" placeholders:
        #   "role": what role is a tool result? (hint: "tool")
        #   "tool_call_id": how to link this to the tool call above?
        #                   (hint: tool_call.id)
        #   "content": what data do we send back?
        #              (hint: the result variable from Step 4)
        # ==========================================================
        "role": "___",
        "tool_call_id": "___",
        "content": "___",
    },
]

final_response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=messages,
    tools=tools,
)


# -- Step 6: The model writes a final answer --------------------------------
final_text = final_response.choices[0].message.content
print(f'>> Step 6: Model\'s final response: "{final_text}"')

print("\n" + "=" * 60)
print("  That's it. The model asked to call a function, your code")
print("  ran it, and the model used the result to answer.")
print("  This back-and-forth is how EVERY AI agent works.")
print("=" * 60)
