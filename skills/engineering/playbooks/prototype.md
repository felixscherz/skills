# Prototype

Build a proof of concept fast, to learn something: whether an idea works, how it feels to use, or which variant is
better. What counts is how quickly the user sees a result and can react to it, not the quality of the code. Production
concerns are out for the whole playbook: tests, types, error handling, architecture, compatibility, and reviewable
commits. The other rules of this skill apply only where they make the next cycle faster.

## Applies when

The user asks for a prototype, a proof of concept, or a spike, says to just try something or just build it, or works
on a throwaway or hobby project where nothing depends on the code. When the result ships to users or other code will
be built on it, use Build a feature (`feature.md`).

## Who decides

- The agent decides everything about how it is built: the stack, the structure, and the shortcuts. It does not stop for
  design approval. Where the request leaves something open, it picks, keeps going, and names the choice in its reply.
- The user decides what to try next, and whether the prototype becomes real.
- A prototype does not touch production systems, shared environments, or real data without the user's go-ahead, and
  secrets stay out of commits. These hold however quick the cycle is.

## Steps

1. State in one line what the prototype is meant to show, and how the user will see it.
2. Pick the shortest path: the stack already in the project, or the lightest one that works. Hardcoded values,
   in-memory state, and one long file are all fine. In a project that is itself a prototype, work where the user
   works. For a proof of concept inside a production codebase, work on a throwaway branch or outside the repository,
   and say which.
3. Build the thinnest version that runs end to end first, then run it yourself. Seeing it work is the check; do not
   write a test suite.
4. Show the user how to run it and what it does now, take their reaction, and go again. Build everything they asked
   for in one cycle without stopping for approval in between.
5. Commit at each working state so a cycle can be undone. A short message is enough. Do not open a PR unless asked.
6. Keep a list, as you go, of the shortcuts that would matter in production.

## Done

After each cycle, the reply says what works now, how to run or see it, and what the agent chose where the request left
it open. It says plainly that the code is a prototype. When the user wants to make it real, the reply gives the list of
shortcuts, and the next playbook is Design or Build a feature, where the user decides whether to harden the
prototype or rebuild it.
