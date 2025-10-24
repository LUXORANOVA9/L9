# Monorepo Migration Checklist

Use this checklist when importing an existing project into the Luxor9 monorepo.

## Pre-Migration
- [ ] Confirm maintenance window with stakeholders.
- [ ] Snapshot current repositories and tag the last good commit.
- [ ] Identify services, dependencies, secrets, and build pipelines that will be migrated.

## Repository Import
- [ ] Create a new branch for the migration work.
- [ ] Use `git filter-repo` or `git subtree add` to extract the target repository without history noise.
  ```bash
  git remote add legacy <url>
  git fetch legacy main
  git subtree add --prefix=apps/<service> legacy main --squash
  ```
- [ ] Move shared libraries into `packages/` when appropriate.
- [ ] Remove vendored binaries, virtual environments, and secrets.
- [ ] Add service-level README, Makefile targets, and package metadata (Poetry or pnpm).

## Tooling Integration
- [ ] Register the package in `pnpm-workspace.yaml` or add a Poetry project file.
- [ ] Add lint/test scripts (`lint`, `test`, `format`) for pnpm packages.
- [ ] Extend unit/integration tests to run via `make test`.
- [ ] Update `.pre-commit-config.yaml` if new language tooling is required.

## Secrets & Configuration
- [ ] Delete `.env`, `.pem`, `*.key`, and other plaintext secrets.
- [ ] Rotate credentials in upstream systems.
- [ ] Generate new Kubernetes secrets and seal them (`config/README.md`).
- [ ] Commit sealed secrets to `config/secrets/templates/` with ownership comments.

## CI/CD
- [ ] Update `.github/CODEOWNERS` and CI matrix filters if necessary.
- [ ] Ensure `pnpm lint/test` and `poetry run` commands succeed locally.
- [ ] Add infrastructure changes (Helm, Terraform) to `infra/` and validate via `make lint-infra`.

## Documentation
- [ ] Document service overview and runbooks in `docs/` (link from README).
- [ ] Record architecture decisions in `docs/adr/` if the migration introduced structural changes.
- [ ] Update onboarding docs if new tooling or flows were introduced.

## Post-Migration
- [ ] Run the full CI pipeline (`make lint`, `make test`, `make docs`).
- [ ] Open PR, request reviews from platform/security.
- [ ] Announce completion, including rotated credentials and next steps.
