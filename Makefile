help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build single file executable
	pyinstaller --onefile adr/adr.py

.PHONY: install
install: ## Install ADR to /usr/bin  (run as root)
	rm -f /usr/local/bin/adr
	cp dist/adr /usr/local/bin/

.PHONY: test
test: ## Run tests with pytest
	pytest test

