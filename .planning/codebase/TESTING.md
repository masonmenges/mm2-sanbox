# Testing Patterns

**Analysis Date:** 2026-03-31

## Test Framework

**Runner:**
- pytest (implied by `@pytest.fixture` and test file patterns)
- Prefect's built-in test harness: `prefect_test_harness()` from `prefect.testing.utilities`
- `.pytest_cache` directory present at `/Users/masonmenges/Repos/git_hub_repos/mm2-sanbox/.pytest_cache`

**Assertion Library:**
- Python's built-in `assert` statements

**Run Commands:**
```bash
pytest flows/joblib_test.py              # Run specific test file
pytest --co -q                            # List tests (estimated usage)
```

No `pytest.ini` or setup.cfg configuration file found. No standardized test runner commands documented in codebase.

## Test File Organization

**Location:**
- Co-located in same directory as source code
- Test files placed directly in `flows/` directory alongside flow definitions
- No separate `tests/` directory

**Naming:**
- Suffix pattern: `*_test.py`
- Examples: `joblib_test.py`, `block_tests.py`, `extra_loggers_test.py`, `gcl_test.py`, `dbt_test.py`
- Functions named `test_*`: `test_joblib_flow()`, `test_flow()`, `test_webhook()`

**Structure:**
```
flows/
├── joblib_test.py          # Test for joblib integration
├── block_tests.py          # Tests for Prefect blocks
├── schema_validation.py     # Contains test_flow() function
└── [other flow files]
```

## Test Structure

**Suite Organization:**

```python
import pytest
from prefect.testing.utilities import prefect_test_harness
from prefect.blocks.system import Secret

@pytest.fixture(scope="session")
def prefect():
    """Create test harness with pre-configured blocks"""
    ch_block = Secret(value="clickhouse-reader")
    with prefect_test_harness() as harness:
        ch_block.save("clickhouse-reader")
        ch_block.save("clickhouse")
        yield harness

def test_joblib_flow(prefect):
    """Test function with harness fixture"""
    secret = Secret.load("clickhouse-reader")
    assert secret.get() == "clickhouse-reader"
```

**Patterns:**
- Fixtures use `scope="session"` for one-time setup
- `prefect_test_harness()` context manager wraps test execution
- Fixtures yield harness to tests: `yield harness`
- Test functions accept fixture as parameter: `def test_joblib_flow(prefect):`

## Prefect Test Harness Pattern

**Core Usage:**

```python
with prefect_test_harness() as harness:
    # Set up blocks
    block_instance.save("block-name")

    # Run assertions/tests
    loaded_block = BlockType.load("block-name")
    assert loaded_block.get() == expected_value
```

**What the harness provides:**
- Isolated environment for block operations
- In-memory block registry (no persistence to remote)
- Simulated Prefect Cloud operations
- Automatic cleanup after context exit

## Mocking

**Framework:** Pytest fixtures for dependency injection

**Patterns:**
```python
@pytest.fixture(scope="session")
def prefect():
    """Fixture providing test harness"""
    ch_block = Secret(value="clickhouse-reader")
    with prefect_test_harness() as harness:
        ch_block.save("clickhouse-reader")
        yield harness
```

**What to Mock:**
- Prefect blocks (Secret, S3Bucket, etc.) via `prefect_test_harness()`
- External API calls via manual try-except in tests
- Block loading via harness-provided registry

**What NOT to Mock:**
- Core Prefect functions (`get_run_logger()`, `get_run_context()`)
- Flow/task decorators
- HTTP client behavior (test with real harness)

## Fixtures and Factories

**Test Data:**

```python
@pytest.fixture(scope="session")
def prefect():
    ch_block = Secret(value="clickhouse-reader")
    with prefect_test_harness() as harness:
        ch_block.save("clickhouse-reader")
        ch_block.save("clickhouse")
        yield harness
```

**Location:**
- Fixtures defined in test files themselves (co-located)
- No separate `conftest.py` or fixture libraries detected
- No factory pattern for test data generation

**Block Creation Pattern:**
```python
# In tests
block_instance = BlockType(setting_1="value")
block_instance.save("block-name")

# Later retrieval
loaded = BlockType.load("block-name")
```

## Coverage

**Requirements:** Not enforced

- No coverage configuration found (no `pytest.ini` or coverage plugin)
- No minimum coverage threshold documented
- Coverage checking not part of CI/test process

**View Coverage:**
```bash
pytest --cov=flows --cov=mm2           # Estimated command (not configured)
```

## Test Types

**Unit Tests:**
- Scope: Individual task or utility function
- Approach: Direct function call with assertions
- Example: `test_joblib_flow()` tests Secret.load() and .get()
- Framework: Prefect test harness for block isolation

**Integration Tests:**
- Not explicitly separated from unit tests
- Inline deployment tests (commented-out code in source): `demo_flow.from_source(...).deploy(...)`
- Tests run against actual Prefect Cloud when deployed

**E2E Tests:**
- Not detected in codebase
- Deployments tested manually via `flows/*.py` run-if-main blocks
- No dedicated E2E framework (e.g., Playwright, Cypress)

## Async Testing

**Pattern:**
```python
# Flows are async-aware via Prefect
@flow
async def sub_flow(input: str):
    output(input)
    data_futures = [generate.submit() for i in range(10)]
    data = [f.result() for f in data_futures]
    output.map(data)
```

- Async flows defined with `async def` decorator
- Tests run via `asyncio.run()` at module level when needed
- Prefect handles async execution internally
- No explicit `pytest-asyncio` configuration detected

**Example from codebase:**
```python
# flows/async_ex_flow.py
asyncio.run(sub_flow("I'm a Flow"))

# flows/concurrency.py
if __name__ == "__main__":
    asyncio.run(con_flow())
```

## Test Execution Patterns

**Direct Execution:**
```python
# In module if __name__ == "__main__"
if __name__ == "__main__":
    test_flow.serve(name="schema_validation_ui_test")
    # or
    demo_flow()
```

- Flows executed directly via `if __name__ == "__main__"` blocks
- Test flows served with `.serve()` for interactive testing
- Regular flows run directly for local testing

**Deployment Testing:**
```python
# Commented in source but shows test pattern
demo_flow.from_source(
    source=GitRepository(url="..."),
    entrypoint="flows/demo.py:demo_flow"
).deploy(
    name="test_deployment",
    work_pool_name="test_pool"
)
```

- Deployments tested via Git source with specific entrypoints
- Work pool targets vary (k8s-minikube-test, demo_eks)
- Image specification for containerized testing

## Common Testing Scenarios

**Block Loading and Saving:**
```python
class MyBlock(Block):
    setting_1: str = "foo"

blk1 = MyBlock(setting_1="bar")
blk1.save("a-block")

blk3 = MyBlock.load("a-block")
assert blk3.setting_1 == "bar"
```

**Schema Validation:**
```python
class SampleValues(BaseModel):
    date: datetime.datetime
    dropdown: SampleDropdownEnum

@flow(validate_parameters=True)
def test_flow(input: SampleValues = {...}):
    logger.info(f"Data: {input}")
```

- Pydantic models define parameter schemas
- Flow validation via `validate_parameters=True`
- Deployment generates OpenAPI schema

**Deployment Testing:**
```python
# Test flow with multiple task runners
@flow(name="Concurrency_Test_flow_2", retries=4, task_runner=ProcessPoolTaskRunner)
async def con_flow(max_n: int = 25, failure: bool = False):
    # Test with failure injection
    if failure:
        raise Exception("Test failure")
```

- Failure injection via parameters
- Task runner configurations tested
- Retry behavior verified by intentional failures

## Test Utilities

**Prefect-Specific:**
- `prefect_test_harness()`: Isolated test environment
- `get_run_context()`: Access task/flow context in tests
- `get_run_logger()`: Logger for test output capture
- Block `.save()` and `.load()`: Harness persistence operations

**Standard Testing Libraries:**
- `pytest`: Test runner and fixtures
- Python `assert`: Built-in assertions
- `asyncio.run()`: Async test execution

---

*Testing analysis: 2026-03-31*
