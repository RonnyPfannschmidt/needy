# Needy

## inspiration

needy is an experiment about bringing together ideas from various di systems in python

key inspirations are

* pytest fixtures
* dishka
* svc
* morepath
* zope and the surrouding ecosystem
* fastapi

## intended features

* declarations of services/resources and their lifecycles
* scopes and their interactions (testing lifecycles vs application lifecylces - and interplay)
* parameterization and versatile mechanisms of keeping things alive (pytest parametrize with less teardown)
* sync/async usage -> async code, sync outside useage (any dependency that dynamically requests another should be ableto do that async as to ensure control is yielded to the system when obtaining another dependency)
* multiple resolvers/mechanisms to provide dependencies
  * svcs is the key example for something that explicitly avoids injection
  * fastapi/dishka use types and annotations to configure the resolution
  * pytest uses names and parameter values

## Installation

```bash
# Install with uv
uv sync

# Or with pip
pip install -e .
```

## Development

### Pre-commit hooks

This project uses pre-commit hooks for code quality. Install them with:

```bash
# Install pre-commit
pip install pre-commit

# Install the hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### CI/CD

The project uses GitHub Actions with the [build-and-inspect-python-package](https://github.com/hynek/build-and-inspect-python-package) action for:

- **Build & Inspect**: Creates reproducible builds with artifact storage
- **Testing**: Matrix testing across supported Python versions
- **Linting**: ruff, mypy, and codespell checks
- **Documentation**: Automatic docs building
- **PyPI Upload**: Modern OpenID Connect integration for secure uploads

The workflow automatically:
- Uploads to Test PyPI on every push to main
- Uploads to PyPI on releases
- Uses build provenance attestations for security
  