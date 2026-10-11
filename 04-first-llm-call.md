# 04 Your first LLM call

About 30 minutes. You'll get two free keys and send the same question to two different
companies' models with one script.

## What an LLM call is

It's an API call like the ones in step 02: a `POST` with JSON in and JSON out. The request
says three things:

- `model`: which model to use, by name
- `messages`: the conversation so far. A `system` message sets the rules ("you are a
  support agent, keep answers short") and a `user` message asks the question
- `temperature`: how much randomness. Near 0 gives the same answer most times, higher
  values give more variety

The response holds the model's reply, plus `usage`: how many tokens it read and wrote. You
pay by the token, and step 06 is about what that means.

## One SDK, three addresses

Most providers now offer an "OpenAI-compatible" API: the same request shape OpenAI made
popular. So one Python package, `openai`, can talk to all of them. The only things that
change are the address, the key and the model name:

| Provider | Address (`base_url`) | Key |
| --- | --- | --- |
| Gemini (Google) | `https://generativelanguage.googleapis.com/v1beta/openai/` | from AI Studio |
| OpenRouter | `https://openrouter.ai/api/v1` | from openrouter.ai |
| Ollama (your laptop) | `http://localhost:11434/v1` | none |

Here's all the code it takes, from `code/providers.py` and `code/chat.py`:

```python
from openai import OpenAI

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[{"role": "system", "content": "Keep answers short."},
              {"role": "user", "content": "Explain an API in one sentence."}],
)
print(response.choices[0].message.content)
```

The Resolvo code does the same thing in a file called `llm.py`: one place knows about the
provider, and the rest of the program never does.

## Get a Gemini key (free)

1. Go to <https://aistudio.google.com/apikey> and sign in with a Google account.
2. Click "Create API key" and copy it.
3. Paste it into `prep-kit/.env` after `GEMINI_API_KEY=`, with no spaces or quotes.

The free tier needs no credit card. It has per-minute and per-day request limits, and you
can see yours in AI Studio. One thing to know: on the free tier, Google may use what you
send to improve its products. Practise with the Nimbus tickets in this repo, and never send
anything personal or anything from work.

## Get an OpenRouter key (free)

OpenRouter is one account that reaches hundreds of models from many companies.

1. Go to <https://openrouter.ai>, sign up, then open <https://openrouter.ai/settings/keys>.
2. Create a key and paste it into `prep-kit/.env` after `OPENROUTER_API_KEY=`.

The model name `openrouter/free` lets OpenRouter pick one of its free models for each
request. You can also pick one yourself: free models have names ending in `:free` on
<https://openrouter.ai/models>. Without any credit you get about 50 free requests a day,
which is plenty for this kit.

## Make the calls

```powershell
py code\show_env.py        # both keys should now say "set"
py code\chat.py --provider gemini "Explain what an API is in one sentence."
py code\chat.py --provider openrouter "Explain what an API is in one sentence."
```

Under each answer you'll see a line like:

```
[gemini | gemini-3.5-flash-lite | 31 tokens in, 24 out | 870 ms]
```

That's the model that answered, what it read, what it wrote and how long it took. Those
four numbers come back in every lesson of the course.

## Try this

- Run the same OpenRouter command three times. Does `openrouter/free` pick the same model
  each time? Look at the model name in the bracket.
- Ask for a joke with `--temperature 0`, three times. Then with `--temperature 1.5`.
- Ask Gemini something it can't know, like "What did I eat for breakfast?" Models produce
  plausible text. They don't look things up unless you give them the information.

## If something went wrong

`chat.py` turns the usual errors into a sentence. The common ones:

| You see | It means |
| --- | --- |
| `... is not set` | The key isn't in `prep-kit/.env`, or the file is still named `.env.example` |
| `rejected your key (401)` | A typo, or a space or quote mark crept in. `show_env.py` will tell you |
| `Rate limited (429)` | Free tier limit. Wait a minute |
| `Model not found (404)` | The model name in `.env` is wrong or retired. Check the provider's model list |

Next: [05 Local models](05-local-models.md)
