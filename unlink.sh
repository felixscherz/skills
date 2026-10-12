#!/usr/bin/env bash
# Removes the symlinks link.sh created. Leaves everything else in the skill
# directories alone, including skills installed with `npx skills`.
set -e
source "$(dirname "$0")/lib.sh"

for target in "${TARGETS[@]}"; do
	[[ -d "$target" && ! -L "$target" ]] || continue
	for link in "$target"/*; do
		if is_ours "$link"; then
			rm "$link"
			echo "removed $link"
		fi
	done
done
