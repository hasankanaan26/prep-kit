from types import SimpleNamespace

import pytest

import chat
import check_setup as cs
import providers
import show_env
import taste_of_resolvo as taste
from count_tokens import cost_usd, load_ticket, ticket_text


# ---- providers -----------------------------------------------------------------------

def test_every_provider_has_defaults():
    for p in providers.PROVIDERS.values():
        assert providers.base_url_for(p).startswith("http")
        assert providers.model_for(p)


def test_env_overrides_model_and_url(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL", "some-other-model")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://otherhost:11434/v1")
    assert providers.model_for(providers.PROVIDERS["gemini"]) == "some-other-model"
    assert providers.base_url_for(providers.PROVIDERS["ollama"]) == "http://otherhost:11434/v1"


def test_missing_key_explains_the_fix():
    with pytest.raises(providers.SetupError) as err:
        providers.key_for(providers.PROVIDERS["openrouter"])
    assert "OPENROUTER_API_KEY" in str(err.value)
    assert "openrouter.ai" in str(err.value)


def test_ollama_needs_no_key():
    p = providers.PROVIDERS["ollama"]
    assert providers.is_configured(p)
    assert providers.key_for(p) == "ollama"


def test_unknown_provider():
    with pytest.raises(providers.SetupError):
        providers.get_provider("chatgpt")


def test_make_client_points_at_the_provider(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-real")
    client = providers.make_client("gemini")
    assert "generativelanguage.googleapis.com" in str(client.base_url)


# ---- show_env never leaks a key ------------------------------------------------------

def test_describe_never_contains_the_value():
    secret = "sk-THIS-IS-SECRET-1234567890"
    out = show_env.describe(secret)
    assert secret not in out and "SECRET" not in out
    assert f"{len(secret)} chars" in out


def test_describe_flags_common_paste_mistakes():
    assert show_env.describe(None) == "not set"
    assert "spaces" in show_env.describe(" abc ")
    assert "quote" in show_env.describe('"abc"')


# ---- chat.ask with a fake client -----------------------------------------------------

class FakeClient:
    def __init__(self, text):
        reply = SimpleNamespace(
            model="fake-model",
            choices=[SimpleNamespace(message=SimpleNamespace(content=text))],
            usage=SimpleNamespace(prompt_tokens=12, completion_tokens=3),
        )
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=lambda **kw: reply))


def test_ask_returns_text_and_numbers(monkeypatch):
    monkeypatch.setattr(chat, "make_client", lambda name: FakeClient("  hello  "))
    result = chat.ask("ollama", "hi")
    assert result["text"] == "hello"
    assert (result["input_tokens"], result["output_tokens"]) == (12, 3)
    assert result["ms"] >= 0


# ---- tokens and tickets --------------------------------------------------------------

def test_tickets_load():
    ticket = load_ticket("T-1001")
    assert "headphones" in ticket_text(ticket)


def test_count_tokens_any_text(monkeypatch, capsys):
    import count_tokens

    monkeypatch.setattr("sys.argv", ["count_tokens.py", "--text", "I want a refund for my order"])
    count_tokens.main()
    assert "7 words, 7 tokens" in capsys.readouterr().out


def test_cost_math():
    # 1M input tokens at $0.15 + 1M output at $0.60
    assert cost_usd(1_000_000, 1_000_000, {"input": 0.15, "output": 0.60}) == pytest.approx(0.75)


# ---- taste_of_resolvo: the code decides whether to trust the reply --------------------

def test_parse_good_reply():
    result, problem = taste.parse_reply(
        '{"category": "product_defect", "priority": "high", "sentiment": "frustrated"}')
    assert problem == "" and result["category"] == "product_defect"


def test_parse_strips_code_fence():
    result, _ = taste.parse_reply(
        '```json\n{"category": "other", "priority": "low", "sentiment": "calm"}\n```')
    assert result == {"category": "other", "priority": "low", "sentiment": "calm"}


@pytest.mark.parametrize("reply, problem", [
    ("Sure! Here is the JSON you asked for", "not valid JSON"),
    ('["other"]', "not an object"),
    ('{"category": "broken", "priority": "low", "sentiment": "calm"}', "category"),
])
def test_parse_rejects_bad_replies(reply, problem):
    result, why = taste.parse_reply(reply)
    assert result is None and problem in why


def test_prompt_lists_every_allowed_value():
    prompt = taste.build_prompt(load_ticket("T-1001"))
    for values in taste.ALLOWED.values():
        for v in values:
            assert v in prompt


# ---- the doctor ----------------------------------------------------------------------

def test_python_versions():
    assert cs.check_python((3, 12)).status == cs.PASS
    assert cs.check_python((3, 11)).status == cs.PASS
    assert cs.check_python((3, 14)).status == cs.WARN
    assert cs.check_python((3, 9)).status == cs.FAIL


def test_venv_detection(tmp_path):
    repo = tmp_path / "resolvo-workshop"
    assert cs.check_venv(repo, str(repo / ".venv"), "/usr").status == cs.PASS
    assert cs.check_venv(repo, "/usr", "/usr").status == cs.FAIL
    # the kit's own venv is the classic mix-up in step 08
    kit_venv = cs.check_venv(repo, str(providers.KIT_DIR / ".venv"), "/usr")
    assert kit_venv.status == cs.FAIL and "prep kit" in kit_venv.label
    assert cs.check_venv(repo, str(tmp_path / "elsewhere"), "/usr").status == cs.WARN


def make_fake_repo(path):
    (path / "checkpoints" / "00-broken-bot").mkdir(parents=True)
    (path / "requirements.txt").write_text("openai\n")
    return path


def test_find_repo_from_inside_it(tmp_path):
    repo = make_fake_repo(tmp_path / "resolvo-workshop")
    assert cs.find_repo(cwd=repo) == repo.resolve()


def test_find_repo_one_level_up(tmp_path):
    repo = make_fake_repo(tmp_path / "resolvo-workshop")
    assert cs.find_repo(cwd=tmp_path) == repo.resolve()


def test_find_repo_explicit(tmp_path):
    repo = make_fake_repo(tmp_path / "somewhere-else")
    assert cs.find_repo(str(repo)) == repo.resolve()
    assert cs.find_repo(str(tmp_path / "nothing-here")) is None


def test_repo_missing_says_clone_it():
    check = cs.check_repo(None, None)
    assert check.status == cs.FAIL and "Clone" in check.fix


def test_course_env_missing_file():
    assert cs.check_course_env(None)[0].status == cs.FAIL


@pytest.mark.parametrize("env, status", [
    ({}, cs.FAIL),
    ({"LLM_PROVIDER": "gemini"}, cs.FAIL),
    ({"LLM_PROVIDER": "openai", "OPENAI_API_KEY": ""}, cs.FAIL),
    ({"LLM_PROVIDER": "openai", "OPENAI_API_KEY": "x"}, cs.PASS),
    ({"LLM_PROVIDER": "azure", "AZURE_OPENAI_API_KEY": "x"}, cs.FAIL),
    ({"LLM_PROVIDER": "azure", "AZURE_OPENAI_API_KEY": "x", "AZURE_OPENAI_ENDPOINT": "x",
      "AZURE_OPENAI_DEPLOYMENT": "x"}, cs.PASS),
])
def test_course_env(env, status):
    assert cs.check_course_env(env)[0].status == status


def test_spots_the_provider_line_left_on_azure():
    checks = cs.check_course_env({"LLM_PROVIDER": "azure", "OPENAI_API_KEY": "x"})
    assert checks[0].status == cs.FAIL and "LLM_PROVIDER=openai" in checks[0].fix


def test_spots_the_example_azure_endpoint():
    checks = cs.check_course_env({"LLM_PROVIDER": "azure", "AZURE_OPENAI_API_KEY": "x",
                                  "AZURE_OPENAI_ENDPOINT": "https://your-resource.openai.azure.com/",
                                  "AZURE_OPENAI_DEPLOYMENT": "gpt-4.1-mini"})
    assert checks[0].status == cs.FAIL and "example" in checks[0].label


def test_anthropic_warns_without_an_openai_key():
    checks = cs.check_course_env({"LLM_PROVIDER": "anthropic", "ANTHROPIC_API_KEY": "x"})
    assert [c.status for c in checks] == [cs.PASS, cs.WARN]
    checks = cs.check_course_env({"LLM_PROVIDER": "anthropic", "ANTHROPIC_API_KEY": "x",
                                  "OPENAI_API_KEY": "y"})
    assert [c.status for c in checks] == [cs.PASS, cs.PASS]


def test_doctor_never_prints_a_key():
    secret = "sk-VERY-SECRET-VALUE"
    for c in cs.check_course_env({"LLM_PROVIDER": "openai", "OPENAI_API_KEY": secret}):
        assert secret not in c.label + c.fix


def test_mock_api_down_is_only_a_warning(monkeypatch):
    import httpx

    def refuse(*a, **kw):
        raise httpx.ConnectError("refused")

    monkeypatch.setattr(httpx, "get", refuse)
    assert cs.check_mock_api().status == cs.WARN
