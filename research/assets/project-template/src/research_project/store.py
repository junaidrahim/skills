"""DuckDB storage helpers for one portable research project."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def find_project_root(start: Path | None = None) -> Path:
    env_root = os.environ.get("RESEARCH_PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "project.toml").is_file() and (candidate / "pyproject.toml").is_file():
            return candidate
    raise RuntimeError("Run this command inside a research project directory.")


def database_path(root: Path | None = None) -> Path:
    env_path = os.environ.get("RESEARCH_DUCKDB")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return find_project_root(root) / "research.duckdb"


def connect(root: Path | None = None) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(database_path(root)))


def init_db(root: Path | None = None) -> Path:
    path = database_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(path)) as con:
        con.execute("CREATE SCHEMA IF NOT EXISTS research_meta")
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS research_meta.datasets (
                dataset_id VARCHAR NOT NULL,
                version VARCHAR NOT NULL,
                table_name VARCHAR NOT NULL,
                source_uri VARCHAR,
                content_sha256 VARCHAR NOT NULL,
                row_count BIGINT,
                unit_of_analysis VARCHAR,
                schema_json VARCHAR,
                distribution_notes VARCHAR,
                parser_version VARCHAR,
                ingested_at TIMESTAMP NOT NULL,
                PRIMARY KEY (dataset_id, version)
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS research_meta.experiments (
                experiment_id VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                parent_experiment VARCHAR,
                hypothesis VARCHAR,
                status VARCHAR NOT NULL,
                implementation_sha256 VARCHAR,
                created_at TIMESTAMP NOT NULL,
                frozen_at TIMESTAMP
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS research_meta.runs (
                run_id VARCHAR PRIMARY KEY,
                experiment_id VARCHAR NOT NULL,
                implementation_sha256 VARCHAR NOT NULL,
                dataset_snapshot_json VARCHAR NOT NULL,
                lockfile_sha256 VARCHAR,
                seed BIGINT,
                started_at TIMESTAMP NOT NULL,
                finished_at TIMESTAMP,
                status VARCHAR NOT NULL,
                notes VARCHAR
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS research_meta.metrics (
                run_id VARCHAR NOT NULL,
                experiment_id VARCHAR NOT NULL,
                metric_name VARCHAR NOT NULL,
                metric_value DOUBLE NOT NULL,
                unit VARCHAR,
                split VARCHAR,
                lower_bound DOUBLE,
                upper_bound DOUBLE,
                sample_size BIGINT,
                recorded_at TIMESTAMP NOT NULL
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS research_meta.artifacts (
                run_id VARCHAR NOT NULL,
                experiment_id VARCHAR NOT NULL,
                artifact_type VARCHAR NOT NULL,
                relative_path VARCHAR NOT NULL,
                content_sha256 VARCHAR,
                description VARCHAR,
                recorded_at TIMESTAMP NOT NULL
            )
            """
        )
    return path


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def register_dataset(
    *,
    dataset_id: str,
    version: str,
    table_name: str,
    content_sha256: str,
    source_uri: str = "",
    row_count: int | None = None,
    unit_of_analysis: str = "",
    schema: dict[str, Any] | None = None,
    distribution_notes: str = "",
    parser_version: str = "",
    root: Path | None = None,
) -> None:
    init_db(root)
    schema_json = json.dumps(schema or {}, sort_keys=True)
    incoming = (
        table_name,
        source_uri,
        content_sha256,
        row_count,
        unit_of_analysis,
        schema_json,
        distribution_notes,
        parser_version,
    )
    with connect(root) as con:
        if "." in table_name:
            table_schema, local_table_name = table_name.split(".", 1)
        else:
            table_schema, local_table_name = "main", table_name
        table_exists = con.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = ? AND table_name = ?
            """,
            [table_schema, local_table_name],
        ).fetchone()[0]
        if table_exists == 0:
            raise ValueError(f"Dataset table does not exist: {table_name}")
        existing = con.execute(
            """
            SELECT table_name, source_uri, content_sha256, row_count, unit_of_analysis,
                   schema_json, distribution_notes, parser_version
            FROM research_meta.datasets
            WHERE dataset_id = ? AND version = ?
            """,
            [dataset_id, version],
        ).fetchone()
        if existing is not None:
            if tuple(existing) == incoming:
                return
            raise ValueError(
                f"Dataset version already exists with different metadata: {dataset_id}@{version}. "
                "Create a new version."
            )
        con.execute(
            """
            INSERT INTO research_meta.datasets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                dataset_id,
                version,
                table_name,
                source_uri,
                content_sha256,
                row_count,
                unit_of_analysis,
                schema_json,
                distribution_notes,
                parser_version,
                utc_now(),
            ],
        )


def dataset_snapshot(specifications: list[str], root: Path | None = None) -> list[dict[str, Any]]:
    if not specifications:
        return []

    init_db(root)
    snapshot: list[dict[str, Any]] = []
    with connect(root) as con:
        for specification in specifications:
            if "@" not in specification:
                raise ValueError(f"Dataset '{specification}' must use dataset-id@version.")
            dataset_id, version = specification.rsplit("@", 1)
            row = con.execute(
                """
                SELECT dataset_id, version, table_name, content_sha256, row_count, unit_of_analysis
                FROM research_meta.datasets
                WHERE dataset_id = ? AND version = ?
                """,
                [dataset_id, version],
            ).fetchone()
            if row is None:
                raise ValueError(f"Dataset version is not registered: {specification}")
            snapshot.append(
                {
                    "dataset_id": row[0],
                    "version": row[1],
                    "table_name": row[2],
                    "content_sha256": row[3],
                    "row_count": row[4],
                    "unit_of_analysis": row[5],
                }
            )
    return snapshot


def upsert_experiment(
    *,
    experiment_id: str,
    name: str,
    parent_experiment: str,
    hypothesis: str,
    status: str,
    implementation_sha256: str,
    created_at: str,
    frozen_at: str | None,
    root: Path | None = None,
) -> None:
    init_db(root)
    with connect(root) as con:
        con.execute(
            """
            INSERT OR REPLACE INTO research_meta.experiments VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                experiment_id,
                name,
                parent_experiment,
                hypothesis,
                status,
                implementation_sha256,
                created_at,
                frozen_at,
            ],
        )


def start_run(
    *,
    run_id: str,
    experiment_id: str,
    implementation_sha256: str,
    dataset_versions: list[dict[str, Any]],
    lockfile_sha256: str,
    seed: int,
    root: Path | None = None,
) -> None:
    init_db(root)
    with connect(root) as con:
        con.execute(
            """
            INSERT INTO research_meta.runs VALUES (?, ?, ?, ?, ?, ?, ?, NULL, 'running', NULL)
            """,
            [
                run_id,
                experiment_id,
                implementation_sha256,
                json.dumps(dataset_versions, sort_keys=True),
                lockfile_sha256,
                seed,
                utc_now(),
            ],
        )


def finish_run(run_id: str, status: str, notes: str = "", root: Path | None = None) -> None:
    with connect(root) as con:
        con.execute(
            """
            UPDATE research_meta.runs
            SET finished_at = ?, status = ?, notes = ?
            WHERE run_id = ?
            """,
            [utc_now(), status, notes, run_id],
        )


def record_metric(
    metric_name: str,
    metric_value: float,
    *,
    unit: str = "",
    split: str = "",
    lower_bound: float | None = None,
    upper_bound: float | None = None,
    sample_size: int | None = None,
    run_id: str | None = None,
    experiment_id: str | None = None,
    root: Path | None = None,
) -> None:
    run_id = run_id or os.environ.get("RESEARCH_RUN_ID")
    experiment_id = experiment_id or os.environ.get("RESEARCH_EXPERIMENT_ID")
    if not run_id or not experiment_id:
        raise ValueError("A run ID and experiment ID are required.")
    with connect(root) as con:
        con.execute(
            """
            INSERT INTO research_meta.metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                run_id,
                experiment_id,
                metric_name,
                float(metric_value),
                unit,
                split,
                lower_bound,
                upper_bound,
                sample_size,
                utc_now(),
            ],
        )


def record_artifact(
    path: Path,
    artifact_type: str,
    description: str = "",
    *,
    run_id: str | None = None,
    experiment_id: str | None = None,
    root: Path | None = None,
) -> None:
    project_root = find_project_root(root)
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(project_root)
    except ValueError as error:
        raise ValueError("Artifacts must stay inside the research project directory.") from error
    run_id = run_id or os.environ.get("RESEARCH_RUN_ID")
    experiment_id = experiment_id or os.environ.get("RESEARCH_EXPERIMENT_ID")
    if not run_id or not experiment_id:
        raise ValueError("A run ID and experiment ID are required.")
    sha256 = file_sha256(resolved) if resolved.is_file() else ""
    with connect(project_root) as con:
        con.execute(
            """
            INSERT INTO research_meta.artifacts VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [run_id, experiment_id, artifact_type, str(relative), sha256, description, utc_now()],
        )
