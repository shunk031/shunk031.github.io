from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from ruamel.yaml import YAML


yaml = YAML(typ="safe")
ARXIV_HOSTS = {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}


@dataclass
class ResolvedSource:
    kind: str
    value: str
    origin: str


def normalize_arxiv_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc not in ARXIV_HOSTS:
        return url

    if parsed.path.startswith("/abs/"):
        paper_id = parsed.path.removeprefix("/abs/")
        return f"https://arxiv.org/pdf/{paper_id}.pdf"

    if parsed.path.startswith("/pdf/") and parsed.path.endswith(".pdf"):
        return f"https://arxiv.org{parsed.path}"

    if parsed.path.startswith("/pdf/"):
        paper_id = parsed.path.removeprefix("/pdf/")
        return f"https://arxiv.org/pdf/{paper_id}.pdf"

    return url


def load_frontmatter(index_path: Path) -> dict:
    text = index_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Missing frontmatter in {index_path}")

    for end_index in range(1, len(lines)):
        if lines[end_index].strip() == "---":
            frontmatter_text = "\n".join(lines[1:end_index]) + "\n"
            return yaml.load(frontmatter_text) or {}

    raise ValueError(f"Missing frontmatter terminator in {index_path}")


def resolve_publication_paths(repo_root: Path, slug: str) -> tuple[Path, Path]:
    publication_dir = repo_root / "content" / "publication" / slug
    index_path = publication_dir / "index.md"
    if not publication_dir.is_dir():
        raise FileNotFoundError(f"Publication directory not found: {publication_dir}")
    if not index_path.is_file():
        raise FileNotFoundError(f"Publication frontmatter not found: {index_path}")
    return publication_dir, index_path


def resolve_local_pdf_path(repo_root: Path, publication_dir: Path, raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    if candidate.is_absolute():
        resolved = candidate.resolve()
        if resolved.is_file():
            return resolved
        raise FileNotFoundError(f"Local PDF not found: {resolved}")

    relative_candidates = [
        publication_dir / candidate,
        repo_root / candidate,
    ]
    for relative_candidate in relative_candidates:
        resolved = relative_candidate.resolve()
        if resolved.is_file():
            return resolved

    raise FileNotFoundError(f"Local PDF not found: {raw_path}")


def find_preprint_url(frontmatter: dict) -> str | None:
    links = frontmatter.get("links") or []
    if not isinstance(links, list):
        return None

    for link in links:
        if not isinstance(link, dict):
            continue
        name = str(link.get("name", "")).strip().lower()
        url = str(link.get("url", "")).strip()
        if name == "preprint" and url:
            return url

    return None


def resolve_source(
    repo_root: Path,
    slug: str,
    *,
    pdf: str | None = None,
    arxiv_url: str | None = None,
) -> ResolvedSource:
    publication_dir, index_path = resolve_publication_paths(repo_root, slug)

    if pdf:
        resolved_pdf = resolve_local_pdf_path(repo_root, publication_dir, pdf)
        return ResolvedSource(kind="local", value=str(resolved_pdf), origin="explicit-pdf")

    if arxiv_url:
        normalized = normalize_arxiv_url(arxiv_url)
        if urlparse(normalized).netloc not in ARXIV_HOSTS:
            raise ValueError(f"--arxiv-url must point to arXiv: {arxiv_url}")
        return ResolvedSource(kind="remote", value=normalized, origin="explicit-arxiv")

    frontmatter = load_frontmatter(index_path)
    preprint_url = find_preprint_url(frontmatter)
    if preprint_url:
        return ResolvedSource(
            kind="remote",
            value=normalize_arxiv_url(preprint_url),
            origin="frontmatter-preprint",
        )

    url_pdf = str(frontmatter.get("url_pdf") or "").strip()
    if url_pdf:
        parsed = urlparse(url_pdf)
        if parsed.scheme and parsed.netloc:
            return ResolvedSource(kind="remote", value=url_pdf, origin="frontmatter-url-pdf")
        local_pdf = resolve_local_pdf_path(repo_root, publication_dir, url_pdf)
        return ResolvedSource(kind="local", value=str(local_pdf), origin="frontmatter-url-pdf")

    raise ValueError(
        f"Could not resolve a PDF source for '{slug}'. "
        "Pass --pdf or --arxiv-url, or populate links: Preprint / url_pdf in the publication frontmatter."
    )


def download_remote_pdf(url: str, destination: Path) -> Path:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=120) as response:
        data = response.read()

    if not data.startswith(b"%PDF-"):
        raise ValueError(f"Downloaded content is not a PDF: {url}")

    destination.write_bytes(data)
    return destination


def create_thumbnail(repo_root: Path, slug: str, pdf_path: Path) -> Path:
    if shutil.which("magick") is None:
        raise RuntimeError("ImageMagick 'magick' command is required but was not found in PATH.")

    output_path = repo_root / "content" / "publication" / slug / "featured.png"
    env = os.environ.copy()
    env["PWD"] = str(repo_root)
    subprocess.run(
        [
            "make",
            "publication-thumbnail",
            f"pdf={pdf_path}",
            f"name={slug}",
        ],
        cwd=repo_root,
        check=True,
        env=env,
    )

    if not output_path.is_file():
        raise FileNotFoundError(f"Thumbnail was not created: {output_path}")

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Hugo publication thumbnail from a PDF source.")
    parser.add_argument("--repo-root", default=".", help="Repository root containing content/publication and Makefile.")
    parser.add_argument("--name", required=True, help="Publication slug under content/publication/<name>.")
    parser.add_argument("--pdf", help="Path to a local PDF file.")
    parser.add_argument("--arxiv-url", help="arXiv abstract or PDF URL.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    source = resolve_source(repo_root, args.name, pdf=args.pdf, arxiv_url=args.arxiv_url)

    output_path = repo_root / "content" / "publication" / args.name / "featured.png"
    if output_path.exists():
        print(f"Overwriting existing thumbnail: {output_path}")

    if source.kind == "local":
        output_path = create_thumbnail(repo_root, args.name, Path(source.value))
    else:
        with tempfile.TemporaryDirectory(prefix="publication-thumbnail-") as tmp_dir:
            tmp_pdf_path = Path(tmp_dir) / "paper.pdf"
            download_remote_pdf(source.value, tmp_pdf_path)
            output_path = create_thumbnail(repo_root, args.name, tmp_pdf_path)

    print(f"Created {output_path} from {source.origin}: {source.value}")


if __name__ == "__main__":
    main()
