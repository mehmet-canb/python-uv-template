#!/usr/bin/env bash
#
# Rename the package from "app" to a new name.
# Usage: ./scripts/rename-package.sh <new-package-name>
#
# This script updates:
# - pyproject.toml (name, scripts, isort, pytest coverage)
# - Makefile (run target)
# - src/app directory → src/<new-name>
# - All Python imports in src/ and tests/

set -euo pipefail

OLD_NAME="app"

usage() {
    echo "Usage: $0 <new-package-name>"
    echo ""
    echo "Renames the package from 'app' to the specified name."
    echo ""
    echo "Example:"
    echo "  $0 myproject"
    exit 1
}

# Validate arguments
if [[ $# -ne 1 ]]; then
    usage
fi

NEW_NAME="$1"

# Validate package name (PEP 503 normalized: lowercase, hyphens become underscores)
if [[ ! "$NEW_NAME" =~ ^[a-z][a-z0-9_-]*$ ]]; then
    echo "Error: Package name must start with a lowercase letter and contain only lowercase letters, numbers, hyphens, or underscores."
    exit 1
fi

# For Python imports, convert hyphens to underscores
NEW_NAME_PYTHON="${NEW_NAME//-/_}"

# Check if already renamed
if [[ ! -d "src/$OLD_NAME" ]]; then
    echo "Error: src/$OLD_NAME directory not found."
    echo "Has the package already been renamed?"
    exit 1
fi

echo "Renaming package: $OLD_NAME → $NEW_NAME"
echo "Python import name: $NEW_NAME_PYTHON"
echo ""

# 1. Update pyproject.toml
echo "Updating pyproject.toml..."
sed -i "s/^name = \"$OLD_NAME\"/name = \"$NEW_NAME\"/" pyproject.toml
sed -i "s/^$OLD_NAME = \"$OLD_NAME\.main:main\"/$NEW_NAME_PYTHON = \"$NEW_NAME_PYTHON.main:main\"/" pyproject.toml
sed -i "s/known-first-party = \[\"$OLD_NAME\"\]/known-first-party = [\"$NEW_NAME_PYTHON\"]/" pyproject.toml
sed -i "s/--cov=$OLD_NAME/--cov=$NEW_NAME_PYTHON/" pyproject.toml

# 2. Update Makefile
echo "Updating Makefile..."
sed -i "s/uv run $OLD_NAME/uv run $NEW_NAME_PYTHON/" Makefile

# 3. Update Python imports in src/ and tests/
echo "Updating Python imports..."
find src tests -name "*.py" -type f -exec sed -i "s/from $OLD_NAME\./from $NEW_NAME_PYTHON./g" {} +
find src tests -name "*.py" -type f -exec sed -i "s/import $OLD_NAME/import $NEW_NAME_PYTHON/g" {} +

# 4. Rename the package directory, needs to be done last
echo "Renaming src/$OLD_NAME → src/$NEW_NAME_PYTHON..."
mv "src/$OLD_NAME" "src/$NEW_NAME_PYTHON"

# 5. Update lock file and sync environment
echo "Updating lock file and syncing environment..."
uv lock
uv sync --all-groups

echo ""
echo "Done! Package renamed to '$NEW_NAME'."
echo ""
echo "Next steps:"
echo "  1. If using direnv, run: direnv reload"
echo "  2. Review the changes: git diff"
echo "  3. Run tests: make test"
echo "  4. Commit the changes"
