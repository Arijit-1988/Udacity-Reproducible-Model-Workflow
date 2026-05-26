import json
import sys
from pathlib import Path

import mlflow
import tempfile
import os
import wandb
from omegaconf import DictConfig, OmegaConf

_steps = [
    "download",
    "basic_cleaning",
    "data_check",
    "data_split",
    "train_random_forest",
    # NOTE: We do not include this in the steps so it is not run by mistake.
    # You first need to promote a model export to "prod" before you can run this,
    # then you need to run this step explicitly
#    "test_regression_model"
]


def _load_config_from_cli() -> DictConfig:
    config = OmegaConf.load("config.yaml")

    # Keep only dotlist-style overrides (e.g., main.steps='download').
    overrides = [arg for arg in sys.argv[1:] if "=" in arg and not arg.startswith("$(")]
    normalized_overrides: list[str] = []
    for arg in overrides:
        key, value = arg.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        normalized_overrides.append(f"{key}={value}")

    if overrides:
        config = OmegaConf.merge(config, OmegaConf.from_dotlist(normalized_overrides))

    return config


def _load_wandb_key_from_secret(project_root: Path) -> None:
    secret_path = project_root / ".secrets" / "wandb_api_key.env"
    if not secret_path.exists():
        return

    for line in secret_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("WANDB_API_KEY="):
            value = line.split("=", 1)[1].strip().strip("'\"")
            if value:
                os.environ["WANDB_API_KEY"] = value
            break


def go(config: DictConfig):

    project_root = Path(os.getcwd())
    _load_wandb_key_from_secret(project_root)

    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # Allow running without conda by setting MLFLOW_ENV_MANAGER=local
    env_manager = os.getenv("MLFLOW_ENV_MANAGER", "conda")
    if env_manager == "local":
        # Ensure nested MLflow project commands resolve to the same interpreter
        # that is executing this entrypoint (important on Windows).
        interpreter_dir = str(Path(sys.executable).parent)
        os.environ["MLFLOW_PYTHON_BIN"] = sys.executable
        os.environ["PATH"] = interpreter_dir + os.pathsep + os.environ.get("PATH", "")
    project_root = str(project_root)

    # Steps to execute
    steps_par = str(config['main']['steps']).strip().strip("'\"")
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    # Move to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:

        if "download" in active_steps:
            # Download file and load in W&B
            _ = mlflow.run(
                f"{config['main']['components_repository']}/get_data",
                "main",
                env_manager=env_manager,
                parameters={
                    "sample": config["etl"]["sample"],
                    "artifact_name": "sample.csv",
                    "artifact_type": "raw_data",
                    "artifact_description": "Raw file as downloaded"
                },
            )

        if "basic_cleaning" in active_steps:
            _ = mlflow.run(
                os.path.join(project_root, "src", "basic_cleaning"),
                "main",
                env_manager=env_manager,
                parameters={
                    "input_artifact": "sample.csv:latest",
                    "output_artifact": "clean_sample.csv",
                    "output_type": "clean_sample",
                    "output_description": "Data with outliers removed and parsed review dates",
                    "min_price": config["etl"]["min_price"],
                    "max_price": config["etl"]["max_price"],
                },
            )

        if "data_check" in active_steps:
            _ = mlflow.run(
                os.path.join(project_root, "src", "data_check"),
                "main",
                env_manager=env_manager,
                parameters={
                    "csv": "clean_sample.csv:latest",
                    "ref": "clean_sample.csv:reference",
                    "kl_threshold": config["data_check"]["kl_threshold"],
                    "min_price": config["etl"]["min_price"],
                    "max_price": config["etl"]["max_price"],
                },
            )

        if "data_split" in active_steps:
            _ = mlflow.run(
                f"{config['main']['components_repository']}/train_val_test_split",
                "main",
                env_manager=env_manager,
                parameters={
                    "input": "clean_sample.csv:latest",
                    "test_size": config["modeling"]["test_size"],
                    "random_seed": config["modeling"]["random_seed"],
                    "stratify_by": config["modeling"]["stratify_by"],
                },
            )

        if "train_random_forest" in active_steps:

            # NOTE: we need to serialize the random forest configuration into JSON
            rf_config = os.path.abspath("rf_config.json")
            with open(rf_config, "w+") as fp:
                json.dump(dict(config["modeling"]["random_forest"].items()), fp)  # DO NOT TOUCH

            # NOTE: use the rf_config we just created as the rf_config parameter for the train_random_forest
            # step

            _ = mlflow.run(
                os.path.join(project_root, "src", "train_random_forest"),
                "main",
                env_manager=env_manager,
                parameters={
                    "trainval_artifact": "trainval_data.csv:latest",
                    "val_size": config["modeling"]["val_size"],
                    "random_seed": config["modeling"]["random_seed"],
                    "stratify_by": config["modeling"]["stratify_by"],
                    "max_tfidf_features": config["modeling"]["max_tfidf_features"],
                    "rf_config": rf_config,
                    "output_artifact": "random_forest_export",
                },
            )

        if "test_regression_model" in active_steps:

            _ = mlflow.run(
                f"{config['main']['components_repository']}/test_regression_model",
                "main",
                env_manager=env_manager,
                parameters={
                    "mlflow_model": "random_forest_export:prod",
                    "test_dataset": "test_data.csv:latest",
                },
            )


if __name__ == "__main__":
    go(_load_config_from_cli())
