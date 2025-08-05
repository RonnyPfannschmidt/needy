# Needy

An experiment about bringing together ideas from various DI systems in Python.

## Overview

Needy is an experiment about bringing together ideas from various dependency injection systems in Python.

### Key Inspirations

- **pytest fixtures** - Parameterization and versatile mechanisms
- **dishka** - Modern async DI container
- **svc** - Explicit dependency registration
- **morepath** - Framework integration
- **zope** - Mature DI ecosystem
- **fastapi** - Type-based dependency resolution

### Intended Features

- Declarations of services/resources and their lifecycles
- Scopes and their interactions (testing lifecycles vs application lifecycles)
- Parameterization and versatile mechanisms of keeping things alive
- Sync/async usage with async code and sync outside usage
- Multiple resolvers/mechanisms to provide dependencies

## Quick Start

```python
import needy

print(f"Needy version: {needy.__version__}")
```

## Installation

```bash
# Install with uv
uv sync

# Or with pip
pip install -e .
```
