---
name: groove
description: Use when working in a Python repository whose AGENTS.md or CLAUDE.md says it follows Groove, or when the user asks to apply Groove, design a Python codebase for agentic coding, or turn a codebase convention into a CI check. Covers domain naming via a glossary, module boundaries, module naming, injecting time/randomness/IDs/I/O into a functional core, versioned persistent data, and codifying each rule with ruff, pyright, import-linter, and semgrep.
disable-model-invocation: true
---

# Groove

Groove is a way to design Python codebases that agents work on reliably. It
borrows its core idea from Lauren Tan's Dune: make the shortcut the only
correct path. Every concept has one name, every piece of code has one
obvious home, and every dependency on the outside world is visible in a
signature.

Groove is a design philosophy, not a tool. It has no runtime, no CLI, and no
config file of its own. Its principles become real through existing tools
that run in one check command in CI. A rule that lives only in prose drifts,
because every agent session reads it a little differently. A rule in CI
holds, and its error message teaches the fix at the moment it matters.

## Principles

Each reference holds one principle: the rule, why it helps, an example, how
to codify it, and what still needs review by hand. Read a reference in full
when its trigger fires, not up front.

- **Codify rules** (`references/codify-rules.md`). Setting up or changing the
  check command or CI, adopting Groove without a check command, adding a
  tool, writing an error message, or noticing a rule that is followed but
  not checked.
  - One command runs every check. Every check says how to fix what it finds.
- **Glossary** (`references/glossary.md`). Naming anything that represents a
  domain concept, or finding two names for one thing.
  - One canonical term per concept in `docs/glossary.md`, linked from
    `CONTEXT.md`. Names are reviewed by hand; no tool checks them yet.
- **Project context** (`references/project-context.md`). Setting up project
  documentation, recording an architectural decision, or changing an
  approach covered by an existing decision.
  - `AGENTS.md` holds working instructions, `CONTEXT.md` routes readers to
    relevant documentation, and `docs/adrs/` records decisions and reasons.
    Read the relevant ADR before choosing an approach. Documentation content
    is reviewed by hand.
- **Application CLI** (`references/application-cli.md`). Adding or changing
  service startup, launch instructions, server options, or logging setup.
  - The application owns its installed launch command, such as `acme serve`,
    rather than requiring users to invoke Uvicorn or another server directly.
    The startup path owns configuration and logging before application
    initialization. Tests exercise the installed command.
- **Module layout** (`references/module-layout.md`). Creating a module or
  file, deciding which layer code belongs in, writing a use case, or adding
  a unit of work.
  - Split by domain first, then by layer. A small module is one file
    (`customers.py`). It becomes a package with `domain/` (decides, pure),
    `usecases/` (does, owns ports and the transaction), and
    `infrastructure/` (adapters) once it needs an adapter or an entry
    point. Layers are checked per package by import-linter.
- **Architecture boundaries** (`references/architecture-boundaries.md`).
  Adding an import between modules, creating a module, reading from a
  sibling module, or writing an operation that changes state in more than
  one module.
  - Modules are used only through their `__init__.py` (or their single
    file). Dependencies point down declared layers. Both are import-linter
    contracts.
  - Which module of a pair sits higher is a design decision per pair:
    existence and importance can disagree. Other modules' entities are held
    by ID.
  - Adapters and entry points (routers, CLI commands, framework hooks) are
    not exported. Only the composition root imports them, as the one
    allowed importer in each module's `protected` contract.
  - Reading from a sibling goes through a port the reader owns and one
    adapter, declared in the contract.
  - Every write has one owner: the module it writes, or the highest module
    it writes, which changes lower modules through their public API, in one
    unit of work when the domain says so. Siblings that must commit together
    mean one moves up a layer, or, rarely, a workflow the business already
    names gets a module of its own one layer up.
  - Links between modules live in the higher module. Events belong to the
    module that records them and flow up like imports.
- **Meaningful module names** (`references/meaningful-module-names.md`).
  Creating or renaming a module or file, or looking for a home for code that
  seems shared.
  - No `utils`, `helpers`, `common`, `shared`, `misc`, `core`, or similar.
- **Injected external factors** (`references/injected-external-factors.md`).
  Choosing a domain ID type, or writing code that needs the time,
  randomness, a new ID, configuration, or any I/O.
  - A functional core in an imperative shell. External factors arrive through
    injected ports, with fakes next to the port. ruff bans the direct calls.
    Opaque domain IDs are string-backed, frozen value objects, not `NewType`
    aliases or `UUID` values.
- **Versioned persistent data** (`references/versioned-persistent-data.md`).
  Changing the shape of anything stored and read back later.
  - A `version` field, a fixture per version, and a test that every fixture
    loads.

## Working in a Groove codebase

1. Read `AGENTS.md` (or `CLAUDE.md`) for the check command, then
   `CONTEXT.md` and the glossary it links to. Follow its "Read when" links
   to relevant ADRs before choosing an approach, then read the `README.md`
   (or docstring) of each module you will change.
2. Make the change following the principles.
3. Run the check command and fix everything it reports. Do not report done
   while it fails, and do not run only a subset.
4. Review what the tools cannot see (below).
5. Report back (below).

## Review what the tools cannot see

Tools catch the mechanical part of each rule. These questions cover the rest:

1. **Names.** Does every new identifier, test name, and doc line that names a
   domain concept use a glossary term? Did a new concept get a `proposed`
   glossary entry? Did you use a banned synonym anywhere, including inside
   an identifier?
2. **Boundaries.** Did you add a name to a module's `__all__` that exposes
   an internal detail? Did you change the layers contract or add an
   `ignore_imports` entry? If so, was that a deliberate design change?
   Does any new domain code decide only, with the loading and saving in a
   use case?
   Would each entity still make sense if a downstream integration disappeared?
   Which fields exist only because that integration needs them, and who owns them?
3. **Responsibilities.** Does each module you touched still do one thing its
   README or docstring states? Did a single-file module outgrow one file?
   Does any new file or module have a name that passes the check but says
   nothing?
4. **Functional core.** Is new domain logic pure, given the same arguments
   always returning the same result? Did you add a port without a fake, or a
   `port: Port | None = None` fallback?
5. **Persistent data.** Did a stored shape change? If so, is the version
   bumped, with a migration step and a new fixture?
6. **Codification.** Did you follow a rule here that no check enforces? Then
    propose the check, or add it if the user asked you to apply Groove.
7. **Project context.** Does `CONTEXT.md` direct readers to decisions your
   change touches? Do those ADRs distinguish agreed decisions, unresolved
   choices, and implementation status? Did a changed decision get a new
   record that supersedes the old one?
8. **Application CLI.** Do launch instructions and deployment commands use
   the application's CLI? Does that startup path configure logging before
   initializing components, without the server replacing it? Are startup,
   verbosity, and shutdown tested through the installed command?

## Report back

These principles are being tested. At the end of your reply, add a short
**Groove feedback** section when any of these happened:

- A rule was unclear, or two rules pulled in different directions.
- A rule cost a lot of effort for little benefit in this change.
- You added an exception to a check (a per-file ignore, an ignored import).
  Say which and why.
- You added or wanted to add a glossary term.
- You found a rule that could be codified but is not.

Skip the section when none happened. Do not edit this skill unprompted.

## Adopting Groove

Copy from `templates/`:

- `AGENTS.md`: the section that marks a repository as following Groove.
- `module-README.md`: the README for each new package module. It holds only
  what the code cannot say; a single-file module puts it in its docstring.
- `adr.md`: a starting point for a numbered decision in `docs/adrs/`. Add
  records as decisions arise, not empty records for hypothetical choices.
- `example-project/`: a working project where `make check` enforces every
  checked principle. Copy `pyproject.toml` (pyright, ruff, import-linter),
  `semgrep.yml`, `Makefile`, `CONTEXT.md`, and `docs/glossary.md`, then
  adapt the module names and context links. `docs/adrs/` demonstrates a
  decision record; replace it with the project's own decisions.
  `src/acme/` shows a domain module split into
  layers (`invoicing`), a single-file domain module
  (`customers.py`), a read from a sibling through an owned port
  (`invoicing/infrastructure/customer_lookup.py`), single-file port modules
  (`clock.py`, `ids.py`), a workflow that is its own module, with a unit of
  work (`checkout`), and the composition root (`wiring.py`).

In an existing codebase, introduce one principle at a time, starting with
the check command. Never add a tool or contract unprompted when the user has
not asked to apply Groove: propose it instead.

When asked to apply Groove in a repository without a check command, read
`references/codify-rules.md` and establish the command as the first adoption
step. State which rules it enforces and which remain manual review. The
first step need not introduce every tool, but it must provide one repeatable
entry point. If tooling is intentionally deferred, describe the result as
partial adoption rather than full Groove compliance.

### Converting an existing module

Fix the module's public surface before moving anything inside it. Once
every other module imports only from its `__init__.py` and a contract keeps
it that way, internal moves no longer touch the rest of the codebase, and
the contract finds every remaining deep import on the first run instead of
in a late review. Each step below ends in a working, committed state:

1. **Characterize.** Pin the module's observable behavior with tests that go
   through its current entry points and survive the moves. Behavior that
   depends on time or IDs can wait until step 4 brings the ports; do not
   patch to get it earlier.
2. **Public API and contract.** Write `__init__.py` with `__all__`, move
   every outside importer onto it, and add the `protected` contract with the
   composition root as the only outside importer. Any import that cannot
   move (an app factory mounting routers, telemetry registering metrics)
   is part of the composition root: list it in the contract by name.
3. **Domain.** Move the rules into `domain/`, pure, taking time and IDs as
   arguments.
4. **Use cases and ports.** One use case per intent, its ports and their
   fakes, with deterministic tests through the fakes.
5. **Adapters.** Move persistence and other I/O into `infrastructure/`,
   translating their errors into the module's own.
6. **Entry points with their wiring.** Switch routes and commands to the use
   cases in the same step as the composition root that builds them.
7. **Remaining callers.** Move other modules' calls onto the public use
   cases or onto ports they own, then delete the old service.
8. **Contracts and README.** Add the module to the layers contracts, if not
   already done as its layers appeared, and write its README.

A small module with no adapter and no entry point can become a single file
instead: after step 1, move it into `orders.py` with `__all__`, in the order
decide, then ports and fakes, then do, move every outside importer onto it,
and add it to the layers contract. The remaining steps wait until it needs
an adapter.

Before each step, list everything that imports or calls the code it moves,
and make sure this step or an earlier one updates it.
