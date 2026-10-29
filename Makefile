.PHONY: install test clean help lint

.DEFAULT_GOAL := help

install: ## Install package in Editable Mode and set up development environment
		@echo "+ $@"
		@echo "Installing dotfilesrc and setting up development environment"
		@echo "----------------------------------------------------------"
		@python3 -m pip install --editable .[dev,test]

test: ## Run all tests
		@echo "+ $@"
		@echo "Running Tests"
		@echo "-------------"
		@python3 -m pytest . --cov

lint: ## Run static code analysis
		@python3 -m pylint ./dotfilesrc --output-format=colorized --fail-under=8

help:
		@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
