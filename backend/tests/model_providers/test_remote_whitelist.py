import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel

from app.model_providers import whitelist
from app.model_providers.models import ModelDB
from app.model_providers.pricing import TokenPrices
from app.model_providers.service import ModelService


HOSTED = """
schema_version: 1
models:
  - provider: anthropic
    model_id: claude-sonnet-5
    display_name: Hosted Sonnet
    multimodal: false
    reasoning_effort_levels: [low, high]
    reasoning_effort_default: low
    prices: {input: '1e-6', input_cache_read: '1e-7', output: '2e-6'}
  - provider: anthropic
    model_id: hosted-only-model
    display_name: Hosted only
"""


@pytest.fixture
def hosted_whitelist(monkeypatch):
    monkeypatch.setattr(
        whitelist.model_provider_settings,
        "model_whitelist_url",
        "https://example.test/whitelist.yaml",
    )
    response = {"text": HOSTED, "status": 200}

    async def get(self, url):
        return httpx.Response(
            response["status"], text=response["text"], request=httpx.Request("GET", url)
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", get)
    whitelist._catalog.invalidate_memo()
    yield response
    whitelist._catalog.invalidate_memo()


async def test_stale_whitelist_keeps_bundled_model_manageable_and_runnable(
    hosted_whitelist, monkeypatch, tmp_path
):
    monkeypatch.setattr(
        "app.model_providers.service.provider_api_keys",
        lambda: {"anthropic": "test-key"},
    )
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'models.db'}")

    def create_tables(conn):
        SQLModel.metadata.create_all(conn, tables=[ModelDB.__table__])

    try:
        async with engine.begin() as conn:
            await conn.run_sync(create_tables)
        async with AsyncSession(engine, expire_on_commit=False) as db:
            service = ModelService(db)
            managed = {model.model_id: model for model in await service.list_manage()}
            assert managed["claude-haiku-5-5"].is_enabled is False
            assert managed["claude-haiku-5-5"].deprecated is False

            enabled = await service.set_enabled("anthropic", "claude-haiku-5-5", True)
            assert enabled.is_enabled is True
            assert [model.model_id for model in await service.list_available()] == [
                "claude-haiku-5-5"
            ]
            resolved = await service.ensure_available("claude-haiku-5-5")
            assert resolved.model_id == "claude-haiku-5-5"
            assert resolved.provider == "anthropic"
            assert resolved.api_key == "test-key"
    finally:
        await engine.dispose()


async def test_hosted_entries_replace_all_metadata_and_extend_the_whitelist(
    hosted_whitelist,
):
    models = {model.model_id: model for model in await whitelist.get_whitelist()}

    assert "claude-haiku-5-5" in models
    assert models["hosted-only-model"].display_name == "Hosted only"
    shared = models["claude-sonnet-5"]
    assert shared.display_name == "Hosted Sonnet"
    assert shared.multimodal is False
    assert shared.supports_structured_output is False
    assert shared.reasoning_effort_levels == ["low", "high"]
    assert shared.reasoning_effort_default == "low"
    assert shared.prices == TokenPrices(
        input="1e-6", input_cache_read="1e-7", output="2e-6"
    )


async def test_sync_stale_whitelist_reports_no_bundled_removals(hosted_whitelist):
    before = await whitelist.get_whitelist()

    result = await ModelService.sync()

    assert result.added == []
    assert result.removed == []
    assert result.model_count == len(before)
    assert "claude-haiku-5-5" in {
        model.model_id for model in await whitelist.get_whitelist()
    }


async def test_invalid_hosted_whitelist_uses_last_good_as_a_whole(
    hosted_whitelist, fake_shared_redis
):
    before = await whitelist.get_whitelist()
    hosted_whitelist["text"] = (
        HOSTED.replace("Hosted Sonnet", "Partial update")
        + """
  - provider: unsupported
    model_id: invalid
    display_name: Invalid
"""
    )
    whitelist._catalog.invalidate_memo()
    await fake_shared_redis.delete(whitelist._catalog.cache_key)

    assert await whitelist.get_whitelist() == before


async def test_empty_url_serves_only_bundled_whitelist(hosted_whitelist, monkeypatch):
    await whitelist.get_whitelist()
    monkeypatch.setattr(whitelist.model_provider_settings, "model_whitelist_url", "")

    assert await whitelist.get_whitelist() == whitelist.bundled_whitelist()
