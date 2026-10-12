# Shared by link.sh and unlink.sh.

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO/skills"

# opencode and Codex read ~/.agents/skills, Claude Code reads ~/.claude/skills.
TARGETS=("$HOME/.agents/skills" "$HOME/.claude/skills")

# True when $1 is a symlink into this repo's skills, dangling or not.
is_ours() {
	[[ -L "$1" && "$(readlink "$1")" == "$SRC"/* ]]
}
