# Codify rules

## The rule

The mechanical parts of Groove principles are enforced by tools that run
in CI. The skill describes the design. The tools hold the line. Glossary
names and project documentation content are reviewed by hand; the glossary
format is still settling, and tools cannot judge architectural reasoning.

- **One command.** A single command (for example `make check`) runs every
  check: types, lint, format, import contracts, pattern rules, module
  names, fixtures, and tests. CI runs that command and nothing else,
  so local and CI results cannot diverge. `AGENTS.md` names the command.
- **Adoption starts with the command.** If none exists when the user asks to
  apply Groove, establish it before expanding the adoption. Introduce checks
  incrementally and state what is enforced and what is still reviewed by
  hand. Running an improvised sequence of tools is not a replacement. If
  tooling is intentionally deferred, report partial adoption.
- **Use existing tools.** Pick the most specific tool that can express the
  rule, in this order:
  1. The type checker (pyright strict; mypy `--strict` or ty also work).
  2. ruff rules and settings.
  3. import-linter contracts for anything about imports.
  4. semgrep rules for code patterns ruff cannot express.
  5. A few lines of shell in the Makefile for file-level facts (names,
     changed paths).
  6. A pytest test, when the rule is about the code's structure and none of
     the above fits.
  Do not write a custom linter while one of these can do the job.
- **Every check says how to fix it.** Use each tool's message field: ruff's
  `banned-api` `msg`, import-linter's `broken_contract_guidance`, semgrep's
  `message`, an `echo` in the Makefile. A message that only says what is
  wrong costs an agent a round trip and a guess.
- **Exceptions live in tool config, with a reason.** A per-file ignore, an
  `ignore_imports` entry, or a semgrep `exclude`, each with a comment saying
  why. No silent `# noqa` or `# type: ignore` without a reason in the same
  line.
- **Rules graduate.** A rule starts as a review question in this skill. When
  it proves useful and a tool can express it, it moves into the check
  command, and the review question shrinks to whatever the tool cannot see.

The same standard applies to error messages in application code: every
exception message says what went wrong and what to do about it.

## Why

An agent works in a loop: change, check, read the output, change again.
Whatever the check command enforces, the agent gets right within a few
iterations, without having to remember it. Whatever it does not enforce
depends on the agent having read and interpreted the prose correctly, every
session. Fix-it messages turn a failure into the next step, so the check
command teaches the conventions to every agent that runs it.

Existing tools are maintained, documented, fast, and already known to
agents. A config entry is easier to review and change than a custom checker.

## Example

Bad: the rule exists only as prose, and the check gives no direction.

```text
# AGENTS.md
Please don't call datetime.now() in domain code.

$ make check
src/acme/invoicing/domain/model.py:12: error
```

Good: the rule is config, and the output is the fix.

```toml
[tool.ruff.lint.flake8-tidy-imports.banned-api]
"datetime.datetime.now".msg = "Inject a Clock (acme.clock) and call clock.now()."
```

```text
TID251 `datetime.datetime.now` is banned: Inject a Clock (acme.clock) and call clock.now().
  --> src/acme/invoicing/domain/model.py:12:9
```

In application code, bad:

```python
raise ValueError("invalid status")
```

Good:

```python
raise InvoiceAlreadyIssued(
    f"Invoice {invoice.id.value} is already issued and cannot be issued again. "
    "Check invoice.status before calling issue(), or draft a new Invoice."
)
```

## Codify it

`templates/example-project/` has the full, working setup. The check command
in its `Makefile`:

| Target | Tool | Enforces |
|---|---|---|
| `types` | pyright strict | Types everywhere, so the core's inputs are explicit |
| `lint` | ruff | Banned external factors (`TID251`), no calls in default arguments (`B008`), aware datetimes (`DTZ`) |
| `format` | ruff format | One formatting, no style discussions |
| `boundaries` | import-linter | Layers, public APIs, no UUID types in the domain |
| `rules` | semgrep | Direct file I/O outside adapters, exceptions without a message, `NewType` domain IDs |
| `module-names` | shell | No vague module names |
| `fixtures` | shell + git | Committed fixtures never change |
| `test` | pytest | Behavior, including every fixture loading |

The semgrep rule for exceptions without a message:

```yaml
- id: exception-without-message
  languages: [python]
  severity: ERROR
  message: >-
    Exception raised without a message. Say what went wrong and how to fix
    it, inline or in the exception class's __init__.
  pattern-either:
    - pattern: raise $EXC()
    - patterns:
        - pattern: raise $EXC
        - metavariable-regex:
            metavariable: $EXC
            regex: ^[A-Z]\w*$
```

## Review by hand

- Did the check command run in full and pass?
- Does each exception message you wrote say what to do?
- Does each new exception in tool config have a reason next to it?
- Did you follow a rule that no check enforces? Propose the check, naming the
  tool and the config.
- If you reviewed code: does each comment contain the fix?
