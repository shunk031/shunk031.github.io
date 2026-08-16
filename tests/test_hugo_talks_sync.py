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

    entries = module.parse_feed_entries(feed, "https://speakerdeck.com/shunk031.rss")

    assert len(entries) == 1
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

    result = module.audit(tmp_path, ["https://speakerdeck.com/shunk031.rss"])

    assert result["existing_count"] == 1
    assert result["candidate_count"] == 1
    assert result["existing"][0]["existing_path"] == "content/event/existing-talk/index.md"
    assert result["candidates"][0]["source_url"] == "https://speakerdeck.com/shunk031/missing-talk"
    assert result["candidates"][0]["suggested_intake_inputs"] == [
        "https://speakerdeck.com/shunk031/missing-talk",
        "https://example.com/missing",
    ]
