---
name: good-morning
description: Morning routine that reviews incomplete tasks from previous days, asks about mood and priorities, and creates the day's note. Triggers on "good morning" or morning greetings.
---

# Good Morning Routine

When Junaid says good morning or gm, run this workflow.

## Workflow

1. **Find last daily note**
   - Check `Journal/YYYY, Month DD.md` for yesterday
   - If not found, go back day by day until you find one

2. **Extract incomplete tasks**
   - Find all unchecked items (`- [ ]`)
   - These carry forward to today

3. **Ask morning questions**
   - How are you feeling this morning?
   - What are your top 3 priorities for today?
   - Anything specific you want to focus on or avoid?

4. **Create today's note**
   - Use template from `Templates/Daily Note.md`
   - Fill in:
     - Carried-over tasks (under appropriate section)
     - Morning mood/feeling (in Morning Pages)
     - Top 3 priorities
   - Save to `Journal/YYYY, Month DD.md`

## Paths

- Vault: `/Users/junaidrahim/Everything`
- Journal: `Journal/`
- Template: `Templates/Daily Note.md`

## Date Format

Daily notes use: `2026, January 27.md` (YYYY, Month DD)

## Heartbeat Setup

After creating the daily note, update `HEARTBEAT.md` to include hourly check-ins:

- Check progress on today's tasks
- Quick vibe check — how's energy, focus, stress?
- Offer to take things off his plate if overwhelmed
- Keep it brief, not intrusive

This catches things before they pile up.

## Style

Keep the interaction conversational, not robotic.
