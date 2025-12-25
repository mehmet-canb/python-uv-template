# Python Project Template

A modern Python project template using Nix flakes, uv for dependency management, ruff for linting/formatting, and basedpyright for type checking.

## Features

- Python 3.14 - Latest Python version
- uv - Fast Python package installer and dependency manager
- Nix Flakes - Reproducible development environment
- Ruff - Fast Python linter and formatter with isort
- basedpyright - Advanced type checker
- pre-commit - Automated code quality checks
- coverage - Code coverage tracking for tests
- Dependency groups - Organized dev and test dependencies

## Prerequisites

- [Nix](https://nixos.org) with flakes enabled
- [direnv](https://direnv.net/) (optional, for automatic environment activation)

**Recommended:** Use the [Determinate Nix Installer](https://determinate.systems/nix-installer/) for the easiest installation experience. It enables flakes by default and provides automated uninstallation.

<details>
<summary>Alternative: Official Nix installer</summary>

If you prefer the official installer, follow the instructions at [nixos.org/download](https://nixos.org/download.html).

Note that the official installer does not automate the uninstallation process.
</details>

## Quick Start

### 1. Create Your Project

**Recommended:** Use GitHub's template feature

1. Click the "Use this template" button at the top of this repository
2. Create a new repository from the template
3. Clone your new repository:

```bash
git clone https://github.com/<your-username>/<your-project-name>
cd <your-project-name>

# If using direnv
direnv allow

# Or manually enter the nix shell
nix develop
```

<details>
<summary>Alternative: Manual clone (hosting agnostic)</summary>

```bash
# Clone the template repository
git clone https://github.com/mehmet-canb/python-uv-template <your-project-name>
cd <your-project-name>

# Remove the template's git history and start fresh
rm -rf .git
git init
git add .
git commit -m "Initial commit"

# Add your own remote (example uses GitHub)
git remote add origin https://github.com/<your-username>/<your-project-name>
git push -u origin main
```

</details>

The Nix shell will automatically:
- Install Python 3.14, uv, ruff, basedpyright, and pre-commit
- Sync dependencies with `uv sync`
- Activate the virtual environment
- Install pre-commit hooks

### 2. Install Dependencies

```bash
# Install development dependencies
uv sync --group dev

# Install test dependencies
uv sync --group test

# Install all dependencies
uv sync --all-groups
```

### 3. Run the Application

```bash
# Using the CLI entry point
uv run app

# Or directly with Python
uv run python -m app.main
```

### 4. Rename the Package

The default package name is `app`. To rename it to your project name, run:

```bash
./scripts/rename-package.sh <new-project-name>
```

This script updates all configuration files, renames `src/app`, and fixes Python imports.

<details>
<summary>What the script changes</summary>

#### `pyproject.toml`:

The distribution name:

```toml
[project]
name = "app"  # Changed to your project name
version = "0.1.0"
description = "An app description"  # Update this manually
authors = [{ name = "Your Name" }]  # Update this manually
```

Command name and module path:

```toml
[project.scripts]
app = "app.main:main"
```

Import sorting module name:

```toml
[tool.ruff.lint.isort]
known-first-party = ["app"]
```

Coverage report module name:

```toml
[tool.pytest.ini_options]
addopts = "-v --maxfail=1 --cov=app --cov-report=html:tests/test_results/htmlcov"
```

#### `Makefile`

Run target:

```make
run: load-env ## Run the application
	uv run app
```

#### Miscellaneous

`src/app/` directory is renamed to `src/<new-project-name>/` and all Python imports in `src/` and `tests/` are updated.

</details>

## Development

### Code Quality

The project uses pre-commit hooks to enforce code quality:

```bash
# Run all hooks manually
pre-commit run --all-files

# Hooks run automatically on git commit
git commit -m "your message"
```

Hooks include:
- Trailing whitespace removal
- Large file detection
- Python AST validation
- TOML/YAML validation
- Ruff linting (with isort for import sorting)
- Ruff formatting
- basedpyright type checking

### Type Checking

```bash
# Run type checker manually
basedpyright

# Or for specific files
basedpyright src/app/main.py
```

### Linting and Formatting

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

### Testing

This template supports both unit testing with pytest and metric-based evaluation scripts.

```bash
# Run unit tests with coverage
uv run pytest
```

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Project Structure

```
.
├── flake.lock # Development dependency locks
├── flake.nix # Development environment specifications
├── pyproject.toml # Python project specifications
├── README.md # This file
├── src
│   └── app
│       ├── __init__.py
│       └── main.py # Entry point for the program
├── tests/
└── uv.lock # Python dependency locks
```

## Configuration

### Environment Variables

This template uses a `.env` file for environment configuration.

#### Setting Up `.env`

```bash
# Creates .env from .env.example with CWD automatically set
make setup-env
```

The setup process:
1. Copies `.env.example` to `.env`
2. Replaces `DUMMY_PATH` with your current working directory
3. Strips inline comments (e.g., `DEBUG=false # comment` becomes `DEBUG=false`)

**Note:** Inline comments in `.env.example` are for documentation only and are removed in `.env` to ensure compatibility with all tools.

#### Environment Loading in Makefile

The `test` and `run` targets automatically load `.env` variables before execution. This makes environment variables available to non-Python tools that don't use pydantic-settings.

```bash
# Both commands have access to .env variables
make test
make run
```

#### Local Environment Overrides

For personal environment customizations that shouldn't be committed:

1. Create a `.envrc.local` file (already in `.gitignore`)
2. Add your local overrides

The `.envrc` automatically sources `.envrc.local` if it exists, so direnv users get automatic loading of personal settings.

### Changing Python Version

The Python version is read from the `.python-version` file:

```bash
# Change Python version (e.g., to 3.13)
uv python pin 3.13

# Update the uv lock file for the new Python version
uv lock

# Re-enter the Nix shell to use the new version
nix develop
```

**Note**: nixpkgs only provides major.minor Python versions by default (e.g., `python313`, `python314`). Patch-specific versions require additional Nix overlays. See comments in `flake.nix` for details.

### Adding Dependencies

```bash
# Add a production dependency
uv add package-name

# Add a dev dependency
uv add --group dev package-name

# Add a test dependency
uv add --group test package-name
```

### Ruff Configuration

Ruff is configured in `pyproject.toml` with:
- Line length: 88 (Black-compatible)
- Enabled rules: C (complexity), E (errors), F (pyflakes), W (warnings), I (isort)
- Auto-fixing enabled for most rules
- Python 3.14 target

### Basedpyright Configuration

Basedpyright is configured in `pyproject.toml` with:
- Recommended type checking rules
- Including only project files
- Linux oriented target

## Common Tasks

### Update Dependencies

```bash
# Update all dependencies
uv lock --upgrade

# Update specific package
uv lock --upgrade-package package-name
```

### Clean Build Artifacts

```bash
# Remove cache directories
rm -rf __pycache__ .ruff_cache .pytest_cache .mypy_cache
rm -rf .coverage htmlcov/ tests/test_results/
rm -rf build/ dist/ *.egg-info
```

### Update Pre-commit Hooks

```bash
pre-commit autoupdate
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.
