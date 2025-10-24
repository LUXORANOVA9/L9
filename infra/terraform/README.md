# Terraform Baseline

Terraform modules and environment stacks live here. Structure recommendation:

- `modules/` – reusable Terraform modules (networks, compute, databases).
- `environments/<env>/` – environment-specific configuration referencing modules.

Example workflow:
```bash
cd infra/terraform/environments/example
terraform init
terraform plan
```

State should be stored remotely (e.g., S3 + DynamoDB). Document backends in each environment directory.
