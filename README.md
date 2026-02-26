# Print Statements Hook

A Python-based pre-commit hook that uses static analysis to detect and prevent `print()` statements from being committed to your codebase. 

Using `print()` for debugging is common, but leaving them in production code can lead to cluttered logs and potential information leaks. This hook helps you maintain clean code by catching them before they are committed.

## Features

- **Static Analysis**: Uses Python's built-in `ast` module to scan code without executing it.
- **Fast**: Scans files quickly, even in large projects.
- **Pre-commit Integration**: Easy to add to your existing `.pre-commit-config.yaml`.
- **Informative**: Points out the exact file, line, and column where the `print` statement was found.

## Installation

You can install the package locally for development or testing:

```bash
pip install .
```

## Usage

### As a Pre-commit Hook

Add the following to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/kuldeepmodh/print-statements-hook
    rev: v0.1.0  # Use the latest tag or commit hash
    hooks:
      - id: check-print-statements
```

Then run:

```bash
pre-commit install
```

### Manual Usage

You can also run the script manually on specific files or directories:

```bash
# Check specific files
check-print-statements file1.py file2.py

# Check current directory recursively
check-print-statements

# Exclude specific files or directories
check-print-statements --exclude tests --exclude some_legacy_file.py
```

## Development

### Running Tests

This project uses `pytest` for testing.

```bash
pip install pytest
PYTHONPATH=. pytest
```

## How It Works

The hook parses your Python files into an Abstract Syntax Tree (AST). It then walks through the tree looking for `Call` nodes where the function being called is named `print`. If any are found, it reports the location and exits with a non-zero status code, preventing the git commit.

## Versioning

This project follows [Semantic Versioning](https://semver.org/). You can check the installed version using:

```bash
check-print-statements --version
```

### Releasing New Versions

Versioning for pre-commit hooks is primarily handled through Git tags. To release a new version:

1. Update the version in `print_statement_hook/hook.py`, `setup.py`, and `pyproject.toml`.
2. Commit the changes:
   ```bash
   git add .
   git commit -m "Bump version to v0.2.0"
   ```
3. Create a Git tag:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   ```
4. Push the tag to GitHub:
   ```bash
   git push origin v0.2.0
   ```

Users can then reference this specific version in their `.pre-commit-config.yaml`.

## License

MIT License. See [LICENSE](LICENSE) for details.
