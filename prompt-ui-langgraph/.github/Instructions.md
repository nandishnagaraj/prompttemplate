# Coding Standards & Best Practices

> These standards apply to the full `prompt-ui-langgraph` monorepo:
> - **Frontend** — Next.js 14 (App Router), TypeScript, React 18 (`apps/web/`)
> - **Backend** — FastAPI, Python 3.11, Pydantic v2 (`services/orchestrator-api/`)
> - **Orchestration** — LangGraph, LangChain (`services/orchestrator-api/orchestrator_pkg/`)

---

## General Principles

- **Clarity over cleverness** — write code a new team member can read without needing to ask questions.
- **One responsibility per function/class** — functions should do one thing and do it well.
- **No dead code** — remove commented-out code and unused imports before committing.
- **No magic values** — every non-obvious literal must be a named constant or pulled from config/env.
- **Fail fast** — validate inputs at the boundary (API layer, component props); never let bad data propagate deep.

---

## Python (FastAPI / LangGraph)

### Style
- Follow **PEP 8**. Maximum line length is **100 characters**.
- Use **type hints** on every function signature — parameters and return types.
- Use `from __future__ import annotations` at the top of every module.
- Prefer `pathlib.Path` over raw string paths.
- Use f-strings; avoid `%` formatting or `.format()`.

### Project Layout
```
app/
  main.py          # FastAPI app factory, routers, middleware only
  auth.py          # OAuth routes and session helpers
  settings.py      # Pydantic Settings — all env vars centralised here
  <domain>.py      # One module per domain (github_client, bitbucket_client, …)
orchestrator_pkg/  # LangGraph nodes, state, runner — no FastAPI imports here
```

### FastAPI
- Define **one Pydantic model per request/response shape** — never use raw `dict`.
- Use `Field(...)` with constraints (`min_length`, `ge`, `le`) for all request fields.
- Never put business logic inside a route function — delegate to a service module.
- Return meaningful HTTP status codes (`400` for bad input, `401` for auth, `500` for infra).
- Add CORS origins explicitly; never use `allow_origins=["*"]` in non-local configs.

### Settings & Secrets
- All configuration lives in `app/settings.py` via `os.getenv()`.
- `load_dotenv()` is called once at module load in `settings.py` — nowhere else.
- **Never hardcode secrets**. Never commit `.env` (it is gitignored). Commit only `.env.example`.
- Rotate any secret that was accidentally logged or committed.

### Error Handling
- Raise `HTTPException` with a descriptive `detail` string at the API boundary.
- Catch specific exception types; never use bare `except:`.
- Log the original exception before re-raising or transforming it.

### LangGraph / Orchestration
- Keep node functions **pure and stateless** — they read from `state` and return a state update dict.
- Validate node output (required sections present) before passing to the next node.
- Never import FastAPI or `app.*` modules inside `orchestrator_pkg/`.
- Define `ALL_ARTIFACTS`, `ARTIFACT_NODE`, `NODE_DEPS`, `NODE_ORDER` in `runner.py` — do not scatter them.

### Testing
- Every new public function in `app/` should have at least one unit test.
- Use `pytest` with `httpx.AsyncClient` for route tests.
- Mock external network calls (`requests`, OpenAI, Bitbucket/GitHub APIs) — tests must be offline-safe.

---

## TypeScript / Next.js (App Router)

### Style
- Use **TypeScript strict mode** (`"strict": true` in `tsconfig.json`).
- Maximum line length is **100 characters**.
- Use `const` by default; only use `let` when reassignment is necessary.
- Prefer named exports over default exports for components and utilities.
- Use `interface` for object shapes that describe data; use `type` for unions and mapped types.

### Component Rules
- One component per file. File name matches the exported component name (PascalCase).
- Props must be explicitly typed — never use `any` or `object`.
- Keep components **presentational** — data fetching belongs in Server Components or custom hooks.
- Extract repeated JSX fragments (> 5 lines) into a separate component.

### Data Fetching
- Use **Server Components** for initial data reads; avoid `useEffect` for fetching.
- All API calls go through a single base URL configured via `NEXT_PUBLIC_API_BASE_URL`.
- Handle loading and error states explicitly — never render stale/undefined data silently.

### Environment Variables
- Public vars are prefixed `NEXT_PUBLIC_`. Never expose sensitive values with this prefix.
- All env vars used in the app must be listed in `apps/web/.env.example`.

### File Structure
```
app/
  layout.tsx     # Root layout — fonts, global providers only
  page.tsx       # Route entry points — thin orchestration layer
  components/    # Shared UI components
  hooks/         # Custom React hooks
  lib/           # Pure utility functions, API client helpers
```

---

## Git & Workflow

### Commit Messages (Conventional Commits)
```
<type>(<scope>): <short summary>
```
| Type | When to use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code change with no behaviour change |
| `chore` | Tooling, deps, CI config |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |

Example: `fix(auth): store bitbucket refresh_token in session`

### Branch Naming
```
<type>/<short-description>
```
Examples: `feat/gemini-provider`, `fix/bitbucket-token-expiry`, `chore/update-deps`

### Pull Requests
- Title follows the conventional commit format.
- Include a short description of **what** changed and **why**.
- Reference any related issue numbers.
- All CI checks must pass before merging.
- At least one reviewer approval required for changes to `main`.

### What Must Never Be Committed
- `.env` files with real secrets
- `node_modules/`, `.next/`, `__pycache__/`, `*.pyc`
- Large binary files (> 10 MB) — use Git LFS or external storage
- Credentials, API keys, tokens in any file

---

## Security

- Validate and sanitise all user-supplied input before use.
- Use `httponly=True, samesite="lax"` on session cookies (already enforced in `auth.py`).
- Never log OAuth tokens, access tokens, or refresh tokens.
- Enforce `ALLOW_PAT_FALLBACK=false` in production to require proper OAuth.
- Keep dependencies up to date; review `pip` and `npm` audit output regularly.
- Follow [OWASP Top 10](https://owasp.org/www-project-top-ten/) — particularly broken access control, injection, and cryptographic failures.

---

## Environment Setup (New Contributor)

```bash
# 1. Copy env files
cp services/orchestrator-api/.env.example services/orchestrator-api/.env
cp apps/web/.env.example apps/web/.env

# 2. Install Python deps
python -m venv venv && source venv/bin/activate
pip install -r services/orchestrator-api/requirements.txt

# 3. Start API
python -m uvicorn app.main:app \
  --app-dir services/orchestrator-api \
  --host 0.0.0.0 --port 8000

# 4. Install and start web
npm --prefix apps/web install
npm --prefix apps/web run dev -- -p 3003
```

Open: http://localhost:3003
