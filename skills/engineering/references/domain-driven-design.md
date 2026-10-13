# Domain-driven design

DDD gives the user and the agent a shared language. When code uses the
domain's names, the user can name a concept and the agent can find it, and a
complex process can be explained in domain terms instead of implementation
details. This holds for every name in code: types, functions, and methods,
not only entities.

- Name everything in the domain's own words, down to functions and methods.
  When code and domain use different words for one thing, align them.
- Keep one name per concept. Reuse the term the codebase and the user already
  use instead of inventing a synonym (`item`, `record`, `row` for an entry).
  When a concept is renamed, rename it everywhere in the same change; never
  keep two names in parallel. Where the project keeps a glossary, it is the
  source of truth, and a change that introduces or renames a concept updates
  it in the same commit.
- Give each domain concept its own type. A value object for things defined by
  their value (an email, a money amount), an entity for things with identity
  and a lifecycle.
- Keep the domain model free of framework, HTTP, and database concerns.
  Adapters translate at the edges.
- Group things that must change together into an aggregate, and change them
  only through one entry point that enforces the invariants.
- The domain decides, use cases do. Domain behavior takes values and returns
  a decision or new state; it never loads, saves, or calls out. A use case
  named after the intent (`CancelOrder`) loads inputs through ports, lets the
  domain decide, persists results, and owns the transaction boundary: one use
  case, one unit of work. Run every rule before the first write. Entry points
  delegate to one use case. Use cases do not call other use cases, and domain
  services do not orchestrate other services.
- Draw bounded contexts where the same word means different things. A
  "customer" in billing and in support may be two models, not one.
- Keep contexts apart in code. A context reads from another only through a
  port it owns, worded in its own terms and implemented by one adapter that
  translates the other context's model. Dependencies between two contexts
  go one way. A change that must reach a context that cannot commit with
  yours travels as an event, not a shared transaction. Links in both
  directions or frequent cross-context transactions mean the boundary is
  wrong.
