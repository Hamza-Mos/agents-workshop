# 03 - Build Your Agent

This is the centerpiece of the workshop. You'll set up a real personal AI agent: the same platform the instructor runs 24/7 as a personal assistant.

## What you're building

[OpenClaw](https://github.com/openclaw/openclaw) is an open-source agent platform. You connect it to Telegram (or other messaging apps), give it a personality, set safety rules, and it becomes your personal AI assistant. The instructor's setup monitors email, iMessage, WhatsApp, Twitter, and calendar - all through Telegram. You'll set up the same core platform today.

## Before you start: real agents in production

To give you a sense of where this is heading:

**Coding agents** are the most mature category right now. Claude Code, Cursor, and Devin can fix real GitHub issues. On SWE-bench, agents went from solving 2% of issues in 2023 to 72% in 2026. The reason they work so well: code is testable, so the agent can verify its own output.

**Personal agents** (what you're building) are the next frontier. The instructor's setup handles 6-8 daily tasks proactively - morning briefings, email triage, Twitter digests - without being asked. What broke along the way: cron jobs that ran silently for two days burning API credits, WhatsApp sessions dropping randomly, and a prompt injection attempt embedded in an email.

**Workspace files** are how you configure the agent:
- `SOUL.md` - personality and communication style
- `AGENTS.md` - security rules (what the agent can and can't do)
- `USER.md` - context about you (timezone, interests, projects)
- `MEMORY.md` - facts the agent learns over time

You'll create all of these.

## Progress checklist

Everyone goes through all steps:

```
Step 1-3   Install, create Telegram bot, configure     (~10 min)
Step 4     Agent uses tools                            (~5 min)
Step 5     Create workspace files (personality + safety) (~15 min)
Step 6     Add persistent memory                       (~10 min)
Step 7     Add proactive scheduling                    (~10 min)
```

## Step-by-step guide

Follow the [OpenClaw setup guide](track-a-openclaw.md) - it walks you through everything from installation to proactive scheduling.

If you finish early or want to keep building after the workshop, there's also a [Python-from-scratch track](track-b-python.md) where you build an agent with no frameworks, just the OpenAI API.

## Templates

The [templates/](templates/) folder has example workspace files you can customize:
- [SOUL.md](templates/SOUL.md) - personality definition
- [AGENTS.md](templates/AGENTS.md) - security rules
- [USER.md](templates/USER.md) - user context

These are based on real production configs and community contributions. Copy them into your agent's workspace and make them yours.

---

Next: [04 - Trust & Safety](../04-trust-and-safety/) - try to break your agent.
