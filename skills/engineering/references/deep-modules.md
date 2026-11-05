# Deep modules

A module earns its place when its interface is much simpler than what it
hides. Callers learn the interface, not the implementation, so every decision
the module makes for them is one they no longer repeat, and every detail it
leaks is one they can break. Judge depth from the callers' side, by what they
have to know and do to get a job done.

- The interface is everything a caller has to know, not just the signatures:
  errors, ordering, configuration, side effects, lifecycle, and the data
  formats others read. A short signature with a long list of rules for
  calling it is not a simple interface.
- A shallow module, whose interface is nearly as complex as its
  implementation, such as a pass-through wrapper or a function extracted only
  so it can be tested, adds a concept without removing one. Before adding or
  keeping a module, ask whether deleting it would gather its complexity in
  one place or just move it to the callers.
- Look for complexity the callers carry that the module could own:
  - callers have to call things in a set order, such as open, configure,
    run, close
  - callers catch low-level errors or handle special cases that the module
    could handle itself or define out of existence
  - callers pass configuration, flags, or options whose value they do not
    care about
  - callers transform data the same way before or after every call
  - two modules know the same format, protocol, or decision, so a change to
    one forces a change to the other
  - modules split by the order things happen in (read, parse, write) rather
    than by the knowledge each one hides
  - methods or parameters that only pass through to the next layer
  - several special-purpose methods where one general method would serve
    every caller
  - one change needs edits in the module and in its callers
- Pull complexity down. When either the module or its callers has to deal
  with a complication that belongs to the module's responsibility, the module
  should. Leave decisions that differ per caller with the callers.
- Design it twice. Sketch at least two substantially different interfaces as
  caller code before choosing one, for example a small general interface and
  one tailored to today's callers. The first idea usually mirrors the current
  implementation.
- Measure depth before and after a change: the public names the module
  exposes, the imports a caller needs, the steps and concepts a caller has to
  know for each job, and the decisions callers no longer make. A change that
  reduces none of these did not make the module deeper.
