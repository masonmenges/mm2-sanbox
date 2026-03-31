# Coding Conventions

**Analysis Date:** 2026-03-31

## Naming Patterns

**Files:**
- Snake case for all Python files: `async_ex_flow.py`, `task_caching.py`, `schema_validation.py`
- Test files use `_test.py` suffix: `joblib_test.py`, `block_tests.py`, `extra_loggers_test.py`
- Flow files grouped in `flows/` directory
- Helper/utility modules in `mm2/localhelpers/` and `mm2/projectflows/`

**Functions:**
- Snake case for all function names: `get_secrets_from_json()`, `slugify()`, `some_task()`, `test_joblib_flow()`
- Prefect decorators (`@task`, `@flow`) used consistently for async and sync functions
- `get_run_logger()` pattern used for logging access within Prefect tasks/flows

**Variables:**
- Snake case for all variables: `api_key`, `base_url`, `default_page_limit`, `concurrency_limits`
- Constants defined in UPPERCASE: `DEFAULT_PAGE_LIMIT = 100`, `DEFAULT_ACTIVE_SLOTS = 0`
- Context variables from Prefect: `get_run_context()`, `flow_run.run_count`

**Types:**
- Pydantic `BaseModel` for structured data validation: `SampleValues(BaseModel)`, `MetadataConfig(BaseModel)`
- Enums for categorical values: `AssetsToActOnEnum(enum.StrEnum)`, `SampleDropdownEnum(enum.Enum)`
- Type hints in function signatures: `api_key: str`, `client: httpx.Client`, `limit: int = DEFAULT_PAGE_LIMIT`
- Union types for optional parameters: `Union[str, None]` or modern `str | None` syntax

## Code Style

**Formatting:**
- No standardized formatter detected (no `.prettierrc`, `black` config, or `autopep8` config)
- Mixed spacing conventions observed (some files have 1 blank line between functions, others have 0)
- Line length varies across codebase (40-200+ characters observed)

**Linting:**
- No `.flake8`, `.pylintrc`, or `ruff.toml` configuration found
- No automated linting enforcement in place
- Code follows basic Python conventions but lacks strict enforcement

**Import Style:**
- Standard library imports first: `import os`, `from typing import Dict, List, Optional`
- Third-party imports grouped: `import httpx`, `from pydantic import BaseModel`, `import numpy as np`
- Prefect imports commonly used: `from prefect import flow, task, get_run_logger`
- Relative imports within modules: `from localhelpers.create_secrets import slugify`
- No barrel file pattern observed (no `__init__.py` re-exports)

## Import Organization

**Order:**
1. Standard library: `import os`, `from typing import ...`, `from pathlib import Path`
2. Third-party packages: `import httpx`, `import numpy as np`, `from pydantic import ...`
3. Prefect framework: `from prefect import flow, task, get_run_logger`, `from prefect.blocks...`
4. AWS/GCP integrations: `from prefect_aws import S3Bucket`, `from prefect_gcp.secret_manager import GcpSecret`
5. Local application imports: `from localhelpers.create_secrets import slugify`, `from misc.extra_loggers_test as foo`

**Path Aliases:**
- No path aliases (e.g., no `@` or `~` aliases) configured in `pyproject.toml`
- Relative imports use module names directly: `from localhelpers.create_secrets import slugify`

## Error Handling

**Patterns:**
- Try-except blocks wrap HTTP requests and file operations: `try: ... except FileNotFoundError`, `except httpx.HTTPError`, `except json.JSONDecodeError`
- Specific exception types caught and re-raised: `response.raise_for_status()`
- Exception logging with context: `except Exception as e: print(f"Error: {e}")`
- Prefect task retry mechanism used for transient failures: `@task(retries=2, retry_delay_seconds=2)`
- State-based error handling in flows: `raise ValueError("I'm a Failure")` within tasks triggers retries

**Prefect-specific patterns:**
- Task and flow return values indicate success/failure
- Flow state changes trigger automatic retries when `retries` parameter set
- Exception context preserved with `get_run_context()`: `context.task_run.run_count`

## Logging

**Framework:** Prefect's built-in logger via `get_run_logger()`

**Patterns:**
- Access Prefect logger in tasks/flows: `logger = get_run_logger()`
- Log at INFO level for normal flow progress: `logger.info(f"Computing {a_number} + 1")`
- Print statements allowed alongside logging: `print(f"runtime: {end - start}")`
- Custom loggers used for non-task logging: `always_output = get_logger("AlwaysOutput")`
- Prefect log handlers accessible: `prefect_logger.handlers`

## Comments

**When to Comment:**
- Docstrings used for functions with parameters and return values
- Comments explain non-obvious logic or workarounds
- Commented-out code common in flow definitions (deployment blocks)

**Docstring Style:**
```python
def get_secrets_from_json(file_path: str) -> dict:
    """
    Read secrets from a JSON file and return them as a dictionary.

    Args:
        file_path: Path to the JSON file containing secrets

    Returns:
        Dictionary containing the secrets from the JSON file
    """
```

- Functions have docstrings with Args and Returns sections
- Type information in docstrings supplements type hints
- Multi-line docstring format with empty lines between sections

## Function Design

**Size:**
- Functions range from 5-50 lines of code
- Flow definitions (`@flow`) typically 10-40 lines
- Task definitions (`@task`) typically 5-20 lines
- Utility functions (`get_secrets_from_json`, `slugify`) 10-40 lines

**Parameters:**
- Use keyword arguments for configuration: `.with_options(retries=2, retry_delay_seconds=2)`
- Optional parameters use defaults: `httpx_settings: Optional[Dict] = None`
- Prefect parameter validation via Pydantic models: `def demo_flow(configs: SampleValues = SampleValues())`

**Return Values:**
- Simple values returned from tasks: `return a_number + 1`
- None returned explicitly: `return None` or implicit
- Dictionaries returned from helper functions: `return new_keys`
- Futures/submitted tasks handled with `wait()` from `prefect.futures`

## Module Design

**Exports:**
- No explicit `__all__` definitions observed
- All top-level functions accessible for import
- Flow decorators make functions directly callable: `demo_flow()`

**Barrel Files:**
- `mm2/__init__.py` is empty (contains only newline)
- `mm2/projectflows/__init__.py` and `mm2/localhelpers/__init__.py` exist but not used for re-exports
- Direct imports from modules preferred over barrel files

## Task/Flow Patterns

**Decorators and Options:**
```python
@task(retries=2, log_prints=True)
def some_task():
    ...

@flow()
def demo_flow(configs: SampleValues = SampleValues()):
    logger = get_run_logger()
    logger.info(f"Config: {configs.date}")
    some_task()
```

- Tasks and flows defined with optional parameter decorators
- `log_prints=True` captures print output in logs
- `validate_parameters=True` enables Pydantic validation for flow parameters
- `persist_result=True` with `result_storage` for result persistence

**Task Submission and Concurrency:**
```python
data_futures = [generate.submit() for i in range(10)]
data = [f.result() for f in data_futures]
output.map(data)  # Map operation over collection
```

- `.submit()` for async task submission
- `.map()` for parallel execution over collections
- `.with_options()` for applying configuration to task calls
- `wait()` utility to wait for multiple futures

---

*Convention analysis: 2026-03-31*
