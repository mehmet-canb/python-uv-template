# Tests

This directory contains tests for the project, organized into unit tests and benchmarks.

## Structure

```
tests/
├── unit_tests/        # pytest unit tests
├── benchmarks/        # Performance benchmarks and metric-based evaluation scripts
└── test_results/      # Generated coverage reports (gitignored)
```

## Running Unit Tests

The project uses pytest for unit testing with coverage reporting.

```bash
# Run all unit tests with coverage
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/unit_tests/test_example.py

# View coverage report
# Coverage HTML report is generated in tests/test_results/htmlcov/
# Open tests/test_results/htmlcov/index.html in a browser
```

## Test Configuration

pytest is configured in `pyproject.toml`:
- Verbose output (`-v`)
- Stops after first failure (`--maxfail=1`)
- Automatic coverage reporting
- HTML coverage reports saved to `tests/test_results/htmlcov/`

## Writing Unit Tests

Create test files in `tests/unit_tests/` following the naming convention `test_*.py`:

```python
# tests/unit_tests/test_example.py
def test_example():
    assert 1 + 1 == 2
```

## Benchmarks

The `benchmarks/` directory is for:
- Performance benchmarks
- Model evaluation scripts
- Metric-based testing (ideal for AI/ML workflows)
- Data validation tests
- Integration tests for data pipelines
- Inference API tests

Run benchmark scripts directly:
```bash
uv run python tests/benchmarks/your_benchmark.py
```

## Coverage Reports

Coverage reports are automatically generated when running `uv run pytest`:
- HTML report: `tests/test_results/htmlcov/index.html`
- The `test_results/` directory is gitignored

To generate coverage manually with different formats:
```bash
uv run coverage run -m pytest
uv run coverage report          # Terminal output
uv run coverage html            # HTML report
uv run coverage xml             # XML report for CI
```
