---
name: defuddle
description: Save web articles to Obsidian vault using defuddle. Use when Junaid shares a URL (blog post, Substack, article link) and wants it saved/added to his vault, or says "save this", "clip this", "add this to vault". Triggers on any shared link that looks like an article or blog post.
---

# Defuddle — Web Article Clipper

Save web articles as clean Markdown files into the Obsidian vault's Inbox folder.

## Workflow

1. Extract article content and metadata:

```bash
npx defuddle parse "<URL>" --json --markdown
```

2. Parse the JSON output to get: `title`, `author`, `published`, `description`, `domain`, `content` (markdown).

3. Create a note in the Obsidian vault at `/Users/junaidrahim/Everything/Inbox/<title>.md` with this format:

```markdown
---
source: <URL>
author: <author>
published: <published date>
domain: <domain>
clipped: <today's date YYYY-MM-DD>
---

<content>
```

4. Sanitize the title for use as filename — remove special characters like `/`, `\`, `:`, `|`, `?`, `*`, `"`, `<`, `>`.

5. Confirm to Junaid with the title and a short summary.

## Notes

- Always use `--json --markdown` flags to get structured output with markdown content.
- If defuddle fails or returns empty content, fall back to `web_fetch` and save the extracted markdown instead.
- Don't ask for confirmation before saving — just do it.
