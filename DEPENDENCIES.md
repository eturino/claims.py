# Dependency State

Last reviewed: 2026-11-16

State file for the `upgrade-deps` skill (rules: `~/.agents/custom-skills/upgrade-deps/SKILL.md`).
Full per-pass detail lives in `git log -p DEPENDENCIES.md Pipfile`.

## House rules

- **Package manager:** Pipenv. `Pipfile` pins nothing (`"*"`) and `Pipfile.lock` is not tracked (`make clean` deletes it), so every install takes the latest release. `mise.toml` also pins uv, which nothing uses yet.
- **Runtime:** Python 3.13.13 (`mise.toml`). The Makefile reads the version from the `python3` on PATH; the local `.python-version` is gitignored.
- **Green gate:** `make` (pytest, mypy, isort, black, flake8, wheel build). CI runs the same on push to master.

## Major Upgrades Blocked

Every row below was deferred by Edu on 2026-11-16 ("not now, next deps pass"), not blocked upstream. Not tried yet.

| Package | Current | Latest | Blocker | Since | Re-checked | Last tried |
| ------- | ------- | ------ | ------- | ----- | ---------- | ---------- |
| Python (runtime, `mise.toml`) | 3.13.13 | 3.15.2 | Deferred to the next pass | 2026-11-16 | 2026-11-16 | - |
| Pipenv to uv | Pipenv, no lock | uv with `uv.lock` | Deferred. Same move `key_set.py` and `ynab-sdk-openapi-python` made; adds the 5-day gate and a lockfile | 2026-11-16 | 2026-11-16 | - |
| `actions/checkout` | v2 (SHA-pinned) | v5 | Deferred to the next pass | 2026-11-16 | 2026-11-16 | - |

## Upgrade history

- **2026-11-16** CI fixed (empty `--python`), current black formatting applied, workflows SHA-pinned with mise (from June 2026).
