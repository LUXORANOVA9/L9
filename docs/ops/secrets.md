# Secrets Management Runbook

## Overview

All sensitive configuration is managed via Kubernetes Sealed Secrets. Plaintext secrets are prohibited from the repository and CI logs.

## Rotation Checklist

1. Notify stakeholders and schedule a brief maintenance window.
2. Identify the secret to rotate and update the source of truth (password manager, cloud console).
3. Generate a new Kubernetes secret manifest with `kubectl create secret ... --dry-run=client -o yaml` (see `config/secrets/templates/example-app.sealed-secret.yaml` for structure).
4. Seal the manifest using the current controller certificate (`tools/seal-secret.sh secret.yaml config/secrets/templates/<name>.sealed-secret.yaml`).
5. Commit the sealed secret to `config/secrets/templates/` with a clear name and version comment.
6. Run CI to ensure linting/kubectl validation passes.
7. Apply the sealed secret in the target cluster (GitOps or `kubectl apply`).
8. Verify the dependent services restart successfully.
9. Revoke the old credential.

## Emergency Revocation

If a leak is suspected:
- Immediately disable/revoke the compromised credential in its upstream system.
- Remove any plaintext remnants from logs or issue trackers.
- Follow the rotation checklist to provision a new secret.
- Document the incident in `docs/ops/incidents/<date>-<summary>.md`.

## Tooling

- `kubeseal` (https://github.com/bitnami-labs/sealed-secrets)
- `kubectl`
- Optional: automation script in `tools/seal-secret.sh` (to be added)

For questions or reviews, tag the Security/Platform team in the pull request.
