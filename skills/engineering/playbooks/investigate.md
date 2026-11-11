# Investigate

Answer a question about a system by reading it and running it, not by changing it. The question can be how something
works, whether something is feasible or worth doing, or which of several options fits. The answer rests on evidence,
and "no" or "not worth it" is a valid one. The agent works through the question on its own and comes back with the
answer, not with questions it could have settled itself.

## Applies when

The user asks how a service, a codebase, or a library works, whether a change, an upgrade, or an integration is
feasible, or asks to analyze or compare options. Nothing has failed and nothing is being designed yet. A failure to
explain belongs in Find the cause (`find-the-cause.md`), and working out a solution the user has decided to build
belongs in Design with me (`design-with-me.md`).

## Who decides

- The agent decides how to investigate and settles every fact on its own, by reading code and documentation, running
  the code, or running a throwaway experiment outside the repository. It does not ask the user what it can observe.
- The agent asks only when the question can be read in ways that lead to different investigations, or when the
  evidence that would settle it is out of reach, such as a system it has no access to.
- The user decides what happens with the answer. The agent does not change product code, commit, or open a PR in this
  playbook.
- Access to running systems is read-only. Anything that changes state in a shared environment waits for the user.

## Steps

1. State the question in one line, and what would answer it. For a feasibility question, say what has to be true for
   a yes and what would make it a no.
2. Find the sources: the nearest `CONTEXT.md`, the code at the version that matters, the documentation of third-party
   libraries at the version in use, and the running system where the user pointed to it.
3. Trace what actually happens, from the entry point through every part that plays a role. Read the code instead of
   inferring behavior from names, and read a library's documentation or source for the version in use instead of
   relying on memory. Describe what you find in the domain's words (`../references/domain-driven-design.md`).
4. For a feasibility question, find the part most likely to make the answer no and settle it first. When reading
   cannot settle it, run the smallest experiment that can, outside the repository. When the question is about a
   change, find who relies on the behavior it would alter (`../references/dont-break-production.md`).
5. Keep what you observed apart from what you inferred. Give each claim its evidence: a file and line, a command and
   its output, or a link to the documentation.
6. Reach a verdict and recommend. For feasibility that is yes, no, or yes under named conditions, with what it would
   take and the main risk. Do not soften a no into a plan.

## Done

The reply opens with the answer in a sentence or two. Then it explains how the thing works or why the verdict holds,
with the evidence for each claim, and names what was not checked and what is still uncertain. A feasibility answer
adds what it would take, the main risk, and a recommendation. When the user goes ahead, the next playbook is usually
Design with me, or Make a change for something small. When the answer is no, nothing follows.
