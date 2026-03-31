# External Integrations

**Analysis Date:** 2026-03-31

## APIs & External Services

**LLM & AI:**
- Anthropic Claude (Claude Sonnet 4.5) - LLM backend for Pydantic AI agents
  - Used in: `testing/dbtcloudrun.py` (model: `anthropic:claude-sonnet-4-5-20250929`)
  - SDK/Client: pydantic-ai>=0.4.3
  - Auth: Environment variable (API key required)

**dbt Cloud:**
- dbt Cloud API v2 - Data transformation job orchestration
  - Used in: `flows/dbt_test.py`
  - Client: AsyncClient (httpx) with Bearer token auth
  - Endpoint: `https://cloud.getdbt.com/api/v2/accounts/{account_id}`
  - Auth: `dbt-cloud-api-key` environment variable

**Git & Source Control:**
- GitHub - Repository hosting and code deployment
  - Repository: `https://github.com/masonmenges/mm2-sanbox.git`
  - Used in: Multiple deployment configs (`flows/deploy.py`, `flows/deployment_con_test.py`, etc.)
  - Integration: Prefect GitRepository for code cloning and deployment

## Data Storage

**Databases:**
- Snowflake - Primary data warehouse
  - Connection: Environment configured via Prefect block
  - Client: prefect-snowflake 0.28.2
  - Used for: Analytics and data transformation

- PostgreSQL - Database support available (not actively configured in main flows)
  - Client: sqlalchemy/psycopg2 (via Prefect blocks)

**File Storage:**
- AWS S3 - Cloud object storage for data and results
  - SDK: boto3 1.37.1, aiobotocore 2.26.0
  - Credentials: AwsCredentials block (`"mm2-se-dev"`)
  - Used in: `flows/test_result_persistence.py`, data pipeline flows (Netsuite example in `db_to_s3_netsuite_snippet.py`)
  - Region: us-east-2 (from `prefect_ecs.yaml`)
  - Bucket naming: Environment-dependent via variables

**Caching:**
- DuckDB - Embedded database/caching (used in `flows/many_submitted_tasks.py`)
- Redis - Caching support available via logfire instrumentation (not actively used)

## Authentication & Identity

**Auth Provider:**
- Custom Prefect-managed authentication
  - Implementation: Prefect Cloud API key-based auth
  - Stored in: Environment variables and Prefect block storage

**Credentials Management:**
- Prefect Blocks system for credential storage:
  - AWS credentials (`AwsCredentials` blocks)
  - Slack credentials (`SlackCredentials` blocks)
  - Kubernetes credentials (`KubernetesCredentials` blocks)
  - Example: `SlackWebhook.load("python-slack-test")` in `flows/gcl_test.py`

## Monitoring & Observability

**Error Tracking:**
- Logfire (4.15.1+) - Structured logging, telemetry, and observability
  - Pydantic AI instrumentation: `logfire.instrument_pydantic_ai()`
  - Configuration: `logfire.configure(send_to_logfire=False, console=logfire.ConsoleOptions(verbose=True))` in `testing/dbtcloudrun.py`
  - Can send to Logfire cloud or local console

**Logs:**
- Prefect native logging - `get_run_logger()` for structured flow/task logs
- Custom logging configured via `misc/logging.yml`
- Logfire with OpenTelemetry instrumentation for database and service calls

**State Change Hooks:**
- Prefect state change events trigger custom notifications
- Used in: `flows/state_change_hooks.py` for flow failure/cancellation handling

## CI/CD & Deployment

**Hosting:**
- AWS ECS Fargate (primary) - Containerized task execution
  - Task definition: `arn:aws:ecs:us-east-2:455346737763:task-definition/prefect_mm2_flows:10`
  - Configured in: `prefect_ecs.yaml`

- AWS EC2 (secondary) - Traditional VM-based execution
  - VPC: `vpc-086b1157dc92f4caa`
  - Subnets configured: `subnet-086047cb7d869c59b`, `subnet-05e1c283c2fadbb3b`
  - Security group: `sg-0d0a2c52d51e12bf4`

- Kubernetes (optional) - K8s cluster deployment support
  - SDK: prefect-kubernetes
  - Used in: `testing/get_k8s_job_logs.py`

- Local Worker Pools - Development/testing execution
  - Work pool: `local-worker-test` and `ecs-test-pool`

**CI Pipeline:**
- Prefect Cloud deployment automation
  - Managed via: `prefect.yaml` and `prefect_ecs.yaml`
  - Git-based source control: GitHub repository cloning
  - Build steps: Shell script for commit hash generation

**Infrastructure as Code:**
- Terraform (v2.92.1) - Prefect resource provisioning
  - Provider: prefecthq/prefect (v2.92.1)
  - Manages: Work pools, work queues, Prefect account/workspace configuration
  - State: Local (configurable)

## Environment Configuration

**Required env vars:**
- `PREFECT_API_URL` - Prefect cloud API endpoint
- `PREFECT_API_KEY` - Prefect Cloud authentication (from Terraform)
- `PREFECT_ACCOUNT_ID` - Prefect account ID (from Terraform)
- `CONCURRENCY_LIMIT_NAME` - Concurrency limit resource name (default: "local")
- `REFRESH_CACHE` - Cache refresh flag for task caching (flows/task_caching.py)
- `TEST_ENV_VAR` - Test environment variable (flows/dynamic_task_runner.py)
- `GITHUB_SHA` - Git commit SHA for deployment tracking

**Secrets location:**
- Prefect Blocks (stored in Prefect Cloud)
- `.env` file (local development - never committed)

## Webhooks & Callbacks

**Incoming:**
- Prefect custom events - External event emission for flow triggers
  - Pattern: `mm2_custom_event_id_*` and `mm2_custom_event_id2_*`
  - Used in: `prefect.yaml` deployment triggers (compound event triggers with 360s window)

- Prefect state change hooks - Callbacks for flow/task state transitions
  - Cancellation hooks in: `flows/dbt_test.py` with `on_canellation` parameter
  - State monitoring in: `flows/state_change_hooks.py`, `flows/message_on_failure.py`

**Outgoing:**
- Slack notifications - Failure/completion alerts
  - Service: Slack (via prefect-slack)
  - Credentials block: `SlackCredentials.load("slack-creds")`
  - Webhook alternative: `SlackWebhook.load("python-slack-test")`
  - Used in: `flows/message_on_failure.py`, `flows/gcl_test.py`

- Prefect Cloud webhooks - Event emission for external systems
  - API: `PREFECT_API_URL` base endpoint

## Rate Limiting & Concurrency

**Prefect Concurrency:**
- Named concurrency limits (e.g., "local" work pool)
- Concurrency limit example: `limit: 1, collision_strategy: CANCEL_NEW` in `prefect.yaml`
- Rate limiting: `prefect.concurrency.sync.rate_limit` (in `flows/rate_limit_ex.py`)

## Data Transformation & Processing

**ETL Integration:**
- Netsuite ERP system - Data extraction and migration
  - Pattern: `db_to_s3_netsuite_snippet.py` with database-to-S3 flows
  - Process: Extract from Netsuite database, transform, load to S3
  - CSV output with configurable format (delimiter, encoding, quote style)

## Distributed Computing

**Task Runners:**
- Dask - Distributed task execution (`prefect[dask]`)
  - Used in: `flows/dask_runner_ex.py`
  - Config: `dask-cluster.yaml` template in `misc/`

- Ray - Distributed computing framework
  - SDK: prefect-ray
  - Used in: `ray_testing/flow.py`

- Process Pool - CPU-bound parallel execution
  - Used in: `db_to_s3_netsuite_snippet.py` for multiprocessing

---

*Integration audit: 2026-03-31*
