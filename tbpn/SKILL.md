---
name: tbpn
description: >-
  Weekly newspaper-style summary of TBPN (Technology Business Programming Network) episodes.
  Use when the user asks for a TBPN summary, weekly tech news roundup, or says
  "tbpn summary", "tbpn newspaper", "what happened on tbpn this week",
  "pull the last N tbpn episodes". Also suitable for cron/scheduled end-of-week summaries.
license: MIT
compatibility: Requires yt-dlp and a PO Token server (bgutil-ytdlp-pot-provider) for YouTube transcript downloads. Works with any agent that can run shell commands and fetch URLs.
metadata:
  author: junaidrahim
  version: "1.0"
---

# TBPN Weekly Summary

Generate a newspaper-style summary of TBPN episodes and save it as Markdown.

## Configuration

Before first use, set these paths for your environment. Agents should check for a `tbpn.config.json` in this skill's directory. If it doesn't exist, use sensible defaults or ask the user.

```json
{
  "ytDlp": "yt-dlp",
  "potServerDir": "~/bgutil-ytdlp-pot-provider/server",
  "outputDir": "./output",
  "tempDir": "/tmp"
}
```

- **ytDlp** — path to the `yt-dlp` binary (default: `yt-dlp` on PATH)
- **potServerDir** — path to the bgutil PO Token server directory
- **outputDir** — where to save generated summaries (e.g. an Obsidian vault folder like `~/vault/TBPN/`)
- **tempDir** — where to store temporary transcript files

## Feeds

- **YouTube:** `https://www.youtube.com/feeds/videos.xml?channel_id=UC-DRzaGnL_vtBUpCFH5M0tg`
- **Newsletter (Substack):** `https://tbpn.substack.com/feed`

## Workflow

### 1. Fetch episodes

- Pull the YouTube RSS feed
- Filter for full episodes (skip Shorts — URLs containing `/shorts/`)
- By default, get episodes from the current week (Monday–Friday)
- The user may also request a specific number of recent episodes

### 2. Get transcripts

- Start the PO Token server: `cd <potServerDir> && node build/main.js &`
- For each episode, download the auto-generated transcript:
  ```
  <ytDlp> --write-auto-sub --skip-download --sub-lang en -o '<tempDir>/tbpn-%(id)s' 'VIDEO_URL'
  ```
- The bgutil plugin auto-provides tokens when the server is running on port 4416
- Clean transcripts: strip VTT headers, timestamps, positioning tags, and deduplicate consecutive identical lines
- Kill the PO Token server when done
- If transcripts aren't available, fall back to episode descriptions from the RSS feed

### 3. Generate the summary

Read all transcripts and produce a structured summary:

- **Headline** — the single biggest story
- **Top Stories** — 3-5 major topics, each with a 2-3 sentence summary
- **Interviews & Guests** — notable guests and key takeaways
- **Hot Takes** — spicy opinions from John or Jordi worth noting
- **Quick Hits** — bullet list of smaller stories mentioned
- **Links** — relevant links mentioned on the show

Tone: informative, slightly casual, like a tech-savvy friend summarising the week. Aim for 500-800 words total.

### 4. Save the summary

Save to `<outputDir>/YYYY-WNN.md` (e.g. `2026-W14.md`). Create the output directory if it doesn't exist.

Use the template in [references/TEMPLATE.md](references/TEMPLATE.md).

### 5. Generate PDF (optional)

If the user requests a PDF export, convert the Markdown summary to PDF with a design language inspired by *The Wall Street Journal*:

- **Fonts:** Use a serif font for body text (e.g. Georgia, Times New Roman) and a bold serif for headlines
- **Layout:** Single-column, clean and typographically dense
- **Margins:** 1 inch (72pt) on all sides — top, bottom, left, right. This is non-negotiable for readability
- **Headline:** Large, bold, uppercase or small-caps for the main headline
- **Section headers:** Bold, slightly larger than body, with a thin horizontal rule beneath
- **Body text:** 11pt, 1.4 line-height
- **Color:** Black and white only, no color accents
- **Footer:** "TBPN Weekly Summary — Week NN, YYYY" centered at the bottom of each page

Use Pandoc with a custom LaTeX template, or generate HTML styled with the above rules and convert to PDF via `wkhtmltopdf` or a headless browser. Ensure the `--margin-top`, `--margin-bottom`, `--margin-left`, and `--margin-right` flags are set to `25mm` (≈1 inch) if using wkhtmltopdf.

Save the PDF alongside the Markdown file as `<outputDir>/YYYY-WNN.pdf`.

### 6. Notify the user

After saving, let the user know: "TBPN weekly summary for Week NN is ready."

## Notes

- TBPN streams weekdays 11 AM–2 PM PT (John Coogan & Jordi Hays)
- Show was acquired by OpenAI in April 2026
- If no episodes aired in a given week, skip and note it
- The Substack feed can supplement YouTube when transcripts are unavailable
