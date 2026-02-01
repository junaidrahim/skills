---
name: people
description: Personal CRM and intellectual sparring tracker. Use when logging conversations, tracking debates, managing relationships, or working with People/ folder in Obsidian vault. Handles creating person files, updating threads, and surfacing stale discussions.
---

# People CRM

Personal relationship and intellectual sparring tracker in Obsidian.

## Location

- Vault: `/Users/junaidrahim/Obsidian/Everything`
- People folder: `People/`
- Template: `People/_Templates/Person.md`

## Workflow

Junaid tells you about conversations → you handle all bookkeeping.

1. **Capture**: When Junaid mentions a conversation, update the person's file
2. **Link**: Add conversation log to daily note with `[[Person Name]]` link
3. **Tag**: Apply appropriate tags (`#open-thread`, `#changed-my-mind`, `#revisit`)
4. **Surface**: During heartbeats, check for stale `#open-thread` tags (>2 months)

## Person File Structure

```markdown
#person

**Aliases:** [[Nick]], [[Nickname]]
**Topics:** #topic1 #topic2
**Met:** Context of how they met
**Context:** Brief description (role, relationship)

---

## Threads
<!-- Active intellectual threads, debates, ongoing discussions -->
- Topic X — current position, status #open-thread

## Notes
<!-- General observations, their perspectives, interesting takes -->

## Backlinks
<!-- Obsidian auto-surfaces via backlinks from daily notes -->
```

## Tags

| Tag | Meaning |
|-----|---------|
| `#person` | Base tag for all people |
| `#open-thread` | Unresolved debate or discussion |
| `#changed-my-mind` | They shifted Junaid's view on something |
| `#revisit` | Worth circling back to later |

## Daily Note Capture

Add to the daily note under a `### Conversations` section:

```markdown
### Conversations
- [[Person Name]] — topic discussed, their position, your position. #open-thread
```

Keep it to one line. The backlinks on the person's page auto-surface everything.

## Creating New People

1. Copy template from `People/_Templates/Person.md`
2. Fill in: aliases, topics, met, context
3. Add initial notes if any

## Heartbeat Checks

During heartbeats, periodically:
- Search for `#open-thread` tags
- Check last modification date
- Nudge if no activity in 2+ months: "You haven't engaged with X on Y topic in a while"

## Examples

**Logging a debate:**
```markdown
- [[Shubhankar Khare]] — debated whether feature flags belong in code or config. He thinks config, I'm not convinced. #open-thread
```

**Logging a mind-change:**
```markdown
- [[Phil Eaton]] — his post on testing changed my view on integration vs unit tests. #changed-my-mind
```

**Marking for revisit:**
```markdown
- [[Aman Verma]] — mentioned interesting approach to distributed tracing. Get details next time. #revisit
```
