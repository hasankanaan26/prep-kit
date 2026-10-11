# 03 Secrets and .env

About 15 minutes. LLM providers give you an API key: a long string that acts as both your
username and password, attached to your credit card. This step is about keeping it safe.

## Where keys live

A key never goes in your code. Code gets shared, pushed to GitHub and pasted into chats,
and bots scan public GitHub for leaked keys within minutes.

Instead, keys live in environment variables: named values that your operating system hands
to each program it starts. Python reads them with `os.getenv("GEMINI_API_KEY")`.

Typing them into the terminal every time gets old, so projects keep them in a file called
`.env`:

```
GEMINI_API_KEY=AIza...your key...
GEMINI_MODEL=gemini-3.5-flash-lite
```

A small package called `python-dotenv` reads that file at startup and turns each line into
an environment variable. Open `code/providers.py` and look for `load_dotenv`: that one
line is all it takes.

## Why .env never reaches GitHub

Projects kept in git have a file called `.gitignore` that lists what git should never
track. This kit has one too: open `prep-kit/.gitignore` and find the line `.env`. Git
won't see that file, so you can't commit it by accident. The course repo you download in
step 08 has the same line.

What a project does ship is `.env.example`: the same file with the values left empty, so
everyone knows which names to fill in.

## Set up the kit's .env

From `prep-kit/`:

```powershell
copy .env.example .env      # macOS/Linux: cp .env.example .env
py code\show_env.py
```

`show_env.py` tells you which keys Python can see without ever printing one. It also
warns about the two usual paste mistakes: a space at the end, or quote marks around the
value. Your keys are all "not set" for now. Step 04 fills them in.

## Four habits

- Never paste a key into code, a chat (including an AI assistant), a screenshot or a slide.
- Set a monthly spending limit on every paid account the day you create the key.
- If a key leaks, don't panic and don't hope: go to the provider's dashboard, revoke it,
  and make a new one. It takes a minute.
- One key per project, so you can revoke one without breaking the others.

There are two `.env` files in this course. `prep-kit/.env` holds your free practice keys.
The course folder's `.env` (`resolvo-workshop/.env`) holds the course key, and you fill it
in during step 08. They're kept apart on purpose.

Next: [04 Your first LLM call](04-first-llm-call.md)
