#!/usr/bin/env python
"""Tag the best W&B model artifact as prod based on a metric (default: MAE)."""

from __future__ import annotations

import argparse
import math
import os
from typing import Iterable

import wandb


def _safe_metric(value: object) -> float | None:
    if value is None:
        return None
    try:
        as_float = float(value)
    except (TypeError, ValueError):
        return None

    if math.isnan(as_float) or math.isinf(as_float):
        return None
    return as_float


def _artifact_basename(artifact_name: str) -> str:
    """Convert entity/project/name:version -> name."""
    no_version = artifact_name.split(":", 1)[0]
    return no_version.rsplit("/", 1)[-1]


def _iter_model_artifacts(run: wandb.apis.public.Run, expected_name: str) -> Iterable[wandb.apis.public.Artifact]:
    for artifact in run.logged_artifacts():
        if artifact.type != "model_export":
            continue
        if _artifact_basename(artifact.name) != expected_name:
            continue
        yield artifact


def main() -> None:
    parser = argparse.ArgumentParser(description="Tag best model artifact as prod")
    parser.add_argument("--entity", default=os.getenv("WANDB_ENTITY"), help="W&B entity/user/team")
    parser.add_argument("--project", default="nyc_airbnb", help="W&B project name")
    parser.add_argument("--group", default="development", help="W&B run group to filter")
    parser.add_argument("--metric", default="mae", help="Run summary metric used for ranking")
    parser.add_argument("--maximize", action="store_true", help="Use max metric instead of min")
    parser.add_argument(
        "--artifact-name",
        default="random_forest_export",
        help="Artifact logical name to tag",
    )
    parser.add_argument("--alias", default="prod", help="Alias to add to the selected artifact")
    args = parser.parse_args()

    if not args.entity:
        raise SystemExit("Missing --entity (or set WANDB_ENTITY)")

    api = wandb.Api()
    path = f"{args.entity}/{args.project}"

    filters: dict[str, object] = {"jobType": "train_random_forest"}
    if args.group:
        filters["group"] = args.group

    runs = list(api.runs(path=path, filters=filters))
    if not runs:
        raise SystemExit("No train_random_forest runs found with the requested filters")

    best_candidate: tuple[float, wandb.apis.public.Run, wandb.apis.public.Artifact] | None = None

    for run in runs:
        metric_val = _safe_metric(run.summary.get(args.metric))
        if metric_val is None:
            continue

        for artifact in _iter_model_artifacts(run, args.artifact_name):
            if best_candidate is None:
                best_candidate = (metric_val, run, artifact)
                continue

            current_best, _, _ = best_candidate
            is_better = metric_val > current_best if args.maximize else metric_val < current_best
            if is_better:
                best_candidate = (metric_val, run, artifact)

    if best_candidate is None:
        raise SystemExit(
            f"No model_export artifact named '{args.artifact_name}' found on runs with metric '{args.metric}'"
        )

    score, run, artifact = best_candidate
    aliases = set(artifact.aliases)
    aliases.add(args.alias)
    artifact.aliases = sorted(aliases)
    artifact.save()

    print("Tagged artifact successfully")
    print(f"entity/project: {path}")
    print(f"run_id: {run.id}")
    print(f"metric ({args.metric}): {score}")
    print(f"artifact: {artifact.name}")
    print(f"aliases: {artifact.aliases}")


if __name__ == "__main__":
    main()
