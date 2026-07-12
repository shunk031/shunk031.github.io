---
name: hugo-event-intake
description: Create repo-local Hugo/HugoBlox `content/event` entries from one or more source URLs or sparse notes, gather missing metadata from explicit pages and web search, confirm the candidate spec with the user, and write the page plus `featured.*`. Use when working in this repository and asked to add a Recent & Upcoming Talks item, invited talk, journal club, presentation, poster, report, or similar event entry from Speaker Deck, connpass, confit, PDF, YouTube, official event pages, or rough notes.
---

# Hugo Event Intake

Create a new `content/event/<slug>/index.md` plus `featured.*` for this repository.

Prefer a confirm-then-write workflow. Never overwrite an existing event entry.

## Workflow

1. Probe first.
- Run:
```bash
uv run python .agents/skills/hugo-event-intake/scripts/hugo_event_intake.py probe --repo-root . --input <value> --input <value> --output /tmp/event-spec.json
```
- Inputs may mix URLs and short notes.
- The helper extracts metadata from explicit URLs only.
- It stops early if any input or discovered source already matches an existing `content/event/*/index.md`.

2. Fill unresolved fields.
- Read `unresolved_fields` in `/tmp/event-spec.json`.
- Prefer repository facts first.
- Then inspect the explicit source URLs.
- If gaps remain, browse the web and prefer official organizer pages, conference schedules, or source pages over secondary summaries.
- Re-run `probe` with overrides such as `--kind`, `--title`, `--event`, `--date`, `--date-end`, `--location`, `--summary`, `--abstract`, `--author`, `--tag`, `--url-slides`, `--url-pdf`, `--url-video`, `--url-code`, `--featured-source-url`, or edit the JSON directly.

3. Confirm with the user.
- Show the candidate `slug`, `kind`, `title`, `event`, `date`, `date_end`, `location`, `authors`, `tags`, main URLs, `featured_source_url`, and any remaining unresolved items.
- Check that `slug` is human readable. If it is only digits (for example a connpass event id), derive a descriptive slug from the title or event name instead.
- Check that `summary` is non-empty because the talks list renders it directly.
- Ask for confirmation before writing.
- If the user accepts blanks or guesses, keep that explicit in the summary you show.

4. Write only after confirmation.
- Run:
```bash
uv run python .agents/skills/hugo-event-intake/scripts/hugo_event_intake.py write --repo-root . --spec-json /tmp/event-spec.json
```
- This creates `content/event/<slug>/index.md` and downloads or generates `featured.*`.
- This is create-only. If the slug already exists, stop instead of editing.

## Source Handling

- Speaker Deck URL:
- Set `url_slides`
- Extract title, description, slide cover, and embed id/ratio
- Render `## 資料 - Slides` with the Speaker Deck embed

- Generic HTML event page:
- Set `event_url`
- Extract OG metadata and JSON-LD event fields when present
- Follow discovered media links such as Speaker Deck, PDF, or YouTube

- PDF URL:
- Set `url_pdf`
- Use the PDF as a fallback featured source and generate `featured.png` from the first page

- YouTube URL:
- Set `url_video`

- Search:
- Use browsing only to resolve fields the helper cannot infer from explicit inputs
- Do not treat search results as write-ready unless the key facts line up

## Defaults

- For kind, title, tags, and body conventions, use [references/event-patterns.md](references/event-patterns.md).
- Default authors become `["Shunsuke Kitada"]` unless the user or source clearly indicates otherwise.
- Featured asset priority:
- Explicit `featured_source_url`
- Slide cover or `og:image`
- PDF first page thumbnail
- Keep `summary` non-empty whenever possible because the talks list renders it directly.

## When To Stop

- Stop if the same source URL already exists in `content/event`.
- Stop if official sources disagree on date, event name, or location and the user has not resolved it.
- Stop if the page is too custom for the standard template and would require substantial hand-written body content.
