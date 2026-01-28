# Skills

Custom Clawdbot skills for personal and work use.

## Structure

```
skills/
├── personal/     # Personal skills (home automation, side projects, etc.)
├── work/         # Work-related skills (Atlan-specific tooling, etc.)
└── shared/       # Skills usable in both contexts
```

## Usage

Point Clawdbot to this directory in your config:

```yaml
skills:
  - /path/to/skills/personal
  - /path/to/skills/work
  - /path/to/skills/shared
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
