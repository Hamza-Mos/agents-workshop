# 00 - Setup

~10 minutes. **You do NOT need Python installed** — uv downloads it for you.

## Step 1: Open a terminal

**macOS:** Press `Cmd + Space` (the key with ⌘), type **Terminal**, press Enter.

**Windows:** Click the Start menu, type **PowerShell**, click **Windows PowerShell**.

> Keep this window open for the whole workshop. You'll type all commands here.

## Step 2: Install VS Code

This is the text editor you'll use to read and edit code during the workshop.

**macOS:**

1. Go to [code.visualstudio.com](https://code.visualstudio.com/), click the big blue download button
2. Open the downloaded zip, and drag **Visual Studio Code** into your **Applications** folder
3. Open VS Code from Applications
4. Press `Cmd + Shift + P` (opens a search bar at the top of VS Code)
5. Type **shell command** and click **Shell Command: Install 'code' command in PATH**

Step 5 is important — without it, `code` won't work in your terminal.

**Windows (PowerShell):**

```powershell
winget install Microsoft.VisualStudioCode --accept-source-agreements --accept-package-agreements
```

If Windows asks "Do you want to allow this app to make changes?", click **Yes**.

**Close your terminal and open a new one.** Then verify:

```bash
code --version
```

## Step 3: Install uv

uv handles Python, packages, and virtual environments — all automatically.

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
winget install astral-sh.uv --accept-source-agreements --accept-package-agreements
```

**Close your terminal and open a new one.** Then verify:

```bash
uv --version
```

## Step 4: Install Telegram

Your agent in Part 3 talks to you through Telegram.

- **iPhone:** App Store → search **Telegram** → Get
- **Android:** Play Store → search **Telegram** → Install
- Create an account (just needs a phone number)

Already have it? Skip this.

## Step 5: Install Node.js and git

**macOS:** Go to [nodejs.org](https://nodejs.org/), click the green **LTS** button, open the downloaded file and follow the prompts. (git gets installed automatically in Step 7 — it may take 5-10 minutes the first time as macOS downloads developer tools.)

**Windows (PowerShell):**

```powershell
winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
winget install Git.Git --accept-source-agreements --accept-package-agreements
```

**Close your terminal and open a new one.** Then verify:

```bash
node --version
git --version
```

## Step 6: Clone the repo

This downloads the workshop files to your computer.

```bash
git clone https://github.com/Hamza-Mos/agents-workshop.git
cd agents-workshop
```

**macOS — if you see a popup** asking to install developer tools, click **Install** and wait (5-10 minutes). Then run the two commands above again.

Now open the project in VS Code:

```bash
code .
```

> From this point on, stay in the `agents-workshop` folder. If you ever close and reopen your terminal, run `cd agents-workshop` to get back.

## Step 7: Install dependencies

```bash
uv sync
```

This automatically downloads Python (if you don't have it), creates a virtual environment, and installs all packages. You'll see some download messages — that's normal.

## Step 8: API keys

You'll receive keys at the workshop — no accounts or payments needed.

Create your `.env` file:

**macOS / Linux:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

Open it in VS Code:

```bash
code .env
```

Replace the placeholder text with your actual keys so it looks like this:

```
OPENAI_API_KEY=sk-proj-abc123...
ANTHROPIC_API_KEY=sk-ant-api03-xyz789...
```

Press `Ctrl+S` (`Cmd+S` on macOS) to save. Both keys will be provided at the workshop.

## Step 9: Verify it works

```bash
uv run 01-what-are-agents/talk_to_agent.py
```

If you see `You:` waiting for input — you're good! Type `hello`, press Enter. Press `Ctrl+C` to exit.

**All workshop commands use `uv run` instead of `python3`.** Same command on every OS.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `uv: command not found` | Close your terminal completely and open a fresh one |
| `code: command not found` | macOS: open VS Code → `Cmd+Shift+P` → type "shell command" → click Install. Windows: close and reopen terminal. |
| `node: command not found` | Close terminal, open a new one |
| `git: command not found` (Windows) | Run `winget install Git.Git --accept-source-agreements --accept-package-agreements`, reopen terminal |
| `winget: command not found` | Open Microsoft Store, search "App Installer", click Update. Reopen terminal. |
| `No module named 'openai'` | Use `uv run script.py` not `python3 script.py` |
| `AuthenticationError` | Check your `.env` file — make sure you replaced the placeholder with your actual key |
| `RateLimitError` | Shared key hit its limit — wait a few seconds, try again |

**Already have Python and prefer pip?** `pip install -r requirements.txt` then use `python3` (macOS/Linux) or `python` (Windows) instead of `uv run`.

---

Ready? Go to [01 - What Are Agents?](../01-what-are-agents/)
