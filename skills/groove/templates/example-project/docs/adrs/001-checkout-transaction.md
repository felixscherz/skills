# ADR 001: Commit Checkout through one unit of work

## Status

Accepted. The use case and fake unit of work are implemented. A production storage adapter is not implemented.

## Context

Checkout issues an Invoice and charges the Customer its total. Both changes must happen together or neither
must happen. Invoicing and Customers each own their own rules, but neither owns this combined intent.

## Decision

Give Checkout its own module one layer above Invoicing and Customers. Its use case calls their public APIs and
owns a unit-of-work port covering both writes. Run the rules on loaded values before writing, then commit once.

Do not put the sequence in a route or require callers to combine two independent commits. Either approach would
leave the all-or-nothing rule outside the use case that owns it.

## Consequences

- Invoicing and Customers remain independent of Checkout.
- A production adapter must make both writes atomic. The fake allows deterministic use-case tests but does not
  prove production transaction behavior.
- Entry points call the Checkout use case rather than coordinating the writes themselves.
