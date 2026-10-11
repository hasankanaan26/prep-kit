"""Module 01: which Python is running, and is it inside a virtual environment?

    py code\\where_am_i.py          (Windows)
    python3 code/where_am_i.py     (macOS / Linux)

Run it before and after activating the venv and compare the output.
"""
import importlib.util
import sys


def in_venv() -> bool:
    # Inside a venv, sys.prefix points at the venv folder and base_prefix at the real Python.
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def main() -> None:
    print(f"Python version : {sys.version.split()[0]}")
    print(f"Running from   : {sys.executable}")
    if in_venv():
        print(f"Virtual env    : YES  ({sys.prefix})")
    else:
        print("Virtual env    : NO   (this is the computer-wide Python)")
        print("                 Activate the venv first. See 01-terminal-python-venv.md")

    print("\nPackages the prep kit needs:")
    for pkg in ("openai", "httpx", "dotenv", "tiktoken"):
        found = importlib.util.find_spec(pkg) is not None
        print(f"  {'ok     ' if found else 'MISSING'}  {pkg}")
    if not all(importlib.util.find_spec(p) for p in ("openai", "httpx", "dotenv", "tiktoken")):
        print("\nFix: pip install -r requirements.txt   (with the venv active)")


if __name__ == "__main__":
    main()
