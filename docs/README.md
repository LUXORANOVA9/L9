# Documentation Hub

This folder will become the single entry point for engineering documentation.

Recommended layout:
- `docs/dev/` – local development guides, toolchain setup, coding standards.
- `docs/ops/` – runbooks, incident response, maintenance procedures.
- `docs/adr/` – lightweight Architecture Decision Records (one Markdown file per decision).

Suggested tooling: [MkDocs](https://www.mkdocs.org/) with the Material theme. Once initial content is in place, add a `mkdocs.yml` at the repo root and a CI job that builds the docs on every pull request.

Link each app/package README back to relevant pages here to minimise duplication.
