"""MLflow experiment tracking integration."""

from typing import Any

import mlflow
import mlflow.sklearn


def setup_mlflow(experiment_name: str = "churn-prediction") -> None:
    """Initialize MLflow experiment."""
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment(experiment_name)


def log_training_run(
    model_name: str,
    params: dict[str, Any],
    metrics: dict[str, float],
    model: Any,
    artifacts: dict[str, str] | None = None,
) -> None:
    """Log a complete training run to MLflow."""
    with mlflow.start_run(run_name=model_name):
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        # Log the trained model
        mlflow.sklearn.log_model(model, "model")

        # Log any additional artifacts (like feature importance CSVs, charts)
        if artifacts:
            for _name, path in artifacts.items():
                mlflow.log_artifact(path)
