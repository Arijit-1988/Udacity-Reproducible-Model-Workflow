# Resubmission Evidence (Final)

## Status Summary

- Hyperparameter search: complete (more than 2 training jobs with different hyperparameters)
- Best model selection + prod tag: complete
- Project releases: git tags `1.0.0` and `1.0.1` are pushed

## Links To Paste In Submission

- W&B project: https://wandb.ai/we4/nyc_airbnb
- Best training run (lowest MAE): https://wandb.ai/we4/nyc_airbnb/runs/x2whfj6w
- Production model artifact (`random_forest_export:prod`): https://wandb.ai/we4/nyc_airbnb/artifacts/model_export/random_forest_export/prod
- GitHub repository: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow
- GitHub tag 1.0.0: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.0
- GitHub tag 1.0.1: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.1

## Hyperparameter Search Evidence

Recent train jobs with different hyperparameters:

- https://wandb.ai/we4/nyc_airbnb/runs/uo0c59nn (n_estimators=220, MAE=34.089594285459306)
- https://wandb.ai/we4/nyc_airbnb/runs/362kb3qj (n_estimators=380, MAE=33.904899098366926)
- https://wandb.ai/we4/nyc_airbnb/runs/x2whfj6w (n_estimators=260, MAE=33.85856298530949)
- https://wandb.ai/we4/nyc_airbnb/runs/a1chvha0 (n_estimators=120, MAE=33.95185122529132)

Distinct `n_estimators` values observed in recent runs: 120, 220, 260, 380.

## Screenshots To Attach

1. W&B runs table showing multiple `train_random_forest` jobs with different hyperparameters.
2. Best run page showing MAE metric.
3. Artifact page showing `random_forest_export` with alias `prod`.
4. GitHub Releases page showing `1.0.0` and `1.0.1`.

## Quick Submission Text (Copy/Paste)

I completed a Hydra-based hyperparameter search and logged multiple `train_random_forest` runs in W&B with different configurations (for example `n_estimators`: 120, 220, 260, 380). I selected the best model based on MAE and tagged the model artifact as `prod`.

W&B project: https://wandb.ai/we4/nyc_airbnb
Best run: https://wandb.ai/we4/nyc_airbnb/runs/x2whfj6w
Prod artifact: https://wandb.ai/we4/nyc_airbnb/artifacts/model_export/random_forest_export/prod

I also created and pushed two project releases/tags:
- 1.0.0: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.0
- 1.0.1: https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/tag/1.0.1

## Important Note About GitHub Release Entries

In this environment, automated GitHub release creation is blocked by authentication (GitHub sign-in required in browser, and GitHub CLI is not installed). The tags are already pushed, so release entries can be created quickly from these pages after login:

- https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/new?tag=1.0.0
- https://github.com/Arijit-1988/Udacity-Reproducible-Model-Workflow/releases/new?tag=1.0.1
