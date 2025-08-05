"""Scope types for dependency injection lifecycle management."""
from __future__ import annotations

from typing import Final, Optional, Set, Dict, List, Any, Type, TypeVar, Union, Generic, Sequence




class ScopeDeclaration:
    """Helper class for declaring scope relationships using the descriptor protocol."""
    name: str | None
    direct_parents: Final[tuple["ScopeDeclaration", ...]]

    def __init__(self, direct_parents: Sequence["ScopeDeclaration"] = ()):
        self.name = None  # Will be set by __set_name__
        self.direct_parents = tuple(direct_parents)
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Set the name from the attribute name in the class."""
        self.name = name
    
    def __get__(self, instance: Any, owner: type[T]) -> BoundScopeDefinition[T]:
        assert self.name is not None
        """Create and return a BoundScopeDefinition when accessed."""
        return BoundScopeDefinition(owner, self.name, self)
    
    def __str__(self) -> str:
        return self.name or "unnamed"
    
    def __repr__(self) -> str:
        return f"ScopeDeclaration(name='{self.name}')"



class BaseScope:
    """Base class for all scope types with parent tracking."""
    
    

T = TypeVar('T', bound=BaseScope)

class BoundScopeDefinition(Generic[T]):
    """A scope definition bound to a specific scope class with a name."""
    
    def __init__(self, scope_class: Type[T], name: str, declaration: ScopeDeclaration):
        self.scope_class = scope_class
        self.name = name
        self.declaration = declaration
    
    def __str__(self) -> str:
        return f"{self.scope_class.__name__}.{self.name}"
    
    def __repr__(self) -> str:
        return f"<{self.scope_class.__name__}.{self.name}>"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BoundScopeDefinition):
            return False
        return self.scope_class == other.scope_class and self.name == other.name
    
    def __hash__(self) -> int:
        return hash((self.scope_class, self.name))
    
    def get_direct_parents(self) -> Set["BoundScopeDefinition"]:
        """Get direct parent scope definitions for this scope."""
        if self.declaration:
            # Get the parent names and look them up in the scope class
            parent_names = [parent.name for parent in self.declaration.direct_parents if parent.name]
            return {getattr(self.scope_class, name) for name in parent_names if hasattr(self.scope_class, name)}
        return set()
    
    def get_valid_parents(self) -> Set["BoundScopeDefinition"]:
        """Get all valid parent scope definitions for this scope (including indirect)."""
        return self._compute_all_parents()
    
    def _compute_all_parents(self) -> Set["BoundScopeDefinition"]:
        """Compute all valid parents by traversing the parent hierarchy."""
        all_parents = set()
        to_visit = list(self.get_direct_parents())
        
        while to_visit:
            parent = to_visit.pop(0)
            if parent not in all_parents:
                all_parents.add(parent)
                to_visit.extend(parent.get_direct_parents())
        
        return all_parents


def root() -> ScopeDeclaration:
    """Declare a root scope with no parents."""
    return ScopeDeclaration()


def has_parents(*parents: ScopeDeclaration) -> ScopeDeclaration:
    """Declare a scope type with direct parents."""
    # Store the actual ScopeDeclaration objects
    return ScopeDeclaration(list(parents))


class ScopeType(BaseScope):
    """Base scope types for general dependency injection."""
    
    SINGLETON = root()
    REQUEST = has_parents(SINGLETON)
    SESSION = has_parents(REQUEST)


class PytestScope(BaseScope):
    """Mirror pytest scopes for integration with pytest."""
    
    SESSION = root()
    PACKAGE = has_parents(SESSION)
    MODULE = has_parents(PACKAGE)
    CLASS = has_parents(MODULE)
    DEFINITION = has_parents(CLASS)
    FUNCTION = has_parents(DEFINITION)
    SUBTEST = has_parents(FUNCTION)


class FastAPIScope(BaseScope):
    """Mirror FastAPI scopes for integration with FastAPI."""
    
    APPLICATION = root()
    REQUEST = has_parents(APPLICATION)
    BACKGROUND_TASK = has_parents(APPLICATION)


__all__ = [
    "BaseScope",
    "ScopeType",
    "PytestScope", 
    "FastAPIScope",
    "has_parents",
    "root",
    "ScopeDeclaration",
    "BoundScopeDefinition",
] 