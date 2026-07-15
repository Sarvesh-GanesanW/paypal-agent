# PayPal Agent TUI Guide

This guide starts the terminal UI from the repository, connects it to a PayPal
sandbox account, and configures one model provider. Keep real credentials in
your local `.env`; never commit that file.

## 1. What you need

- Python 3.11 or newer
- `uv`
- A PayPal Developer sandbox application
- One model provider: Codex, AWS Bedrock, OpenAI, or Anthropic

You don't need PostgreSQL for ordinary PayPal reads or the built-in Markdown
documentation fallback. PostgreSQL is only needed for the optional pgvector
RAG setup.

## 2. Install the project

Run these commands from the repository root:

```bash
cd datazoic-paypal-agent
uv sync --extra dev
cp .env.example .env
```

The app reads `.env` from the current working directory, so start the TUI from
the repository root. `.env` is ignored by Git.

## 3. Add PayPal sandbox credentials

Create or select an app under **Apps & Credentials** in the PayPal Developer
Dashboard. Use the sandbox client ID and secret in `.env`:

```dotenv
PAYPAL_ENVIRONMENT=sandbox
PAYPAL_CLIENT_ID=<your-sandbox-client-id>
PAYPAL_CLIENT_SECRET=<your-sandbox-client-secret>
PAYPAL_ACCESS_TOKEN=
PAYPAL_ALLOW_MUTATIONS=false
```

Leave `PAYPAL_ACCESS_TOKEN` empty when using a client ID and secret. The agent
will request and refresh OAuth access tokens for you.

Keep `PAYPAL_ALLOW_MUTATIONS=false` while testing. Chat can prepare a mutation,
but it won't execute account-changing requests. Mutations require a separate
confirmed direct call and `PAYPAL_ALLOW_MUTATIONS=true`.

The managed-account variables are only needed for PayPal's limited-release
Managed Accounts APIs:

```dotenv
PAYPAL_MANAGED_CLIENT_ID=
PAYPAL_MANAGED_CLIENT_SECRET=
PAYPAL_MANAGED_ACCESS_TOKEN=
```

## 4. Choose one model provider

### Option A: Codex

Use Codex when the Codex CLI is installed and logged in locally:

```dotenv
MODEL_PROVIDER=codex
CODEX_COMMAND=codex
CODEX_MODEL_ID=
CODEX_TIMEOUT_SECONDS=180
CODEX_SANDBOX=read-only
ROUTER_TIMEOUT_SECONDS=190
```

Log in once:

```bash
uv run paypal-agent --login-codex
```

For device-code login:

```bash
uv run paypal-agent --login-codex --device-auth
```

Codex reuses that local login. You don't need `OPENAI_API_KEY` for this option.

### Option B: AWS Bedrock with Claude Opus 4.6

Use the normal AWS credential chain: an AWS profile, `aws configure`, an IAM
role, or shell environment variables. Don't paste AWS secret keys into this
guide or commit them to the repository.

```dotenv
MODEL_PROVIDER=bedrock
AWS_REGION=us-east-1
BEDROCK_ROUTER_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0
BEDROCK_MAIN_MODEL_ID=us.anthropic.claude-opus-4-6-v1
BEDROCK_SUBAGENT_MODEL_ID=us.anthropic.claude-opus-4-6-v1
```

The example keeps the smaller Haiku model for tool selection and uses Opus 4.6
for the main and sub-agent answers. To test Opus 4.6 for tool selection too,
set:

```dotenv
BEDROCK_ROUTER_MODEL_ID=us.anthropic.claude-opus-4-6-v1
```

If you use a named profile, export it before starting the TUI:

```bash
export AWS_PROFILE=<your-profile>
```

The AWS identity needs permission to invoke the configured Bedrock models in
the selected region.

### Option C: OpenAI API

```dotenv
MODEL_PROVIDER=openai
OPENAI_API_KEY=<your-openai-api-key>
```

### Option D: Anthropic API

```dotenv
MODEL_PROVIDER=anthropic
ANTHROPIC_API_KEY=<your-anthropic-api-key>
```

Only configure the provider you plan to use.

## 5. Start the TUI

Run the current repository source:

```bash
uv run paypal-agent --provider codex --no-color
```

Replace `codex` with `bedrock`, `openai`, or `anthropic` when needed. Then type
normal questions at the `user>` prompt:

```text
user> What all tools do you have?
user> Can you check account balances?
user> List my products
user> Show order details for order ID 5O190127TN364715T
```

The default output streams each graph stage before printing the answer. Add
`--no-stream` if you only want the final response.

Useful commands inside the TUI:

```text
/help
/provider
/provider codex
/provider bedrock
/tools balance
/tools invoice
/rag how do I create an invoice?
/quit
```

The `/tools`, `/rag`, `/grep`, and `/find` query shortcuts use the same
LangGraph router, sub-agent, and main answer model as normal text.

## 6. Run one query and exit

Use `--once` for scripts and quick checks:

```bash
uv run paypal-agent --provider codex --once \
  "Can you check account balances?" --no-color
```

Natural-language queries require one configured model provider. Each routing
turn sends that provider the user query and sanitized metadata for all 116
PayPal tools; there is no keyword-only mode or selection fallback. After the
selected LangGraph branch runs, the configured sub-agent and main model compose
the final answer from the prepared answer and route payload. There is no
deterministic final-answer fallback.

The answer models receive relevant PayPal response or mutation-plan data. That
data can contain account details, balances, customer information, or other PII.
Use only providers approved by your data-handling policy. Authentication
headers and literal Postman header/query samples are removed before answer-model
calls.

## 7. Verify the setup

Start with a request that doesn't call PayPal:

```bash
uv run paypal-agent --provider codex --once \
  "What all tools do you have?" --no-color
```

Then try a read-only PayPal request:

```bash
uv run paypal-agent --provider codex --once \
  "Can you check account balances?" --no-color
```

A working PayPal call prints the selected tool and HTTP status. It also prints
a PayPal Debug ID when PayPal provides one. Treat returned balances, account
IDs, customer details, and transaction data as sensitive.

## 8. Troubleshooting

### A fix isn't showing up

Exit every running TUI and restart with `uv run paypal-agent` from the
repository root. A previously started process keeps the old Python code in
memory.

If you installed the command globally, reinstall it after pulling changes:

```bash
uv tool install --force .
```

### PayPal returns 401

Check that the client ID and secret belong to the selected environment. Sandbox
credentials won't authenticate against `PAYPAL_ENVIRONMENT=live`, and live
credentials won't authenticate against the sandbox endpoint.

### PayPal returns 403

The credentials are valid but the app or account may not have access to that
API. Managed Accounts and other limited-release APIs require PayPal approval.

### PayPal returns 404

Check the resource ID and make sure it belongs to the same sandbox account as
the credentials in `.env`.

### Codex routing times out

`ROUTER_TIMEOUT_SECONDS` must be greater than `CODEX_TIMEOUT_SECONDS`. The
values in the Codex example allow the subprocess up to 180 seconds and the
router up to 190 seconds.

### Codex asks you to log in

Run `uv run paypal-agent --login-codex`, then restart the TUI. You can also use
`--provider bedrock` if AWS Bedrock is already configured.

### Bedrock returns an authorization or model-access error

Confirm the AWS region, active profile, IAM permissions, and access to every
configured model ID.

## 9. Safety checks

- Never commit `.env`.
- Never paste access tokens, client secrets, or AWS keys into chat prompts.
- Keep sandbox mode and mutations disabled until read-only queries work.
- Review every mutation payload before enabling and confirming a direct call.
- Restart the TUI after pulling or changing code.
