# Experiment Protocol

## Research contract

Before execution, get these decisions from Junaid:

- The research goal.
- A falsifiable hypothesis.
- The target population or operating setting.
- The baseline.
- One primary metric.
- The minimum useful effect.
- The success and stop conditions.
- The data sources and known limits.
- The allowed experiment count, time, cost, network access, and external writes.

If Junaid has not given an autonomy boundary, ask for it. Do not infer permission to run a long, costly, networked, or externally mutating experiment.

Use one of these modes in `project.toml`:

- `plan-only`: frame and design, but do not run.
- `run-approved`: run only the named experiment.
- `bounded-autoresearch`: design and run incremental experiments within the recorded limits.

## A good hypothesis

A useful hypothesis states:

- The intervention or method.
- The baseline or comparison.
- The measured outcome.
- The population or dataset.
- The expected direction.
- The condition that would weaken or reject it.

Do not use a question such as “Does this work?” as the full hypothesis.

## Design an experiment

Record these items before implementation:

1. Hypothesis and rationale.
2. Parent experiment, if any.
3. One deliberate change from the parent.
4. Dataset IDs and versions.
5. Baseline and controls.
6. Primary metric and minimum useful effect.
7. Secondary metrics.
8. Sample unit and sample-size plan.
9. Randomization and seeds.
10. Analysis plan and statistical test, if needed.
11. Known validity threats.
12. Expected artifacts and report.

Use Python by default. Put reusable code in a new immutable shared-library version. Ask before using Rust or PyO3.

## Freeze before execution

Run `uv run research freeze <id>` only when the method, configuration, code, dataset versions, and shared versions are ready. The freeze file records their hashes.

A frozen experiment may run more than once with recorded seeds or execution settings. It may not change its method. A failed implementation is still evidence. Create a child experiment for a fix.

Analysis notes and reports may grow after a run because they describe the frozen evidence. Do not edit them to hide a failed or contradictory result. Record corrections explicitly.

## Run and journal

Use `uv run research run <id>`. The CLI must verify the frozen hash before execution. It records a run ID, implementation hash, dataset-version snapshot, seed, start time, finish time, and status.

Append a journal entry after every run:

```markdown
## YYYY-MM-DDTHH:MM:SSZ — E001 / <run-id>

- Actor:
- Goal:
- Method:
- Data:
- Result:
- Statistical limits:
- Decision:
- Next action:
```

Write observations when they occur. Do not wait until the final report to reconstruct the reasoning.

## Bounded autoresearch

Use a slow hill-climb, not a blind parameter sweep.

1. Run the baseline first.
2. Change one important factor when practical.
3. Inspect the result and failure mode.
4. Form the next hypothesis from evidence.
5. Create a new numbered child experiment.
6. Stop at the first recorded stop condition.

Do not optimize against the final holdout set. Use a development set for iteration. Re-run the selected method once on the untouched holdout.

Stop when:

- The experiment, time, or cost budget is spent.
- The success condition is met.
- Improvement is below the minimum useful effect.
- Data quality makes the result invalid.
- Results remain statistically inconclusive and more data is not authorized.
- The next change requires new authority.
- Junaid asks to stop.

## Conclusions

Use these conclusion states:

- `supports`: the result supports the hypothesis within the tested setting.
- `weakens`: the result is inconsistent with the expected effect.
- `inconclusive`: the evidence cannot distinguish useful effect from noise or bias.
- `invalid`: a design, data, or execution fault prevents interpretation.

Do not write “proved.” State the tested scope and the main threat to validity.
