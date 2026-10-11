# 07 A taste of Resolvo

About 20 minutes. This is a small version of the first thing you'll build: read a support
ticket and sort it, so the right thing can happen next.

## The job

Nimbus gets tickets like this one (T-1001):

> I ordered the wireless headphones two weeks ago, order #48291. They arrived with a
> cracked case. I want a refund or a replacement...

The program asks a model to label it with three things, using the same labels as
checkpoint 01 of the course:

| Field | Allowed values |
| --- | --- |
| category | refund_request, replacement, shipping_delay, product_defect, account, other |
| priority | low, medium, high, urgent |
| sentiment | calm, frustrated, angry |

## Run it

```powershell
py code\taste_of_resolvo.py --provider gemini
py code\taste_of_resolvo.py --provider ollama
```

You can pass ticket ids too: `py code\taste_of_resolvo.py --provider gemini T-1003 T-1011`.

## The important part: the code checks the reply

The prompt asks for "ONLY a JSON object". The model may still say "Sure! Here's the
JSON:", wrap it in a code fence, or invent a category that isn't on the list. So
`parse_reply()` in the script checks every reply before trusting it:

1. Is it valid JSON?
2. Is it an object (a dict)?
3. Is every field one of the allowed values?

Anything that fails is printed as `REJECTED`, with the raw reply, instead of being used.
That's the rule the whole course runs on: the model suggests, and your code decides.

## Two kinds of wrong

Here's a real run with `llama3.2` on a laptop:

```
--- T-1002: Hi, checking on order O-58204 (SoundBar Mini). It says shipped over a week ago...
    OK      {'category': 'shipping_delay', 'priority': 'low', 'sentiment': 'calm'}

--- T-1011: Hi, I received a Nimbus smart speaker as a birthday gift last week and I already own...
    OK      {'category': 'product_defect', 'priority': 'low', 'sentiment': 'calm'}
```

Both say `OK`. But T-1011 is someone who got a duplicate gift and wants to return it.
Nothing is broken, so `product_defect` is the wrong label.

So there are two ways a reply can be wrong:

- Wrong shape: not JSON, or a value off the list. Code can catch this every time.
  Session 2 makes it nearly impossible with structured outputs.
- Wrong answer: perfectly shaped, but mistaken. Code can't see this by looking at one reply.
  You find it by testing against tickets where you already know the right answer.
  Session 10 is about exactly that.

## Try this

- Run tickets T-1001 to T-1012 on two providers. Where do they disagree? Who's right?
- T-1006 is a trick ticket. Read it in `data/tickets.json` before you run it. What
  is the customer trying to do? (Session 11 is about this kind of ticket.)
- Change `temperature=0` to `temperature=1` in the script and run the same ticket three
  times.

Next: [08 Get ready for Session 1](08-get-ready.md)
