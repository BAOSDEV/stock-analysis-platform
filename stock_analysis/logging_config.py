"""Logging configuration for the stock analysis platform."""

import logging
import sys


def setup_logging(verbose: bool = False) -> None:
    """Configure root logger with a standard format."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module."""
    return logging.getLogger(name)
