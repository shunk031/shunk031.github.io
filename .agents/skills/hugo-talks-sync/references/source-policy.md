# Source Policy

Use this reference when `hugo-talks-sync` finds candidate talks.

## Authority Order

1. Existing `content/event` entries decide whether a source is already registered.
2. Official organizer pages decide event name, exact date/time, location, and session context.
3. Speaker Deck feed and oEmbed decide slide title, slide URL, cover image, and description.
4. Secondary sources may confirm facts, but should not be the only source for event metadata.

## Speaker Deck Handling

- Prefer `<profile>.rss` or `<profile>.atom` for listing decks.
- Prefer Speaker Deck oEmbed for embed metadata after a candidate is selected.
- Treat `pubDate` as upload/publication date until an organizer page confirms the actual event time.
- Treat URLs inside the feed description as discovery hints. Inspect them before writing.

## Candidate Classification

- Paper-reading titles or descriptions usually become `Journal Club`.
- Invited event pages, seminars, and conference talks usually become `Invited Talk`.
- Conference recap decks usually become `Report`.
- Poster sessions or explicitly poster-like pages usually become `Invited Poster`.
- If classification is unclear, leave it for `hugo-event-intake` confirmation instead of guessing.
