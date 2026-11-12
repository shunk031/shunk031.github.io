"""Regression checks for public, agent-facing site content.

The Hugo deployment build checks rendering. These lightweight checks guard
the source templates and discovery guide without requiring network access.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_llms_txt_includes_actionable_when_to_use_guidance() -> None:
    text = (ROOT / "static" / "llms.txt").read_text(encoding="utf-8")
    assert text.startswith("# Shunsuke Kitada")
    assert "## When to use this site" in text
    assert "ordinary GET requests" in text
    assert "not an agent tool, authenticated service, or API endpoint" in text

    for url in (
        "https://shunk031.me/authors/shunsuke-kitada/",
        "https://shunk031.me/publication/",
        "https://shunk031.me/#projects",
        "https://shunk031.me/event/",
        "https://shunk031.me/#recent-news",
        "https://shunk031.me/sitemap.xml",
    ):
        assert url in text


def test_project_card_headings_are_level_two_with_previous_visual_size() -> None:
    template = (ROOT / "layouts" / "partials" / "views" / "masonry.html").read_text(
        encoding="utf-8"
    )
    assert '<h2 class="h4"><a href="{{ $link }}"' in template
    assert "</a></h2>" in template
    assert "<h4>" not in template


def test_homepage_biography_is_rendered_by_hugo_without_javascript() -> None:
    homepage = (ROOT / "content" / "_index.md").read_text(encoding="utf-8")
    template = (ROOT / "layouts" / "partials" / "blocks" / "about.biography.html").read_text(
        encoding="utf-8"
    )
    profile = (
        ROOT / "content" / "authors" / "shunsuke-kitada" / "_index.md"
    ).read_text(encoding="utf-8")

    assert "block: about.biography" in homepage
    assert '{{ with $person_page.Content }}' in template
    assert '{{ . }}' in template
    assert '<div class="article-style">' in template
    # Site metadata / scripts are not a substitute for a substantial bio.
    assert len(profile.split("---", 2)[-1].strip()) >= 500
