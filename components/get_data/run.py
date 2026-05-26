#!/usr/bin/env python
"""
This script download a URL to a local destination
"""
import argparse
import logging
import os
import sys
from pathlib import Path

import wandb

try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

# Local env_manager mode does not install `-e ..`, so add components root to path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wandb_utils.log_artifact import log_artifact

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="download_file")
    run.config.update(args)

    artifact_description = (
        " ".join(args.artifact_description)
        if isinstance(args.artifact_description, list)
        else args.artifact_description
    )

    logger.info(f"Returning sample {args.sample}")
    logger.info(f"Uploading {args.artifact_name} to Weights & Biases")
    log_artifact(
        args.artifact_name,
        args.artifact_type,
        artifact_description,
        os.path.join("data", args.sample),
        run,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download URL to a local destination")

    parser.add_argument("sample", type=str, help="Name of the sample to download")

    parser.add_argument("artifact_name", type=str, help="Name for the output artifact")

    parser.add_argument("artifact_type", type=str, help="Output artifact type.")

    parser.add_argument(
        "artifact_description", nargs="+", help="A brief description of this artifact"
    )

    args = parser.parse_args()

    go(args)
