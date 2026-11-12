#!/usr/bin/env bash
# global-layer.sh <layer-dir>
# Snapshots the user's skills and global AGENTS.md into <layer-dir>/{skills/,AGENTS.md},
# resolving symlinks and stripping the benchmarking skills and other leaks. A variant's
# job config points `skills:` at <layer-dir>/skills and `kwargs.instructions` at
# <layer-dir>/AGENTS.md.
set -euo pipefail

dest="${1:-}"
if [ -z "$dest" ]; then
	echo "usage: $0 <layer-dir>" >&2
	exit 1
fi
skills="${SKILLS_DIR:-$HOME/.agents/skills}"
config="${OPENCODE_DIR:-$HOME/.config/opencode}"

mkdir -p "$dest/skills"
rsync -aL \
	--exclude 'benchmarking-the-harness' \
	--exclude 'create-benchmark' \
	--exclude 'benchmark-*' \
	--exclude 'synced' \
	"$skills/" "$dest/skills/"
if [ -e "$config/AGENTS.md" ]; then
	cp -L "$config/AGENTS.md" "$dest/AGENTS.md"
fi

if grep -rlIiE '\b(benchmark|rubric|arena|harbor)\b' "$dest" >/dev/null; then
	echo "check these files for leaks:" >&2
	grep -rlIiE '\b(benchmark|rubric|arena|harbor)\b' "$dest" >&2
fi
