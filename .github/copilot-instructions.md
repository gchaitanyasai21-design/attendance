<!--
This file is an AI-agent guide scaffold. It was generated because no
existing agent instruction files were found in the workspace. Customize
the sections below with project-specific details (architecture, build
commands, test commands, important file locations) so future agents can
be immediately productive.
-->
# Copilot / AI Agent Instructions

Purpose: Give concise, actionable guidance for an AI coding agent working
in this repository. Keep this file short (20–50 lines) and update it with
concrete project details after reviewing the codebase.

1) Quick orientation
- **Repo top-level cues:** look for `package.json`, `pyproject.toml`,
  `requirements.txt`, `go.mod`, `Cargo.toml`, `Dockerfile`, or `Makefile`
  to infer language and build system.
- **Primary source roots:** expect `src/`, `app/`, `lib/`, or top-level
  language folders (e.g., `packages/` for monorepos). If unclear, run
  a workspace file search for `src/**` and `**/*.ts|**/*.py|**/*.go`.

2) Architecture & high-level responsibilities (how to discover)
- Find service boundaries by locating subfolders with their own
  manifest files: `package.json`, `pyproject.toml`, `go.mod`, or
  `Dockerfile` per subfolder. Those are likely independent services.
- Look for `README.md` files in subfolders — they often explain the
  responsibility of a service or component. Use them as authoritative
  short summaries for the agent.

3) Critical developer workflows (how to find and run)
- To discover build/test/debug commands: check `package.json` scripts,
  `Makefile` targets, `.github/workflows/*.yml`, and `tox.ini` or
  `pyproject.toml`'s `[tool.poetry.scripts]`/`[tool.pytest]` sections.
- When running commands locally, prefer the project-standard method.
  If `npm`/`pnpm`/`yarn` exist pick the one in `packageManager` or lock
  files (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`).

4) Project-specific conventions to look for
- Naming: check for consistent directory names (e.g. `api/`, `worker/`,
  `web/`). Use those to infer responsibility and where to place new
  features or tests.
- Error handling / logging: search for centralized logger files
  (e.g., `logger.js`, `logging.py`, `internal/logging`) and mirror
  the existing patterns for new code.

5) Integration points & external dependencies
- Look for environment examples `(.env.example, .env.sample)`,
  `config/*.yaml` or `config/*.json` to find required external services
  (DBs, queues, third-party APIs). Agents should not hardcode credentials
  — use config files and mention required env var names in PR descriptions.

6) Safe/approved automated actions
- Create focused changes: one logical change per PR with tests and
  relevant updates to `README` or docs.
- When adding or modifying CI, run local lint/test commands first and
  include a short summary of expected CI steps in the PR body.

7) What to include in PR descriptions created by the agent
- Short motivation: why the change is needed.
- Files changed and the high-level design choice.
- Commands to run locally to verify (exact commands found in repo).

8) If you (the agent) cannot determine something
- Ask a human for the missing authoritative information (build command,
  service boundaries, or environment variables). Provide the precise
  file or location where the information would be placed.

9) Housekeeping for maintainers
- After you update this file with concrete commands or file paths,
  agents will use those instead of inferring them. Keep this file
  minimal and concrete.

---
Notes: Replace the discovery heuristics above with concrete examples
from this repository (for example: `Run tests: `npm test` in
`packages/api`), once you populate the repo or provide the missing
project files to the agent.
