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

shell: ## Start Flask CLI shell
	FLASK_APP=app/app.py FLASK_SECRETS=config.py FLASK_DEBUG=0 FLASK_ENV=production .venv/bin/flask shell
