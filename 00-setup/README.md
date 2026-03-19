# 00 - Setup

About 10 minutes. **You do not need Python installed** because `uv` downloads it for you.

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

Install Node.js and git:

**macOS**

Install the LTS version from [nodejs.org](https://nodejs.org/). If macOS asks to install developer tools later, click **Install**.

**Windows (PowerShell)**

```powershell
winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
winget install Git.Git --accept-source-agreements --accept-package-agreements
```

Then reopen your terminal and check:

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

You'll receive the keys at the workshop.

**macOS / Linux**

```bash
cp .env.example .env
```

**Windows (PowerShell)**

```powershell
Copy-Item .env.example .env
```

Open `.env` in your favourite code editor and replace the placeholders with your real keys.

## 7. Verify it works

```bash
uv run 01-what-are-agents/talk_to_agent.py
```

If you see `You:` waiting for input, you're ready.

## Troubleshooting

- `uv`, `node`, or `git` not found: close the terminal and open a new one.
- `AuthenticationError`: check that your `.env` file contains the real keys.
- `No module named 'openai'`: use `uv run`, not `python`.
