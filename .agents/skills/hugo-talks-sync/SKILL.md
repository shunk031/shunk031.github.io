---
name: hugo-talks-sync
description: Discover missing Recent & Upcoming Talks for this Hugo/HugoBlox repository by comparing shunk031's external talk sources with existing content/event entries. Use when asked to update, audit, backfill, or synchronize talks from Speaker Deck profiles, generic RSS/Atom feeds, slide lists, organizer pages, or other external talk indexes before creating event pages with hugo-event-intake.
---

# Hugo Talks Sync

Find candidate talks that are present on external indexes but missing from
`content/event`, then route accepted candidates through `hugo-event-intake`.

Use this skill as the discovery layer. Use `hugo-event-intake` as the write layer.
Do not create or overwrite event pages directly from this skill.

## Workflow

1. Audit external sources.

Run the helper from the repository root:

```bash
uv run python .agents/skills/hugo-talks-sync/scripts/hugo_talks_sync.py audit --repo-root . --output /tmp/hugo-talks-sync.json
```

Defaults:

- Source adapter: `speakerdeck-profile`
- Speaker Deck profile URL: `https://speakerdeck.com/shunk031`
- Existing event root: `content/event`
- Duplicate check fields: `event_url`, `url_slides`, `url_pdf`, `url_video`, `url_code`, and Markdown body URLs

Use source options when the user names different sources:

- `--profile-url <speakerdeck-profile-url>` changes the default Speaker Deck profile.
- `--feed-url <rss-or-atom-url>` adds a generic auto-detected RSS/Atom `feed` source. Repeat it for multiple feeds.
- `--source-config <json-file>` loads explicit source definitions.

Source config shape:

```json
{
  "sources": [
    {
      "name": "speakerdeck-shunk031",
      "adapter": "speakerdeck-profile",
      "profile_url": "https://speakerdeck.com/shunk031",
      "options": {}
    },
    {
      "name": "personal-talk-feed",
      "adapter": "atom",
      "url": "https://example.com/talks.atom",
      "options": {}
    }
  ]
}
```

First-class adapters are currently `speakerdeck-profile`, auto-detected `feed`,
explicit `rss`, and explicit `atom`. For HTML index pages, APIs, or
platform-specific sources such as connpass users or YouTube channels, add a
source adapter to the registry in
`scripts/hugo_talks_sync.py` instead of scraping ad hoc in the workflow.

2. Review `/tmp/hugo-talks-sync.json`.

For each candidate, inspect:

- `source_url`: the Speaker Deck page or external source
- `source_name`, `adapter`, and `source_type` (a compatibility alias of `adapter`)
- `title`
- `published_at`
- `image_url`
- `description`
- `extracted_urls`: organizer, paper, code, video, or PDF URLs found in the feed description
- `likely_kind` and `suggested_tags`: tentative classification to carry into
  `hugo-event-intake` review. Empty `likely_kind` means the source did not
  provide enough evidence; resolve it before writing.
- `suggested_intake_inputs`: URLs to pass to `hugo-event-intake`

Skip candidates marked `existing_path`. They already match an event entry.

3. Cross-check uncertain candidates.

Read [references/source-policy.md](references/source-policy.md) when deciding which
external facts are sufficient. In short: feeds are enough to identify source
items, but not always enough to determine event name, exact talk time, location,
or talk kind. Prefer organizer pages discovered in `extracted_urls`.

4. Present a proposal before writing.

Show the user a compact table of missing candidates with:

- title
- source URL
- date from the feed
- likely organizer URL if discovered
- any missing fields that `hugo-event-intake` will need to resolve

Ask which candidates to create. Do not assume that every Speaker Deck upload should
be a site event; some decks are notes, paper readings, or drafts.
Do not keep `Speaker Deck` as the event name or `Report` as the kind when the
description or discovered URLs show that the deck is a paper reading or journal
club entry.

5. Create accepted events through `hugo-event-intake`.

For each accepted candidate, run the existing intake probe with the suggested URLs:

```bash
uv run python .agents/skills/hugo-event-intake/scripts/hugo_event_intake.py probe --repo-root . --input <speaker-deck-url> --input <organizer-url> --output /tmp/event-spec.json
```

Then follow the `hugo-event-intake` confirm-then-write workflow. Keep one
`/tmp/event-spec-<slug>.json` per candidate when processing several talks.

## Source Matching Rules

- Treat exact normalized URLs as duplicates.
- Also inspect Markdown body URLs because older event pages may include source links
  outside top-level frontmatter.
- Keep slide-deck sources such as Speaker Deck as `url_slides`.
- Pass organizer URLs such as connpass or official conference pages as additional
  `hugo-event-intake` inputs.
- Use RSS/Atom and source-specific public metadata first. Avoid scraping HTML
  unless a source adapter owns that parsing.
- Keep adapter-specific settings in each source's `options` object so future
  HTML/API adapters can own selectors, pagination, API parameters, or URL-role
  rules without changing the audit workflow.

## When To Stop

- Stop if Speaker Deck or the named feed is unavailable and the user did not provide
  another source list.
- Stop before writing if official organizer metadata conflicts with Speaker Deck
  title, date, or description.
- Stop before creating pages when the candidate is not clearly a public talk,
  presentation, poster, report, or journal club entry.
