FROM localhost/opencode-base

# Toolchains the work needs, pinned to the versions it used, e.g. Go:
# RUN case "$(uname -m)" in aarch64|arm64) arch=arm64 ;; x86_64) arch=amd64 ;; esac \
#  && curl -fsSL "https://go.dev/dl/goX.Y.Z.linux-${arch}.tar.gz" | tar -xz -C /usr/local
# ENV PATH=/usr/local/go/bin:/root/go/bin:$PATH GOTOOLCHAIN=local

# The repository at the base commit, plus any uncommitted work in progress.
# The start tree is written to the object store so the verifier can diff against it.
COPY REPO.bundle /tmp/
RUN git clone --quiet /tmp/REPO.bundle /root/REPO \
 && cd /root/REPO \
 && git remote remove origin \
 && git reflog expire --expire=now --all \
 && rm /tmp/REPO.bundle \
 && test "$(git rev-parse HEAD)" = BASE_COMMIT \
 && GIT_INDEX_FILE=/tmp/start.index git add -A \
 && test "$(GIT_INDEX_FILE=/tmp/start.index git write-tree)" = START_TREE \
 && rm /tmp/start.index
WORKDIR /root/REPO
# Build and test once, so a broken fixture fails here and caches are warm.
# RUN go build ./... && go test ./...
