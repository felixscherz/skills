# Program design

Structure a codebase so its parts can be used, and therefore tested, on their
own. Testability is a first-class design goal, not an afterthought. A test is
the first user of an API, and code that is awkward to test is awkward to use.

- Keep a pure core. Domain logic takes values and returns values. Side effects
  (database, HTTP, filesystem, clock) live at the edges.
- Build seams. Dependencies with side effects come in through parameters or
  interfaces, so tests pass in-memory fakes instead of patching. This includes
  the easily overlooked ones: current time, sleeping, randomness, ID
  generation, environment variables, and network calls. Read configuration in
  one place at startup and pass the values in. Add a seam where a second
  implementation exists or a test needs one, not speculatively.
- Make modules deep. A module earns its place when its interface is much
  simpler than what it hides. A shallow module, whose interface is nearly as
  complex as its implementation, such as a pass-through wrapper or a function
  extracted only so it can be tested, adds a concept without removing one.
  Before adding or keeping a module, ask whether deleting it would gather its
  complexity in one place or just move it to the callers. Tests target the
  interface, so everything behind it can change freely.
- When designing an API or model, write the calling code, a test or an
  example, before the implementation.
- Let the layout say where code belongs. Every responsibility should have
  one obvious place, so a reader knows where to find a piece of code and
  where to put a new one. Many layouts achieve this; what matters is that
  the intent is clear and nothing has two plausible homes. My default splits
  by bounded context first and by layer inside each context (domain, use
  cases, infrastructure, entry points), so a change to one concept stays in
  one directory and the boundaries between contexts can be checked.
- Make dependency direction executable. When the codebase has layers or
  modules that must not depend on each other, check it with an
  import-contract tool (e.g. import-linter for Python, dependency-cruiser for
  TypeScript, ArchUnit for Java) rather than describing it in prose only.
- Names matter. A good name carries enough meaning for a reader to not have to
  dive into the implementation in order to understand the code. This holds
  for modules too: name a module after what it does (`slugs`, `retry`), never
  `utils`, `helpers`, `common`, or `shared`, which attract unrelated code and
  have no owner. Code that two modules need is either a concept with its own
  name (`money`, `validity`) or belongs to one of them.
