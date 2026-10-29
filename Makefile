PYTHON ?= python3
DB     ?= shiori.db
OUT    ?= shiori-export.html

.DEFAULT_GOAL := help

## help: print this help message
.PHONY: help
help:
	@echo 'usage: make <target>'
	@echo
	@echo '  where <target> is one of the following:'
	@echo
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' | sed -e 's/^/ /'

.PHONY: needs-python
needs-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo >&2 "$(PYTHON) is required but it's not installed. Aborting."; exit 1; }

## export: export with tags
.PHONY: export
export: needs-python
	$(PYTHON) shiori2netscape.py $(DB) $(OUT)

## export-no-tags: export without tags
.PHONY: export-no-tags
export-no-tags: needs-python
	$(PYTHON) shiori2netscape.py --no-tags $(DB) $(OUT)

## clean: remove generated files
.PHONY: clean
clean:
	rm -f $(OUT)
