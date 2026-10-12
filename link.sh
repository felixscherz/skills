#!/usr/bin/env bash
# Symlinks each namespace folder under skills/ (such as skills/felixscherz) into
# the global skill directories, so edits here take effect immediately. Skills
# added inside a namespace show up without a rerun. Rerun after adding,
# renaming, or removing a namespace.
# For a pinned copy instead, install with `npx skills` (see README.md).
set -e
source "$(dirname "$0")/lib.sh"

conflicts=0
for target in "${TARGETS[@]}"; do
	if [[ -L "$target" ]]; then
		echo "conflict: $target is a symlink to $(readlink "$target"), replace it with a directory" >&2
		conflicts=1
		continue
	fi
	mkdir -p "$target"

	for ns in "$SRC"/*/; do
		ns="${ns%/}"
		# Harnesses find skills nested in the linked folder, so a namespace only
		# needs a SKILL.md somewhere below it.
		[[ -n "$(find "$ns" -name SKILL.md -print -quit)" ]] || continue
		dest="$target/$(basename "$ns")"
		if [[ -L "$dest" ]]; then
			if [[ "$(readlink "$dest")" == "$ns" ]]; then
				continue
			fi
			if ! is_ours "$dest"; then
				echo "conflict: $dest links to $(readlink "$dest")" >&2
				conflicts=1
				continue
			fi
			rm "$dest"
		elif [[ -e "$dest" ]]; then
			echo "conflict: $dest exists, remove it first" >&2
			conflicts=1
			continue
		fi
		ln -s "$ns" "$dest"
		echo "linked $dest"
	done

	# Drop links to namespaces that were removed or renamed in this repo.
	for link in "$target"/*; do
		if is_ours "$link" && [[ ! -e "$link" ]]; then
			rm "$link"
			echo "removed stale $link"
		fi
	done
done

exit "$conflicts"
