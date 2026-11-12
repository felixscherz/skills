"""Harbor agent for opencode 2, baked into the task image by assets/base/Dockerfile.

Harbor's built-in opencode agent targets opencode 1: it installs Node and opencode on
every trial and passes flags opencode 2 no longer has. This agent checks the baked
version instead of installing, so a trial never runs an agent other than the one under
test, and runs `opencode run` with opencode 2 flags.

Besides Harbor's own `skills`, it installs a variant's global instruction file
(`instructions` kwarg) and leaves the trace and the request in /logs/artifacts/agent,
where a separate verifier (assets/judge.py) can read them.

    agents:
      - import_path: harbor_agents.baked_opencode:BakedOpenCode
        model_name: deepseek/deepseek-flash
        kwargs: {version: "2.2.7", instructions: layers/global/AGENTS.md}
        skills: [layers/global/skills]
"""

import shlex
from pathlib import Path
from typing import override

from pydantic import Field

from harbor.agents.installed.base import NonZeroAgentExitCodeError, with_prompt_template
from harbor.agents.installed.opencode import OpenCode, OpenCodeOptions
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext

ARTIFACTS = "/logs/artifacts/agent"


class BakedOpenCodeOptions(OpenCodeOptions):
    instructions: str | None = Field(
        default=None, description="AGENTS.md to install as opencode's global instruction file."
    )


class BakedOpenCode(OpenCode):
    options_model = BakedOpenCodeOptions

    def __init__(self, *args, instructions: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._instructions = Path(instructions).expanduser().resolve() if instructions else None

    @override
    def get_version_command(self) -> str | None:
        return "opencode --version"

    @override
    async def install(self, environment: BaseEnvironment) -> None:
        result = await environment.exec(command="opencode --version")
        found = (result.stdout or "").strip().removeprefix("opencode ").removeprefix("v")
        if result.return_code != 0 or (self._version and found != self._version):
            raise RuntimeError(
                f"image has opencode {found!r}, the job wants {self._version!r}: "
                "rebuild the base image with scripts/build-base.sh and the task images on top"
            )

    @override
    @with_prompt_template
    async def run(self, instruction: str, environment: BaseEnvironment, context: AgentContext) -> None:
        self._instruction = instruction
        if not self.model_name:
            raise ValueError("model_name must be provider/model")
        env = dict(self.model_connection.env)

        if command := self._build_register_skills_command():
            await self.exec_as_agent(environment, command=command, env=env)
        if command := self._build_register_config_command():
            await self.exec_as_agent(environment, command=command, env=env)
        if self._instructions:
            await self.exec_as_agent(environment, command="mkdir -p ~/.config/opencode", env=env)
            home = (await self.exec_as_agent(environment, command="printf %s ~", env=env)).stdout
            await environment.upload_file(self._instructions, f"{home}/.config/opencode/AGENTS.md")

        out = shlex.quote((self.environment_logs_dir / self._OUTPUT_FILENAME).as_posix())
        await self.exec_as_agent(
            environment,
            command=(
                "opencode run --standalone --auto --format json --thinking "
                f"-m {shlex.quote(self._execution_model_name())} -- {shlex.quote(instruction)} "
                f"2>&1 </dev/null | stdbuf -oL tee {out}"
            ),
            env=env,
        )

        # A separate verifier sees /logs/artifacts, not /logs/agent.
        await environment.exec(
            command=(
                f"mkdir -p {ARTIFACTS} && cp {out} {ARTIFACTS}/events.jsonl && "
                f"printf %s {shlex.quote(instruction)} > {ARTIFACTS}/instruction.md"
            )
        )
        if messages := self._error_messages():
            raise NonZeroAgentExitCodeError("opencode emitted error event(s): " + "; ".join(messages[:3]))
