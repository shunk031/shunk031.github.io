---
name: hugo-publication-thumbnail
description: "Create or regenerate publication `featured.png` thumbnails for this Hugo/HugoBlox site from a local PDF, an arXiv URL, or publication frontmatter. Use when working in this repository and asked to make a publication thumbnail, refresh an existing `featured.png`, resolve a PDF source from `links: Preprint` or `url_pdf`, or run the existing `make publication-thumbnail` flow safely."
---

# Hugo Publication Thumbnail

Create `content/publication/<slug>/featured.png` for publication pages in this repository.

Prefer the repo's existing Makefile target and use the helper script to resolve the PDF source before invoking it.

## Workflow

1. Confirm the publication slug.
- The target page must exist at `content/publication/<slug>/index.md`.

2. Choose the PDF source in this order.
- Use `--pdf <local-path>` when the user already has a PDF file.
- Use `--arxiv-url <url>` when the user gives an arXiv abstract or PDF URL.
- If neither is provided, fall back to publication frontmatter:
- `links` entry with `name: Preprint`
- `url_pdf`

3. Run the helper script.
- Use:
```bash
uv run --with ruamel.yaml python .agents/skills/hugo-publication-thumbnail/scripts/create_publication_thumbnail.py --repo-root . --name <slug> [--pdf <path> | --arxiv-url <url>]
```

4. Validate the result.
- Confirm `content/publication/<slug>/featured.png` exists.
- If the repository has Hugo available, run `hugo build` or spot-check the page.

## Resolution Rules

- Explicit inputs win over frontmatter.
- `--pdf` takes precedence over `--arxiv-url`.
- arXiv abstract URLs are normalized to `https://arxiv.org/pdf/<id>.pdf`.
- When frontmatter fallback is used, `links: Preprint` is preferred over `url_pdf`.
- `url_pdf` may be remote or local. If it resolves to non-PDF content, stop and ask for an explicit local PDF or arXiv URL.

## Repository-Specific Notes

- This repository already defines `make publication-thumbnail`.
- The Makefile converts the first PDF page with ImageMagick and writes `content/publication/<slug>/featured.png`.
- `make ogp-image` writes to the same `featured.png` path. Running this thumbnail workflow may overwrite an existing OGP-style image.

## Script

### scripts/
- `scripts/create_publication_thumbnail.py`
- Resolve the source PDF from explicit inputs or frontmatter.
- Download remote PDFs to a temporary file when needed.
- Delegate image generation to `make publication-thumbnail`.
