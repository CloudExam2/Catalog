# Catalog Service Repository

Standalone microservice for **Product**, **Client**, and **Address** data. It follows **database-per-service**: only this service owns its catalog schema and its PostgreSQL instance.

This document describes the **intended production architecture**. Some pieces (Terraform, SQS publishing, API Gateway integration) may not be fully implemented in code yet; the sections below are the target end state.

## AWS student lab constraint

**Outbound internet from workloads:** Student lab accounts often **do not allow** application instances to reach the **public internet** for arbitrary traffic (generic HTTP/HTTPS egress, public package indexes, Docker Hub at runtime, etc.). Treat the lab as **private-by-default**: use **VPC endpoints** (or other AWS-documented private integration) for **ECR, SSM, S3, SQS**, and similar, unless your instructor explicitly permits open egress.

**Internet Gateway (optional in Core):** Core’s `vpc.tf` keeps the **IGW and default route commented out** by default. **VPC interface endpoints** (see Core `vpc_endpoints.tf`) provide **PrivateLink-style** access to **ECR, SSM, and S3** inside the VPC. Your laptop **cannot** rely on **`http://<public-EC2-IP>/`** the same way as on the open internet without an IGW route; use **SSM port forwarding** or **API Gateway** when you add that path.

### How to hit the Catalog API from your laptop (no IGW)

1. AWS CLI configured, instance registered with SSM.
2. `aws ssm start-session --target <instance-id> --document-name AWS-StartPortForwardingSession --parameters '{"portNumber":["80"],"localPortNumber":["8080"]}'`
3. Open `http://localhost:8080/` in the browser.

The Catalog CI job **Verify app via SSM** only checks **`curl` on the instance** (inside the VPC); it does **not** prove your home PC can reach PrivateLink, because GitHub’s runner is not in your VPC.

---

## Target architecture

### What lives in this repository (service scope)

The Catalog service’s own infrastructure is intentionally narrow: **compute**, **database**, and **networking** that attach to the shared platform.

| Layer | Responsibility |
| :--- | :--- |
| **Compute** | Dockerized FastAPI application running on a **dedicated EC2** instance. |
| **Database** | **Private RDS (PostgreSQL)** used only by Catalog. No shared DB with Sales or other services. |
| **Networking** | **Subnets and security groups** so the app can talk to RDS and to AWS APIs (SQS) from private address space, without exposing the API directly on the public internet. |

Service-specific **Terraform** in this repo should provision those pieces (EC2, RDS, instance profile/IAM for the host, security groups, subnet placement) using outputs or remote state from **Core** for the shared VPC identifiers.

### What comes from Core (global platform)

Per the **Core** repository, shared concerns are **not** duplicated here:

* **VPC, subnets, and baseline routing** — shared network foundation.
* **Amazon API Gateway** — **single public entry** for HTTP. External clients call routes such as `/catalog/*`; the gateway forwards traffic to this service’s EC2 integration. The Catalog app is **not** meant to be reached by opening a public port on the instance alone.
* **Amazon SQS** — queues used for **asynchronous service-to-service** messaging. Catalog’s role is to **publish** messages when catalog data changes so **Sales** can consume and stay consistent (Sales runs the consumer). Queue definitions and cross-service IAM are owned at the platform level; Catalog receives queue URLs and credentials via configuration (see `environment.md` when populated for this service).

### Integration summary

```text
Internet / clients
        │
        ▼
  API Gateway (Core)  ──HTTP──►  Catalog EC2 (this repo)
        │                              │
        │                              ├──► RDS PostgreSQL (private, this repo)
        │                              │
        │                              └──► SQS publish ──► Sales (consumer)
```

---

## Monitoring (target)

* **Functional:** Track HTTP status codes from requests that reach the app (2xx vs 4xx/5xx), including traffic forwarded from API Gateway.
* **Performance:** Track end-to-end handling time for persistence and (when implemented) event publish to SQS.
* **Alarms:** Example policy — alert on sustained high latency (e.g. processing consistently above **500 ms**), tuned after baseline metrics exist.

Central dashboards and cross-service aggregation are expected to live in **Core** observability; this service should expose metrics and structured logs in a way that platform collection can scrape or ship.

---

## Repository layout

* `src/main.py` — FastAPI application entrypoint.
* `src/routers/` — HTTP route handlers (clients, products, addresses).
* `src/schemas/` — Request/response models.
* `src/database.py`, `src/models.py`, `src/repositories.py` — DB session, ORM models, and data access.
* `db/schema.sql` — SQL reference / migrations aid for the catalog schema.
* `Dockerfile` — Container image for deployment on EC2.
* `terraform/` — EC2, RDS, security groups; **reads Core’s remote state** (`remote_state.tf`) for `vpc_id` and `public_subnet_ids`. **Apply Core before Catalog** so that state exists.
* `.github/workflows/` — Build, push to ECR, and deploy (e.g. SSM-based restart on EC2).

Configuration keys for runtime (database URL, SQS queue URL, region, etc.) belong in **`environment.md`** in this directory as they are finalized.
