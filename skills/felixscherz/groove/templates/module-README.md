# <module name>

<!-- Copy into the new module's directory as README.md and fill in every
section. Add the module to the import-linter layers contract and to
containers of the contract inside modules, and give it a protected
contract. -->

## Responsibility

<One or two sentences: what this module is responsible for. No "and various",
no "utilities". If you need "and", consider two modules.>

Not responsible for: <neighbouring responsibilities that live elsewhere, and
where.>

## Layout

- `domain/`: <values and rules this module decides>
- `usecases/`: <one file per intent>, plus `ports.py` and `fakes.py`
- `infrastructure/`: <adapters, persisted record shapes>

## Public API

Everything other modules may import, as exported in `__init__.py`:

- `<Name>`: <one line>

## Glossary terms

The glossary terms this module implements or uses:

- <Term>

## Ports

Protocols this module defines, with their fake and real implementations:

| Port | Fake | Adapter |
|---|---|---|
| `<Protocol>` | `<Fake>` | `<Adapter>` |

## Persisted data

| Shape | Current version | Fixtures |
|---|---|---|
| `<Shape>` | <N> | `tests/fixtures/<shape>/` |

Dependencies are declared in the import-linter contracts in `pyproject.toml`.
