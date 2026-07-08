# 🌐 AI Translator

A full-stack AI-powered translation web application built with **Python**,
**Flask**, and the **OpenAI Responses API**. It supports multi-language
translation, automatic source-language detection, translation history, dark
mode, and a clean, responsive UI.

This README is written for **complete beginners**. Even if you have never
run a Python project before, follow the steps below in order and you will
have the app running locally in Visual Studio Code.

---

## Table of Contents

1. [Features](#1-features)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [Prerequisites](#4-prerequisites)
5. [Step-by-Step Setup in Visual Studio Code](#5-step-by-step-setup-in-visual-studio-code)
6. [Getting an OpenAI API Key](#6-getting-an-openai-api-key)
7. [Configuring Environment Variables](#7-configuring-environment-variables)
8. [Running the Application](#8-running-the-application)
9. [Using the App](#9-using-the-app)
10. [How the AI Integration Works](#10-how-the-ai-integration-works)
11. [Folder & File Explanation](#11-folder--file-explanation)
12. [Troubleshooting](#12-troubleshooting)
13. [Future Improvements](#13-future-improvements)
14. [License](#14-license)

---

## 1. Features

- 🔤 Translate text between 30+ languages
- 🧭 Auto language detection (leave source as "Auto Detect")
- 🔃 One-click language swap
- 📋 One-click copy of the translated text
- 🕓 Local translation history (persisted in your browser)
- 🌗 Dark mode with saved preference
- 📱 Fully responsive design (desktop, tablet, mobile)
- 🧠 Demonstrates key GenAI engineering concepts:
  - **System Prompt** — a fixed instruction that defines the model's role
  - **Prompt Engineering** — structured, explicit user prompts
  - **Structured Output** — JSON Schema-enforced responses via the
    OpenAI Responses API
  - **Temperature control** — adjustable via a UI slider
  - **JSON parsing** — safe, validated parsing of model output

---

## 2. Tech Stack

| Layer          | Technology                              |
|----------------|-------------------------------------------|
| Backend        | Python 3.10+, Flask 3                    |
| AI Provider    | OpenAI Responses API (`openai` Python SDK) |
| Frontend       | HTML5, CSS3 (custom properties), vanilla JavaScript |
| Config/Secrets | `python-dotenv`, environment variables    |

No frontend build tools (React/Webpack/etc.) are required — everything
runs directly in the browser.

---

## 3. Project Structure

```
ai-translator/
│
├── app.py                 # Flask application entrypoint & routes
├── translator.py          # OpenAI Responses API integration (core AI logic)
├── config.py               # Environment-based configuration loader
│
├── templates/
│   └── index.html          # Main HTML page (Jinja2 template)
│
├── static/
│   ├── css/
│   │   └── style.css       # Styling, responsive layout, dark mode
│   └── js/
│       └── script.js       # Frontend logic (fetch calls, history, UI state)
│
├── requirements.txt        # Python dependencies
├── .env.example             # Template for required environment variables
├── .gitignore                # Files/folders excluded from Git
└── README.md                 # This file
```

---

## 4. Prerequisites

Before you start, make sure you have the following installed:

1. **Visual Studio Code** — [Download here](https://code.visualstudio.com/)
2. **Python 3.10 or newer**
   - Download from [python.org/downloads](https://www.python.org/downloads/)
   - ⚠️ On Windows, during installation, **check the box** that says
     **"Add Python to PATH"** before clicking Install.
3. **The VS Code Python extension**
   - Open VS Code → click the Extensions icon in the left sidebar (or press
     `Ctrl+Shift+X` / `Cmd+Shift+X`) → search for **"Python"** (by
     Microsoft) → click **Install**.
4. **An OpenAI account and API key** — see [Section 6](#6-getting-an-openai-api-key).
5. **Git** (optional, only needed if you plan to clone/push to a repository)
   — [Download here](https://git-scm.com/downloads)

### Verify Python is installed correctly

Open a terminal (in VS Code: **Terminal → New Terminal**, or `` Ctrl+` ``)
and run:

```bash
python --version
```

or, on some macOS/Linux systems:

```bash
python3 --version
```

You should see something like `Python 3.11.4`. If you see an error like
`command not found`, revisit step 2 above and make sure Python was added to
your PATH.

---

## 5. Step-by-Step Setup in Visual Studio Code

### Step 1 — Open the project folder

1. Launch **Visual Studio Code**.
2. Go to **File → Open Folder...**
3. Select the `ai-translator` folder (the one containing `app.py`).
4. VS Code will reload with the project open in the Explorer sidebar.

### Step 2 — Open the integrated terminal

Go to **Terminal → New Terminal** in the VS Code menu bar (or press
`` Ctrl+` ``). A terminal panel will open at the bottom, already pointed at
your project folder.

### Step 3 — Create a virtual environment

A virtual environment keeps this project's Python packages isolated from
the rest of your system. In the terminal, run:

**Windows:**
```powershell
python -m venv venv
```

**macOS / Linux:**
```bash
python3 -m venv venv
```

This creates a `venv/` folder inside your project (already excluded from
Git via `.gitignore`).

### Step 4 — Activate the virtual environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```
> If you get an error about "running scripts is disabled on this system",
> run this once, then try activating again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

When activated, you'll see `(venv)` appear at the start of your terminal
prompt. VS Code may also prompt you: *"We noticed a new environment has
been created. Do you want to select it for the workspace folder?"* — click
**Yes**.

You can also select the interpreter manually:
1. Press `Ctrl+Shift+P` (`Cmd+Shift+P` on Mac) to open the Command Palette.
2. Type **"Python: Select Interpreter"** and press Enter.
3. Choose the interpreter located at `./venv/...`.

### Step 5 — Install dependencies

With the virtual environment active, run:

```bash
pip install -r requirements.txt
```

This installs:
- `Flask` — the web framework
- `openai` — the official OpenAI Python SDK (Responses API client)
- `python-dotenv` — loads variables from a `.env` file

### Step 6 — Configure your environment variables

Continue to [Section 7](#7-configuring-environment-variables) below.

---

## 6. Getting an OpenAI API Key

1. Go to [https://platform.openai.com/](https://platform.openai.com/) and
   sign up or log in.
2. Click your profile icon (top-right) → **View API keys**, or go directly
   to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
3. Click **Create new secret key**, give it a name (e.g. "ai-translator"),
   and click **Create secret key**.
4. **Copy the key immediately** — OpenAI will only show it to you once.
   It looks like `sk-...`.
5. Make sure your OpenAI account has billing set up (Settings → Billing)
   since API usage is billed separately from ChatGPT Plus subscriptions.

Keep this key private. Never paste it into chat messages, screenshots, or
commit it to a public repository.

---

## 7. Configuring Environment Variables

1. In the VS Code Explorer, find the file named **`.env.example`**.
2. Duplicate it and rename the copy to **`.env`**:
   - Easiest way: in the integrated terminal, run:
     - **Windows:** `copy .env.example .env`
     - **macOS/Linux:** `cp .env.example .env`
3. Open the new `.env` file and replace the placeholder with your real key:

   ```env
   OPENAI_API_KEY=sk-your-real-key-here
   ```

4. (Optional) Adjust other values such as `OPENAI_MODEL` or
   `DEFAULT_TEMPERATURE` if desired — the defaults work out of the box.
5. Save the file (`Ctrl+S` / `Cmd+S`).

> ✅ The `.env` file is listed in `.gitignore`, so it will **never** be
> committed to version control. `config.py` reads these values using
> `python-dotenv` — no secrets are ever hardcoded in the source code.

---

## 8. Running the Application

With your virtual environment active and dependencies installed:

```bash
python app.py
```

You should see log output similar to:

```
2026-07-08 10:00:00 | INFO     | werkzeug | * Running on http://127.0.0.1:5000
```

Now open your browser and go to:

```
http://127.0.0.1:5000
```

You should see the AI Translator interface. 🎉

To stop the server, click into the terminal and press `Ctrl+C`.

### Running with the VS Code Debugger (optional but recommended)

1. Click the **Run and Debug** icon in the left sidebar (or press
   `Ctrl+Shift+D`).
2. Click **create a launch.json file** if prompted, and choose **Python →
   Flask**, or simply click **Run and Debug** with `app.py` open and
   active — VS Code will run it with the "Python File" configuration.
3. Set breakpoints in `app.py` or `translator.py` by clicking to the left
   of a line number, then trigger a translation from the browser to step
   through the code.

---

## 9. Using the App

1. **Choose a source language** (or leave it on "Auto Detect").
2. **Choose a target language** from the second dropdown.
3. Type or paste text into the left text box (up to 5,000 characters).
4. (Optional) Adjust the **temperature slider** — lower values produce
   more literal, consistent translations; higher values allow more
   creative phrasing.
5. Click **Translate** (or press `Ctrl+Enter` / `Cmd+Enter` while focused
   in the text box).
6. The translated text appears on the right, along with the detected
   source language badge (if Auto Detect was used).
7. Use **📋 Copy** to copy the result, or **⇄** to swap the languages and
   translated text.
8. Every successful translation is saved to the **History** panel below
   (stored in your browser's `localStorage`). Click **Reuse** on any item
   to load it back into the editor, or **Delete**/**Clear all** to remove
   entries.
9. Toggle the 🌙/☀️ icon in the top-right corner to switch between light
   and dark mode — your preference is remembered on your next visit.

### Example

- Source: `Auto Detect`
- Target: `French`
- Input: `Good morning! How are you today?`
- Output: `Bonjour ! Comment allez-vous aujourd'hui ?`
- Detected badge: `Detected: English`

---

## 10. How the AI Integration Works

This project is designed to clearly demonstrate five core GenAI
engineering concepts, all implemented in **`translator.py`**:

### System Prompt
A constant `SYSTEM_PROMPT` string defines the model's persistent role
("LinguaBridge", a professional translation engine) and hard rules (never
add commentary, preserve formatting, always respond in the required JSON
schema, etc.). This is sent as the `system` role message on every request.

### Prompt Engineering
The `_build_user_prompt()` method dynamically constructs a clear, explicit
user instruction: it states the exact task, whether the source language is
known or must be auto-detected, formatting rules, and wraps the input text
in clear delimiters (`-----BEGIN TEXT-----` / `-----END TEXT-----`) so the
model can't confuse instructions with content.

### Structured Output
`TRANSLATION_JSON_SCHEMA` is a strict JSON Schema passed to the OpenAI
Responses API via:

```python
text={
    "format": {
        "type": "json_schema",
        "name": "translation_result",
        "schema": TRANSLATION_JSON_SCHEMA,
        "strict": True,
    }
}
```

This forces the model to always return a JSON object with exactly the
fields `translated_text`, `detected_source_language`,
`source_language_code`, `confidence`, and `notes` — never free-form prose.

### Temperature
The `temperature` parameter (0.0–2.0) is passed directly to
`client.responses.create(...)`. It is:
- configurable via `DEFAULT_TEMPERATURE` in `.env`,
- overridable per-request via the UI slider (sent in the POST body),
- clamped defensively in both `app.py` and `translator.py`.

### JSON Parsing
Even though Structured Outputs guarantees schema conformance from the
model, `_parse_response()` still explicitly runs `json.loads()`, checks
for required fields, and validates types — defensive programming that
protects the app if the API ever returns something unexpected, and makes
the parsing logic explicit and testable.

---

## 11. Folder & File Explanation

| Path                     | Purpose |
|---------------------------|---------|
| `app.py`                   | Creates the Flask app, defines HTTP routes (`/`, `/api/translate`, `/api/languages`), validates input, and returns JSON responses. Contains no AI logic itself. |
| `translator.py`            | All OpenAI Responses API logic: system prompt, prompt construction, structured output schema, the API call itself, and response parsing/validation. |
| `config.py`                 | Loads and validates environment variables (`.env`) into a single immutable `AppConfig` object used throughout the app. |
| `templates/index.html`      | The Jinja2-rendered HTML page: language dropdowns, text panels, controls, and history section. |
| `static/css/style.css`      | All visual styling, including CSS custom properties for light/dark themes and responsive breakpoints. |
| `static/js/script.js`       | Client-side logic: calling the API, rendering results, managing history in `localStorage`, dark mode toggle, swap/copy/clear actions. |
| `requirements.txt`          | Pinned Python package versions needed to run the app. |
| `.env.example`               | Template listing every environment variable the app understands — copy to `.env` and fill in real values. |
| `.gitignore`                  | Prevents secrets (`.env`), virtual environments, caches, and editor files from being committed to Git. |

---

## 12. Troubleshooting

### `ModuleNotFoundError: No module named 'flask'` (or `openai`, `dotenv`)
Your virtual environment is either not activated or dependencies were not
installed into it.
- Confirm `(venv)` appears in your terminal prompt.
- Re-run `pip install -r requirements.txt`.
- In VS Code, confirm the correct interpreter is selected: `Ctrl+Shift+P` →
  "Python: Select Interpreter" → choose the one inside `./venv`.

### `RuntimeError: OPENAI_API_KEY is not set`
- Make sure you created a `.env` file (not just `.env.example`) in the
  project root, and that it contains a real key:
  `OPENAI_API_KEY=sk-...`
- Make sure there are no extra quotes or spaces around the value.
- Restart the Flask server after editing `.env` — environment variables
  are only read on startup.

### `openai.AuthenticationError` / 401 errors in the terminal
- Your API key is invalid, expired, or was revoked. Generate a new one at
  [platform.openai.com/api-keys](https://platform.openai.com/api-keys) and
  update `.env`.

### `openai.RateLimitError` / "too many requests"
- You've hit your OpenAI usage/rate limit. Wait a minute and try again, or
  check your usage/billing at platform.openai.com.

### The page loads but translation fails with a network/502 error
- Check your internet connection.
- Check the terminal running `python app.py` for a detailed logged error
  message — `translator.py` logs the exact OpenAI exception.
- Confirm your OpenAI account has an active payment method if you're on a
  usage-based plan.

### `Address already in use` / port 5000 busy
- Another process is already using port 5000 (common on macOS with
  AirPlay Receiver). Either:
  - Stop the other process, or
  - Change the port in `.env`: `FLASK_PORT=5050`, then restart and visit
    `http://127.0.0.1:5050`.

### PowerShell won't let me activate the virtual environment
- Run this once in PowerShell, then try activating again:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

### Dark mode / history doesn't persist
- These features use browser `localStorage`. If you're in a private/
  incognito window, or have cookies/site data disabled, they will reset
  each session — this is expected browser behavior, not a bug.

### Nothing happens when I click "Translate"
- Open your browser DevTools console (F12) and check for JavaScript
  errors.
- Make sure `static/js/script.js` loaded successfully (check the Network
  tab) — this can fail if the Flask app isn't serving static files
  correctly, which usually means the app isn't running from the project
  root folder.

---

## 13. Future Improvements

Ideas for extending this project further:

- 🔊 Text-to-speech playback of translations
- 🎙️ Speech-to-text input (microphone)
- 📄 File upload translation (`.txt`, `.docx`, `.pdf`)
- 🗂️ Batch/bulk translation of multiple text blocks at once
- 🔐 User accounts with server-side (database-backed) history instead of
  `localStorage`
- 🧪 Automated tests (`pytest`) for `translator.py` and `app.py` routes
- 🚦 Rate limiting / request throttling per user
- 🌍 More granular regional dialect support (e.g. "Spanish (Mexico)" vs
  "Spanish (Spain)")
- 📊 An admin dashboard showing usage/token consumption statistics
- 🧵 Streaming translations token-by-token using the Responses API's
  streaming support, for a more real-time typing effect
- 🐳 A `Dockerfile` for containerized deployment
- ♻️ Response caching for repeated identical translation requests

---

## 14. License

This project is provided as an educational example. You are free to use,
modify, and extend it for personal or commercial projects.

---

**Enjoy building with AI! If you run into an issue not covered above,
re-read the terminal output carefully — Flask and the OpenAI SDK both log
detailed, specific error messages that usually point directly at the fix.**
