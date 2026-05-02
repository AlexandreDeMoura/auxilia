from unittest.mock import patch

from app.model_providers.catalog import ChatModelFactory


@patch("app.model_providers.catalog.ChatAnthropic")
def test_anthropic_legacy_thinking_mapping(chat_anthropic):
    ChatModelFactory().create("anthropic", "claude-sonnet-4-6", "secret")

    assert chat_anthropic.call_count == 1
    kwargs = chat_anthropic.call_args.kwargs
    assert kwargs["thinking"] == {"type": "enabled", "budget_tokens": 1024}


@patch("app.model_providers.catalog.ChatAnthropic")
def test_anthropic_off_disables_thinking(chat_anthropic):
    ChatModelFactory().create("anthropic", "claude-sonnet-4-6", "secret", effort="off")

    assert chat_anthropic.call_count == 1
    kwargs = chat_anthropic.call_args.kwargs
    assert "thinking" not in kwargs


@patch("app.model_providers.catalog.ChatGoogleGenerativeAI")
def test_google_medium_effort_mapping(chat_google):
    ChatModelFactory().create(
        "google", "gemini-3-flash-preview", "secret", effort="medium"
    )

    assert chat_google.call_count == 1
    kwargs = chat_google.call_args.kwargs
    assert kwargs["include_thoughts"] is True
    assert kwargs["thinking_budget"] == 8192


@patch("app.model_providers.catalog.ChatGoogleGenerativeAI")
def test_google_off_disables_thinking(chat_google):
    ChatModelFactory().create(
        "google", "gemini-3-flash-preview", "secret", effort="off"
    )

    assert chat_google.call_count == 1
    kwargs = chat_google.call_args.kwargs
    assert kwargs["include_thoughts"] is False
    assert kwargs["thinking_budget"] == 0


@patch("app.model_providers.catalog.ChatDeepSeek")
def test_deepseek_legacy_is_disabled(chat_deepseek):
    ChatModelFactory().create("deepseek", "deepseek-chat", "secret")

    assert chat_deepseek.call_count == 1
    kwargs = chat_deepseek.call_args.kwargs
    assert kwargs["extra_body"] == {"thinking": {"type": "disabled"}}


@patch("app.model_providers.catalog.ChatDeepSeek")
def test_deepseek_on_enables_thinking(chat_deepseek):
    ChatModelFactory().create("deepseek", "deepseek-reasoner", "secret", effort="on")

    assert chat_deepseek.call_count == 1
    kwargs = chat_deepseek.call_args.kwargs
    assert kwargs["extra_body"] == {"thinking": {"type": "enabled"}}
