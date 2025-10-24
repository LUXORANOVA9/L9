# Toolchain Overview

The monorepo standardises on the following developer tooling:

- **Python** – managed by [Poetry 1.8](https://python-poetry.org/). All Python packages should declare dependencies in their own `pyproject.toml` and rely on the root virtualenv for shared tooling (ruff, black, pytest, mkdocs).
- **JavaScript/TypeScript** – managed by [pnpm 9](https://pnpm.io/). Front-end and Node services should be added to the workspace via `pnpm-workspace.yaml` and expose `lint`, `test`, and `format` scripts.
- **Formatting/Linting** – enforced by `pre-commit`, `ruff`, `black`, `eslint`, `prettier`, and `yamllint`. Run `make lint` / `make format` before submitting PRs.
- **License Reporting** – run `make license-scan` (or `tools/license-scan.sh`) to export Python and pnpm dependency notices.
- **Documentation** – built with MkDocs + Material theme; update navigation in `mkdocs.yml` when adding new sections.

When introducing new languages or frameworks, document expectations here and extend the bootstrap/CI tooling accordingly.
