"""Local command line interface for a portable research project."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .store import (
    connect,
    dataset_snapshot,
    file_sha256,
    find_project_root,
    finish_run,
    init_db,
    start_run,
    upsert_experiment,
    utc_now,
)


EXPERIMENT_PATTERN = re.compile(r"^(E\d{3})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
MUTABLE_OUTPUTS = {"analysis.md", "report.md", "FROZEN.json"}
MUTABLE_DIRECTORIES = {"artifacts", "__pycache__"}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("The experiment name must contain a letter or number.")
    return slug


def read_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def experiment_directories(root: Path) -> list[Path]:
    directory = root / "experiments"
    if not directory.exists():
        return []
    return sorted(path for path in directory.iterdir() if path.is_dir() and EXPERIMENT_PATTERN.match(path.name))


def resolve_experiment(root: Path, identifier: str) -> Path:
    normalized = identifier.upper()
    matches = [
        path
        for path in experiment_directories(root)
        if path.name.upper() == normalized or path.name.upper().startswith(f"{normalized}-")
    ]
    if not matches:
        raise ValueError(f"Experiment not found: {identifier}")
    if len(matches) > 1:
        raise ValueError(f"Experiment identifier is ambiguous: {identifier}")
    return matches[0]


def experiment_config(experiment: Path) -> dict[str, Any]:
    path = experiment / "experiment.toml"
    if not path.is_file():
        raise ValueError(f"Missing experiment.toml in {experiment.name}")
    return read_toml(path)


def implementation_hash(root: Path, experiment: Path) -> tuple[str, list[str]]:
    digest = hashlib.sha256()
    files: list[tuple[str, Path]] = []

    for path in experiment.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(experiment)
        if relative.name in MUTABLE_OUTPUTS or any(part in MUTABLE_DIRECTORIES for part in relative.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        files.append((f"experiment/{relative.as_posix()}", path))

    config = experiment_config(experiment)
    for shared_version in config.get("shared_versions", []):
        shared_path = (root / "shared" / shared_version).resolve()
        shared_root = (root / "shared").resolve()
        try:
            shared_path.relative_to(shared_root)
        except ValueError as error:
            raise ValueError(f"Shared version leaves the shared directory: {shared_version}") from error
        if not shared_path.is_dir():
            raise ValueError(f"Shared version does not exist: {shared_version}")
        for path in shared_path.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}:
                relative = path.relative_to(root)
                files.append((relative.as_posix(), path))

    if not files:
        raise ValueError(f"No implementation files found in {experiment.name}")

    names: list[str] = []
    for logical_name, path in sorted(files, key=lambda item: item[0]):
        names.append(logical_name)
        digest.update(logical_name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest(), names


def append_journal(root: Path, title: str, fields: list[tuple[str, str]]) -> None:
    path = root / "journal.md"
    with path.open("a", encoding="utf-8") as stream:
        stream.write(f"\n## {utc_now()} — {title}\n\n")
        for key, value in fields:
            stream.write(f"- {key}: {value}\n")


def next_experiment_id(root: Path) -> str:
    numbers = [int(path.name[1:4]) for path in experiment_directories(root)]
    number = max(numbers, default=0) + 1
    if number > 999:
        raise ValueError("Experiment sequence exceeds E999.")
    return f"E{number:03d}"


def cmd_init_db(_: argparse.Namespace) -> int:
    root = find_project_root()
    path = init_db(root)
    print(f"Initialized {path.relative_to(root)}")
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    root = find_project_root()
    experiment_id = next_experiment_id(root)
    name = args.name.strip()
    experiment = root / "experiments" / f"{experiment_id}-{slugify(name)}"
    experiment.mkdir(parents=True)
    (experiment / "artifacts").mkdir()

    created = utc_now()
    parent = args.parent.upper() if args.parent else ""
    if parent:
        resolve_experiment(root, parent)

    (experiment / "experiment.toml").write_text(
        "\n".join(
            [
                f'id = {json.dumps(experiment_id)}',
                f'name = {json.dumps(name)}',
                f'created = {json.dumps(created)}',
                f'parent_experiment = {json.dumps(parent)}',
                'primary_metric = ""',
                'minimum_useful_effect = ""',
                "datasets = []",
                "shared_versions = []",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (experiment / "hypothesis.md").write_text(
        f"# {experiment_id} Hypothesis\n\n[Describe the falsifiable hypothesis, population, baseline, outcome, and rejection condition.]\n",
        encoding="utf-8",
    )
    (experiment / "method.md").write_text(
        "# Method\n\n[Describe the data versions, intervention, controls, sample plan, seeds, and analysis plan.]\n",
        encoding="utf-8",
    )
    (experiment / "analysis.md").write_text(
        "# Analysis and Observations\n\nAppend observations after each run. Do not remove failed or contradictory results.\n",
        encoding="utf-8",
    )
    (experiment / "report.md").write_text(
        "# Report\n\n## Question\n\n## Decision\n\n## Method\n\n## Data\n\n## Result\n\n## Validity Limits\n\n## Reproduction\n",
        encoding="utf-8",
    )
    (experiment / "run.py").write_text(
        '''"""Implementation entrypoint for this frozen experiment."""\n\nfrom __future__ import annotations\n\n\ndef main() -> None:\n    raise SystemExit("IMPLEMENT_EXPERIMENT: replace this line before freeze")\n\n\nif __name__ == "__main__":\n    main()\n''',
        encoding="utf-8",
    )

    append_journal(
        root,
        f"{experiment_id} created",
        [
            ("Actor", "research CLI"),
            ("Goal", f"Frame {name}."),
            ("Evidence", f"Created {experiment.relative_to(root)}."),
            ("Decision", "Experiment remains a draft until it is frozen."),
            ("Next action", "Complete the hypothesis, method, data declarations, and implementation."),
        ],
    )
    print(f"Created {experiment.relative_to(root)}")
    return 0


def assert_ready_to_freeze(experiment: Path) -> None:
    hypothesis = (experiment / "hypothesis.md").read_text(encoding="utf-8")
    method = (experiment / "method.md").read_text(encoding="utf-8")
    run_code = (experiment / "run.py").read_text(encoding="utf-8")
    if "[Describe the falsifiable hypothesis" in hypothesis:
        raise ValueError("Complete hypothesis.md before freeze.")
    if "[Describe the data versions" in method:
        raise ValueError("Complete method.md before freeze.")
    if "IMPLEMENT_EXPERIMENT" in run_code:
        raise ValueError("Implement run.py before freeze.")


def cmd_freeze(args: argparse.Namespace) -> int:
    root = find_project_root()
    experiment = resolve_experiment(root, args.experiment)
    assert_ready_to_freeze(experiment)
    if not (root / "uv.lock").is_file():
        raise ValueError("Run 'uv lock' before freeze.")

    config = experiment_config(experiment)
    frozen_path = experiment / "FROZEN.json"
    if frozen_path.exists():
        existing = json.loads(frozen_path.read_text(encoding="utf-8"))
        digest, _ = implementation_hash(root, experiment)
        root_lock_hash = file_sha256(root / "uv.lock")
        if (
            existing.get("implementation_sha256") == digest
            and existing.get("lockfile_sha256") == root_lock_hash
        ):
            print(f"{experiment.name} is already frozen and unchanged.")
            return 0
        raise ValueError("The experiment has a freeze record with different inputs. Restore it or create a new experiment.")

    (experiment / "uv.lock").write_bytes((root / "uv.lock").read_bytes())
    specifications = list(config.get("datasets", []))
    datasets = dataset_snapshot(specifications, root)
    digest, files = implementation_hash(root, experiment)
    lock_hash = file_sha256(root / "uv.lock")

    frozen_at = utc_now()
    record = {
        "experiment_id": config.get("id", experiment.name[:4]),
        "frozen_at": frozen_at,
        "implementation_sha256": digest,
        "lockfile_sha256": lock_hash,
        "datasets": datasets,
        "shared_versions": list(config.get("shared_versions", [])),
        "files": files,
    }
    frozen_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    hypothesis = (experiment / "hypothesis.md").read_text(encoding="utf-8").strip()
    upsert_experiment(
        experiment_id=record["experiment_id"],
        name=str(config.get("name", experiment.name)),
        parent_experiment=str(config.get("parent_experiment", "")),
        hypothesis=hypothesis,
        status="frozen",
        implementation_sha256=digest,
        created_at=str(config.get("created", frozen_at)),
        frozen_at=frozen_at,
        root=root,
    )
    append_journal(
        root,
        f"{record['experiment_id']} frozen",
        [
            ("Actor", "research CLI"),
            ("Method", f"Implementation hash {digest}."),
            ("Data", ", ".join(specifications) if specifications else "No registered dataset declared."),
            ("Decision", "Inputs are immutable. Any change requires a new experiment."),
            ("Next action", f"Run uv run research run {record['experiment_id']}."),
        ],
    )
    print(f"Frozen {experiment.name} at {digest[:12]}")
    return 0


def read_autonomy(root: Path) -> dict[str, Any]:
    return dict(read_toml(root / "project.toml").get("autonomy", {}))


def enforce_autonomy(root: Path, experiment_id: str) -> dict[str, Any]:
    autonomy = read_autonomy(root)
    mode = str(autonomy.get("mode", "not-granted"))
    if mode in {"not-granted", "plan-only"}:
        raise ValueError("Experiment execution is not authorized in project.toml.")
    if mode == "run-approved":
        approved = {str(value).upper() for value in autonomy.get("approved_experiments", [])}
        if experiment_id.upper() not in approved:
            raise ValueError(f"{experiment_id} is not listed in autonomy.approved_experiments.")
    elif mode == "bounded-autoresearch":
        limit = int(autonomy.get("max_experiments", 0))
        if limit <= 0:
            raise ValueError("bounded-autoresearch requires a positive max_experiments value.")
        init_db(root)
        with connect(root) as con:
            prior = {row[0] for row in con.execute("SELECT DISTINCT experiment_id FROM research_meta.runs").fetchall()}
        if experiment_id not in prior and len(prior) >= limit:
            raise ValueError("The bounded-autoresearch experiment limit is exhausted.")
    else:
        raise ValueError(f"Unknown autonomy mode: {mode}")
    return autonomy


def cmd_run(args: argparse.Namespace) -> int:
    root = find_project_root()
    experiment = resolve_experiment(root, args.experiment)
    frozen_path = experiment / "FROZEN.json"
    if not frozen_path.is_file():
        raise ValueError("Freeze the experiment before execution.")

    record = json.loads(frozen_path.read_text(encoding="utf-8"))
    experiment_id = str(record["experiment_id"])
    autonomy = enforce_autonomy(root, experiment_id)
    current_datasets = dataset_snapshot(
        [f"{item['dataset_id']}@{item['version']}" for item in record.get("datasets", [])], root
    )
    if current_datasets != record.get("datasets", []):
        raise ValueError("A declared dataset version changed after freeze. Restore it or create a new version.")
    current_hash, _ = implementation_hash(root, experiment)
    if current_hash != record.get("implementation_sha256"):
        raise ValueError("Frozen experiment inputs changed. Restore them or create a new experiment.")
    current_lock_hash = file_sha256(root / "uv.lock")
    if current_lock_hash != record.get("lockfile_sha256"):
        raise ValueError("uv.lock changed after freeze. Create a new experiment for the new dependency set.")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{experiment_id}-{timestamp}-{current_hash[:8]}"
    seed = int(args.seed)
    start_run(
        run_id=run_id,
        experiment_id=experiment_id,
        implementation_sha256=current_hash,
        dataset_versions=list(record.get("datasets", [])),
        lockfile_sha256=current_lock_hash,
        seed=seed,
        root=root,
    )

    env = os.environ.copy()
    env.update(
        {
            "RESEARCH_PROJECT_ROOT": str(root),
            "RESEARCH_DUCKDB": str(root / "research.duckdb"),
            "RESEARCH_EXPERIMENT_ID": experiment_id,
            "RESEARCH_RUN_ID": run_id,
            "RESEARCH_SEED": str(seed),
            "RESEARCH_NETWORK_ALLOWED": str(bool(autonomy.get("network", False))).lower(),
            "RESEARCH_EXTERNAL_WRITES_ALLOWED": str(bool(autonomy.get("external_writes", False))).lower(),
            "RESEARCH_MAX_COST_USD": str(float(autonomy.get("max_cost_usd", 0.0))),
        }
    )
    timeout_hours = float(autonomy.get("max_wall_time_hours", 0.0))
    timeout_seconds = timeout_hours * 3600 if timeout_hours > 0 else None

    try:
        completed = subprocess.run(
            [sys.executable, str(experiment / "run.py")],
            cwd=experiment,
            env=env,
            check=False,
            timeout=timeout_seconds,
        )
        status = "completed" if completed.returncode == 0 else "failed"
        notes = f"Process exit code {completed.returncode}."
    except subprocess.TimeoutExpired:
        status = "failed"
        notes = f"Run exceeded the {timeout_hours:g}-hour wall-time limit."

    finish_run(run_id, status, notes, root)
    append_journal(
        root,
        f"{experiment_id} / {run_id}",
        [
            ("Actor", "research CLI"),
            ("Goal", f"Execute frozen experiment {experiment_id}."),
            ("Method", f"Implementation hash {current_hash}."),
            ("Data", json.dumps(record.get("datasets", []), sort_keys=True)),
            ("Result", f"Run status: {status}. {notes}"),
            ("Statistical limits", "Add the sample size, uncertainty, and distribution limits after analysis."),
            ("Decision", "Pending analysis."),
            ("Next action", f"Run uv run research show {experiment_id} and update analysis.md."),
        ],
    )
    print(f"{run_id}: {status}")
    return 0 if status == "completed" else 1


def freeze_state(root: Path, experiment: Path) -> str:
    path = experiment / "FROZEN.json"
    if not path.exists():
        return "draft"
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        digest, _ = implementation_hash(root, experiment)
        if digest != record.get("implementation_sha256"):
            return "tampered"
        if (root / "uv.lock").is_file() and file_sha256(root / "uv.lock") != record.get("lockfile_sha256"):
            return "lock-changed"
        return "frozen"
    except (OSError, ValueError, json.JSONDecodeError):
        return "invalid"


def cmd_list(_: argparse.Namespace) -> int:
    root = find_project_root()
    experiments = experiment_directories(root)
    if not experiments:
        print("No experiments.")
        return 0
    for experiment in experiments:
        config = experiment_config(experiment)
        print(f"{experiment.name[:4]}\t{freeze_state(root, experiment)}\t{config.get('name', experiment.name)}")
    return 0


def format_value(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def cmd_show(args: argparse.Namespace) -> int:
    root = find_project_root()
    init_db(root)
    experiment_id = args.experiment.upper() if args.experiment else ""
    if experiment_id:
        resolve_experiment(root, experiment_id)
    where = "WHERE experiment_id = ?" if experiment_id else ""
    parameters = [experiment_id] if experiment_id else []
    with connect(root) as con:
        runs = con.execute(
            f"""
            SELECT run_id, experiment_id, status, seed, started_at, finished_at, notes
            FROM research_meta.runs
            {where}
            ORDER BY started_at DESC
            LIMIT 20
            """,
            parameters,
        ).fetchall()
        metrics = con.execute(
            f"""
            SELECT run_id, experiment_id, metric_name, metric_value, unit, split,
                   lower_bound, upper_bound, sample_size
            FROM research_meta.metrics
            {where}
            ORDER BY recorded_at DESC
            LIMIT 100
            """,
            parameters,
        ).fetchall()

    print("Runs")
    if not runs:
        print("No runs recorded.")
    for row in runs:
        print("\t".join(format_value(value) for value in row))

    print("\nMetrics")
    if not metrics:
        print("No metrics recorded.")
    else:
        print("run_id\texperiment\tmetric\tvalue\tunit\tsplit\tlower\tupper\tn")
        for row in metrics:
            print("\t".join(format_value(value) for value in row))

    if experiment_id:
        report = root / "reports" / experiment_id / "index.html"
        if not report.is_file():
            report = resolve_experiment(root, experiment_id) / "report.md"
        print(f"\nReport: {report.relative_to(root)}")
    else:
        print("\nReports: reports/index.html")
    return 0


def cmd_datasets(_: argparse.Namespace) -> int:
    root = find_project_root()
    init_db(root)
    with connect(root) as con:
        rows = con.execute(
            """
            SELECT dataset_id, version, table_name, row_count, unit_of_analysis,
                   content_sha256, distribution_notes
            FROM research_meta.datasets
            ORDER BY dataset_id, version
            """
        ).fetchall()
    if not rows:
        print("No datasets registered.")
        return 0
    print("dataset\tversion\ttable\trows\tunit\tsha256\tdistribution_notes")
    for row in rows:
        print("\t".join(format_value(value) for value in row))
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    root = find_project_root()
    reports = root / "reports"
    handler = lambda *handler_args, **handler_kwargs: SimpleHTTPRequestHandler(
        *handler_args, directory=str(reports), **handler_kwargs
    )
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving {reports.relative_to(root)} at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


def cmd_validate(_: argparse.Namespace) -> int:
    root = find_project_root()
    errors: list[str] = []
    warnings: list[str] = []
    required_files = [
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        "project.toml",
        "pyproject.toml",
        "uv.lock",
        "research.duckdb",
        "journal.md",
    ]
    required_directories = ["experiments", "ingest", "shared/python", "shared/rust", "reports", "src/research_project"]

    for relative in required_files:
        if not (root / relative).is_file():
            errors.append(f"Missing file: {relative}")
    for relative in required_directories:
        if not (root / relative).is_dir():
            errors.append(f"Missing directory: {relative}")

    database_files = list(root.glob("*.duckdb"))
    if len(database_files) != 1 or (database_files and database_files[0].name != "research.duckdb"):
        errors.append("The project must contain exactly one root database named research.duckdb.")

    try:
        project = read_toml(root / "project.toml")
        goal = project.get("goal", {})
        for field in ("statement", "hypothesis", "baseline", "primary_metric", "stop_condition"):
            if not str(goal.get(field, "")).strip():
                warnings.append(f"Goal field is empty: {field}")
        if str(project.get("autonomy", {}).get("mode", "not-granted")) == "not-granted":
            warnings.append("Experiment execution is not authorized.")
    except (OSError, tomllib.TOMLDecodeError) as error:
        errors.append(f"Invalid project.toml: {error}")

    for experiment in experiment_directories(root):
        if not EXPERIMENT_PATTERN.match(experiment.name):
            errors.append(f"Invalid experiment name: {experiment.name}")
            continue
        for name in ("experiment.toml", "hypothesis.md", "method.md", "analysis.md", "report.md", "run.py"):
            if not (experiment / name).is_file():
                errors.append(f"{experiment.name} is missing {name}")
        frozen_path = experiment / "FROZEN.json"
        if frozen_path.exists():
            try:
                record = json.loads(frozen_path.read_text(encoding="utf-8"))
                digest, _ = implementation_hash(root, experiment)
                if digest != record.get("implementation_sha256"):
                    errors.append(f"Frozen inputs changed: {experiment.name}")
                if (root / "uv.lock").is_file() and file_sha256(root / "uv.lock") != record.get("lockfile_sha256"):
                    errors.append(f"Lockfile changed after freeze: {experiment.name}")
                current_datasets = dataset_snapshot(
                    [f"{item['dataset_id']}@{item['version']}" for item in record.get("datasets", [])], root
                )
                if current_datasets != record.get("datasets", []):
                    errors.append(f"Dataset metadata changed after freeze: {experiment.name}")
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
                errors.append(f"Invalid freeze record for {experiment.name}: {error}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Project is valid.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a portable applied-AI research project.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-db", help="Create the DuckDB metadata schema.")
    init_parser.set_defaults(function=cmd_init_db)

    new_parser = subparsers.add_parser("new", help="Create the next experiment.")
    new_parser.add_argument("name")
    new_parser.add_argument("--parent", default="")
    new_parser.set_defaults(function=cmd_new)

    freeze_parser = subparsers.add_parser("freeze", help="Freeze an experiment's inputs.")
    freeze_parser.add_argument("experiment")
    freeze_parser.set_defaults(function=cmd_freeze)

    run_parser = subparsers.add_parser("run", help="Run a frozen experiment.")
    run_parser.add_argument("experiment")
    run_parser.add_argument("--seed", type=int, default=0)
    run_parser.set_defaults(function=cmd_run)

    list_parser = subparsers.add_parser("list", help="List experiments.")
    list_parser.set_defaults(function=cmd_list)

    show_parser = subparsers.add_parser("show", help="Show local runs, metrics, and report paths.")
    show_parser.add_argument("experiment", nargs="?", default="")
    show_parser.set_defaults(function=cmd_show)

    datasets_parser = subparsers.add_parser("datasets", help="List registered dataset versions.")
    datasets_parser.set_defaults(function=cmd_datasets)

    serve_parser = subparsers.add_parser("serve", help="Serve static reports on localhost.")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.set_defaults(function=cmd_serve)

    validate_parser = subparsers.add_parser("validate", help="Validate project invariants.")
    validate_parser.set_defaults(function=cmd_validate)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        exit_code = args.function(args)
    except (OSError, RuntimeError, ValueError, tomllib.TOMLDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2) from error
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
