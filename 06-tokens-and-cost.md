# 06 Tokens and cost

About 20 minutes. Models don't read words. They read tokens, and you pay per token, so
this is the unit behind every cost and speed number in the course.

## What a token is

A token is a chunk of text: often a whole short word, sometimes part of a long word, a
number or a punctuation mark. Before the model sees your text, a tokenizer cuts it up and
turns each chunk into a number.

```powershell
py code\count_tokens.py
```

This runs offline. It takes ticket T-1001 from `data/tickets.json` (the same 60 tickets
the course uses) and shows how it's cut:

```
Ticket T-1001: 217 characters, 40 words, 47 tokens

'I' | ' ordered' | ' the' | ' wireless' | ' headphones' | ' two' | ' weeks' | ' ago' | ',' |
' order' | ' #' | '482' | '91' | ...
```

Look at the order number: `48291` became two tokens, `482` and `91`. The model never sees
"48291" as one thing, which is part of why models make mistakes copying long numbers.

The rule of thumb for English is about 3 tokens for every 4 words. Other languages,
including Arabic, usually take more tokens for the same meaning, so they cost more.

## What it costs

Providers charge per million tokens, with separate prices for what the model reads (input)
and what it writes (output). Output costs more. The same script works out the price of
reading this ticket and writing a 150-token reply:

```
gpt-4o-mini (OpenAI)           $0.000097 each   $0.97 per 10,000 tickets
gemini-3.5-flash-lite (paid)   $0.000389 each   $3.89 per 10,000 tickets
gpt-4o (OpenAI)                $0.001618 each   $16.18 per 10,000 tickets
```

A single call costs a fraction of a cent. At a real store's volume the choice of model
makes a 16 times difference in the bill. These prices are from October 2026 and they
change, so check the provider's pricing page before you rely on them.

## Speed

Every call to a cloud model takes time: the request travels to the provider, waits in a
queue, and then the model writes the reply one token at a time. Longer replies take
longer.

```powershell
py code\compare.py
```

This sends the same ticket to every provider you've set up (it skips the ones without a
key) and prints the time, the tokens and the answer for each. Run it twice. The times
change from run to run, and that variation is why Session 1 measures speed with many
calls instead of one.

## Try this

- `py code\count_tokens.py T-1005`: an angry customer, in capital letters. Do capitals
  cost more tokens?
- Count a sentence in another language you know:
  `py code\count_tokens.py --text "your sentence"`. How does it compare with the English?
  [The extra reading](extra-how-llms-work.md) has Arabic examples.
- In `compare.py`, which provider was fastest? Was it the one you expected?

Next: [07 A taste of Resolvo](07-taste-of-resolvo.md)
