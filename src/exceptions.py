"""Custom exceptions for the churn analytics pipeline."""


class ChurnAnalyticsError(Exception):
    """Base exception for all project errors."""


class DataLoadError(ChurnAnalyticsError):
    """Raised when data files cannot be loaded."""


class DataValidationError(ChurnAnalyticsError):
    """Raised when data fails quality checks."""


class ModelLoadError(ChurnAnalyticsError):
    """Raised when the trained model cannot be loaded."""


class ModelPredictionError(ChurnAnalyticsError):
    """Raised when prediction fails."""


class PipelineError(ChurnAnalyticsError):
    """Raised when the pipeline encounters a fatal error."""


class ConfigError(ChurnAnalyticsError):
    """Raised when configuration is invalid."""
