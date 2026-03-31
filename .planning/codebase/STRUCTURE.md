# Codebase Structure

**Analysis Date:** 2026-03-31

## Directory Layout

```
mm2-sanbox/
├── flows/                          # Primary flow definitions and examples
│   ├── background_tasks/          # Background task implementations
│   └── flow_utils/                # Flow utility functions and helpers
├── mm2/                           # Main package directory
│   ├── projectflows/              # Project-specific flow implementations
│   └── localhelpers/              # Local helper utilities
├── project_utils/                 # Utilities and operational helpers
│   └── helpers/                   # Helpers organized by function
│       ├── automations/           # Automation-related utilities
│       ├── deployments/           # Deployment utilities
│       ├── events/                # Event handling utilities
│       ├── permissions/           # Permission management utilities
│       └── secrets/               # Secret management utilities
├── assets/                        # Asset definitions and configurations
├── agent_testing/                 # Agent testing experiments
├── testing/                       # Integration and manual testing
├── ray_testing/                   # Ray-specific testing
├── misc/                          # Miscellaneous configurations and test files
├── Docker_stuff/                  # Docker-related files and templates
├── terraform/                     # Terraform infrastructure as code
├── legacy_prefect/                # Legacy Prefect 2.x code (deprecated)
├── prefect.yaml                   # Prefect Cloud deployment configuration
├── requirements.txt               # Python dependencies
└── pyproject.toml                 # Project metadata (if present)
```

## Directory Purposes

**flows/:**
- Purpose: Core workflow definitions using Prefect framework
- Contains: Flow functions (@flow decorated), task functions (@task decorated), deployment examples, execution tests
- Key files: `async_ex_flow.py`, `basic_flow.py`, `concurrency.py`, `demo.py`, `task_caching.py`, `deploy.py`

**flows/background_tasks/:**
- Purpose: Long-running background task implementations
- Contains: Standalone task definitions for background execution
- Key files: `delayed_task.py` (serves background task)

**flows/flow_utils/:**
- Purpose: Utility functions for flow deployment and configuration
- Contains: Deployment step functions, configuration helpers
- Key files: `deployment_steps.py` (sets environment variables for deployment)

**mm2/:**
- Purpose: Main package module for project-specific functionality
- Contains: Package initialization, project flows, local helpers
- Key files: `__init__.py` (empty package marker)

**mm2/projectflows/:**
- Purpose: Domain-specific flow definitions at package level
- Contains: Flows for cloud resource management, secret handling
- Key files: `manage_secrets.py` (creates Prefect Cloud secrets)

**mm2/localhelpers/:**
- Purpose: Local utility functions used by project flows
- Contains: Helper functions for slugification, secret operations
- Key files: `create_secrets.py` (Prefect Cloud 2+ secret creation utilities)

**project_utils/helpers/:**
- Purpose: Reusable operational utilities for Prefect Cloud management
- Contains: API clients, state management, secret management, deployment utilities
- Key files: `flow_run_utils.py`, `change_run_states.py`, helper modules by function

**project_utils/helpers/automations/:**
- Purpose: Automation search and management
- Contains: Functions to query and manage Prefect automations
- Key files: `get_automations.py`

**project_utils/helpers/deployments/:**
- Purpose: Deployment management utilities
- Contains: Deployment utilities, concurrency management
- Key files: `deployment_utils.py`, `reset_deployment_concurrency.py`

**project_utils/helpers/events/:**
- Purpose: Event subscription and streaming
- Contains: Event subscriber implementations
- Key files: `stream_events.py` (subscribes to Prefect flow-run events)

**project_utils/helpers/permissions/:**
- Purpose: Service account and permissions management
- Contains: RBAC utilities for Prefect workspace
- Key files: `permissions_management.py`, `update_sa_roles.py`

**project_utils/helpers/secrets/:**
- Purpose: Secret creation and management
- Contains: Prefect Cloud secret block creation utilities
- Key files: `create_secrets.py` (identical to mm2/localhelpers/create_secrets.py)

**assets/:**
- Purpose: Asset definitions and flow examples
- Contains: Example flows, custom block definitions, Pydantic models for configuration
- Key files: `assets.py`, `main_flow.py`

**agent_testing/:**
- Purpose: Agent/AI-based testing experiments
- Contains: Local server implementations, agent response handling
- Key files: `response_agent.py`, `local_server.py`

**testing/:**
- Purpose: Integration testing and manual test flows
- Contains: DBT runner, K8s testing, Prefect Cloud integration tests
- Key files: `dbt_runner.py`, `get_k8s_job_logs.py`, `flows.py`

**ray_testing/:**
- Purpose: Ray distributed computing testing
- Contains: Ray cluster examples and utilities
- Key files: `flow.py`, `ray_utils.py`

**misc/:**
- Purpose: Miscellaneous configuration and test files
- Contains: Prefect YAML configurations, JSON test files, logging configurations
- Key files: `prefect.yaml` (backup deployment config), `logging.yml`, test JSON files

**Docker_stuff/:**
- Purpose: Docker image building and deployment templates
- Contains: Dockerfile variants for different execution environments, ECS task definitions
- Key files: `Dockerfile_worker`, `ecs_worker_task_def.json`

**terraform/:**
- Purpose: Infrastructure as code for deployment targets
- Contains: Terraform configurations for work pools, deployment patterns
- Key files: `main.tf`, `workpools/` directory

**legacy_prefect/:**
- Purpose: Deprecated Prefect 2.x code (for historical reference)
- Contains: Old flow implementations no longer in use
- Key files: `basic_flow.py` and other legacy flows

## Key File Locations

**Entry Points:**
- `hello.py`: Simple "Hello from mm2-sanbox!" main entry point
- `flows/deploy.py`: Deployment configuration and serving example
- `flows/demo.py`: Example flow with typed parameters and retry logic
- `mm2/projectflows/manage_secrets.py`: Package-level secret management entry point

**Configuration:**
- `prefect.yaml`: Primary Prefect Cloud deployment manifest with schedules, triggers, work pools
- `misc/prefect.yaml`: Backup deployment configuration
- `misc/logging.yml`: Logging configuration for deployments
- `requirements.txt`: Python package dependencies
- `.python-version`: Python version specification (3.0 or similar)

**Core Logic:**
- `flows/concurrency.py`: Concurrency patterns with asyncio and ProcessPoolTaskRunner
- `flows/task_caching.py`: Result persistence and cache policy examples
- `flows/async_ex_flow.py`: Async task execution with asyncio patterns
- `project_utils/helpers/change_run_states.py`: Flow run state management and rate limit utilities
- `project_utils/helpers/flow_run_utils.py`: Flow run querying and state manipulation
- `mm2/localhelpers/create_secrets.py`: Prefect Cloud secret block creation

**Testing:**
- `testing/dbt_runner.py`: DBT orchestration integration
- `testing/flows.py`: Manual test flows
- `ray_testing/flow.py`: Ray-based distributed flow examples

## Naming Conventions

**Files:**
- Flow definition files: `{name}_flow.py` or `{verb}_{subject}.py` (e.g., `demo.py`, `task_caching.py`, `create_automation_flow.py`)
- Test/example files: `{feature}_test.py` or `{feature}_ex.py` (e.g., `block_tests.py`, `ray_concurrency_ex.py`)
- Utility files: `{verb}_{noun}.py` or `{noun}_utils.py` (e.g., `change_run_states.py`, `get_automations.py`)

**Directories:**
- Flow directory: lowercase `flows/`
- Utility directories: lowercase plural (automations, deployments, events, permissions, secrets)
- Package directory: lowercase (mm2, project_utils)
- Test/experiment directories: lowercase with purpose suffix (agent_testing, ray_testing)

**Functions/Classes:**
- Flow functions: lowercase with underscores (demo_flow, create_secrets_flow)
- Task functions: lowercase with underscores (some_task, generate, output)
- Helper functions: lowercase with underscores (get_flow_runs_from_deployment, slugify)
- Pydantic models: PascalCase (SampleValues, AssetsToActOnEnum)
- Enums: PascalCase suffix with Enum (AssetsToActOnEnum, SampleDropdownEnum)

## Where to Add New Code

**New Flow:**
- Primary code: `flows/{purpose}_{subject}.py` (e.g., `flows/sync_data_flow.py`)
- Tests/examples: `flows/{purpose}_test.py` or `testing/flows.py`
- Deployment config: Add entry to `prefect.yaml` deployments section with entrypoint

**New Helper Module:**
- Implementation: `project_utils/helpers/{category}/{function_name}.py` (follow existing pattern)
- Examples: Automations in `project_utils/helpers/automations/`, deployments in `project_utils/helpers/deployments/`

**New Utility Function:**
- Shared utilities: `project_utils/helpers/{category}/` based on purpose (automations, deployments, events, permissions, secrets)
- Local helpers: `mm2/localhelpers/{module_name}.py` for package-specific utilities

**Configuration/Data:**
- Flow configuration models: `assets/` directory using Pydantic BaseModel
- Deployment configuration: Update `prefect.yaml` or add to `misc/` for backups
- Environment files: Use `.env` (not committed) or environment variables in deployment

**Tests:**
- Integration tests: `testing/{feature}_test.py`
- Experimental code: `{domain}_testing/{experiment}.py` (e.g., `agent_testing/`, `ray_testing/`)

## Special Directories

**flows/__pycache__/:**
- Purpose: Python compiled bytecode cache
- Generated: Yes (automatic)
- Committed: No (in .gitignore)

**project_utils/build/:**
- Purpose: Python package build artifacts
- Generated: Yes (from setup.py/pyproject.toml)
- Committed: No (in .gitignore)

**dist/:**
- Purpose: Built distribution packages (wheels, tarballs)
- Generated: Yes (from python setup.py sdist bdist_wheel)
- Committed: No (in .gitignore)

**~/:**
- Purpose: Backup/reference directory containing nested Repos structure
- Generated: Unknown (appears to be artifact)
- Committed: No

---

*Structure analysis: 2026-03-31*
