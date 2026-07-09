# Datazoic PayPal Agent

Production-oriented PayPal tool router built from the public PayPal Postman
collection linked in the task PDF.

## What This Contains

- 116 PayPal requests loaded from the Postman collection.
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
- Real PayPal execution through environment credentials.
- Mutation guard requiring both request confirmation and environment approval.
- Optional LangSmith tracing for chat, routing, RAG, model, and tool spans.

## Setup

```bash
uv sync --extra dev
cp .env.example .env
```

Set credentials in `.env`:

```text
PAYPAL_ENVIRONMENT=live
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
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

`PAYPAL_ACCESS_TOKEN` can be used instead of client credentials.
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

Useful endpoints:

```bash
curl http://localhost:8000/tools
curl "http://localhost:8000/tools/search?query=send%20invoice&limit=5"
curl http://localhost:8000/observability
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"userInput":"send an invoice for 50 dollars","conversationId":"demo"}'
```

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
answer text. Use `--no-stream` to print only the final response.
When chat routes to a PayPal tool, the agent sends one selected PayPal request
and displays the returned status code, even when PayPal returns `401`, `404`,
or another non-2xx response.

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

Local memory is append-only JSONL under `MEMORY_DIR`. Chat and PayPal tool
events are sanitized before writing so tokens and secret-looking fields are
redacted. The agent can route natural-language memory prompts to `memory_grep`
or `memory_find`, and the CLI exposes direct `/grep` and `/find` commands.

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

Mutating calls require:

- `PAYPAL_ALLOW_MUTATIONS=true`
- request JSON with `"confirm": true`
- exact body/path/query values supplied by the caller

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
