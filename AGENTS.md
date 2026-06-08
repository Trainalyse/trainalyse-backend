# AGENTS.md

## Tech stack

- **Framework**: FastAPI, deployed as a [Cloudflare Python Worker](https://developers.cloudflare.com/workers/languages/python/) (`python_workers` compat flag).
- **Entrypoint**: `src/trainalyse-backend/main.py` — `Default(WorkerEntrypoint)` wrapping FastAPI via `asgi.fetch()`.
- **Package manager**: `uv` (uv.lock lockfile, no pip/poetry).
- **Python**: 3.13 (`.python-version` + `requires-python` in pyproject.toml).

## Commands

| Action | Command |
|---|---|
| Run tests | `uv run pytest` |
| Deploy to Cloudflare Workers | `uvx --from workers-py pywrangler deploy` (requires `CLOUDFLARE_API_TOKEN` env) |

No lint or typecheck config exists. Only test runs in CI.

## CI/CD

3-job pipeline on push to `main`:
1. `run-tests` — `uv run pytest`
2. `tag-and-release` — reads `project.version` from `pyproject.toml`, creates GitHub release if tag doesn't exist
3. `deploy-to-cloudflare` — deploys via pywrangler

Bump version in `pyproject.toml` to trigger a new release.

## Architecture notes

- The `Default` class name and `.fetch()` method are required by Cloudflare's Workers runtime (maps to FetchEvent).
- `asgi` module is a Cloudflare Workers built-in (not pip-installable).
- `workers-py` / `pywrangler` are dev dependencies only; they bundle the ASGI bridge for the Worker runtime.
- `.venv/`, `.venv-workers/`, `python_modules/`, `.wrangler/` are gitignored.
