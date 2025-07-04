.PHONY: all ensure_tools init install_browsers test run_agents lint clean

# Default target: run everything
all: ensure_tools init

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

# Clean up
clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache

.PHONY: run
run:
	@echo "▶ Running src/main.py via PDM"
	pdm run python src/main.py

.PHONY: check-tools

# all phony targets must be declared at the left margin
.PHONY: check-tools pull-ollama-models compose-up

# verify Docker and Ollama are installed
check-tools:
	@command -v docker >/dev/null 2>&1 || { \
	  echo >&2 "Error: Docker is not installed."; \
	  exit 1; \
	}
	@command -v ollama >/dev/null 2>&1 || { \
	  echo >&2 "Error: Ollama is not installed."; \
	  exit 1; \
	}

# pull your models (depends on check-tools)
pull-ollama-models: check-tools
	@echo "✔ Ollama found—pulling models..."
	@ollama pull nomic-embed-text
	@ollama pull llama3.2

# bring up docker-compose (also depends on check-tools)
compose-up: check-tools
	@echo "📦 Bringing up containers in detached mode..."
	@docker-compose up -d