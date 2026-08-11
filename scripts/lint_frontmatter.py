#!/usr/bin/env python3
"""Lint Hugo content frontmatter for issues typo checkers cannot catch.

Checks:
  (a) Frontmatter keys containing non-ASCII characters. These are valid YAML
      (e.g. a full-width "１" glued onto "projects") but Hugo silently
      ignores the resulting key instead of erroring, so the config the key
      was meant to set never takes effect.
  (b) tags/categories values that share a casefolded spelling but differ in
      case (e.g. "Non-refereed" vs "Non-Refereed"). Both are valid English,
      so a spell checker won't flag them, but Hugo treats each spelling as a
      distinct taxonomy term and generates a separate (wrong) term page.
  (c) Partial publication poster registrations. The local PDF, canonical tag,
      URL, and dedicated thumbnail form one atomic Projects gallery contract.

Usage:
    python scripts/lint_frontmatter.py [--content-dir content]
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from collections import defaultdict
from collections.abc import Iterable
from io import StringIO
from typing import Any

from ruamel.yaml import YAML

FRONTMATTER_LIST_FIELDS = ("tags", "categories")
POSTER_TAG = "Posters"
POSTER_PDF = "poster.pdf"
POSTER_THUMBNAIL = "poster-thumbnail.webp"

# Pre-existing tag/category casing variants that predate this lint. They are
# reported as warnings (not build failures) until a dedicated content-cleanup
# PR normalizes them. Remove entries here as they get fixed upstream.
KNOWN_CASING_EXCEPTIONS: set[tuple[str, str]] = {
    ("tags", "invited talk"),
    ("categories", "multi-modal model"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lint Hugo content frontmatter for non-ASCII keys and tag/category casing drift."
    )
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--content-dir",
        type=pathlib.Path,
        default=repo_root / "content",
        help="Path to content directory (default: content/)",
    )
    return parser.parse_args()


def iter_markdown_files(content_dir: pathlib.Path) -> Iterable[pathlib.Path]:
    yield from sorted(content_dir.rglob("*.md"))


def load_frontmatter(path: pathlib.Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    yaml = YAML(typ="safe")
    data = yaml.load(StringIO(parts[1]))
    if not isinstance(data, dict):
        return None
    return data


def find_non_ascii_keys(frontmatter: dict[str, Any]) -> list[str]:
    return [key for key in frontmatter if isinstance(key, str) and not key.isascii()]


def collect_casing_groups(
    content_dir: pathlib.Path,
) -> dict[tuple[str, str], dict[str, set[pathlib.Path]]]:
    """Map (field, casefolded value) -> {spelling: {file paths using it}}."""
    groups: dict[tuple[str, str], dict[str, set[pathlib.Path]]] = defaultdict(
        lambda: defaultdict(set)
    )
    for path in iter_markdown_files(content_dir):
        frontmatter = load_frontmatter(path)
        if frontmatter is None:
            continue
        for field in FRONTMATTER_LIST_FIELDS:
            values = frontmatter.get(field)
            if not isinstance(values, list):
                continue
            for value in values:
                if not isinstance(value, str):
                    continue
                groups[(field, value.casefold())][value].add(path)
    return groups


def find_poster_registration_violations(content_dir: pathlib.Path) -> list[str]:
    violations: list[str] = []
    publication_dir = content_dir / "publication"
    if not publication_dir.is_dir():
        return violations

    bundle_dirs = {
        path.parent
        for pattern in ("*/index.md", f"*/{POSTER_PDF}")
        for path in publication_dir.glob(pattern)
    }
    for bundle_dir in sorted(bundle_dirs):
        index_path = bundle_dir / "index.md"
        poster_path = bundle_dir / POSTER_PDF
        frontmatter = load_frontmatter(index_path) if index_path.is_file() else None
        if frontmatter is None:
            if poster_path.is_file():
                violations.append(
                    f"{poster_path}: {POSTER_PDF} requires publication index.md"
                )
            continue

        slug = bundle_dir.name
        thumbnail_path = bundle_dir / POSTER_THUMBNAIL
        tags = frontmatter.get("tags")
        has_poster_tag = isinstance(tags, list) and POSTER_TAG in tags
        has_poster_url = bool(frontmatter.get("url_poster"))

        if not poster_path.is_file():
            if has_poster_tag:
                violations.append(
                    f"{index_path}: tag {POSTER_TAG!r} requires {POSTER_PDF}"
                )
            if has_poster_url:
                violations.append(f"{index_path}: url_poster requires {POSTER_PDF}")
            if thumbnail_path.is_file():
                violations.append(
                    f"{thumbnail_path}: {POSTER_THUMBNAIL} requires {POSTER_PDF}"
                )
            continue

        if not has_poster_tag:
            violations.append(
                f"{index_path}: {POSTER_PDF} requires the exact tag {POSTER_TAG!r}"
            )

        expected_url = f"publication/{slug}/{POSTER_PDF}"
        if frontmatter.get("url_poster") != expected_url:
            violations.append(
                f"{index_path}: {POSTER_PDF} requires url_poster {expected_url!r}"
            )

        if not thumbnail_path.is_file():
            violations.append(f"{index_path}: {POSTER_PDF} requires {POSTER_THUMBNAIL}")

    return violations


def main() -> int:
    args = parse_args()

    violations: list[str] = []
    warnings: list[str] = []
    checked = 0

    for path in iter_markdown_files(args.content_dir):
        frontmatter = load_frontmatter(path)
        if frontmatter is None:
            continue
        checked += 1
        for key in find_non_ascii_keys(frontmatter):
            violations.append(
                f"{path}: frontmatter key {key!r} contains non-ASCII characters"
            )

    groups = collect_casing_groups(args.content_dir)
    for (field, casefold_key), spellings in groups.items():
        if len(spellings) <= 1:
            continue
        other_spellings = sorted(spellings)
        for spelling, paths in sorted(spellings.items()):
            conflicts = [s for s in other_spellings if s != spelling]
            for path in sorted(paths):
                line = (
                    f"{path}: {field} value {spelling!r} has inconsistent casing "
                    f"with {conflicts!r} (casefold key: {casefold_key!r})"
                )
                if (field, casefold_key) in KNOWN_CASING_EXCEPTIONS:
                    warnings.append(line)
                else:
                    violations.append(line)

    violations.extend(find_poster_registration_violations(args.content_dir))

    if warnings:
        print("Known pre-existing casing issues (reported, not failing the build):")
        for warning in sorted(warnings):
            print(warning)
        print()

    if violations:
        print("Frontmatter lint violations:")
        for violation in sorted(violations):
            print(violation)
        return 1

    print(f"frontmatter lint OK ({checked} files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
