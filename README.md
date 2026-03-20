# Agents in the Wild: Building AI That Actually Does Things

### [Workshop Slides](https://docs.google.com/presentation/d/1aOLggFxcjNJyCzIBuaZYleKcgOvIgmjX/edit?usp=sharing&ouid=101398429659460548301&rtpof=true&sd=true)

A 3-hour hands-on workshop. You'll build a real AI agent from scratch, give it a personality, teach it to remember things, and then try to break it.

## What you'll walk away with

- A working AI agent you built yourself
- Understanding of how tool calling, memory, and the agent loop work
- Hands-on experience breaking and defending agents
- A repo you can keep building on after the workshop

## Workshop flow

| #  | Section | What you'll do |
|----|---------|---------------|
| 00 | [Setup](00-setup/) | Install uv, get your API key |
| 01 | [What Are Agents?](01-what-are-agents/) | Talk to a real agent, watch it think |
| 02 | [Building Blocks](02-building-blocks/) | Build tool calling, an agent loop, and memory from scratch |
| 03 | [Build Your Agent](03-build-your-agent/) | Build your own personal AI agent with personality and memory |
| 04 | [Trust & Safety](04-trust-and-safety/) | Try to break agents, learn why safety rules matter |
| 05 | [What's Next](05-whats-next/) | Keep building after the workshop |

Start with [00-setup](00-setup/) if you haven't set up yet, or jump to [01-what-are-agents](01-what-are-agents/) if you're ready.

## Quick start

```bash
# 1. Install uv (installs Python for you automatically)
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS/Linux
# Windows (PowerShell): powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Clone and run
git clone https://github.com/Hamza-Mos/agents-workshop.git
cd agents-workshop
cp .env.example .env
# paste your API key into .env (provided at the workshop)
uv run 01-what-are-agents/talk_to_agent.py
```

`uv run` handles everything: downloads Python, installs dependencies, runs the script. No pip, no venv, no setup headaches.

## What you need

- A laptop with WiFi
- Node.js 22+ (for Part 3 - OpenClaw agent setup) — install from [nodejs.org](https://nodejs.org/)
- Telegram installed on your phone (for Part 3)
- API keys are provided at the workshop — you don't pay for anything
- **You do NOT need Python installed** — uv downloads it for you
