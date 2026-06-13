"""MLflow experiment tracking integration."""

import mlflow
import mlflow.sklearn
from typing import Dict, Any

def setup_mlflow(experiment_name: str = "churn-prediction") -> None:
    """Initialize MLflow experiment."""
    mlflow.set_experiment(experiment_name)

def log_training_run(
    model_name: str, 
    params: Dict[str, Any], 
    metrics: Dict[str, float], 
    model: Any, 
    artifacts: Dict[str, str] = None
) -> None:
    """Log a complete training run to MLflow."""
    with mlflow.start_run(run_name=model_name):
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        
        # Log the trained model
        mlflow.sklearn.log_model(model, "model")
        
        # Log any additional artifacts (like feature importance CSVs, charts)
        if artifacts:
            for name, path in artifacts.items():
                mlflow.log_artifact(path)
