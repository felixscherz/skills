#!/usr/bin/env bash
# Symlinks every skill in this repo into the global skill directories, so edits
# here take effect immediately. Rerun after adding or removing a skill.
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

	for skill in "$SRC"/*/; do
		skill="${skill%/}"
		[[ -f "$skill/SKILL.md" ]] || continue
		dest="$target/$(basename "$skill")"
		if [[ -L "$dest" ]]; then
			if [[ "$(readlink "$dest")" == "$skill" ]]; then
				continue
			fi
			if ! is_ours "$dest"; then
				echo "conflict: $dest links to $(readlink "$dest")" >&2
				conflicts=1
				continue
			fi
			rm "$dest"
		elif [[ -e "$dest" ]]; then
			echo "conflict: $dest exists, remove it first (installed with npx? run: npx skills remove -g $(basename "$skill"))" >&2
			conflicts=1
			continue
		fi
		ln -s "$skill" "$dest"
		echo "linked $dest"
	done

	# Drop links to skills that were removed or renamed in this repo.
	for link in "$target"/*; do
		if is_ours "$link" && [[ ! -e "$link" ]]; then
			rm "$link"
			echo "removed stale $link"
		fi
	done
done

exit "$conflicts"
