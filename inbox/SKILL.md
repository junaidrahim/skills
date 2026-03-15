---
name: inbox
description: Check, search, and manage Gmail inbox. Use when Junaid asks about emails, unread messages, inbox summary, or wants to send/draft/reply to emails.
---

# Inbox

Manage Junaid's Gmail via `gog`.

## Prerequisites

Requires `gog` with gmail service authenticated. If not set up, point to the `gog` skill.

## Common Operations

### Check inbox

```bash
gog gmail search "in:inbox is:unread" --max 10
```

- Default to unread if Junaid just says "check my inbox"
- Use `newer_than:1d` for recent emails

### Search emails

```bash
gog gmail search "from:someone@example.com newer_than:7d" --max 10
```

### Read a specific email

```bash
gog gmail messages search "rfc822msgid:<msgId>" --max 1
```

### Send email

```bash
gog gmail send --to recipient@example.com --subject "Subject" --body-file - <<'EOF'
Message body here
EOF
```

- Always confirm with Junaid before sending
- Use `--body-file` for multi-line messages
- Use `--body-html` only when rich formatting is needed

### Draft email

```bash
gog gmail drafts create --to recipient@example.com --subject "Subject" --body-file - <<'EOF'
Draft body here
EOF
```

### Reply

```bash
gog gmail send --to recipient@example.com --subject "Re: Original" --body "Reply text" --reply-to-message-id <msgId>
```

## Style

- When summarizing inbox, show sender + subject + time, one per line
- Flag anything that looks urgent or time-sensitive
- Don't dump raw output; format human-readable
- For long emails, summarize key points unless Junaid asks for the full text
