from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "lint_frontmatter.py"


def run_lint(content_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--content-dir", str(content_dir)],
        capture_output=True,
        text=True,
        check=False,
    )


def write_post(path: Path, frontmatter: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter}\n---\nbody\n", encoding="utf-8")


def test_passes_on_clean_content(tmp_path: Path) -> None:
    write_post(
        tmp_path / "post" / "a" / "index.md",
        'title: "A"\ntags: ["Foo", "Bar"]\ncategories: ["Baz"]\n',
    )
    write_post(
        tmp_path / "post" / "b" / "index.md",
        'title: "B"\ntags: ["Bar"]\ncategories: ["Baz"]\n',
    )

    result = run_lint(tmp_path)

    assert result.returncode == 0, result.stdout
    assert "frontmatter lint OK" in result.stdout


def test_detects_non_ascii_frontmatter_key(tmp_path: Path) -> None:
    write_post(
        tmp_path / "post" / "a" / "index.md",
        'title: "A"\n１projects: []\n',
    )

    result = run_lint(tmp_path)

    assert result.returncode == 1
    assert "non-ASCII characters" in result.stdout
    assert "１projects" in result.stdout


def test_detects_tag_casing_mismatch(tmp_path: Path) -> None:
    write_post(
        tmp_path / "post" / "a" / "index.md",
        'title: "A"\ntags: ["Foo Bar"]\n',
    )
    write_post(
        tmp_path / "post" / "b" / "index.md",
        'title: "B"\ntags: ["foo bar"]\n',
    )

    result = run_lint(tmp_path)

    assert result.returncode == 1
    assert "inconsistent casing" in result.stdout
    assert "'Foo Bar'" in result.stdout
    assert "'foo bar'" in result.stdout


def test_known_casing_exception_is_reported_as_warning_not_failure(
    tmp_path: Path,
) -> None:
    write_post(
        tmp_path / "post" / "a" / "index.md",
        'title: "A"\ntags: ["Invited talk"]\n',
    )
    write_post(
        tmp_path / "post" / "b" / "index.md",
        'title: "B"\ntags: ["Invited Talk"]\n',
    )

    result = run_lint(tmp_path)

    assert result.returncode == 0, result.stdout
    assert "Known pre-existing casing issues" in result.stdout
    assert "Invited talk" in result.stdout


def test_poster_registration_passes_when_all_assets_and_frontmatter_exist(
    tmp_path: Path,
) -> None:
    publication_dir = tmp_path / "publication" / "sample2026conf"
    write_post(
        publication_dir / "index.md",
        'title: "Sample Poster"\n'
        'tags: ["Posters"]\n'
        "url_poster: publication/sample2026conf/poster.pdf",
    )
    (publication_dir / "poster.pdf").write_bytes(b"%PDF-1.7\n")
    (publication_dir / "poster-thumbnail.webp").write_bytes(b"WEBP")

    result = run_lint(tmp_path)

    assert result.returncode == 0, result.stdout


def test_poster_pdf_requires_projects_registration(tmp_path: Path) -> None:
    publication_dir = tmp_path / "publication" / "sample2026conf"
    write_post(
        publication_dir / "index.md",
        'title: "Sample Poster"\ntags: []\nurl_poster: ""',
    )
    (publication_dir / "poster.pdf").write_bytes(b"%PDF-1.7\n")

    result = run_lint(tmp_path)

    assert result.returncode == 1
    assert "requires the exact tag 'Posters'" in result.stdout
    assert (
        "requires url_poster 'publication/sample2026conf/poster.pdf'" in result.stdout
    )
    assert "requires poster-thumbnail.webp" in result.stdout


def test_posters_tag_requires_poster_pdf(tmp_path: Path) -> None:
    publication_dir = tmp_path / "publication" / "sample2026conf"
    write_post(
        publication_dir / "index.md",
        'title: "Sample Poster"\ntags: ["Posters"]\nurl_poster: ""',
    )

    result = run_lint(tmp_path)

    assert result.returncode == 1
    assert "tag 'Posters' requires poster.pdf" in result.stdout


def test_poster_url_requires_projects_registration(tmp_path: Path) -> None:
    publication_dir = tmp_path / "publication" / "sample2026conf"
    write_post(
        publication_dir / "index.md",
        'title: "Sample Poster"\ntags: []\nurl_poster: https://example.com/poster.pdf',
    )

    result = run_lint(tmp_path)

    assert result.returncode == 1
    assert "url_poster requires poster.pdf" in result.stdout


def test_poster_thumbnail_requires_projects_registration(tmp_path: Path) -> None:
    publication_dir = tmp_path / "publication" / "sample2026conf"
    write_post(
        publication_dir / "index.md",
        'title: "Sample Poster"\ntags: []\nurl_poster: ""',
    )
    (publication_dir / "poster-thumbnail.webp").write_bytes(b"WEBP")

    result = run_lint(tmp_path)

    assert result.returncode == 1
    assert "poster-thumbnail.webp requires poster.pdf" in result.stdout


def test_poster_pdf_requires_publication_frontmatter(tmp_path: Path) -> None:
    publication_dir = tmp_path / "publication" / "sample2026conf"
    publication_dir.mkdir(parents=True)
    (publication_dir / "poster.pdf").write_bytes(b"%PDF-1.7\n")

    result = run_lint(tmp_path)

    assert result.returncode == 1
    assert "poster.pdf requires publication index.md" in result.stdout
