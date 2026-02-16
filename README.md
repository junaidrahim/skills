# Skills

Personal OpenClaw skills for Junaid.

## Skills

| Skill | Purpose |
| --- | --- |
| `goodmorning` | Morning briefing — reviews tasks, asks about mood & priorities, creates daily note |
| `reflection` | Periodic reflection routines (weekly, monthly, yearly) |
| `undertones` | Writing emo, reflective essays for Undertones (Substack) |
| `blogs` | Technical blog writing for junaid.foo |
| `obsidian` | Obsidian vault conventions and note management |
| `letters` | Weekly letter-writing practice |
| `people` | Personal CRM and conversation tracker in Obsidian |
| `reading` | Quarterly reading list management and progress tracking |
| `learning` | Structured learning quests with syllabi, deadlines, and project outputs |

## Usage

Point OpenClaw to this directory in your config:

```yaml
skills:
  - /path/to/skills
```

## Creating a Skill

Each skill is a folder with at minimum a `SKILL.md`:

```
my-skill/
├── SKILL.md      # Instructions for the agent
├── scripts/      # Helper scripts (optional)
└── refs/         # Reference docs (optional)
```

See [OpenClaw docs](https://docs.openclaw.ai) for the full skill authoring guide.
