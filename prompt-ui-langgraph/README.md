# Prompt Template UI + LangGraph + Git Provider Push (Local Demo)

## What It Does
- Git provider OAuth login (GitHub and Bitbucket)
- Runs the bundled LangGraph orchestrator to generate SDLC artifacts
- Writes outputs to `runs/<timestamp>/`
- Pushes `runs/<timestamp>/` into the selected repository under `runs/`

## Tech Stack

### Frontend
- Next.js `14.2.5` (App Router)
- React `18.3.1`
- React DOM `18.3.1`
- TypeScript typings (`@types/react`)

### Backend API
- Python `3.11` (Docker base image: `python:3.11-slim`)
- FastAPI `>=0.110.0`
- Uvicorn `>=0.27.0`
- Pydantic `>=2.0.0`
- Requests `>=2.31.0`

### Orchestration And LLM
- LangGraph `>=0.2.0`
- LangChain `>=0.1.0` (API layer) and `>=0.2.0` (bundled orchestrator)
- LangChain OpenAI integration (`langchain-openai >=0.1.0`)
- LangChain Gemini integration (`langchain-google-genai >=2.0.0`)
- Azure OpenAI client path via `AzureChatOpenAI`
- Gemini client path via `ChatGoogleGenerativeAI`
- OpenAI-compatible client path via `ChatOpenAI`

### Git And Auth
- GitPython `>=3.1.43`
- Provider OAuth (`/auth/login?provider=github|bitbucket`)
- Cookie-based in-memory session handling in API

### Container And Runtime
- Docker Compose
- Node `20` container for web service in compose
- API exposed on `8000`, web exposed on `3003` (mapped to container port `3000`)

## Environment Configuration

### Web
File: `apps/web/.env`
```env
NEXT_PUBLIC_API_BASE_URL=https://your-subdomain.ngrok-free.app
```

### API
File: `services/orchestrator-api/.env`
```env
# GitHub OAuth
GITHUB_BASE_URL=https://github.com
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
GITHUB_REDIRECT_URI=http://localhost:8000/auth/callback

# Bitbucket OAuth
BITBUCKET_CLIENT_ID=...
BITBUCKET_CLIENT_SECRET=...
BITBUCKET_REDIRECT_URI=https://your-subdomain.ngrok-free.app/auth/bitbucket/callback

# Public API URL when using tunnel for OAuth callbacks
PUBLIC_API_BASE_URL=https://your-subdomain.ngrok-free.app

# Optional PAT fallback (for non-OAuth demo use)
GITHUB_TOKEN=...
ALLOW_PAT_FALLBACK=false

# Frontend redirect after OAuth
FRONTEND_URL=http://localhost:3003

# Cross-site cookie settings for localhost frontend + tunnel backend
SESSION_COOKIE_SAMESITE=none
SESSION_COOKIE_SECURE=true

# Azure OpenAI
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://<resource>.cognitiveservices.azure.com/
AZURE_OPENAI_DEPLOYMENT=<deployment_name>
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Gemini
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-1.5-flash
```

## Run

### Option A: Docker Compose
1. Copy env files:
	- `services/orchestrator-api/.env.example` -> `services/orchestrator-api/.env`
	- `apps/web/.env.example` -> `apps/web/.env`
2. Start:
```bash
docker compose up --build
```
3. Open: http://localhost:3003

## UI Provider Selection
- In the web UI, set **LLM Provider** to `Azure OpenAI` or `Gemini`.
- For `Azure OpenAI`, the backend uses `AZURE_OPENAI_*` values from API env.
- For `Gemini`, the backend uses `GEMINI_API_KEY` and optional `GEMINI_MODEL`.
- You can optionally override model name using the UI **Model (optional)** field.

### Option B: Local Development (recommended when compose web install is flaky)
1. Start API:
```bash
cd services/orchestrator-api
set -a && source .env && set +a
/path/to/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
2. Start web:
```bash
npm --prefix apps/web run dev -- -p 3003
```
3. Open: http://localhost:3003

## OAuth Notes
- GitHub callback URL must exactly match `GITHUB_REDIRECT_URI` (`http://localhost:8000/auth/callback`).
- Bitbucket callback URL must exactly match `BITBUCKET_REDIRECT_URI`.
- Use UI provider selector first, then sign in for that provider.

## Bitbucket Tunnel Setup
Use this when Bitbucket requires HTTPS callback URLs.

1. Start backend on local port `8000`.
2. Expose it using a tunnel URL like `https://your-subdomain.ngrok-free.app`.
3. In Bitbucket OAuth consumer, set callback URL to `https://your-subdomain.ngrok-free.app/auth/bitbucket/callback`.
4. In `services/orchestrator-api/.env`, set:
	- `BITBUCKET_REDIRECT_URI=https://your-subdomain.ngrok-free.app/auth/bitbucket/callback`
	- `PUBLIC_API_BASE_URL=https://your-subdomain.ngrok-free.app`
	- `SESSION_COOKIE_SAMESITE=none`
	- `SESSION_COOKIE_SECURE=true`
5. In `apps/web/.env`, set:
	- `NEXT_PUBLIC_API_BASE_URL=https://your-subdomain.ngrok-free.app`

This ensures OAuth callback, browser API calls, and session cookies all use the same API domain.

## Adding New Nodes

Short answer: node pickup is currently explicit, not fully dynamic.

The API execution path uses `orchestrator/runner.py` with a dependency-aware node chain. This means adding a node requires wiring in a few places.

### 1) Add state fields
- File: `services/orchestrator-api/orchestrator_pkg/langgraph-orchestrator/orchestrator/state.py`
- Add any new state keys your node reads/writes.

### 2) Add node implementation
- File: `services/orchestrator-api/orchestrator_pkg/langgraph-orchestrator/orchestrator/nodes.py`
- Create a new node function (for example, `security_node(...)`).
- Write artifacts conditionally based on `selected_artifacts` (same pattern as existing nodes).

### 3) Register artifacts and chain dependencies
- File: `services/orchestrator-api/orchestrator_pkg/langgraph-orchestrator/orchestrator/runner.py`
- Update:
	- `ALL_ARTIFACTS`
	- `ARTIFACT_NODE`
	- `NODE_DEPS`
	- `NODE_ORDER`
- Add execution call for your new node in `run(...)`.

### 4) Expose selection in UI
- File: `apps/web/app/page.tsx`
- Update:
	- `ArtifactId` type
	- `ARTIFACT_OPTIONS`
	- `ROLE_PRESETS` (if needed)
	- Chain preview maps: `ARTIFACT_NODE`, `NODE_DEPS`, `NODE_ORDER`, `NODE_LABELS`

### 5) API contract
- File: `services/orchestrator-api/app/main.py`
- No schema change is needed if you are only adding new artifact ids to `selected_artifacts`.
- Add request schema changes only if your new node needs extra user input.

### Optional: LangGraph graph path
- File: `services/orchestrator-api/orchestrator_pkg/langgraph-orchestrator/orchestrator/graph.py`
- This is still useful for CLI/graph-based flows, but the API path currently runs through `runner.py`.
- If you want both paths to behave the same, mirror node/dependency updates there too.

## Node Handoff Validation (Implemented)

Validation rules are enforced for all node-pair handoffs in:
`services/orchestrator-api/orchestrator_pkg/langgraph-orchestrator/orchestrator/nodes.py`

Behavior:
- Each major artifact is checked for required markdown sections before it is handed to the next node.
- If sections are missing, the system performs one automatic LLM rewrite pass to repair structure.
- If required sections are still missing after repair, pipeline execution fails fast with a clear validation error.

This improves consistency and traceability between:
- PM -> Architect
- Architect -> Developer
- Developer -> QA
- QA -> Developer loopback

## Important Security Note
Do not commit secrets. Rotate any credentials that were exposed in logs, commits, or chat.

## Author
Developed by nandish: https://github.com/nandishnagaraj/
