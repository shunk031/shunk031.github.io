---
name: hugo-conference-news-sync
description: Create and maintain conference-year news posts for Hugo/HugoBlox sites by grouping `content/publication/*/index.md` entries with `publication_short`, backfilling conference tags, and generating posts in `content/news` with conference tags. Use when asked to batch-create conference announcements, synchronize publication tags (`ANLP`, `ANLP2026` style), add conference tags to news, or avoid duplicate news creation against existing publication links.
---

# Hugo Conference News Sync

Generate conference-year news posts from publication metadata and keep conference tags synchronized.

## Workflow

1. Confirm repository shape.
- Ensure `content/publication` and `content/news` exist.
- Ensure the repo uses front matter with `publication_short`, `publication_types`, `title`, `tags`.

2. Run dry-run first.
- Run:
```bash
uv run --with ruamel.yaml python scripts/sync_conference_news.py --repo-root <repo> --dry-run
```
- Validate:
- Which publication files will receive new conference tags.
- Which conference-year groups will be created.
- Which groups are skipped due to existing publication links in existing news.

3. Apply updates.
- Run:
```bash
uv run --with ruamel.yaml python scripts/sync_conference_news.py --repo-root <repo>
```
- Default behavior:
- Add missing conference tags and conference-year tags to publication entries.
- Classify each publication group from publication `tags`:
- `Domestic Conference` -> presentation-style news under `content/news/<conference>-<year>-presentations/index.md`
- `International Conference` or `International Publication` -> acceptance-style news under `content/news/acceptance-to-<conference-label>/index.md`
- Initialize each new news file with `make news name="<generated-slug>"` before writing final content.
- For both presentation-style and acceptance-style conference news, set tags to `["News", "<CONF>", "<CONF><YEAR>"]`.
- Use `--draft` only when intentionally creating unpublished drafts.
- Set `date` and `lastmod` to the earliest publication `date` in the conference-year group.
- Skip groups already referenced by existing news publication links.

4. Validate output.
- Run `hugo build`.
- Spot-check a few generated files for link quality and description quality.

## Key Rules Implemented by the Script

- Conference/year extraction from `publication_short`:
- Handles `CONF 2026`, `CONF2026`, `CONF-CONF2026`, and `CONF` + year from `date`.
- Removes award annotations like `*（...）*`.
- Uses stripped base venue names for conference tag backfill.
- Maps `NLP` to `ANLP`.
- Keeps venue modifiers such as `SRW` and `Findings of` in generated international news labels/slugs.

- Publication filtering:
- Skip `publication_types` containing `thesis` or `article-journal`.
- Skip journal-like `publication_short` values such as `IEEE Access`, `APIN`, `Appl. Sci.`.

- Tag backfill:
- Ensure `<CONF>` and `<CONF><YEAR>` are present in `tags`.
- Append only missing values.

- News style:
- Domestic conference groups generate `Our Presentations at ...` / `We will present ...`.
- International conference groups generate `Accepted our paper(s) to ...` / `The following paper(s) have/has been accepted ...`.

- Duplicate prevention:
- Parse existing `content/news/*/index.md` and collect `/publication/<slug>` links.
- If any slug in a conference-year group is already linked, skip creating that group by default.

- File bootstrap:
- Prefer `make news` when generating into the repository default `content/news`.
- Fall back to direct file creation if `make news` is unavailable or fails.

- News body format:
- Emit one line per publication in this format:
- `<authors>. ["<title>"](/publication/<slug>).`

## Script

- Path: `scripts/sync_conference_news.py`
- Main options:
```bash
--repo-root <path>         # repository root
--dry-run                  # preview only
--no-sync-tags             # generate news only
--no-skip-linked           # do not skip groups linked by existing news
--draft                    # generate news with draft:true
--target "ANLP 2026"       # limit to specific conference-year (repeatable)
--author "Shunsuke Kitada" # frontmatter author for generated news
```

## Expected Outputs

- Updated publication files with missing conference tags.
- New news files grouped by venue/year, with domestic groups using `*-presentations` and international groups using `acceptance-to-*`.
- Summary logs for modified files, created groups, and skipped groups.

## Post-Processing Checklist

- Confirm `hugo build` passes.
- Confirm generated bullets are link-only.
- Confirm the generated slug/title/body follow the domestic/international convention.
- When needed, regenerate with `--draft` for unpublished staging.
