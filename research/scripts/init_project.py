#!/usr/bin/env python3
"""Create one self-contained applied-AI research project."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path


TEXT_SUFFIXES = {"", ".md", ".toml", ".html", ".py", ".txt", ".gitignore"}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("The project title must contain a letter or number.")
    return slug


def replace_tokens(root: Path, replacements: dict[str, str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        content = path.read_text(encoding="utf-8")
        for token, value in replacements.items():
            content = content.replace(token, value)
        path.write_text(content, encoding="utf-8")


def run_command(command: list[str], cwd: Path) -> None:
    print(f"Running: {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def init_project(target: Path, title: str, slug: str, sync: bool) -> None:
    skill_root = Path(__file__).resolve().parents[1]
    template = skill_root / "assets" / "project-template"
    if not template.is_dir():
        raise RuntimeError(f"Project template not found: {template}")

    if target.exists() and any(target.iterdir()):
        raise RuntimeError(f"Target directory is not empty: {target}")
    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, target, dirs_exist_ok=True)

    for relative in (
        "experiments",
        "reports/assets",
        "shared/python",
        "shared/rust",
    ):
        (target / relative).mkdir(parents=True, exist_ok=True)

    replace_tokens(
        target,
        {
            "__PROJECT_TITLE__": title,
            "__PROJECT_SLUG__": slug,
            "__CREATED_DATE__": date.today().isoformat(),
        },
    )

    if sync:
        uv = shutil.which("uv")
        if not uv:
            raise RuntimeError("uv is required for --sync.")
        run_command([uv, "lock"], target)
        run_command([uv, "sync", "--locked"], target)
        run_command([uv, "run", "research", "init-db"], target)
        run_command([uv, "run", "research", "validate"], target)

    print(f"Created research project: {target}")
    if not sync:
        print("Next commands:")
        print(f"  cd {target}")
        print("  uv lock")
        print("  uv sync --locked")
        print("  uv run research init-db")
        print("  uv run research validate")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a portable applied-AI research project.")
    parser.add_argument("target", type=Path)
    parser.add_argument("--title", default="")
    parser.add_argument("--slug", default="")
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Resolve the uv lockfile, install dependencies, initialize DuckDB, and validate.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    target = args.target.expanduser().resolve()
    title = args.title.strip() or target.name.replace("-", " ").title()
    slug = slugify(args.slug.strip() or title)
    try:
        init_project(target, title, slug, args.sync)
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
