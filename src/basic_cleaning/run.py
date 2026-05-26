#!/usr/bin/env python
"""Basic cleaning step for Airbnb sample data."""
import argparse
import logging

import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args: argparse.Namespace) -> None:
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(vars(args))

    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    idx = df["price"].between(args.min_price, args.max_price)
    df = df[idx].copy()

    df["last_review"] = pd.to_datetime(df["last_review"])

    # Remove listings outside NYC bounds to prevent boundary test failures on new samples.
    idx = df["longitude"].between(-74.25, -73.50) & df["latitude"].between(40.5, 41.2)
    df = df[idx].copy()

    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Input raw CSV artifact",
        required=True,
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for the output cleaned artifact",
        required=True,
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Type for the output artifact",
        required=True,
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description for the output artifact",
        required=True,
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum accepted listing price",
        required=True,
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum accepted listing price",
        required=True,
    )

    go(parser.parse_args())
