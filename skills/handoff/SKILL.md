---
name: handoff
description: Write a handoff prompt that carries the useful context of the current session into a fresh agent session the user starts by pasting it in. Use when the user says "handoff", "hand this off", "write a prompt for a new session", "summarize this for the next agent", or wants to continue the work with a clean context. Not for summaries meant for humans (PR descriptions, status updates).
argument-hint: "[what the next session should do]"
---

# Handoff

The user is about to start a new session with an empty context and paste in what you write. The next agent knows
nothing of this session: not the goal, not what you read, not what failed. Your job is to give it the context that
took this session effort to obtain, so it can start working instead of re-discovering.

The handoff is a prompt for an agent, not a report for a human. Write it to the next agent, in the second person.

## Gather before writing

1. Work out what the next session is for. Use the user's argument if they gave one. Otherwise infer it from where
   the work stopped, and state your assumption in the handoff's goal. If the session covered several threads,
   ask which one to hand off rather than packing in all of them.
2. Check the current state instead of trusting your memory of it:
   - `git status`, the current branch, and `git log` for commits made in this session.
   - Line numbers by `grep -n` on the current files, since edits during the session shifted them.
   - Whether the tests or commands you cite still pass or fail the way you say.
3. Sort what you know into verified facts and hypotheses. The next agent will act on what you write, so it must
   be able to tell which is which.

## What to include

Use these sections, in this order. Leave out a section that would be empty.

- **Goal** - what the next session should achieve, and how it will know it is done.
- **Background** - why this work exists, and the decisions already made together with the reasons. A decision
  without its reason gets re-litigated.
- **Current state** - branch, commits, uncommitted changes, what works, and what is broken right now.
- **Relevant files** - paths relative to the repository root (or absolute outside a repository), with line
  numbers where it helps, and one line on why each matters. Prefer pointing to a file over pasting it, since the
  next agent can read files.
- **Code snippets** - only what the next agent cannot cheaply read itself, or what is the crux: the key lines of
  a function, an error message or stack trace, a command and its output, a working invocation that took trial and
  error to find. Keep each one short and say where it comes from.
- **Findings** - what this session learned: how the system actually behaves, root causes, surprising facts. Mark
  hypotheses as such, with what would confirm them.
- **Dead ends** - approaches tried and abandoned, and why. This keeps the next agent from repeating them.
- **Edge cases and pitfalls** - traps in the code, tooling, or environment that bit this session or are likely to
  bite the next.
- **Next steps** - concrete, ordered instructions, as far as they are known. Say where they are not known.
- **Open questions** - what still needs deciding, and whether the user or the agent decides it.

## What to leave out

- The story of the session. Give conclusions, not the chronology of how you reached them.
- Anything the next agent picks up on its own: the content of instruction files such as `AGENTS.md` or
  `CLAUDE.md`, general knowledge, files it will read anyway.
- Pleasantries and preamble ("Here is the handoff", "Good luck").

Keep it dense. A handoff that is too long buries the important parts and fills the fresh context the user wanted.
Every line should save the next agent a step or a mistake.

## Output

The user copies the handoff from the terminal, so the raw markdown must survive the copy:

- Put the whole handoff in a single fenced block with four backticks (` ```` `), so it is shown unrendered and
  the three-backtick code snippets inside it do not end the block.
- Write nothing inside the block that is not part of the prompt.
- After the block, at most one line, such as the assumption you made about the goal if you did not ask.

If the user asks for a file instead, write the handoff to the path they give, or to `HANDOFF.md` in the
repository root, without the outer fence, and tell them the path. Do not commit it.
