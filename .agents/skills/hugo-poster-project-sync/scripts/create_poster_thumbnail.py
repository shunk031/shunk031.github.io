from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def resolve_publication_dir(repo_root: Path, slug: str) -> Path:
    publication_dir = repo_root / "content" / "publication" / slug
    index_path = publication_dir / "index.md"
    if not publication_dir.is_dir():
        raise FileNotFoundError(f"Publication directory not found: {publication_dir}")
    if not index_path.is_file():
        raise FileNotFoundError(f"Publication frontmatter not found: {index_path}")
    return publication_dir


def create_poster_thumbnail(repo_root: Path, slug: str) -> Path:
    publication_dir = resolve_publication_dir(repo_root, slug)
    poster_path = publication_dir / "poster.pdf"
    output_path = publication_dir / "poster-thumbnail.webp"

    if not poster_path.is_file():
        raise FileNotFoundError(f"Poster PDF not found: {poster_path}")

    magick = shutil.which("magick")
    if magick is None:
        raise RuntimeError(
            "ImageMagick 'magick' command is required but was not found in PATH."
        )

    subprocess.run(
        [
            magick,
            "-density",
            "150",
            f"{poster_path}[0]",
            "-background",
            "white",
            "-alpha",
            "remove",
            "-resize",
            "1100x>",
            "-gravity",
            "north",
            "-crop",
            "1100x495+0+0",
            "+repage",
            "-strip",
            "-quality",
            "84",
            str(output_path),
        ],
        cwd=repo_root,
        check=True,
    )

    if not output_path.is_file():
        raise FileNotFoundError(f"Poster thumbnail was not created: {output_path}")

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the Projects thumbnail for a publication poster."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing content/publication.",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Publication slug under content/publication/<name>.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    output_path = create_poster_thumbnail(repo_root, args.name)
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
