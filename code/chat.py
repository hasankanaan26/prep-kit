"""Module 04/05: your first LLM call. The same code works with three providers.

    py code\\chat.py --provider gemini "Explain an API in one sentence."
    py code\\chat.py --provider openrouter "Explain an API in one sentence."
    py code\\chat.py --provider ollama "Explain an API in one sentence."

Add --temperature 1.5 and run it a few times to see the answers drift.
"""
from __future__ import annotations

import argparse
import sys
import time

from providers import PROVIDERS, SetupError, explain_error, get_provider, make_client, model_for


def ask(provider: str, prompt: str, temperature: float = 0.2) -> dict:
    """One request, one answer. Returns the text plus the numbers worth watching."""
    client = make_client(provider)
    model = model_for(get_provider(provider))
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[
            # The system message sets the rules. The user message is the question.
            {"role": "system", "content": "You are a helpful assistant. Keep answers short."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    ms = (time.perf_counter() - started) * 1000
    usage = response.usage
    return {
        "provider": provider,
        "model": response.model or model,
        "text": (response.choices[0].message.content or "").strip(),
        "input_tokens": getattr(usage, "prompt_tokens", None),
        "output_tokens": getattr(usage, "completion_tokens", None),
        "ms": round(ms),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one prompt to one LLM provider.")
    parser.add_argument("prompt", nargs="?", default="Explain what an API is in one sentence.")
    parser.add_argument("--provider", choices=list(PROVIDERS), default="gemini")
    parser.add_argument("--temperature", type=float, default=0.2)
    args = parser.parse_args()

    try:
        result = ask(args.provider, args.prompt, args.temperature)
    except SetupError as err:
        print(err)
        return 1
    except Exception as err:  # noqa: BLE001  (show beginners a sentence, not a stack trace)
        print(explain_error(args.provider, err))
        return 1

    print(result["text"])
    print(f"\n[{result['provider']} | {result['model']} | "
          f"{result['input_tokens']} tokens in, {result['output_tokens']} out | {result['ms']} ms]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
