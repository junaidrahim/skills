---
name: reading
description: Manage Junaid's quarterly reading lists. Track books, check progress, carry over unread titles, and nudge for reading time. Use when discussing books, updating reading progress, or planning what to read next.
---

# Reading Tracker

Quarterly reading lists in Obsidian.

## Location

- **Reading lists:** `Notes/Leisure Reading YYYY QN.md`
- **Current:** `Notes/Leisure Reading 2025 Q2.md`

## File Structure

```markdown
---
Status: In Progress
Quarter: "[[2025, Q2]]"
---

#project

Picking up a tentative list of books that are to be read in this quarter.

### Books

- [ ] Book Title
- [x] Completed Book

### List

(Optional links to reading challenges, recommendations)
```

## Workflow

### To Be Read List

Maintain a single note for book recommendations: `Notes/To Be Read.md`

When Junaid finds a book or asks to add one:
1. Add to `To Be Read.md` with source/context if available
2. Format: `- Book Title by Author — (source/who recommended)`

This is the backlog. Quarterly lists pull from here.

### Adding to Quarterly List

When starting a quarter or actively reading:
1. Pick from `To Be Read.md`
2. Add to current quarter's list as `- [ ] Book Title by Author`

### Tracking Progress

- Mark completed: `- [ ]` → `- [x]`
- Books carry over if not finished by quarter end

### Quarter Rollover

At start of new quarter:
1. Create new file: `Leisure Reading YYYY QN.md`
2. Copy unread books from previous quarter
3. Add new books for the quarter
4. Set Status: In Progress

### Book Reflections (Voice Dumps)

After finishing a book, Junaid does a **voice dump** of his thoughts.

Workflow:
1. Junaid sends voice note with reflections
2. Transcribe the audio
3. Summarize into a structured note
4. Save to `Notes/Book Title.md` (use tags, not folders)

Reflection note format:
```markdown
#book

**Book:** Title by Author
**Finished:** YYYY-MM-DD

## Summary
(Brief plot/premise)

## Thoughts
(Junaid's reflections, summarized from voice dump)

## Quotes / Highlights
(If mentioned)

## Rating
(If given)
```

Keep the voice of the reflection — don't over-sanitize.

## Heartbeat Integration

Periodically (weekly or bi-weekly):
- "How's the reading going? Any progress on your list?"
- Surface current list if asked

## When Helping

- Suggest books based on his interests (literary fiction, essays, Indian authors)
- Track recommendations from conversations
- Don't nag — reading should be enjoyable, not a chore
- Help find specific books (availability, editions)

## Patterns from Past Lists

Genres he enjoys:
- Literary fiction
- Indian authors (Benyamin, Vikrant Khanna, Kavitha Rao)
- Essays and non-fiction
- Contemporary fiction (Han Kang, Sylvia Plath)

Challenges he follows:
- Champaca Reading Challenge
