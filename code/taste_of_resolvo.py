"""Module 07: a first taste of Resolvo. Ask a model to sort real Nimbus tickets.

    py code\\taste_of_resolvo.py --provider ollama
    py code\\taste_of_resolvo.py --provider gemini T-1003 T-1008

We ask for JSON, then check what came back. The model can reply with anything,
so the code decides whether to trust it. That one idea runs through the whole course.
"""
from __future__ import annotations

import argparse
import json

from chat import ask
from count_tokens import load_ticket, ticket_text
from providers import PROVIDERS, SetupError, explain_error

# The same labels the course's checkpoint 01 uses for its triage step.
ALLOWED = {
    "category": {"refund_request", "replacement", "shipping_delay", "product_defect",
                 "account", "other"},
    "priority": {"low", "medium", "high", "urgent"},
    "sentiment": {"calm", "frustrated", "angry"},
}

PROMPT = """Sort this customer support ticket for an electronics store.

Reply with ONLY a JSON object, no other text, like this:
{{"category": "...", "priority": "...", "sentiment": "..."}}

category: one of {category}
priority: one of {priority}
sentiment: one of {sentiment}

Ticket:
{ticket}"""


def build_prompt(ticket: dict) -> str:
    opts = {k: ", ".join(sorted(v)) for k, v in ALLOWED.items()}
    return PROMPT.format(ticket=ticket_text(ticket), **opts)


def parse_reply(text: str) -> tuple[dict | None, str]:
    """(result, problem). result is None when the reply can't be trusted."""
    cleaned = text.strip()
    if cleaned.startswith("```"):  # models love wrapping JSON in a markdown code fence
        cleaned = cleaned.strip("`").removeprefix("json").strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return None, "not valid JSON"
    if not isinstance(data, dict):
        return None, "JSON, but not an object"
    for field, allowed in ALLOWED.items():
        if data.get(field) not in allowed:
            return None, f"{field}={data.get(field)!r} is not one of the allowed values"
    return {k: data[k] for k in ALLOWED}, ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Sort a few real tickets with an LLM.")
    parser.add_argument("tickets", nargs="*", default=["T-1001", "T-1002", "T-1005"])
    parser.add_argument("--provider", choices=list(PROVIDERS), default="gemini")
    args = parser.parse_args()

    for ticket_id in args.tickets:
        ticket = load_ticket(ticket_id)
        print(f"\n--- {ticket_id}: {ticket_text(ticket)[:100]}...")
        try:
            reply = ask(args.provider, build_prompt(ticket), temperature=0)
        except SetupError as err:
            print(err)
            return 1
        except Exception as err:  # noqa: BLE001
            print(explain_error(args.provider, err))
            return 1
        result, problem = parse_reply(reply["text"])
        if result:
            print(f"    OK      {result}   ({reply['ms']} ms)")
        else:
            print(f"    REJECTED: {problem}")
            print(f"    raw reply was: {reply['text'][:200]!r}")
    print("\nOK only means the reply had the right shape. Read each ticket: is the label right?")
    print("Session 2 makes the shape reliable (structured outputs). Session 10 measures the labels.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
