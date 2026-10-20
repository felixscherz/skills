# Python domain modeling

Python's static types and runtime values provide different guarantees. Choose
the representation that expresses the domain contract, not just one that
satisfies the type checker.

- Prefer small, immutable value objects for domain identifiers. A frozen
  dataclass with an explicitly typed `value` gives the identifier a runtime
  type and a home for validation. Keep it with the concept that owns it,
  not in a generic ID base class or a shared registry.
- `NewType` provides static distinction only. It returns the underlying value
  at runtime, with no `.value` attribute or constructor validation hook. Use
  it when static distinction is the intended contract, not as a substitute
  for a domain value object.
- An opaque ID need not expose how it was generated. A UUID-backed adapter
  can return a string; the use case wraps it in the owning domain ID before
  calling domain behavior. Require UUID semantics only when the model needs
  them. Generation remains outside the domain in either case.
- Start with the known contract. A value object provides a home for
  invariants; creating one does not establish new invariants. Do not add
  blank checks, length limits, or normalization without a domain reason.
  Trimming or lowercasing an identifier changes identity, so treat it as a
  behavior decision, not housekeeping.
- Parse external values into domain IDs at the boundary and unwrap `.value`
  when formatting output, serializing, or translating to another context. Keep persisted shapes
  explicit: replacing an in-memory string with a value object does not
  require changing its stored string representation.
- Test the observable contract: value access, equality within one ID type,
  inequality between different ID types, use as a dictionary key, and
  serialization round trips. Test validation only for rules the model has.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ProductId:
    value: str


@dataclass(frozen=True)
class SupplierProductId:
    value: str


assert ProductId("same") == ProductId("same")
assert ProductId("same") != SupplierProductId("same")
assert ProductId(" product-1 ").value == " product-1 "  # no normalization rule
```

The ID classes do not generate their own values. Neither needs validation
until a domain rule calls for it. The classes remain distinct at runtime
even when their underlying strings match.
