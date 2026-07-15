# PayPal REST API operating guidance

Sources:

- https://developer.paypal.com/api/rest/
- https://developer.paypal.com/docs/api/invoicing/v2/
- https://developer.paypal.com/docs/api/orders/v2/
- https://developer.paypal.com/docs/api/transaction-search/v1/
- https://developer.paypal.com/docs/transaction-search/transaction-event-codes/

## Authentication and credentials

Use OAuth 2.0 client credentials to request an access token from
`POST /v1/oauth2/token`. Keep client secrets and access tokens out of prompts,
logs, source control, and user-visible errors. Send the token in the
`Authorization: Bearer` header. Sandbox and live credentials are separate.

## Create and send an invoice

Creating and sending are two separate operations. First call
`POST /v2/invoicing/invoices` with the complete draft invoice body. The body
includes invoice detail, merchant and recipient information, currency, and an
items array. Save the invoice ID returned by PayPal. Then call
`POST /v2/invoicing/invoices/{invoice_id}/send` with the separate send body.
Do not invent an invoice ID or reuse a sample body from documentation.

Both calls mutate PayPal state. Review the exact body before execution, require
explicit confirmation, and use an application-generated `PayPal-Request-Id`
for idempotent POST retries. Reuse the same request ID when retrying the same
operation.

## Orders and payments

`GET /v2/checkout/orders/{order_id}` retrieves one order. The order ID must
come from the caller or a prior PayPal response. Authorization, capture,
refund, void, and update endpoints change payment state and require a separate
confirmed request with exact IDs and bodies.

## Transaction search and sales-volume questions

`GET /v1/reporting/transactions` requires RFC3339 `start_date` and `end_date`
values. A search range cannot exceed 31 days. Page numbers start at 1,
`page_size` can be at most 500, and a query can return at most 10,000 records.
Follow pagination with the same filters and an incremented page number.

Transaction amounts are signed decimal strings and must be calculated with
decimal arithmetic. Never combine different currencies. Status `S` means a
successfully completed transaction; `P` is pending, `D` is denied, and `V` is
fully reversed. T-codes classify money movement. An unfiltered transaction
sum is not accounting revenue. If a sales-event allowlist is unavailable,
label any positive completed T00xx subtotal as a transaction-volume proxy and
show its currency and event-code breakdown. Transaction Search data can lag by
up to three hours.

## Response and error handling

Validate PayPal response shapes, status codes, pagination metadata, and IDs at
the API boundary. Preserve the PayPal Debug ID for troubleshooting without
logging credentials or full sensitive payloads. Do not claim execution when a
request was rejected locally, timed out, or failed before PayPal responded.
