# Meaningful module names

## The rule

Every module, package, and file is named after what it is responsible for.
Vague names are banned:

`utils`, `util`, `helpers`, `helper`, `common`, `shared`, `misc`, `core`,
`lib`, `base`, `tools`, `stuff`, `general`, `extras`, and plural catch-alls
like `functions` or `classes`.

The ban is on vague names, not on technical code. A module that does one
technical job and is named for it is fine: `retry`, `pagination`, `money`,
`clock`, `slugs`. A domain module is named with a glossary term:
`invoicing`, `customers`.

When code seems shared:

1. Ask what it is about. A function formatting an invoice number belongs in
   `invoicing`, even if two modules call it. The others import it from the
   public API.
2. If it is about no domain concept, name the technical job it does and give
   it its own module (`retry`) in the layer it belongs to.
3. If you cannot name the job in one or two words, it does more than one
   thing. Split it.

Inside a module, file names follow the same rule. The layer names
`domain`, `usecases`, and `infrastructure` (see `module-layout.md`) and role
names that say what a file holds within its layer are fine: `model.py`,
`ports.py`, `fakes.py`, `records.py`. Use cases are named after their intent
(`issue_invoice.py`), adapters after what they talk to (`json_files.py`).

The small technical modules at the bottom of the layers take the place of a
`shared` package: name each for its job (`clock`, `ids`, `money`).

## Why

A vague name attracts unrelated code, because anything fits. An agent
looking for a home for a helper will pick `utils` every time it exists, and
the module grows into a dependency of everything, with no owner and no
boundary. A specific name tells an agent both where to look for code and
where not to put it.

## Example

Bad:

```python
# acme/utils.py
def format_invoice_number(n: int) -> str: ...
def retry(fn: Callable[[], T], attempts: int) -> T: ...
def slugify(text: str) -> str: ...
```

Good:

```python
# acme/invoicing/domain/model.py
def format_invoice_number(n: int) -> str: ...

# acme/retry.py
def retry[T](fn: Callable[[], T], attempts: int) -> T: ...

# acme/slugs.py
def slugify(text: str) -> str: ...
```

## Codify it

No common Python linter checks module names, so the example project's
`Makefile` does it with `find`:

```make
VAGUE_MODULE_NAMES := utils?|helpers?|common|shared|misc|core|lib|base|tools|stuff|general|extras

module-names:
	@bad=$$(find src -name '*.py' | grep -E '/($(VAGUE_MODULE_NAMES))(/|\.py$$)'); \
	if [ -n "$$bad" ]; then \
		echo "$$bad"; \
		echo "Vague module name. Name the module after its responsibility, or move the code into the module that owns the concept."; \
		exit 1; \
	fi
```

The layers contract adds a second guard: a new top-level module that is
not in a layer stands out in review, and any domain module importing it
breaks the contract if it sits in the wrong layer.

## Review by hand

- For each new module or file: can you state its responsibility in one
  sentence without "and" or "various"?
- Does a new name pass the check but still say nothing (`stuff2`, `extra`,
  `things`)? Add the pattern to `VAGUE_MODULE_NAMES`.
