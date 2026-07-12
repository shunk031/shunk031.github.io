from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


URL_FIELDS = ("event_url", "url_slides", "url_pdf", "url_video", "url_code")
ADDRESS_KEYS = ("street", "city", "region", "postcode", "country")
TOP_LEVEL_FIELDS = {"title", "event", *URL_FIELDS}
USER_AGENT = "Mozilla/5.0 (compatible; hugo-event-intake/1.0)"


@dataclass
class RemoteResponse:
    url: str
    content_type: str
    text: str
    data: bytes


@dataclass
class SourceInfo:
    url: str
    source_type: str
    title: str = ""
    description: str = ""
    image_url: str = ""
    event_hint: str = ""
    date: str = ""
    date_end: str = ""
    location: str = ""
    address: dict[str, str] = field(default_factory=lambda: empty_address())
    discovered_urls: list[str] = field(default_factory=list)
    embed_id: str = ""
    embed_ratio: str = ""


@dataclass
class EventSpec:
    slug: str = ""
    kind: str = ""
    title: str = ""
    event: str = ""
    event_url: str = ""
    location: str = ""
    address: dict[str, str] = field(default_factory=lambda: empty_address())
    summary: str = ""
    abstract: str = ""
    date: str = ""
    date_end: str = ""
    publish_date: str = ""
    authors: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    url_slides: str = ""
    url_pdf: str = ""
    url_video: str = ""
    url_code: str = ""
    links: list[dict[str, str]] = field(default_factory=list)
    body_markdown: str = ""
    featured_source_url: str = ""
    evidence_urls: list[str] = field(default_factory=list)
    unresolved_fields: list[str] = field(default_factory=list)
    duplicate_of: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EventSpec":
        payload = dict(data)
        payload.setdefault("address", empty_address())
        payload["address"] = normalize_address(payload["address"])
        for key in ("authors", "tags", "links", "evidence_urls", "unresolved_fields"):
            payload.setdefault(key, [])
        return cls(**payload)


class MetadataHTMLParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.meta: dict[str, str] = {}
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self.json_ld_blocks: list[str] = []
        self.speakerdeck_embed_id = ""
        self.speakerdeck_embed_ratio = ""
        self._capture_title = False
        self._capture_json_ld = False
        self._current_script: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key.lower(): value or "" for key, value in attrs}
        if tag == "meta":
            key = attr_map.get("property") or attr_map.get("name")
            content = attr_map.get("content", "")
            if key and content:
                self.meta[key.lower()] = unescape(content.strip())
        elif tag == "title":
            self._capture_title = True
        elif tag == "a":
            href = attr_map.get("href", "").strip()
            if href:
                self.links.append(urljoin(self.base_url, href))
        elif (
            tag == "script"
            and attr_map.get("type", "").lower() == "application/ld+json"
        ):
            self._capture_json_ld = True
            self._current_script = []
        elif (
            "speakerdeck-embed" in attr_map.get("class", "")
            and not self.speakerdeck_embed_id
        ):
            self.speakerdeck_embed_id = attr_map.get("data-id", "")
            self.speakerdeck_embed_ratio = attr_map.get("data-ratio", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._capture_title = False
        elif tag == "script" and self._capture_json_ld:
            self.json_ld_blocks.append("".join(self._current_script).strip())
            self._capture_json_ld = False
            self._current_script = []

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self.title_parts.append(data)
        if self._capture_json_ld:
            self._current_script.append(data)

    @property
    def title(self) -> str:
        return unescape("".join(self.title_parts).strip())


def empty_address() -> dict[str, str]:
    return {key: "" for key in ADDRESS_KEYS}


def normalize_address(value: dict[str, Any] | None) -> dict[str, str]:
    address = empty_address()
    if not value:
        return address
    for key in ADDRESS_KEYS:
        address[key] = str(value.get(key, "") or "").strip()
    return address


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def looks_like_url(value: str) -> bool:
    parsed = urlsplit(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def normalize_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    path = parsed.path.rstrip("/") or parsed.path or "/"
    return urlunsplit(
        (parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, "")
    )


def slugify(value: str) -> str:
    ascii_value = value.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return re.sub(r"-{2,}", "-", slug)


def split_prefixed_title(raw_title: str) -> tuple[str, str, str]:
    text = unescape(raw_title).strip()
    prefix = ""
    remainder = text
    if text.startswith("[") and "]" in text:
        prefix, remainder = text[1:].split("]", 1)
        prefix = prefix.strip()
        remainder = remainder.strip()
    alias = ""
    if " / " in remainder:
        left, right = remainder.split(" / ", 1)
        remainder = left.strip() or remainder
        alias = right.strip()
    return prefix, remainder, alias


def is_speakerdeck_url(url: str) -> bool:
    return urlsplit(url).netloc.lower().endswith("speakerdeck.com")


def is_youtube_url(url: str) -> bool:
    host = urlsplit(url).netloc.lower()
    return host.endswith("youtube.com") or host.endswith("youtu.be")


def is_pdf_url(url: str) -> bool:
    parsed = urlsplit(url)
    return parsed.path.lower().endswith(".pdf")


def default_tags_for_kind(kind: str) -> list[str]:
    mapping = {
        "Invited Talk": ["Invited Talk"],
        "Journal Club": ["Journal Club", "Paper Reading"],
        "Invited Presentation": ["Invited Talk", "Invited Presentation"],
        "Invited Poster": ["Presentation"],
        "Report": [],
    }
    return list(mapping.get(kind, [kind] if kind else []))


def render_title(kind: str, core_title: str) -> str:
    core = core_title.strip()
    if not core:
        return ""
    if kind == "Report":
        return core
    return f"[{kind}] {core}"


def infer_kind(
    notes: list[str], sources: list[SourceInfo], explicit_kind: str = ""
) -> str:
    if explicit_kind.strip():
        return explicit_kind.strip()
    haystack = " ".join(
        [
            *notes,
            *[source.title for source in sources],
            *[source.event_hint for source in sources],
        ]
    ).lower()
    if any(
        keyword in haystack
        for keyword in (
            "journal club",
            "reading",
            "paper reading",
            "論文読み会",
            "読み会",
            "輪読",
        )
    ):
        return "Journal Club"
    if "poster" in haystack:
        return "Invited Poster"
    if "presentation" in haystack:
        return "Invited Presentation"
    if any(keyword in haystack for keyword in ("report", "速報", "summary", "survey")):
        return "Report"
    return "Invited Talk"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def read_top_level_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith(" ") or line.startswith("-") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in TOP_LEVEL_FIELDS:
            continue
        result[key] = parse_scalar(value.strip())
    return result


def parse_scalar(raw: str) -> str:
    text = raw.strip()
    if not text:
        return ""
    if text in {"null", "None"}:
        return ""
    if text.startswith(("'", '"')) and text.endswith(("'", '"')) and len(text) >= 2:
        return text[1:-1]
    return text


def load_existing_events(repo_root: Path) -> list[dict[str, Any]]:
    records = []
    event_root = repo_root / "content" / "event"
    for path in sorted(event_root.glob("*/index.md")):
        frontmatter = read_top_level_frontmatter(path)
        urls = []
        for field in URL_FIELDS:
            value = frontmatter.get(field, "").strip()
            if value and looks_like_url(value):
                urls.append(normalize_url(value))
        records.append(
            {
                "path": str(path.relative_to(repo_root)),
                "title": frontmatter.get("title", ""),
                "event": frontmatter.get("event", ""),
                "urls": urls,
            }
        )
    return records


def detect_duplicate(existing_events: list[dict[str, Any]], urls: list[str]) -> str:
    normalized_urls = {normalize_url(url) for url in urls if looks_like_url(url)}
    for record in existing_events:
        if normalized_urls.intersection(record["urls"]):
            return record["path"]
    return ""


def fetch_text_response(url: str) -> RemoteResponse:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request) as response:
        data = response.read()
        content_type = response.headers.get_content_type()
        charset = response.headers.get_content_charset() or "utf-8"
    text = data.decode(charset, errors="replace")
    return RemoteResponse(url=url, content_type=content_type, text=text, data=data)


def fetch_json(url: str) -> dict[str, Any]:
    return json.loads(fetch_text_response(url).text)


def download_binary(url: str) -> tuple[bytes, str]:
    response = fetch_text_response(url)
    return response.data, response.content_type


def parse_html(url: str, html_text: str) -> MetadataHTMLParser:
    parser = MetadataHTMLParser(url)
    parser.feed(html_text)
    return parser


def parse_json_ld_event(blocks: list[str]) -> dict[str, str | dict[str, str]]:
    for block in blocks:
        if not block:
            continue
        try:
            payload = json.loads(block)
        except json.JSONDecodeError:
            continue
        event = find_event_object(payload)
        if event:
            address = normalize_schema_address(event.get("location", {}).get("address"))
            location_name = ""
            location = event.get("location")
            if isinstance(location, dict):
                location_name = str(location.get("name", "") or "").strip()
            return {
                "event_hint": str(event.get("name", "") or "").strip(),
                "date": str(event.get("startDate", "") or "").strip(),
                "date_end": str(event.get("endDate", "") or "").strip(),
                "location": location_name,
                "address": address,
            }
    return {
        "event_hint": "",
        "date": "",
        "date_end": "",
        "location": "",
        "address": empty_address(),
    }


def find_event_object(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        event_type = value.get("@type")
        if isinstance(event_type, list):
            is_event = "Event" in event_type
        else:
            is_event = event_type == "Event"
        if is_event:
            return value
        for nested in value.values():
            found = find_event_object(nested)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = find_event_object(item)
            if found:
                return found
    return None


def normalize_schema_address(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return empty_address()
    return {
        "street": str(value.get("streetAddress", "") or "").strip(),
        "city": str(value.get("addressLocality", "") or "").strip(),
        "region": str(value.get("addressRegion", "") or "").strip(),
        "postcode": str(value.get("postalCode", "") or "").strip(),
        "country": str(value.get("addressCountry", "") or "").strip(),
    }


def extract_candidate_urls(base_url: str, urls: list[str]) -> list[str]:
    discovered = []
    seen = set()
    for href in urls:
        if not looks_like_url(href):
            href = urljoin(base_url, href)
        if not (is_speakerdeck_url(href) or is_youtube_url(href) or is_pdf_url(href)):
            continue
        normalized = normalize_url(href)
        if normalized in seen:
            continue
        seen.add(normalized)
        discovered.append(href)
    return discovered


def resolve_source_url(
    url: str,
    *,
    fetch_text_response: Callable[[str], RemoteResponse] = fetch_text_response,
    fetch_json: Callable[[str], dict[str, Any]] = fetch_json,
) -> SourceInfo:
    if is_speakerdeck_url(url):
        return resolve_speakerdeck_source(
            url, fetch_text_response=fetch_text_response, fetch_json=fetch_json
        )
    if is_youtube_url(url):
        return SourceInfo(url=url, source_type="video")
    if is_pdf_url(url):
        return SourceInfo(url=url, source_type="pdf")
    return resolve_html_source(url, fetch_text_response=fetch_text_response)


def resolve_speakerdeck_source(
    url: str,
    *,
    fetch_text_response: Callable[[str], RemoteResponse],
    fetch_json: Callable[[str], dict[str, Any]],
) -> SourceInfo:
    oembed_url = f"https://speakerdeck.com/oembed.json?url={quote(url, safe='')}"
    oembed = {}
    try:
        oembed = fetch_json(oembed_url)
    except Exception:
        oembed = {}
    response = fetch_text_response(url)
    parser = parse_html(url, response.text)
    raw_title = str(
        oembed.get("title", "") or parser.meta.get("og:title") or parser.title
    ).strip()
    event_hint, _, _ = split_prefixed_title(raw_title)
    return SourceInfo(
        url=url,
        source_type="speakerdeck",
        title=raw_title,
        description=parser.meta.get("og:description", ""),
        image_url=parser.meta.get("og:image", ""),
        event_hint=event_hint,
        discovered_urls=[],
        embed_id=parser.speakerdeck_embed_id,
        embed_ratio=parser.speakerdeck_embed_ratio
        or str(oembed.get("ratio", "") or ""),
    )


def resolve_html_source(
    url: str,
    *,
    fetch_text_response: Callable[[str], RemoteResponse],
) -> SourceInfo:
    response = fetch_text_response(url)
    parser = parse_html(url, response.text)
    event_metadata = parse_json_ld_event(parser.json_ld_blocks)
    return SourceInfo(
        url=url,
        source_type="html",
        title=parser.meta.get("og:title", "") or parser.title,
        description=parser.meta.get("og:description", "")
        or parser.meta.get("description", ""),
        image_url=parser.meta.get("og:image", ""),
        event_hint=str(event_metadata.get("event_hint", "") or ""),
        date=str(event_metadata.get("date", "") or ""),
        date_end=str(event_metadata.get("date_end", "") or ""),
        location=str(event_metadata.get("location", "") or ""),
        address=normalize_address(event_metadata.get("address")),
        discovered_urls=extract_candidate_urls(url, parser.links),
    )


def derive_slug(
    explicit_slug: str,
    sources: list[SourceInfo],
    title_core: str,
    event_name: str,
    date: str,
) -> str:
    if explicit_slug.strip():
        return explicit_slug.strip()
    for source in sources:
        parsed = urlsplit(source.url)
        candidate = slugify(Path(parsed.path).name)
        if candidate and not candidate.replace("-", "").isdigit():
            return candidate
    for candidate in (event_name, title_core):
        slug = slugify(candidate)
        if slug:
            return slug
    if date:
        return f"event-{date[:10].replace('-', '')}"
    return "event-entry"


def build_body_markdown(
    spec: EventSpec, *, description: str, speakerdeck_source: SourceInfo | None
) -> str:
    parts: list[str] = []
    if spec.event:
        parts.append(f"# {spec.event}\n")
    if description.strip():
        quote_lines = [
            f"> {line.strip()}" if line.strip() else ">"
            for line in description.strip().splitlines()
        ]
        parts.append("\n".join(quote_lines) + "\n")
    if speakerdeck_source and speakerdeck_source.embed_id:
        ratio = speakerdeck_source.embed_ratio or "1.7777777777777777"
        parts.append(
            "## 資料 - Slides\n\n"
            f'<script defer class="speakerdeck-embed" data-id="{speakerdeck_source.embed_id}" '
            f'data-ratio="{ratio}" src="//speakerdeck.com/assets/embed.js"></script>\n'
        )
        return "\n".join(part.rstrip() for part in parts if part.strip()) + "\n"

    links = []
    if spec.event_url:
        links.append(("Event", spec.event_url))
    if spec.url_slides:
        links.append(("Slides", spec.url_slides))
    if spec.url_pdf:
        links.append(("PDF", spec.url_pdf))
    if spec.url_video:
        links.append(("Video", spec.url_video))
    if spec.url_code:
        links.append(("Code", spec.url_code))
    if spec.links:
        for link in spec.links:
            links.append((link["name"], link["url"]))
    if links:
        parts.append(
            "## Links\n\n"
            + "\n".join(f"- [{name}]({url})" for name, url in links)
            + "\n"
        )
    return "\n".join(part.rstrip() for part in parts if part.strip()) + "\n"


def probe_event(
    repo_root: Path,
    *,
    inputs: list[str],
    slug: str = "",
    kind: str = "",
    title: str = "",
    event: str = "",
    event_url: str = "",
    location: str = "",
    street: str = "",
    city: str = "",
    region: str = "",
    postcode: str = "",
    country: str = "",
    date: str = "",
    date_end: str = "",
    publish_date: str = "",
    summary: str = "",
    abstract: str = "",
    authors: list[str] | None = None,
    tags: list[str] | None = None,
    url_slides: str = "",
    url_pdf: str = "",
    url_video: str = "",
    url_code: str = "",
    body_markdown: str = "",
    featured_source_url: str = "",
    fetch_text_response: Callable[[str], RemoteResponse] = fetch_text_response,
    fetch_json: Callable[[str], dict[str, Any]] = fetch_json,
) -> EventSpec:
    explicit_authors = list(authors or [])
    explicit_tags = list(tags or [])
    url_inputs = [value.strip() for value in inputs if looks_like_url(value)]
    notes = [
        value.strip() for value in inputs if value.strip() and not looks_like_url(value)
    ]
    existing_events = load_existing_events(repo_root)
    duplicate = detect_duplicate(existing_events, url_inputs)
    if duplicate:
        return EventSpec(duplicate_of=duplicate)

    seen_urls: set[str] = set()
    pending = list(url_inputs)
    sources: list[SourceInfo] = []
    while pending:
        current = pending.pop(0)
        normalized = normalize_url(current)
        if normalized in seen_urls:
            continue
        seen_urls.add(normalized)
        source = resolve_source_url(
            current,
            fetch_text_response=fetch_text_response,
            fetch_json=fetch_json,
        )
        sources.append(source)
        for discovered in source.discovered_urls:
            if normalize_url(discovered) not in seen_urls:
                pending.append(discovered)

    duplicate = detect_duplicate(existing_events, [source.url for source in sources])
    if duplicate:
        return EventSpec(duplicate_of=duplicate)

    speakerdeck_source = next(
        (source for source in sources if source.source_type == "speakerdeck"), None
    )
    html_source = next(
        (source for source in sources if source.source_type == "html"), None
    )
    pdf_source = next(
        (source for source in sources if source.source_type == "pdf"), None
    )
    video_source = next(
        (source for source in sources if source.source_type == "video"), None
    )

    raw_title = title.strip()
    if not raw_title:
        for candidate in (speakerdeck_source, html_source):
            if candidate and candidate.title:
                raw_title = candidate.title
                break
        if not raw_title and pdf_source:
            raw_title = (
                Path(urlsplit(pdf_source.url).path).stem.replace("-", " ").strip()
            )

    event_hint = event.strip()
    title_core = raw_title.strip()
    if speakerdeck_source and speakerdeck_source.title:
        source_event_hint, cleaned_title, _ = split_prefixed_title(
            speakerdeck_source.title
        )
        title_core = cleaned_title or title_core
        if not event_hint:
            event_hint = source_event_hint
    elif raw_title:
        _, cleaned_title, _ = split_prefixed_title(raw_title)
        title_core = cleaned_title or raw_title

    if not event_hint and html_source and html_source.event_hint:
        event_hint = html_source.event_hint
    if (
        not event_hint
        and html_source
        and html_source.title
        and html_source.title != title_core
    ):
        event_hint = html_source.title

    inferred_kind = infer_kind(notes, sources, explicit_kind=kind)
    final_title = title.strip() or render_title(inferred_kind, title_core)
    final_event = event_hint
    final_summary = summary.strip()
    if not final_summary:
        for candidate in (speakerdeck_source, html_source):
            if candidate and candidate.description:
                final_summary = candidate.description.strip()
                break
    final_abstract = abstract.strip() or final_summary
    final_event_url = event_url.strip() or (html_source.url if html_source else "")
    final_date = date.strip() or (html_source.date if html_source else "")
    final_date_end = date_end.strip() or (
        html_source.date_end if html_source and html_source.date_end else final_date
    )
    final_publish_date = publish_date.strip() or final_date or now_iso()
    final_location = location.strip() or (html_source.location if html_source else "")
    final_address = normalize_address(
        {
            "street": street.strip()
            or (html_source.address["street"] if html_source else ""),
            "city": city.strip()
            or (html_source.address["city"] if html_source else ""),
            "region": region.strip()
            or (html_source.address["region"] if html_source else ""),
            "postcode": postcode.strip()
            or (html_source.address["postcode"] if html_source else ""),
            "country": country.strip()
            or (html_source.address["country"] if html_source else ""),
        }
    )
    final_url_slides = url_slides.strip() or (
        speakerdeck_source.url if speakerdeck_source else ""
    )
    final_url_pdf = url_pdf.strip() or (pdf_source.url if pdf_source else "")
    final_url_video = url_video.strip() or (video_source.url if video_source else "")
    final_url_code = url_code.strip()
    final_authors = explicit_authors or ["Shunsuke Kitada"]
    final_tags = explicit_tags or default_tags_for_kind(inferred_kind)
    final_featured_source = featured_source_url.strip()
    if not final_featured_source:
        for candidate in (speakerdeck_source, html_source):
            if candidate and candidate.image_url:
                final_featured_source = candidate.image_url
                break
        if not final_featured_source and final_url_pdf:
            final_featured_source = final_url_pdf

    spec = EventSpec(
        slug=derive_slug(slug, sources, title_core, final_event, final_date),
        kind=inferred_kind,
        title=final_title,
        event=final_event,
        event_url=final_event_url,
        location=final_location,
        address=final_address,
        summary=final_summary,
        abstract=final_abstract,
        date=final_date,
        date_end=final_date_end,
        publish_date=final_publish_date,
        authors=final_authors,
        tags=final_tags,
        url_slides=final_url_slides,
        url_pdf=final_url_pdf,
        url_video=final_url_video,
        url_code=final_url_code,
        links=[],
        body_markdown="",
        featured_source_url=final_featured_source,
        evidence_urls=[source.url for source in sources],
        unresolved_fields=[],
        duplicate_of="",
    )
    spec.body_markdown = body_markdown.strip() or build_body_markdown(
        spec,
        description=final_summary or final_abstract,
        speakerdeck_source=speakerdeck_source,
    )
    for field_name in (
        "title",
        "event",
        "date",
        "date_end",
        "location",
        "summary",
        "featured_source_url",
    ):
        if not getattr(spec, field_name):
            spec.unresolved_fields.append(field_name)
    if spec.slug == "event-entry":
        spec.unresolved_fields.append("slug")
    spec.unresolved_fields = sorted(set(spec.unresolved_fields))
    return spec


def detect_file_extension(url: str, content_type: str) -> str:
    type_lower = (content_type or "").lower()
    if "image/jpeg" in type_lower or "image/jpg" in type_lower:
        return ".jpg"
    if "image/png" in type_lower:
        return ".png"
    if "image/webp" in type_lower:
        return ".webp"
    if "application/pdf" in type_lower:
        return ".pdf"
    suffix = Path(urlsplit(url).path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp", ".pdf"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    return ".jpg"


def create_pdf_thumbnail(pdf_path: Path, output_path: Path) -> Path:
    command = ""
    if shutil.which("magick"):
        command = "magick"
    elif shutil.which("convert"):
        command = "convert"
    if not command:
        raise FileNotFoundError(
            "ImageMagick command not found: expected `magick` or `convert`."
        )
    subprocess.run(
        [
            command,
            f"{pdf_path}[0]",
            "-resize",
            "640x640^",
            "-crop",
            "640x480+0+0",
            "-alpha",
            "remove",
            str(output_path),
        ],
        check=True,
    )
    return output_path


def write_featured_asset(
    event_dir: Path,
    source_url: str,
    *,
    download_binary: Callable[[str], tuple[bytes, str]] = download_binary,
) -> Path:
    data, content_type = download_binary(source_url)
    suffix = detect_file_extension(source_url, content_type)
    if suffix == ".pdf":
        with tempfile.TemporaryDirectory(prefix="event-intake-pdf-") as tmp_dir:
            pdf_path = Path(tmp_dir) / "source.pdf"
            pdf_path.write_bytes(data)
            output_path = event_dir / "featured.png"
            create_pdf_thumbnail(pdf_path, output_path)
            return output_path
    output_path = event_dir / f"featured{suffix}"
    output_path.write_bytes(data)
    return output_path


def render_frontmatter(spec: EventSpec) -> str:
    lines = [
        "---",
        "title: " + yaml_string(spec.title),
        "event: " + yaml_string(spec.event),
        "event_url: " + yaml_string(spec.event_url),
        "location: " + yaml_string(spec.location),
        "address:",
        f"  street: {yaml_string(spec.address['street'])}",
        f"  city: {yaml_string(spec.address['city'])}",
        f"  region: {yaml_string(spec.address['region'])}",
        f"  postcode: {yaml_string(spec.address['postcode'])}",
        f"  country: {yaml_string(spec.address['country'])}",
        "summary: " + yaml_string(spec.summary),
        "abstract: " + yaml_string(spec.abstract),
        "date: " + yaml_string(spec.date),
        "date_end: " + yaml_string(spec.date_end or spec.date),
        "all_day: false",
        "publishDate: " + yaml_string(spec.publish_date or spec.date or now_iso()),
        "authors: " + json.dumps(spec.authors, ensure_ascii=False),
        "tags: " + json.dumps(spec.tags, ensure_ascii=False),
        "featured: false",
        "image:",
        '  caption: ""',
        '  focal_point: ""',
        "  preview_only: false",
    ]
    if spec.links:
        lines.append("links:")
        for link in spec.links:
            lines.append(f"- name: {yaml_string(link['name'])}")
            lines.append(f"  url: {yaml_string(link['url'])}")
    else:
        lines.append("links: []")
    lines.extend(
        [
            "url_slides: " + yaml_string(spec.url_slides),
            "url_code: " + yaml_string(spec.url_code),
            "url_pdf: " + yaml_string(spec.url_pdf),
            "url_video: " + yaml_string(spec.url_video),
            'slides: ""',
            "projects: []",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def write_event(
    repo_root: Path,
    spec: EventSpec,
    *,
    download_binary: Callable[[str], tuple[bytes, str]] = download_binary,
) -> Path:
    if spec.duplicate_of:
        raise FileExistsError(f"Event already exists: {spec.duplicate_of}")
    event_dir = repo_root / "content" / "event" / spec.slug
    index_path = event_dir / "index.md"
    if index_path.exists():
        raise FileExistsError(f"Event already exists: {index_path}")
    event_dir.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        render_frontmatter(spec) + spec.body_markdown.strip() + "\n", encoding="utf-8"
    )
    if spec.featured_source_url:
        write_featured_asset(
            event_dir, spec.featured_source_url, download_binary=download_binary
        )
    return index_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create Hugo event entries from URLs or sparse notes."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    probe = subparsers.add_parser(
        "probe", help="Gather metadata and emit an event spec as JSON."
    )
    probe.add_argument("--repo-root", required=True, help="Repository root.")
    probe.add_argument(
        "--input",
        action="append",
        required=True,
        help="Input URL or free-form note. Repeatable.",
    )
    probe.add_argument("--output", help="Optional path to write the JSON spec.")
    probe.add_argument("--slug", default="")
    probe.add_argument("--kind", default="")
    probe.add_argument("--title", default="")
    probe.add_argument("--event", default="")
    probe.add_argument("--event-url", default="")
    probe.add_argument("--location", default="")
    probe.add_argument("--street", default="")
    probe.add_argument("--city", default="")
    probe.add_argument("--region", default="")
    probe.add_argument("--postcode", default="")
    probe.add_argument("--country", default="")
    probe.add_argument("--date", default="")
    probe.add_argument("--date-end", default="")
    probe.add_argument("--publish-date", default="")
    probe.add_argument("--summary", default="")
    probe.add_argument("--abstract", default="")
    probe.add_argument("--author", action="append", default=[])
    probe.add_argument("--tag", action="append", default=[])
    probe.add_argument("--url-slides", default="")
    probe.add_argument("--url-pdf", default="")
    probe.add_argument("--url-video", default="")
    probe.add_argument("--url-code", default="")
    probe.add_argument("--body-markdown", default="")
    probe.add_argument("--featured-source-url", default="")

    write = subparsers.add_parser(
        "write", help="Write an event page from a confirmed JSON spec."
    )
    write.add_argument("--repo-root", required=True, help="Repository root.")
    write.add_argument(
        "--spec-json", required=True, help="Path to the JSON spec emitted by `probe`."
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    if args.command == "probe":
        spec = probe_event(
            repo_root,
            inputs=args.input,
            slug=args.slug,
            kind=args.kind,
            title=args.title,
            event=args.event,
            event_url=args.event_url,
            location=args.location,
            street=args.street,
            city=args.city,
            region=args.region,
            postcode=args.postcode,
            country=args.country,
            date=args.date,
            date_end=args.date_end,
            publish_date=args.publish_date,
            summary=args.summary,
            abstract=args.abstract,
            authors=args.author,
            tags=args.tag,
            url_slides=args.url_slides,
            url_pdf=args.url_pdf,
            url_video=args.url_video,
            url_code=args.url_code,
            body_markdown=args.body_markdown,
            featured_source_url=args.featured_source_url,
        )
        serialized = json.dumps(spec.to_dict(), ensure_ascii=False, indent=2) + "\n"
        if args.output:
            Path(args.output).write_text(serialized, encoding="utf-8")
        print(serialized, end="")
        return 0
    spec_data = json.loads(Path(args.spec_json).read_text(encoding="utf-8"))
    spec = EventSpec.from_dict(spec_data)
    path = write_event(repo_root, spec)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
