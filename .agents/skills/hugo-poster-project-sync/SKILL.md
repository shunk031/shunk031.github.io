---
name: hugo-poster-project-sync
description: Register publication posters in this Hugo/HugoBlox site's Projects gallery, generate the dedicated poster thumbnail, and validate the poster bundle contract. Use when adding or replacing a publication `poster.pdf`, backfilling poster thumbnails, adding the `Posters` Projects filter, or fixing CI failures about poster registration, `url_poster`, or `poster-thumbnail.webp`.
---

# Hugo Poster Project Sync

Keep poster assets in the publication leaf bundle and expose only registered posters in the homepage Projects gallery. Do not overwrite `featured.*`; those files remain owned by the publication/OGP thumbnail workflow.

## Workflow

1. Confirm `content/publication/<slug>/index.md` and `poster.pdf` exist.
2. Add the exact `Posters` tag without reformatting unrelated frontmatter.
3. Set `url_poster` to `publication/<slug>/poster.pdf`.
4. Generate the dedicated thumbnail:

   ```sh
   make poster-thumbnail name=<slug>
   ```

   The target delegates to `scripts/create_poster_thumbnail.py` in this skill and writes `poster-thumbnail.webp` beside the PDF.

5. Validate the registration and site:

   ```sh
   uv run --with ruamel.yaml python scripts/lint_frontmatter.py
   mise exec -- hugo --gc --minify --printUnusedTemplates
   ```

## Removal

To remove a poster from Projects, remove the `Posters` tag, `url_poster` value, `poster.pdf`, and `poster-thumbnail.webp` together. Publications without `poster.pdf` are valid and remain outside Projects.

## Thumbnail Contract

- Render the first PDF page at 150 DPI.
- Resize to 1100 px wide, crop the top to 1100 x 495 px, flatten on white, strip metadata, and encode WebP at quality 84.
- Keep the filename exactly `poster-thumbnail.webp` so CI and the Projects view can find it.
