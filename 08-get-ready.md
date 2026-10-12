# 08 Get ready for Session 1

About 50 minutes, mostly waiting for the install. This is the one step that has to be
done before Monday.

The free keys from step 04 are for practice. The course itself needs a paid key from a
provider the Resolvo code supports, and you bring your own.

## Which provider

| Provider | Works for the whole course? | Notes |
| --- | --- | --- |
| OpenAI (recommended) | Yes | One key covers everything, including embeddings in week 3 |
| Azure OpenAI | Yes | Pick this if your employer already gives you Azure. Needs two deployments |
| Anthropic (Claude) | Not on its own | Session 1's bot only speaks OpenAI/Azure, and Anthropic has no embeddings. You'd need an OpenAI key as well |

Gemini, OpenRouter and Ollama aren't wired into the course code. The checkpoints were
built and tested against the three providers above, and the later sessions use features
(structured outputs, embeddings) that behave differently across providers.

## Get an OpenAI key

1. Sign up at <https://platform.openai.com>.
2. Billing: add prepaid credit. $10 is plenty: on the default small model (`gpt-4o-mini`)
   a typical lab run costs cents. The slides warn you before anything costs more.
3. Limits: set a monthly budget, so a bug in a loop can't run up a bill.
4. API keys: create a key named `resolvo` and copy it. You only see it once.

A ChatGPT Plus subscription is a separate product and doesn't include API access. The same
goes for Claude Pro/Max and the Anthropic API.

## Get the course code

The course code lives in a git repository. Git keeps track of every version of the code,
and you need three commands this month: `clone` (download it once), `pull` (get the latest
changes) and `status` (what have I changed?).

Install git from <https://git-scm.com/downloads> if `git --version` doesn't work yet.
Then, from the folder that holds `prep-kit` (your `projects` folder from step 01):

```powershell
cd ..                       # if you're still inside prep-kit
git clone https://github.com/hasankanaan26/resolvo-workshop.git
cd resolvo-workshop
git status
```

You now have two folders side by side:

```
projects/
  prep-kit/            this kit
  resolvo-workshop/    the course
```

## A second toolbox, for the course

The course gets its own virtual environment, inside `resolvo-workshop/`. Leave the kit's
venv first, then make and activate the new one:

```powershell
deactivate                  # leaves the prep kit's venv
py -3.12 -m venv .venv      # macOS/Linux: python3.12 -m venv .venv
.venv\Scripts\activate      # macOS/Linux: source .venv/bin/activate
```

From now on, "activate the venv" for the course means this one.

## Install everything

With the course venv active, from `resolvo-workshop/`:

```powershell
pip install -r requirements.txt
```

This is the full course list (LangChain, LangGraph, a vector store, evaluation tools). It
can take 10 to 20 minutes, so start it now and get a coffee while you do the next part.
You only do this once.

## Fill in the course .env

Also from `resolvo-workshop/`:

```powershell
copy .env.example .env      # macOS/Linux: cp .env.example .env
```

Open `.env` in your editor and change two lines:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...your key...
```

The template starts with `LLM_PROVIDER=azure`, so make sure you change it. Leave the other
lines as they are.

If you use Azure: fill in `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT` and
`AZURE_OPENAI_DEPLOYMENT`. The deployment is the name you chose when you deployed the
model, not the model's own name. That mix-up is the most common Azure error (404,
`DeploymentNotFound`).

## Run the setup check

Still in `resolvo-workshop/`, with the course venv active, run the kit's check:

```powershell
python ..\prep-kit\code\check_setup.py      # macOS/Linux: python ../prep-kit/code/check_setup.py
```

If you put the kit somewhere else, use its path instead of `..\prep-kit`. The check finds
the course folder because you're standing in it. (You can also point at it with
`--repo C:\path\to\resolvo-workshop`.)

It checks the course folder, your Python, the course venv, git, both package lists, your
course `.env` (it looks at which settings are filled in, never at the values), your
practice keys and the mock API. When everything passes, make one real call with your
course key. It costs a tiny fraction of a cent:

```powershell
python ..\prep-kit\code\check_setup.py --live
```

The goal is the last line:

```
Ready for Day 1. See you on Monday.
```

`warn` lines are fine. Only `FAIL` lines need fixing, and each one prints what to do. The
usual one is "This is the prep kit's venv": run `deactivate`, activate the course venv,
and try again.

## Before Session 3: an AI coding assistant

Session 3 is about working with an AI coding assistant, and its lab starts with one open
on the course code. If you already use one (Cursor, Claude Code, GitHub Copilot or
similar), bring it. If not, install one before that Friday: a free tier is enough, for
example GitHub Copilot Free in VS Code. Check that it can open a folder and answer a
question about a file in it. No assistant on the day? You'll pair with someone who has one.

You won't need Docker for this course.

## Before Monday

- `git pull` in `resolvo-workshop/` to get the latest code.
- Run `check_setup.py --live` once more, from `resolvo-workshop/`.
- In `resolvo-workshop/`, skim `checkpoints/00-broken-bot/README.md`. Session 1 starts by
  breaking that bot.

See you on Monday.
