from __future__ import annotations

import importlib.util
import os
import stat
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "hugo-publication-thumbnail"
    / "scripts"
    / "create_publication_thumbnail.py"
)


def load_thumbnail_module():
    assert SCRIPT_PATH.exists(), f"missing script: {SCRIPT_PATH}"
    spec = importlib.util.spec_from_file_location("create_publication_thumbnail", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_publication(
    tmp_path: Path,
    *,
    slug: str = "sample2026paper",
    preprint_url: str | None = None,
    url_pdf: str | None = None,
) -> tuple[Path, Path]:
    repo_root = tmp_path / "repo"
    publication_dir = repo_root / "content" / "publication" / slug
    publication_dir.mkdir(parents=True)

    links_block = "links: []"
    if preprint_url is not None:
        links_block = "\n".join(
            [
                "links:",
                "- name: Preprint",
                f"  url: {preprint_url}",
            ]
        )

    pdf_value = '""' if url_pdf is None else url_pdf
    (publication_dir / "index.md").write_text(
        "\n".join(
            [
                "---",
                'title: "Sample Publication"',
                links_block,
                f"url_pdf: {pdf_value}",
                "---",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return repo_root, publication_dir


def install_fake_command(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def test_normalize_arxiv_url_converts_abs_to_pdf() -> None:
    module = load_thumbnail_module()

    assert module.normalize_arxiv_url("https://arxiv.org/abs/2507.02212") == "https://arxiv.org/pdf/2507.02212.pdf"
    assert module.normalize_arxiv_url("https://arxiv.org/pdf/2507.02212.pdf") == "https://arxiv.org/pdf/2507.02212.pdf"
    assert module.normalize_arxiv_url("https://arxiv.org/abs/2104.08763v1") == "https://arxiv.org/pdf/2104.08763v1.pdf"


def test_resolve_source_prefers_explicit_pdf_over_other_inputs(tmp_path: Path) -> None:
    module = load_thumbnail_module()
    repo_root, _ = write_publication(
        tmp_path,
        preprint_url="https://arxiv.org/abs/2507.02212",
        url_pdf="https://example.com/paper.pdf",
    )
    pdf_path = tmp_path / "explicit.pdf"
    pdf_path.write_bytes(b"%PDF-1.7\n")

    resolved = module.resolve_source(
        repo_root,
        "sample2026paper",
        pdf=str(pdf_path),
        arxiv_url="https://arxiv.org/abs/9999.99999",
    )

    assert resolved.kind == "local"
    assert resolved.value == str(pdf_path.resolve())
    assert resolved.origin == "explicit-pdf"


def test_resolve_source_uses_explicit_arxiv_url_when_pdf_is_missing(tmp_path: Path) -> None:
    module = load_thumbnail_module()
    repo_root, _ = write_publication(
        tmp_path,
        preprint_url="https://arxiv.org/abs/2507.02212",
        url_pdf="https://example.com/paper.pdf",
    )

    resolved = module.resolve_source(
        repo_root,
        "sample2026paper",
        arxiv_url="https://arxiv.org/abs/2605.00551",
    )

    assert resolved.kind == "remote"
    assert resolved.value == "https://arxiv.org/pdf/2605.00551.pdf"
    assert resolved.origin == "explicit-arxiv"


def test_resolve_source_uses_frontmatter_preprint_before_url_pdf(tmp_path: Path) -> None:
    module = load_thumbnail_module()
    repo_root, _ = write_publication(
        tmp_path,
        preprint_url="https://arxiv.org/abs/2507.02212",
        url_pdf="https://example.com/paper.pdf",
    )

    resolved = module.resolve_source(repo_root, "sample2026paper")

    assert resolved.kind == "remote"
    assert resolved.value == "https://arxiv.org/pdf/2507.02212.pdf"
    assert resolved.origin == "frontmatter-preprint"


def test_resolve_source_falls_back_to_frontmatter_url_pdf(tmp_path: Path) -> None:
    module = load_thumbnail_module()
    repo_root, _ = write_publication(
        tmp_path,
        url_pdf="https://example.com/paper.pdf",
    )

    resolved = module.resolve_source(repo_root, "sample2026paper")

    assert resolved.kind == "remote"
    assert resolved.value == "https://example.com/paper.pdf"
    assert resolved.origin == "frontmatter-url-pdf"


def test_resolve_source_raises_when_no_source_is_available(tmp_path: Path) -> None:
    module = load_thumbnail_module()
    repo_root, _ = write_publication(tmp_path)

    with pytest.raises(ValueError, match="Could not resolve a PDF source"):
        module.resolve_source(repo_root, "sample2026paper")


def test_create_thumbnail_runs_make_target_and_writes_featured_png(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_thumbnail_module()
    repo_root, publication_dir = write_publication(tmp_path)
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"%PDF-1.7\n")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    make_log = tmp_path / "make.log"
    install_fake_command(
        bin_dir / "magick",
        "#!/bin/sh\nexit 0\n",
    )
    install_fake_command(
        bin_dir / "make",
        "\n".join(
            [
                "#!/bin/sh",
                f"printf '%s\\n' \"$@\" > '{make_log}'",
                "name=''",
                "for arg in \"$@\"; do",
                "  case \"$arg\" in",
                "    name=*) name=\"${arg#name=}\" ;;",
                "  esac",
                "done",
                "mkdir -p \"$PWD/content/publication/$name\"",
                "printf 'PNG' > \"$PWD/content/publication/$name/featured.png\"",
                "exit 0",
            ]
        )
        + "\n",
    )
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")

    output_path = module.create_thumbnail(repo_root, "sample2026paper", pdf_path)

    assert output_path == publication_dir / "featured.png"
    assert output_path.exists()
    assert make_log.read_text(encoding="utf-8").splitlines() == [
        "publication-thumbnail",
        f"pdf={pdf_path}",
        "name=sample2026paper",
    ]


def test_create_thumbnail_sets_pwd_env_to_repo_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_thumbnail_module()
    repo_root, publication_dir = write_publication(tmp_path)
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"%PDF-1.7\n")
    captured: dict[str, str] = {}

    def fake_run(*args, **kwargs) -> None:
        captured["pwd"] = kwargs["env"]["PWD"]
        (publication_dir / "featured.png").write_bytes(b"PNG")

    monkeypatch.setattr(module.shutil, "which", lambda command: "/tmp/magick" if command == "magick" else None)
    monkeypatch.setattr(module.subprocess, "run", fake_run)

    output_path = module.create_thumbnail(repo_root, "sample2026paper", pdf_path)

    assert output_path == publication_dir / "featured.png"
    assert captured["pwd"] == str(repo_root)
