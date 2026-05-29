# Resubmission Evidence (Final)

## Status Summary

- Hyperparameter search: complete (more than 2 training jobs with different hyperparameters)
- Best model selection + prod tag: complete
- Project releases: git tags `1.0.0` and `1.0.1` are pushed

## Links To Paste In Submission

- W&B project: https://wandb.ai/arijit-h-roy-accenture/nyc_airbnb
- Best training run (lowest MAE): https://wandb.ai/arijit-h-roy-accenture/nyc_airbnb/runs/4yaeskhi
- Production model artifact (`random_forest_export:prod`): https://wandb.ai/arijit-h-roy-accenture/nyc_airbnb/artifacts/model_export/random_forest_export/prod
- GitHub repository: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow
- GitHub tag 1.0.0: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.0
- GitHub tag 1.0.1: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.1

## Hyperparameter Search Evidence

Recent train jobs with different hyperparameters:

- https://wandb.ai/arijit-h-roy-accenture/nyc_airbnb/runs/wd0su1rx (n_estimators=120, MAE=34.11986329799576)
- https://wandb.ai/arijit-h-roy-accenture/nyc_airbnb/runs/4yaeskhi (n_estimators=220, MAE=34.089594285459306)
- https://wandb.ai/arijit-h-roy-accenture/nyc_airbnb/runs/g9jb5qgd (n_estimators=320, MAE=34.12159035267593)

Distinct `n_estimators` values observed in recent runs: 100, 120, 220, 320.

## Screenshots To Attach

1. W&B runs table showing multiple `train_random_forest` jobs with different hyperparameters.
2. Best run page showing MAE metric.
3. Artifact page showing `random_forest_export` with alias `prod`.
4. GitHub Releases page showing `1.0.0` and `1.0.1`.

## Quick Submission Text (Copy/Paste)

I completed a Hydra-based hyperparameter search and logged multiple `train_random_forest` runs in W&B with different configurations (for example `n_estimators`: 120, 220, 320). I selected the best model based on MAE and tagged the model artifact as `prod`.

W&B project: https://wandb.ai/arijit-h-roy-accenture/nyc_airbnb
Best run: https://wandb.ai/arijit-h-roy-accenture/nyc_airbnb/runs/4yaeskhi
Prod artifact: https://wandb.ai/arijit-h-roy-accenture/nyc_airbnb/artifacts/model_export/random_forest_export/prod

I also created and pushed two project releases/tags:
- 1.0.0: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.0
- 1.0.1: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.1

## Release Entries

Both release entries are published:

- https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.0
- https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.1
