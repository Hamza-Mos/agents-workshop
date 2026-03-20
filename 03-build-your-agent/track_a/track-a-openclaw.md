# Track A: OpenClaw Setup

Set up a personal AI agent on Telegram with a custom personality, safety rules, and persistent memory.

## Fresh start (if you're stuck)

If you tried setting up before and want to start clean:

```bash
npm uninstall -g openclaw
rm -rf ~/.openclaw
```

Then follow the steps below from the beginning.

## Prerequisites

- Node.js 22+ (check: `node --version`; install from [nodejs.org](https://nodejs.org), Node 24 recommended)
- An Anthropic API key (provided at the workshop)
- Telegram on your phone

## Step 1: Install OpenClaw

```bash
npm install -g openclaw@latest
```

Verify:

```bash
openclaw --version
```

> **Permission errors on macOS?** Use `sudo npm install -g openclaw@latest`

## Step 2: Create a Telegram bot

1. Open Telegram, search for `@BotFather`
2. Send `/newbot`, follow prompts, pick a username ending in `bot`
3. Copy the bot token (looks like `7123456789:AAH...`)

**Find your bot:**

1. In Telegram, search for `@your_bot_username` (the username you chose in BotFather)
2. Tap the bot, then tap **Start** (or send `/start`)

## Step 3: Run onboarding

```bash
openclaw onboard
```

The wizard walks you through setup. When prompted:

| Prompt         | What to enter                   |
| -------------- | ------------------------------- |
| Model provider | **Anthropic**                   |
| API key        | The workshop key (`sk-ant-...`) |
| Channel        | **Telegram**                    |
| Bot token      | Your token from Step 2          |

### Approve your pairing code

After onboarding, your bot uses **pairing mode** — it won't respond until you approve yourself.

1. Message your bot on Telegram (tap Start or send `/start`)
2. The bot replies with something like:
   ```
   OpenClaw: access not configured.
   Your Telegram user id: 6065404262
   Pairing code: 2N7NYWUV
   Ask the bot owner to approve with:
   openclaw pairing approve telegram 2N7NYWUV
   ```
3. Copy the pairing code and run this in your terminal:
   ```bash
   openclaw pairing approve telegram YOUR_CODE
   ```
4. Send another message to your bot — it should respond now!

## Step 4: Test it

```bash
openclaw gateway status
```

Message your bot on Telegram. If it responds, you're live.

**Not working?**

| Problem                            | Fix                                                                              |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| Bot says "access not configured"   | Run `openclaw pairing approve telegram YOUR_CODE` with the code the bot gave you |
| Bot doesn't respond at all         | `openclaw gateway status` — is it running? If not: `openclaw gateway start`      |
| Gateway running, still no response | Check `openclaw pairing list telegram` for pending codes to approve              |
| Config errors                      | `openclaw doctor --fix`                                                          |

## Step 5: Create workspace files

These define your agent's personality, rules, and memory. Copy the templates from the repo:

```bash
mkdir -p ~/.openclaw/workspace
cp 03-build-your-agent/track_a/templates/SOUL.md ~/.openclaw/workspace/
cp 03-build-your-agent/track_a/templates/AGENTS.md ~/.openclaw/workspace/
cp 03-build-your-agent/track_a/templates/USER.md ~/.openclaw/workspace/
```

**Customize them:**

1. Open `~/.openclaw/workspace/USER.md` — fill in your name, timezone, interests
2. Open `~/.openclaw/workspace/SOUL.md` — tweak the personality to match how you want your agent to talk
3. **Don't touch AGENTS.md** unless you know what you're doing — the safety rules are important

**Add MEMORY.md** — get your Chat ID by messaging [@userinfobot](https://t.me/userinfobot) on Telegram:

```bash
cp 03-build-your-agent/track_a/templates/MEMORY.md ~/.openclaw/workspace/
```

Open `~/.openclaw/workspace/MEMORY.md` and paste your Chat ID.

Restart and test:

```bash
openclaw gateway restart
```

Tell your agent something ("my favorite language is Python"), then restart and ask "what do you know about me?" — if it remembers, memory works.

## Step 6: Proactive scheduling

Make the agent message you without being asked.

> **Always use `--announce --channel telegram`** or the output never reaches Telegram.

Quick test (runs every minute):

```bash
openclaw cron add --name "Workshop test" \
  --cron "* * * * *" \
  --announce --channel telegram \
  --message "Send me an encouraging message about the workshop."
```

When you get an unprompted message, it works. Clean up:

```bash
openclaw cron list
openclaw cron rm <id>
```

### Actually useful cron jobs

**Morning briefing (every day at 8am):**

```bash
openclaw cron add --name "Morning briefing" \
  --cron "0 8 * * *" \
  --announce --channel telegram \
  --message "Give me a 30-second morning briefing: weather in Waterloo, any reminders I've set, and one interesting thing in AI news today."
```

**Study accountability (every evening at 9pm):**

```bash
openclaw cron add --name "Study check" \
  --cron "0 21 * * *" \
  --announce --channel telegram \
  --message "Ask me what I studied today. If I didn't study, give me a motivational push."
```

**One-shot exam reminder:**

```bash
openclaw cron add --name "Midterm reminder" \
  --at "48h" \
  --announce --channel telegram \
  --message "Your CS 341 midterm is TOMORROW. Ask me if I've reviewed the key topics."
```

> **Timing formats:** `--cron "0 7 * * *"` for recurring, `--at "90m"` for one-shot reminders, `--every "2h"` for intervals. Add `--delete-after-run` to one-shots.

## Why this is different from ChatGPT

You already have ChatGPT. Here's what your OpenClaw agent does that ChatGPT **cannot**:

|                     | ChatGPT                               | Your OpenClaw Agent                      |
| ------------------- | ------------------------------------- | ---------------------------------------- |
| **Proactive**       | Never messages you first              | Wakes you up with a morning briefing     |
| **Always on**       | You go to a browser tab               | It's in Telegram — text it like a friend |
| **Memory**          | Limited, opaque, controlled by OpenAI | A markdown file YOU own and edit         |
| **Personality**     | Generic                               | YOUR rules, YOUR voice (SOUL.md)         |
| **Scheduled tasks** | Impossible                            | Cron jobs run while you sleep            |
| **Privacy**         | Your data trains their models         | Runs on your machine, stays private      |
| **Cost**            | $20/mo subscription                   | ~$5-15/mo in API credits (pay per use)   |
| **Extensible**      | Closed ecosystem                      | Add email, iMessage, WhatsApp, calendar  |

**The bottom line:** ChatGPT is a tool you go to. OpenClaw is an assistant that comes to you.

## Use it right now

Everything below works with what you just set up — no extra integrations needed.

### Things ChatGPT can't do (proactive + scheduled)

- **Morning briefing every day at 8am:** weather, news, your reminders — waiting on your phone when you wake up
- **Study accountability:** "Ask me what I studied today. If I didn't, roast me." — runs every night at 9pm
- **Exam reminders:** "In 3 days, remind me my CS 341 midterm is tomorrow" — fires once, then deletes itself
- **Daily motivation:** "Send me one thing I should be grateful for today" — every morning
- **Research digest:** "Every Monday, search for new AI papers on [topic] and summarize the top 3"

### Things that are better on Telegram than a browser tab

- "Summarize this paper in 3 bullets" — paste text or a URL, get the answer in your messaging app
- "Quiz me on [topic]. 5 questions. Grade my answers." — study on the go, from your phone
- "Is it true that [claim]? Search the web and verify." — instant fact-checking in conversation
- "Draft an email to Prof. Smith about [request]" — agent writes it, you copy-paste into Gmail
- "Prep me for my interview tomorrow — ask me technical questions" — practice anywhere

### Things that get better over time (memory)

- Tell it your course schedule, and it references it in every future conversation
- Tell it your study habits, and it adapts its accountability check-ins
- Tell it your career goals, and it tailors advice and job search results
- Every fact it learns about you stays in MEMORY.md — you can read it, edit it, seed it

## Go further: add more integrations

For setup instructions on any of these channels, see [github.com/Hamza-Mos/openclaw-setup](https://github.com/Hamza-Mos/openclaw-setup).

| Integration          | What it unlocks                                                      | What you need                                                                                       |
| -------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **Gmail + Calendar** | "Check my email — anything urgent?" / "What's on my schedule today?" | Google Cloud OAuth ([setup guide, Part 3](https://github.com/Hamza-Mos/openclaw-setup))             |
| **iMessage**         | "Any texts I need to reply to?" / "Draft a reply to Mom"             | Mac + BlueBubbles app ([setup guide, Part 3](https://github.com/Hamza-Mos/openclaw-setup))          |
| **WhatsApp**         | "Summarize what I missed in my study group"                          | Secondary phone number + wacli ([setup guide, Part 3](https://github.com/Hamza-Mos/openclaw-setup)) |
| **Twitter/X**        | "What's trending in AI?" / "Draft a tweet about [topic]"             | Twitter dev account + xurl ([setup guide, Part 3](https://github.com/Hamza-Mos/openclaw-setup))     |

Docs: [docs.openclaw.ai](https://docs.openclaw.ai)

## After the workshop: switch to your own API keys

The workshop keys will be deactivated after today. To keep your agent running, swap in your own keys:

1. Get your own Anthropic API key at [console.anthropic.com](https://console.anthropic.com/) (add ~$5 in credits to start)
2. Run the configuration wizard:
   ```bash
   openclaw configure
   ```
3. When it asks for the API key, paste your new one
4. Restart:
   ```bash
   openclaw gateway restart
   ```

You can also edit the config file directly:

```bash
openclaw config set anthropicApiKey "sk-ant-your-new-key-here"
openclaw gateway restart
```

> To verify your config is valid: `openclaw config validate`
