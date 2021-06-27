.PHONY: format help

# Help system from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Establish local environment with dependencies installed
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

up: ## Build and run the required containers by fetching binaries
	docker-compose -f docker-compose.yaml up -d

shell: ## Start Quart CLI shell
	QUART_APP=app.py QUART_SECRETS=config.py QUART_DEBUG=0 QUART_ENV=production .venv/bin/quart shell

dev: ## Start Quart development web server
	QUART_APP=app.py QUART_SECRETS=config.py QUART_DEBUG=1 QUART_ENV=development .venv/bin/quart run
