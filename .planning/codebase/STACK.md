# Technology Stack

**Analysis Date:** 2026-03-31

## Languages

**Primary:**
- Python 3.12 - Core language for all flow definitions and tasks (`requires-python = ">=3.12"` in `pyproject.toml`)

## Runtime

**Environment:**
- Python 3.12 (specified in `.python-version`)

**Package Manager:**
- uv (modern Python package manager with lock file `uv.lock`)
- Lockfile: Present (`uv.lock` - 3240 lines)

## Frameworks

**Core:**
- Prefect 3.6.4+ - Workflow orchestration and task execution (`prefect[dask,docker,aws,kubernetes,shell]>=3.6.4` in `pyproject.toml`)
  - Includes built-in support for Dask, Docker, AWS, Kubernetes, and Shell task runners

**AI/ML:**
- Pydantic AI 0.4.3+ - AI agent framework with LLM integration (`pydantic-ai>=0.4.3`)
- Logfire 4.15.1+ - Structured logging and observability (`logfire>=4.15.1`)

**Testing:**
- Not detected - no test framework specified in main requirements

**Build/Dev:**
- Terraform 2.92.1 - Infrastructure as code for Prefect resources
- Docker - Containerization (multiple Dockerfile variants in `Docker_stuff/`)

## Key Dependencies

**Critical:**
- prefect 3.6.4+ - Core workflow orchestration
- pydantic-ai 0.4.3+ - AI agent execution with LLM models
- logfire 4.15.1+ - Telemetry, structured logging, and observability with Pydantic integration

**Infrastructure & Cloud:**
- aiobotocore 2.26.0 - Async AWS SDK for S3, ECS, and other services
- boto3 1.37.1+ - AWS SDK for resource management
- prefect-aws 0.5.9 - Prefect blocks and tasks for AWS integration
- prefect-docker - Docker container management
- prefect-kubernetes - Kubernetes job execution
- prefect-ray - Ray distributed computing support
- prefect-snowflake 0.28.2 - Snowflake database integration
- prefect-gitlab 0.3.1 - GitLab integration
- prefect-gcp[aiplatform] - Google Cloud Platform and Vertex AI
- prefect-shell 0.3.1 - Shell command execution

**HTTP Clients:**
- httpx - Async HTTP client for API calls (`flows/dbt_test.py`, `flows/scratch3.py`)
- requests - Synchronous HTTP client (`flows/client.py`)

**Async & Concurrency:**
- aiohttp 3.13.2+ - Async HTTP client library
- asyncio - Python's built-in async framework (used extensively)

**Data & Serialization:**
- numpy - Numerical computing (in `requirements_testing.txt`)
- websockets - WebSocket protocol support

**AWS & CLI:**
- urllib3 1.26.20 - HTTP client (pinned for compatibility)

## Configuration

**Environment:**
- Environment variables managed via `.env` file (present - do not read)
- Prefect blocks for credentials storage:
  - AWS credentials (`AwsCredentials.load("mm2-se-dev")` in `flows/test_result_persistence.py`)
  - Slack credentials (`SlackCredentials.load("slack-creds")` in `flows/message_on_failure.py`)
  - Kubernetes credentials in `testing/get_k8s_job_logs.py`

**Build:**
- `prefect.yaml` - Primary Prefect deployment config with GitHub integration
- `prefect_ecs.yaml` - ECS-specific Prefect deployment config
- `pyproject.toml` - Python project metadata and dependencies
- `uv.lock` - Dependency lock file

**Infrastructure:**
- `terraform/main.tf` - Terraform configuration for Prefect work pools, work queues, and resources (version 2.92.1)

## Platform Requirements

**Development:**
- Python 3.12+
- uv package manager
- Terraform (for infrastructure management)
- Docker (for containerized execution)

**Production:**
- AWS (ECS Fargate, EC2, S3) - primary deployment target
- Kubernetes - optional K8s worker pool support
- Prefect Cloud - remote state management and UI
- Docker - for containerized execution

---

*Stack analysis: 2026-03-31*
