# skills

My Agent Skills, written to work across harnesses: Claude Code, Codex, and
opencode. Each skill is a directory with a `SKILL.md` under a namespace
folder, `skills/felixscherz/<skill>/`. Other namespaces, such as vendored
skills, go next to it as `skills/<namespace>/`. Skills can be grouped further
inside a namespace, as long as no folder above a `SKILL.md` has one of its own.

## Install

Pick one of the two methods. They install into the same directories, so do
not mix them for the same skill.

### Pinned copy with `npx skills`

Copies the skills into `~/.agents/skills/` and links them into each agent's
skill directory. Use this on machines where you only consume the skills.

```sh
npx skills add felixscherz/skills -g -s '*' -a claude-code -a codex -a opencode
```

Update with `npx skills update -g`, remove with `npx skills remove -g`.

### Live symlinks from a clone

Symlinks each namespace folder from a local clone into `~/.agents/skills/`
(opencode, Codex) and `~/.claude/skills/` (Claude Code). The harnesses find
the skills nested inside it. Edits in the clone take effect immediately. Use
this where you develop the skills.

```sh
git clone git@github.com:felixscherz/skills.git ~/workspaces/personal/skills
~/workspaces/personal/skills/link.sh
```

Skills added to a namespace show up without a rerun. Rerun `link.sh` after
adding, renaming, or removing a namespace. It only touches symlinks that
point into the clone, and reports anything else in its way instead of
replacing it. `unlink.sh` removes the links again.

To switch from `npx skills` to symlinks, run `npx skills remove -g` for the
skills first, then `link.sh`. Otherwise each skill is installed twice, once
flat and once inside the namespace.
