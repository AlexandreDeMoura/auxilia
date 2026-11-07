import json

import httpx
import pytest
from pydantic import BaseModel, TypeAdapter

from app.utils.remote_catalog import RemoteCatalog


class Entry(BaseModel):
    id: str
    label: str


BUNDLED = [Entry(id="shared", label="Bundled"), Entry(id="bundled", label="Kept")]
HOSTED = [Entry(id="remote", label="Added"), Entry(id="shared", label="Hosted")]
MERGED = [
    Entry(id="shared", label="Hosted"),
    Entry(id="bundled", label="Kept"),
    Entry(id="remote", label="Added"),
]


def document(entries):
    return json.dumps([entry.model_dump() for entry in entries])


@pytest.fixture
def hosted(monkeypatch):
    response = {"text": document(HOSTED), "status": 200}

    async def get(self, url):
        return httpx.Response(
            response["status"], text=response["text"], request=httpx.Request("GET", url)
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", get)
    return response


@pytest.fixture
def catalog_factory(tmp_path):
    bundled_path = tmp_path / "catalog.json"
    bundled_path.write_text(document(BUNDLED))

    def create(**options):
        options.setdefault("url", lambda: "https://example.test/catalog.json")
        return RemoteCatalog(
            prefix="test:catalog",
            item_model=Entry,
            parse=TypeAdapter(list[Entry]).validate_json,
            key=lambda entry: entry.id,
            bundled_path=bundled_path,
            **options,
        )

    return create


async def test_merge_keeps_bundled_order_and_overrides_whole_entries(
    catalog_factory, hosted
):
    catalog = catalog_factory(merge_with_bundled=True)

    assert await catalog.get() == MERGED


async def test_sync_diffs_effective_lists_and_can_remove_hosted_only_entries(
    catalog_factory, hosted
):
    catalog = catalog_factory(merge_with_bundled=True)
    assert await catalog.get() == MERGED
    hosted["text"] = document(
        [Entry(id="shared", label="Updated"), Entry(id="new", label="New")]
    )

    result = await catalog.sync()

    assert result.added == ["new"]
    assert result.removed == ["remote"]
    assert result.count == 3
    assert await catalog.get() == [
        Entry(id="shared", label="Updated"),
        Entry(id="bundled", label="Kept"),
        Entry(id="new", label="New"),
    ]


@pytest.mark.parametrize("source", ["memo", "redis", "last_good"])
@pytest.mark.parametrize("failure", ["http", "invalid"])
async def test_cached_layers_keep_the_merge_when_hosted_file_breaks(
    catalog_factory, hosted, fake_shared_redis, source, failure
):
    catalog = catalog_factory(merge_with_bundled=True)
    assert await catalog.get() == MERGED
    if failure == "http":
        hosted["status"] = 503
    else:
        # Even a valid first entry must not partially replace the last good file.
        hosted["text"] = '[{"id": "shared", "label": "Bad update"}, {"id": "invalid"}]'
    if source != "memo":
        catalog.invalidate_memo()
    if source == "last_good":
        await fake_shared_redis.delete(catalog.cache_key)

    assert await catalog.get() == MERGED


@pytest.mark.parametrize("source", ["redis", "last_good"])
async def test_shared_cache_is_merged_with_each_releases_own_bundle(
    catalog_factory, hosted, fake_shared_redis, tmp_path, source
):
    previous_release = catalog_factory(merge_with_bundled=True)
    assert await previous_release.get() == MERGED
    (tmp_path / "catalog.json").write_text(
        document([Entry(id="new-bundled", label="New release")])
    )
    hosted["status"] = 503
    if source == "last_good":
        await fake_shared_redis.delete(previous_release.cache_key)

    current_release = catalog_factory(merge_with_bundled=True)
    assert await current_release.get() == [
        Entry(id="new-bundled", label="New release"),
        Entry(id="remote", label="Added"),
        Entry(id="shared", label="Hosted"),
    ]


@pytest.mark.parametrize("failure", ["http", "invalid"])
async def test_no_good_hosted_file_falls_back_to_bundle(
    catalog_factory, hosted, failure
):
    catalog = catalog_factory(merge_with_bundled=True)
    if failure == "http":
        hosted["status"] = 503
    else:
        hosted["text"] = "not JSON"

    assert await catalog.get() == BUNDLED


@pytest.mark.parametrize("url", [None, ""])
async def test_disabling_url_ignores_previous_memo_and_cache(
    catalog_factory, hosted, url
):
    source = {"url": "https://example.test/catalog.json"}
    catalog = catalog_factory(merge_with_bundled=True, url=lambda: source["url"])
    assert await catalog.get() == MERGED
    source["url"] = url

    assert await catalog.get() == BUNDLED


async def test_merge_is_opt_in(catalog_factory, hosted):
    catalog = catalog_factory()
    assert await catalog.get() == HOSTED
    hosted["text"] = document([Entry(id="replacement", label="Replacement")])

    result = await catalog.sync()

    assert result.added == ["replacement"]
    assert result.removed == ["remote", "shared"]
    assert result.count == 1
    assert await catalog.get() == [Entry(id="replacement", label="Replacement")]


@pytest.mark.parametrize("failure", ["http", "invalid"])
async def test_failed_sync_raises_and_preserves_the_working_catalog(
    catalog_factory, hosted, failure
):
    catalog = catalog_factory(merge_with_bundled=True)
    assert await catalog.get() == MERGED
    if failure == "http":
        hosted["status"] = 503
    else:
        hosted["text"] = "not JSON"

    with pytest.raises((httpx.HTTPError, ValueError)):
        await catalog.sync()

    catalog.invalidate_memo()
    assert await catalog.get() == MERGED
