.PHONY: help setup-env clean test run

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-15s %s\n", $$1, $$2}'

define load_env # Taken from https://unix.stackexchange.com/a/594401
	$(eval ENV_FILE := $(1).env)
	$(eval include $(1).env)
	$(eval export)
endef

load-env: setup-env ## load env/local-dev.env environment
	$(call load_env,)

setup-env: ## Copy .env.example to .env and replace DUMMY_PATH with current directory
	@if [ -f .env ]; then \
		echo "Warning: .env already exists. Skipping..."; \
		echo "If you want to reset, delete .env first."; \
	else \
		sed "s|DUMMY_PATH|$$(pwd)|g" .env.example > .env; \
		echo ".env file created from .env.example"; \
		echo "CWD set to $$(pwd)"; \
		echo "Removing the comments in the .env file that start with #"; \
		sed -i "s|^\([^#]\+\)[[:space:]]\+#[^#]\+$$|\1|g" .env; \
		echo "Please edit .env with your configuration."; \
	fi

test: load-env ## Run tests
	uv run pytest

# Change the app to the package name
run: load-env ## Run the application
	uv run app

clean: ## Clean build artifacts and cache
	rm -rf __pycache__ .ruff_cache .pytest_cache .mypy_cache
	rm -rf .coverage htmlcov/ tests/test_results/
	rm -rf build/ dist/ *.egg-info
	# Clean runtime directories (logs and data) but keep .gitignore files
	find logs/ -mindepth 1 ! -name '.gitignore' -delete 2>/dev/null || true
	find data/ -mindepth 1 ! -name '.gitignore' -delete 2>/dev/null || true
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
