"""Needy - A dependency injection library for Python."""

from ._version import __version__
from .scopes import (
    BaseScope,
    BoundScopeDefinition,
    FastAPIScope,
    PytestScope,
    ScopeDeclaration,
    ScopeType,
    has_parents,
    root,
)

__all__ = [
    "__version__",
    "BaseScope",
    "ScopeType",
    "PytestScope",
    "FastAPIScope",
    "has_parents",
    "root",
    "ScopeDeclaration",
    "BoundScopeDefinition",
]
