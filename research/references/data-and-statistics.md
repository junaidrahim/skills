# Data and Statistical Discipline

## One canonical data store

Use `research.duckdb` as the only database file. Store canonical dataset snapshots and structured results there. Raw source files may exist in `ingest/` when a license, size, or acquisition process requires them. The DuckDB table and its metadata remain the experiment input.

For unstructured data, add a small Python ingestion script. Convert each document or unit into rows. Preserve the source ID, source URI, content hash, ingestion time, parser version, and raw text or a stable reference to it.

Register each dataset version with:

- Dataset ID and version.
- DuckDB schema and table name.
- Source and acquisition time.
- Content hash.
- Row count and unit of analysis.
- Parser or transformation version.
- Expected population.
- Distribution and quality notes.

Never replace a version used by a frozen experiment. Create the next version.

## Data audit before execution

Ask Junaid or inspect the evidence for:

- How the data was collected.
- The target population.
- Selection and survivorship bias.
- Missing values and duplicate units.
- Label source and label quality.
- Time range and freshness.
- Leakage between train, development, and test sets.
- Repeated entities across splits.
- Customer, domain, language, and geography mix.
- Out-of-distribution cases expected in deployment.
- Whether the sample is large enough for the claimed conclusion.

If the tested data does not represent the target setting, say so before the run. Ask whether to narrow the claim, get new data, stratify the analysis, or stop.

## Statistical plan

Decide whether the result is descriptive or inferential.

For every quantitative result, report:

- The sample unit and sample size.
- The baseline value.
- The observed value.
- The absolute and relative effect size.
- An uncertainty interval when possible.
- The random seed or resampling method.
- The number of comparisons or variants tried.
- Missing-data handling.

For hypothesis tests, define the test and threshold before running. Check its assumptions. Correct for multiple comparisons when several variants or metrics influence the conclusion. Do not use a p-value without an effect size and interval.

For model evaluation:

- Keep an untouched final holdout.
- Prevent prompt, example, and label leakage.
- Report results by important slices, not only as one average.
- Use paired comparisons when methods run on the same examples.
- Use bootstrap intervals when the metric has no simple parametric interval.
- Repeat stochastic runs with recorded seeds when run variance can change the decision.

## Practical significance

Statistical significance is not enough. Compare the result with the minimum useful effect from `project.toml`. A small effect can be real and still be operationally useless. A large observed effect with little data can remain uncertain.

Use `inconclusive` when the sample cannot support the intended claim. Do not hide this result. It is a valid research outcome.

## Reproducibility record

Each run must record:

- Experiment ID and frozen implementation hash.
- Dataset IDs, versions, and content hashes.
- Shared-library versions.
- Dependency lockfile hash.
- Model identifiers and provider settings.
- Seeds and sampling settings.
- Hardware details when they can affect the result.
- Start and finish times.
- Structured metrics and artifact hashes.

Do not put secrets in the project directory, DuckDB file, journal, or report. Record only the name of a required environment variable.
