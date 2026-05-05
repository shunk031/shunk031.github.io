#!/usr/bin/env python3
"""Sync conference-year tags and generate conference news posts from publications."""

from __future__ import annotations

import argparse
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq


CONF_NAME_MAP = {
    "NLP": "ANLP",
}
NEWS_KIND_PRESENTATIONS = "presentations"
NEWS_KIND_ACCEPTANCE = "acceptance"
DOMESTIC_CONFERENCE_TAG = "Domestic Conference"
INTERNATIONAL_NEWS_TAGS = {"International Conference", "International Publication"}

SKIP_PUBLICATION_TYPES = {"thesis", "article-journal"}
JOURNAL_LIKE_SHORTS = {
    "IEEE Access",
    "APIN",
    "Appl. Sci.",
    "Applied Sciences",
    "Ph.D. dissertation",
}


@dataclass(frozen=True)
class ConferenceKey:
    """Conference identifier used for grouping and news slug generation."""

    name: str
    year: str
    display_label: str
    news_kind: str

    @property
    def label(self) -> str:
        """Return display label such as `ANLP 2026` or `ACL2026 SRW`."""

        return self.display_label

    @property
    def slug(self) -> str:
        """Return news slug based on the domestic/international convention."""

        base = slugify_label(self.display_label)
        if self.news_kind == NEWS_KIND_ACCEPTANCE:
            return f"acceptance-to-{base}"
        return f"{base}-presentations"


@dataclass
class Publication:
    """Publication metadata required for tag sync and news rendering."""

    path: Path
    slug: str
    title: str
    authors: list[str]
    date: str
    conf: ConferenceKey


@dataclass(frozen=True)
class ConferenceTagKey:
    """Conference tag identifier used for existing news tag backfill."""

    name: str
    year: str


def slugify_label(value: str) -> str:
    """Convert a human-readable label into a stable slug fragment."""

    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def conference_year_tag(name: str, year: str) -> str:
    """Return the conference-year tag value such as `CVPR2026`."""

    return f"{name}{year}"


def conference_news_tags(name: str, year: str) -> list[str]:
    """Return the standard news tags for conference news."""

    return ["News", name, conference_year_tag(name, year)]


def flow_style_sequence(items: list[str]) -> CommentedSeq:
    """Return a flow-style YAML sequence for compact front matter lists."""

    sequence = CommentedSeq(items)
    sequence.fa.set_flow_style()
    return sequence


def conference_news_tags_line(name: str, year: str) -> str:
    """Return the YAML line for standard conference news tags."""

    return f'tags: ["News", "{name}", "{conference_year_tag(name, year)}"]'


class FrontmatterIO:
    """Read and write Hugo front matter while preserving formatting."""

    def __init__(self) -> None:
        """Configure `ruamel.yaml` for stable front matter round-trip edits."""

        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.default_flow_style = None
        self.yaml.width = 4096
        self.yaml.allow_duplicate_keys = True

    def read(self, path: Path) -> tuple[dict, str]:
        """Return parsed front matter and markdown body from a content file."""

        text = path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) < 3:
            raise ValueError(f"Invalid frontmatter format: {path}")
        frontmatter = self.yaml.load(parts[1]) or {}
        body = parts[2]
        return frontmatter, body

    def write(self, path: Path, frontmatter: dict, body: str) -> None:
        """Write front matter and body back to disk."""

        from io import StringIO

        stream = StringIO()
        self.yaml.dump(frontmatter, stream)
        fm = stream.getvalue().rstrip("\n")
        path.write_text(f"---\n{fm}\n---{body}", encoding="utf-8")


def strip_publication_short_decorations(value: str) -> str:
    """Remove award-like decorations while keeping the visible venue label."""

    normalized = value.strip()
    normalized = re.sub(r"\s*\*（[^）]*）\*", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def build_display_label(publication_short: str) -> str:
    """Build the visible news label while preserving venue modifiers like `SRW`."""

    display = strip_publication_short_decorations(publication_short)
    display = re.sub(r"^NLP(?=(?:\s|\d))", "ANLP", display)
    return display


def normalize_publication_short(value: str) -> str:
    """Normalize `publication_short` for base conference/year parsing."""

    normalized = strip_publication_short_decorations(value)
    normalized = re.sub(r"^(?i:findings of)\s+", "", normalized)
    normalized = re.sub(r"\s+SRW$", "", normalized)
    return normalized.strip()


def infer_news_kind(tags: object) -> str:
    """Decide whether a news post should use acceptance or presentation wording."""

    normalized_tags = {str(tag) for tag in (tags or [])}
    if DOMESTIC_CONFERENCE_TAG in normalized_tags:
        return NEWS_KIND_PRESENTATIONS
    if normalized_tags & INTERNATIONAL_NEWS_TAGS:
        return NEWS_KIND_ACCEPTANCE
    return NEWS_KIND_PRESENTATIONS


def infer_tag_key_from_title(title: str) -> ConferenceTagKey | None:
    """Infer conference/year tags from a news title when linked publications are insufficient."""

    normalized_title = " ".join(str(title).strip().split())
    if not normalized_title or "journal" in normalized_title.lower():
        return None

    matches: list[ConferenceTagKey] = []
    patterns = (
        r"([A-Z]+-[A-Z]+)\s*(\d{4})",
        r"([A-Z]+[A-Z-]*)\s*(\d{4})",
        r"([A-Z]+)\s+(\d{4})",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, normalized_title):
            conf = CONF_NAME_MAP.get(match.group(1), match.group(1))
            matches.append(ConferenceTagKey(conf, match.group(2)))

    if not matches:
        return None
    return matches[-1]


def parse_conf_key(
    publication_short: str, date_value: object, tags: object
) -> ConferenceKey | None:
    """Parse conference metadata from `publication_short`, tags, and fallback date."""

    short = normalize_publication_short(publication_short)
    if not short or short in JOURNAL_LIKE_SHORTS:
        return None

    display_label = build_display_label(publication_short)
    news_kind = infer_news_kind(tags)
    patterns = (
        r"^([A-Z]+)\s+(\d{4})$",
        r"^([A-Z]+[A-Z-]*)(\d{4})$",
        r"^([A-Z]+-[A-Z]+)(\d{4})$",
    )
    for pattern in patterns:
        match = re.match(pattern, short)
        if match:
            conf = CONF_NAME_MAP.get(match.group(1), match.group(1))
            return ConferenceKey(conf, match.group(2), display_label, news_kind)

    only_name = re.match(r"^([A-Z]+)$", short)
    if only_name:
        year_match = re.search(r"(\d{4})", str(date_value or ""))
        if not year_match:
            return None
        conf = CONF_NAME_MAP.get(only_name.group(1), only_name.group(1))
        return ConferenceKey(conf, year_match.group(1), display_label, news_kind)

    return None


def find_linked_publication_slugs(news_dir: Path) -> set[str]:
    """Collect publication slugs already linked from existing news posts."""

    linked: set[str] = set()
    if not news_dir.exists():
        return linked
    for index_md in news_dir.glob("*/index.md"):
        text = index_md.read_text(encoding="utf-8")
        linked.update(re.findall(r"/publication/([a-zA-Z0-9-]+)", text))
    return linked


def parse_publications(publication_dir: Path, io: FrontmatterIO) -> list[Publication]:
    """Load conference-related publications from `content/publication`."""

    publications: list[Publication] = []

    for index_md in sorted(publication_dir.glob("*/index.md")):
        frontmatter, _ = io.read(index_md)
        publication_types = set(frontmatter.get("publication_types") or [])
        if publication_types & SKIP_PUBLICATION_TYPES:
            continue

        publication_short = frontmatter.get("publication_short")
        if not publication_short:
            continue

        conf = parse_conf_key(
            str(publication_short),
            frontmatter.get("date"),
            frontmatter.get("tags") or [],
        )
        if not conf:
            continue

        publications.append(
            Publication(
                path=index_md,
                slug=index_md.parent.name,
                title=str(frontmatter.get("title") or index_md.parent.name),
                authors=[str(author) for author in (frontmatter.get("authors") or [])],
                date=str(frontmatter.get("date") or ""),
                conf=conf,
            )
        )

    return publications


def sync_tags(
    publications: Iterable[Publication], io: FrontmatterIO, dry_run: bool
) -> tuple[int, list[str]]:
    """Backfill conference tags for publication pages and report changes."""

    modified = 0
    details: list[str] = []

    for publication in publications:
        frontmatter, body = io.read(publication.path)
        tags = list(frontmatter.get("tags") or [])
        missing: list[str] = []
        conf_tag = publication.conf.name
        year_tag = f"{publication.conf.name}{publication.conf.year}"
        for tag in (conf_tag, year_tag):
            if tag not in tags:
                tags.append(tag)
                missing.append(tag)
        if not missing:
            continue

        frontmatter["tags"] = tags
        modified += 1
        details.append(f"{publication.slug}: +{', '.join(missing)}")
        if not dry_run:
            io.write(publication.path, frontmatter, body)

    return modified, details


def infer_existing_news_tag_key(
    frontmatter: dict, body: str, publications_by_slug: dict[str, Publication]
) -> ConferenceTagKey | None:
    """Infer conference/year tags for an existing acceptance-style news file."""

    linked_slugs = re.findall(r"/publication/([a-zA-Z0-9-]+)", body)
    linked_keys = {
        ConferenceTagKey(publication.conf.name, publication.conf.year)
        for slug in linked_slugs
        if (publication := publications_by_slug.get(slug)) is not None
    }
    if len(linked_keys) == 1:
        return next(iter(linked_keys))

    return infer_tag_key_from_title(str(frontmatter.get("title") or ""))


def sync_existing_news_tags(
    news_dir: Path,
    publications_by_slug: dict[str, Publication],
    io: FrontmatterIO,
    dry_run: bool,
) -> tuple[int, list[str]]:
    """Backfill conference tags for existing acceptance-style conference news."""

    modified = 0
    details: list[str] = []

    for index_md in sorted(news_dir.glob("acceptance-to-*/index.md")):
        frontmatter, body = io.read(index_md)
        tag_key = infer_existing_news_tag_key(frontmatter, body, publications_by_slug)
        if tag_key is None:
            continue

        tags = list(frontmatter.get("tags") or [])
        missing = [
            tag
            for tag in conference_news_tags(tag_key.name, tag_key.year)
            if tag not in tags
        ]
        if not missing:
            continue

        frontmatter["tags"] = flow_style_sequence(tags + missing)
        modified += 1
        details.append(f"{index_md.parent.name}: +{', '.join(missing)}")
        if not dry_run:
            io.write(index_md, frontmatter, body)

    return modified, details


def render_news_markdown(
    conf: ConferenceKey,
    publications: list[Publication],
    *,
    author: str,
    conference_date: str,
    draft: bool,
) -> str:
    """Render a complete `content/news/<slug>/index.md` markdown string."""

    paper_word = "paper" if len(publications) == 1 else "papers"
    news_tags = conference_news_tags_line(conf.name, conf.year)
    if conf.news_kind == NEWS_KIND_ACCEPTANCE:
        title = f"Accepted our {paper_word} to {conf.label}"
        body = (
            f"The following {paper_word} has been accepted to {conf.label}:"
            if len(publications) == 1
            else f"The following {paper_word} have been accepted to {conf.label}:"
        )
    else:
        title = f"Our Presentations at {conf.label}"
        body = f"We will present the following {paper_word} at {conf.label}:"

    lines: list[str] = [
        "---",
        "# Documentation: https://docs.hugoblox.com/managing-content/",
        "",
        f'title: "{title}"',
        'subtitle: ""',
        'summary: ""',
        f'authors: ["{author}"]',
        news_tags,
        'categories: ["News"]',
        f"date: {conference_date}",
        f"lastmod: {conference_date}",
        "featured: false",
        f"draft: {'true' if draft else 'false'}",
        "",
        "# Featured image",
        "# To use, add an image named `featured.jpg/png` to your page's folder.",
        "# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.",
        "image:",
        '  caption: ""',
        '  focal_point: ""',
        "  preview_only: false",
        "",
        "# Projects (optional).",
        "#   Associate this post with one or more of your projects.",
        "#   Simply enter your project's folder or file name without extension.",
        '#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.',
        "#   Otherwise, set `projects = []`.",
        "projects: []",
        "---",
        "",
        body,
        "",
    ]
    for publication in publications:
        author_text = ", ".join(publication.authors) if publication.authors else "Unknown Author"
        title_text = publication.title.replace('"', '\\"')
        lines.append(
            f'- {author_text}. ["{title_text}"](/publication/{publication.slug}).'
        )
    lines.append("")
    return "\n".join(lines)


def parse_targets(values: list[str]) -> set[str]:
    """Normalize repeated `--target` values for exact label matching."""

    normalized: set[str] = set()
    for value in values:
        normalized.add(" ".join(value.strip().split()))
    return normalized


def resolve_conference_date(publications: list[Publication], fallback: str) -> str:
    """Return earliest publication date in a group, or fallback when missing."""

    parsed: list[tuple[datetime, str]] = []
    for publication in publications:
        try:
            parsed.append((datetime.fromisoformat(publication.date), publication.date))
        except Exception:
            continue
    if not parsed:
        return fallback
    parsed.sort(key=lambda x: x[0])
    return parsed[0][1]


def initialize_news_file(repo_root: Path, news_dir: Path, out_file: Path, slug: str) -> str:
    """Initialize a new news file via `make news`, with direct-write fallback."""

    default_news_dir = (repo_root / "content/news").resolve()
    use_make = news_dir.resolve() == default_news_dir

    if use_make:
        try:
            subprocess.run(
                ["make", "news", f"name={slug}"],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            )
            if out_file.exists():
                return "make news"
        except (FileNotFoundError, subprocess.CalledProcessError) as error:
            print(f"[news] warning {slug}: make news failed, fallback to direct write ({error})")

    out_file.parent.mkdir(parents=True, exist_ok=True)
    if not out_file.exists():
        out_file.touch()
    return "direct write"


def main() -> None:
    """Run conference tag sync and conference-year news generation."""

    parser = argparse.ArgumentParser(
        description=(
            "Backfill conference tags in publications and create conference-year "
            "news posts from publication_short."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Repository root that contains content/publication and content/news.",
    )
    parser.add_argument(
        "--publication-dir",
        type=Path,
        default=Path("content/publication"),
        help="Publication directory, relative to --repo-root unless absolute.",
    )
    parser.add_argument(
        "--news-dir",
        type=Path,
        default=Path("content/news"),
        help="News directory, relative to --repo-root unless absolute.",
    )
    parser.add_argument(
        "--author",
        default="Shunsuke Kitada",
        help="Author name used in generated news frontmatter.",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Generate news with draft:true (default is draft:false).",
    )
    parser.add_argument(
        "--no-sync-tags",
        action="store_true",
        help="Skip publication tag backfill.",
    )
    parser.add_argument(
        "--no-skip-linked",
        action="store_true",
        help=(
            "Generate news even when an existing news file already links one of the "
            "group's publication slugs."
        ),
    )
    parser.add_argument(
        "--target",
        action="append",
        default=[],
        metavar="CONF_YEAR",
        help='Limit generation to specific groups, e.g., --target "ANLP 2026".',
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned updates without writing files.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    publication_dir = (
        args.publication_dir
        if args.publication_dir.is_absolute()
        else repo_root / args.publication_dir
    )
    news_dir = args.news_dir if args.news_dir.is_absolute() else repo_root / args.news_dir
    if not publication_dir.exists():
        raise FileNotFoundError(f"Publication directory not found: {publication_dir}")
    if not news_dir.exists():
        raise FileNotFoundError(f"News directory not found: {news_dir}")

    io = FrontmatterIO()
    publications = parse_publications(publication_dir, io)
    publications_by_slug = {publication.slug: publication for publication in publications}
    grouped: dict[ConferenceKey, list[Publication]] = defaultdict(list)
    for publication in publications:
        grouped[publication.conf].append(publication)

    targets = parse_targets(args.target)
    if targets:
        grouped = {
            key: value
            for key, value in grouped.items()
            if key.label in targets
        }

    now_iso = datetime.now().astimezone().replace(microsecond=0).isoformat()
    linked = find_linked_publication_slugs(news_dir)

    if not args.no_sync_tags:
        modified, details = sync_tags(publications, io, args.dry_run)
        print(f"[tags] modified publication files: {modified}")
        for item in details:
            print(f"  - {item}")
    else:
        print("[tags] skipped")

    existing_news_modified, existing_news_details = sync_existing_news_tags(
        news_dir,
        publications_by_slug,
        io,
        args.dry_run,
    )
    print(f"[news-tags] modified existing news files: {existing_news_modified}")
    for item in existing_news_details:
        print(f"  - {item}")

    created = 0
    skipped = 0
    draft = args.draft
    skip_linked = not args.no_skip_linked

    for conf in sorted(grouped, key=lambda c: (c.year, c.name)):
        items = sorted(grouped[conf], key=lambda x: x.slug)
        out_dir = news_dir / conf.slug
        out_file = out_dir / "index.md"

        if skip_linked and any(item.slug in linked for item in items):
            skipped += 1
            print(f"[news] skip {conf.label}: already linked in existing news")
            continue
        if out_file.exists():
            skipped += 1
            print(f"[news] skip {conf.label}: {out_file} already exists")
            continue

        content = render_news_markdown(
            conf,
            items,
            author=args.author,
            conference_date=resolve_conference_date(items, now_iso),
            draft=draft,
        )

        created += 1
        if args.dry_run:
            print(f"[news] create {conf.label}: {out_file}")
            continue

        method = initialize_news_file(repo_root, news_dir, out_file, conf.slug)
        out_file.write_text(content, encoding="utf-8")
        print(f"[news] created {conf.label}: {out_file} ({method})")

    print(
        f"[summary] groups={len(grouped)} created={created} skipped={skipped} dry_run={args.dry_run}"
    )


if __name__ == "__main__":
    main()
