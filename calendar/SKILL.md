---
name: calendar
description: Check, create, and manage Google Calendar events. Use when Junaid asks about his schedule, upcoming events, free slots, or wants to create/update/delete calendar events.
---

# Calendar

Manage Junaid's Google Calendar via `gog`.

## Prerequisites

Requires `gog` with calendar service authenticated. If not set up, point to the `gog` skill.

## Common Operations

### Check schedule

```bash
gog calendar events primary --from <start_iso> --to <end_iso>
```

- Default to today if no date specified
- For "this week", use Monday–Sunday range
- For "tomorrow", use next day's range

### Create event

```bash
gog calendar create primary --summary "Title" --from <iso> --to <iso>
```

- Always confirm with Junaid before creating
- Use `--event-color <id>` if he specifies a color

### Update event

```bash
gog calendar update primary <eventId> --summary "New Title"
```

### Free slot check

- Pull events for the requested range
- Identify gaps between events (respect working hours 10:00–22:00 IST unless told otherwise)

## Timezone

Always use `Asia/Kolkata` (IST, +05:30) for times unless Junaid specifies otherwise.

## Style

- When listing events, keep it scannable — time + title, one per line
- Flag conflicts or tight gaps proactively
- Don't dump raw JSON; format it human-readable
