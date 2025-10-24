# Infrastructure

Centralised infrastructure-as-code lives in this directory. Suggested layout:

- `infra/kubernetes/` – Helm charts, Kustomize overlays, sealed secrets manifests.
- `infra/terraform/` – Cloud infrastructure modules and environments.
- `infra/docker/` – Shared Docker Compose files or base images.

Guidelines:
- Keep environment-specific values out of source; reference encrypted manifests in `config/secrets/`.
- Run formatters (`terraform fmt`, `yamlfmt`, `helm lint`) locally or via `make format`.
- Document deployment procedures in `docs/ops/` and link from service READMEs.
