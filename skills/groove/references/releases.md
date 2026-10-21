# Releases

## The rule

For Python projects that publish versioned artifacts, default to Git tags as
the version source, hatch-vcs for package versions, and git-cliff for the
changelog. Keep an established release mechanism unless changing it is part
of the task. Do not introduce publishing to a repository that does not need it.

- **One version source.** Stable release tags are
  `v<major>.<minor>.<patch>`, such as `v0.1.0`, without leading zeroes.
  A clean checkout of that tag builds package version `0.1.0`. Untagged
  commits get development versions. Do not maintain a second version literal
  in `pyproject.toml` or application code, or move a published tag.
- **Generate release notes from commits.** Use Conventional Commits and
  git-cliff with a committed `cliff.toml` and `CHANGELOG.md`. Group changes,
  expose breaking changes, and omit release preparation commits. Decide
  explicitly whether non-conventional commits are omitted; do not silently
  lose user-visible changes. Any commit links point to the project's host.
- **Prepare explicitly.** Provide commands to regenerate the changelog,
  prepare it for a chosen tag, suggest the next version, and build artifacts.
  Use the existing task runner, whether Make, just, or another tool. Version
  suggestions are advice, not a compatibility decision. Validate a supplied
  tag before changing files, and quote command arguments.
- **Check, build, then publish.** A release pipeline matches only valid
  release tags, fetches full history and tags, and runs the repository's
  single check command before building. Build from the clean tagged commit.
  Generate host release notes only for that tag's changes. Publishing cannot
  run when validation or the build fails.
- **Choose distribution separately.** GitHub or GitLab releases, a Python
  package index, and a container registry are project choices. Do not infer
  public PyPI publishing, Docker packaging, credentials, or network exposure
  from the versioning convention. Keep downloadable artifacts for the
  supported lifetime of a release; a release page linking to expired CI
  artifacts is not a working distribution channel.
- **Document the procedure.** Put prerequisites, preparation, review, tagging,
  and publication steps in `docs/releases.md`, linked from `CONTEXT.md` and
  the README. Tool choices and release commands do not by themselves need an
  ADR. Distribution, security, and compatibility decisions may need one; see
  `project-context.md`. Setting up a release mechanism does not authorize
  creating or pushing an actual release.

## Why

A version literal, a Git tag, and a manually edited changelog can disagree.
Deriving the package version from the tag removes one source of drift.
Generating notes from commits makes release preparation repeatable, while
review still decides which compatibility promise the version makes.

The release host should not determine package versioning. The same tagged
source can produce a Python distribution or be packaged into a container
without inventing a separate version for each artifact.

## Example

For a project already using Hatchling, replace its static project version
with dynamic versioning and extend its build configuration:

```toml
[project]
name = "acme"
dynamic = ["version"]

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"

[tool.hatch.version.raw-options]
tag_regex = '^v(?P<version>(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*))$'

[tool.hatch.build.hooks.vcs]
version-file = "src/acme/_version.py"
```

This is a configuration excerpt, not a replacement for the project's
metadata. Add `git-cliff` and `hatch-vcs` to the development dependencies and
refresh the lockfile. Ignore the generated `src/acme/_version.py` and build
output in Git. Read the installed version through package metadata or the
generated version module, not another constant. If the project uses a
different build backend, preserve it unless migration is in scope.

Use the same stable tag pattern in git-cliff and the release pipeline:

```toml
[git]
conventional_commits = true
filter_unconventional = true
protect_breaking_commits = true
tag_pattern = '^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'

[bump]
initial_tag = "v0.1.0"
```

Complete `cliff.toml` with a changelog header, a body grouped by change type,
and commit parsers. Skip `chore(release): ...` preparation commits, but retain
breaking changes even when their commit type would otherwise be skipped.
The first release version is an explicit choice; `v0.1.0` is a starting
default, not a claim that every new project has the same maturity.

For a uv-based project, task-runner recipes can wrap these commands:

```sh
uv run --locked git-cliff --output CHANGELOG.md
uv run --locked git-cliff --tag v0.1.0 --output CHANGELOG.md
uv run --locked git-cliff --bumped-version
uv build --no-sources
```

Preparing a changelog does not create a tag. Review and commit it through
the project's normal integration process. Tag the resulting clean commit,
then build from it. In the tag pipeline, generate release notes with
`uv run --locked git-cliff --latest --strip all`; send that output to the
project's release host. Use locked tool environments when available.

Build from a clone with full history and tags or a generated source
distribution. A host's source archive usually lacks the Git metadata needed
to derive the version. Do not add a fallback release version that would hide
missing history or a broken build setup.

## Codify it

Add release verification to the existing check command. Use isolated
temporary Git repositories or clones, never create verification tags in the
developer's working repository. Avoid recursive checks when building a
fixture package. Verify the actual build and git-cliff behavior rather than
only asserting configuration keys:

- Invalid tag names are rejected before a preparation command changes files.
  Include missing components, leading zeroes, and prerelease suffixes when
  only stable releases are supported.
- A clean exact tag builds a wheel and source distribution whose metadata
  version matches the tag without `v`. Verify that a wheel can also be built
  from the source distribution without Git metadata.
- A later untagged commit builds a development version, not the released one.
- With two release tags, the latest release notes contain new changes but
  exclude changes from the earlier release and preparation commits.
- The lockfile remains valid at a release tag. Packaged assets and installed
  entry points remain present when relevant to the application.

Keep those checks non-publishing and runnable locally. Validate pipeline
configuration with the host's CI linter when changing it. Tag matching,
check/build ordering, and artifact retention belong in CI configuration;
test them where the host offers pipeline simulation. None of these checks
should need publishing credentials or create a release.

The example project does not yet implement these release checks. Adding
this reference is not evidence that a repository enforces them.

## Review by hand

- Does the chosen version match the actual compatibility change? Are data
  schema versions kept distinct from application release versions?
- Are the release notes useful to users, including breaking changes and
  any migration steps, or just a dump of internal maintenance commits?
- Does the chosen publishing destination match deployment and access
  requirements? Are signing, approvals, or an SBOM required by the project?
- Can users still download artifacts for supported releases? Do the docs
  distinguish available distribution from future packaging plans?
- Does preparation respect branch protection and the team's review process,
  without treating a setup request as permission to tag or publish?
