"""Module 06: what is a token, and what does a ticket cost?

    py code\\count_tokens.py            (ticket T-1001)
    py code\\count_tokens.py T-1002     (any ticket id from data/tickets.json)
    py code\\count_tokens.py --text "any sentence, in any language"

Runs offline. Nothing is sent anywhere.
"""
from __future__ import annotations

import argparse
import json
import sys

import tiktoken

from providers import DATA_DIR

TICKETS_PATH = DATA_DIR / "tickets.json"

# USD per 1 million tokens, checked October 2026. Prices change: always check the
# provider's pricing page. These are only here to make the arithmetic concrete.
PRICES = {
    "gpt-4o-mini (OpenAI)":          {"input": 0.15, "output": 0.60},
    "gemini-3.5-flash-lite (paid)":  {"input": 0.30, "output": 2.50},
    "gpt-4o (OpenAI)":               {"input": 2.50, "output": 10.00},
}


def load_ticket(ticket_id: str) -> dict:
    tickets = json.loads(TICKETS_PATH.read_text(encoding="utf-8"))["tickets"]
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            return t
    raise SystemExit(f"No ticket {ticket_id}. Try T-1001 to T-{1000 + len(tickets)}.")


def ticket_text(ticket: dict) -> str:
    return "\n".join(m["text"] for m in ticket["messages"])


def cost_usd(input_tokens: int, output_tokens: int, price: dict) -> float:
    return (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000


def main() -> None:
    parser = argparse.ArgumentParser(description="Count the tokens in a ticket or any text.")
    parser.add_argument("ticket_id", nargs="?", default="T-1001")
    parser.add_argument("--text", help="count this text instead of a ticket")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):  # so Arabic and other scripts print on Windows
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if args.text:
        label, text = "Your text", args.text
    else:
        ticket = load_ticket(args.ticket_id)
        label, text = f"Ticket {ticket['ticket_id']}", ticket_text(ticket)
    enc = tiktoken.get_encoding("o200k_base")  # the tokenizer used by GPT-4o models
    ids = enc.encode(text)

    print(f"{label}: {len(text)} characters, {len(text.split())} words, {len(ids)} tokens\n")
    print("The first 20 tokens, as the model sees them:")
    print("  " + " | ".join(repr(enc.decode([i])) for i in ids[:20]))

    reply_tokens = 150  # a short support reply
    print(f"\nCost of reading this and writing a {reply_tokens}-token reply:")
    for model, price in PRICES.items():
        one = cost_usd(len(ids), reply_tokens, price)
        print(f"  {model:<30} ${one:.6f} each   ${one * 10_000:,.2f} per 10,000 tickets")
    print("\nRule of thumb: 1 token is about 3/4 of an English word. Other languages use more.")
    print("Each provider has its own tokenizer, so Gemini's count will differ a little.")


if __name__ == "__main__":
    main()
