# Machine Learning Template

This project provides a machine learning quickstart template using PyTorch Lightning, Hydra, MLflow, and uv.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd machine-learning
    ```
2.  **Install uv:**
    Follow the instructions on the [uv website](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it installed.
3.  **Install dependencies:**
    This command creates a virtual environment and installs all necessary packages defined in [`pyproject.toml`](pyproject.toml).
    ```bash
    uv sync
    ```
    or if you need to submit a job to a cluster, use:
    ```bash
    uv sync --extra job
    ```

## Configuration

This project uses [Hydra](https://hydra.cc/) for configuration management.

-   Configuration files are located in the [`configs/`](configs) directory.
-   The configuration file [`configs/base.yaml`](configs/base.yaml) is the default project configuration which all other configurations inherit from.
-   You can override configuration parameters directly from the command line. For example, to change the batch size:
    ```bash
    uv run python -m <project_name> mode=fit data.batch_size=64
    ```
    Such approach is recomended throughtout development process, however, when submitting final changes to master branch it's recommended to create separate experiment configuration files in the `experiment` subdirectory for better organization and reproducibility.
-   The structure of the configs directory should follow the example below.
    ```plaintext
    configs
    ├── data                        # Data-related configurations
    ├── experiment                  # Experiment-specific configurations
    │   └── <some_experiment>
    ├── hydra
    │   ├── default.yaml
    │   └── job_logging
    │       └── custom.yaml
    ├── logger
    │   └── mlflow.yaml
    ├── preprocessing
    │   ├── qc.yaml
    │   ├── tiling.yaml
    │   └── tissue_masks.yaml
    ├── base.yaml
    ├── preprocessing.yaml
    ├── ml.yaml
    └── ml
        └── <some_configurations>   # Place your training configurations here
    ```
-   Please do not delete the `configs/hydra` directory as it is required for Hydra execution.
-   MLflow is configured as the default logger (see [`configs/default.yaml`](configs/default.yaml)).

## Usage

-   **Train the model:**
    ```bash
    uv run python -m <project_name> mode=fit
    ```

-   **Validate the model:**
    Requires a checkpoint path to be set in the configuration (e.g., `checkpoint=path/to/your/checkpoint.ckpt`) or passed via the command line.
    ```bash
    uv run python -m <project_name> mode=validate checkpoint=path/to/checkpoint.ckpt
    ```

-   **Test the model:**
    Requires a checkpoint path.
    ```bash
    uv run python -m <project_name> mode=test checkpoint=path/to/checkpoint.ckpt
    ```

-   **Run prediction:**
    Requires a checkpoint path.
    ```bash
    uv run python -m <project_name> mode=predict checkpoint=path/to/checkpoint.ckpt
    ```

## Provenance

Every run in this repo is provenance-tracked via [rationai-provenance](https://github.com/RationAI/provenance): preprocessing apps call `log_provenance`, and the training run gets the `ProvenanceCallback` (already wired in [`configs/ml.yaml`](configs/ml.yaml)). Runs link to the user who started them, the dataset registration, the git commit, the Docker image and the hardware — an unregistered user fails the run at startup.

Prerequisites (see the [provenance template](https://github.com/RationAI/prov-ml-template) for the full pipeline with splits and embeddings):

```bash
export MLFLOW_TRACKING_URI=...  # your MLflow server
export MLFLOW_USER=...          # must be your exact Rancher username

# register yourself (once ever)
uv run python -c "from rationai.provenance import register_new_user; register_new_user(
    username='...', real_name='...', email='...',
    organization='...', lead_name='...', lead_email='...')"

# register the dataset (data manager, once per dataset version) — prints the run_id
uv run python -c "from rationai.provenance import register_dataset; print(register_dataset(
    'cohort.csv', path_column='path', dataset_name='my-dataset'))"
```

Paste the printed `run_id` (and your split URIs, if your split pipeline produces train/test CSVs) into [`configs/ml.yaml`](configs/ml.yaml):

```yaml
dataset:
  run_id: f0c2a1…
  split_uris: {train: 'mlflow-artifacts:/<exp_id>/<run_id>/artifacts/train.csv',
               test: 'mlflow-artifacts:/<exp_id>/<run_id>/artifacts/test.csv'}
```

Training then verifies the data on disk against the registration (`fail_fast` aborts on mismatch) and references the splits instead of recomputing them.

## Linting, Formatting and Type Checking:

```bash
uvx ruff check  # Check and fix linting issues
uvx ruff format # Format code
uv run mypy .     # Run mypy
```
