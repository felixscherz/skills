# localhost/opencode-base, the image every benchmark task builds FROM: a plain
# Linux dev box with opencode baked in, so trials never install the agent.
# Built for the Docker daemon's own architecture (arm64 on Apple silicon),
# never emulated.
#   scripts/build-base.sh [opencode-version]
FROM debian:trixie-slim

ARG OPENCODE_VERSION

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# coreutils provides the stdbuf the agent pipes through; python3 runs the judge.
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      ca-certificates coreutils curl git less procps python3 ripgrep \
 && rm -rf /var/lib/apt/lists/*

RUN case "$(uname -m)" in aarch64|arm64) arch=arm64 ;; x86_64) arch=x64 ;; *) exit 1 ;; esac \
 && curl -fsSL "https://github.com/anomalyco/opencode/releases/download/v${OPENCODE_VERSION}/opencode-linux-${arch}.tar.gz" \
    | tar -xz -C /usr/local/bin opencode \
 && opencode --version

# A neutral identity, so a commit behaves as on a configured machine.
RUN git config --system user.name "Developer" \
 && git config --system user.email "dev@example.com" \
 && git config --system init.defaultBranch main
