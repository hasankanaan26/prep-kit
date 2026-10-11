"""Module 03: which keys does Python see? (It never prints the keys themselves.)

    py code\\show_env.py

A key is a password. This script only says whether each one is set and how long it
is, which is enough to spot the usual mistakes: not set, or pasted with extra spaces.
"""
from __future__ import annotations

import os

from providers import KIT_DIR, PROVIDERS


def describe(value: str | None) -> str:
    """'not set', or 'set, N chars' plus a warning for whitespace or quotes. Never the value."""
    if value is None or value == "":
        return "not set"
    notes = []
    if value != value.strip():
        notes.append("has spaces at the start or end")
    if value[:1] in "\"'" or value[-1:] in "\"'":
        notes.append("has quote marks around it")
    msg = f"set, {len(value)} chars"
    return msg + (f"  <- WARNING: {', '.join(notes)}" if notes else "")


def main() -> None:
    env_file = KIT_DIR / ".env"
    print(f"Reading {env_file}  ({'found' if env_file.exists() else 'NOT FOUND: copy .env.example to .env'})\n")
    for p in PROVIDERS.values():
        if p.key_env is None:
            print(f"  {p.name:<11} no key needed (runs locally)")
        else:
            print(f"  {p.name:<11} {p.key_env:<20} {describe(os.getenv(p.key_env))}")
    print("\nThe values stay in .env. Never paste a key into code, chat, a screenshot or git.")


if __name__ == "__main__":
    main()
