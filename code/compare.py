"""Module 06: the same question to every provider you have set up, side by side.

    py code\\compare.py
    py code\\compare.py T-1004

It skips any provider without a key, and tells you if one fails.
"""
from __future__ import annotations

import sys

from chat import ask
from count_tokens import load_ticket, ticket_text
from providers import PROVIDERS, explain_error, is_configured


def main() -> None:
    ticket = load_ticket(sys.argv[1] if len(sys.argv) > 1 else "T-1001")
    prompt = ("A customer wrote to an electronics store. Summarise what they want in one "
              f"sentence.\n\nCustomer message:\n{ticket_text(ticket)}")

    rows = []
    for name, p in PROVIDERS.items():
        if not is_configured(p):
            print(f"skip {name}: {p.key_env} not set")
            continue
        print(f"asking {name} ...")
        try:
            rows.append(ask(name, prompt))
        except Exception as err:  # noqa: BLE001
            print(f"  {name} failed: {explain_error(name, err)}")

    print(f"\nTicket {ticket['ticket_id']}\n")
    for r in rows:
        print(f"{r['provider']:<11} {r['ms']:>6} ms  {r['input_tokens']} in / "
              f"{r['output_tokens']} out  ({r['model']})")
        print(f"            {r['text']}\n")
    if not rows:
        print("No provider answered. Run code\\show_env.py and see module 04.")


if __name__ == "__main__":
    main()
