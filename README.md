# Datazoic PayPal Agent

PayPal tool router and execution service built from the public PayPal Postman
collection linked in the task PDF.

## What This Contains

- 116 PayPal requests loaded into the catalog from the Postman collection.
- Lexical shortlist routing before model routing.
- Configurable model provider: Bedrock, OpenAI API, Anthropic API, or local
  Codex CLI auth.
- Small router model at temperature `0` with strict Pydantic output.
- LangGraph `StateGraph` orchestration for shortlist, routing, RAG/system
  search branches, PayPal planning, answer generation, and request logging.
- Main orchestrator and sub-agent model for grounded final answers.
- pgvector hybrid RAG with Bedrock Cohere Embed v4 and Cohere rerank.
- HNSW and IVFFLAT vector indexes plus a GIN index on `tsvector`.
- System-search support tool over capabilities and recent request logs.
- Local JSONL memory with `memory_grep` and `memory_find` support tools.
- Natural-language execution of one exact, validated, read-only PayPal request.
- Real PayPal execution through sandbox or explicitly selected live credentials.
- Expiring OAuth token caches for standard and managed-account credentials.
- Mutation guard requiring both request confirmation and environment approval.
- Optional LangSmith tracing for chat, routing, RAG, model, and tool spans.

A catalog entry describes a collection request; it is executable only when its
required inputs, credentials, and request body are available. Limited-release
PayPal APIs still require the corresponding PayPal account approval.

## Setup

```bash
uv sync --extra dev
cp .env.example .env
```

Set credentials in `.env`:

```text
PAYPAL_ENVIRONMENT=sandbox
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
PAYPAL_ACCESS_TOKEN=
PAYPAL_MANAGED_CLIENT_ID=
PAYPAL_MANAGED_CLIENT_SECRET=
PAYPAL_MANAGED_ACCESS_TOKEN=
PAYPAL_UPLOAD_ROOT=
PAYPAL_ALLOW_MUTATIONS=false
MODEL_PROVIDER=bedrock
MODEL_ROUTER_ENABLED=
AWS_REGION=us-east-1
BEDROCK_ROUTER_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0
BEDROCK_MAIN_MODEL_ID=us.anthropic.claude-opus-4-6-v1
BEDROCK_SUBAGENT_MODEL_ID=us.anthropic.claude-opus-4-6-v1
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
CODEX_COMMAND=codex
CODEX_MODEL_ID=
MEMORY_DIR=~/.local/share/paypal-agent/memory
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=paypal-agent
LANGSMITH_ENDPOINT=https://aws.api.smith.langchain.com
LANGSMITH_WORKSPACE_ID=
```

`PAYPAL_ACCESS_TOKEN` can be used instead of standard client credentials. Static
tokens are never refreshed automatically because they have no reliable expiry
metadata. For refreshable authentication, omit `PAYPAL_ACCESS_TOKEN` and use
client credentials; the client caches OAuth tokens until shortly before
PayPal's `expires_in` time and can refresh once after an authentication failure.

Managed Accounts requests use `PAYPAL_MANAGED_CLIENT_ID` and
`PAYPAL_MANAGED_CLIENT_SECRET`, or `PAYPAL_MANAGED_ACCESS_TOKEN`; they do not
fall back to the standard PayPal credentials. These APIs are limited release
and require an approved PayPal account. `PAYPAL_MANAGED_ACCESS_TOKEN` is likewise
never refreshed automatically.

Set `LANGSMITH_TRACING=true` only when a local `.env` contains a valid
LangSmith key. The app never returns or logs the key.

## Model Providers

Set `MODEL_PROVIDER` to one of:

- `bedrock`: AWS Bedrock router, sub-agent, and orchestrator. This is the
  default used for the Datazoic task.
- `openai`: direct OpenAI API calls with `OPENAI_API_KEY`.
- `anthropic`: direct Anthropic API calls with `ANTHROPIC_API_KEY`.
- `codex`: shells out to local `codex exec`, so the Codex CLI can reuse the
  user's ChatGPT/Codex login or API-key login.

The Codex subprocess runs ephemerally from an isolated temporary directory with
a scrubbed environment and read-only permissions. It is intended for a trusted
local operator; prefer the direct Bedrock, OpenAI, or Anthropic provider for an
untrusted multi-user service.

Install the terminal UI globally:

```bash
uv tool install --force .
paypal-agent
```

Persist the provider outside the repo:

```bash
paypal-agent --provider codex --save-provider --once "what tools are available?"
paypal-agent --login-codex
paypal-agent --login-codex --device-auth
```

Inside the TUI:

```text
/provider codex
/login codex
/login codex device
```

## Run The API

```bash
docker compose up -d postgres
uv run python scripts/download_paypal_docs.py
uv run python scripts/ingest_paypal_docs.py
uv run uvicorn paypal_agent.api:app --reload
```

The API does not include application-level authentication. The command above
uses Uvicorn's loopback default and is intended for local use. Do not bind it to
a public or shared interface unless an authenticated, authorized reverse proxy
protects every endpoint, especially `/tools/*/call` and `/memory/*`.

Useful endpoints:

```bash
curl http://localhost:8000/tools
curl "http://localhost:8000/tools/search?query=send%20invoice&limit=5"
curl http://localhost:8000/observability
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"userInput":"show order ORDER-123"}'
```

`/chat` calls PayPal only when routing produces one unambiguous read-only tool
and all IDs, dates, and filters are grounded in the user's request. Missing
inputs, ambiguity, low confidence, or a model-provider failure returns a
clarification and makes no PayPal request. A mutating chat request also makes
no PayPal request; it returns an unconfirmed direct-call payload for the user
to review. The separate direct caller must add confirmation.

The first `/chat` response includes a random UUIDv4 `conversationId`. Treat it
as a bearer session token and send it on follow-up turns. The API no longer
shares a default conversation across callers; supplied conversation IDs must
be UUIDv4 values.

Flush buffered LangSmith traces after a demo run:

```bash
curl -X POST http://localhost:8000/observability/flush
```

## Terminal Chat UI

Use the terminal UI for natural conversations against the same LangGraph
orchestrator:

```bash
uv run paypal-agent
```

One-shot prompt:

```bash
uv run paypal-agent --once \
  "I need to send a $50 invoice to buyer@example.com. What do you need from me?"
```

The CLI streams LangGraph node progress by default, then streams the final
answer text. Use `--no-stream` to print only the final response. For an
executed read, the answer includes the bounded PayPal response along with the
upstream status and PayPal Debug ID, including non-2xx error details.

Helpful terminal commands:

```text
/provider
/provider codex
/login codex
/tools invoice
/rag how do I create an invoice?
/grep invoice
/find previous invoice
/quit
```

Local memory is append-only JSONL under `MEMORY_DIR`. PayPal tool events store
only tool, status, status code, and PayPal Debug ID metadata; PayPal request and
response bodies, chat prompts, and raw conversation IDs are not written to
durable JSONL memory. `memory_grep` and `memory_find` return only an explicit
metadata allowlist, including when they read files created by an older version.
The in-process recent-request log is also metadata-only. Delete pre-upgrade
JSONL files under `MEMORY_DIR` if the sensitive values must also be removed from
disk. Raw PayPal results are returned to the requesting user, but operational
PayPal responses and mutation plans are rendered deterministically rather than
sent to an answer model. Optional LangSmith tracing should still be enabled only
under the operator's data handling policy.

## Terminal Demo

The demo artifact is a terminal recording, not a browser dashboard. It runs the
installed `paypal-agent` CLI against natural language prompts for invoice
planning, PayPal docs RAG, transaction search, order lookup, refund guardrails,
webhook signature verification, and JSONL memory find/grep.

```bash
npm run record:demo
```

Outputs:

- `artifacts/demo/datazoic_paypal_agent_demo.webm`
- `artifacts/demo/terminal_demo_transcript.txt`

Direct execution sends a real PayPal request:

```bash
curl -X POST http://localhost:8000/tools/paypal_orders_show_order_details/call \
  -H "Content-Type: application/json" \
  -d '{"pathParams":{"order_id":"ORDER_ID"}}'
```

Each result keeps the full upstream payload under `response`, the upstream
HTTP code under `status_code`, and the response-header value under
`paypal_debug_id`. List and search calls return one PayPal page per tool call;
the service does not automatically follow `next` links. Supply `page` and
`page_size` query values for another bounded page, and use the returned PayPal
links as pagination metadata.

Transaction Search requires `start_date` and `end_date`, accepts either
`YYYY-MM-DD` or RFC3339 timestamps, and rejects ranges longer than 31 days. It
defaults to `page=1` and `page_size=100` and clamps `page_size` to PayPal's 500
item maximum. Ordinary list requests still send one page. Sales-volume prompts
retrieve every reported page up to PayPal's 10,000-record search limit, then
return a currency-separated completed-positive-payment proxy with its T-code
definition and exclusions rather than presenting it as accounting revenue.

The direct tool endpoint supports collection-declared raw JSON, URL-encoded,
and multipart request bodies. Multipart calls are rejected unless
`PAYPAL_UPLOAD_ROOT` is configured. Every caller-supplied file path must resolve
beneath that directory; the service opens it only for the duration of the
request. All body modes require exact caller-supplied values rather than
Postman sample files or bodies.

The collection's Appeal dispute entry declares a raw `multipart/related` body
that cannot be encoded safely from its metadata. It is marked unsupported in
the catalog and rejected before any HTTP request. Use a corrected
`multipart/form-data` definition before enabling that operation.

Mutating calls require:

- `PAYPAL_ALLOW_MUTATIONS=true`
- request JSON with `"confirm": true`
- exact body/path/query values supplied by the caller

Natural-language chat never satisfies this confirmation gate. It only returns
an unconfirmed direct-call payload for explicit review. A separate direct
caller must add `"confirm": true` after that review. For POST mutations, the
reviewed plan includes a stable `PayPal-Request-Id`; reuse the same value for
every retry so an ambiguous timeout cannot create a duplicate operation.

## Production Collection Run

```bash
uv run python scripts/run_paypal_collection.py --tool paypal_orders_show_order_details \
  --fixtures fixtures.local.json
```

Mutation run:

```bash
uv run python scripts/run_paypal_collection.py \
  --include-mutations \
  --confirm-mutations \
  --fixtures fixtures.local.json
```

The runner has no dry-run mode. Calls that lack required fixtures are skipped
instead of sending sample Postman payloads.

## Verification

```bash
uv run pytest -q
uv run ruff check .
uv run pyright src scripts tests
uv run python scripts/evaluate_rag.py
```

`scripts/evaluate_rag.py` runs RAGAS ID-based context precision and recall
against the local PayPal pgvector index and writes JSON results under `logs/`.

## Source

PayPal Postman collection:
https://www.postman.com/collections/19024122-92a85d0e-51e7-47da-9f83-c45dcb1cdf24
