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


@dataclass(frozen=True)
class SourceConfig:
    name: str
    adapter: str
    url: str
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExistingEvent:
    path: str
    urls: list[str]


@dataclass
class FeedEntry:
    source_url: str
    title: str
    source_name: str
    adapter: str
    published_at: str = ""
    description: str = ""
    image_url: str = ""
    extracted_urls: list[str] = field(default_factory=list)
    duplicate_of: str = ""
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
        payload["source_type"] = self.adapter
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


def default_feed_url(profile_url: str) -> str:
    return profile_url.rstrip("/") + ".rss"


def source_name_from_url(url: str) -> str:
    parsed = urlsplit(url)
    candidate = f"{parsed.netloc}{parsed.path}".strip("/")
    name = re.sub(r"[^a-zA-Z0-9]+", "-", candidate).strip("-").lower()
    return name or "feed"


def default_sources(profile_url: str) -> list[SourceConfig]:
    return [
        SourceConfig(
            name=source_name_from_url(profile_url),
            adapter="speakerdeck-profile",
            url=default_feed_url(profile_url),
            options={"profile_url": profile_url},
        )
    ]


def normalize_source_config(raw: dict[str, Any], index: int) -> SourceConfig:
    adapter = str(
        raw.get("adapter") or raw.get("type") or raw.get("source_type") or ""
    ).strip()
    if adapter not in SOURCE_ADAPTERS:
        raise ValueError(
            f"Unsupported source adapter at index {index}: {adapter!r}. "
            f"Supported adapters are {', '.join(sorted(SOURCE_ADAPTERS))}."
        )
    raw_options = raw.get("options") or {}
    if not isinstance(raw_options, dict):
        raise ValueError(f"source options at index {index} must be an object.")
    options = dict(raw_options)
    profile_url = str(raw.get("profile_url") or "").strip()
    url = str(raw.get("url") or "").strip()
    if profile_url:
        options["profile_url"] = profile_url
    if adapter == "speakerdeck-profile":
        if not profile_url and url.endswith((".rss", ".atom")):
            profile_url = url.rsplit(".", 1)[0]
            options["profile_url"] = profile_url
        if not profile_url:
            raise ValueError(
                f"speakerdeck-profile source at index {index} requires profile_url."
            )
        if not url:
            url = default_feed_url(profile_url)
    elif not url:
        raise ValueError(f"{adapter} source at index {index} requires url.")
    name = str(raw.get("name") or source_name_from_url(profile_url or url)).strip()
    return SourceConfig(
        name=name,
        adapter=adapter,
        url=url,
        options=options,
    )


def load_source_configs(path: Path) -> list[SourceConfig]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        raw_sources = payload
    elif isinstance(payload, dict):
        raw_sources = payload.get("sources", [])
    else:
        raise ValueError("source config must be a JSON object or array.")
    if not isinstance(raw_sources, list) or not raw_sources:
        raise ValueError("source config must contain a non-empty 'sources' list.")
    return [
        normalize_source_config(raw_source, index)
        for index, raw_source in enumerate(raw_sources)
    ]


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


def assert_root(root: ET.Element, expected: str, source: SourceConfig) -> None:
    actual = root.tag.rsplit("}", 1)[-1].lower()
    if expected == "rss" and actual != "rss":
        raise ValueError(f"{source.name} expected RSS XML, got {root.tag!r}.")
    if expected == "atom" and actual != "feed":
        raise ValueError(f"{source.name} expected Atom XML, got {root.tag!r}.")


def detect_xml_format(root: ET.Element, source: SourceConfig) -> str:
    actual = root.tag.rsplit("}", 1)[-1].lower()
    if actual == "rss":
        return "rss"
    if actual == "feed":
        return "atom"
    raise ValueError(
        f"{source.name} uses auto feed detection, but XML root {root.tag!r} "
        "is neither RSS nor Atom."
    )


def parse_rss_entries(root: ET.Element, source: SourceConfig) -> list[FeedEntry]:
    entries: list[FeedEntry] = []
    for item in root.findall("./channel/item"):
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
                source_name=source.name,
                adapter=source.adapter,
                published_at=first_text(item, ("pubDate", "dc:date")),
                description=description,
                image_url=image_url,
                extracted_urls=extracted,
            )
        )
    return entries


def parse_atom_entries(root: ET.Element, source: SourceConfig) -> list[FeedEntry]:
    entries: list[FeedEntry] = []
    for entry in root.findall("atom:entry", RSS_NAMESPACES):
        source_url = ""
        for link in entry.findall("atom:link", RSS_NAMESPACES):
            rel = link.attrib.get("rel", "alternate")
            href = link.attrib.get("href", "")
            if href and rel == "alternate":
                source_url = urljoin(source.url, href)
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
                source_name=source.name,
                adapter=source.adapter,
                published_at=first_text(entry, ("atom:published", "atom:updated")),
                description=description,
                image_url="",
                extracted_urls=extracted,
            )
        )
    return entries


def parse_feed_entries(feed_xml: str, source: SourceConfig) -> list[FeedEntry]:
    root = ET.fromstring(feed_xml)
    xml_format = source.adapter
    if xml_format == "speakerdeck-profile":
        xml_format = "rss"
    elif xml_format == "feed":
        xml_format = detect_xml_format(root, source)
    assert_root(root, xml_format, source)
    if xml_format == "rss":
        return parse_rss_entries(root, source)
    if xml_format == "atom":
        return parse_atom_entries(root, source)
    raise ValueError(f"{source.name} cannot parse XML as adapter {source.adapter!r}.")


class FeedSourceAdapter:
    def __init__(self, source: SourceConfig) -> None:
        self.source = source

    def entries(self) -> list[FeedEntry]:
        return parse_feed_entries(read_text_url(self.source.url), self.source)


SOURCE_ADAPTERS = {
    "speakerdeck-profile": FeedSourceAdapter,
    "feed": FeedSourceAdapter,
    "rss": FeedSourceAdapter,
    "atom": FeedSourceAdapter,
}


def build_source_adapter(source: SourceConfig) -> FeedSourceAdapter:
    adapter_type = SOURCE_ADAPTERS.get(source.adapter)
    if not adapter_type:
        raise ValueError(f"Unsupported source adapter: {source.adapter}")
    return adapter_type(source)


def audit(repo_root: Path, sources: list[SourceConfig]) -> dict[str, Any]:
    existing_events = load_existing_events(repo_root)
    candidates: list[FeedEntry] = []
    existing: list[FeedEntry] = []
    duplicates: list[FeedEntry] = []
    seen_candidate_urls: dict[str, str] = {}
    for source in sources:
        for entry in build_source_adapter(source).entries():
            urls = [entry.source_url, *entry.extracted_urls]
            entry.existing_path = find_existing_path(existing_events, urls)
            if entry.existing_path:
                existing.append(entry)
            elif entry.source_url and normalize_url(entry.source_url) in seen_candidate_urls:
                entry.duplicate_of = seen_candidate_urls[normalize_url(entry.source_url)]
                duplicates.append(entry)
            else:
                if entry.source_url:
                    seen_candidate_urls[normalize_url(entry.source_url)] = entry.source_url
                candidates.append(entry)
    return {
        "candidate_count": len(candidates),
        "existing_count": len(existing),
        "duplicate_count": len(duplicates),
        "candidates": [entry.to_dict() for entry in candidates],
        "existing": [entry.to_dict() for entry in existing],
        "duplicates": [entry.to_dict() for entry in duplicates],
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
    audit_parser.add_argument(
        "--source-config",
        type=Path,
        help=(
            "JSON file with sources. Supports adapters 'speakerdeck-profile', "
            "'feed', 'rss', and 'atom'."
        ),
    )
    audit_parser.add_argument("--output", type=Path)
    audit_parser.add_argument("--include-existing", action="store_true")
    args = parser.parse_args()

    if args.command == "audit":
        repo_root = args.repo_root.resolve()
        if args.source_config:
            sources = load_source_configs(args.source_config)
        elif args.feed_url:
            sources = [
                SourceConfig(
                    name=source_name_from_url(feed_url),
                    adapter="feed",
                    url=feed_url,
                )
                for feed_url in args.feed_url
            ]
        else:
            sources = default_sources(args.profile_url)
        result = audit(repo_root, sources)
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
