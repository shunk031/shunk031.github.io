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
