# Versioned persistent data

## The rule

Persistent data is anything written now and read back later by code that may
have changed in between: files, documents, JSON columns, cached blobs,
events, and queue messages. In-memory types are not persistent data, even if
they are dataclasses.

- **Records, not domain types.** Each persisted shape has a record
  representation, separate from the domain type, with conversion functions
  `to_record` and `from_record`.
- **Version field.** Every record carries an integer `version` at the top
  level, starting at 1.
- **Bump on every shape change.** Adding, removing, renaming, or retyping a
  field, or changing what a value means, bumps the version.
- **Tightening is a shape change.** Making a field required, or narrowing
  its type, writes nothing new, but records written before may not satisfy
  it. Either migrate old records to the new shape (a version bump with a
  migration step that fills the field), or show that every stored record
  already satisfies it, record that evidence in the pull request, and add a
  fixture of the oldest realistic record so the test loads it.
- **Stepwise migrations.** `from_record` accepts every version ever written.
  Each version has a pure function that migrates it to the next one, and
  loading applies them in order until it reaches the current version.
- **One fixture per version.** A realistic record of each version lives in
  `tests/fixtures/<shape>/v<N>.json`. Old fixtures are never edited or
  deleted.
- **Fixture test.** A test loads every fixture into the current domain type,
  and checks that a fixture exists for the current version.

Relational schemas managed by a migration tool (such as Alembic) are
versioned by that tool. This rule covers the shapes the migration tool does
not see, including JSON stored inside a column.

## Why

Old data does not go away when the code changes. An agent that renames a
field sees green tests, because every test builds fresh data with the new
shape, and the change breaks the first time production reads a record
written last week. Fixtures put old data in front of the tests, so the
breakage shows up in the check command instead of in production. The
version field makes the shape of every record explicit, so loading code
never has to guess.

## Example

Version 1 stored amounts as integer cents. Version 2 stores decimal strings.

Bad:

```python
def from_record(raw: dict[str, Any]) -> Invoice:
    # silently changed from amount_cents; every v1 record now fails
    return Invoice(amount=Decimal(raw["amount"]), ...)
```

Good:

```python
CURRENT_VERSION = 2


def _v1_to_v2(raw: dict[str, Any]) -> dict[str, Any]:
    items = [
        {"description": i["description"], "amount": str(Decimal(i["amount_cents"]) / 100)}
        for i in raw["line_items"]
    ]
    return {**raw, "version": 2, "line_items": items}


_MIGRATIONS: dict[int, Callable[[dict[str, Any]], dict[str, Any]]] = {1: _v1_to_v2}


def from_record(raw: dict[str, Any]) -> Invoice:
    while (version := raw["version"]) < CURRENT_VERSION:
        raw = _MIGRATIONS[version](raw)
    return Invoice(...)
```

```python
FIXTURES = sorted(Path(__file__).parent.joinpath("fixtures/invoice").glob("v*.json"))


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_every_invoice_fixture_loads(path: Path) -> None:
    from_record(json.loads(path.read_text()))


def test_current_invoice_version_has_a_fixture() -> None:
    assert f"v{CURRENT_VERSION}" in {p.stem for p in FIXTURES}, (
        f"Add tests/fixtures/invoice/v{CURRENT_VERSION}.json with a realistic record."
    )
```

## Codify it

- **pytest** loads every fixture and checks that the current version has one,
  as in the example above (`templates/example-project/tests/test_invoicing.py`).
- **git in the Makefile** fails when a committed fixture changes or
  disappears:

  ```make
  BASE ?= origin/main

  fixtures:
  	@changed=$$(git diff --name-only --diff-filter=MD $(BASE) -- tests/fixtures 2>/dev/null); \
  	if [ -n "$$changed" ]; then \
  		echo "$$changed"; \
  		echo "Committed fixtures must not change. Restore them. If the shape changed, bump the record version and add a new fixture."; \
  		exit 1; \
  	fi
  ```

  In CI, set `BASE` to the pull request's base commit and fetch enough
  history for the diff.
- **A schema snapshot test** can catch a shape change without a version
  bump: store the record's JSON schema (for example from pydantic's
  `model_json_schema()`) per version, and fail when the current schema
  differs from the snapshot of `CURRENT_VERSION`.

## Review by hand

- Did your change touch a record type, `to_record`, `from_record`, or any
  code that writes to storage or a queue?
- If the shape changed: is `CURRENT_VERSION` bumped, with a migration step
  and a new fixture? Without a schema snapshot test, nothing else catches a
  forgotten bump.
- Did the meaning of a value change while its type stayed the same (cents
  to euros in the same `int`)? That is a shape change too.
- Did an optional field become required, or a type get narrower? Then old
  records need a migration, or evidence that none violates it plus a fixture
  of the oldest record.
- Is the module README's persisted data section up to date?
