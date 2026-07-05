"""Centralized logging configuration."""

import logging
import sys
import time
from functools import wraps


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure root logger with structured format."""
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger("churn_analytics")


def log_step(step_name: str):
    """Decorator that logs start/end/duration of a pipeline step."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger("churn_analytics.pipeline")
            logger.info("START  %s", step_name)
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.info("DONE   %s (%.2fs)", step_name, elapsed)
            return result

        return wrapper

    return decorator
