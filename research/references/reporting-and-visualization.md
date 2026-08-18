# Reporting and Visualization

## Reporting goal

Make the result easy to understand, audit, and reproduce. A report is a decision surface, not a diary. Keep the reasoning history in `journal.md` and link to it when needed.

Use ASD-STE100 Simplified Technical English:

- Use short and direct sentences.
- Use active voice.
- Put one main idea in each sentence.
- Use one term for one concept.
- Define technical terms that affect the result.
- Remove filler, hype, and model-like summary language.

Keep the main report short. Put detailed tables, prompts, traces, and diagnostics in appendices or local artifacts.

## Report structure

Use this order:

1. **Question** — What did the experiment test?
2. **Decision** — What should happen next?
3. **Method** — What changed from the baseline?
4. **Data** — Which versions and population were used?
5. **Result** — What was the effect and uncertainty?
6. **Validity limits** — What can make the conclusion wrong?
7. **Reproduction** — Which command reproduces the run?
8. **Artifacts** — Where are the local tables, charts, and logs?

State whether the result supports, weakens, or does not resolve the hypothesis.

## Tufte-style visual rules

No separate Tufte skill is required. Apply these rules directly:

- Show the data. Do not decorate the chart.
- Use the simplest chart that answers the question.
- Remove 3D effects, heavy borders, gradients, and redundant legends.
- Label important values and series directly when possible.
- Use consistent scales across comparisons.
- Start a bar axis at zero. Explain any non-zero baseline for another chart.
- Show individual observations or distributions when the sample size permits it.
- Show uncertainty intervals and sample size.
- Use small multiples for repeated comparisons.
- Use color for meaning and emphasis. Do not use color only for decoration.
- Use a muted base palette and one emphasis color.
- Keep fonts, spacing, line weight, and number formats consistent.
- Put the data source, dataset version, metric definition, and run ID near the chart.

Do not make a chart when a sentence or a small table is clearer.

## Local-first result surface

Do not require Weights & Biases or another hosted account.

Preferred result order:

1. Store structured metrics in `research.duckdb`.
2. Make `uv run research show <id>` print the key result.
3. Write a static HTML report under `reports/<experiment-id>/index.html`.
4. Store local chart assets with relative paths.
5. Use `uv run research serve` to view all reports on a laptop.

Use Evidence.dev when it is already available and the project needs a richer local dashboard. Keep the `uv` CLI as the stable entry point. Do not add a Node runtime only for one simple chart.

Use Matplotlib for the default fallback. Save charts as SVG when possible and PNG when needed. Build a small static HTML page that includes the chart, result table, method, data version, uncertainty, and reproduction command.

## Chart conventions

Use a shared plotting module in a versioned directory. Set:

- One neutral background.
- One text color.
- One emphasis color.
- A color-blind-safe categorical palette.
- Consistent figure sizes and margins.
- Consistent decimal and percentage formats.
- Titles that state the finding, not only the metric name.

Do not edit a shared plotting version used by a frozen experiment. Create the next version.

## Audit check

Before handoff, verify:

- Every claim maps to a metric, table, or artifact.
- Every chart names the dataset version and run ID.
- The report shows sample size and uncertainty.
- The report distinguishes observation from inference.
- The reproduction command works from the project root.
- All links and assets work through `uv run research serve`.
- The report does not contain secrets or private source data that is not authorized for communication.
