# Event Patterns

Use these defaults unless the user explicitly asks for another style.

## Kind And Tags

- `Invited Talk`
- Title: `[Invited Talk] <core title>`
- Tags: `["Invited Talk"]`

- `Journal Club`
- Title: `[Journal Club] <core title>`
- Tags: `["Journal Club", "Paper Reading"]`

- `Invited Presentation`
- Title: `[Invited Presentation] <core title>`
- Tags: `["Invited Talk", "Invited Presentation"]`

- `Invited Poster`
- Title: `[Invited Poster] <core title>`
- Tags: `["Presentation"]`

- `Report`
- Title: `<core title>`
- Tags: `[]`

## Body Defaults

- If a Speaker Deck embed is available:
- Start with `# <event>` when `event` is known
- Add a short quoted description when available
- Add `## 資料 - Slides`
- Add the `<script ... class="speakerdeck-embed" ...>` block

- If there is no Speaker Deck embed:
- Start with `# <event>` when `event` is known
- Add a short quoted description when available
- Add `## Links`
- List available `event_url`, `url_slides`, `url_pdf`, `url_video`, `url_code`, and explicit `links`

## Search Priorities

- Prefer official organizer or conference pages
- Then prefer official schedules or CFP/program pages
- Then use deck pages, PDFs, and videos
- Use secondary summaries only to confirm, not as the sole source of record
