# Scopes in Dependency Injection

Scopes define the lifecycle and lifetime of dependencies in a dependency injection system. They determine when dependencies are created, how long they live, and when they are destroyed.

## What are Scopes?

A scope is a context within which dependencies have a specific lifetime. Dependencies within the same scope are typically created once and reused throughout the scope's lifetime. When the scope ends, all dependencies within that scope are cleaned up.

## Using Scopes in Needy

Needy provides a flexible scope system that uses class declarations to define scope hierachies

### Declarative Scope Definition

Scopes are defined using a clean, declarative syntax:

```python
from needy import BaseScope, root, has_parents

class MyScope(BaseScope):
    SINGLETON = root()
    REQUEST = has_parents(SINGLETON)
    SESSION = has_parents(REQUEST)
```

### Accessing Scope Definitions

Scope definitions are created on-demand when accessed:

```python
from needy import ScopeType, PytestScope, FastAPIScope

# Access scope definitions
singleton = ScopeType.SINGLETON
request = ScopeType.REQUEST

# Check parent relationships
assert ScopeType.SINGLETON in request.get_direct_parents()
assert ScopeType.SINGLETON in request.get_valid_parents()
```

### Parent Scope Validation

Each scope definition knows its valid parent scopes:

```python
# Direct parents (immediate parent in hierarchy)
direct_parents = PytestScope.FUNCTION.get_direct_parents()
# Returns: {PytestScope.DEFINITION}

# All valid parents (including indirect parents)
all_parents = PytestScope.FUNCTION.get_valid_parents()
# Returns: {PytestScope.DEFINITION, PytestScope.CLASS, PytestScope.MODULE, 
#           PytestScope.PACKAGE, PytestScope.SESSION}
```

## Predefined Scope Types

Needy comes with predefined scope types for common frameworks:

- **[ScopeType](api/scopes.md#scopetype)** - Base scope types (SINGLETON, REQUEST, SESSION)
- **[PytestScope](api/scopes.md#pytestscope)** - Pytest testing scopes (SESSION, PACKAGE, MODULE, CLASS, DEFINITION, FUNCTION, SUBTEST)
- **[FastAPIScope](api/scopes.md#fastapiscope)** - FastAPI web scopes (APPLICATION, REQUEST, BACKGROUND_TASK)

## Scope Best Practices

1. **Choose Appropriate Scopes**: Use the narrowest scope that meets your needs
2. **Avoid Scope Leaks**: Don't store request-scoped dependencies in application scope
3. **Resource Management**: Always clean up resources when scopes end
4. **Testing**: Use test scopes to isolate tests and clean up after each test

## Common Anti-Patterns

```python
# ❌ Bad - Request data in app scope
app.state.current_user = None

# ✅ Good - Use request scope
def get_current_user(request: Request):
    return request.state.current_user

# ❌ Bad - Expensive operation in function scope
@pytest.fixture(scope="function")
def heavy_computation():
    return expensive_operation()  # Runs for every test

# ✅ Good - Use session scope for expensive operations
@pytest.fixture(scope="session")
def heavy_computation():
    return expensive_operation()  # Runs once
```

The actual scope management and dependency resolution will be handled by containers that use these scope definitions to determine when to create, cache, and clean up dependencies. 