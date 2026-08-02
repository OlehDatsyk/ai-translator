# 🧭 INSTRUCTION.md - Complete Beginner's Guide to Running AI Translator

This guide assumes you have **never** used Python, Visual Studio Code, Git, a terminal, a virtual environment, or an API before. Every step is spelled out. Just follow along in order - you don't need to understand everything to get the app running.

By the end, you'll have a working AI-powered translation web app running on your own computer.

---

## Table of Contents

1. [What This App Is](#1-what-this-app-is)
2. [What You'll Need](#2-what-youll-need)
3. [Installing Python](#3-installing-python)
4. [Installing Git (optional but recommended)](#4-installing-git-optional-but-recommended)
5. [Installing Visual Studio Code](#5-installing-visual-studio-code)
6. [Required VS Code Extensions](#6-required-vs-code-extensions)
7. [Opening the Project](#7-opening-the-project)
8. [What Is a Terminal?](#8-what-is-a-terminal)
9. [What Is a Virtual Environment, and Why Do I Need One?](#9-what-is-a-virtual-environment-and-why-do-i-need-one)
10. [Creating the Virtual Environment](#10-creating-the-virtual-environment)
11. [Activating the Virtual Environment](#11-activating-the-virtual-environment)
12. [Installing Dependencies](#12-installing-dependencies)
13. [What Is an API, and What Is an API Key?](#13-what-is-an-api-and-what-is-an-api-key)
14. [Getting Your OpenAI API Key](#14-getting-your-openai-api-key)
15. [Creating the .env File](#15-creating-the-env-file)
16. [Running the Application](#16-running-the-application)
17. [Using Every Feature of the App](#17-using-every-feature-of-the-app)
18. [Testing That Everything Works](#18-testing-that-everything-works)
19. [Troubleshooting](#19-troubleshooting)
20. [FAQ](#20-faq)
21. [Common Mistakes Beginners Make](#21-common-mistakes-beginners-make)
22. [Security Recommendations](#22-security-recommendations)
23. [Next Learning Steps](#23-next-learning-steps)

---

## 1. What This App Is

**AI Translator** is a small website that runs on your own computer. You type text into a box, pick a language, click "Translate," and it uses OpenAI's AI models to translate your text - while also detecting what language you originally wrote in.

It's built with:
- **Python** - the programming language that powers the "backend" (the part you don't see, which talks to the AI).
- **Flask** - a lightweight Python framework used to run a small web server on your computer.
- **HTML/CSS/JavaScript** - what makes up the actual webpage you see and click on in your browser.

You don't need to know how to code to run it - just follow the steps below.

---

## 2. What You'll Need

- A Windows, macOS, or Linux computer.
- An internet connection.
- About 20-30 minutes for first-time setup.
- An OpenAI account (free to create; using the AI does cost a small amount of money per translation - usually fractions of a cent for short text, covered in [Section 14](#14-getting-your-openai-api-key)).

---

## 3. Installing Python

Python is the programming language this app is written in. Your computer almost certainly doesn't have the right version pre-installed, so let's install it.

1. Go to **[python.org/downloads](https://www.python.org/downloads/)**.
2. Click the big **Download Python** button (it will detect your operating system automatically). Get version **3.10 or newer**.
3. Run the installer you downloaded.
   - **On Windows:** On the very first installer screen, **check the box that says "Add python.exe to PATH"** (or "Add Python to PATH") at the bottom, **before** clicking "Install Now." This step is easy to miss and is the #1 cause of setup problems for beginners.
   - **On macOS:** Run through the installer normally, clicking "Continue" and "Install" as prompted.
4. Once installation finishes, verify it worked:
   - Open a terminal (see [Section 8](#8-what-is-a-terminal) if you don't know how yet).
   - Type: `python --version` and press Enter.
   - If that doesn't work, try: `python3 --version`.
   - You should see something like `Python 3.11.4`. If you instead see an error like "command not found" or "'python' is not recognized," Python either isn't installed or wasn't added to PATH - reinstall and make sure to check that box.

---

## 4. Installing Git (optional but recommended)

Git is a tool for tracking changes to code and is commonly used to upload projects to GitHub. **You do not need Git to run this app locally** - it's only needed if you want to publish this project to GitHub or clone it from there.

1. Go to **[git-scm.com/downloads](https://git-scm.com/downloads)**.
2. Download the installer for your operating system.
3. Run it, accepting the default options throughout (the defaults are fine for beginners).
4. Verify it worked by opening a terminal and typing: `git --version`.

---

## 5. Installing Visual Studio Code

Visual Studio Code (VS Code) is a free code editor - it's where you'll open, view, and run this project.

1. Go to **[code.visualstudio.com](https://code.visualstudio.com/)**.
2. Click **Download**.
3. Run the installer, accepting the default settings.
4. Launch Visual Studio Code once installation finishes.

---

## 6. Required VS Code Extensions

Extensions add extra features to VS Code. You need one:

1. Open VS Code.
2. Click the **Extensions** icon in the left-hand sidebar (it looks like four small squares, or press `Ctrl+Shift+X` on Windows/Linux, `Cmd+Shift+X` on Mac).
3. In the search box, type **Python**.
4. Find the one published by **Microsoft** (it will usually be the first result, and it's the official one).
5. Click **Install**.

This gives VS Code the ability to understand Python files, run them, and help you select the right Python environment (explained in [Section 9](#9-what-is-a-virtual-environment-and-why-do-i-need-one)).

---

## 7. Opening the Project

1. Unzip the project folder somewhere easy to find, like your Desktop or Documents folder. You should end up with a folder named `ai-translator` containing files like `app.py`, `config.py`, `README.md`, etc.
2. Open **Visual Studio Code**.
3. Go to the top menu: **File -> Open Folder...**
4. Navigate to and select the `ai-translator` folder (the one that directly contains `app.py`).
5. Click **Select Folder** (Windows) or **Open** (Mac).
6. VS Code will reload with the project's files listed in the left-hand **Explorer** sidebar.

---

## 8. What Is a Terminal?

A **terminal** (also called a "command line" or "console") is a text-based way of giving your computer instructions, instead of clicking buttons. You'll use it to set up and run this app.

To open a terminal **inside VS Code** (the easiest way):

- Go to the top menu: **Terminal -> New Terminal**
- Or press `` Ctrl+` `` (Windows/Linux) or `` Cmd+` `` (Mac) - that's the backtick key, usually above the Tab key.

A panel will open at the bottom of VS Code with a blinking cursor, already pointed at your project folder. You type commands here and press **Enter** to run them.

---

## 9. What Is a Virtual Environment, and Why Do I Need One?

A **virtual environment** (often shortened to "venv") is an isolated, self-contained copy of Python just for this one project. It keeps the specific package versions this app needs (like `Flask` and `openai`) separate from anything else installed on your computer, and separate from other Python projects you might create in the future.

Without one, installing packages for different projects can eventually conflict with each other. Using a virtual environment for every Python project is standard best practice - it costs a couple of extra commands and saves you from confusing bugs later.

---

## 10. Creating the Virtual Environment

In the VS Code terminal (opened in [Section 8](#8-what-is-a-terminal)), make sure you're in the `ai-translator` folder (it should already show this in the terminal prompt), then run:

**Windows:**
```powershell
python -m venv venv
```

**macOS / Linux:**
```bash
python3 -m venv venv
```

This creates a new folder named `venv` inside your project. This is normal - it's already excluded from Git via `.gitignore`, so it won't clutter any future GitHub upload. Give it a few seconds to finish; it produces no output when successful.

---

## 11. Activating the Virtual Environment

"Activating" tells your terminal to use this project's isolated Python instead of your computer's main Python. You need to do this **every time** you open a new terminal to work on this project.

**Windows (PowerShell - the default VS Code terminal):**
```powershell
venv\Scripts\Activate.ps1
```

> If you see an error mentioning "running scripts is disabled on this system," run this command once, then try activating again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> Type `Y` and press Enter if prompted.

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

**How do you know it worked?** Your terminal prompt will now show `(venv)` at the very beginning of the line. VS Code may also pop up a message asking if you want to use this environment for the workspace - click **Yes**.

---

## 12. Installing Dependencies

"Dependencies" are the external packages this project relies on to work (listed in `requirements.txt`). With your virtual environment **active** (you should see `(venv)` in your prompt), run:

```bash
pip install -r requirements.txt
```

This downloads and installs:
- **Flask** - runs the local web server.
- **openai** - the official OpenAI SDK, used to talk to the translation AI.
- **python-dotenv** - reads your secret API key from a `.env` file instead of hardcoding it.

You'll see progress text scroll by. When it returns to a normal prompt without errors, you're done.

---

## 13. What Is an API, and What Is an API Key?

An **API** (Application Programming Interface) is how one piece of software talks to another over the internet. This app doesn't do the translation itself - it sends your text to OpenAI's servers, and OpenAI's AI model sends back the translated text.

An **API key** is a private password-like string that identifies *you* (or your account) to OpenAI, so they know who to bill and who's making the request. Anyone who has your API key can use your OpenAI account and run up charges on it - treat it like a password. Never share it, post it publicly, or commit it to GitHub.

---

## 14. Getting Your OpenAI API Key

1. Go to **[platform.openai.com](https://platform.openai.com/)** and sign up, or log in if you already have an account.

   > Note: this is a **separate** account/product from a ChatGPT Plus subscription - API usage is billed separately, even if you use the same login.
2. Click your profile icon in the top-right corner and choose **View API keys**, or go directly to **[platform.openai.com/api-keys](https://platform.openai.com/api-keys)**.
3. Click **Create new secret key**. Give it a name like `ai-translator` so you remember what it's for.
4. Click **Create secret key**. A long string starting with `sk-` will appear.
5. **Copy it immediately and save it somewhere safe** - OpenAI will only show you the full key once. If you lose it, you'll need to create a new one.
6. Make sure your account has billing enabled: go to **Settings -> Billing** and add a payment method. Short translations typically cost a very small fraction of a cent each with the default model, but the API will not work at all without billing set up.

---

## 15. Creating the .env File

The `.env` file is where your API key and other settings live - it is **never** shared or uploaded anywhere (it's excluded via `.gitignore`).

1. In the VS Code Explorer sidebar, find the file `.env.example`.
2. Make a copy of it named exactly `.env`. Easiest way - in the terminal, run:
   - **Windows:** `copy .env.example .env`
   - **macOS/Linux:** `cp .env.example .env`
3. Open the new `.env` file (double-click it in the Explorer sidebar).
4. Find this line:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
5. Replace `sk-your-api-key-here` with the real key you copied in [Section 14](#14-getting-your-openai-api-key), so it looks like:
   ```
   OPENAI_API_KEY=sk-abc123...(your real key)
   ```
6. Save the file (`Ctrl+S` / `Cmd+S`).

You can leave every other line in `.env` as-is - the defaults work out of the box.

---

## 16. Running the Application

With your virtual environment active (`(venv)` visible in the terminal) and dependencies installed, run:

```bash
python app.py
```

You should see log output ending with something like:

```
* Running on http://127.0.0.1:5000
```

Now open your web browser and go to:

```
http://127.0.0.1:5000
```

You should see the AI Translator page. 🎉

**To stop the app**, click back into the terminal and press `Ctrl+C`.

---

## 17. Using Every Feature of the App

- **Source language dropdown (left):** choose the language your text is written in, or leave it on **"Auto Detect"** to let the AI figure it out.
- **Target language dropdown (right):** choose the language you want to translate into.
- **⇄ swap button:** swaps the source and target languages (and swaps any text already in the boxes). Note: you must pick a specific source language before swapping - you can't swap *from* "Auto Detect."
- **Left text box:** type or paste your text (up to 5,000 characters). A counter below shows how many characters you've used.
- **Clear button:** empties the input box and any translation shown.
- **Creativity (temperature) slider:** controls how literal vs. creative the translation is. Lower = more literal/consistent; higher = more natural/flexible phrasing.
- **Translate button:** sends your text to the AI. You can also press `Ctrl+Enter` (`Cmd+Enter` on Mac) while typing in the text box instead of clicking the button.
- **Right text box:** shows the translated result once it comes back. If you used Auto Detect, a small badge appears showing what source language was detected.
- **📋 Copy button:** copies the translated text to your clipboard.
- **History panel:** every successful translation is automatically saved here (in your browser, not on any server). Click **Reuse** on a past entry to load it back into the boxes, **Delete** to remove a single entry, or **Clear all** to wipe the whole history.
- **🌙/☀️ dark mode toggle** (top-right corner): switches between light and dark themes. Your choice is remembered the next time you open the app.

---

## 18. Testing That Everything Works

Once the app is running (Section 16), try this simple test:

1. Leave the source language on **Auto Detect**.
2. Set the target language to **French**.
3. In the left box, type: `Good morning! How are you today?`
4. Click **Translate**.
5. You should see a French translation appear on the right (e.g., something like *"Bonjour ! Comment allez-vous aujourd'hui ?"*), along with a badge reading **"Detected: English."**

If that works, your setup is complete and correct.

---

## 19. Troubleshooting

**`ModuleNotFoundError: No module named 'flask'` (or `openai`, `dotenv`)**
Your virtual environment isn't active, or dependencies weren't installed into it.
- Check that `(venv)` appears in your terminal prompt.
- Re-run `pip install -r requirements.txt`.
- In VS Code, press `Ctrl+Shift+P` (`Cmd+Shift+P`), type "Python: Select Interpreter," and choose the one inside `./venv`.

**`RuntimeError: OPENAI_API_KEY is not set`**
- Confirm you created a file literally named `.env` (not `.env.example`) in the project's root folder.
- Confirm it contains `OPENAI_API_KEY=sk-...` with your real key, no extra quotes or spaces.
- Restart the app (`Ctrl+C`, then `python app.py` again) - `.env` is only read at startup.

**`openai.AuthenticationError` or a 401 error in the terminal**
Your API key is invalid, expired, or revoked. Generate a new one at platform.openai.com/api-keys and update `.env`.

**`openai.RateLimitError` / "too many requests"**
You've hit your usage limit. Wait a minute, or check your usage/billing settings at platform.openai.com.

**Translation fails with a network or "502" error**
- Check your internet connection.
- Look at the terminal running `python app.py` for a detailed error message.
- Confirm your OpenAI account has an active payment method.

**"Address already in use" / port 5000 busy**
Something else on your computer is already using port 5000 (common on Macs, due to AirPlay Receiver). Either close that other program, or open `.env` and change:
```
FLASK_PORT=5050
```
then restart the app and visit `http://127.0.0.1:5050` instead.

**PowerShell won't let me activate the virtual environment**
Run this once, then try activating again:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Dark mode or history doesn't save between visits**
These are stored in your browser's local storage. If you're in a private/incognito window, or have site data disabled, they'll reset each session - this is expected, not a bug.

**Nothing happens when I click "Translate"**
Open your browser's developer console (press `F12`) and check for red error messages. Also confirm the app is being run from the project's root folder (not from inside a subfolder).

---

## 20. FAQ

**Do I have to pay to use this app?**
Yes, indirectly - OpenAI charges per API request based on how much text you send. Costs are typically very small (fractions of a cent for short translations with the default model), but you do need a payment method on file with OpenAI.

**Can I use this without an OpenAI account?**
No - the app requires a valid OpenAI API key to function at all; it won't start without one.

**Is my translated text stored anywhere?**
Your translation history is stored only in your own browser (via `localStorage`) - it is not saved on any server or database. Clearing your browser data will erase it.

**Can other people on the internet use my running app?**
Not by default. It runs on `127.0.0.1` (your own computer only) and isn't accessible from outside your machine unless you specifically configure and deploy it that way.

**Do I need to keep the terminal window open while using the app?**
Yes - closing the terminal (or pressing `Ctrl+C`) stops the web server, and the page will stop working.

**Can I run this on my phone?**
Not directly - it's designed to run on a computer. You could access it from a phone's browser only if you deploy it to a publicly reachable server, which is a more advanced setup not covered here.

---

## 21. Common Mistakes Beginners Make

- **Forgetting to activate the virtual environment** before installing packages or running the app (you'll get `ModuleNotFoundError`s).
- **Editing `.env.example` instead of `.env`** - the app only reads `.env`, never the example file.
- **Forgetting to save `.env`** after pasting in the API key.
- **Not checking "Add Python to PATH"** during Python installation on Windows.
- **Pasting the API key with extra spaces or quotes** around it.
- **Closing the terminal and expecting the app to still work** in the browser.
- **Running `python app.py` from the wrong folder** (make sure your terminal is inside the `ai-translator` folder itself).

---

## 22. Security Recommendations

- **Never share your `.env` file or your API key** with anyone, in a screenshot, in a chat message, or in a public repository.
- **Never commit `.env` to Git/GitHub.** It's already excluded by `.gitignore`, but always double-check before pushing if you ever modify that file.
- **Set a spending limit** on your OpenAI account (Settings -> Billing -> Usage limits) so a bug or unexpected usage can't produce a surprise bill.
- **Rotate your API key** (create a new one and delete the old one) if you ever suspect it's been exposed.
- If you ever deploy this app somewhere publicly reachable (not just your own computer), do not use the default `FLASK_SECRET_KEY` value - set your own random string in `.env`, and see `PROJECT_REVIEW.md` for further hardening recommendations before going public.

---

## 23. Next Learning Steps

If this is your first Python/web project, here are good next things to learn, roughly in order:

1. **Basic Python syntax** - variables, functions, loops, if statements (free resources: [python.org's official tutorial](https://docs.python.org/3/tutorial/), [W3Schools Python](https://www.w3schools.com/python/)).
2. **How HTTP works** - what a request and response are, what JSON is (this app uses both constantly).
3. **Flask basics** - read through `app.py` in this project alongside the [official Flask Quickstart](https://flask.palletsprojects.com/en/latest/quickstart/).
4. **Git and GitHub basics** - how to track changes and publish a project (try [GitHub's own guide](https://docs.github.com/en/get-started)).
5. **Writing your first automated test** - try adding a simple `pytest` test for one function in `translator.py`.
6. **Environment variables and secrets management** - you're already using this via `.env`; understanding *why* it matters is a great next step.
7. **Basic web deployment** - once comfortable, look into deploying a Flask app (e.g., via Render, Railway, or Fly.io) to make it reachable outside your own computer.

Good luck - and if something breaks, re-read the terminal output carefully. Both Flask and the OpenAI SDK print specific, descriptive error messages that usually point straight at the fix.
