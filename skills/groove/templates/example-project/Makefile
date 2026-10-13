# One command for every check. CI runs `make check` and nothing else.
.PHONY: check types lint format boundaries rules glossary module-names fixtures test

BASE ?= origin/main
VAGUE_MODULE_NAMES := utils?|helpers?|common|shared|misc|core|lib|base|tools|stuff|general|extras

check: types lint format boundaries rules glossary module-names fixtures test

types:
	uv run pyright src tests

lint:
	uv run ruff check src tests

format:
	uv run ruff format --check src tests

boundaries:
	uv run lint-imports

rules:
	uv run semgrep scan --metrics=off --config semgrep.yml --error --quiet

glossary:
	@awk -f scripts/glossary-dictionary.awk GLOSSARY.md > .glossary-dictionary.txt
	@uv run codespell --dictionary .glossary-dictionary.txt --regex '[A-Z]?[a-z]+' src tests \
		|| (echo "Banned synonym found. Use the glossary term shown after '==>' (see GLOSSARY.md)."; exit 1)

module-names:
	@bad=$$(find src -name '*.py' | grep -E '/($(VAGUE_MODULE_NAMES))(/|\.py$$)'); \
	if [ -n "$$bad" ]; then \
		echo "$$bad"; \
		echo "Vague module name. Name the module after its responsibility, or move the code into the module that owns the concept."; \
		exit 1; \
	fi

fixtures:
	@changed=$$(git diff --name-only --diff-filter=MD $(BASE) -- tests/fixtures 2>/dev/null); \
	if [ -n "$$changed" ]; then \
		echo "$$changed"; \
		echo "Committed fixtures must not change. Restore them. If the shape changed, bump the record version and add a new fixture."; \
		exit 1; \
	fi

test:
	uv run pytest -q
