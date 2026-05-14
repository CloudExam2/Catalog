# Catalog service — configuration

## GitHub Actions secrets (Catalog repository)

These are read by `.github/workflows/deploy.yml` and Terraform in this repo. They are **not** defined in the Core repo.

| Secret | Used for |
| :--- | :--- |
| **AWS_ACCESS_KEY_ID**, **AWS_SECRET_ACCESS_KEY**, **AWS_SESSION_TOKEN** | AWS API access from the workflow (Terraform, ECR, SSM). |
| **GH_PAT** | GitHub provider in Terraform (e.g. writing `EC2_INSTANCE_ID`, `CATALOG_DATABASE_URL` to repo secrets). Needs appropriate repo scope. |
| **DB_PASSWORD** | RDS PostgreSQL master password for `catalog-postgres`. Must satisfy **AWS rules** below. |

### `DB_PASSWORD` (RDS) — required shape

Amazon RDS **PostgreSQL** rejects invalid master passwords. If this is wrong, `CreateDBInstance` fails with **Invalid master password** (this is **not** a Core issue).

- Length: **8–128** characters.
- **Must not** contain: `/`, `@`, `"` (double quote), or **spaces**.

Examples that work: `CatalogLab2026x` or `MyP4ssw0rdForCatalog` (alphanumeric only is safest).

After changing the secret, re-run the workflow so Terraform applies with the new password.

## Terraform remote state (S3)

Backend bucket and key are set in `terraform/providers.tf` (same pattern as other services). Core does **not** supply `DB_PASSWORD`; each service repo owns its own database secret.
