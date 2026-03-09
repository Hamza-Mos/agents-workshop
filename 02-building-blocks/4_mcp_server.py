"""
Stretch: Build an MCP Server

MCP (Model Context Protocol) is the "USB standard" for connecting
AI agents to tools. Build once, connect to Claude Desktop, Cursor,
VS Code, or any MCP-compatible client.

Install: pip install mcp
Run:     python3 4_mcp_server.py

Then add this server to your MCP client's config.
Learn more: https://modelcontextprotocol.io
"""

import math
from datetime import datetime

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("MCP not installed. Run: pip install mcp")
    print("This is a stretch exercise - it's optional.")
    exit(1)

server = FastMCP("Workshop Demo")


@server.tool()
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@server.tool()
def calculate(expression: str) -> str:
    """Evaluate a math expression like '2**10' or 'sqrt(144)'."""
    allowed = {"__builtins__": {}, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}
    return str(eval(expression, allowed))


if __name__ == "__main__":
    print("Starting MCP server with tools: get_current_time, calculate")
    print("Connect to this server from Claude Desktop or any MCP client.")
    server.run()
