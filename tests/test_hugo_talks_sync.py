from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "hugo-talks-sync"
    / "scripts"
    / "hugo_talks_sync.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("hugo_talks_sync", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_rss_feed_extracts_deck_and_description_urls() -> None:
    module = load_module()
    feed = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <item>
      <title>[Event] Talk Title / Deck Title</title>
      <description>See https://example.com/event/42/ and https://github.com/example/code.</description>
      <media:content url="https://files.speakerdeck.com/preview.jpg" />
      <pubDate>Sat, 18 Jul 2026 00:00:00 -0400</pubDate>
      <link>https://speakerdeck.com/shunk031/deck-title</link>
      <guid>https://speakerdeck.com/shunk031/deck-title</guid>
    </item>
  </channel>
</rss>
"""

    source = module.SourceConfig(
        name="speakerdeck-shunk031",
        adapter="speakerdeck-profile",
        url="https://speakerdeck.com/shunk031.rss",
    )
    entries = module.parse_feed_entries(feed, source)

    assert len(entries) == 1
    assert entries[0].source_name == "speakerdeck-shunk031"
    assert entries[0].adapter == "speakerdeck-profile"
    assert entries[0].source_url == "https://speakerdeck.com/shunk031/deck-title"
    assert entries[0].image_url == "https://files.speakerdeck.com/preview.jpg"
    assert entries[0].extracted_urls == [
        "https://example.com/event/42/",
        "https://github.com/example/code",
    ]


def test_audit_marks_existing_deck_and_keeps_missing_candidate(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_module()
    event_dir = tmp_path / "content" / "event" / "existing-talk"
    event_dir.mkdir(parents=True)
    (event_dir / "index.md").write_text(
        """---
title: Existing
url_slides: https://speakerdeck.com/shunk031/existing-talk
---
body
""",
        encoding="utf-8",
    )
    feed = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item>
      <title>Existing Talk</title>
      <description></description>
      <pubDate>Sat, 18 Jul 2026 00:00:00 -0400</pubDate>
      <link>https://speakerdeck.com/shunk031/existing-talk</link>
      <guid>https://speakerdeck.com/shunk031/existing-talk</guid>
    </item>
    <item>
      <title>Missing Talk</title>
      <description>Event https://example.com/missing</description>
      <pubDate>Sun, 19 Jul 2026 00:00:00 -0400</pubDate>
      <link>https://speakerdeck.com/shunk031/missing-talk</link>
      <guid>https://speakerdeck.com/shunk031/missing-talk</guid>
    </item>
  </channel>
</rss>
"""
    monkeypatch.setattr(module, "read_text_url", lambda _url: feed)

    result = module.audit(
        tmp_path,
        [
            module.SourceConfig(
                name="speakerdeck-shunk031",
                adapter="speakerdeck-profile",
                url="https://speakerdeck.com/shunk031.rss",
            )
        ],
    )

    assert result["existing_count"] == 1
    assert result["candidate_count"] == 1
    assert result["existing"][0]["existing_path"] == "content/event/existing-talk/index.md"
    assert result["candidates"][0]["source_name"] == "speakerdeck-shunk031"
    assert result["candidates"][0]["source_type"] == "speakerdeck-profile"
    assert result["candidates"][0]["source_url"] == "https://speakerdeck.com/shunk031/missing-talk"
    assert result["candidates"][0]["suggested_intake_inputs"] == [
        "https://speakerdeck.com/shunk031/missing-talk",
        "https://example.com/missing",
    ]


def test_load_source_configs_supports_profile_and_generic_feed(tmp_path: Path) -> None:
    module = load_module()
    config_path = tmp_path / "sources.json"
    config_path.write_text(
        """{
  "sources": [
    {
      "name": "speakerdeck-shunk031",
      "type": "speakerdeck-profile",
      "profile_url": "https://speakerdeck.com/shunk031"
    },
    {
      "name": "personal-talk-feed",
      "type": "feed",
      "url": "https://example.com/talks.atom"
    }
  ]
}
""",
        encoding="utf-8",
    )

    sources = module.load_source_configs(config_path)

    assert sources == [
        module.SourceConfig(
            name="speakerdeck-shunk031",
            adapter="speakerdeck-profile",
            url="https://speakerdeck.com/shunk031.rss",
            options={"profile_url": "https://speakerdeck.com/shunk031"},
        ),
        module.SourceConfig(
            name="personal-talk-feed",
            adapter="feed",
            url="https://example.com/talks.atom",
        ),
    ]


def test_load_source_configs_preserves_explicit_adapter_and_options(
    tmp_path: Path,
) -> None:
    module = load_module()
    config_path = tmp_path / "sources.json"
    config_path.write_text(
        """{
  "sources": [
    {
      "name": "personal-talks",
      "adapter": "atom",
      "url": "https://example.com/talks.atom",
      "options": {
        "owner": "shunk031",
        "selector": ".talk"
      }
    }
  ]
}
""",
        encoding="utf-8",
    )

    sources = module.load_source_configs(config_path)

    assert sources == [
        module.SourceConfig(
            name="personal-talks",
            adapter="atom",
            url="https://example.com/talks.atom",
            options={"owner": "shunk031", "selector": ".talk"},
        )
    ]


def test_default_sources_use_requested_profile_name_and_feed_url() -> None:
    module = load_module()

    sources = module.default_sources("https://speakerdeck.com/example-user")

    assert sources == [
        module.SourceConfig(
            name="speakerdeck-com-example-user",
            adapter="speakerdeck-profile",
            url="https://speakerdeck.com/example-user.rss",
            options={"profile_url": "https://speakerdeck.com/example-user"},
        )
    ]


def test_explicit_rss_adapter_rejects_atom_xml() -> None:
    module = load_module()
    source = module.SourceConfig(
        name="rss-source",
        adapter="rss",
        url="https://example.com/talks.rss",
    )
    atom_feed = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry><title>Atom Talk</title></entry>
</feed>
"""

    try:
        module.parse_feed_entries(atom_feed, source)
    except ValueError as exc:
        assert "expected RSS XML" in str(exc)
    else:
        raise AssertionError("explicit rss adapter accepted Atom XML")


def test_unknown_auto_feed_xml_fails_closed() -> None:
    module = load_module()
    source = module.SourceConfig(
        name="unknown-source",
        adapter="feed",
        url="https://example.com/feed.xml",
    )

    try:
        module.parse_feed_entries("<items></items>", source)
    except ValueError as exc:
        assert "neither RSS nor Atom" in str(exc)
    else:
        raise AssertionError("unknown XML root was treated as an empty feed")


def test_audit_supports_multiple_source_adapters(tmp_path: Path, monkeypatch) -> None:
    module = load_module()
    (tmp_path / "content" / "event").mkdir(parents=True)
    rss_feed = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item>
      <title>RSS Talk</title>
      <description>Event https://example.com/rss-event</description>
      <pubDate>Sun, 19 Jul 2026 00:00:00 -0400</pubDate>
      <link>https://slides.example.com/rss-talk</link>
      <guid>https://slides.example.com/rss-talk</guid>
    </item>
  </channel>
</rss>
"""
    atom_feed = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Atom Talk</title>
    <link rel="alternate" href="https://video.example.com/atom-talk" />
    <updated>2026-07-20T00:00:00Z</updated>
    <summary>Video https://example.com/atom-event</summary>
  </entry>
</feed>
"""
    feeds = {
        "https://example.com/talks.rss": rss_feed,
        "https://example.com/talks.atom": atom_feed,
    }
    monkeypatch.setattr(module, "read_text_url", lambda url: feeds[url])

    result = module.audit(
        tmp_path,
        [
            module.SourceConfig(
                name="rss-source",
                adapter="feed",
                url="https://example.com/talks.rss",
            ),
            module.SourceConfig(
                name="atom-source",
                adapter="feed",
                url="https://example.com/talks.atom",
            ),
        ],
    )

    assert result["candidate_count"] == 2
    assert [
        (item["source_name"], item["source_type"], item["source_url"])
        for item in result["candidates"]
    ] == [
        ("rss-source", "feed", "https://slides.example.com/rss-talk"),
        ("atom-source", "feed", "https://video.example.com/atom-talk"),
    ]


def test_audit_deduplicates_same_candidate_across_sources(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_module()
    (tmp_path / "content" / "event").mkdir(parents=True)
    rss_feed = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item>
      <title>Shared Talk</title>
      <description></description>
      <pubDate>Sun, 19 Jul 2026 00:00:00 -0400</pubDate>
      <link>https://slides.example.com/shared-talk</link>
      <guid>https://slides.example.com/shared-talk</guid>
    </item>
  </channel>
</rss>
"""
    feeds = {
        "https://example.com/one.rss": rss_feed,
        "https://example.com/two.rss": rss_feed,
    }
    monkeypatch.setattr(module, "read_text_url", lambda url: feeds[url])

    result = module.audit(
        tmp_path,
        [
            module.SourceConfig(
                name="first",
                adapter="rss",
                url="https://example.com/one.rss",
            ),
            module.SourceConfig(
                name="second",
                adapter="rss",
                url="https://example.com/two.rss",
            ),
        ],
    )

    assert result["candidate_count"] == 1
    assert result["duplicate_count"] == 1
    assert result["duplicates"][0]["source_name"] == "second"
    assert result["duplicates"][0]["duplicate_of"] == "https://slides.example.com/shared-talk"
