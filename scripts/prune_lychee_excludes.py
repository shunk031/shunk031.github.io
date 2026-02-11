#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys
from typing import Any, Iterable

URL_PATTERN = re.compile(r"https?://[^\s\"'<>)]+")
PROTO_RELATIVE_PATTERN = re.compile(r"(?<!:)//[^\s\"'<>)]+")
REGEX_META = re.compile(r"[\\.^$*+?{}\\[\\]|()]")
TRAILING_PUNCT = "\"'.,);]"


class PatternEntry:
    def __init__(self, index: int, raw_line: str, token: str, regex: re.Pattern | None):
        self.index = index
        self.raw_line = raw_line
        self.token = token
        self.regex = regex


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Remove revived URLs from a lychee temporary exclude file based on JSON output."
        )
    )
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--json",
        dest="json_path",
        type=pathlib.Path,
        default=repo_root / "lychee-excludes.json",
        help="Path to lychee JSON output (default: lychee-excludes.json)",
    )
    parser.add_argument(
        "--exclude-file",
        dest="exclude_path",
        type=pathlib.Path,
        default=repo_root / ".lychee" / "exclude-temporary.txt",
        help="Path to temporary exclude file (default: .lychee/exclude-temporary.txt)",
    )
    parser.add_argument(
        "--public-dir",
        dest="public_dir",
        type=pathlib.Path,
        default=repo_root / "public",
        help="Path to built site directory (default: ./public)",
    )
    parser.add_argument(
        "--links-output",
        dest="links_output",
        type=pathlib.Path,
        help="Write matched URLs for lychee input",
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Only generate the links output and exit",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show removals without updating the exclude file",
    )
    return parser.parse_args()


def iter_entries(node: Any) -> Iterable[dict[str, Any]]:
    if isinstance(node, dict):
        if "url" in node and "status" in node:
            yield node
        for value in node.values():
            yield from iter_entries(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_entries(item)


def status_to_int(value: Any) -> int | None:
    if isinstance(value, dict):
        return status_to_int(value.get("code"))
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)
        digits = []
        for ch in stripped:
            if ch.isdigit():
                digits.append(ch)
            else:
                break
        if digits:
            return int("".join(digits))
    return None


def collect_status_map(data: Any) -> dict[str, set[int]]:
    status_map: dict[str, set[int]] = {}
    for entry in iter_entries(data):
        url = entry.get("url")
        status_value = entry.get("status")
        if not isinstance(url, str):
            continue
        status = status_to_int(status_value)
        if status is None:
            continue
        status_map.setdefault(url, set()).add(status)
    return status_map


def load_json(path: pathlib.Path) -> Any | None:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print(f"json not found: {path}", file=sys.stderr)
        return None
    except json.JSONDecodeError as exc:
        print(f"json parse error: {path}: {exc}", file=sys.stderr)
        return None


def load_lines(path: pathlib.Path) -> list[str] | None:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.readlines()
    except FileNotFoundError:
        print(f"exclude file not found: {path}", file=sys.stderr)
        return None


def is_comment_or_blank(line: str) -> bool:
    stripped = line.strip()
    return stripped == "" or stripped.startswith("#")


def parse_patterns(lines: list[str]) -> list[PatternEntry]:
    patterns: list[PatternEntry] = []
    for index, line in enumerate(lines):
        if is_comment_or_blank(line):
            continue
        token = line.strip()
        if not token:
            continue
        regex = None
        if REGEX_META.search(token):
            try:
                regex = re.compile(token)
            except re.error:
                regex = None
        patterns.append(PatternEntry(index=index, raw_line=line.rstrip("\n"), token=token, regex=regex))
    return patterns


def normalize_url(url: str) -> str:
    return url.rstrip(TRAILING_PUNCT)


def extract_urls(public_dir: pathlib.Path) -> set[str]:
    urls: set[str] = set()
    if not public_dir.exists():
        print(f"public dir not found: {public_dir}", file=sys.stderr)
        return urls
    for path in public_dir.rglob("*.html"):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        content = html.unescape(content)
        for match in URL_PATTERN.finditer(content):
            urls.add(normalize_url(match.group(0)))
        for match in PROTO_RELATIVE_PATTERN.finditer(content):
            urls.add(normalize_url("https:" + match.group(0)))
    return urls


def matches_pattern(pattern: PatternEntry, url: str) -> bool:
    if pattern.regex is not None:
        return pattern.regex.search(url) is not None
    return pattern.token in url


def build_pattern_map(patterns: list[PatternEntry], urls: set[str]) -> dict[int, set[str]]:
    mapping: dict[int, set[str]] = {pattern.index: set() for pattern in patterns}
    for url in urls:
        for pattern in patterns:
            if matches_pattern(pattern, url):
                mapping[pattern.index].add(url)
    return mapping


def is_success(statuses: set[int]) -> bool:
    return any(200 <= status <= 299 or status == 302 for status in statuses)


def write_lines(path: pathlib.Path, lines: list[str]) -> None:
    if lines and not lines[-1].endswith("\n"):
        lines[-1] = lines[-1] + "\n"
    with open(path, "w", encoding="utf-8") as handle:
        handle.writelines(lines)


def write_links(path: pathlib.Path, urls: set[str]) -> None:
    sorted_urls = sorted(urls)
    if sorted_urls:
        content = "\n".join(sorted_urls) + "\n"
    else:
        content = ""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def main() -> int:
    args = parse_args()

    lines = load_lines(args.exclude_path)
    if lines is None:
        print("no change")
        return 0

    patterns = parse_patterns(lines)
    if not patterns:
        print("no change")
        return 0

    urls = extract_urls(args.public_dir)
    pattern_map = build_pattern_map(patterns, urls)
    matched_urls: set[str] = set()
    for urls_for_pattern in pattern_map.values():
        matched_urls.update(urls_for_pattern)

    if args.links_output is not None:
        write_links(args.links_output, matched_urls)
        if args.prepare:
            print(f"prepared {len(matched_urls)} links")
            return 0

    if args.prepare:
        print("no change")
        return 0

    data = load_json(args.json_path)
    if data is None:
        print("no change")
        return 0

    status_map = collect_status_map(data)
    removed_indices: set[int] = set()
    removed_lines: list[str] = []

    for pattern in patterns:
        matched = pattern_map.get(pattern.index, set())
        if not matched:
            continue
        all_revived = True
        for url in matched:
            statuses = status_map.get(url)
            if statuses is None:
                continue
            if not is_success(statuses):
                all_revived = False
                break
        if all_revived:
            removed_indices.add(pattern.index)
            removed_lines.append(pattern.raw_line)

    if not removed_lines:
        print("no change")
        return 0

    if args.dry_run:
        for line in removed_lines:
            print(line)
        return 0

    kept_lines = [line for idx, line in enumerate(lines) if idx not in removed_indices]
    write_lines(args.exclude_path, kept_lines)
    for line in removed_lines:
        print(line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
