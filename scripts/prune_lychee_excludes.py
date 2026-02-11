#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any, Iterable
import re


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


def collect_revived(data: Any) -> set[str]:
    revived: set[str] = set()
    for entry in iter_entries(data):
        url = entry.get("url")
        status_value = entry.get("status")
        if not isinstance(url, str):
            continue
        status = status_to_int(status_value)
        if status is None:
            continue
        if 200 <= status <= 299 or status == 302:
            revived.add(url)
    return revived


def load_json(path: pathlib.Path) -> Any | None:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_lines(path: pathlib.Path) -> list[str] | None:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.readlines()


def is_comment_or_blank(line: str) -> bool:
    stripped = line.strip()
    return stripped == "" or stripped.startswith("#")


def should_remove(line: str, revived_urls: set[str]) -> bool:
    if is_comment_or_blank(line):
        return False
    token = line.strip()
    if not token:
        return False
    is_regex = bool(re.search(r"[\\.^$*+?{}\\[\\]|()]", token))
    for url in revived_urls:
        if is_regex:
            try:
                if re.search(token, url):
                    return True
            except re.error:
                if token in url:
                    return True
        else:
            if token in url or url in token:
                return True
    return False


def write_lines(path: pathlib.Path, lines: list[str]) -> None:
    if lines and not lines[-1].endswith("\n"):
        lines[-1] = lines[-1] + "\n"
    with open(path, "w", encoding="utf-8") as handle:
        handle.writelines(lines)


def main():
    args = parse_args()

    data = load_json(args.json_path)
    if data is None:
        print("no change")
        return

    lines = load_lines(args.exclude_path)
    if lines is None:
        print("no change")
        return

    revived = collect_revived(data)
    if not revived:
        print("no change")
        return

    kept: list[str] = []
    removed: list[str] = []
    for line in lines:
        if should_remove(line, revived):
            removed.append(line.rstrip("\n"))
        else:
            kept.append(line)

    if not removed:
        print("no change")
        return

    if args.dry_run:
        for line in removed:
            print(line)
        return

    write_lines(args.exclude_path, kept)
    for line in removed:
        print(line)


if __name__ == "__main__":
    main()
