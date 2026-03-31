# Check for uv installation
check-uv:
    #!/usr/bin/env sh
    if ! command -v uv >/dev/null 2>&1; then
        echo "uv is not installed or not found in expected locations."
        case "$(uname)" in
            "Darwin")
                echo "To install uv on macOS, run one of:"
                echo "• brew install uv"
                echo "• curl -LsSf https://astral.sh/uv/install.sh | sh"
                ;;
            "Linux")
                echo "To install uv, run:"
                echo "• curl -LsSf https://astral.sh/uv/install.sh | sh"
                ;;
            *)
                echo "To install uv, visit: https://github.com/astral-sh/uv"
                ;;
        esac
        exit 1
    fi

# Get set up as a new developer
setup: check-uv
    uv sync
    uv run pre-commit install

# Run linting
lint:
    uv run --frozen ruff check --fix

# Run type checker
typecheck:
    uv run --frozen ty check

# Run formatter
format:
    uv run --frozen ruff format

# Run all pre-commit checks locally (matches CI exactly)
check:
    @echo "Running ruff check..."
    uv run --frozen ruff check --exit-non-zero-on-fix
    @echo "Running ruff format..."
    uv run --frozen ruff format
    @echo "Running type check..."
    uv run --frozen ty check
    @echo "All checks passed!"

# Deploy all examples to Prefect Cloud
deploy:
    uv run --frozen prefect --no-prompt deploy --all

# Run an example locally (e.g. just run examples/01_basic_flow.py)
run file:
    uv run python {{file}}
