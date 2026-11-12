#!/usr/bin/env bash
# build-base.sh [opencode-version]
# Builds localhost/opencode-base:<version> from assets/base for the Docker
# daemon's native architecture, and tags it as localhost/opencode-base:latest,
# which task Dockerfiles start FROM. The agent's version kwarg catches a
# mismatch between the job and the image.
set -euo pipefail

version="${1:-2.2.7}"
here="$(cd "$(dirname "$0")" && pwd)"
docker build --build-arg OPENCODE_VERSION="$version" \
	-t "localhost/opencode-base:$version" -t localhost/opencode-base:latest \
	"$here/../assets/base"
docker run --rm "localhost/opencode-base:$version" opencode --version
