---
name: managing-obsidian-vault
description: Junaid's Obsidian vault conventions — tag-first organization, daily notes as life OS, journal structure. Use when working with the vault, creating notes, or managing tasks.
---

# Obsidian Vault

Junaid's knowledge management system.

## Location

- **Vault:** `/Users/junaidrahim/Obsidian/Everything`

## Core Principles

### Tags Over Folders

Use nested tags for hierarchy, not folder structures:
- `#category/subcategory`
- `#project/atlan`
- `#animals/dog`
- `#tbw` (to be written)

### Daily Notes = Life OS

The daily note is the central task/life management system:
- Heartbeat checks it hourly for pending tasks
- **Reminders for specific dates** → add to that day's daily note, not cron
- Everything that needs to happen on a day goes in that day's note

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `Notes/` | All notes (use tags for hierarchy) |
| `Journal/` | Daily, monthly, quarterly, yearly entries |
| `Templates/` | Note templates |
| `People/` | Personal CRM (see `people` skill) |

## File Naming

- **Daily notes:** `2026, January 27.md` (YYYY, Month DD)
- **Monthly notes:** `2026, January.md`
- **Project files:** tagged with `#project`

## Daily Note Template

Use template from `Templates/Daily Note.md`:

```markdown
#journal/daily

### Morning Pages
### Top 3 Priorities
### Other Notes
```

## When Adding Content

- Glitch's additions go in **"Notes from Glitch"** section in daily notes
- Use appropriate tags immediately
- Link to related notes with `[[Note Name]]`

## Related Skills

- `people` — Personal CRM in `People/` folder
- `starting-the-day` — Morning routine creates daily notes
- `reflecting-on-life` — Reflection outputs go to vault
