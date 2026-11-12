#!/usr/bin/env python3
"""Grade one trial against tests/rubric.md with an LLM judge, from inside a Harbor verifier.

Usage: python3 /tests/judge.py --repo <dir> --base <commit> [--extra name=value ...]

The source of truth is benchmarking-the-harness/assets/judge.py; create-benchmark copies it into
each task's tests/, so a task stays self-contained.

Reads the trace and request the agent left in /logs/artifacts/agent (events.jsonl, instruction.md),
redacts the environment (skills, instruction files) so the judge cannot tell variants apart,
runs opencode as the judge in an empty home, and writes /logs/verifier/reward.json: one key
per rubric criterion (score / 2), each --extra value, and "reward", the mean of all of them.
/tests/redact.tsv, if present, adds `regex<TAB>replacement` rewrites for giveaway phrases.

Environment: JUDGE_MODEL (provider/model) and that provider's API key, from [verifier.env].
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TESTS = Path("/tests")
AGENT = Path("/logs/artifacts/agent")
VERIFIER = Path("/logs/verifier")
ENV_PATH = re.compile(r"\.config/opencode|\.agents/skills|\.claude/skills|AGENTS\.md|CLAUDE\.md|/runtime/skills")
CRITERION = re.compile(r"^##\s+(\S+?):", re.MULTILINE)


def diff(repo: Path, base: str) -> str:
    """Everything the agent changed since base, untracked files included, without touching the repo."""
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "GIT_INDEX_FILE": f"{tmp}/index"}
        git = ["git", "-c", "safe.directory=*", "-C", str(repo)]
        subprocess.run([*git, "add", "-A"], env=env, check=True)
        return subprocess.run([*git, "diff", "--cached", base], env=env, check=True, capture_output=True, text=True).stdout


def events() -> list[dict]:
    path = AGENT / "events.jsonl"
    if not path.is_file():  # e.g. the oracle agent, which leaves no trace
        return []
    lines = path.read_text().splitlines()
    return [json.loads(line) for line in lines if line.startswith("{")]


def render_trace(evts: list[dict]) -> tuple[str, str]:
    """Return (trace, final reply), with every trace of the environment removed."""
    skills = {
        value
        for e in evts
        if e.get("type") == "tool_use" and e["part"].get("tool") == "skill"
        for value in e["part"].get("state", {}).get("input", {}).values()
        if isinstance(value, str)
    }
    names = "|".join(re.escape(s) for s in sorted(skills, key=len, reverse=True))
    mention = re.compile(rf"`?\b({names})\b`?( skill)?", re.IGNORECASE) if names else None
    rewrites = []
    if (TESTS / "redact.tsv").is_file():
        pairs = [line.split("\t", 1) for line in (TESTS / "redact.tsv").read_text().splitlines() if "\t" in line]
        rewrites = [(re.compile(pattern, re.IGNORECASE), replacement) for pattern, replacement in pairs]

    def clean(text: str) -> str:
        if mention:
            text = mention.sub("[guidance]", text)
        for pattern, replacement in rewrites:
            text = pattern.sub(replacement, text)
        return text

    def short(value: object, limit: int) -> str:
        text = value if isinstance(value, str) else json.dumps(value)
        return text if len(text) <= limit else text[:limit] + f" ...[{len(text) - limit} chars cut]"

    out, replies = [], []
    for e in evts:
        part = e.get("part", {})
        if e["type"] == "text":
            replies.append(part.get("text", ""))
            out.append(f"\nASSISTANT:\n{clean(part.get('text', ''))}\n")
        elif e["type"] == "tool_use":
            replies.clear()
            state = part.get("state", {})
            raw = json.dumps(state.get("input", {})) + str(state.get("output") or state.get("error") or "")
            if part.get("tool") == "skill" or ENV_PATH.search(raw) or (mention and mention.search(raw)):
                continue  # dropped without a marker: a count of markers reveals the variant
            out.append(f"TOOL {part.get('tool')}: {clean(short(state.get('input', {}), 600))}")
            out.append(f"  => {clean(short(state.get('output') or state.get('error') or '', 1500))}")
        elif e["type"] == "error":
            out.append(f"ERROR: {clean(json.dumps(e.get('error')))}")
    return "\n".join(out), clean("\n".join(replies))


def instruction() -> str:
    path = AGENT / "instruction.md"
    return path.read_text() if path.is_file() else "(not recorded)"


def judge(review: Path, criteria: list[str]) -> dict:
    model = os.environ["JUDGE_MODEL"]
    provider, model_id = model.split("/", 1)
    home = Path(tempfile.mkdtemp())
    (home / ".config/opencode").mkdir(parents=True)
    config = {"provider": {provider: {"models": {model_id: {}}}}, "share": "disabled", "autoupdate": False}
    (home / ".config/opencode/opencode.json").write_text(json.dumps(config))
    prompt = f"""You are grading how well a coding agent handled a task. Everything is in {review}:
- task.md: the request the agent received, word for word
- rubric.md: the criteria ({", ".join(criteria)}), each scored 0, 1 or 2 with anchors
- reference.patch: one accepted solution; other approaches that meet the criteria score the same
- trace.txt: what the agent did and said, in order
- diff.patch: the agent's final change to the repository
- reply.md: the agent's final message to the user

Read every file before scoring. Follow the anchors literally and ground each score in the trace or diff, citing what you saw. Do not reward length or style.
Write {review}/verdict.json as {{"<criterion id>": {{"score": 0|1|2, "why": "..."}}}} with exactly these ids: {", ".join(criteria)}."""
    env = {**os.environ, "HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"), "XDG_DATA_HOME": str(home / ".local/share")}
    with (VERIFIER / "judge.jsonl").open("w") as log:
        subprocess.run(
            ["opencode", "run", "--standalone", "--auto", "--format", "json", "-m", model, "--", prompt],
            cwd=review, env=env, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, check=False,
        )
    verdict = json.loads((review / "verdict.json").read_text())
    missing = set(criteria) - verdict.keys()
    if missing:
        sys.exit(f"verdict misses criteria {sorted(missing)}")
    return verdict


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--extra", action="append", default=[], help="name=value, a reward in [0, 1] from a check")
    args = parser.parse_args()

    rubric = (TESTS / "rubric.md").read_text()
    criteria = CRITERION.findall(rubric)
    if not criteria:
        sys.exit("rubric.md has no '## <id>: <title>' criteria")

    review = Path(tempfile.mkdtemp())
    trace, reply = render_trace(events())
    (review / "task.md").write_text(instruction())
    (review / "rubric.md").write_text(rubric)
    shutil.copy(TESTS / "reference.patch", review / "reference.patch")
    (review / "trace.txt").write_text(trace)
    (review / "reply.md").write_text(reply)
    (review / "diff.patch").write_text(diff(args.repo, args.base))

    verdict = judge(review, criteria)
    shutil.copy(review / "verdict.json", VERIFIER / "verdict.json")
    shutil.copy(review / "trace.txt", VERIFIER / "trace.txt")
    rewards = {c: verdict[c]["score"] / 2 for c in criteria}
    rewards.update({k: float(v) for k, v in (e.split("=", 1) for e in args.extra)})
    rewards["reward"] = sum(rewards.values()) / len(rewards)
    (VERIFIER / "reward.json").write_text(json.dumps(rewards))
    print(json.dumps(rewards))


if __name__ == "__main__":
    main()
