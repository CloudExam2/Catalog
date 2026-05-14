# Catalog Service Repository

Standalone microservice for **Product**, **Client**, and **Address** data. It follows **database-per-service**: only this service owns its catalog schema and its PostgreSQL instance.

This document describes the **intended production architecture**. Some pieces (Terraform, SQS publishing, API Gateway integration) may not be fully implemented in code yet; the sections below are the target end state.

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
* `terraform/` — **Planned:** EC2, RDS, security groups, and IAM for this service only (once added).
* `.github/workflows/` — Build, push to ECR, and deploy (e.g. SSM-based restart on EC2).

Configuration keys for runtime (database URL, SQS queue URL, region, etc.) belong in **`environment.md`** in this directory as they are finalized.
