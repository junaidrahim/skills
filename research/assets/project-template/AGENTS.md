# Agent Instructions

This directory is one applied-AI research project. Keep it portable, reproducible, and easy for another agent to audit.

## Before work

1. Read `project.toml`.
2. Read the latest `journal.md` entries.
3. Run `uv run research validate`.
4. Run `uv run research list` and `uv run research show`.
5. Read the active experiment before you change anything.

## Invariants

- Use `uv` for Python dependencies and commands.
- Use `research.duckdb` as the only database file.
- Number experiments as `E001-<slug>`, `E002-<slug>`, and so on.
- Never edit a frozen experiment input. Create a new child experiment.
- Never edit a shared-library version used by a frozen experiment.
- Version every dataset. Record its hash and distribution notes.
- Append decisions, runs, observations, and conclusions to `journal.md`.
- Prefer Python. Ask Junaid before adding Rust, PyO3, or another language boundary.
- Check sample size, effect size, uncertainty, leakage, and distribution shift.
- Use ASD-STE100 Simplified Technical English in reports.
- Keep reports short and technical.
- Use local DuckDB results and static HTML. Do not require a hosted experiment tracker.

## Authority

The `[autonomy]` section in `project.toml` controls experiment execution. Do not run an experiment when the mode is `not-granted` or `plan-only`. Do not exceed its experiment, time, cost, network, or external-write limits.

## Result access

```bash
uv run research show <experiment-id>
uv run research serve
```

Update this file with project-specific context, commands, risks, and current state. Keep it canonical.
