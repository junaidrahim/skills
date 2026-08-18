# Research Project Layout

Use this layout for every project:

```text
<project>/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── project.toml
├── pyproject.toml
├── uv.lock
├── research.duckdb
├── journal.md
├── experiments/
│   └── E001-short-name/
│       ├── experiment.toml
│       ├── hypothesis.md
│       ├── method.md
│       ├── analysis.md
│       ├── report.md
│       ├── run.py
│       ├── uv.lock
│       ├── FROZEN.json
│       └── artifacts/
├── ingest/
├── shared/
│   ├── python/
│   │   └── v001/
│   └── rust/
│       └── v001/
├── reports/
│   ├── index.html
│   └── assets/
└── src/
    └── research_project/
        ├── __init__.py
        ├── cli.py
        └── store.py
```

## Root files

### `project.toml`

This file is the current research contract. It records the goal, hypothesis, population, baseline, primary metric, stop condition, and autonomy boundary. Keep it short. Update it only when Junaid changes the project contract. Record the change in `journal.md`.

### `journal.md`

This is the append-only narrative ledger. Add an entry after a framing decision, dataset version, experiment freeze, run, analysis, conclusion, or change in direction. Each entry must include the time, actor, action, evidence, and next decision.

### `research.duckdb`

This is the only database file. It stores canonical dataset versions, experiment metadata, runs, metrics, and artifact records. Do not create one database per experiment.

### `AGENTS.md` and `CLAUDE.md`

`AGENTS.md` is canonical. It gives an arriving agent the goal, commands, invariants, autonomy limit, current experiment, and known risks. `CLAUDE.md` points to `AGENTS.md` so the rules do not drift.

### `pyproject.toml` and `uv.lock`

These files make the project runnable on another laptop. Add every Python dependency to `pyproject.toml`. Lock it with `uv lock`. Do not depend on an unrecorded global Python package.

## Experiment directories

Use a three-digit sequence: `E001`, `E002`, and so on. The suffix is a short kebab-case description.

An experiment starts as a draft. Edit its method and implementation until it is ready. Then run `uv run research freeze E001`. The command writes `FROZEN.json` with hashes for the implementation and declared dependencies.

After freeze:

- Do not edit the experiment input files.
- Do not edit a declared shared-library version.
- Do not replace a declared dataset version.
- You may append analysis and report material that describes the existing run.
- Create a new numbered experiment for any method or implementation change.

The freeze command also copies the active `uv.lock` into the experiment directory. This preserves the exact dependency resolution. The root lockfile must match that snapshot when the experiment runs. If dependencies change, create a child experiment. Restore the root lockfile from the frozen copy when you need to reproduce an older experiment.

## Shared libraries

Shared code also needs immutable versions. Use `shared/python/v001`, `shared/python/v002`, or the matching Rust path. An experiment declares the versions it uses in `experiment.toml`. Never edit a shared version used by a frozen experiment. Copy it to the next version and change it there.

Ask Junaid before adding Rust or PyO3. Use it only after a measured Python bottleneck.

## Local CLI contract

Every project exposes these commands through `uv run research`:

| Command | Purpose |
| --- | --- |
| `init-db` | Create the DuckDB metadata schema |
| `new <name>` | Create the next experiment directory |
| `freeze <id>` | Freeze inputs and record hashes |
| `run <id>` | Verify the frozen hash and run the experiment |
| `list` | List experiments and freeze state |
| `show [id]` | Show runs, metrics, uncertainty, sample size, and report path |
| `datasets` | List registered dataset versions |
| `serve` | Serve `reports/` on localhost |
| `validate` | Check the project and frozen hashes |

Do not require Weights & Biases or another hosted service. The DuckDB file and static reports are the portable result surface.

## Portability check

Before handoff, test the project from its root:

```bash
uv sync --locked
uv run research validate
uv run research list
uv run research show
```

The project fails the portability check if it needs an untracked environment variable, an unrecorded global package, an absolute path, a cloud login for local results, or a second database file.
