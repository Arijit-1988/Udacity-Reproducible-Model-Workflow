# Submission Checklist (Udacity Rubric)

## Implemented in code

- [x] Added basic_cleaning step under src/basic_cleaning with:
  - [x] conda.yml
  - [x] MLproject
  - [x] run.py
- [x] Added cleaning logic:
  - [x] Price range filtering
  - [x] last_review datetime conversion
  - [x] NYC geoboundary filtering for release fix
- [x] Added basic_cleaning call to main pipeline (main.py)
- [x] Added data_check call to main pipeline (main.py)
- [x] Added data_split call to main pipeline (main.py)
- [x] Added train_random_forest call to main pipeline (main.py)
- [x] Added test_regression_model call to main pipeline (main.py)
- [x] Implemented test_row_count in src/data_check/test_data.py
- [x] Implemented test_price_range in src/data_check/test_data.py
- [x] Completed all TODO blocks in src/train_random_forest/run.py
- [x] Added EDA notebook at src/eda/EDA.ipynb with markdown and code cells
- [x] Added required submission-links section to README.md

## Manual steps you still need to do

- [ ] Fork this repository to your GitHub account
- [ ] Push your updated code to your fork
- [ ] Create/activate conda env from environment.yml (recommended in WSL for Windows)
- [ ] Run wandb login with your own API key in terminal
- [ ] Run pipeline steps and verify artifacts in W&B:
  - [ ] sample.csv
  - [ ] clean_sample.csv
  - [ ] trainval_data.csv and test_data.csv
  - [ ] random_forest_export model artifact
- [ ] In W&B, add alias reference to clean_sample.csv latest version
- [ ] In W&B, select best model and tag random_forest_export as prod
- [ ] Run test_regression_model step explicitly
- [ ] Update README placeholders with actual links:
  - [ ] public W&B project URL
  - [ ] GitHub repo URL
- [ ] Create GitHub release v1.0.0 (and v1.0.1+ if needed)
- [ ] Run released pipeline on sample2.csv; if failing, ensure NYC boundary fix is included and release new version
- [ ] Paste both links in Udacity Submission Details box

## Suggested commands

- Full pipeline:
  mlflow run .

- Single steps:
  mlflow run . -P steps=download
  mlflow run . -P steps=basic_cleaning,data_check,data_split,train_random_forest

- Hyperparameter sweep:
  mlflow run . -P steps=train_random_forest -P hydra_options="modeling.max_tfidf_features=10,15,30 modeling.random_forest.max_features=0.1,0.33,0.5,0.75,1 -m"

- Regression model test (after prod tag exists):
  mlflow run . -P steps=test_regression_model
