```
   _____ __ __ _ ____    __    _____
  / ___// //_/(_)/ / /   / /   / ___/
  \__ \/ ,<  / // / /   / /    \__ \ 
 ___/ / /| |/ // / /___/ /___ ___/ / 
/____/_/ |_/_//_/_____/_____//____/  
                                      
  ⚡ co-authored by junaid × glitch ⚡
```

# Skills

> *A human and an AI walk into a repo. They write the rules together so neither of them screws up.*

Personal [OpenClaw](https://github.com/openclaw/openclaw) skill modules — co-authored by **Junaid** and **Glitch** (Claude Opus 4). These aren't generic prompts. They're battle-tested workflows for how we actually get things done.

## The Stack

| Skill | What It Does |
| --- | --- |
| `goodmorning` | Morning briefing — reviews tasks, checks mood, boots up the day |
| `reflection` | Periodic sync routines (weekly / monthly / yearly) |
| `undertones` | Emo essays and literary prose for [Undertones](https://undertones.substack.com) |
| `blogs` | Technical posts for [junaid.foo](https://junaid.foo) |
| `obsidian` | Vault conventions, daily notes, tag-first organization |
| `letters` | Weekly letter-writing practice |
| `people` | Personal CRM — tracking conversations, debates, relationships |
| `reading` | Quarterly reading lists and progress tracking |
| `learning` | Structured deep-dive quests with syllabi and deadlines |
| `coding` | Branch-first PRs, conventional commits, research→plan→implement |

## Usage

Point OpenClaw to this directory:

```yaml
skills:
  - /path/to/skills
```

## Anatomy of a Skill

```
my-skill/
├── SKILL.md      # The instructions — this is what the agent reads
├── scripts/      # Helper scripts (optional)
└── refs/         # Reference docs (optional)
```

## Philosophy

These skills exist because context beats intelligence. A smart model with no instructions will guess. A smart model with *good* instructions will execute. We write these together — Junaid sets the intent, Glitch refines the structure — so future-Glitch wakes up knowing exactly what to do.

---

<sub>Built with [OpenClaw](https://docs.openclaw.ai) · Find more skills at [CławHub](https://clawhub.com)</sub>
