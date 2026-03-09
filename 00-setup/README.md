# 00 - Setup

Get your environment ready. This takes about 10 minutes.

## Prerequisites

You need **two things** installed before the workshop:

| Tool | What it's for | Check if installed |
|------|--------------|-------------------|
| **Python 3.9+** | Exercises in Parts 1-2 | `python3 --version` |
| **Node.js 18+** | OpenClaw agent in Part 3 | `node --version` |

## Step 1: Python

Check your version:

```bash
python3 --version
```

If you don't have it, install it from [python.org/downloads](https://www.python.org/downloads/).

**On macOS:** Python 3 usually comes pre-installed. If not: `brew install python3`

**On Windows:** Download from python.org. During installation, check "Add Python to PATH."

## Step 2: Node.js

Check your version:

```bash
node --version
```

If you don't have it or it's below 18, install from [nodejs.org](https://nodejs.org/) (use the LTS version).

**On macOS:** `brew install node`

**On Windows:** Download the LTS installer from nodejs.org.

## Step 3: Clone the repo

```bash
git clone https://github.com/Hamza-Mos/agents-workshop.git
cd agents-workshop
```

## Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

This installs two packages: `openai` (the API client) and `python-dotenv` (loads your API key from a file).

If `pip` doesn't work, try `pip3` or `python3 -m pip install -r requirements.txt`.

## Step 5: API keys

At the workshop, you'll receive API keys. You don't need to create any accounts or pay for anything.

**Two keys are used in this workshop:**

| Key | What it's for | How to configure |
|-----|--------------|-----------------|
| **OpenAI API key** | Python exercises (Parts 1-2, Track B) | Paste into `.env` file |
| **Anthropic API key** | OpenClaw agent (Track A - the main track) | Entered during `openclaw configure` |

For the Python exercises, set up your `.env` file:

```bash
cp .env.example .env
```

Open `.env` in any text editor and paste your OpenAI key:

```
OPENAI_API_KEY=sk-...your-key-here...
```

The Anthropic key for Track A gets configured separately when you run `openclaw configure` in Part 3.

**After the workshop**, if you want to keep using the exercises, you can create your own keys:
- OpenAI key: [platform.openai.com](https://platform.openai.com)
- Anthropic key: [console.anthropic.com](https://console.anthropic.com)

## Step 6: Verify it works

```bash
python3 01-what-are-agents/talk_to_agent.py
```

If you see `You:` waiting for your input, you're good. Type "hello" and press Enter.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `python3: command not found` | Install Python from python.org |
| `No module named 'openai'` | Run `pip install -r requirements.txt` |
| `AuthenticationError` | Check your `.env` file has the right API key |
| `RateLimitError` | The shared key is getting too many requests. Wait a few seconds and try again. |
| Something else | Check the [troubleshooting section](../README.md) or search the error message online |

---

Ready? Go to [01 - What Are Agents?](../01-what-are-agents/)
