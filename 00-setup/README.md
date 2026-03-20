# 00 - Setup

**You do not need Python installed** because `uv` downloads it for you.

## 1. Open a terminal

Keep one terminal open for the whole workshop.

## 2. Install the tools

Install `uv`:

**macOS / Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**

```powershell
winget install astral-sh.uv --accept-source-agreements --accept-package-agreements
```

Install Node.js (version 22 or newer) and git:

**macOS**

Install from [nodejs.org](https://nodejs.org/) (LTS version). If macOS asks to install developer tools later, click **Install**.

**Windows**

Download and install from [nodejs.org](https://nodejs.org/) (LTS version). **Use the installer, not winget** — it adds Node to your PATH correctly. Then install git:

```powershell
winget install Git.Git --accept-source-agreements --accept-package-agreements
```

**Close and reopen your terminal**, then check:

```bash
uv --version
node --version
git --version
```

## 3. Clone the repo

```bash
git clone https://github.com/Hamza-Mos/agents-workshop.git
cd agents-workshop
```

Open the project in your favourite code editor.

## 4. Install dependencies

```bash
uv sync
```

## 5. Install Telegram

You'll use Telegram in Part 3.

- Install `Telegram` on your phone.
- Create a Telegram account.

## 6. Add API keys

Please go to this website for API keys: **[bit.ly/agents-workshop-keys](https://bit.ly/agents-workshop-keys)**

**macOS / Linux**

```bash
cp .env.example .env
```

**Windows (PowerShell)**

```powershell
Copy-Item .env.example .env
```

Open `.env` in your favourite code editor and paste in all 3 keys (OpenAI, Anthropic, and Brave Search).

> Stuck? Raise your hand — TAs are circulating.

## 7. Verify it works

```bash
uv run 01-what-are-agents/talk_to_agent.py
```

If you see `You:` waiting for input, you're ready.

## Troubleshooting

- **`node` not found (Windows, installed via winget):** winget updates your PATH, but your current terminal doesn't see it. **Close PowerShell and open a new one.** This is a [known winget behavior](https://github.com/microsoft/winget-cli/issues/222). If a fresh terminal still doesn't work, uninstall (`winget uninstall OpenJS.NodeJS.LTS`) and reinstall from [nodejs.org](https://nodejs.org) — the installer handles PATH more reliably.
- **`uv` or `git` not found:** same fix — close and reopen your terminal.
- **`AuthenticationError`:** check that your `.env` file contains the real keys, not the placeholder text.
- **`No module named 'openai'`:** use `uv run`, not `python`.
