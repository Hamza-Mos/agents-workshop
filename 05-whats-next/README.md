# 05 - What's Next

You built an AI agent. Here's how to keep going.

## This weekend

If you set up OpenClaw (Track A), add more integrations using the [full setup guide](https://github.com/Hamza-Mos/openclaw-setup):

- **iMessage** via BlueBubbles (Mac only)
- **WhatsApp** via wacli
- **Gmail** via Google API
- **Google Calendar** for scheduling
- **Twitter/X** for monitoring and drafting

Each integration takes 15-30 minutes to set up.

## If you did the Python track (Track B)

Next steps for your Python agent:
- Connect it to Telegram using [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- Build an MCP server (see Exercise 4 in [Building Blocks](../02-building-blocks/))
- Load personality from a SOUL.md file instead of a hardcoded system prompt
- Add more tools: file operations, HTTP requests, database queries

## Build an MCP server

MCP (Model Context Protocol) is becoming the standard for agent tools. Build a server and it works with Claude Desktop, Cursor, VS Code, and more.

Start with Exercise 4 in [Building Blocks](../02-building-blocks/4_mcp_server.py), then check out:
- [MCP documentation](https://modelcontextprotocol.io)
- [Community MCP servers](https://github.com/modelcontextprotocol/servers) (12,000+ and growing)

## Go deeper: research

Open problems in agent safety and reliability:

- **Prompt injection defenses** - No complete solution exists yet. Active research area.
- **Explainability** - Can an agent explain why it took a specific action?
- **Algorithmic recourse** - If an agent decision affects you, can you change the outcome? (Prof. Karimi's research at [CHARM Lab](https://uwaterloo.ca/computational-health-and-reasoning-machines-lab/))
- **Multi-agent coordination** - How do agents work together safely?

## Resources

- [OpenClaw](https://github.com/openclaw/openclaw) - the platform you set up today
- [OpenClaw setup guide](https://github.com/Hamza-Mos/openclaw-setup) - full integration walkthrough
- [OpenAI function calling docs](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic tool use docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [MCP specification](https://modelcontextprotocol.io)
- [ReAct paper](https://arxiv.org/abs/2210.03629) (Yao et al., ICLR 2023)
- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

## Cost context

- What you built today: ~$1-2 in API credits
- Basic personal agent (Telegram only): ~$5-15/month
- Full 7-channel setup (email, iMessage, WhatsApp, etc.): ~$120-195/month

You can start for almost nothing and scale up as you add integrations.

## Stay connected

- This repo stays public. Everything you need to keep going is here.
- Star the repo if you want updates.
- PRs welcome if you build something cool and want to share it.
