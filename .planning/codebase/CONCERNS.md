# Codebase Concerns

**Analysis Date:** 2026-03-31

## Tech Debt

**Exception Handling - Silent Failures:**
- Issue: Multiple locations catch exceptions too broadly or suppress errors, masking failures in production
- Files:
  - `db_to_s3_netsuite_snippet.py:75-78` - Exception caught, printed, but `final_flow_state` may be undefined
  - `flows/long_running_test.py:38-49` - Exception caught at flow level but not properly propagated
  - `testing.py:78-80` - Broad `Exception` catch with only print output
  - `flows/multiprocessing_test.py:28-30` - Catches all exceptions and returns `[None]`
  - `project_utils/helpers/deployments/reset_deployment_concurrency.py:77-79` - Catches HTTPError then all Exception
- Impact: Failed operations may silently continue execution. Errors are logged to stdout instead of proper logging. Retry logic becomes impossible.
- Fix approach: Replace broad `except Exception` with specific exception types. Use proper logging (logger.error) instead of print. Add context manager for resource cleanup.

**Uninitialized Variable References:**
- Issue: Variables referenced in except/finally blocks that may not be defined in try block
- Files: `db_to_s3_netsuite_snippet.py:78` - `final_flow_state` used in finally block but only set in try block
- Impact: UnboundLocalError at runtime if exception occurs before variable assignment
- Fix approach: Initialize `final_flow_state = None` before try block, then check in finally before returning

**Print Statements in Production Code:**
- Issue: 78 files use `print()` for debugging instead of proper logging
- Files: All 71 flows, testing utilities, helpers use print() instead of logger
- Impact: No log levels, no timestamp correlation, cannot control verbosity in production. Lost in container logs.
- Fix approach: Replace all `print()` with `get_run_logger().info()` (or .debug/.warning). Use `log_prints=True` in flow decorators only as fallback.

**Hardcoded Credentials and Sensitive Data:**
- Issue: AWS credentials, Slack tokens, API keys, and file paths hardcoded in files
- Files:
  - `flows/long_running_test.py:61` - Hardcoded Docker image ECR URI with account ID
  - `db_to_s3_netsuite_snippet.py:48,57-62` - Hardcoded vault path, bucket name, S3 keys
  - `flows/create_automation_flow.py` - Slack webhook blocks loaded by hardcoded names
  - Various flows load blocks by hardcoded names instead of config
- Impact: Credentials in git history (if not carefully managed). Environment changes require code modifications. Credential rotation breaks deployments.
- Fix approach: All credentials should come from environment variables or Prefect Cloud Secret blocks. Use deployment parameters for non-secret config.

**Commented Out Code Left in Place:**
- Issue: Large blocks of dead/test code commented but not removed
- Files:
  - `testing/dbt_runner.py:10-11, 47-69` - 20+ lines of commented tracing code
  - `flows/test.py:25-26, 50-59` - Commented rollbar integration and deployment setup
  - `db_to_s3_netsuite_snippet.py` - Multiple commented alternative approaches
  - `flows/flow_runs_with_names.py:36` - Commented exception handler
  - `misc/block_tests.py:16-30` - Dead test code
- Impact: Code is harder to read and understand. Increases maintenance burden. Makes history harder to follow.
- Fix approach: Delete all commented code. Use git history for recovery if needed. Keep issue references if code might return.

**Inconsistent Module Structure:**
- Issue: Duplicate implementations of core utilities across multiple module hierarchies
- Files:
  - `mm2/localhelpers/create_secrets.py` vs `project_utils/helpers/secrets/create_secrets.py` - 99% identical
  - `mm2/` package exists but `project_utils/` is the primary package
  - `project_utils/build/lib/` contains stale copies of helpers
- Impact: Changes to one version don't propagate. Unclear which is canonical. Build artifacts left in repo.
- Fix approach: Consolidate to single package hierarchy. Remove `mm2/` and `project_utils/build/`. Use one import path throughout codebase.

**Missing Variable Definition in Exception Path:**
- Issue: Variable may not be assigned before use in error handlers
- Files: `db_to_s3_netsuite_snippet.py:75-78`
- Impact: If exception occurs before line 47, `final_flow_state` is undefined at line 78 finally block
- Fix approach: Ensure `final_flow_state = None` before the try block

## Known Bugs

**Missing Import in block_tests.py:**
- Symptoms: `ImportError: cannot import name 'steps'`
- Files: `misc/block_tests.py:3`
- Trigger: Run the file directly
- Code: `from prefect.deployments.steps` is incomplete - should be `from prefect.deployments.steps import ...`
- Workaround: Comment out line 3 if block_tests are not needed
- Fix: Import specific functions: `from prefect.deployments.steps import git_clone` (or similar)

**Broken Jinja2 Workaround Hardcoded:**
- Symptoms: DBT models with range() calls above 100,000 will be silently truncated
- Files: `testing/dbt_runner.py:13-15`
- Trigger: Run DBT models with `range()` calls
- Root Cause: `jinja2.sandbox.MAX_RANGE = 100000` is hardcoded as a monkey-patch, not configurable
- Impact: Cannot adjust for models requiring higher ranges without code change
- Fix: Make this configurable via environment variable: `MAX_RANGE = int(os.getenv("JINJA_MAX_RANGE", "100000"))`

**Type Annotation Inconsistency:**
- Symptoms: Python 3.12 compatibility issues with mixed type hints
- Files: Multiple files use `list[Type]` and `List[Type]` interchangeably
- Impact: May cause issues with older type checkers or IDE support
- Fix: Standardize on `list[Type]` (3.9+) or ensure all files import `from typing import List`

**Undefined Variable in Exception Handler:**
- Symptoms: `UnboundLocalError` if exception occurs in try block before variable assignment
- Files: `db_to_s3_netsuite_snippet.py:75-78`
- Trigger: If `create_db_to_s3_sub_flow()` raises exception on first line
- Root Cause: `final_flow_state` assigned in try block, used in finally block
- Fix: Move assignment before try block: `final_flow_state = None`

## Security Considerations

**Credential Exposure in Code:**
- Risk: AWS credentials, database URLs, API keys embedded in source
- Files:
  - `flows/long_running_test.py:61` - AWS ECR account ID visible
  - `db_to_s3_netsuite_snippet.py:48,57-62` - Vault path and bucket names
  - Various block names that are environment-specific
- Current mitigation: `.env` file exists in `.gitignore`, but some paths/IDs still exposed
- Recommendations:
  - Ensure ALL credentials come from `PREFECT_API_KEY` or Prefect Cloud Secrets blocks
  - Move AWS account IDs to environment variables
  - Parameterize bucket names, vault paths, and deployment settings
  - Consider using AWS Secrets Manager instead of Vault for better audit trails

**Print Statements in Error Handlers:**
- Risk: Error details printed to stdout may expose sensitive data in CI/CD logs
- Files: 60+ locations with `print(f"... {e}")` in exception handlers
- Current mitigation: None
- Recommendations:
  - Never print full exception details to stdout
  - Use structured logging with redaction
  - Filter secrets from exception messages before logging

**IAM and Authentication:**
- Risk: No authentication validation on local utilities and helper scripts
- Files: `project_utils/helpers/` contains scripts that assume authenticated AWS/Prefect environment
- Current mitigation: Reliance on execution environment having proper credentials
- Recommendations:
  - Add explicit auth checks at module startup
  - Raise clear errors if required environment variables are missing
  - Document required IAM permissions in comments

**Docker Images:**
- Risk: Multiple Dockerfile variants with unclear purpose and no versioning strategy
- Files: `Dockerfile_test`, `Dockerfile_test2`, `Dockerfile_testing` all identical or similar
- Current mitigation: None - appears to be development leftovers
- Recommendations:
  - Remove test Dockerfiles or consolidate to one
  - Use version pinning for Prefect base image
  - Document which Dockerfile is canonical

## Performance Bottlenecks

**Inefficient Pagination in API Calls:**
- Problem: API pagination implemented with manual offset tracking across multiple files
- Files:
  - `testing.py:59-73` - Manual pagination with fixed offset increment
  - `project_utils/helpers/deployments/reset_deployment_concurrency.py:55-81` - Same pattern repeated
- Cause: No pagination helper, code duplicated with tight loop no backoff
- Impact: Unnecessary API calls if limit not divisible by dataset size. No retry backoff on rate limits.
- Improvement path: Create shared paginator utility, add exponential backoff, use httpx timeout settings

**Synchronous HTTP Calls in Async Context:**
- Problem: `httpx.Client` (sync) used in async functions without proper async wrapper
- Files: `testing.py`, `project_utils/helpers/` - create_client uses sync Client
- Impact: Blocking operations in async context defeat concurrency benefits
- Improvement path: Use `httpx.AsyncClient` for all async operations, or wrap sync calls with `asyncio.to_thread()`

**No Connection Pooling or Reuse:**
- Problem: New httpx.Client created per function call or request batch
- Files: `testing.py:13-36`, `reset_deployment_concurrency.py:17-42`
- Impact: Each new client creates new connections, increasing latency and resource usage
- Improvement path: Create single reusable client per module, use context manager

**Unoptimized S3 Operations:**
- Problem: S3 download/upload operations not batched, no multipart upload
- Files: `flows/multiprocessing_test.py:52-62` - Downloads files synchronously one at a time
- Impact: Linear download time for large datasets
- Improvement path: Use S3 client batch operations or concurrent downloads with boto3 transfer manager

**DBT Range Limit Hardcoded:**
- Problem: `jinja2.sandbox.MAX_RANGE = 100000` is global and non-configurable
- Files: `testing/dbt_runner.py:13-15`
- Impact: Models requiring larger ranges will silently fail
- Improvement path: Make configurable, add validation, log when limit is reached

## Fragile Areas

**Flow Definition and Deployment Coupling:**
- Files: `flows/` directory contains 71 Python files, many with inline deployment configuration
- Why fragile: Each flow defines its own deployment settings (image URI, work pool, concurrency) as code. Changes to deployment strategy require code edits and redeployment.
- Safe modification: Extract deployment config to `prefect.yaml` using unified deployment patterns
- Test coverage: Only 5 dedicated test flows in 71 files; most are examples

**Exception Handling in Async Flows:**
- Files: `flows/long_running_test.py:38-49`, `db_to_s3_netsuite_snippet.py:75-78`
- Why fragile: Mix of asyncio.CancelledError, custom exceptions, and broad Exception catches. Finally block variable references may fail.
- Safe modification: Wrap all async exception handling in helper functions with explicit type handling
- Test coverage: Gaps - cancellation behavior not tested

**API Client Initialization Pattern:**
- Files: `testing.py:13-36`, `project_utils/helpers/deployments/reset_deployment_concurrency.py:17-42`
- Why fragile: Identical code duplicated across modules. Settings dict manipulated directly. No validation.
- Safe modification: Create shared `prefect_api.py` module with `PrefectApiClient` class
- Test coverage: No tests for client initialization

**Sub-flow Error Propagation:**
- Files: `db_to_s3_netsuite_snippet.py:75-78`
- Why fragile: Exception caught, logged to print, variable may be undefined in finally
- Safe modification: Use explicit state object, initialize before try, check in finally, re-raise if needed
- Test coverage: Gaps - no tests for error cases

## Scaling Limits

**No Rate Limiting or Backoff:**
- Current capacity: Prefect API calls made in tight loops without backoff
- Limit: Will hit rate limits when processing 1000+ deployments
- Files: `reset_deployment_concurrency.py`, `testing.py` pagination loops
- Scaling path: Add exponential backoff decorator, implement queue-based rate limiting

**Async Task Concurrency Unbounded:**
- Current capacity: `gather()` used without semaphores in `db_to_s3_netsuite_snippet.py`
- Limit: May exhaust resource limits with 1000+ concurrent sub-flows
- Files: `db_to_s3_netsuite_snippet.py:23-25` - gather with generator expression, no limit
- Scaling path: Use `CoroutineThrottler` (already imported but not used in gather), add concurrency parameter

**Deployment Concurrency Loop:**
- Current capacity: While loop processes all deployments before next iteration
- Limit: If deployment list is large (1000+ items), memory usage grows linearly
- Files: `reset_deployment_concurrency.py:45-81` - concurrency_limits list extends indefinitely
- Scaling path: Process deployments in batches, implement streaming processor pattern

**HTTP Connection Pool Size:**
- Current capacity: httpx.Client uses default connection pool (10 connections)
- Limit: Will bottleneck if making 100+ concurrent requests
- Files: All files using httpx
- Scaling path: Configure pool size in httpx settings, use connection limits parameter

## Dependencies at Risk

**Websockets Version Constraint:**
- Risk: `websockets<14` in requirements.txt is overly restrictive
- Files: `requirements.txt:1`
- Impact: Blocks security updates, may conflict with other dependencies requiring newer versions
- Current state: Version 13.x used, why 14+ blocked is undocumented
- Migration plan: Test with websockets 14+, document breaking changes if any, update constraint

**Prefect Version Pinning:**
- Risk: `prefect>=3.6.4` pins relatively recent version, may miss critical updates
- Files: `pyproject.toml:9`
- Impact: Security fixes in 3.7+ won't auto-apply
- Current state: 3.6.4+ specified but no upper bound
- Migration plan: Regularly test latest 3.x versions, document breaking changes

**Unused Dependencies:**
- Risk: `numpy` imported in `mm2/localhelpers/create_secrets.py:2` but never used
- Files: `mm2/localhelpers/create_secrets.py:2`, `db_to_s3_netsuite_snippet.py` (QUOTE_ALL imported but source unclear)
- Impact: Increases attack surface, adds unnecessary size
- Migration plan: Audit imports, remove unused dependencies, use linting to catch future instances

**DBT and Datadog SDKs:**
- Risk: `dbt.cli.main` and `ddtrace` used only in testing but no error handling for missing optional deps
- Files: `testing/dbt_runner.py:6` - Imports fail if dbt not installed
- Impact: Module fails to import if dbt not available, even if dbt functionality not used
- Migration plan: Move dbt/datadog imports to function-level lazy imports with try/except

## Missing Critical Features

**No Unified Logging Configuration:**
- Problem: Mix of print(), get_run_logger(), and logging module across codebase
- Blocks: Cannot achieve consistent log levels, structured logging, or centralized log aggregation
- Current state: Each file implements logging differently
- Solution: Create `mm2/logging_config.py` with centralized logger setup, use in all flows

**No Error Recovery or Retry Logic:**
- Problem: API calls and flow operations fail without retry
- Blocks: Production resilience, cannot handle transient network failures
- Current state: Exceptions are caught but not retried
- Solution: Implement Prefect's built-in retry decorator, add exponential backoff

**No Configuration Management System:**
- Problem: Settings hardcoded in flows, duplicated across files
- Blocks: Environment-specific deployments, testing in multiple regions
- Current state: Magic strings for block names, bucket names, vault paths
- Solution: Create config module with pydantic models for each environment

**No Schema Validation for API Responses:**
- Problem: API responses parsed as dicts without validation
- Blocks: Cannot detect API contract changes, type safety lost
- Current state: `response.json()` used directly, no schema validation
- Solution: Create pydantic models for Prefect API response types, validate at call sites

**No Distributed Tracing:**
- Problem: While DDTrace is imported, tracing is commented out
- Blocks: Cannot trace requests across service boundaries
- Current state: `testing/dbt_runner.py:59-69` has tracing code but it's disabled
- Solution: Re-enable tracing, implement trace ID propagation in async flows

## Test Coverage Gaps

**No Unit Tests for Utility Functions:**
- Untested: All helper functions in `project_utils/helpers/` lack unit tests
- Files:
  - `reset_deployment_concurrency.py` - 200+ lines, no tests
  - `deployment_utils.py` - 180+ lines, no tests
  - `create_secrets.py` - 150+ lines, no tests
- Risk: Refactoring these modules is dangerous. Changes often break in production.
- Priority: HIGH - These are critical infrastructure utilities

**No Error Case Testing:**
- Untested: Exception handlers and error paths
- Files: `db_to_s3_netsuite_snippet.py:75-78`, `flows/long_running_test.py:38-49`
- Risk: Error handling bugs only surface in production
- Priority: HIGH - Silent failures in error paths are production risks

**No Integration Tests for Prefect API Calls:**
- Untested: API client creation, pagination, response parsing
- Files: `testing.py`, `reset_deployment_concurrency.py`
- Risk: API changes not caught until flows fail
- Priority: MEDIUM - Can use test workspace for integration tests

**No Async Cancellation Testing:**
- Untested: Flow cancellation behavior, CancelledError handling
- Files: `flows/long_running_test.py:38-49`, `flows/state_change_hooks.py`
- Risk: Cancellation handling may not work in production
- Priority: MEDIUM - Edge case but critical for reliability

**No Performance Benchmarks:**
- Untested: Paginator performance, sub-flow concurrency limits
- Files: All pagination code, async flows
- Risk: Performance degradation not detected until deployment
- Priority: LOW - Can implement incrementally

---

*Concerns audit: 2026-03-31*
