# Extra reading: how LLMs work, in plain words

About 20 minutes, no code required. This page is background. Session 1 assumes you've
heard these ideas once, so it can spend its time on the broken bot instead. Read it any
time before Monday, ideally after step 04, when you've made your first call.

## How we got here

What a language model can do today took four steps over about 20 years. You don't need
the history to build anything in this course, but it explains what's behind the API.

| Step | The idea in plain words | Example |
| --- | --- | --- |
| Classic machine learning | A person decides which clues to look at, and the computer learns how much each clue counts. | A spam filter that counts words like "free" and "winner". |
| Deep learning | Show it millions of examples and it works out which clues matter by itself. | A photo app that finds every picture of your dog, though nobody defined "dog". |
| Transformers (2017) | It reads a whole passage at once, and every word can "look at" every other word to work out what refers to what. | In "The headphones arrived cracked, so I want *them* replaced", it links *them* to the headphones. |
| Instruction tuning (about 2022) | Extra training on pairs of questions and good answers, so it follows instructions instead of just continuing text. | ChatGPT, November 2022. |

Add scale on top: far more text and far bigger models. That combination is what you call
through the API.

Instruction tuning is the step that made it useful. Ask a raw model "What is your refund
window?" and it may continue with "What is your shipping time? What is your warranty?",
because it thinks it's in the middle of an FAQ page. An instruction-tuned model answers
the question.

Before all this, sorting support tickets into "refund", "shipping" and "warranty" meant
labelling thousands of tickets by hand, training a model and keeping a specialist team to
look after it: weeks of work. Today it's one API call and a paragraph of instructions.
What didn't change is the engineering: the API can be slow, down or wrong, and every call
costs money. That's what the course is about.

## The one sentence

> An LLM predicts the next token, over and over, based only on the text you sent it.

Try this on your phone. Open a messaging app, type "I want a" and look at the three
suggestions above the keyboard. That's the mechanism. A large language model (LLM) is the
same idea trained on a huge amount of text, with a much better sense of context.

Given some text, the model gives a score to every possible next piece, picks one, adds it
to the text, and repeats until it predicts "end". Every reply you've seen from ChatGPT
was written this way, one piece at a time. That's why answers appear word by word, and why
long answers take longer.

There's no database inside and nothing gets looked up. The model only has patterns it
learned and the text you sent it. Session 1 starts from this sentence and shows how most
of the broken bot's failures follow from it.

## Tokens up close

The "pieces" are tokens. You met them in step 06. A few more examples, all counted with
the tokenizer GPT-4o uses:

| Text | Split into | Tokens |
| --- | --- | --- |
| `refund` | refund | 1 |
| `REFUND` | REF · UND | 2 |
| `unbelievable` | un · bel · ievable | 3 |
| `$24.99` | $ · 24 · . · 99 | 4 |
| `strawberry` | st · raw · berry | 3 |

Two things follow from this:

- The model never sees letters. "How many r's are in strawberry?" is famously hard for it,
  because it sees `st`, `raw` and `berry`, not ten letters.
- Prices get cut into pieces too, so exact arithmetic on them isn't reliable. When money
  is involved, do the maths in code.

## Tokens in other languages

The tokenizer was built mostly from English text, so common English words became single
tokens and words in other languages get cut into more pieces. The same request costs a
different amount depending on the language:

| The same request | Words | Tokens |
| --- | --- | --- |
| I want a refund for my order | 7 | 7 |
| أريد استرداد المبلغ لطلبي | 4 | 10 |
| بدي رجّع المصاري (Lebanese) | 3 | 7 |
| The headphones arrived broken | 4 | 4 |
| وصلت السماعات مكسورة | 3 | 7 |

The single word `refund` is 1 token, and `استرداد` is 3 (`است · رد · اد`).

So an Arabic ticket costs more, takes a little longer, and fills more of the model's space
for that call. If you build for Arabic-speaking customers, estimate costs with their real
messages, not with English test data. Newer tokenizers have narrowed the gap, but it's
still there, and other providers (Claude, Gemini) use different tokenizers with different
counts.

Count your own:

```powershell
py code\count_tokens.py --text "بدي رجّع المصاري"
py code\count_tokens.py --text "I want a refund for my order"
```

## What to take into Monday

- An LLM predicts likely text. Likely is not the same as true.
- It only knows what's in the text you send, on this call.
- Tokens are the unit of cost, speed and space.

Back to the [README](README.md).
