# oarc-log

A simple Context-Aware Logger for Python that automatically detects which module is generating log messages, making your logs clearer and more useful for debugging.

## Features

| Feature                     | Description                                                  |
| :-------------------------- | :----------------------------------------------------------- |
| 🔍 **Context Detection**    | Automatically identifies which module is logging             |
| 🔄 **Singleton Pattern**    | Consistent logging configuration across your application     |
| 🌐 **External Integration** | Easily redirect and control logs from third-party libraries  |
| 🎛️ **Debug Toggle**        | Simple activation of verbose logging                         |
| 🧩 **Standard Compatible**  | Built on Python's standard logging module                   |

## Setup

OARC-Log requires Python >=3.10 and <3.12.

### Basic Installation

```bash
# Install directly from PyPI
pip install oarc-log
```

## Basic Usage

OARC-Log provides a simple, intuitive logging interface with automatic module context detection.

```python
from oarc_log import log

# Basic logging - automatically includes calling module name
log.info("Application started")
log.debug("This message only shows when debug is enabled")
log.warning("Something to note")
log.error("Something went wrong")
log.critical("Fatal error occurred")
```

### Enable Debug Logging

```python
from oarc_log import enable_debug_logging

# Enable debug logging globally
enable_debug_logging()

# Now debug messages will be displayed
log.debug("This will now be shown")
```

### Integration with Click CLI

```python
import click
from oarc_log import log, enable_debug_logging

@click.command()
@click.option("--verbose", is_flag=True, callback=enable_debug_logging, 
              help="Enable debug logging")
def cli(verbose):
    log.info("CLI started")
    if log.is_debug_enabled():
        log.debug("Debug mode active")
```

### Module-Specific Loggers

```python
from oarc_log import get_logger

# Get a named logger for a specific component
logger = get_logger("my_component")
logger.info("Component initialized")
```

### Managing External Libraries

```python
from oarc_log import redirect_external_loggers
import logging

# Redirect and quiet down noisy libraries
redirect_external_loggers("requests", "urllib3", "boto3", level=logging.WARNING)
```

## API Reference

### Primary Objects

- **`log`**: The main logging object with automatic context detection
- **`get_logger(name=None)`**: Get a configured logger for a specific module
- **`redirect_external_loggers(*module_names, level=logging.WARNING)`**: Configure external loggers
- **`enable_debug_logging()`**: Set logging level to DEBUG

### Core Classes

- **`ContextAwareLogger`**: Wrapper that determines the calling module
- **`Logger`**: Singleton manager for logging configuration

## Development

For development, clone the repository and install with development dependencies:

```bash
# Clone the repository
git clone https://github.com/Ollama-Agent-Roll-Cage/oarc-log.git
cd oarc-log

# Install UV package manager
pip install uv

# Create & activate virtual environment with UV
uv venv --python 3.11

# Install in development mode with dev dependencies
uv pip install -e ".[dev]"
```

## Project Structure

```
oarc-log/
├── docs/                # Documentation
│   └── Specification.md # Technical specification
├── src/
│   └── oarc_log/        # Source code
│       ├── __init__.py  # Package exports
│       └── log.py       # Core logging implementation
└── README.md            # Project overview
```

## License

This project is licensed under the [Apache 2.0 License](LICENSE)

## Citations

Please use the following BibTeX entry to cite this project:

```bibtex
@software{oarc,
  author = {Leo Borcherding, Kara Rawson},
  title = {OARC: Ollama Agent Roll Cage is a powerful multimodal toolkit for AI interactions, automation, and workflows.},
  date = {4-20-2026},
  howpublished = {\url{https://github.com/Ollama-Agent-Roll-Cage/oarc}}
}
```

## Contact

For questions or support, please contact us at:

- **Email**: <NotSetup@gmail.com>
- **Issues**: [GitHub Issues](https://github.com/Ollama-Agent-Roll-Cage/oarc-log/issues)