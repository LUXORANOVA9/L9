# Scripts

Bootstrap and maintenance scripts live here. Examples:

- `bootstrap.sh` – installs prerequisite toolchains and hooks.
- `format.sh` – runs formatters across languages.
- `ci-local.sh` – emulates the CI pipeline for pre-flight checks.

Scripts should:
- Be safe to run multiple times (idempotent).
- Log actions clearly and exit non-zero on failure.
- Avoid hard-coded paths; detect repo root dynamically.
