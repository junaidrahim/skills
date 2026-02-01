# Skills

Personal Clawdbot skills for Junaid.

## Skills

| Skill         | Purpose                           |
| ------------- | --------------------------------- |
| `goodmorning` | Morning briefing routine          |
| `reflection`  | Periodic reflection routines      |
| `undertones`  | Writing for Undertones (Substack) |
| `blogs`       | Technical blog writing            |
| `obsidian`    | Obsidian vault management         |
| `letters`     | Drafting letters for people       |
| `people`      | CRM management in Obsidian        |

## Usage

Point Clawdbot to this directory in your config:

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

See [Clawdbot docs](https://docs.clawd.bot) for full skill authoring guide.
