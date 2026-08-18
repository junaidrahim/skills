---
name: research
description: Manage reproducible applied-AI research projects from hypothesis through experiments, statistical analysis, and concise local reports. Use when Junaid wants to start, run, continue, audit, reproduce, or communicate an empirical research project. Do not use for a literature-only survey or a writing notebook with no experiments.
---

# Research

Manage the full lifecycle of an applied-AI research project. Keep each project in one portable directory. A new agent must be able to enter the directory, read the state, reproduce a result, and continue the work.

## Core invariants

1. One research project is one self-contained directory.
2. Every project contains `AGENTS.md`, `CLAUDE.md`, `project.toml`, `journal.md`, `pyproject.toml`, `uv.lock`, and one `research.duckdb` file.
3. Use `uv` for the Python environment and all project commands.
4. The project provides a local `research` CLI. It must list, create, freeze, run, show, validate, and serve experiments.
5. Number experiments as `E001-<slug>`, `E002-<slug>`, and so on.
6. An experiment becomes immutable when it is frozen. Never edit its hypothesis, method, configuration, code, dataset versions, or shared-library versions after that point.
7. A method change always creates a new experiment. Record the parent experiment and the reason for the change.
8. Version datasets. Store canonical experiment data and structured results in the single DuckDB file.
9. Append research progress to `journal.md`. Do not rewrite earlier entries.
10. Prefer Python. Use Rust only for measured data-processing bottlenecks. Ask Junaid before introducing Rust, PyO3, or another language boundary.
11. Keep reports short, technical, and auditable. Use ASD-STE100 Simplified Technical English.
12. Do not depend on a hosted experiment tracker. A person with the directory and `uv` must be able to inspect the results on a laptop.

## Read the relevant guidance

- Before creating or repairing a project, read [references/project-layout.md](references/project-layout.md).
- Before framing, changing, freezing, or running an experiment, read [references/experiment-protocol.md](references/experiment-protocol.md).
- Before ingesting data or drawing a quantitative conclusion, read [references/data-and-statistics.md](references/data-and-statistics.md).
- Before making charts or communicating results, read [references/reporting-and-visualization.md](references/reporting-and-visualization.md).

## Start a project

First, get a clear research contract from Junaid:

- The goal and falsifiable hypothesis.
- The target population or operating setting.
- The primary outcome and baseline.
- The success and stop conditions.
- The available data and known distribution risks.
- The autonomy mode and its limits.

Do not execute experiments until Junaid grants autonomy or explicitly asks for a specific run. A valid autonomy grant states the experiment count, time or cost boundary, allowed data, allowed network use, and stop conditions. Planning and local inspection do not need an execution grant.

Create a project with:

```bash
python3 <skill-directory>/scripts/init_project.py <project-directory> --title "<title>"
cd <project-directory>
uv lock
uv sync
uv run research init-db
uv run research validate
```

Ask before `uv lock` or `uv sync` when they require network access. Commit `uv.lock` when the project uses Git.

Fill in `project.toml` before the first experiment. Update both agent files with project-specific context. Keep `AGENTS.md` canonical. Keep `CLAUDE.md` as a short pointer to it unless another harness requires duplicated instructions.

## Continue a project

Read these files in order:

1. `AGENTS.md`
2. `project.toml`
3. `README.md`
4. The latest entries in `journal.md`
5. `uv run research list`
6. The relevant experiment's `experiment.toml`, `hypothesis.md`, `method.md`, `analysis.md`, and `report.md`
7. `uv run research show <experiment-id>`

Run `uv run research validate` before new work. If a frozen experiment fails validation, stop. Do not repair it in place. Restore the original files or create a child experiment.

## Run the research loop

1. Frame one falsifiable hypothesis.
2. Define the baseline, primary metric, population, and minimum useful effect.
3. Audit the data and distribution assumptions.
4. Create the next experiment with `uv run research new "<name>"`.
5. Fill in its hypothesis, method, data versions, code, and analysis plan.
6. Freeze it with `uv run research freeze <experiment-id>`.
7. Run it with `uv run research run <experiment-id>`.
8. Record observations and statistical limits immediately.
9. Show the result with `uv run research show <experiment-id>`.
10. Decide whether to stop, conclude, or create one new child experiment.

Change one important variable at a time when practical. Use the evidence from one run to select the next experiment. Do not hill-climb on the evaluation set. Do not continue after an autonomy limit or stop condition is reached.

## Local result access

The generated project must support:

```bash
uv run research list
uv run research show E001
uv run research serve
```

`show` prints run status, metrics, uncertainty fields, sample size, and the local report path. `serve` hosts the static `reports/` directory on `127.0.0.1`. Reports must use relative assets and must not require a cloud account.

## Completion

A research conclusion must state:

- What was tested.
- What data and versions were used.
- What changed from the baseline.
- The effect size and uncertainty.
- Whether the result supports, weakens, or does not resolve the hypothesis.
- The main validity threats.
- The next decision.

End with `uv run research validate`. Keep the DuckDB file, lockfile, frozen experiment material, journal, and static reports together.
