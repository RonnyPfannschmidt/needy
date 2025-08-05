"""Needy - An experiment about bringing together ideas from various DI systems in Python."""

import importlib.metadata
import sys

# Lazy version handling using __getattr__
def __getattr__(name: str) -> str:
    """Lazy attribute loading for __version__."""
    if name == "__version__":
        try:
            return importlib.metadata.version("needy")
        except importlib.metadata.PackageNotFoundError:
            return "0.0+unknwon.error"
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ["__version__"] 