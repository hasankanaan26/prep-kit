# Prep kit: before day one

Welcome. On Monday, October 19 you start four weeks of building Resolvo, a system that
reads support tickets for a small electronics store (Nimbus Electronics) and helps resolve
them with a language model.

This kit gets your laptop and your head ready for that. It works on its own: download it
from <https://github.com/hasankanaan26/prep-kit> (step 01 shows how), put it anywhere, and
you'll download the course code itself in step 08.

Maintainers: the files in `data/`, `mock_api/` and `slides/` are copies from the course
repo. Keep both repos side by side and run `pytest`: it fails on any copy that has drifted
and prints the command to refresh it. Every topic gets a light first
touch. You don't need to master any of it before Monday, and nothing here will be graded.
If you get stuck on a step, write down what you saw and move on. The course covers all of
it again, slowly.

Plan on 3 to 4 hours in total, split however you like. The optional online kickoff call
the weekend before covers the same material from the slides in this folder:
open [`slides/session-00.html`](slides/session-00.html) in a browser (arrow keys to move,
`f` for full screen), or use `slides/session-00.pptx`.

## The route

| Step | What you'll do | Time |
| --- | --- | --- |
| [01 Terminal, Python, venv](01-terminal-python-venv.md) | Open a terminal, install Python, make a virtual environment | 35 min |
| [02 APIs](02-apis.md) | Send requests to a small order API running on your laptop | 30 min |
| [03 Secrets and .env](03-secrets-and-env.md) | Keep API keys out of your code | 15 min |
| [04 Your first LLM call](04-first-llm-call.md) | Free keys from Gemini and OpenRouter, one script that talks to both | 30 min |
| [05 Local models](05-local-models.md) | Run a model on your own laptop with Ollama | 30 min |
| [06 Tokens and cost](06-tokens-and-cost.md) | See what a model reads and what it costs | 20 min |
| [07 A taste of Resolvo](07-taste-of-resolvo.md) | Ask a model to sort real Nimbus tickets | 20 min |
| [08 Get ready for Session 1](08-get-ready.md) | Your course key, the course code, the full install, the setup check | 50 min |

Steps 04 and 05 are alternatives as much as companions: if you can only do one, do the
one that works on your machine. Step 08 is the one that must be done before Monday.

Extra reading, about 20 minutes, no code:
[how LLMs work, in plain words](extra-how-llms-work.md). It covers where language models
came from, the one sentence Session 1 is built on, and why the same request costs more in
Arabic. Session 1 assumes you've seen it once.

## What's in this folder

```
prep-kit/
  README.md            you are here
  01-...08-*.md        the eight steps
  extra-how-llms-work.md   background reading for Session 1
  requirements.txt     the small install for steps 01-07
  .env.example         a template for your free practice keys
  code/                the scripts each step runs
  data/tickets.json    the 60 Nimbus support tickets the course uses
  mock_api/            a small fake Nimbus order system (step 02)
  slides/              the Session 0 deck (HTML and PowerPoint)
  tests/               checks for the scripts (run: pytest)
```

All commands in steps 01 to 07 are run from this `prep-kit/` folder with its virtual
environment active. Step 08 moves to the course folder and says so. Windows commands come first, and
macOS/Linux versions follow where they differ.

## Ready for day one

Tick these off before Monday:

- [ ] Python 3.12 (or 3.11) installed, and the kit's `.venv` created and activated
- [ ] You ran `code\hello_api.py` against the mock order API and saw a 404 and a 500
- [ ] You made at least one LLM call with `code\chat.py` (Gemini, OpenRouter or Ollama)
- [ ] You have a paid course key (OpenAI recommended) with a spending limit set
- [ ] The course code is cloned next to the kit, with its own `.venv`
- [ ] `deskhand-workshop/.env` is filled in, and the full course install finished
- [ ] From `deskhand-workshop/`, `python ..\prep-kit\code\check_setup.py --live` ends with
      "Ready for Day 1"

If the last line fails and you can't fix it, bring your laptop 20 minutes early on Monday
along with the output of `check_setup.py`. We'll sort it out together.
