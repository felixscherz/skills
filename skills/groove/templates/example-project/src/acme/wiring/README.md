# wiring

## Responsibility

The composition root. Builds every adapter and binds it to the use cases that
consume its port, so routes and commands receive ready use cases.

Not responsible for: any rule or workflow. Those belong to the modules it wires.

## Public API

- `build_invoicing`, `Invoicing`: the invoicing use cases bound to the JSON file
  repository, the customers lookup, the system clock, and UUIDs.

The only code outside a module allowed to import that module's
`infrastructure/` and its routes or commands, declared in each module's `protected`
contract in `pyproject.toml`.
