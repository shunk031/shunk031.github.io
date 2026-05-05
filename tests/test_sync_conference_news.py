from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "sync_conference_news.py"


def load_sync_conference_news_module():
    spec = importlib.util.spec_from_file_location("sync_conference_news", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_conf_key_uses_base_conference_for_findings_acceptance_news() -> None:
    module = load_sync_conference_news_module()

    conf = module.parse_conf_key(
        "Findings of CVPR 2026",
        "2026-02-21T00:00:00+00:00",
        ["International Conference"],
    )

    assert conf is not None
    assert conf.name == "CVPR"
    assert conf.year == "2026"
    assert conf.label == "Findings of CVPR 2026"
    assert conf.news_kind == module.NEWS_KIND_ACCEPTANCE


def test_render_news_markdown_keeps_conference_tags_for_acceptance_news() -> None:
    module = load_sync_conference_news_module()

    conf = module.ConferenceKey(
        name="CVPR",
        year="2026",
        display_label="Findings of CVPR 2026",
        news_kind=module.NEWS_KIND_ACCEPTANCE,
    )
    publications = [
        module.Publication(
            path=Path("content/publication/kawada2025sciga/index.md"),
            slug="kawada2025sciga",
            title="SciGA: A Comprehensive Dataset for Designing Graphical Abstracts in Academic Papers",
            authors=["Takuro Kawada", "Shunsuke Kitada"],
            date="2026-02-21T00:00:00+00:00",
            conf=conf,
        )
    ]

    markdown = module.render_news_markdown(
        conf,
        publications,
        author="Shunsuke Kitada",
        conference_date="2026-02-21T00:00:00+00:00",
        draft=False,
    )

    assert 'title: "Accepted our paper to Findings of CVPR 2026"' in markdown
    assert 'tags: ["News", "CVPR", "CVPR2026"]' in markdown
    assert "The following paper has been accepted to Findings of CVPR 2026:" in markdown


def test_sync_existing_news_tags_backfills_from_linked_publications(tmp_path: Path) -> None:
    module = load_sync_conference_news_module()

    news_dir = tmp_path / "content/news"
    news_file = news_dir / "acceptance-to-eccv2024/index.md"
    news_file.parent.mkdir(parents=True)
    news_file.write_text(
        """---
title: "Accepted our paper to ECCV2024"
tags: ["News"]
categories: ["News"]
---

- Paper: [Layout-Corrector](/publication/iwai2024layout)
""",
        encoding="utf-8",
    )

    io = module.FrontmatterIO()
    conf = module.ConferenceKey(
        name="ECCV",
        year="2024",
        display_label="ECCV2024",
        news_kind=module.NEWS_KIND_ACCEPTANCE,
    )
    publications_by_slug = {
        "iwai2024layout": module.Publication(
            path=Path("content/publication/iwai2024layout/index.md"),
            slug="iwai2024layout",
            title="Layout-Corrector",
            authors=["Shoma Iwai"],
            date="2024-07-01T00:00:00+09:00",
            conf=conf,
        )
    }

    modified, details = module.sync_existing_news_tags(
        news_dir,
        publications_by_slug,
        io,
        dry_run=False,
    )

    frontmatter, _ = io.read(news_file)
    assert modified == 1
    assert details == ["acceptance-to-eccv2024: +ECCV, ECCV2024"]
    assert list(frontmatter["tags"]) == ["News", "ECCV", "ECCV2024"]


def test_sync_existing_news_tags_falls_back_to_title_for_workshop_news(tmp_path: Path) -> None:
    module = load_sync_conference_news_module()

    news_dir = tmp_path / "content/news"
    news_file = news_dir / "acceptance-to-iccv2025-found-workshop/index.md"
    news_file.parent.mkdir(parents=True)
    news_file.write_text(
        """---
title: "Accepted our Workshop Proposal on Foundation Data to ICCV 2025"
tags: ["News"]
categories: ["News"]
---

No publication links yet.
""",
        encoding="utf-8",
    )

    io = module.FrontmatterIO()
    modified, details = module.sync_existing_news_tags(
        news_dir,
        {},
        io,
        dry_run=False,
    )

    frontmatter, _ = io.read(news_file)
    assert modified == 1
    assert details == ["acceptance-to-iccv2025-found-workshop: +ICCV, ICCV2025"]
    assert list(frontmatter["tags"]) == ["News", "ICCV", "ICCV2025"]


def test_sync_existing_news_tags_skips_journal_news_without_conference_year(tmp_path: Path) -> None:
    module = load_sync_conference_news_module()

    news_dir = tmp_path / "content/news"
    news_file = news_dir / "acceptance-to-ieee-access/index.md"
    news_file.parent.mkdir(parents=True)
    news_file.write_text(
        """---
title: "Accepted our journal paper to IEEE Access"
tags: ["News"]
categories: ["News"]
---

No conference information.
""",
        encoding="utf-8",
    )

    io = module.FrontmatterIO()
    modified, details = module.sync_existing_news_tags(
        news_dir,
        {},
        io,
        dry_run=False,
    )

    frontmatter, _ = io.read(news_file)
    assert modified == 0
    assert details == []
    assert list(frontmatter["tags"]) == ["News"]
