# Architecture

**Analysis Date:** 2026-03-31

## Pattern Overview

**Overall:** Prefect Flow-Based Workflow Orchestration with Modular Helpers

**Key Characteristics:**
- Flow and task composition using Prefect framework for distributed workflow execution
- Asynchronous and concurrent task execution patterns with multiple task runners (ProcessPool, Dask, Ray)
- Separation of workflow definitions from utility/helper functions
- Cloud-native design with support for remote deployments (Kubernetes, ECS)
- Event-driven automation with Prefect Cloud integration
- Result persistence and caching strategies for long-running computations

## Layers

**Flow Layer:**
- Purpose: Define workflow orchestration using Prefect @flow and @task decorators
- Location: `flows/` directory
- Contains: Flow definitions, task definitions, deployment configurations, execution examples
- Depends on: Prefect SDK, external services (AWS, Slack, DBT), helper utilities
- Used by: Direct execution, Prefect Cloud deployments, API webhooks

**Helper/Utility Layer:**
- Purpose: Provide reusable functions for Prefect Cloud API interaction, secret management, and operational utilities
- Location: `project_utils/helpers/` and `mm2/localhelpers/`
- Contains: API clients, state management, secret creation, event handling, deployment utilities
- Depends on: Prefect settings/client, httpx/requests for API communication
- Used by: Flow layer, scripts, deployment automation

**Project-Level Flows:**
- Purpose: Domain-specific flows and secrets management at package level
- Location: `mm2/projectflows/`
- Contains: Create secrets flows, configuration-specific workflows
- Depends on: Local helpers, Prefect decorators
- Used by: Package initialization, specific deployment contexts

**Assets & Configuration:**
- Purpose: Store flow definitions, asset definitions, and configuration blocks
- Location: `assets/`, `misc/` (configuration files)
- Contains: Pydantic models for typed flow parameters, Prefect deployment YAML, test configurations
- Depends on: Pydantic, Prefect schemas
- Used by: Flows for typed parameters and configuration

## Data Flow

**Basic Flow Execution:**
1. Flow is defined with @flow decorator in `flows/{name}.py`
2. Flow may contain @task functions that execute in parallel/serial
3. Flow is invoked either locally (asyncio.run) or deployed to Prefect Cloud
4. Tasks execute with configured concurrency, caching, retries based on @task options
5. Results are optionally persisted to S3 or cached based on cache_policy

**Cloud Deployment Flow:**
1. Flow source is git repository (`GitRepository` in `flows/deploy.py`)
2. Deployment configuration defined in `prefect.yaml` specifies entrypoint, schedules, triggers
3. Prefect Cloud pulls code from git, executes tasks in work pool
4. State transitions trigger automations and events via Prefect Cloud API
5. Results stored according to `result_storage` configuration

**Event-Driven Execution:**
1. Custom events emitted via `prefect.events.emit_event()` in flows
2. Automations listen for event patterns (e.g., "mm2_custom_event_id_*" in `prefect.yaml`)
3. Automation triggers deployment run with event data as parameters
4. Event streaming available via `PrefectEventSubscriber` in `project_utils/helpers/events/`

**State Management Flow:**
1. Flow run states transition through Prefect state machine (Pending→Running→Completed/Failed)
2. State transitions trigger state change hooks for notifications
3. Utilities in `project_utils/helpers/change_run_states.py` allow manual state manipulation
4. API rate limits tracked and monitored via helper functions

## Key Abstractions

**Flow Abstraction:**
- Purpose: Represents a unit of work with multiple tasks
- Examples: `flows/demo.py`, `flows/concurrency.py`, `flows/task_caching.py`
- Pattern: Decorated async or sync function with @flow, contains @task calls

**Task Abstraction:**
- Purpose: Represents a single unit of work with retry/cache/concurrency configuration
- Examples: Task definitions across all flow files
- Pattern: Decorated async or sync function with @task, with configuration options (retries, cache_policy, refresh_cache)

**Deployment Abstraction:**
- Purpose: Configure flow for cloud execution with scheduling, concurrency, and triggers
- Examples: `prefect.yaml` deployments section, `flows/deploy.py`
- Pattern: Flow.from_source() + .to_deployment() with work pool, schedules, triggers

**Helper Client Pattern:**
- Purpose: Encapsulate Prefect API interactions
- Examples: `create_client()` in `project_utils/helpers/change_run_states.py`
- Pattern: Factory function creating httpx.Client with authentication, used for API calls

**Result Storage Abstraction:**
- Purpose: Persist flow/task results to external storage
- Examples: S3Bucket block in `flows/task_caching.py`
- Pattern: Load block by name, assign to flow via result_storage parameter

## Entry Points

**Local Flow Execution:**
- Location: `flows/{name}.py` with `if __name__ == "__main__"` block
- Triggers: Direct Python script execution (python flows/demo.py)
- Responsibilities: Demonstrate flow execution locally, test flow logic, serve for local deployment

**Cloud Deployment Entry:**
- Location: `prefect.yaml` deployments section
- Triggers: Prefect Cloud via schedule, trigger, API call, or manual run
- Responsibilities: Execute flow on remote worker pool, manage state transitions, emit events

**Webhook/Event Entry:**
- Location: Prefect Cloud hooks configured in flow files and deployment configurations
- Triggers: External service events (e.g., Fivetran connector events in `flows/client.py`)
- Responsibilities: Ingest webhook payloads, trigger associated automations

**Package Scripts:**
- Location: Root-level Python files (hello.py, extract_ids.py) and helper scripts
- Triggers: Direct execution or import by other modules
- Responsibilities: Provide utility functions, demonstrate package usage

## Error Handling

**Strategy:** Task-level retries with Prefect configuration, flow-level state validation

**Patterns:**
- Task retries configured via @task(retries=N, retry_delay_seconds=M) decorator
- Flow failure triggers Slack notifications via `prefect_slack` integration in `flows/message_on_failure.py`
- State change hooks in `flows/state_change_hooks.py` monitor flow state transitions and trigger custom logic
- HTTP exceptions (raise_for_status) used for API calls in helper functions
- Manual exception raising in tasks for test failure scenarios (e.g., `flows/concurrency.py` raises after success)

## Cross-Cutting Concerns

**Logging:**
- Prefect's get_run_logger() provides structured logging in tasks/flows
- Custom loggers configured via logging.yml in deployment contexts
- Task execution context accessible via get_run_context() for runtime information

**Validation:**
- Pydantic models used for typed flow parameters (SampleValues in flows/demo.py)
- Configuration validation via BaseModel fields with defaults and type hints

**Authentication:**
- Prefect credentials loaded from blocks (SlackWebhook.load(), S3Bucket.load())
- API authentication via PREFECT_API_KEY and PREFECT_API_URL settings
- Git credentials for source repositories via GitCredentials in deployments

---

*Architecture analysis: 2026-03-31*
