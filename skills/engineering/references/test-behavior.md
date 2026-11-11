# Test behavior

The best tests are examples of someone using the code. They call the public
API the way a user would and assert what that user would observe. Writing the
test first is design work: it is the first use of the new API, and code
written test-first tends toward better design because testability shapes it
from the start. A test full of mocks and patches is a design signal: the code
is tightly coupled and lacks seams (see `program-design.md`).

- Before implementing, state how you will verify the feature works or the bug
  is gone.
- Write the test first and run it. Confirm it fails, and fails for the
  intended reason, before writing the fix or feature.
- For a bug, the failing test is the reproduction. Don't fix what you have not
  reproduced.
- When a test would be clunky or cannot cover the behavior, use the closest
  other check. A runnable one-off script, or steps for the user to verify in a
  test environment after deploying. Say which check you used and why.
- Test through the public API. When a test reaches into internals, ask whether
  it sits at the right level, or whether the behavior is better tested from
  further out, maybe without calling this code directly.
- When moving responsibility between components, verify the behavior through
  the entry point that currently invokes it. A direct test of the replacement
  component does not prove the application uses it. Start from fresh state
  where existing resources could otherwise hide missing initialization.
- When a public interface gains tests, judge each existing test of internals
  on its own rather than deleting them all because the interface is covered.
  Keep one that checks behavior the interface tests do not reach or that
  pinpoints failures in hard logic; delete one that only fixes how the code
  is arranged.
- Avoid mocks and patches. At a real external boundary (a third-party API, the
  clock), pass in a fake through a seam instead of patching. When no seam
  exists, push back and revisit the design instead of patching around it.
- A fake is a small, working implementation of the same interface as the real
  dependency, such as an in-memory repository or a settable clock. A mock
  asserts which calls happened; a fake lets the test assert on outcomes, so
  the test survives refactoring and fails when behavior breaks. Share fakes
  across tests instead of redefining them per test, and let the type checker
  verify they fit the interface.
- Keep fakes honest. Run one contract test suite per interface against its
  fake and every real implementation, so a fake cannot drift from the
  behavior it stands in for.
- Patching is acceptable only for process-level state that has no seam, such
  as environment variables in tests of configuration loading.
- Name a test after the behavior it checks. A failing test's name alone
  should say which behavior broke.

  ```python
  # Bad
  def test_create() -> None: ...

  # Good
  def test_created_instruction_can_be_found_through_a_query() -> None: ...
  ```
