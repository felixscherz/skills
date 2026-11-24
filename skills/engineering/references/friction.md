# Friction

Friction is the moment code resists the work: a good test will not come
together, or a simple change spreads across many files. It is the cheapest
design signal there is, because it shows up during the work, at the place
where the design is weak. Each signal below is something you notice yourself
doing, and points to the reference that holds the cure.

- A simple change touches many files. Knowledge that belongs in one place is
  spread out: two modules know the same format or decision, modules are split
  by the order things happen in rather than by what they hide, parameters
  pass through layers, or a concept has no home and is rebuilt wherever it
  is needed (`deep-modules.md`, `domain-driven-design.md`).
- You reach for a mock or a patch. A dependency with side effects is created
  inside the code instead of passed in, so there is no seam for a fake
  (`program-design.md`, `test-behavior.md`).
- Test setup builds half the system. The code under test does too much, or
  mixes logic with side effects, so the logic cannot be reached on its own
  (`program-design.md`).
- The behavior is only reachable through a private function, or the test has
  to reach into internals. A step is hidden behind the wrong interface, or
  the test sits at the wrong level (`test-behavior.md`).
- You read the implementation to learn how to call it: the order of calls,
  which flags matter, which errors to catch. The interface is shallow, and
  its real rules live in the implementation (`deep-modules.md`).
- You copy a sequence or a transformation from another caller. That is
  complexity the module should own (`deep-modules.md`).
- New code has two plausible homes, or none. The layout does not say where
  code belongs (`program-design.md`).
- You add a special case to make a requirement fit. The model has drifted
  from the problem (`redesign-from-first-principles.md`).
- The same check on a string, dict, or flag appears in several places. A type
  is missing (`type-system.md`).
- A name sends you into the implementation, or one concept goes by two names
  (`domain-driven-design.md`).

Write each friction down when it happens, in one sentence: what you tried,
what resisted, and where. For example, "had to patch `requests.post` because
`InvoiceClient.__init__` builds its own session". Friction you cannot tie to
such a moment is a guess about the code, not a finding. What to do with it
is in "When code resists" in `../SKILL.md`.
