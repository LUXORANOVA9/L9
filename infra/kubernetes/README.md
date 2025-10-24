# Kubernetes Assets

This directory captures cluster-level assets used by the Luxor9 platform.

Suggested layout:
- `base/` – shared manifests (namespaces, RBAC, sealed secret controllers, ingress classes).
- `overlays/<env>/` – environment-specific kustomizations.
- `charts/` – Helm charts maintained in-house.

Example commands (once manifests exist):
```bash
kubectl kustomize infra/kubernetes/overlays/dev | kubectl apply -f -
helm lint infra/kubernetes/charts/luxor9
```

Keep secrets out of this tree—reference encrypted manifests from `config/secrets/templates/` instead.
