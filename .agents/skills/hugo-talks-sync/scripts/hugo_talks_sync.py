#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


URL_FIELDS = ("event_url", "url_slides", "url_pdf", "url_video", "url_code")
USER_AGENT = "Mozilla/5.0 (compatible; hugo-talks-sync/1.0)"
RSS_NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "media": "http://search.yahoo.com/mrss/",
}
URL_RE = re.compile(r"https?://[^\s<>()\"']+")


@dataclass
class ExistingEvent:
    path: str
    urls: list[str]


@dataclass
class FeedEntry:
    source_url: str
    title: str
    published_at: str = ""
    description: str = ""
    image_url: str = ""
    extracted_urls: list[str] = field(default_factory=list)
    feed_url: str = ""
    existing_path: str = ""

    @property
    def suggested_intake_inputs(self) -> list[str]:
        inputs = [self.source_url] if self.source_url else []
        for url in self.extracted_urls:
            if url not in inputs:
                inputs.append(url)
        return inputs

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["suggested_intake_inputs"] = self.suggested_intake_inputs
        return payload


def normalize_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    path = parsed.path.rstrip("/") or parsed.path or "/"
    return urlunsplit(
        (parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, "")
    )


def read_text_url(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request) as response:
        data = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
    return data.decode(charset, errors="replace")


def parse_scalar(raw: str) -> str:
    text = raw.strip()
    if not text or text in {"null", "None"}:
        return ""
    if text.startswith(("'", '"')) and text.endswith(("'", '"')) and len(text) >= 2:
        return text[1:-1]
    return text


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for match in URL_RE.finditer(unescape(text or "")):
        url = match.group(0).rstrip(".,;]")
        normalized = normalize_url(url)
        if normalized in seen:
            continue
        seen.add(normalized)
        urls.append(url)
    return urls


def read_top_level_frontmatter_urls(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    urls: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith(" ") or line.startswith("-") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() not in URL_FIELDS:
            continue
        url = parse_scalar(value)
        if url.startswith(("http://", "https://")):
            urls.append(url)
    return urls


def load_existing_events(repo_root: Path) -> list[ExistingEvent]:
    events: list[ExistingEvent] = []
    event_root = repo_root / "content" / "event"
    for index_md in sorted(event_root.glob("*/index.md")):
        text = index_md.read_text(encoding="utf-8")
        urls = read_top_level_frontmatter_urls(text)
        urls.extend(extract_urls(text))
        normalized_urls = sorted({normalize_url(url) for url in urls})
        events.append(
            ExistingEvent(
                path=str(index_md.relative_to(repo_root)),
                urls=normalized_urls,
            )
        )
    return events


def find_existing_path(existing_events: list[ExistingEvent], urls: list[str]) -> str:
    normalized = {
        normalize_url(url) for url in urls if url.startswith(("http://", "https://"))
    }
    if not normalized:
        return ""
    for event in existing_events:
        if normalized.intersection(event.urls):
            return event.path
    return ""


def first_text(element: ET.Element, names: tuple[str, ...]) -> str:
    for name in names:
        found = element.find(name, RSS_NAMESPACES)
        if found is not None and found.text:
            return unescape(found.text).strip()
    return ""


def first_attr(element: ET.Element, names: tuple[str, ...], attr: str) -> str:
    for name in names:
        found = element.find(name, RSS_NAMESPACES)
        if found is not None:
            value = found.attrib.get(attr, "").strip()
            if value:
                return value
    return ""


def parse_feed_entries(feed_xml: str, feed_url: str) -> list[FeedEntry]:
    root = ET.fromstring(feed_xml)
    entries: list[FeedEntry] = []
    if root.tag.endswith("rss"):
        item_nodes = root.findall("./channel/item")
        for item in item_nodes:
            description = first_text(item, ("description", "content:encoded"))
            source_url = first_text(item, ("link", "guid"))
            image_url = first_attr(item, ("media:content",), "url")
            extracted = [
                url
                for url in extract_urls(description)
                if normalize_url(url) != normalize_url(source_url)
            ]
            entries.append(
                FeedEntry(
                    source_url=source_url,
                    title=first_text(item, ("title",)),
                    published_at=first_text(item, ("pubDate", "dc:date")),
                    description=description,
                    image_url=image_url,
                    extracted_urls=extracted,
                    feed_url=feed_url,
                )
            )
        return entries

    entry_nodes = root.findall("atom:entry", RSS_NAMESPACES)
    for entry in entry_nodes:
        source_url = ""
        for link in entry.findall("atom:link", RSS_NAMESPACES):
            rel = link.attrib.get("rel", "alternate")
            href = link.attrib.get("href", "")
            if href and rel == "alternate":
                source_url = urljoin(feed_url, href)
                break
        description = first_text(entry, ("atom:summary", "atom:content"))
        extracted = [
            url
            for url in extract_urls(description)
            if normalize_url(url) != normalize_url(source_url)
        ]
        entries.append(
            FeedEntry(
                source_url=source_url,
                title=first_text(entry, ("atom:title",)),
                published_at=first_text(entry, ("atom:published", "atom:updated")),
                description=description,
                image_url="",
                extracted_urls=extracted,
                feed_url=feed_url,
            )
        )
    return entries


def default_feed_url(profile_url: str) -> str:
    return profile_url.rstrip("/") + ".rss"


def audit(repo_root: Path, feed_urls: list[str]) -> dict[str, Any]:
    existing_events = load_existing_events(repo_root)
    candidates: list[FeedEntry] = []
    existing: list[FeedEntry] = []
    for feed_url in feed_urls:
        for entry in parse_feed_entries(read_text_url(feed_url), feed_url):
            urls = [entry.source_url, *entry.extracted_urls]
            entry.existing_path = find_existing_path(existing_events, urls)
            if entry.existing_path:
                existing.append(entry)
            else:
                candidates.append(entry)
    return {
        "candidate_count": len(candidates),
        "existing_count": len(existing),
        "candidates": [entry.to_dict() for entry in candidates],
        "existing": [entry.to_dict() for entry in existing],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find external talk feed entries missing from content/event."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("--repo-root", type=Path, default=Path("."))
    audit_parser.add_argument(
        "--profile-url", default="https://speakerdeck.com/shunk031"
    )
    audit_parser.add_argument("--feed-url", action="append", default=[])
    audit_parser.add_argument("--output", type=Path)
    audit_parser.add_argument("--include-existing", action="store_true")
    args = parser.parse_args()

    if args.command == "audit":
        repo_root = args.repo_root.resolve()
        feed_urls = args.feed_url or [default_feed_url(args.profile_url)]
        result = audit(repo_root, feed_urls)
        if not args.include_existing:
            result.pop("existing", None)
        payload = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(payload + "\n", encoding="utf-8")
        else:
            print(payload)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
