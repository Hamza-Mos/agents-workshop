# Agents in the Wild: Building AI That Actually Does Things

A 3-hour hands-on workshop. You'll build a real AI agent from scratch, give it a personality, teach it to remember things, and then try to break it.

## What you'll walk away with

- A working AI agent you built yourself
- Understanding of how tool calling, memory, and the agent loop work
- Hands-on experience breaking and defending agents
- A repo you can keep building on after the workshop

## Workshop flow

| #  | Section | What you'll do |
|----|---------|---------------|
| 00 | [Setup](00-setup/) | Install Python, get your API key |
| 01 | [What Are Agents?](01-what-are-agents/) | Talk to a real agent, watch it think |
| 02 | [Building Blocks](02-building-blocks/) | Build tool calling, an agent loop, and memory from scratch |
| 03 | [Build Your Agent](03-build-your-agent/) | Build your own personal AI agent with personality and memory |
| 04 | [Trust & Safety](04-trust-and-safety/) | Try to break agents, learn why safety rules matter |
| 05 | [What's Next](05-whats-next/) | Keep building after the workshop |

Start with [00-setup](00-setup/) if you haven't set up yet, or jump to [01-what-are-agents](01-what-are-agents/) if you're ready.

## Quick start

```bash
git clone https://github.com/Hamza-Mos/agents-workshop.git
cd agents-workshop
pip install -r requirements.txt
cp .env.example .env
# paste your API key into .env (provided at the workshop)
python3 01-what-are-agents/talk_to_agent.py
```

## What you need

- A laptop with WiFi
- Python 3.9+ (for Parts 1-2 exercises)
- Node.js 18+ (for Part 3 - OpenClaw agent setup)
- Telegram installed on your phone (for Part 3)
- API keys are provided at the workshop - you don't pay for anything
