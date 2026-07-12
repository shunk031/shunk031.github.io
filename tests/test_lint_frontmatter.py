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
