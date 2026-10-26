# Open question: module layout

Not loaded by the skill. Notes for deciding how strict Groove is about module
structure.

## Decided

Recorded in `references/module-layout.md` and
`references/architecture-boundaries.md`, and enforced in the example project.

1. **What is a module?** A top-level package or file under the source
   root. A small module is a single file (`customers.py`) and becomes a
   package once it needs an adapter or an entry point, or outgrows one
   read. A package's layer subpackages are not modules of their own: they
   have no public API and are private behind the module's `__init__.py`
   (`protected` with `acme.<module>.**`). A single-file module needs no
   `protected` contract and no README; its docstring holds the
   responsibility.
2. **Fixed roles?** Yes, as layers: `domain/`, `usecases/`,
   `infrastructure/`, plus an entry-point layer (`api/`) where a module has
   one. One `layers` contract with `containers` checks all modules, with
   optional layers in parentheses. The ruff and semgrep ignores became one
   pattern each (`*/infrastructure/`). `clock.py` and `ids.py` keep port,
   fake, and real implementation in one file with their own ignores.
3. **Where do ports live?** In `usecases/ports.py`, since use cases consume
   them; the domain defines no ports. Fakes sit next to them in
   `usecases/fakes.py`.
4. **Reading from a sibling module.** A port owned by the reader, one
   adapter in its `infrastructure/`, and an `ignore_imports` entry in the
   layers contract.
5. **No `shared` package.** Code that several modules need goes into a small
   technical module named for its job, in the bottom layer.
6. **No module types.** Modules are not classified as domain, coordinator,
   or technical. A module has the layers it needs, and a missing `domain/`
   says nothing else about it. An operation that changes several modules
   has one owner: the module it writes, or the highest module it writes.
   Only siblings that must commit together, where neither moves up a layer
   and the business already names the workflow (Checkout), get a module of
   their own one layer up.
7. **Composition root and adapters.** A top-level `composition` module in the
   top layer builds the adapters. Adapters and entry points are not exported
   from `__init__.py`; each module's `protected` contract lists `composition` as
   its only outside importer, so they are reachable from the composition
   root alone. The example's `composition` has no environment reads yet, so no
   `TID251` ignore; `customers` still has no storage adapter and `checkout`
   no real unit of work, so `composition` builds only invoicing.
8. **Module READMEs hold only what the code cannot say.** Responsibility,
   what the module is not responsible for, glossary terms, and decisions.
   Public API, ports, persisted shapes, and dependencies are left out: the
   code and the contracts already state them, and a copy in prose drifts.

## Still open

1. **Recipes.** Step-by-step procedures for creating a module, an entity, a
   persisted shape, or a glossary term. These are the manual form of future
   generators, and the layout is now fixed enough to write them.
2. **Where do tests live?** One top-level `tests/` mirroring modules, or
   tests inside each module? Today tests of a module may import its
   internals, while tests of other modules may not; a layout should make
   that boundary visible.
3. **One protected contract per module.** import-linter needs a contract per
   module to keep submodules private, which is boilerplate that grows with
   the module count. Adding a package module now touches three contracts
   (layers between modules, `containers` inside modules, `protected`); a
   single-file module touches only the first. tach covers
   the boundary part in one `interfaces` setting. Worth switching, or worth
   a check that every top-level package appears in all three?
4. **Events between modules.** The boundaries reference says to use an event
   when two modules cannot commit together, but there is no example of
   where events, their handlers, and an outbox live.
