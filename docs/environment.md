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

### Core VPC dependency

Catalog Terraform reads **Core’s applied state** (`terraform/remote_state.tf` → S3 key `core/terraform.tfstate`) for **`vpc_id`** and **`public_subnet_ids`**.

1. Run **Core** CI/CD (or `terraform apply` in Core) **first** so the VPC exists and outputs are written to that state file.
2. Then run **Catalog** CI/CD. The IAM user used in GitHub Actions must be allowed to **`s3:GetObject`** on the state bucket for **both** `core/terraform.tfstate` and `catalog/terraform.tfstate`.

### In-VPC health check job (Catalog workflow)

The **verify-in-vpc** job runs **`curl http://127.0.0.1/`** on the EC2 instance **through SSM**. That proves the container responds **inside the VPC**. It does **not** validate your laptop’s browser path (GitHub runners are not in your VPC). To test from your machine without an IGW, use **SSM port forwarding** (see `catalog.md`).
