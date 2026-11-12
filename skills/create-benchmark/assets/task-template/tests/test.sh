#!/bin/bash
# Checks run on a copy, so build output never reaches the diff the judge grades.
set -uo pipefail
copy="$(mktemp -d)"
cp -a /root/REPO "$copy/REPO"
tests=0
(cd "$copy/REPO" && TEST_COMMAND) >/logs/verifier/checks.txt 2>&1 && tests=1
python3 /tests/judge.py --repo /root/REPO --base START_TREE --extra "tests=$tests"
