from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "hugo-poster-project-sync"
    / "scripts"
    / "create_poster_thumbnail.py"
)


def load_thumbnail_module():
    assert SCRIPT_PATH.exists(), f"missing script: {SCRIPT_PATH}"
    spec = importlib.util.spec_from_file_location(
        "create_poster_thumbnail", SCRIPT_PATH
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def create_publication(
    tmp_path: Path, *, with_poster: bool = True
) -> tuple[Path, Path]:
    repo_root = tmp_path / "repo"
    publication_dir = repo_root / "content" / "publication" / "sample2026conf"
    publication_dir.mkdir(parents=True)
    (publication_dir / "index.md").write_text(
        '---\ntitle: "Sample Poster"\n---\n',
        encoding="utf-8",
    )
    if with_poster:
        (publication_dir / "poster.pdf").write_bytes(b"%PDF-1.7\n")
    return repo_root, publication_dir


def test_create_thumbnail_uses_projects_card_dimensions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_thumbnail_module()
    repo_root, publication_dir = create_publication(tmp_path)
    captured: dict[str, object] = {}

    monkeypatch.setattr(shutil, "which", lambda command: "/tmp/magick")

    def fake_run(command: list[str], **kwargs: object) -> None:
        captured["command"] = command
        captured["cwd"] = kwargs["cwd"]
        (publication_dir / "poster-thumbnail.webp").write_bytes(b"WEBP")

    monkeypatch.setattr(subprocess, "run", fake_run)

    output_path = module.create_poster_thumbnail(repo_root, "sample2026conf")

    assert output_path == publication_dir / "poster-thumbnail.webp"
    assert captured["cwd"] == repo_root
    assert captured["command"] == [
        "/tmp/magick",
        "-density",
        "150",
        f"{publication_dir / 'poster.pdf'}[0]",
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
        str(publication_dir / "poster-thumbnail.webp"),
    ]


def test_create_thumbnail_requires_poster_pdf(tmp_path: Path) -> None:
    module = load_thumbnail_module()
    repo_root, _ = create_publication(tmp_path, with_poster=False)

    with pytest.raises(FileNotFoundError, match="Poster PDF not found"):
        module.create_poster_thumbnail(repo_root, "sample2026conf")


def test_create_thumbnail_requires_imagemagick(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_thumbnail_module()
    repo_root, _ = create_publication(tmp_path)
    monkeypatch.setattr(shutil, "which", lambda command: None)

    with pytest.raises(RuntimeError, match="ImageMagick"):
        module.create_poster_thumbnail(repo_root, "sample2026conf")
