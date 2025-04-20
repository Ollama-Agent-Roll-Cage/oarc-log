"""
OARC Crawlers Utilities

This package provides essential utilities for the OARC Crawlers project, including:

- Centralized, context-aware logging for consistent and informative output across all modules
- Standardized error classes to facilitate robust exception handling
- Path management and helper functions to simplify crawler development and maintenance

Import this package to access the `log` object for logging, error types, and utility classes that streamline building and operating OARC crawlers.
"""

from .log import (
    log,
    ContextAwareLogger,
    get_logger,
    redirect_external_loggers,
    enable_debug_logging,
)

__all__ = [
    "log",
    "ContextAwareLogger",
    "get_logger",
    "redirect_external_loggers",
    "enable_debug_logging"
]