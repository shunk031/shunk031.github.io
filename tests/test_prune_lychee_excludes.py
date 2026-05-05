from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "prune_lychee_excludes.py"


def run_prune(
    tmp_path: Path,
    *,
    html: str,
    exclude_text: str,
    results: list[dict],
    pr_body_output: str | None = None,
) -> subprocess.CompletedProcess[str]:
    public_dir = tmp_path / "public"
    public_dir.mkdir()
    (public_dir / "index.html").write_text(html, encoding="utf-8")

    exclude_path = tmp_path / "exclude-temporary.txt"
    exclude_path.write_text(exclude_text, encoding="utf-8")

    json_path = tmp_path / "lychee-excludes.json"
    json_path.write_text(json.dumps(results), encoding="utf-8")

    command = [
        sys.executable,
        str(SCRIPT_PATH),
        "--public-dir",
        str(public_dir),
        "--json",
        str(json_path),
        "--exclude-file",
        str(exclude_path),
    ]
    if pr_body_output is not None:
        command.extend(["--pr-body-output", str(tmp_path / pr_body_output)])

    return subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )


def test_keeps_pattern_when_any_matched_url_is_missing_from_results(tmp_path: Path) -> None:
    result = run_prune(
        tmp_path,
        html="""
        <a href="https://scholar.google.com/citations?user=GUzGhQIAAAAJ">Kitada</a>
        <a href="https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_enggeneral">Metrics</a>
        """,
        exclude_text="scholar.google.com/citations\n",
        results=[
            {
                "url": "https://scholar.google.com/citations?user=GUzGhQIAAAAJ",
                "status": {"code": 200},
            }
        ],
    )

    exclude_path = tmp_path / "exclude-temporary.txt"
    assert exclude_path.read_text(encoding="utf-8") == "scholar.google.com/citations\n"
    assert result.stdout.strip() == "no change"


def test_keeps_pattern_when_a_matched_url_has_mixed_success_and_failure_statuses(tmp_path: Path) -> None:
    scholar_url = "https://scholar.google.com/citations?user=GUzGhQIAAAAJ"
    result = run_prune(
        tmp_path,
        html=f'<a href="{scholar_url}">Kitada</a>',
        exclude_text="scholar.google.com/citations\n",
        results=[
            {"url": scholar_url, "status": {"code": 200}},
            {"url": scholar_url, "status": {"code": 403}},
        ],
    )

    exclude_path = tmp_path / "exclude-temporary.txt"
    assert exclude_path.read_text(encoding="utf-8") == "scholar.google.com/citations\n"
    assert result.stdout.strip() == "no change"


def test_prunes_pattern_when_all_matched_urls_have_success_statuses(tmp_path: Path) -> None:
    result = run_prune(
        tmp_path,
        html="""
        <a href="https://example.com/a">A</a>
        <a href="https://example.com/b">B</a>
        """,
        exclude_text="example.com\n",
        results=[
            {"url": "https://example.com/a", "status": {"code": 200}},
            {"url": "https://example.com/b", "status": {"code": 302}},
        ],
    )

    exclude_path = tmp_path / "exclude-temporary.txt"
    assert exclude_path.read_text(encoding="utf-8") == ""
    assert result.stdout.strip() == "example.com"


def test_writes_pr_body_with_removed_patterns_and_recovered_urls(tmp_path: Path) -> None:
    result = run_prune(
        tmp_path,
        html="""
        <a href="https://example.com/a">A</a>
        <a href="https://example.com/b">B</a>
        """,
        exclude_text="example.com\n",
        results=[
            {"url": "https://example.com/a", "status": {"code": 200}},
            {"url": "https://example.com/b", "status": {"code": 302}},
        ],
        pr_body_output="pr-body.md",
    )

    pr_body_path = tmp_path / "pr-body.md"
    assert pr_body_path.read_text(encoding="utf-8") == (
        "Removed recovered URLs from temporary broken-link excludes because the scheduled check returned 2xx/302.\n"
        "\n"
        "## Recovered URLs\n"
        "\n"
        "### `example.com`\n"
        "- `https://example.com/a`\n"
        "- `https://example.com/b`\n"
    )
    assert result.stdout.strip() == "example.com"
