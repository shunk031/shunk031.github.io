# Source Policy

Use this reference when `hugo-talks-sync` finds candidate talks.

## Authority Order

1. Existing `content/event` entries decide whether a source is already registered.
2. Official organizer pages decide event name, exact date/time, location, and session context.
3. Source feeds and source-specific metadata decide item title, source URL, cover image, and description.
4. Secondary sources may confirm facts, but should not be the only source for event metadata.

## Source Handling

- Prefer explicit source adapters over one-off scraping.
- Use `speakerdeck-profile` for Speaker Deck profiles, `feed` for auto-detected RSS/Atom sources, and explicit `rss` or `atom` adapters when the expected feed format is known.
- Treat feed `pubDate`, `published`, or `updated` as source publication dates until an organizer page confirms the actual event time.
- Treat URLs inside descriptions or summaries as discovery hints. Inspect them before writing.
- Add a new adapter when a source needs platform-specific semantics, such as user profile pagination, API authentication, HTML selectors, video metadata, or source-specific URL roles. Put adapter-specific settings in `options`.

## Candidate Classification

- Paper-reading titles or descriptions usually become `Journal Club`.
- Speaker Deck-only items that cite a paper URL such as arXiv or describe a
  survey/paper explanation usually become `Journal Club`, not `Report`.
- Invited event pages, seminars, and conference talks usually become `Invited Talk`.
- Conference recap decks usually become `Report`.
- Poster sessions or explicitly poster-like pages usually become `Invited Poster`.
- If classification is unclear, leave it for `hugo-event-intake` confirmation instead of guessing.
  An empty `likely_kind` in audit output is preferable to a false `Invited Talk`.
