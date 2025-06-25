.PHONY: all ensure_tools init install_browsers test run_agents lint clean

# Default target: run everything
all: ensure_tools init install_browsers lint run_agents test

# Step 0: Ensure pip and pdm are installed
ensure_tools:
	@command -v pip >/dev/null 2>&1 || { \
		echo "❌ ERROR: pip is not installed. Please install pip first."; \
		exit 1; \
	}
	@command -v pdm >/dev/null 2>&1 || { \
		echo "📦 PDM not found. Installing with pip..."; \
		pip install --user pdm; \
		echo "✅ PDM installed."; \
		echo "👉 If 'pdm' is still not recognized, add this to your shell config:"; \
		echo '   export PATH="$$HOME/.local/bin:$$PATH"'; \
	}

# Step 1: Install dependencies
init:
	pdm install
	pdm list

# Step 2: Install Playwright browsers
# install_browsers:
# 	pdm run python -m playwright install

# Step 3: Run linter
# lint:
# 	pdm run ruff check . --fix

# Step 4: Run agents (Planner → Generator → Executor → Validator)
# run_agents:
# 	pdm run python main.py

# Step 5: Run test suite
# test:
# 	pdm run pytest

# Clean up
clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache