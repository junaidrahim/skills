# __PROJECT_TITLE__

This directory contains one self-contained applied-AI research project.

## Start here

```bash
uv sync --locked
uv run research validate
uv run research list
uv run research show
```

Read `AGENTS.md`, `project.toml`, and the latest entries in `journal.md` before you change the project.

## Common commands

```bash
uv run research new "experiment name"
uv run research freeze E001
uv run research run E001
uv run research show E001
uv run research datasets
uv run research serve
```

`research.duckdb` is the only database file. Static reports live under `reports/` and work without a hosted experiment tracker.
