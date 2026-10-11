"""Module 08: the setup doctor. Run it the night before Session 1.

From your course folder (resolvo-workshop/), with the course venv active:

    python ..\\prep-kit\\code\\check_setup.py           checks everything, costs nothing
    python ..\\prep-kit\\code\\check_setup.py --live    also one tiny paid call (< $0.001)

Kit somewhere else? Use its path instead of ..\\prep-kit, or add --repo <course folder>.

It reads the course's .env only to see which settings are filled in. It never
prints a key, and it never changes any file.
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

from providers import KIT_DIR, PROVIDERS, is_configured

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
REPO_NAME = "resolvo-workshop"
ACTIVATE = r".venv\Scripts\activate  (macOS/Linux: source .venv/bin/activate)"


@dataclass
class Check:
    status: str
    label: str
    fix: str = ""


# Settings each course provider needs, by name. Values are never read out loud.
COURSE_KEYS = {
    "openai": ["OPENAI_API_KEY"],
    "azure": ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT"],
    "anthropic": ["ANTHROPIC_API_KEY"],
}

KIT_PACKAGES = ["openai", "httpx", "dotenv", "tiktoken"]
COURSE_PACKAGES = ["fastapi", "uvicorn", "pydantic", "anthropic", "langchain_core",
                   "langgraph", "qdrant_client", "pytest"]


def is_repo(path: Path) -> bool:
    """Does this folder look like a clone of the course repo?"""
    return (path / "checkpoints" / "00-broken-bot").is_dir() and (path / "requirements.txt").is_file()


def find_repo(explicit: str | None = None, cwd: Path | None = None) -> Path | None:
    """--repo if given; else the folder you're in (or one inside it); else next to the kit."""
    if explicit:
        path = Path(explicit).expanduser().resolve()
        return path if is_repo(path) else None
    cwd = cwd or Path.cwd()
    for candidate in (cwd, cwd / REPO_NAME, KIT_DIR.parent, KIT_DIR.parent / REPO_NAME):
        if is_repo(candidate):
            return candidate.resolve()
    return None


def check_repo(repo: Path | None, explicit: str | None) -> Check:
    if repo:
        return Check(PASS, f"Course repo found: {repo}")
    if explicit:
        return Check(FAIL, f"{explicit} doesn't look like the course repo",
                     f"Point --repo at the {REPO_NAME} folder you cloned (it has a checkpoints/ folder)")
    return Check(FAIL, "Course repo not found",
                 f"Clone it (step 08), then run this from inside {REPO_NAME}/, or add --repo <path>")


def check_python(version: tuple[int, int] = sys.version_info[:2]) -> Check:
    shown = f"{version[0]}.{version[1]}"
    if version in ((3, 12), (3, 11)):
        return Check(PASS, f"Python {shown}")
    if version >= (3, 13):
        return Check(WARN, f"Python {shown} is newer than the course was tested on",
                     "Install Python 3.12 if anything fails to install (see step 01).")
    return Check(FAIL, f"Python {shown} is too old", "Install Python 3.12 (see step 01).")


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def check_venv(repo: Path | None, prefix: str = sys.prefix,
               base: str = getattr(sys, "base_prefix", sys.prefix)) -> Check:
    """The *course* venv should be active here, not the prep kit's."""
    if prefix == base:
        return Check(FAIL, "No virtual environment active",
                     f"From {REPO_NAME}/: {ACTIVATE}")
    if _inside(Path(prefix), KIT_DIR):
        return Check(FAIL, "This is the prep kit's venv, not the course's",
                     f"deactivate, then from {REPO_NAME}/: {ACTIVATE}, and run me again")
    if repo and _inside(Path(prefix), repo):
        return Check(PASS, "The course's virtual environment is active")
    return Check(WARN, "A virtual environment outside the course folder is active",
                 f"Fine if it has the course packages. Usually it's {REPO_NAME}/.venv")


def check_packages(names: list[str], what: str, fix: str) -> Check:
    missing = [n for n in names if importlib.util.find_spec(n) is None]
    if not missing:
        return Check(PASS, f"{what} installed")
    return Check(FAIL, f"{what}: missing {', '.join(missing)}", fix)


def check_git() -> Check:
    if shutil.which("git"):
        return Check(PASS, "git is installed")
    return Check(FAIL, "git not found", "Install it from https://git-scm.com/downloads")


def check_course_env(env: dict[str, str | None] | None) -> list[Check]:
    """env is the parsed course .env, or None when the file doesn't exist."""
    if env is None:
        return [Check(FAIL, f"{REPO_NAME}/.env not found",
                      f"In {REPO_NAME}/: copy .env.example .env  then fill in one provider")]
    provider = (env.get("LLM_PROVIDER") or "").strip().lower()
    if not provider:
        return [Check(FAIL, f"LLM_PROVIDER is not set in {REPO_NAME}/.env",
                      "Set LLM_PROVIDER=openai (or azure / anthropic). See step 08.")]
    if provider not in COURSE_KEYS:
        return [Check(FAIL, f"LLM_PROVIDER={provider!r} is not one the course supports",
                      "Use openai, azure or anthropic. (Gemini/OpenRouter/Ollama are for the prep kit.)")]
    missing = [k for k in COURSE_KEYS[provider] if not (env.get(k) or "").strip()]
    if missing:
        # The template ships with LLM_PROVIDER=azure, so this is the classic slip.
        others = [p for p, keys in COURSE_KEYS.items()
                  if p != provider and (env.get(keys[0]) or "").strip()]
        if others:
            return [Check(FAIL, f"LLM_PROVIDER={provider}, but you filled in the {others[0]} key",
                          f"Change the line to LLM_PROVIDER={others[0]} in {REPO_NAME}/.env")]
        return [Check(FAIL, f"LLM_PROVIDER={provider}, but {', '.join(missing)} not filled in",
                      f"Fill those lines in {REPO_NAME}/.env. See step 08.")]
    if provider == "azure" and "your-resource" in (env.get("AZURE_OPENAI_ENDPOINT") or ""):
        return [Check(FAIL, "AZURE_OPENAI_ENDPOINT still has the example value",
                      "Copy the endpoint URL from your Azure resource's 'Keys and Endpoint' page")]
    checks = [Check(PASS, f"Course provider: {provider} (key filled in)")]
    if provider == "anthropic":
        has_backup = (env.get("OPENAI_API_KEY") or "").strip() or (env.get("AZURE_OPENAI_API_KEY") or "").strip()
        checks.append(Check(PASS if has_backup else WARN,
                            "Anthropic: an OpenAI or Azure key is also needed" +
                            (" (found one)" if has_backup else ""),
                            "" if has_backup else
                            "Session 1's bot and the RAG weeks need OpenAI/Azure. See step 08."))
    return checks


def check_mock_api(url: str = "http://localhost:9000") -> Check:
    import httpx

    try:
        httpx.get(f"{url}/orders/O-48291", timeout=2).raise_for_status()
        return Check(PASS, "Mock order API is running on :9000")
    except Exception:  # noqa: BLE001
        return Check(WARN, "Mock order API not running (fine for now)",
                     "Only needed while you use it. See step 02.")


def check_kit_providers() -> Check:
    ready = [name for name, p in PROVIDERS.items() if is_configured(p) and p.key_env]
    if ready:
        return Check(PASS, f"Prep-kit practice keys: {', '.join(ready)}")
    return Check(WARN, "No Gemini or OpenRouter key in prep-kit/.env",
                 "Optional, but free and useful. See step 04.")


def live_call(env: dict[str, str | None]) -> Check:
    """One tiny real request with the course key: a few dozen tokens."""
    provider = (env.get("LLM_PROVIDER") or "").strip().lower()
    messages = [{"role": "user", "content": "Reply with the single word: ready"}]
    try:
        if provider == "anthropic":
            import anthropic

            client = anthropic.Anthropic(api_key=env["ANTHROPIC_API_KEY"])
            model = env.get("ANTHROPIC_MODEL") or "claude-haiku-5-5"
            reply = client.messages.create(model=model, max_tokens=10, messages=messages)
            text = reply.content[0].text
        else:
            import openai

            if provider == "azure":
                client = openai.AzureOpenAI(
                    api_key=env["AZURE_OPENAI_API_KEY"],
                    azure_endpoint=env["AZURE_OPENAI_ENDPOINT"],
                    api_version=env.get("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview")
                model = env["AZURE_OPENAI_DEPLOYMENT"]
            else:
                client = openai.OpenAI(api_key=env["OPENAI_API_KEY"])
                model = env.get("OPENAI_MODEL") or "gpt-4o-mini"
            # No max_tokens: newer OpenAI models renamed it. The reply is one word anyway.
            reply = client.chat.completions.create(model=model, messages=messages)
            text = reply.choices[0].message.content or ""
        return Check(PASS, f"Live call to {provider} ({model}) answered: {text.strip()[:30]!r}")
    except Exception as err:  # noqa: BLE001
        hint = "Check the key, and that the account has credit and a spending limit set."
        if "DeploymentNotFound" in str(err):
            hint = "Azure wants the DEPLOYMENT name you chose, not the model name."
        return Check(FAIL, f"Live call to {provider} failed: {type(err).__name__}", hint)


def run(live: bool = False, repo_arg: str | None = None) -> list[Check]:
    repo = find_repo(repo_arg)
    env_path = repo / ".env" if repo else None
    env = dotenv_values(env_path) if env_path and env_path.exists() else None
    checks = [
        check_repo(repo, repo_arg),
        check_python(),
        check_venv(repo),
        check_git(),
        check_packages(KIT_PACKAGES, "Prep-kit packages",
                       "pip install -r requirements.txt  (the course list includes these too)"),
        check_packages(COURSE_PACKAGES, "Course packages",
                       f"From {REPO_NAME}/, venv active: pip install -r requirements.txt  (takes a while)"),
    ]
    if repo:
        checks += check_course_env(env)
    checks += [check_kit_providers(), check_mock_api()]
    if live:
        if env and all(c.status != FAIL for c in check_course_env(env)):
            checks.append(live_call(env))
        else:
            checks.append(Check(FAIL, "Skipped the live call", "Fix the .env problems above first."))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Check your machine is ready for Session 1.")
    parser.add_argument("--live", action="store_true", help="also make one tiny paid call")
    parser.add_argument("--repo", help=f"path to your {REPO_NAME} folder (found automatically if you run from it)")
    args = parser.parse_args()
    checks = run(args.live, args.repo)

    marks = {PASS: "[ ok ]", WARN: "[warn]", FAIL: "[FAIL]"}
    for c in checks:
        print(f"{marks[c.status]} {c.label}")
        if c.fix and c.status != PASS:
            print(f"        -> {c.fix}")

    fails = sum(c.status == FAIL for c in checks)
    print()
    if fails:
        print(f"{fails} thing(s) to fix. Fix the first one and run me again.")
        return 1
    print("Ready for Day 1. See you on Monday.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
