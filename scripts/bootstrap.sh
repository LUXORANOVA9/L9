#!/usr/bin/env bash
set -euo pipefail

# Determine repo root (script may be run from any directory)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔧 LUXOR9 monorepo bootstrap"

command -v poetry >/dev/null 2>&1 || {
  echo "❌ Poetry is not installed. Install with 'pipx install poetry' or see https://python-poetry.org/docs/#installation"
  exit 1
}

command -v pnpm >/dev/null 2>&1 || {
  echo "❌ pnpm is not installed. Install with 'npm install -g pnpm' or see https://pnpm.io/installation"
  exit 1
}

command -v pre-commit >/dev/null 2>&1 || {
  echo "❌ pre-commit is not installed. Install with 'pipx install pre-commit' or 'pip install pre-commit'."
  exit 1
}

echo "• Installing Python dependencies via Poetry"
poetry install --no-root

echo "• Installing JavaScript dependencies via pnpm"
pnpm install

echo "• Installing pre-commit hooks"
pre-commit install

echo "✅ Bootstrap complete"
