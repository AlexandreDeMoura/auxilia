from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from app.agents.runtime import (
    AgentRuntime,
    _resolve_thread_thinking_mode,
    _resolve_web_thinking_mode,
)
from app.model_providers.catalog import Model, ModelProvider
from app.threads.models import ThreadDB
from app.users.models import UserDB


def _make_thread(
    *,
    thinking_enabled: bool | None = None,
    thinking_effort: str | None = None,
) -> ThreadDB:
    return ThreadDB(
        id=str(uuid4()),
        user_id=uuid4(),
        agent_id=uuid4(),
        model_id="test-model",
        thinking_enabled=thinking_enabled,
        thinking_effort=thinking_effort,
    )


def test_resolve_thread_thinking_mode_defaults_to_medium_for_effort_models():
    thread = _make_thread()

    mode = _resolve_thread_thinking_mode(
        thread,
        supports_thinking=True,
        supports_thinking_effort=True,
    )

    assert mode == "medium"


def test_resolve_thread_thinking_mode_for_non_effort_models():
    thread = _make_thread(thinking_enabled=None, thinking_effort="high")

    mode = _resolve_thread_thinking_mode(
        thread,
        supports_thinking=True,
        supports_thinking_effort=False,
    )

    assert mode == "on"


def test_resolve_thread_thinking_mode_off_when_model_does_not_support_thinking():
    thread = _make_thread(thinking_enabled=True, thinking_effort="high")

    mode = _resolve_thread_thinking_mode(
        thread,
        supports_thinking=False,
        supports_thinking_effort=False,
    )

    assert mode == "off"


async def test_resolve_web_thinking_mode_returns_legacy_when_opt_out():
    thread = _make_thread(thinking_enabled=True, thinking_effort="high")
    db = AsyncMock()
    db.get.return_value = UserDB(
        id=thread.user_id,
        name="User",
        email="user@example.com",
        thinking_controls_enabled=False,
    )

    mode = await _resolve_web_thinking_mode(
        db,
        thread,
        supports_thinking=True,
        supports_thinking_effort=True,
    )

    assert mode is None


@pytest.mark.asyncio
@patch("app.agents.runtime.ChatModelFactory.create")
@patch("app.agents.runtime.Agent.resolve", new_callable=AsyncMock)
@patch("app.agents.runtime._resolve_web_thinking_mode", new_callable=AsyncMock)
async def test_build_web_uses_resolved_thinking_mode(
    resolve_web_mode,
    resolve_agent,
    create_model,
):
    thread = _make_thread(thinking_enabled=True, thinking_effort="high")
    db = AsyncMock()
    resolve_web_mode.return_value = "high"
    resolve_agent.return_value = MagicMock(
        config=MagicMock(subagents=None),
        toolset=MagicMock(interrupt_on={}),
    )
    create_model.return_value = MagicMock()

    model = Model(
        name="test-model",
        provider="anthropic",
        display_name="Test",
        chef="Chef",
        chef_slug="chef",
        supports_thinking=True,
        supports_thinking_effort=True,
    )
    provider = ModelProvider(name="anthropic", api_key="secret")

    with (
        patch("app.agents.runtime.MODELS", [model]),
        patch("app.agents.runtime.LLM_PROVIDERS", [provider]),
    ):
        await AgentRuntime.build(thread=thread, db=db, invocation_source="web")

    resolve_web_mode.assert_awaited_once_with(
        db,
        thread,
        supports_thinking=True,
        supports_thinking_effort=True,
    )
    create_model.assert_called_once_with(
        "anthropic",
        "test-model",
        "secret",
        effort="high",
    )


@pytest.mark.asyncio
@patch("app.agents.runtime.ChatModelFactory.create")
@patch("app.agents.runtime.Agent.resolve", new_callable=AsyncMock)
@patch("app.agents.runtime._resolve_web_thinking_mode", new_callable=AsyncMock)
async def test_build_slack_forces_legacy_thinking(
    resolve_web_mode,
    resolve_agent,
    create_model,
):
    thread = _make_thread(thinking_enabled=True, thinking_effort="high")
    db = AsyncMock()
    resolve_web_mode.return_value = "high"
    resolve_agent.return_value = MagicMock(
        config=MagicMock(subagents=None),
        toolset=MagicMock(interrupt_on={}),
    )
    create_model.return_value = MagicMock()

    model = Model(
        name="test-model",
        provider="anthropic",
        display_name="Test",
        chef="Chef",
        chef_slug="chef",
        supports_thinking=True,
        supports_thinking_effort=True,
    )
    provider = ModelProvider(name="anthropic", api_key="secret")

    with (
        patch("app.agents.runtime.MODELS", [model]),
        patch("app.agents.runtime.LLM_PROVIDERS", [provider]),
    ):
        await AgentRuntime.build(thread=thread, db=db, invocation_source="slack")

    resolve_web_mode.assert_not_called()
    create_model.assert_called_once_with(
        "anthropic",
        "test-model",
        "secret",
        effort=None,
    )
