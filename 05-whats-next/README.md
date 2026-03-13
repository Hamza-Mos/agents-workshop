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

## Agents for academia

The same primitives you learned today power tools built specifically for research. Here's what's out there:

### Literature review and paper discovery

- **[Elicit](https://elicit.com)** — searches, summarizes, and extracts data from 125M+ papers. Used by 2M+ researchers.
- **[Semantic Scholar](https://www.semanticscholar.org)** — free AI-powered search from the Allen Institute (AI2). Understands topics, not just keywords.
- **[Consensus](https://consensus.app)** — answers research questions by showing agree/disagree across studies.
- **[Liner](https://liner.ai)** — AI agents for literature synthesis, peer review, and finding research gaps.
- **[Connected Papers](https://www.connectedpapers.com)** / **[Research Rabbit](https://www.researchrabbit.ai)** / **[Litmaps](https://www.litmaps.com)** — visual citation graphs for discovering related work.

### Paper review and writing

- **[Paperpal](https://paperpal.com)** — writing support, paraphrasing, plagiarism detection, and submission readiness checks.
- **[Scite](https://scite.ai)** — shows how a paper has been cited: supported, contradicted, or just mentioned.

### Grading and teaching

- **[Gradescope](https://www.gradescope.com)** — AI-assisted grading for assignments, exams, and handwritten work. Originally from UC Berkeley.

### Coding agents

- **Claude Code, Cursor, GitHub Copilot** — coding agents with tool calling under the hood.
- **[Agent Skills](https://agentskills.io)** — an open standard for giving agents new capabilities via SKILL.md files. Works across 30+ products.

### The connection to what you built today

Every one of these tools runs on the same ideas you just learned:
- Elicit searching 125M papers? **Tool calling.**
- Consensus tracking agreement across studies? **An agent loop with structured output.**
- scienceOS remembering your research context? **That's MEMORY.md.**
- And every single one can hallucinate citations. **Part 04 applies here too.**

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
