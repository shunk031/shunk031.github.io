from __future__ import annotations

import importlib.util
import json
import os
import stat
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "hugo-event-intake"
    / "scripts"
    / "hugo_event_intake.py"
)


def load_module():
    assert SCRIPT_PATH.exists(), f"missing script: {SCRIPT_PATH}"
    spec = importlib.util.spec_from_file_location("hugo_event_intake", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_existing_event(repo_root: Path, *, slug: str, url_slides: str = "", event_url: str = "") -> None:
    event_dir = repo_root / "content" / "event" / slug
    event_dir.mkdir(parents=True, exist_ok=True)
    (event_dir / "index.md").write_text(
        "\n".join(
            [
                "---",
                'title: "Existing Event"',
                'event: "Existing Event"',
                f"url_slides: {json.dumps(url_slides)}",
                f"event_url: {json.dumps(event_url)}",
                "---",
                "",
            ]
        ),
        encoding="utf-8",
    )


def install_fake_command(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def test_probe_detects_duplicate_before_fetch(tmp_path: Path) -> None:
    module = load_module()
    repo_root = tmp_path / "repo"
    write_existing_event(
        repo_root,
        slug="existing-talk",
        url_slides="https://speakerdeck.com/shunk031/existing-talk",
    )

    def fail_fetch(*args, **kwargs):
        raise AssertionError("network fetch should not happen for duplicates")

    result = module.probe_event(
        repo_root,
        inputs=["https://speakerdeck.com/shunk031/existing-talk"],
        fetch_text_response=fail_fetch,
        fetch_json=fail_fetch,
    )

    assert result.duplicate_of == "content/event/existing-talk/index.md"
    assert result.unresolved_fields == []


def test_probe_follows_event_page_links_and_uses_jsonld_event_fields(tmp_path: Path) -> None:
    module = load_module()
    repo_root = tmp_path / "repo"
    (repo_root / "content" / "event").mkdir(parents=True, exist_ok=True)

    event_html = """
    <html>
      <head>
        <title>PyData Tokyo #1</title>
        <meta property="og:description" content="Deep learning for the impatient.">
        <meta property="og:image" content="https://example.com/poster.png">
      </head>
      <body>
        <a href="https://speakerdeck.com/shunk031/deep-learning-for-the-impatient">Slides</a>
        <script type="application/ld+json">
          {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": "PyData Tokyo #1",
            "startDate": "2026-12-03T19:00:00+09:00",
            "endDate": "2026-12-03T20:00:00+09:00",
            "location": {
              "@type": "Place",
              "name": "Shibuya Stream",
              "address": {
                "@type": "PostalAddress",
                "streetAddress": "1-2-3 Shibuya",
                "addressLocality": "Shibuya-ku",
                "addressRegion": "Tokyo",
                "postalCode": "150-0002",
                "addressCountry": "Japan"
              }
            }
          }
        </script>
      </body>
    </html>
    """
    speakerdeck_html = """
    <html>
      <head>
        <meta property="og:title" content="[PyData Tokyo #1] Deep Learning for the Impatient / deep-learning-for-the-impatient">
        <meta property="og:description" content="A pragmatic overview of deep learning workflows.">
        <meta property="og:image" content="https://files.speakerdeck.com/presentations/abc123/slide_0.jpg">
      </head>
      <body>
        <div class="speakerdeck-embed" data-id="abc123" data-ratio="1.7777777777777777"></div>
      </body>
    </html>
    """

    def fake_fetch_text(url: str):
        if url == "https://example.com/events/pydata-tokyo-1":
            return module.RemoteResponse(url=url, content_type="text/html", text=event_html, data=event_html.encode())
        if url == "https://speakerdeck.com/shunk031/deep-learning-for-the-impatient":
            return module.RemoteResponse(url=url, content_type="text/html", text=speakerdeck_html, data=speakerdeck_html.encode())
        raise AssertionError(f"unexpected url: {url}")

    def fake_fetch_json(url: str):
        assert url == "https://speakerdeck.com/oembed.json?url=https%3A%2F%2Fspeakerdeck.com%2Fshunk031%2Fdeep-learning-for-the-impatient"
        return {
            "title": "[PyData Tokyo #1] Deep Learning for the Impatient / deep-learning-for-the-impatient",
            "author_name": "Shunsuke KITADA",
            "ratio": 1.7777777777777777,
        }

    result = module.probe_event(
        repo_root,
        inputs=["https://example.com/events/pydata-tokyo-1"],
        fetch_text_response=fake_fetch_text,
        fetch_json=fake_fetch_json,
    )

    assert result.duplicate_of == ""
    assert result.event == "PyData Tokyo #1"
    assert result.title == "[Invited Talk] Deep Learning for the Impatient"
    assert result.date == "2026-12-03T19:00:00+09:00"
    assert result.date_end == "2026-12-03T20:00:00+09:00"
    assert result.location == "Shibuya Stream"
    assert result.address["city"] == "Shibuya-ku"
    assert result.url_slides == "https://speakerdeck.com/shunk031/deep-learning-for-the-impatient"
    assert result.event_url == "https://example.com/events/pydata-tokyo-1"
    assert result.featured_source_url == "https://files.speakerdeck.com/presentations/abc123/slide_0.jpg"
    assert result.unresolved_fields == []


def test_probe_infers_journal_club_and_report_tags() -> None:
    module = load_module()

    assert module.infer_kind(
        notes=["KDD2026 論文読み会で話す"],
        sources=[],
        explicit_kind="",
    ) == "Journal Club"
    assert module.default_tags_for_kind("Journal Club") == ["Journal Club", "Paper Reading"]
    assert module.render_title("Report", "ECCV 2026 速報") == "ECCV 2026 速報"
    assert module.render_title("Invited Talk", "Practical ML") == "[Invited Talk] Practical ML"


def test_write_event_downloads_featured_image_and_renders_body(tmp_path: Path) -> None:
    module = load_module()
    repo_root = tmp_path / "repo"
    (repo_root / "content" / "event").mkdir(parents=True, exist_ok=True)
    spec = module.EventSpec(
        slug="practical-ml",
        kind="Invited Talk",
        title="[Invited Talk] Practical ML",
        event="PyData Tokyo #1",
        event_url="https://example.com/events/pydata-tokyo-1",
        location="Shibuya Stream",
        address={
            "street": "1-2-3 Shibuya",
            "city": "Shibuya-ku",
            "region": "Tokyo",
            "postcode": "150-0002",
            "country": "Japan",
        },
        summary="Deep learning for the impatient.",
        abstract="Deep learning for the impatient.",
        date="2026-12-03T19:00:00+09:00",
        date_end="2026-12-03T20:00:00+09:00",
        publish_date="2026-11-01T09:00:00+09:00",
        authors=["Shunsuke Kitada"],
        tags=["Invited Talk"],
        url_slides="https://speakerdeck.com/shunk031/deep-learning-for-the-impatient",
        url_pdf="",
        url_video="",
        url_code="",
        links=[],
        body_markdown="## 資料 - Slides\n\n<script defer class=\"speakerdeck-embed\" data-id=\"abc123\" data-ratio=\"1.7777777777777777\" src=\"//speakerdeck.com/assets/embed.js\"></script>\n",
        featured_source_url="https://files.speakerdeck.com/presentations/abc123/slide_0.jpg",
        evidence_urls=[
            "https://example.com/events/pydata-tokyo-1",
            "https://speakerdeck.com/shunk031/deep-learning-for-the-impatient",
        ],
        unresolved_fields=[],
        duplicate_of="",
    )

    def fake_download(url: str):
        assert url == "https://files.speakerdeck.com/presentations/abc123/slide_0.jpg"
        return b"JPEGDATA", "image/jpeg"

    output_path = module.write_event(
        repo_root,
        spec,
        download_binary=fake_download,
    )

    assert output_path == repo_root / "content" / "event" / "practical-ml" / "index.md"
    markdown = output_path.read_text(encoding="utf-8")
    assert 'title: "[Invited Talk] Practical ML"' in markdown
    assert 'event: "PyData Tokyo #1"' in markdown
    assert 'url_slides: "https://speakerdeck.com/shunk031/deep-learning-for-the-impatient"' in markdown
    assert "<script defer class=\"speakerdeck-embed\"" in markdown
    assert (output_path.parent / "featured.jpg").read_bytes() == b"JPEGDATA"


def test_write_event_generates_thumbnail_from_pdf(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_module()
    repo_root = tmp_path / "repo"
    event_root = repo_root / "content" / "event"
    event_root.mkdir(parents=True, exist_ok=True)
    spec = module.EventSpec(
        slug="eccv-2026-report",
        kind="Report",
        title="ECCV 2026 速報",
        event="ECCV 2026 速報",
        event_url="https://example.com/eccv2026.pdf",
        location="",
        address=module.empty_address(),
        summary="Conference report.",
        abstract="",
        date="2026-10-07T11:00:00+09:00",
        date_end="2026-10-07T11:00:00+09:00",
        publish_date="2026-10-07T11:00:00+09:00",
        authors=["Shunsuke Kitada"],
        tags=[],
        url_slides="",
        url_pdf="https://example.com/eccv2026.pdf",
        url_video="",
        url_code="",
        links=[],
        body_markdown="## Links\n\n- [PDF](https://example.com/eccv2026.pdf)\n",
        featured_source_url="https://example.com/eccv2026.pdf",
        evidence_urls=["https://example.com/eccv2026.pdf"],
        unresolved_fields=[],
        duplicate_of="",
    )

    def fake_download(url: str):
        assert url == "https://example.com/eccv2026.pdf"
        return b"%PDF-1.7\n", "application/pdf"

    captured: dict[str, object] = {}

    def fake_run(*args, **kwargs):
        captured["args"] = args[0]
        output = event_root / "eccv-2026-report" / "featured.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"PNGDATA")

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    monkeypatch.setattr(module.shutil, "which", lambda name: "/usr/bin/magick" if name == "magick" else None)

    output_path = module.write_event(
        repo_root,
        spec,
        download_binary=fake_download,
    )

    assert output_path.exists()
    assert captured["args"][0] == "magick"
    assert (event_root / "eccv-2026-report" / "featured.png").read_bytes() == b"PNGDATA"


def test_write_event_rejects_existing_slug(tmp_path: Path) -> None:
    module = load_module()
    repo_root = tmp_path / "repo"
    write_existing_event(repo_root, slug="existing-talk", event_url="https://example.com/events/existing")
    spec = module.EventSpec(
        slug="existing-talk",
        kind="Invited Talk",
        title="[Invited Talk] Existing Talk",
        event="Existing Talk",
        event_url="https://example.com/events/existing",
        location="",
        address=module.empty_address(),
        summary="",
        abstract="",
        date="2026-01-01T10:00:00+09:00",
        date_end="2026-01-01T10:00:00+09:00",
        publish_date="2026-01-01T10:00:00+09:00",
        authors=["Shunsuke Kitada"],
        tags=["Invited Talk"],
        url_slides="",
        url_pdf="",
        url_video="",
        url_code="",
        links=[],
        body_markdown="",
        featured_source_url="",
        evidence_urls=[],
        unresolved_fields=[],
        duplicate_of="",
    )

    with pytest.raises(FileExistsError, match="already exists"):
        module.write_event(repo_root, spec)
