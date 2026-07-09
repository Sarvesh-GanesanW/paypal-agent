# Payments

Source: https://developer.paypal.com/docs/api/payments/v2/

Payments
REST APIs
Get Started with PayPal REST APIs
Authentication
Postman Guide
Codespaces
API requests
API responses
Core Resources
Overview
API Integration
Release Notes
Orders
Orders sdkV2
Payments
Payments
get
Show details for authorized payment
post
Capture authorized payment
post
Reauthorize authorized payment
post
Void authorized payment
get
Show captured payment details
post
Refund captured payment
post
Find a list of eligible payment methods.
get
Show refund details
Errors
Definitions
Payments sdkV2
Payment Method Tokens
Payment Method Tokens sdkV3
Add Tracking
Catalog Products
Currency Exchange
Disputes
Identity
Invoicing
Partner Referrals
Payment Experience
Payouts
Referenced Payouts
Subscriptions
Transaction Search
Webhooks Management
Webhooks
Overview
Webhook event names
Webhooks Events dashboard
Webhooks simulator
Integration
Go Live
Production Environment
PayPal Application Guidelines
PayPal Security Guidelines
Rate Limiting Guidelines
Idempotency
Troubleshooting
Agreement already cancelled
Cannot pay self
Currency mismatch
Duplicate transaction
Merchant not enabled for reference transaction
Validation error
Not authorized
Resource not found
Unprocessable entity
Validation error
Reference
Currency Codes
Country Codes
State & Province Codes
Locale codes
Deprecated Resources
Deprecated resources
Billing Agreements
Billing Plans
Invoicing v1
Partner Referrals v1
Payments v1
Payments
(
2
)
API Version v2
Call the Payments API to authorize payments, capture authorized payments, refund payments that have already been captured, and show payment information. Use the Payments API in conjunction with the
Orders API
. For more information, see the
PayPal Checkout Overview
.
Show details for authorized payment
get
/v2/payments/authorizations/{authorization_id}
Try it
Shows details for an authorized payment, by ID.
Security
Oauth2
Request
path
Parameters
authorization_id
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The ID of the authorized payment for which to show details.
header
Parameters
Authorization
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
Holds authorization information for external API calls.
Examples
:
Bearer authorization.
An authorization header with information for the Bearer authorization scheme. The authorization parameter value is randomized for this example.
Bearer A21AAGHr9qtiRRXH4oYcQokQgV99rGqEIfgrr8xHCclP0OzmD9KVgg5ppIIg1jzJgQkV4wd02svIvBJyg6cLFJjFow_SjBhxQ
PayPal-Auth-Assertion
string
[ 1 .. 10000 ] characters
^.*$
Header for an API client-provided JWT assertion that identifies the merchant. Establishing the consent to act-on-behalf of a merchant is a prerequisite for using this header.
Examples
:
An auth assertion.
A paypal-auth-assertion header with a randomized value.
eyJhbGciOiJub25lIn0.eyJlbWFpbCI6Im15QGVtYWlsLmNvbSJ9
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows authorization details.
401
Unauthorized.
403
Forbidden.
404
Not Found.
500
Internal Server Error.
default
Default response.
Response samples
200
401
403
404
500
default
1 more
default
1 more
application/json
Show Authorized Payment Details
Show Authorized Payment Details with Metadata
Show Authorized Payment Details
Show Authorized Payment Details
Shows details for an authorized payment, by ID.
Copy
Expand all
Collapse all
{
"id"
:
"0VF52814937998046"
,
"status"
:
"CREATED"
,
"amount"
:
{
"value"
:
"10.99"
,
"currency_code"
:
"USD"
}
,
"invoice_id"
:
"INVOICE-123"
,
"seller_protection"
:
{
"status"
:
"ELIGIBLE"
,
"dispute_categories"
:
[
"ITEM_NOT_RECEIVED"
,
"UNAUTHORIZED_TRANSACTION"
]
}
,
"payee"
:
{
"email_address"
:
"
[email protected]
"
,
"merchant_id"
:
"7KNGBPH2U58GQ"
}
,
"expiration_time"
:
"2017-10-10T23:23:45Z"
,
"create_time"
:
"2017-09-11T23:23:45Z"
,
"update_time"
:
"2017-09-11T23:23:45Z"
,
"links"
:
[
{
"rel"
:
"self"
,
"method"
:
"GET"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/authorizations/0VF52814937998046
"
}
,
{
"rel"
:
"capture"
,
"method"
:
"POST"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/authorizations/0VF52814937998046/capture
"
}
,
{
"rel"
:
"void"
,
"method"
:
"POST"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/authorizations/0VF52814937998046/void
"
}
,
{
"rel"
:
"reauthorize"
,
"method"
:
"POST"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/authorizations/0VF52814937998046/reauthorize
"
}
]
}
Capture authorized payment
post
/v2/payments/authorizations/{authorization_id}/capture
Try it
Captures an authorized payment, by ID.
Security
Oauth2
Request
path
Parameters
authorization_id
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the authorized payment to capture.
header
Parameters
PayPal-Request-Id
string
[ 1 .. 10000 ] characters
^.*$
A unique ID identifying the request header for idempotency purposes.
Examples
:
A request id.
A paypal-request-id header with a randomized value.
17e81d06-77ab-11e8-adc0-fa71639ebebc
Prefer
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
Default:
return=minimal
The preferred server response upon successful completion of the request. Value is:
return=minimal
. The server returns a minimal response to optimize communication between the API caller and the server. A minimal response includes the
id
,
status
and HATEOAS links.
return=representation
. The server returns a complete resource representation, including the current state of the resource.
Authorization
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
Holds authorization information for external API calls.
Examples
:
Bearer authorization.
An authorization header with information for the Bearer authorization scheme. The authorization parameter value is randomized for this example.
Bearer A21AAGHr9qtiRRXH4oYcQokQgV99rGqEIfgrr8xHCclP0OzmD9KVgg5ppIIg1jzJgQkV4wd02svIvBJyg6cLFJjFow_SjBhxQ
PayPal-Auth-Assertion
string
[ 1 .. 10000 ] characters
^.*$
Header for an API client-provided JWT assertion that identifies the merchant. Establishing the consent to act-on-behalf of a merchant is a prerequisite for using this header.
Examples
:
An auth assertion.
A paypal-auth-assertion header with a randomized value.
eyJhbGciOiJub25lIn0.eyJlbWFpbCI6Im15QGVtYWlsLmNvbSJ9
Request Body schema:
application/json
optional
invoice_id
string
[ 0 .. 127 ] characters
^[\S\s]*$
The API caller-provided external invoice number for this order. Appears in both the payer's transaction history and the emails that the payer receives.
note_to_payer
string
[ 0 .. 255 ] characters
^[\S\s]*$
An informational note about this settlement. Appears in both the payer's transaction history and the emails that the payer receives.
amount
object
(
amount_with_breakdown
)
The total order amount with an optional breakdown that provides details, such as the total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
If you specify
amount.breakdown
, the amount equals
item_total
plus
tax_total
plus
shipping
plus
handling
plus
insurance
minus
shipping_discount
minus discount.
The amount must be a positive number. For listed of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
final_capture
boolean
Default:
false
Indicates whether you can make additional captures against the authorized payment. Set to
true
if you do not intend to capture additional payments against the authorization. Set to
false
if you intend to capture additional payments against the authorization.
payment_instruction
object
(
payment_instruction
)
Any additional payment instructions to be consider during payment processing. This processing instruction is applicable for Capturing an order or Authorizing an Order.
soft_descriptor
string
[ 0 .. 22 ] characters
^[\S\s]*$
The payment descriptor on the payer's account statement.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows captured payment details.
201
A successful request returns the HTTP
201 Created
status code and a JSON response body that shows captured payment details.
400
The request failed because it is not well-formed or is syntactically incorrect or violates schema.
401
Unauthorized.
403
Forbidden.
404
Not Found.
409
The server has detected a conflict while processing this request.
422
The request failed because it is semantically incorrect or failed business validation.
500
Internal Server Error.
default
Default response.
Request samples
Payload
application/json
Capture Authorized Payment
Capture Authorized Payment - 200 idempotent response
Capture Authorized Payment with an empty request
Capture Authorized Payment with Prefer Request Header
Capture Authorized Payment
Captures an authorized payment, by ID.
Copy
Expand all
Collapse all
{
"amount"
:
{
"value"
:
"10.99"
,
"currency_code"
:
"USD"
}
,
"invoice_id"
:
"INVOICE-123"
,
"final_capture"
:
true
,
"note_to_payer"
:
"If the ordered color is not available, we will substitute with a different color free of charge."
,
"soft_descriptor"
:
"Bob's Custom Sweaters"
}
Response samples
200
201
400
401
403
404
409
422
500
default
5 more
404
409
422
500
default
5 more
application/json
Capture Authorized Payment - 200 idempotent response
Capture Authorized Payment - 200 idempotent response
Captures an authorized payment, by ID.
Copy
Expand all
Collapse all
{
"id"
:
"23T524207X938445J"
,
"amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"100.00"
}
,
"final_capture"
:
false
,
"seller_protection"
:
{
"status"
:
"ELIGIBLE"
,
"dispute_categories"
:
[
"ITEM_NOT_RECEIVED"
,
"UNAUTHORIZED_TRANSACTION"
]
}
,
"seller_receivable_breakdown"
:
{
"gross_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"1.00"
}
,
"paypal_fee"
:
{
"currency_code"
:
"USD"
,
"value"
:
"0.52"
}
,
"net_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"0.48"
}
,
"exchange_rate"
:
{ }
}
,
"invoice_id"
:
"OrderInvoice-10_10_2024_12_58_20_pm"
,
"status"
:
"COMPLETED"
,
"create_time"
:
"2024-10-14T21:29:26Z"
,
"update_time"
:
"2024-10-14T21:29:26Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/payments/captures/23T524207X938445J
"
,
"rel"
:
"self"
,
"method"
:
"GET"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/payments/captures/23T524207X938445J/refund
"
,
"rel"
:
"refund"
,
"method"
:
"POST"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/payments/authorizations/6DR965477U7140544
"
,
"rel"
:
"up"
,
"method"
:
"GET"
}
]
}
Reauthorize authorized payment
post
/v2/payments/authorizations/{authorization_id}/reauthorize
Try it
Reauthorizes an authorized PayPal account payment, by ID. To ensure that funds are still available, reauthorize a payment after its initial three-day honor period expires. Within the 29-day authorization period, you can issue multiple re-authorizations after the honor period expires.
If 30 days have transpired since the date of the original authorization, you must create an authorized payment instead of reauthorizing the original authorized payment.
A reauthorized payment itself has a new honor period of three days.
You can reauthorize an authorized payment from 4 to 29 days after the 3-day honor period. The allowed amount depends on context and geography, for example in US it is up to 115% of the original authorized amount, not to exceed an increase of $75 USD.
Supports only the
amount
request parameter.
Security
Oauth2
Request
path
Parameters
authorization_id
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the authorized payment to reauthorize.
header
Parameters
PayPal-Request-Id
string
[ 1 .. 10000 ] characters
^.*$
A unique ID identifying the request header for idempotency purposes.
Examples
:
A request id.
A paypal-request-id header with a randomized value.
17e81d06-77ab-11e8-adc0-fa71639ebebc
Prefer
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
Default:
return=minimal
The preferred server response upon successful completion of the request. Value is:
return=minimal
. The server returns a minimal response to optimize communication between the API caller and the server. A minimal response includes the
id
,
status
and HATEOAS links.
return=representation
. The server returns a complete resource representation, including the current state of the resource.
Authorization
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
Holds authorization information for external API calls.
Examples
:
Bearer authorization.
An authorization header with information for the Bearer authorization scheme. The authorization parameter value is randomized for this example.
Bearer A21AAGHr9qtiRRXH4oYcQokQgV99rGqEIfgrr8xHCclP0OzmD9KVgg5ppIIg1jzJgQkV4wd02svIvBJyg6cLFJjFow_SjBhxQ
PayPal-Auth-Assertion
string
[ 1 .. 10000 ] characters
^.*$
Header for an API client-provided JWT assertion that identifies the merchant. Establishing the consent to act-on-behalf of a merchant is a prerequisite for using this header.
Examples
:
An auth assertion.
A paypal-auth-assertion header with a randomized value.
eyJhbGciOiJub25lIn0.eyJlbWFpbCI6Im15QGVtYWlsLmNvbSJ9
Request Body schema:
application/json
optional
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows the reauthorized payment details.
201
A successful request returns the HTTP
201 Created
status code and a JSON response body that shows the reauthorized payment details.
400
The request failed because it is not well-formed or is syntactically incorrect or violates schema.
401
Unauthorized.
403
Forbidden.
404
Not Found.
422
The request failed because it either is semantically incorrect or failed business validation.
500
Internal Server Error.
default
Default response.
Request samples
Payload
application/json
Reauthorize Authorized Payment
Reauthorize Authorized Payment - 200 idempotent response
Reauthorize Authorized Payment with an empty request
Reauthorize Authorized Payment with Prefer Request Header
Reauthorize Authorized Payment
Reauthorizes an authorized payment, by ID. The honor period for the authorized payment has expired.
Copy
Expand all
Collapse all
{
"amount"
:
{
"value"
:
"10.99"
,
"currency_code"
:
"USD"
}
}
Response samples
200
201
400
401
403
404
422
500
default
4 more
404
422
500
default
4 more
application/json
Reauthorize Authorized Payment - 200 idempotent response
Reauthorize Authorized Payment - 200 idempotent response
Reauthorizes an authorized payment, by ID. The honor period for the authorized payment has expired.
Copy
Expand all
Collapse all
{
"id"
:
"8AA831015G517922L"
,
"status"
:
"CREATED"
,
"links"
:
[
{
"rel"
:
"self"
,
"method"
:
"GET"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/authorizations/8AA831015G517922L
"
}
,
{
"rel"
:
"capture"
,
"method"
:
"POST"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/authorizations/8AA831015G517922L/capture
"
}
,
{
"rel"
:
"void"
,
"method"
:
"POST"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/authorizations/8AA831015G517922L/void
"
}
,
{
"rel"
:
"reauthorize"
,
"method"
:
"POST"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/authorizations/8AA831015G517922L/reauthorize
"
}
]
}
Void authorized payment
post
/v2/payments/authorizations/{authorization_id}/void
Try it
Voids, or cancels, an authorized payment, by ID. You cannot void an authorized payment that has been fully captured.
Security
Oauth2
Request
path
Parameters
authorization_id
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the authorized payment to void.
header
Parameters
Authorization
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
Holds authorization information for external API calls.
Examples
:
Bearer authorization.
An authorization header with information for the Bearer authorization scheme. The authorization parameter value is randomized for this example.
Bearer A21AAGHr9qtiRRXH4oYcQokQgV99rGqEIfgrr8xHCclP0OzmD9KVgg5ppIIg1jzJgQkV4wd02svIvBJyg6cLFJjFow_SjBhxQ
PayPal-Auth-Assertion
string
[ 1 .. 10000 ] characters
^.*$
Header for an API client-provided JWT assertion that identifies the merchant. Establishing the consent to act-on-behalf of a merchant is a prerequisite for using this header.
Examples
:
An auth assertion.
A paypal-auth-assertion header with a randomized value.
eyJhbGciOiJub25lIn0.eyJlbWFpbCI6Im15QGVtYWlsLmNvbSJ9
PayPal-Request-Id
string
[ 1 .. 10000 ] characters
^.*$
A unique ID identifying the request header for idempotency purposes.
Examples
:
A request id.
A paypal-request-id header with a randomized value.
17e81d06-77ab-11e8-adc0-fa71639ebebc
Prefer
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
Default:
return=minimal
The preferred server response upon successful completion of the request. Value is:
return=minimal
. The server returns a minimal response to optimize communication between the API caller and the server. A minimal response includes the
id
,
status
and HATEOAS links.
return=representation
. The server returns a complete resource representation, including the current state of the resource.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows authorization details. This response is returned when the Prefer header is set to return=representation.
204
No Content.
401
Unauthorized.
403
Forbidden.
404
Not Found.
409
The request failed because a previous call for the given resource is in progress.
422
The request failed because it either is semantically incorrect or failed business validation.
500
Internal Server Error.
default
Default response.
Response samples
200
401
403
404
409
422
500
default
3 more
422
500
default
3 more
application/json
Void Authorized Payment
Void Authorized Payment
Voids an authorized PayPal account payment, by ID. You cannot void an authorized payment that has been fully captured.
Copy
Expand all
Collapse all
{
"id"
:
"5C908745JK343851U"
,
"status"
:
"VOIDED"
,
"amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"100.00"
}
,
"invoice_id"
:
"OrderInvoice-10_10_2024_12_06_00_pm"
,
"seller_protection"
:
{
"status"
:
"ELIGIBLE"
,
"dispute_categories"
:
[
"ITEM_NOT_RECEIVED"
,
"UNAUTHORIZED_TRANSACTION"
]
}
,
"expiration_time"
:
"2024-11-08T09:06:03-08:00"
,
"create_time"
:
"2024-10-10T10:06:03-07:00"
,
"update_time"
:
"2024-10-10T10:06:19-07:00"
,
"links"
:
[
{
"href"
:
"
https://api.paypal.com/v2/payments/authorizations/5C908745JK343851U
"
,
"rel"
:
"self"
,
"method"
:
"GET"
}
]
}
Show captured payment details
get
/v2/payments/captures/{capture_id}
Try it
Shows details for a captured payment, by ID.
Security
Oauth2
Request
path
Parameters
capture_id
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the captured payment for which to show details.
header
Parameters
Authorization
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
Holds authorization information for external API calls.
Examples
:
Bearer authorization.
An authorization header with information for the Bearer authorization scheme. The authorization parameter value is randomized for this example.
Bearer A21AAGHr9qtiRRXH4oYcQokQgV99rGqEIfgrr8xHCclP0OzmD9KVgg5ppIIg1jzJgQkV4wd02svIvBJyg6cLFJjFow_SjBhxQ
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows captured payment details.
401
Unauthorized.
403
Forbidden.
404
Not Found.
500
Internal Server Error.
default
Default response.
Response samples
200
401
403
404
500
default
1 more
default
1 more
application/json
Show Captured Payment Details
Show Captured Payment Details
Shows details for a captured payment, by ID.
Copy
Expand all
Collapse all
{
"id"
:
"74L756601X447022Y"
,
"amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"100.00"
}
,
"final_capture"
:
true
,
"seller_protection"
:
{
"status"
:
"ELIGIBLE"
,
"dispute_categories"
:
[
"ITEM_NOT_RECEIVED"
,
"UNAUTHORIZED_TRANSACTION"
]
}
,
"seller_receivable_breakdown"
:
{
"gross_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"100.00"
}
,
"paypal_fee"
:
{
"currency_code"
:
"USD"
,
"value"
:
"3.98"
}
,
"net_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"96.02"
}
}
,
"invoice_id"
:
"OrderInvoice-23_10_2024_12_27_32_pm"
,
"status"
:
"COMPLETED"
,
"supplementary_data"
:
{
"related_ids"
:
{
"order_id"
:
"25M43554V9523650M"
,
"authorization_id"
:
"0T620041CK889853A"
}
}
,
"payee"
:
{
"email_address"
:
"
[email protected]
"
,
"merchant_id"
:
"YXZY75W2GKDQE"
}
,
"create_time"
:
"2024-10-23T20:55:19Z"
,
"update_time"
:
"2024-10-23T20:55:19Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.sandbox.paypal.com/v2/payments/captures/74L756601X447022Y
"
,
"rel"
:
"self"
,
"method"
:
"GET"
}
,
{
"href"
:
"
https://api-m.sandbox.paypal.com/v2/payments/captures/74L756601X447022Y/refund
"
,
"rel"
:
"refund"
,
"method"
:
"POST"
}
,
{
"href"
:
"
https://api-m.sandbox.paypal.com/v2/payments/authorizations/0T620041CK889853A
"
,
"rel"
:
"up"
,
"method"
:
"GET"
}
]
}
Refund captured payment
post
/v2/payments/captures/{capture_id}/refund
Try it
Refunds a captured payment, by ID. For a full refund, include an empty payload in the JSON request body. For a partial refund, include an
amount
object in the JSON request body.
Security
Oauth2
Request
path
Parameters
capture_id
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the captured payment to refund.
header
Parameters
PayPal-Request-Id
string
[ 1 .. 10000 ] characters
^.*$
A unique ID identifying the request header for idempotency purposes.
Examples
:
A request id.
A paypal-request-id header with a randomized value.
17e81d06-77ab-11e8-adc0-fa71639ebebc
Prefer
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
Default:
return=minimal
The preferred server response upon successful completion of the request. Value is:
return=minimal
. The server returns a minimal response to optimize communication between the API caller and the server. A minimal response includes the
id
,
status
and HATEOAS links.
return=representation
. The server returns a complete resource representation, including the current state of the resource.
Authorization
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
Holds authorization information for external API calls.
Examples
:
Bearer authorization.
An authorization header with information for the Bearer authorization scheme. The authorization parameter value is randomized for this example.
Bearer A21AAGHr9qtiRRXH4oYcQokQgV99rGqEIfgrr8xHCclP0OzmD9KVgg5ppIIg1jzJgQkV4wd02svIvBJyg6cLFJjFow_SjBhxQ
PayPal-Auth-Assertion
string
[ 1 .. 10000 ] characters
^.*$
Header for an API client-provided JWT assertion that identifies the merchant. Establishing the consent to act-on-behalf of a merchant is a prerequisite for using this header.
Examples
:
An auth assertion.
A paypal-auth-assertion header with a randomized value.
eyJhbGciOiJub25lIn0.eyJlbWFpbCI6Im15QGVtYWlsLmNvbSJ9
Request Body schema:
application/json
optional
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
custom_id
string
[ 1 .. 127 ] characters
^.*$
The API caller-provided external ID. Used to reconcile API caller-initiated transactions with PayPal transactions. Appears in transaction and settlement reports. The pattern is defined by an external party and supports Unicode.
invoice_id
string
[ 1 .. 127 ] characters
^.*$
The API caller-provided external invoice ID for this order. The pattern is defined by an external party and supports Unicode.
note_to_payer
string
[ 1 .. 255 ] characters
^.*$
The reason for the refund. Appears in both the payer's transaction history and the emails that the payer receives. The pattern is defined by an external party and supports Unicode.
payment_instruction
object
(
payment_instruction
)
Any additional payments instructions during refund payment processing. This object is only applicable to merchants that have been enabled for PayPal Commerce Platform for Marketplaces and Platforms capability. Please speak to your account manager if you want to use this capability.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows refund details.
201
A successful request returns the HTTP
201 Created
status code and a JSON response body that shows refund details.
400
The request failed because it is not well-formed or is syntactically incorrect or violates schema.
401
Unauthorized.
403
Forbidden.
404
Not Found.
409
The request failed because a previous call for the given resource is in progress.
422
The request failed because it either is semantically incorrect or failed business validation.
500
Internal Server Error.
default
Default response.
Request samples
Payload
application/json
Refund Captured Payment - 200 idempotent response
Refund Captured Payment with an empty request
Refund Captured Payment
Refund Captured Payment with Buyer Context (Personal Account)
Refund Captured Payment with Buyer Context (Business Account)
Refund Captured Payment with Buyer Context (Guest Checkout)
Refund Captured Payment - 200 idempotent response
Refunds a captured payment, by ID. For a full refund, include an empty payload in the request body. For a partial refund, include an
amount
object.
Copy
Expand all
Collapse all
{
"amount"
:
{
"value"
:
"1.00"
,
"currency_code"
:
"USD"
}
,
"invoice_id"
:
"RefundInvoice-123"
,
"custom_id"
:
"RefundCustom-123"
}
Response samples
200
201
400
401
403
404
409
422
500
default
5 more
404
409
422
500
default
5 more
application/json
Refund Captured Payment - 200 idempotent response
Refund Captured Payment - 200 idempotent response
Refunds a captured payment, by ID. For a full refund, include an empty payload in the request body. For a partial refund, include an
amount
object.
Copy
Expand all
Collapse all
{
"id"
:
"0K35355239430361V"
,
"amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"1.00"
}
,
"seller_payable_breakdown"
:
{
"gross_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"1.00"
}
,
"paypal_fee"
:
{
"currency_code"
:
"USD"
,
"value"
:
"0.00"
}
,
"net_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"1.00"
}
,
"total_refunded_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"11.00"
}
}
,
"invoice_id"
:
"RefundInvoice-14_10_2024_4_58_32_pm"
,
"custom_id"
:
"RefundCustom-14_10_2024_4_58_32_pm"
,
"status"
:
"COMPLETED"
,
"create_time"
:
"2024-10-14T14:58:34-07:00"
,
"update_time"
:
"2024-10-14T14:58:34-07:00"
,
"links"
:
[
{
"href"
:
"
https://api.paypal.com/v2/payments/refunds/0K35355239430361V
"
,
"rel"
:
"self"
,
"method"
:
"GET"
}
,
{
"href"
:
"
https://api.paypal.com/v2/payments/captures/7TK53561YB803214S
"
,
"rel"
:
"up"
,
"method"
:
"GET"
}
]
}
Find a list of eligible payment methods.
post
/v2/payments/find-eligible-methods
Try it
Get a list of eligible payment methods based on the input parameters provided.
Security
Oauth2
Request
header
Parameters
Authorization
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
Holds authorization information for external API calls.
Examples
:
Bearer authorization.
An authorization header with information for the Bearer authorization scheme. The authorization parameter value is randomized for this example.
Bearer A21AAGHr9qtiRRXH4oYcQokQgV99rGqEIfgrr8xHCclP0OzmD9KVgg5ppIIg1jzJgQkV4wd02svIvBJyg6cLFJjFow_SjBhxQ
PayPal-Auth-Assertion
string
[ 1 .. 10000 ] characters
^.*$
Header for an API client-provided JWT assertion that identifies the merchant. Establishing the consent to act-on-behalf of a merchant is a prerequisite for using this header.
Examples
:
An auth assertion.
A paypal-auth-assertion header with a randomized value.
eyJhbGciOiJub25lIn0.eyJlbWFpbCI6Im15QGVtYWlsLmNvbSJ9
User-Agent
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
A characteristic string that lets servers and network peers identify the application, operating system, vendor, and/or version of the requesting user agent. API calls made by PayPal SDKs SHOULD be identified using this request header.
Examples
:
A user-agent for Safari on iPad.
A user-agent header for Safari on iPad.
Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405
PayPal-Client-Metadata-Id
string
(
GUID
)
[ 1 .. 68 ] characters
^[A-Za-z0-9-{}(),]*$
A GUID value originating from Fraudnet and Dyson passed from external API clients via HTTP header. The value is used by Risk decisions to correlate calls which, in turn, might result in lower decline rates..
Examples
:
A GUID.
A paypal-client-metadata-id header with a randomized value.
1295065d-6f34-42dc-ac65-fac0c86af250
Request Body schema:
application/json
optional
customer
object
(
Customer
)
Customer who is making a purchase from the merchant/partner.
purchase_units
Array of
objects
(
eligibility_purchase_unit_request
)
[ 1 .. 10 ] items
Array of purchase units.
preferences
object
(
Preferences
)
Preferences of merchant/partner consuming the API.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that provides list of eligibile payments.
400
The request failed because it is not well-formed or is syntactically incorrect or violates schema.
401
Unauthorized.
403
Forbidden.
422
The request failed because it either is semantically incorrect or failed business validation.
500
Internal Server Error.
default
Default response.
Request samples
Payload
application/json
Eligible Payment Methods - Exclude listed payment methods
Eligible Payment Methods for a customer who is purchasing from multiple sellers
Eligible Payment Methods with User-Agent header
Eligible Payment Methods without payment token information
Customer recognition using customer email and phone number
Customer recognition using customer email and phone number
Customer recognition using customer email and phone number
Customer recognition using customer email and phone number
Eligible Payment Methods - with payment tokens
Cards Payment Method
Apple Pay Payment Method
Eligible Payment Methods - 400 Invalid Request
Eligible Payment Methods - 422 Unprocessable Entity
Basic Cards Payment Method
Google Pay Payment Method
Find Eligible Payment Methods with ACH
Eligible Payment Methods - Exclude listed payment methods
Eligible Payment Methods - Exclude listed payment methods
Copy
Expand all
Collapse all
{
"customer"
:
{
"country_code"
:
"US"
,
"channel"
:
{
"browser_type"
:
"SAFARI"
,
"device_type"
:
"MOBILE"
,
"client_os"
:
"IOS"
}
}
,
"purchase_units"
:
[
{
"amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"100.00"
}
}
]
,
"preferences"
:
{
"payment_source_constraint"
:
{
"constraint_type"
:
"EXCLUDE"
,
"payment_sources"
:
[
"PAYPAL"
]
}
}
}
Response samples
200
400
401
403
422
500
default
2 more
500
default
2 more
application/json
Eligible Payment Methods - Exclude listed payment methods
Eligible Payment Methods for a customer who is purchasing from multiple sellers
Eligible Payment Methods with User-Agent header
Eligible Payment Methods without payment token information
Customer recognition using customer email and phone number
Customer recognition using customer email and phone number
Customer recognition using customer email and phone number
Customer recognition using customer email and phone number
Eligible Payment Methods - with payment tokens
Cards Payment Method
Apple Pay Payment Method
Basic Cards Payment Method
Google Pay Payment Method
Find Eligible Payment Methods with ACH
Eligible Payment Methods - Exclude listed payment methods
Eligible Payment Methods - Exclude listed payment methods
Copy
Expand all
Collapse all
{
"eligible_methods"
:
{
"venmo"
:
{
"can_be_vaulted"
:
true
}
}
}
Show refund details
get
/v2/payments/refunds/{refund_id}
Try it
Shows details for a refund, by ID.
Security
Oauth2
Request
path
Parameters
refund_id
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the refund for which to show details.
header
Parameters
Authorization
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
Holds authorization information for external API calls.
Examples
:
Bearer authorization.
An authorization header with information for the Bearer authorization scheme. The authorization parameter value is randomized for this example.
Bearer A21AAGHr9qtiRRXH4oYcQokQgV99rGqEIfgrr8xHCclP0OzmD9KVgg5ppIIg1jzJgQkV4wd02svIvBJyg6cLFJjFow_SjBhxQ
PayPal-Auth-Assertion
string
[ 1 .. 10000 ] characters
^.*$
Header for an API client-provided JWT assertion that identifies the merchant. Establishing the consent to act-on-behalf of a merchant is a prerequisite for using this header.
Examples
:
An auth assertion.
A paypal-auth-assertion header with a randomized value.
eyJhbGciOiJub25lIn0.eyJlbWFpbCI6Im15QGVtYWlsLmNvbSJ9
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows refund details.
401
Unauthorized.
403
Forbidden.
404
Not Found.
500
Internal Server Error.
default
Default response.
Response samples
200
401
403
404
500
default
1 more
default
1 more
application/json
Show Refund Details with Platform Fees
Show Refund Details with Buyer Context (Personal Account)
Show Refund Details with Buyer Context (Business Account)
Show Refund Details with Buyer Context (Guest Checkout)
Show Refund Details with Platform Fees
Shows details for a refund, by ID, with platform fees.
Copy
Expand all
Collapse all
{
"id"
:
"1JU08902781691411"
,
"amount"
:
{
"value"
:
"10.99"
,
"currency_code"
:
"USD"
}
,
"status"
:
"COMPLETED"
,
"note"
:
"Defective product"
,
"seller_payable_breakdown"
:
{
"gross_amount"
:
{
"value"
:
"10.99"
,
"currency_code"
:
"USD"
}
,
"paypal_fee"
:
{
"value"
:
"0.33"
,
"currency_code"
:
"USD"
}
,
"platform_fees"
:
[
{
"amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"1.00"
}
,
"payee"
:
{
"email_address"
:
"
[email protected]
"
}
}
]
,
"net_amount"
:
{
"value"
:
"9.66"
,
"currency_code"
:
"USD"
}
,
"total_refunded_amount"
:
{
"value"
:
"10.99"
,
"currency_code"
:
"USD"
}
}
,
"invoice_id"
:
"INVOICE-123"
,
"create_time"
:
"2018-09-11T23:24:19Z"
,
"update_time"
:
"2018-09-11T23:24:19Z"
,
"links"
:
[
{
"rel"
:
"self"
,
"method"
:
"GET"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/refunds/1JU08902781691411
"
}
,
{
"rel"
:
"up"
,
"method"
:
"GET"
,
"href"
:
"
https://api-m.paypal.com/v2/payments/captures/2GG279541U471931P
"
}
]
}
Errors
AUTH_CAPTURE_CURRENCY_MISMATCH
Message:
Currency of capture must be the same as currency of authorization.
Description:
Verify the currency of the capture and try the request again.
AUTH_CURRENCY_MISMATCH
Message:
The currency specified during reauthorization should be the same as the currency specified in the original authorization. Please check the currency of the authorization for which you are trying to reauthorize and try again.
AUTHENTICATION_FAILURE
Message:
Authentication failed due to missing authorization header, or invalid authentication credentials.
Description:
Account validations failed for the user.
AUTHORIZATION_ALREADY_CAPTURED
Message:
Authorization has already been captured.
Description:
If
final_capture
is set to to
true
, additional captures are not possible against the authorization.
AUTHORIZATION_AMOUNT_EXCEEDED
Description:
Authorization amount specified exceeded allowable limit. Specify a different amount and try the request again. Alternately, contact Customer Support to increase your limits. Local regulations (e.g. in PSD2 countries) prohibit overages above the amount authorized by the payer.
AUTHORIZATION_DENIED
Message:
A denied authorization cannot be captured.
Description:
You cannot capture a denied authorization.
AUTHORIZATION_EXPIRED
Message:
An expired authorization cannot be captured.
Description:
You cannot capture an expired authorization.
AUTHORIZATION_VOIDED
Message:
A voided authorization cannot be captured or reauthorized.
Description:
You cannot capture or reauthorize a voided authorization.
CANNOT_BE_NEGATIVE
Description:
Must be greater than or equal to 0.
CANNOT_BE_VOIDED
Message:
A reauthorization cannot be voided. Please void the original parent authorization.
Description:
You cannot void a reauthorized payment. You must void the original parent authorized payment.
CANNOT_BE_ZERO_OR_NEGATIVE
Message:
Must be greater than zero. If the currency supports decimals, only two decimal place precision is supported.
Description:
Specify a different value and try the request again.
CANNOT_REFUND_SELF
Description:
The payer and payee for the refund cannot be same.
CAPTURE_FULLY_REFUNDED
Message:
The capture has already been fully refunded.
Description:
You cannot capture additional refunds against this capture.
CAPTURED_AMOUNT_FULLY_REFUNDED
Description:
The captured amount has already been fully refunded.
CARD_BILLING_ADDRESS_COUNTRY_NOT_SUPPORTED
Description:
Specified country is not currently supported for payment processing.
CARD_BRAND_NOT_SUPPORTED
Description:
Refund cannot be issued to this card. The card brand
card_brand
is not supported. Please try again with another card.
CARD_EXPIRED
Description:
The card is expired.
CARD_ISSUER_COUNTRY_NOT_SUPPORTED
Description:
Card is issued by a financial institution for a country (e.g. Cuba, Iran, North Korea, Syria) that is not current supported for payment processing.
CARD_TYPE_NOT_SUPPORTED
Description:
Processing of this card type is not supported. Use another type of card.
COMPLIANCE_VIOLATION
Description:
Transaction is declined due to compliance violation.
CURRENCY_MISMATCH
Message:
All amounts specified should be in the same currency. Please ensure that the currency for the 'amount' and that of 'platform_fees.amount' is the same.
CURRENCY_NOT_SUPPORTED_FOR_CARD_BRAND
Description:
Currency not supported for card specified. Card is
card_brand
. Only
currency_code
is supported for this brand of card.
CURRENCY_NOT_SUPPORTED_FOR_CARD_TYPE
Description:
Currency code not supported for direct card payments using this card type. See
Currency codes
for list of supported currency codes.
CURRENCY_NOT_SUPPORTED_FOR_COUNTRY
Description:
Currency code not supported for card payments in your country.
DECIMAL_PRECISION
Message:
The value of the field should not be more than two decimal places.
Description:
If the currency supports decimals, only two decimal place precision is supported.
DECIMALS_NOT_SUPPORTED
Message:
Currency does not support decimals.
Description:
Currency does not support decimals. Please refer to
https://developer.paypal.com/docs/api/reference/currency-codes/
for more information.
DELAYED_DISBURSEMENT_NOT_SUPPORTED
Message:
The API Caller is not enabled to process transactions by specifying disbursement mode as delayed.
Description:
Verify the API caller is enabled to process transaction with delayed disbursement.
DUPLICATE_INVOICE_ID
Message:
Requested invoice number has been previously captured. Possible duplicate transaction.
Description:
Payment for this invoice was already captured.
DUPLICATE_REFUND
Description:
Requested invoice_id has been previously refunded. Possible duplicate transaction.
DUPLICATE_TRANSACTION
Description:
Duplicate invoice Id detected.
FX_RATE_CHANGE_DUE_TO_MARKET_EVENT
Description:
The FX rate associated with the specified FX rate ID has been changed due to market events. Please refer to the provided new_fx_id link to retrieve a new FX rate ID and try the request again.
INSTRUMENT_DECLINED
Description:
The instrument presented was either declined by the processor or bank, or it can't be used for this payment.
INTERNAL_SERVER_ERROR
Message:
An internal server error has occurred.
Description:
Try your request again later.
INVALID_ACCOUNT_STATUS
Message:
Account validations failed for the user.
Description:
The user account could not be validated.
INVALID_ARRAY_LENGTH
Message:
Request is not well-formed, syntactically incorrect, or violates schema.
Description:
The number of items in an array parameter is too small or too large.
INVALID_CARD_NUMBER
Description:
The card number is invalid.
INVALID_COUNTRY_CODE
Message:
The requested action could not be performed, semantically incorrect, or failed business validation.
Description:
Country code is invalid. Please refer to
https://developer.paypal.com/docs/integration/direct/rest/country-codes/
for a list of supported country codes.
INVALID_CURRENCY_CODE
Message:
Currency code should be a three-character ISO-4217 currency code.
Description:
Currency code is invalid or is not currently supported. Please refer
https://developer.paypal.com/docs/api/reference/currency-codes/
for list of supported currency codes.
INVALID_FX_RATE_ID
Description:
The specified FX Rate ID is not valid.
INVALID_INVOICE_ID
Message:
Specified invoice_id does not exist.
Description:
Please check the invoice_id and try again.
INVALID_PARAMETER_SYNTAX
Message:
The value of the field does not conform to the expected format.
Description:
Verify the specification for supported
pattern
and try the request again.
INVALID_PARAMETER_VALUE
Message:
The value of a field is invalid.
Description:
Verify the specification for the allowed values and try the request again.
INVALID_PAYEE_ACCOUNT
Message:
Payee account is invalid.
Description:
Verify the payee account information and try the request again.
INVALID_PLATFORM_FEES_ACCOUNT
Message:
The specified platform_fees payee account is either invalid or account setup is incomplete. Please work with your PayPal Account Manager to enable this option for your account.
Description:
Verify the platform fee account set up is completed or correct account.
INVALID_PLATFORM_FEES_AMOUNT
Message:
The
platform_fees
amount cannot be greater than the capture amount.
Description:
Verify the
platform_fees
amount and try the request again.
INVALID_RESOURCE_ID
Message:
Specified resource ID does not exist. Please check the resource ID and try again.
Description:
Verify the resource ID and try the request again.
INVALID_SECURITY_CODE_LENGTH
Description:
The security_code length is invalid for the specified card brand.
INVALID_STRING_LENGTH
Message:
The value of a field is either too short or too long.
Description:
Verify the specification for the supported
min
and
max
values and try the request again.
INVALID_STRING_MAX_LENGTH
Message:
The value of a field is too long.
Description:
The parameter string is too long.
KYC_HOLD
Message:
The merchant's KYC status is incomplete.
Description:
The payment was pending due to the merchant's incomplete KYC status.
MALFORMED_REQUEST_JSON
Message:
Request is not well-formed, syntactically incorrect, or violates schema.
Description:
The request JSON is not well formed.
MAX_CAPTURE_AMOUNT_EXCEEDED
Message:
Capture amount exceeds allowable limit. Please contact customer service or your account manager to request the change to your overage limit. The default overage limit is 115%, which allows the sum of all captures to be up to 115% of the order amount. Local regulations (e.g. in PSD2 countries) prohibit overages above the amount authorized by the payer.
Description:
Specify a different amount and try the request again. Alternately, contact Customer Support to increase your limits.
MAX_CAPTURE_COUNT_EXCEEDED
Message:
Maximum number of allowable captures has been reached. No additional captures are possible for this authorization. Please contact customer service or your account manager to change the number of captures that be made for a given authorization.
Description:
You cannot make additional captures.
MAX_NUMBER_OF_REFUNDS_EXCEEDED
Message:
You have exceeded the number of refunds that can be processed per capture.
Description:
Please contact customer support or your account manager to review the number of refunds that can be processed per capture.
MAX_PAYEE_AMOUNT_LIMIT_EXCEEDED
Description:
Refund amount exceeds the allowed cumulative limit that the payee can receive.
MAX_PAYER_AMOUNT_LIMIT_EXCEEDED
Description:
Refund amount exceeds the allowed cumulative limit that the payer can refund.
MAX_REFUND_LIMIT_EXCEEDED
Description:
Refund amount exceeds allowable limit. Specify a different amount and try the request again. Alternately, contact Customer Support to increase your limits.
MISSING_REQUIRED_PARAMETER
Message:
A required field / parameter is missing.
Description:
Verify the specification for
required
fields and try the request again.
MULTI_CURRENCY_CODE
Message:
The requested action could not be performed, semantically incorrect, or failed business validation.
Description:
Multiple differing values of currency_code are not supported. Entire request must have the same currency_code.
MULTIPLE_AUTHORIZATIONS_FOUND
Message:
Cannot void multiple authorizations.
Description:
Specified invoice_id is associated with more than one authorization.
NOT_AUTHORIZED
Message:
You do not have permission to access or perform operations on this resource.
Description:
To make API calls on behalf of a merchant, ensure that you have sufficient permissions to proceed with this transaction.
PARTIAL_REFUND_NOT_ALLOWED
Message:
You cannot do a refund for an amount less than the original capture amount.
Description:
Specify an amount equal to the capture amount or omit the
amount
object from the request. Then, try the request again.
PAYEE_ACCOUNT_INVALID
Message:
The requested action could not be performed, semantically incorrect, or failed business validation.
Description:
Payee account specified is invalid. Please check the
payee.merchant_id
specified and try again.
PAYEE_ACCOUNT_LOCKED_OR_CLOSED
Message:
Transaction could not complete because payee account is locked or closed.
Description:
To get more information about the status of the account, call Customer Support.
PAYEE_ACCOUNT_RESTRICTED
Message:
Payee account is restricted.
Description:
To get more information about the status of the account, call Customer Support.
PAYEE_FX_RATE_ID_CURRENCY_MISMATCH
Description:
The specified FX Rate ID is for a currency that does not match with the currency of this request.
PAYEE_FX_RATE_ID_EXPIRED
Description:
The specified FX Rate ID has expired.
PAYEE_NOT_CONSENTED
Description:
Payee does not have appropriate consent to allow the API caller to process this type of transaction on their behalf. Your current setup requires the 'payee' to provide a consent before this transaction can be processed successfully.
PAYEE_REFUND_AMOUNT_LIMIT_EXCEEDED
Description:
Refund amount exceeds per transaction limit that the payee can receive.
PAYER_ACCOUNT_LOCKED_OR_CLOSED
Message:
The payer account cannot be used for this transaction.
Description:
Contact the payer for an alternate payment method.
PAYER_ACCOUNT_RESTRICTED
Message:
Payer account is restricted.
Description:
To get more information about the status of the account, call Customer Support.
PAYER_CANNOT_PAY
Message:
Payer cannot pay for this transaction.
Description:
Please contact the payer to find other ways to pay for this transaction.
PAYER_REFUND_AMOUNT_LIMIT_EXCEEDED
Description:
Refund amount exceeds per transaction limit that the payer can refund.
PENDING_CAPTURE
Message:
Cannot initiate a refund as the capture is pending.
Description:
Capture is typically pending when the payer has funded the transaction by using an e-check or bank account.
PERMISSION_DENIED
Message:
You do not have permission to access or perform operations on this resource.
Description:
To make API calls on behalf of a merchant, ensure that you have sufficient permissions to proceed with this transaction.
PERMISSION_NOT_GRANTED
Message:
Payee of the authorization has not granted permission to perform capture on the authorization.
Description:
To make API calls on behalf of a merchant, ensure that you have sufficient permissions to capture the authorization.
PLATFORM_FEE_EXCEEDED
Message:
Platform fee amount specified exceeds the amount that is available for refund. You can only refund up to the available platform fee amount. This error is also returned when no platform_fee was specified or was zero when the payment was captured.
PLATFORM_FEE_NOT_ENABLED
Message:
The API Caller account is not setup to be able to process refunds with 'platform_fees'. Please contact your Account Manager. This feature is useful when you want to contribute a portion of the 'platform_fees' you had capture as part of the refund being processed.
PLATFORM_FEES_NOT_SUPPORTED
Message:
The API Caller is not enabled to process transactions by specifying 'platform_fees'. Please work with your PayPal Account Manager to enable this option for your account.
Description:
Verify the API caller is enabled to process the transaction with platform fees.
PREVIOUS_REQUEST_IN_PROGRESS
Message:
A previous request on this resource is currently in progress. Please wait for sometime and try again. It is best to space out the initial and the subsequent request(s) to avoid receiving this error.
Description:
This scenario only occurs when making multiple API requests on the same resource within a very short duration. To resolve this, API callers need to make subsequent requests with a delay.
PREVIOUSLY_CAPTURED
Message:
Authorization has been previously captured and hence cannot be voided.
Description:
This authorized payment was already captured. You cannot capture it again.
PREVIOUSLY_VOIDED
Message:
Authorization has been previously voided and hence cannot be voided again.
Description:
This authorized payment was already voided. You cannot void it again.
RATE_LIMIT_REACHED
Message:
Too many requests. Blocked due to rate limiting.
Description:
The rate limit was reached.
REAUTHORIZATION_DECLINED_BY_PROCESSOR
Description:
The reauthorization was declined by the processor.
REAUTHORIZATION_NOT_SUPPORTED
Message:
A reauthorize cannot be attempted on an authorization_id that is the result of a prior reauthorization or on an authorization made on an Order saved using the
v2/orders/id/save
API.
REAUTHORIZATION_NOT_SUPPORTED_FOR_PAYMENT_SOURCE
Description:
Reauthorization is not supported for the payment source.
REAUTHORIZATION_TOO_SOON
Description:
A reauthorization is only allowed once from Day 4 to Day 29 since the date of the original authorization.
REFUND_AMOUNT_EXCEEDED
Message:
The refund amount must be less than or equal to the capture amount that has not yet been refunded.
Description:
Verify the refund amount and try the request again.
REFUND_AMOUNT_TOO_LOW
Message:
The amount after applying currency conversion is zero and hence the capture cannot be refunded. The currency conversion is required because the currency of the capture is different than the currency in which the amount was settled into the payee account.
Description:
The amount after applying currency conversion is zero and hence the capture cannot be refunded. The currency conversion is required because the currency of the capture is different than the currency in which the amount was settled into the payee account.
REFUND_CAPTURE_CURRENCY_MISMATCH
Message:
Refund must be in the same currency as the capture.
Description:
Verify the currency of the refund and try the request again.
REFUND_CURRENCY_MISMATCH
Description:
Refund must be in the same currency as the capture.
REFUND_FAILED_BY_PAYMENT_SOURCE
Message:
Refund was refused by the payment source.
Description:
We're unable to process refunds for the payer's selected payment source. Contact the payer directly to arrange a refund via alternative means.
REFUND_FAILED_INSUFFICIENT_FUNDS
Message:
Refund cannot be processed due to insufficient funds.
Description:
Capture could not be refunded due to insufficient funds. Please check to see if you have sufficient funds in your PayPal account or if the bank account linked to your PayPal account is verified and has sufficient funds.
REFUND_FUNDS_NOT_AVAILABLE
Description:
There is no valid funding instrument linked to the account from which refund can be processed.
REFUND_IS_RESTRICTED
Message:
This refund can only be processed by the API caller that had 'captured' the transaction. If you facilitate your transactions via a platform/partner, please initiate a refund through them.
REFUND_NOT_ALLOWED
Message:
Capture cannot be refunded.
Description:
You cannot refund this capture.
REFUND_NOT_PERMITTED_DUE_TO_CHARGEBACK
Message:
The requested action could not be performed, semantically incorrect, or failed business validation.
Description:
Refunds not allowed on this capture due to a chargeback on the card or bank. Please contact the payee to resolve the chargeback.
REFUND_NOT_SUPPORTED_FOR_PAYMENT_SOURCE
Message:
Refund was refused by the payment source.
Description:
Refunds are not supported for the payer's selected payment source. Contact the payer directly to arrange a refund via alternative means.
REFUND_REFUSED_BY_PROCESSOR
Description:
The funding instrument linked to the account has been declined by either the processor or PayPal internal system.
REFUND_TIME_EXCEEDED_FOR_PAYMENT_SOURCE
Message:
Refund was refused by the payment source.
Description:
The time limit set by the payer's selected payment source to refund this transaction has expired. Contact the payer directly to arrange a refund via alternative means.
REFUND_TIME_LIMIT_EXCEEDED
Message:
You are over the time limit to perform a refund on this capture.
Description:
The refund cannot be issued at this time.
REFUND_TRANSACTION_REFUSED
Description:
PayPal's internal controls or user account settings prevent refund from being processed.
SHIPPING_ADDRESS_INVALID
Message:
Address field does not match the corresponding validation regex.
SHIPPING_ADDRESS_NOT_ALLOWED_BY_RESIDENCE_COUNTRY
Message:
The provided shipping address is not allowed by buyer's residency country.
TRANSACTION_DISPUTED
Message:
Partial refunds cannot be offered at this time because there is an open case on this transaction. Visit the PayPal Resolution Center to review this case.
Description:
Refund for an amount less than the remaining transaction amount cannot be processed at this time because of an open dispute on the capture. Please visit the PayPal Resolution Center to view the details.
TRANSACTION_REFUSED
Message:
PayPal's internal controls prevent authorization from being captured.
Description:
For more information about this transaction, contact customer support.
UPDATE_AUTHORIZATION_NOT_SUPPORTED
Message:
Update authorization is not allowed for this type of authorization.
Definitions
activity_timestamps
The date and time stamps that are common to authorized payment, captured payment, and refund transactions.
create_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
update_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
Copy
{
"create_time"
:
"string"
,
"update_time"
:
"string"
}
Advanced Cards Config
Configuration details for advanced card payment methods including credit and debit card processing capabilities.
can_be_vaulted
boolean
Indicates if the payment method can be saved for future use.
supports_installments
boolean
Indicates if installment payment option is available.
vendors
Array of
objects
(
Card Vendor
)
[ 1 .. 100 ] items
Payment card vendors configuration.
Copy
Expand all
Collapse all
{
"can_be_vaulted"
:
true
,
"supports_installments"
:
true
,
"vendors"
:
[
{
"network"
:
"AMEX"
,
"eligible"
:
true
,
"can_be_vaulted"
:
true
,
"branded"
:
true
}
]
}
amount_breakdown
The breakdown of the amount. Breakdown provides details such as total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
item_total
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
shipping
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
handling
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
tax_total
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
insurance
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
shipping_discount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
discount
object
(
discount_with_breakdown
)
The discount amount and currency code. For list of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
Copy
Expand all
Collapse all
{
"item_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"handling"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"tax_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"insurance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping_discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
amount_with_breakdown
The total order amount with an optional breakdown that provides details, such as the total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
If you specify
amount.breakdown
, the amount equals
item_total
plus
tax_total
plus
shipping
plus
handling
plus
insurance
minus
shipping_discount
minus discount.
The amount must be a positive number. For listed of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
currency_code
required
string
(
currency_code
)
= 3 characters
^[\S\s]*$
The
three-character ISO-4217 currency code
that identifies the currency.
value
required
string
[ 0 .. 32 ] characters
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The value, which might be:
An integer for currencies like
JPY
that are not typically fractional.
A decimal fraction for currencies like
TND
that are subdivided into thousandths.
For the required number of decimal places for a currency code, see
Currency Codes
.
breakdown
object
(
amount_breakdown
)
The breakdown of the amount. Breakdown provides details such as total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
Copy
Expand all
Collapse all
{
"currency_code"
:
"str"
,
"value"
:
"string"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"handling"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"tax_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"insurance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping_discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
}
Apple Pay Config
Configuration details for Apple Pay payment method.
eligible
required
boolean
Indicates if Apple Pay is eligible.
merchant_country
required
string
(
country_code-2
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
supported_networks
required
Array of
strings
[ 1 .. 100 ] items
Supported card networks.
Items
Enum Value
Description
MASTERCARD
MasterCard network.
DISCOVER
Discover network.
VISA
Visa network.
AMEX
American Express network.
merchant_capabilities
required
Array of
strings
[ 1 .. 10 ] items
An array of the payment capabilities that the merchant supports.
Items
Enum Value
Description
SUPPORTS_CREDIT
Merchant supports credit card payments.
SUPPORTS_DEBIT
Merchant supports debit card payments.
SUPPORTS_3DS
Merchant supports 3D Secure authentication.
token_notification_url
required
string
<
uri
>
[ 10 .. 2000 ] characters
Token notification url for recurring payment request.
Copy
Expand all
Collapse all
{
"eligible"
:
true
,
"merchant_country"
:
"string"
,
"supported_networks"
:
[
"MASTERCARD"
]
,
"merchant_capabilities"
:
[
"SUPPORTS_CREDIT"
]
,
"token_notification_url"
:
"
http://example.com
"
}
authorization
The authorized payment transaction.
status
string
(
Authorization Status
)
The status for the authorized payment.
Enum Value
Description
CREATED
The authorized payment is created. No captured payments have been made for this authorized payment.
CAPTURED
The authorized payment has one or more captures against it. The sum of these captured payments is greater than the amount of the original authorized payment.
DENIED
PayPal cannot authorize funds for this authorized payment.
PARTIALLY_CAPTURED
A captured payment was made for the authorized payment for an amount that is less than the amount of the original authorized payment.
VOIDED
The authorized payment was voided. No more captured payments can be made against this authorized payment.
PENDING
The created authorization is in pending state. For more information, see
status.details
.
status_details
object
(
authorization_status_details
)
The details of the authorized payment status.
id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the authorized payment.
amount
object
(
amount_with_breakdown
)
The total order amount with an optional breakdown that provides details, such as the total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
If you specify
amount.breakdown
, the amount equals
item_total
plus
tax_total
plus
shipping
plus
handling
plus
insurance
minus
shipping_discount
minus discount.
The amount must be a positive number. For listed of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
invoice_id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The API caller-provided external invoice number for this order. Appears in both the payer's transaction history and the emails that the payer receives.
custom_id
string
[ 0 .. 255 ] characters
^[\S\s]*$
The API caller-provided external ID. Used to reconcile API caller-initiated transactions with PayPal transactions. Appears in transaction and settlement reports.
network_transaction_reference
object
(
network_transaction
)
Reference values used by the card network to identify a transaction.
seller_protection
object
(
seller_protection
)
The level of protection offered as defined by
PayPal Seller Protection for Merchants
.
expiration_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
links
Array of
objects
(
Link Description
)
[ 0 .. 32767 ] items
An array of related
HATEOAS links
.
create_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
update_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
Copy
Expand all
Collapse all
{
"status"
:
"CREATED"
,
"status_details"
:
{
"reason"
:
"PENDING_REVIEW"
}
,
"id"
:
"string"
,
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"handling"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"tax_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"insurance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping_discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
}
,
"invoice_id"
:
"string"
,
"custom_id"
:
"string"
,
"network_transaction_reference"
:
{
"id"
:
"stringstr"
,
"date"
:
"stri"
,
"network"
:
"VISA"
,
"acquirer_reference_number"
:
"string"
}
,
"seller_protection"
:
{
"status"
:
"ELIGIBLE"
,
"dispute_categories"
:
[
"ITEM_NOT_RECEIVED"
]
}
,
"expiration_time"
:
"string"
,
"links"
:
[
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
]
,
"create_time"
:
"string"
,
"update_time"
:
"string"
}
Authorization
The authorized payment transaction.
status
string
(
Authorization Status
)
The status for the authorized payment.
Enum Value
Description
CREATED
The authorized payment is created. No captured payments have been made for this authorized payment.
CAPTURED
The authorized payment has one or more captures against it. The sum of these captured payments is greater than the amount of the original authorized payment.
DENIED
PayPal cannot authorize funds for this authorized payment.
PARTIALLY_CAPTURED
A captured payment was made for the authorized payment for an amount that is less than the amount of the original authorized payment.
VOIDED
The authorized payment was voided. No more captured payments can be made against this authorized payment.
PENDING
The created authorization is in pending state. For more information, see
status.details
.
status_details
object
(
authorization_status_details
)
The details of the authorized payment status.
id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the authorized payment.
amount
object
(
amount_with_breakdown
)
The total order amount with an optional breakdown that provides details, such as the total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
If you specify
amount.breakdown
, the amount equals
item_total
plus
tax_total
plus
shipping
plus
handling
plus
insurance
minus
shipping_discount
minus discount.
The amount must be a positive number. For listed of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
invoice_id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The API caller-provided external invoice number for this order. Appears in both the payer's transaction history and the emails that the payer receives.
custom_id
string
[ 0 .. 255 ] characters
^[\S\s]*$
The API caller-provided external ID. Used to reconcile API caller-initiated transactions with PayPal transactions. Appears in transaction and settlement reports.
network_transaction_reference
object
(
network_transaction
)
Reference values used by the card network to identify a transaction.
seller_protection
object
(
seller_protection
)
The level of protection offered as defined by
PayPal Seller Protection for Merchants
.
expiration_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
links
Array of
objects
(
Link Description
)
[ 0 .. 32767 ] items
An array of related
HATEOAS links
.
create_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
update_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
supplementary_data
object
(
Payment Supplementary Data
)
The supplementary data.
payee
object
(
payee_base
)
The details for the merchant who receives the funds and fulfills the order. The merchant is also known as the payee.
Copy
Expand all
Collapse all
{
"status"
:
"CREATED"
,
"status_details"
:
{
"reason"
:
"PENDING_REVIEW"
}
,
"id"
:
"string"
,
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"handling"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"tax_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"insurance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping_discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
}
,
"invoice_id"
:
"string"
,
"custom_id"
:
"string"
,
"network_transaction_reference"
:
{
"id"
:
"stringstr"
,
"date"
:
"stri"
,
"network"
:
"VISA"
,
"acquirer_reference_number"
:
"string"
}
,
"seller_protection"
:
{
"status"
:
"ELIGIBLE"
,
"dispute_categories"
:
[
"ITEM_NOT_RECEIVED"
]
}
,
"expiration_time"
:
"string"
,
"links"
:
[
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
]
,
"create_time"
:
"string"
,
"update_time"
:
"string"
,
"supplementary_data"
:
{
"related_ids"
:
{
"order_id"
:
"string"
,
"authorization_id"
:
"string"
,
"capture_id"
:
"string"
}
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
authorization_status
The status fields and status details for an authorized payment.
status
string
(
Authorization Status
)
The status for the authorized payment.
Enum Value
Description
CREATED
The authorized payment is created. No captured payments have been made for this authorized payment.
CAPTURED
The authorized payment has one or more captures against it. The sum of these captured payments is greater than the amount of the original authorized payment.
DENIED
PayPal cannot authorize funds for this authorized payment.
PARTIALLY_CAPTURED
A captured payment was made for the authorized payment for an amount that is less than the amount of the original authorized payment.
VOIDED
The authorized payment was voided. No more captured payments can be made against this authorized payment.
PENDING
The created authorization is in pending state. For more information, see
status.details
.
status_details
object
(
authorization_status_details
)
The details of the authorized payment status.
Copy
Expand all
Collapse all
{
"status"
:
"CREATED"
,
"status_details"
:
{
"reason"
:
"PENDING_REVIEW"
}
}
authorization_status_details
The details of the authorized payment status.
reason
string
(
Authorization Incomplete Reason
)
The reason why the authorized status is
PENDING
.
Enum Value
Description
PENDING_REVIEW
Authorization is pending manual review.
DECLINED_BY_RISK_FRAUD_FILTERS
Risk Filter set by the payee failed for the transaction.
Copy
{
"reason"
:
"PENDING_REVIEW"
}
Basic Cards Config
Configuration details for basic card payment methods including credit and debit card processing capabilities.
can_be_vaulted
boolean
Indicates if the payment method can be saved for future use.
supports_installments
boolean
Indicates if installment payment option is available.
guest_enabled
boolean
Indicates if guest checkout is enabled for this payment method.
supports_inline_presentation_mode
boolean
Indicates if inline presentation mode is supported for this payment method.
Copy
{
"can_be_vaulted"
:
true
,
"supports_installments"
:
true
,
"guest_enabled"
:
true
,
"supports_inline_presentation_mode"
:
true
}
Billing Address Parameters
Configuration parameters for billing address collection in Google Pay.
format
string
Billing address format.
Value
Description
FULL
Full billing address format.
Copy
{
"format"
:
"FULL"
}
Buyer Context
The buyer context for the refund transaction.
transaction_id
string
[ 1 .. 255 ] characters
^[0-9a-zA-Z_-]+$
The PayPal generated transaction ID associated with the buyer's refund.
transaction_details_url
string
<
uri
>
[ 1 .. 2048 ] characters
The URL for the buyer to view the transaction details.
transaction_create_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
transaction_update_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
Copy
{
"transaction_id"
:
"string"
,
"transaction_details_url"
:
"
http://example.com
"
,
"transaction_create_time"
:
"string"
,
"transaction_update_time"
:
"string"
}
capture
A captured payment.
status
string
(
Capture Status
)
The status of the captured payment.
Enum Value
Description
COMPLETED
The funds for this captured payment were credited to the payee's PayPal account.
DECLINED
The funds could not be captured.
PARTIALLY_REFUNDED
An amount less than this captured payment's amount was partially refunded to the payer.
PENDING
The funds for this captured payment was not yet credited to the payee's PayPal account. For more information, see
status.details
.
REFUNDED
An amount greater than or equal to this captured payment's amount was refunded to the payer.
FAILED
There was an error while capturing payment.
status_details
object
(
capture_status_details
)
The details of the captured payment status.
id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the captured payment.
amount
object
(
amount_with_breakdown
)
The total order amount with an optional breakdown that provides details, such as the total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
If you specify
amount.breakdown
, the amount equals
item_total
plus
tax_total
plus
shipping
plus
handling
plus
insurance
minus
shipping_discount
minus discount.
The amount must be a positive number. For listed of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
invoice_id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The API caller-provided external invoice number for this order. Appears in both the payer's transaction history and the emails that the payer receives.
custom_id
string
[ 0 .. 255 ] characters
^[\S\s]*$
The API caller-provided external ID. Used to reconcile API caller-initiated transactions with PayPal transactions. Appears in transaction and settlement reports.
network_transaction_reference
object
(
network_transaction
)
Reference values used by the card network to identify a transaction.
seller_protection
object
(
seller_protection
)
The level of protection offered as defined by
PayPal Seller Protection for Merchants
.
final_capture
boolean
Default:
false
Indicates whether you can make additional captures against the authorized payment. Set to
true
if you do not intend to capture additional payments against the authorization. Set to
false
if you intend to capture additional payments against the authorization.
seller_receivable_breakdown
object
(
Seller Receivable Breakdown
)
The detailed breakdown of the capture activity. This is not available for transactions that are in pending state.
disbursement_mode
string
(
disbursement_mode
)
Default:
"INSTANT"
The funds that are held on behalf of the merchant.
Enum Value
Description
INSTANT
The funds are released to the merchant immediately.
DELAYED
The funds are held for a finite number of days. The actual duration depends on the region and type of integration. You can release the funds through a referenced payout. Otherwise, the funds disbursed automatically after the specified duration.
links
Array of
objects
(
Link Description
)
[ 0 .. 32767 ] items
An array of related
HATEOAS links
.
processor_response
object
(
processor_response
)
The processor response information for payment requests, such as direct credit card transactions.
create_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
update_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
Copy
Expand all
Collapse all
{
"status"
:
"COMPLETED"
,
"status_details"
:
{
"reason"
:
"BUYER_COMPLAINT"
}
,
"id"
:
"string"
,
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"handling"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"tax_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"insurance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping_discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
}
,
"invoice_id"
:
"string"
,
"custom_id"
:
"string"
,
"network_transaction_reference"
:
{
"id"
:
"stringstr"
,
"date"
:
"stri"
,
"network"
:
"VISA"
,
"acquirer_reference_number"
:
"string"
}
,
"seller_protection"
:
{
"status"
:
"ELIGIBLE"
,
"dispute_categories"
:
[
"ITEM_NOT_RECEIVED"
]
}
,
"final_capture"
:
false
,
"seller_receivable_breakdown"
:
{
"gross_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"paypal_fee"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"paypal_fee_in_receivable_currency"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"net_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"receivable_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"exchange_rate"
:
{
"source_currency"
:
"string"
,
"target_currency"
:
"string"
,
"value"
:
"string"
}
,
"platform_fees"
:
[
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
]
}
,
"disbursement_mode"
:
"INSTANT"
,
"links"
:
[
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
]
,
"processor_response"
:
{
"avs_code"
:
"A"
,
"cvv_code"
:
"E"
,
"response_code"
:
"0000"
,
"payment_advice_code"
:
"01"
}
,
"create_time"
:
"string"
,
"update_time"
:
"string"
}
Capture Identifier
The capture identification-related fields. Includes the invoice ID, custom ID, note to payer, and soft descriptor.
invoice_id
string
[ 1 .. 127 ] characters
^.{1,127}$
The API caller-provided external invoice number for this order. Appears in both the payer's transaction history and the emails that the payer receives.
note_to_payer
string
[ 1 .. 255 ] characters
^.{1,255}$
An informational note about this settlement. Appears in both the payer's transaction history and the emails that the payer receives.
Copy
{
"invoice_id"
:
"string"
,
"note_to_payer"
:
"string"
}
Capture Request
Captures either a portion or the full authorized amount of an authorized payment.
invoice_id
string
[ 0 .. 127 ] characters
^[\S\s]*$
The API caller-provided external invoice number for this order. Appears in both the payer's transaction history and the emails that the payer receives.
note_to_payer
string
[ 0 .. 255 ] characters
^[\S\s]*$
An informational note about this settlement. Appears in both the payer's transaction history and the emails that the payer receives.
amount
object
(
amount_with_breakdown
)
The total order amount with an optional breakdown that provides details, such as the total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
If you specify
amount.breakdown
, the amount equals
item_total
plus
tax_total
plus
shipping
plus
handling
plus
insurance
minus
shipping_discount
minus discount.
The amount must be a positive number. For listed of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
final_capture
boolean
Default:
false
Indicates whether you can make additional captures against the authorized payment. Set to
true
if you do not intend to capture additional payments against the authorization. Set to
false
if you intend to capture additional payments against the authorization.
payment_instruction
object
(
payment_instruction
)
Any additional payment instructions to be consider during payment processing. This processing instruction is applicable for Capturing an order or Authorizing an Order.
soft_descriptor
string
[ 0 .. 22 ] characters
^[\S\s]*$
The payment descriptor on the payer's account statement.
Copy
Expand all
Collapse all
{
"invoice_id"
:
"string"
,
"note_to_payer"
:
"string"
,
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"handling"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"tax_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"insurance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping_discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
}
,
"final_capture"
:
false
,
"payment_instruction"
:
{
"platform_fees"
:
[
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
]
,
"disbursement_mode"
:
"INSTANT"
,
"payee_pricing_tier_id"
:
"string"
,
"payee_receivable_fx_rate_id"
:
"string"
}
,
"soft_descriptor"
:
"string"
}
capture_status
The status and status details of a captured payment.
status
string
(
Capture Status
)
The status of the captured payment.
Enum Value
Description
COMPLETED
The funds for this captured payment were credited to the payee's PayPal account.
DECLINED
The funds could not be captured.
PARTIALLY_REFUNDED
An amount less than this captured payment's amount was partially refunded to the payer.
PENDING
The funds for this captured payment was not yet credited to the payee's PayPal account. For more information, see
status.details
.
REFUNDED
An amount greater than or equal to this captured payment's amount was refunded to the payer.
FAILED
There was an error while capturing payment.
status_details
object
(
capture_status_details
)
The details of the captured payment status.
Copy
Expand all
Collapse all
{
"status"
:
"COMPLETED"
,
"status_details"
:
{
"reason"
:
"BUYER_COMPLAINT"
}
}
capture_status_details
The details of the captured payment status.
reason
string
(
Capture Incomplete Reason
)
The reason why the captured payment status is
PENDING
or
DENIED
.
Enum Value
Description
BUYER_COMPLAINT
The payer initiated a dispute for this captured payment with PayPal.
CHARGEBACK
The captured funds were reversed in response to the payer disputing this captured payment with the issuer of the financial instrument used to pay for this captured payment.
ECHECK
The payer paid by an eCheck that has not yet cleared.
INTERNATIONAL_WITHDRAWAL
Visit your online account. In your
Account Overview
, accept and deny this payment.
OTHER
No additional specific reason can be provided. For more information about this captured payment, visit your account online or contact PayPal.
PENDING_REVIEW
The captured payment is pending manual review.
RECEIVING_PREFERENCE_MANDATES_MANUAL_ACTION
The payee has not yet set up appropriate receiving preferences for their account. For more information about how to accept or deny this payment, visit your account online. This reason is typically offered in scenarios such as when the currency of the captured payment is different from the primary holding currency of the payee.
REFUNDED
The captured funds were refunded.
TRANSACTION_APPROVED_AWAITING_FUNDING
The payer must send the funds for this captured payment. This code generally appears for manual EFTs.
UNILATERAL
The payee does not have a PayPal account.
VERIFICATION_REQUIRED
The payee's PayPal account is not verified.
DECLINED_BY_RISK_FRAUD_FILTERS
Risk Filter set by the payee failed for the transaction.
Copy
{
"reason"
:
"BUYER_COMPLAINT"
}
Captured Payment
A captured payment.
status
string
(
Capture Status
)
The status of the captured payment.
Enum Value
Description
COMPLETED
The funds for this captured payment were credited to the payee's PayPal account.
DECLINED
The funds could not be captured.
PARTIALLY_REFUNDED
An amount less than this captured payment's amount was partially refunded to the payer.
PENDING
The funds for this captured payment was not yet credited to the payee's PayPal account. For more information, see
status.details
.
REFUNDED
An amount greater than or equal to this captured payment's amount was refunded to the payer.
FAILED
There was an error while capturing payment.
status_details
object
(
capture_status_details
)
The details of the captured payment status.
id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the captured payment.
amount
object
(
amount_with_breakdown
)
The total order amount with an optional breakdown that provides details, such as the total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
If you specify
amount.breakdown
, the amount equals
item_total
plus
tax_total
plus
shipping
plus
handling
plus
insurance
minus
shipping_discount
minus discount.
The amount must be a positive number. For listed of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
invoice_id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The API caller-provided external invoice number for this order. Appears in both the payer's transaction history and the emails that the payer receives.
custom_id
string
[ 0 .. 255 ] characters
^[\S\s]*$
The API caller-provided external ID. Used to reconcile API caller-initiated transactions with PayPal transactions. Appears in transaction and settlement reports.
network_transaction_reference
object
(
network_transaction
)
Reference values used by the card network to identify a transaction.
seller_protection
object
(
seller_protection
)
The level of protection offered as defined by
PayPal Seller Protection for Merchants
.
final_capture
boolean
Default:
false
Indicates whether you can make additional captures against the authorized payment. Set to
true
if you do not intend to capture additional payments against the authorization. Set to
false
if you intend to capture additional payments against the authorization.
seller_receivable_breakdown
object
(
Seller Receivable Breakdown
)
The detailed breakdown of the capture activity. This is not available for transactions that are in pending state.
disbursement_mode
string
(
disbursement_mode
)
Default:
"INSTANT"
The funds that are held on behalf of the merchant.
Enum Value
Description
INSTANT
The funds are released to the merchant immediately.
DELAYED
The funds are held for a finite number of days. The actual duration depends on the region and type of integration. You can release the funds through a referenced payout. Otherwise, the funds disbursed automatically after the specified duration.
links
Array of
objects
(
Link Description
)
[ 0 .. 32767 ] items
An array of related
HATEOAS links
.
processor_response
object
(
processor_response
)
The processor response information for payment requests, such as direct credit card transactions.
create_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
update_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
supplementary_data
object
(
Payment Supplementary Data
)
The supplementary data.
payee
object
(
payee_base
)
The details for the merchant who receives the funds and fulfills the order. The merchant is also known as the payee.
Copy
Expand all
Collapse all
{
"status"
:
"COMPLETED"
,
"status_details"
:
{
"reason"
:
"BUYER_COMPLAINT"
}
,
"id"
:
"string"
,
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"handling"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"tax_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"insurance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping_discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
}
,
"invoice_id"
:
"string"
,
"custom_id"
:
"string"
,
"network_transaction_reference"
:
{
"id"
:
"stringstr"
,
"date"
:
"stri"
,
"network"
:
"VISA"
,
"acquirer_reference_number"
:
"string"
}
,
"seller_protection"
:
{
"status"
:
"ELIGIBLE"
,
"dispute_categories"
:
[
"ITEM_NOT_RECEIVED"
]
}
,
"final_capture"
:
false
,
"seller_receivable_breakdown"
:
{
"gross_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"paypal_fee"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"paypal_fee_in_receivable_currency"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"net_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"receivable_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"exchange_rate"
:
{
"source_currency"
:
"string"
,
"target_currency"
:
"string"
,
"value"
:
"string"
}
,
"platform_fees"
:
[
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
]
}
,
"disbursement_mode"
:
"INSTANT"
,
"links"
:
[
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
]
,
"processor_response"
:
{
"avs_code"
:
"A"
,
"cvv_code"
:
"E"
,
"response_code"
:
"0000"
,
"payment_advice_code"
:
"01"
}
,
"create_time"
:
"string"
,
"update_time"
:
"string"
,
"supplementary_data"
:
{
"related_ids"
:
{
"order_id"
:
"string"
,
"authorization_id"
:
"string"
,
"capture_id"
:
"string"
}
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
Card Vendor
Configuration for a specific card vendor or network.
network
required
string
(
card_brand-2
)
The card brand.
Enum Value
Description
AMEX
The American Express payment network.
CB_NATIONALE
Carte Bleue Nationale (CBN), a major debit card payment system operating in France.
CETELEM
Cetelem, a brand of BNP Paribas Personal Finance, is a French financial institution specializing in financing individuals consumer credit activities.
COFIDIS
Cofidis is a French company, now majority owned by the Crédit Mutuel, based in Villeneuve-d'Ascq, that offers a payment method that allows you to make bank card payments in 3 or 4 times, PayPal payment in 4 times, or one Euro consumer credit.
COFINOGA
Cofinoga, a brand of BNP Paribas Personal Finance, is a credit specialist in France. It offers a card that allows you to pay for credit online purchases.
CHINA_UNION_PAY
China UnionPay (CUP) or UnionPay International (UPI) is a Chinese financial services corporation headquartered in Shanghai, China. It provides bank card services and a major card scheme in mainland China.
DELTA
The Delta Air Lines online payment network.
DISCOVER
The Discover Financial Services (DFS) banking and payment services capability network.
ELECTRON
The Visa Electron debit card payment network. It's offered by issuing banks in every country with the exception of Canada, Australia, Argentina, Ireland, and the United States.
ELO
The Brazilian Elo card payment network.
HIPER
The Hiper - Ingenico ePayment network.
HIPERCARD
The Brazilian Hipercard payment network that's widely accepted in the retail market.
JCB
The Japan Credit Bureau (JCB) card payment network.
MAESTRO
The Maestro debit card payment network owned by Mastercard.
MASTER_CARD
The Mastercard Incorporated payment network.
SOLO
The Hatton National BankFinance's SOLO digital wallet payment network.
STAR
The STAR payment network.
SWITCH
The Switch payment network.
VISA
The Visa Inc. payment network.
GE
The GE Credit Union 3Point card payment network.
RUPAY
The RuPay payment network.
SYNCHRONY
The Synchrony Financial (SYF) payment network.
DINERS
The Diners Club International banking and payment services capability network owned by Discover Financial Services (DFS), one of the most recognized brands in US financial services.
GIROCARD
Girocard is an interbank network and debit card service connecting virtually all German ATMs and banks.
CARNET
Carnet is a fuel card.
V_PAY
V Pay is a Single Euro Payments Area (SEPA) debit card for use in Europe, issued by Visa Europe.
eligible
required
boolean
Indicates if the vendor is eligible.
can_be_vaulted
required
boolean
Indicates if the vendor's payment method can be saved for future use.
branded
required
boolean
Indicates if the vendor has branded customization.
Copy
{
"network"
:
"AMEX"
,
"eligible"
:
true
,
"can_be_vaulted"
:
true
,
"branded"
:
true
}
card_brand
The card network or brand. Applies to credit, debit, gift, and payment cards.
string
(
card_brand
)
The card network or brand. Applies to credit, debit, gift, and payment cards.
Enum Value
Description
VISA
Visa card.
MASTERCARD
Mastercard card.
DISCOVER
Discover card.
AMEX
American Express card.
SOLO
Solo debit card.
JCB
Japan Credit Bureau card.
STAR
Military Star card.
DELTA
Delta Airlines card.
SWITCH
Switch credit card.
MAESTRO
Maestro credit card.
CB_NATIONALE
Carte Bancaire (CB) credit card.
CONFIGOGA
Configoga credit card.
CONFIDIS
Confidis credit card.
ELECTRON
Visa Electron credit card.
CETELEM
Cetelem credit card.
CHINA_UNION_PAY
China union pay credit card.
DINERS
The Diners Club International banking and payment services capability network owned by Discover Financial Services (DFS), one of the most recognized brands in US financial services.
ELO
The Brazilian Elo card payment network.
HIPER
The Hiper - Ingenico ePayment network.
HIPERCARD
The Brazilian Hipercard payment network that's widely accepted in the retail market.
RUPAY
The RuPay payment network.
GE
The GE Credit Union 3Point card payment network.
SYNCHRONY
The Synchrony Financial (SYF) payment network.
EFTPOS
The Electronic Fund Transfer At Point of Sale(EFTPOS) Debit card payment network.
CARTE_BANCAIRE
The Carte Bancaire payment network.
STAR_ACCESS
The Star Access payment network.
PULSE
The Pulse payment network.
NYCE
The NYCE payment network.
ACCEL
The Accel payment network.
UNKNOWN
UNKNOWN payment network.
Copy
"VISA"
card_brand-2
The card brand.
string
(
card_brand-2
)
The card brand.
Enum Value
Description
AMEX
The American Express payment network.
CB_NATIONALE
Carte Bleue Nationale (CBN), a major debit card payment system operating in France.
CETELEM
Cetelem, a brand of BNP Paribas Personal Finance, is a French financial institution specializing in financing individuals consumer credit activities.
COFIDIS
Cofidis is a French company, now majority owned by the Crédit Mutuel, based in Villeneuve-d'Ascq, that offers a payment method that allows you to make bank card payments in 3 or 4 times, PayPal payment in 4 times, or one Euro consumer credit.
COFINOGA
Cofinoga, a brand of BNP Paribas Personal Finance, is a credit specialist in France. It offers a card that allows you to pay for credit online purchases.
CHINA_UNION_PAY
China UnionPay (CUP) or UnionPay International (UPI) is a Chinese financial services corporation headquartered in Shanghai, China. It provides bank card services and a major card scheme in mainland China.
DELTA
The Delta Air Lines online payment network.
DISCOVER
The Discover Financial Services (DFS) banking and payment services capability network.
ELECTRON
The Visa Electron debit card payment network. It's offered by issuing banks in every country with the exception of Canada, Australia, Argentina, Ireland, and the United States.
ELO
The Brazilian Elo card payment network.
HIPER
The Hiper - Ingenico ePayment network.
HIPERCARD
The Brazilian Hipercard payment network that's widely accepted in the retail market.
JCB
The Japan Credit Bureau (JCB) card payment network.
MAESTRO
The Maestro debit card payment network owned by Mastercard.
MASTER_CARD
The Mastercard Incorporated payment network.
SOLO
The Hatton National BankFinance's SOLO digital wallet payment network.
STAR
The STAR payment network.
SWITCH
The Switch payment network.
VISA
The Visa Inc. payment network.
GE
The GE Credit Union 3Point card payment network.
RUPAY
The RuPay payment network.
SYNCHRONY
The Synchrony Financial (SYF) payment network.
DINERS
The Diners Club International banking and payment services capability network owned by Discover Financial Services (DFS), one of the most recognized brands in US financial services.
GIROCARD
Girocard is an interbank network and debit card service connecting virtually all German ATMs and banks.
CARNET
Carnet is a fuel card.
V_PAY
V Pay is a Single Euro Payments Area (SEPA) debit card for use in Europe, issued by Visa Europe.
Copy
"AMEX"
Common response fields
Common response fields for all payment methods.
can_be_vaulted
boolean
Default:
false
Indicates if the payment method can be vaulted or not. A true value indicates the payment method can be vaulted using our vaults product. If false, vaulting is not currently supported for this payment method.
country_code
string
(
country_code-2
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
product_code
string
(
Credit Button Eligibility Button Code
)
The button code corresponding to a particular product or set of products. The values followed are defined by the SDK team.
Enum Value
Description
CREDIT
Open ended credit products.
PAYLATER
Pay Later suite of products.
PAY_IN_3
Pay In 3 suite of products.
PAY_IN_4
Pay In 4 suite of products.
Copy
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
country_code-2
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
string
(
country_code-2
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
Copy
"st"
Credit Button Eligibility Button Code
The button code corresponding to a particular product or set of products. The values followed are defined by the SDK team.
string
(
Credit Button Eligibility Button Code
)
The button code corresponding to a particular product or set of products. The values followed are defined by the SDK team.
Enum Value
Description
CREDIT
Open ended credit products.
PAYLATER
Pay Later suite of products.
PAY_IN_3
Pay In 3 suite of products.
PAY_IN_4
Pay In 4 suite of products.
Copy
"CREDIT"
currency_code
The
three-character ISO-4217 currency code
that identifies the currency.
string
(
currency_code
)
= 3 characters
^[\S\s]*$
The
three-character ISO-4217 currency code
that identifies the currency.
Copy
"str"
Customer
Customer who is making a purchase from the merchant/partner.
country_code
string
(
country_code-2
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
channel
object
(
Customer Channel
)
Channel through which the request is being posted.
email
string
(
email_address
)
[ 3 .. 254 ] characters
^(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za...
Show pattern
The internationalized email address.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
phone
object
(
Phone
)
The phone number in its canonical international
E.164 numbering plan format
.
Copy
Expand all
Collapse all
{
"country_code"
:
"string"
,
"channel"
:
{
"browser_type"
:
"string"
,
"client_os"
:
"string"
,
"device_type"
:
"string"
}
,
"email"
:
"string"
,
"phone"
:
{
"country_code"
:
"str"
,
"national_number"
:
"string"
,
"extension_number"
:
"string"
}
}
Customer Channel
Channel through which the request is being posted.
browser_type
string
[ 1 .. 30 ] characters
^[0-9a-zA-Z_,. -]+$
The browser used by the customer. Example: Safari, Chrome, etc.
client_os
string
[ 1 .. 30 ] characters
^[0-9a-zA-Z_,. -]+$
The operating system on the device used by the customer. Example: iOS 16.5, Android 30, etc.
device_type
string
[ 1 .. 30 ] characters
^[0-9a-zA-Z_,. -]+$
The type of device used by the customer. Example: Mobile, Desktop, Tablet, etc.
Copy
{
"browser_type"
:
"string"
,
"client_os"
:
"string"
,
"device_type"
:
"string"
}
date_time
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
Copy
"stringstringstringst"
disbursement_mode
The funds that are held on behalf of the merchant.
string
(
disbursement_mode
)
Default:
"INSTANT"
The funds that are held on behalf of the merchant.
Enum Value
Description
INSTANT
The funds are released to the merchant immediately.
DELAYED
The funds are held for a finite number of days. The actual duration depends on the region and type of integration. You can release the funds through a referenced payout. Otherwise, the funds disbursed automatically after the specified duration.
Copy
"INSTANT"
discount_with_breakdown
The discount amount and currency code. For list of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
currency_code
required
string
(
currency_code
)
= 3 characters
^[\S\s]*$
The
three-character ISO-4217 currency code
that identifies the currency.
value
required
string
[ 0 .. 32 ] characters
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The value, which might be:
An integer for currencies like
JPY
that are not typically fractional.
A decimal fraction for currencies like
TND
that are subdivided into thousandths.
For the required number of decimal places for a currency code, see
Currency Codes
.
Copy
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
Eligibility Response for ApplePay
Response for ApplePay.
can_be_vaulted
boolean
Default:
false
Indicates if the payment method can be vaulted or not. A true value indicates the payment method can be vaulted using our vaults product. If false, vaulting is not currently supported for this payment method.
country_code
string
(
country_code-2
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
product_code
string
(
Credit Button Eligibility Button Code
)
The button code corresponding to a particular product or set of products. The values followed are defined by the SDK team.
Enum Value
Description
CREDIT
Open ended credit products.
PAYLATER
Pay Later suite of products.
PAY_IN_3
Pay In 3 suite of products.
PAY_IN_4
Pay In 4 suite of products.
config
object
(
Apple Pay Config
)
Configuration details for Apple Pay payment method.
Copy
Expand all
Collapse all
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"config"
:
{
"eligible"
:
true
,
"merchant_country"
:
"string"
,
"supported_networks"
:
[
"MASTERCARD"
]
,
"merchant_capabilities"
:
[
"SUPPORTS_CREDIT"
]
,
"token_notification_url"
:
"
http://example.com
"
}
}
Eligibility Response for GooglePay
Response for GooglePay.
can_be_vaulted
boolean
Default:
false
Indicates if the payment method can be vaulted or not. A true value indicates the payment method can be vaulted using our vaults product. If false, vaulting is not currently supported for this payment method.
country_code
string
(
country_code-2
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
product_code
string
(
Credit Button Eligibility Button Code
)
The button code corresponding to a particular product or set of products. The values followed are defined by the SDK team.
Enum Value
Description
CREDIT
Open ended credit products.
PAYLATER
Pay Later suite of products.
PAY_IN_3
Pay In 3 suite of products.
PAY_IN_4
Pay In 4 suite of products.
config
object
(
Google Pay Config
)
Configuration details for Google Pay payment method.
Copy
Expand all
Collapse all
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"config"
:
{
"eligible"
:
true
,
"merchant_country"
:
"string"
,
"api_version"
:
1
,
"api_version_minor"
:
1
,
"allowed_payment_methods"
:
[
{
"type"
:
"CARD"
,
"parameters"
:
{
"allowed_auth_methods"
:
[
"PAN_ONLY"
]
,
"supported_networks"
:
[
"MASTERCARD"
]
,
"billing_address_required"
:
true
,
"assurance_details_required"
:
true
,
"billing_address_parameters"
:
{
"format"
:
"FULL"
}
}
,
"tokenization_specification"
:
{
"type"
:
"PAYMENT_GATEWAY"
,
"parameters"
:
{
"gateway"
:
"string"
,
"gateway_merchant_id"
:
"string"
}
}
}
]
,
"merchant_info"
:
{
"merchant_origin"
:
"string"
,
"merchant_id"
:
"string"
,
"googlepay_partner_domain_verification_jwt"
:
"stringstri"
}
}
}
eligibility_purchase_unit_request
Purchase unit for payment eligibility.
amount
object
(
amount_with_breakdown
)
The total order amount with an optional breakdown that provides details, such as the total item amount, total tax amount, shipping, handling, insurance, and discounts, if any.
If you specify
amount.breakdown
, the amount equals
item_total
plus
tax_total
plus
shipping
plus
handling
plus
insurance
minus
shipping_discount
minus discount.
The amount must be a positive number. For listed of supported currencies and decimal precision, see the PayPal REST APIs
Currency Codes
.
payee
object
(
payee
)
The merchant who receives the funds and fulfills the order. The merchant is also known as the payee.
Copy
Expand all
Collapse all
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"handling"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"tax_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"insurance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping_discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
email
The internationalized email address.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
string
(
email
)
[ 3 .. 254 ] characters
^.*(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-...
Show pattern
The internationalized email address.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
Copy
"string"
email_address
The internationalized email address.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
string
(
email_address
)
[ 3 .. 254 ] characters
^(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za...
Show pattern
The internationalized email address.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
Copy
"string"
Error
The error details.
name
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The human-readable, unique name of the error.
message
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The message that describes the error.
debug_id
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal internal ID. Used for correlation purposes.
details
Array of
objects
(
Error Details
)
[ 0 .. 32767 ] items
An array of additional details about the error.
links
Array of
objects
(
Link Description
)
[ 0 .. 32767 ] items
An array of request-related
HATEOAS links
.
Copy
Expand all
Collapse all
{
"name"
:
"string"
,
"message"
:
"string"
,
"debug_id"
:
"string"
,
"details"
:
[
{
"field"
:
"string"
,
"value"
:
"string"
,
"location"
:
"body"
,
"issue"
:
"string"
,
"links"
:
[
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
]
,
"description"
:
"string"
}
]
,
"links"
:
[
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
]
}
Error Details
The error details. Required for client-side
4XX
errors.
field
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The field that caused the error. If this field is in the body, set this value to the field's JSON pointer value. Required for client-side errors.
value
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The value of the field that caused the error.
location
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
Default:
"body"
The location of the field that caused the error. Value is
body
,
path
, or
query
.
issue
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The unique, fine-grained application-level error code.
links
Array of
objects
(
Link Description
)
[ 1 .. 4 ] items
An array of request-related
HATEOAS links
that are either relevant to the issue by providing additional information or offering potential resolutions.
description
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The human-readable description for an issue. The description can change over the lifetime of an API, so clients must not depend on this value.
Copy
Expand all
Collapse all
{
"field"
:
"string"
,
"value"
:
"string"
,
"location"
:
"body"
,
"issue"
:
"string"
,
"links"
:
[
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
]
,
"description"
:
"string"
}
exchange_rate
The exchange rate that determines the amount to convert from one currency to another currency.
source_currency
string
(
currency_code
)
= 3 characters
^[\S\s]*$
The
three-character ISO-4217 currency code
that identifies the currency.
target_currency
string
(
currency_code
)
= 3 characters
^[\S\s]*$
The
three-character ISO-4217 currency code
that identifies the currency.
value
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The target currency amount. Equivalent to one unit of the source currency. Formatted as integer or decimal value with one to 15 digits to the right of the decimal point.
Copy
{
"source_currency"
:
"string"
,
"target_currency"
:
"string"
,
"value"
:
"string"
}
Find Eligible Payment Methods Request
Request to get list of eligible payment methods.
customer
object
(
Customer
)
Customer who is making a purchase from the merchant/partner.
purchase_units
Array of
objects
(
eligibility_purchase_unit_request
)
[ 1 .. 10 ] items
Array of purchase units.
preferences
object
(
Preferences
)
Preferences of merchant/partner consuming the API.
Copy
Expand all
Collapse all
{
"customer"
:
{
"country_code"
:
"string"
,
"channel"
:
{
"browser_type"
:
"string"
,
"client_os"
:
"string"
,
"device_type"
:
"string"
}
,
"email"
:
"string"
,
"phone"
:
{
"country_code"
:
"str"
,
"national_number"
:
"string"
,
"extension_number"
:
"string"
}
}
,
"purchase_units"
:
[
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"handling"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"tax_total"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"insurance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"shipping_discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"discount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
]
,
"preferences"
:
{
"payment_flow"
:
"ONE_TIME_PAYMENT"
,
"intent"
:
"CAPTURE"
,
"include_account_details"
:
"false"
,
"include_vault_tokens"
:
"false"
,
"vault"
:
"false"
,
"payment_source_constraint"
:
{
"constraint_type"
:
"INCLUDE"
,
"payment_sources"
:
[
"PAYPAL"
]
}
}
}
Google Pay Config
Configuration details for Google Pay payment method.
eligible
boolean
Indicates if Google Pay is eligible.
merchant_country
string
(
country_code-2
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
api_version
integer
[ 1 .. 10 ]
Google Pay API version.
api_version_minor
integer
[ 1 .. 10 ]
Google Pay API minor version.
allowed_payment_methods
Array of
objects
(
Payment Method
)
[ 1 .. 10 ] items
Allowed payment methods for Google Pay.
merchant_info
object
(
Merchant Information
)
Merchant-specific information required for Google Pay integration.
Copy
Expand all
Collapse all
{
"eligible"
:
true
,
"merchant_country"
:
"string"
,
"api_version"
:
1
,
"api_version_minor"
:
1
,
"allowed_payment_methods"
:
[
{
"type"
:
"CARD"
,
"parameters"
:
{
"allowed_auth_methods"
:
[
"PAN_ONLY"
]
,
"supported_networks"
:
[
"MASTERCARD"
]
,
"billing_address_required"
:
true
,
"assurance_details_required"
:
true
,
"billing_address_parameters"
:
{
"format"
:
"FULL"
}
}
,
"tokenization_specification"
:
{
"type"
:
"PAYMENT_GATEWAY"
,
"parameters"
:
{
"gateway"
:
"string"
,
"gateway_merchant_id"
:
"string"
}
}
}
]
,
"merchant_info"
:
{
"merchant_origin"
:
"string"
,
"merchant_id"
:
"string"
,
"googlepay_partner_domain_verification_jwt"
:
"stringstri"
}
}
GUID
A Globally Unique Identifier (GUID) value.
string
(
GUID
)
[ 1 .. 68 ] characters
^[A-Za-z0-9-{}(),]*$
A Globally Unique Identifier (GUID) value.
Copy
"string"
Link Description
The request-related
HATEOAS link
information.
href
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The complete target URL. To make the related call, combine the method with this
URI Template-formatted
link. For pre-processing, include the
$
,
(
, and
)
characters. The
href
is the key HATEOAS component that links a completed call with a subsequent call.
rel
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The
link relation type
, which serves as an ID for a link that unambiguously describes the semantics of the link. See
Link Relations
.
method
string
The HTTP method required to make the related call.
Enum Value
Description
GET
The HTTP GET method.
POST
The HTTP POST method.
PUT
The HTTP PUT method.
DELETE
The HTTP DELETE method.
HEAD
The HTTP HEAD method.
CONNECT
The HTTP CONNECT method.
OPTIONS
The HTTP OPTIONS method.
PATCH
The HTTP PATCH method.
title
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The link title.
mediaType
string
(
media_type
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The media type, as defined by
RFC 2046
. Describes the link target.
encType
string
(
enc_type
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
Default:
"application/json"
The media type in which to submit the request data.
schema
object
(
Link Schema
)
The request data or link target.
targetSchema
object
(
Link Schema
)
The request data or link target.
Copy
Expand all
Collapse all
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
Link Description
The request-related
HATEOAS link
information.
href
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The complete target URL. To make the related call, combine the method with this
URI Template-formatted
link. For pre-processing, include the
$
,
(
, and
)
characters. The
href
is the key HATEOAS component that links a completed call with a subsequent call.
rel
required
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The
link relation type
, which serves as an ID for a link that unambiguously describes the semantics of the link. See
Link Relations
.
method
string
The HTTP method required to make the related call.
Enum Value
Description
GET
The HTTP GET method.
POST
The HTTP POST method.
PUT
The HTTP PUT method.
DELETE
The HTTP DELETE method.
HEAD
The HTTP HEAD method.
CONNECT
The HTTP CONNECT method.
OPTIONS
The HTTP OPTIONS method.
PATCH
The HTTP PATCH method.
title
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The link title.
mediaType
string
(
media_type
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The media type, as defined by
RFC 2046
. Describes the link target.
encType
string
(
enc_type
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
Default:
"application/json"
The media type in which to submit the request data.
schema
object
(
Link Schema
)
The request data or link target.
targetSchema
object
(
Link Schema
)
The request data or link target.
Copy
Expand all
Collapse all
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
Link Schema
The request data or link target.
additionalItems
object
(
additional_items
)
Any additional items.
dependencies
object
(
Dependencies
)
The dependencies.
items
object
(
Items
)
An item.
definitions
object
(
Definitions
)
Definitions.
patternProperties
object
(
pattern_properties
)
The pattern properties.
properties
object
(
Properties
)
The properties.
allOf
Array of
objects
(
all_of
)
[ 0 .. 32767 ] items
An array of sub-schemas. The data must validate against all sub-schemas.
anyOf
Array of
objects
(
any_of
)
[ 0 .. 32767 ] items
An array of sub-schemas. The data must validate against one or more sub-schemas.
oneOf
Array of
objects
(
one_of
)
[ 0 .. 32767 ] items
An array of sub-schemas. The data must validate against one sub-schema.
not
object
(
Not
)
Not.
links
Array of
objects
(
link
)
[ 0 .. 32767 ] items
An array of links.
fragmentResolution
string
(
fragment_resolution
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The fragment resolution.
media
object
(
Media
)
The media type and context-encoding scheme.
pathStart
string
<
uri
>
(
path_start
)
[ 0 .. 2147483647 ] characters
To apply this schema to the instances' URIs, start the URIs with this value.
Copy
Expand all
Collapse all
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
Link Schema
The request data or link target.
additionalItems
object
(
additional_items
)
Any additional items.
dependencies
object
(
Dependencies
)
Any Dependencies.
items
object
(
Items
)
An item.
definitions
object
(
Definitions
)
Definitions.
patternProperties
object
(
pattern_properties
)
The pattern properties.
properties
object
(
Properties
)
Properties.
allOf
Array of
objects
(
all_of
)
[ 0 .. 32767 ] items
An array of sub-schemas. The data must validate against all sub-schemas.
anyOf
Array of
objects
(
any_of
)
[ 0 .. 32767 ] items
An array of sub-schemas. The data must validate against one or more sub-schemas.
oneOf
Array of
objects
(
one_of
)
[ 0 .. 32767 ] items
An array of sub-schemas. The data must validate against one sub-schema.
not
object
(
Not
)
Not.
links
Array of
objects
(
link
)
[ 0 .. 32767 ] items
An array of links.
fragmentResolution
string
(
fragment_resolution
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The fragment resolution.
media
object
(
Media
)
The media type and context-encoding scheme.
pathStart
string
<
uri
>
(
path_start
)
[ 0 .. 2147483647 ] characters
To apply this schema to the instances' URIs, start the URIs with this value.
Copy
Expand all
Collapse all
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
Merchant Information
Merchant-specific information required for Google Pay integration.
merchant_origin
string
[ 4 .. 253 ] characters
^[a-zA-Z0-9.-]+$
Merchant origin.
merchant_id
string
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The account identifier for a PayPal account.
googlepay_partner_domain_verification_jwt
string
[ 10 .. 2000 ] characters
^[A-Za-z0-9_.-]+$
JWT token used for Google Pay partner domain verification to authenticate the merchant's domain.
Copy
{
"merchant_origin"
:
"string"
,
"merchant_id"
:
"string"
,
"googlepay_partner_domain_verification_jwt"
:
"stringstri"
}
Money
The currency and amount for a financial transaction, such as a balance or payment due.
currency_code
required
string
(
currency_code
)
= 3 characters
^[\S\s]*$
The
three-character ISO-4217 currency code
that identifies the currency.
value
required
string
[ 0 .. 32 ] characters
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The value, which might be:
An integer for currencies like
JPY
that are not typically fractional.
A decimal fraction for currencies like
TND
that are subdivided into thousandths.
For the required number of decimal places for a currency code, see
Currency Codes
.
Copy
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
net_amount_breakdown
The net amount. Returned when the currency of the refund is different from the currency of the PayPal account where the merchant holds their funds.
payable_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
converted_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
exchange_rate
object
(
exchange_rate
)
The exchange rate that determines the amount to convert from one currency to another currency.
Copy
Expand all
Collapse all
{
"payable_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"converted_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"exchange_rate"
:
{
"source_currency"
:
"string"
,
"target_currency"
:
"string"
,
"value"
:
"string"
}
}
network_transaction
Reference values used by the card network to identify a transaction.
id
string
[ 9 .. 36 ] characters
^[a-zA-Z0-9-_@.:&+=*^'~#!$%()]+$
Transaction reference id returned by the scheme. For Visa and Amex, this is the "Tran id" field in response. For MasterCard, this is the "BankNet reference id" field in response. For Discover, this is the "NRID" field in response. The pattern we expect for this field from Visa/Amex/CB/Discover is numeric, Mastercard/BNPP is alphanumeric and Paysecure is alphanumeric with special character -.
date
string
= 4 characters
^[0-9]+$
The date that the transaction was authorized by the scheme. This field may not be returned for all networks. MasterCard refers to this field as "BankNet reference date". For some specific networks, such as MasterCard and Discover, this date field is mandatory when the
previous_network_transaction_reference_id
is passed.
network
string
(
card_brand
)
The card network or brand. Applies to credit, debit, gift, and payment cards.
Enum Value
Description
VISA
Visa card.
MASTERCARD
Mastercard card.
DISCOVER
Discover card.
AMEX
American Express card.
SOLO
Solo debit card.
JCB
Japan Credit Bureau card.
STAR
Military Star card.
DELTA
Delta Airlines card.
SWITCH
Switch credit card.
MAESTRO
Maestro credit card.
CB_NATIONALE
Carte Bancaire (CB) credit card.
CONFIGOGA
Configoga credit card.
CONFIDIS
Confidis credit card.
ELECTRON
Visa Electron credit card.
CETELEM
Cetelem credit card.
CHINA_UNION_PAY
China union pay credit card.
DINERS
The Diners Club International banking and payment services capability network owned by Discover Financial Services (DFS), one of the most recognized brands in US financial services.
ELO
The Brazilian Elo card payment network.
HIPER
The Hiper - Ingenico ePayment network.
HIPERCARD
The Brazilian Hipercard payment network that's widely accepted in the retail market.
RUPAY
The RuPay payment network.
GE
The GE Credit Union 3Point card payment network.
SYNCHRONY
The Synchrony Financial (SYF) payment network.
EFTPOS
The Electronic Fund Transfer At Point of Sale(EFTPOS) Debit card payment network.
CARTE_BANCAIRE
The Carte Bancaire payment network.
STAR_ACCESS
The Star Access payment network.
PULSE
The Pulse payment network.
NYCE
The NYCE payment network.
ACCEL
The Accel payment network.
UNKNOWN
UNKNOWN payment network.
acquirer_reference_number
string
[ 1 .. 36 ] characters
^[a-zA-Z0-9]+$
Reference ID issued for the card transaction. This ID can be used to track the transaction across processors, card brands and issuing banks.
Copy
{
"id"
:
"stringstr"
,
"date"
:
"stri"
,
"network"
:
"VISA"
,
"acquirer_reference_number"
:
"string"
}
payee
The merchant who receives the funds and fulfills the order. The merchant is also known as the payee.
email_address
string
(
email
)
[ 3 .. 254 ] characters
^.*(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-...
Show pattern
The internationalized email address.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
merchant_id
string
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The account identifier for a PayPal account.
Copy
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
payee_base
The details for the merchant who receives the funds and fulfills the order. The merchant is also known as the payee.
email_address
string
(
email
)
[ 3 .. 254 ] characters
^.*(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-...
Show pattern
The internationalized email address.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
merchant_id
string
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The account identifier for a PayPal account.
Copy
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
Payment Method
Configuration for a specific payment method supported by Google Pay.
type
string
Type of payment method.
Value
Description
CARD
Card payment method.
parameters
object
(
Payment Method Parameters
)
Parameters specific to the payment method configuration.
tokenization_specification
object
(
Tokenization Specification
)
Specification for payment method tokenization in Google Pay.
Copy
Expand all
Collapse all
{
"type"
:
"CARD"
,
"parameters"
:
{
"allowed_auth_methods"
:
[
"PAN_ONLY"
]
,
"supported_networks"
:
[
"MASTERCARD"
]
,
"billing_address_required"
:
true
,
"assurance_details_required"
:
true
,
"billing_address_parameters"
:
{
"format"
:
"FULL"
}
}
,
"tokenization_specification"
:
{
"type"
:
"PAYMENT_GATEWAY"
,
"parameters"
:
{
"gateway"
:
"string"
,
"gateway_merchant_id"
:
"string"
}
}
}
Payment Method Parameters
Parameters specific to the payment method configuration.
allowed_auth_methods
Array of
strings
[ 1 .. 100 ] items
Allowed authentication methods.
Items
Enum Value
Description
PAN_ONLY
Authentication method using only the primary account number.
CRYPTOGRAM_3DS
Authentication method using 3DS cryptogram.
supported_networks
Array of
strings
[ 1 .. 100 ] items
Allowed card networks.
Items
Enum Value
Description
MASTERCARD
MasterCard network.
DISCOVER
Discover network.
VISA
Visa network.
AMEX
American Express network.
billing_address_required
boolean
Whether billing address is required.
assurance_details_required
boolean
Whether assurance details are required.
billing_address_parameters
object
(
Billing Address Parameters
)
Configuration parameters for billing address collection in Google Pay.
Copy
Expand all
Collapse all
{
"allowed_auth_methods"
:
[
"PAN_ONLY"
]
,
"supported_networks"
:
[
"MASTERCARD"
]
,
"billing_address_required"
:
true
,
"assurance_details_required"
:
true
,
"billing_address_parameters"
:
{
"format"
:
"FULL"
}
}
Payment Methods
List of payment methods.
paypal
object
(
Response for PayPal
)
Response for PayPal.
venmo
object
(
Response for Venmo
)
Response for Venmo.
paypal_credit
object
(
Common response fields
)
Common response fields for all payment methods.
paypal_pay_later
object
(
Common response fields
)
Common response fields for all payment methods.
ideal
object
(
Common response fields
)
Common response fields for all payment methods.
apple_pay
object
(
Eligibility Response for ApplePay
)
Response for ApplePay.
google_pay
object
(
Eligibility Response for GooglePay
)
Response for GooglePay.
advanced_cards
object
(
Advanced Cards Config
)
Configuration details for advanced card payment methods including credit and debit card processing capabilities.
basic_cards
object
(
Basic Cards Config
)
Configuration details for basic card payment methods including credit and debit card processing capabilities.
ach
object
(
Response for ACH
)
Response for ACH payment method.
blik
object
(
Common response fields
)
Common response fields for all payment methods.
p24
object
(
Common response fields
)
Common response fields for all payment methods.
eps
object
(
Common response fields
)
Common response fields for all payment methods.
bancontact
object
(
Common response fields
)
Common response fields for all payment methods.
swish
object
(
Common response fields
)
Common response fields for all payment methods.
klarna
object
(
Common response fields
)
Common response fields for all payment methods.
mbway
object
(
Common response fields
)
Common response fields for all payment methods.
boletobancario
object
(
Common response fields
)
Common response fields for all payment methods.
twint
object
(
Common response fields
)
Common response fields for all payment methods.
bizum
object
(
Common response fields
)
Common response fields for all payment methods.
afterpay
object
(
Common response fields
)
Common response fields for all payment methods.
zip
object
(
Common response fields
)
Common response fields for all payment methods.
satispay
object
(
Common response fields
)
Common response fields for all payment methods.
trustly
object
(
Common response fields
)
Common response fields for all payment methods.
mybank
object
(
Common response fields
)
Common response fields for all payment methods.
alipay
object
(
Common response fields
)
Common response fields for all payment methods.
wechatpay
object
(
Common response fields
)
Common response fields for all payment methods.
grabpay
object
(
Common response fields
)
Common response fields for all payment methods.
oxxo_pay
object
(
Common response fields
)
Common response fields for all payment methods.
multibanco
object
(
Common response fields
)
Common response fields for all payment methods.
verkkopankki
object
(
Common response fields
)
Common response fields for all payment methods.
bancomatpay
object
(
Common response fields
)
Common response fields for all payment methods.
payu
object
(
Common response fields
)
Common response fields for all payment methods.
blik_pay_later
object
(
Common response fields
)
Common response fields for all payment methods.
floa_pay
object
(
Common response fields
)
Common response fields for all payment methods.
dragonpay
object
(
Common response fields
)
Common response fields for all payment methods.
paysera
object
(
Common response fields
)
Common response fields for all payment methods.
lithuania_banks
object
(
Common response fields
)
Common response fields for all payment methods.
latvia_banks
object
(
Common response fields
)
Common response fields for all payment methods.
thailand_banks
object
(
Common response fields
)
Common response fields for all payment methods.
estonia_banks
object
(
Common response fields
)
Common response fields for all payment methods.
alfamart
object
(
Common response fields
)
Common response fields for all payment methods.
doku
object
(
Common response fields
)
Common response fields for all payment methods.
indonesia_banks
object
(
Common response fields
)
Common response fields for all payment methods.
indomaret
object
(
Common response fields
)
Common response fields for all payment methods.
jenius_pay
object
(
Common response fields
)
Common response fields for all payment methods.
kredivo
object
(
Common response fields
)
Common response fields for all payment methods.
linkaja
object
(
Common response fields
)
Common response fields for all payment methods.
ovo
object
(
Common response fields
)
Common response fields for all payment methods.
paysafecard
object
(
Common response fields
)
Common response fields for all payment methods.
skrill
object
(
Common response fields
)
Common response fields for all payment methods.
wero
object
(
Common response fields
)
Common response fields for all payment methods.
fiuu_cash
object
(
Common response fields
)
Common response fields for all payment methods.
gopay
object
(
Common response fields
)
Common response fields for all payment methods.
fpx
object
(
Common response fields
)
Common response fields for all payment methods.
pay_upon_invoice
object
(
Common response fields
)
Common response fields for all payment methods.
pix_international
object
(
Common response fields
)
Common response fields for all payment methods.
scalapay
object
(
Common response fields
)
Common response fields for all payment methods.
crypto
object
(
Common response fields
)
Common response fields for all payment methods.
Copy
Expand all
Collapse all
{
"paypal"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"eligible_in_paypal_network"
:
true
,
"recommended"
:
"false"
,
"recommended_priority"
:
1
}
,
"venmo"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"eligible_in_paypal_network"
:
true
,
"recommended"
:
"false"
,
"recommended_priority"
:
1
}
,
"paypal_credit"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"paypal_pay_later"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"ideal"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"apple_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"config"
:
{
"eligible"
:
true
,
"merchant_country"
:
"string"
,
"supported_networks"
:
[
"MASTERCARD"
]
,
"merchant_capabilities"
:
[
"SUPPORTS_CREDIT"
]
,
"token_notification_url"
:
"
http://example.com
"
}
}
,
"google_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"config"
:
{
"eligible"
:
true
,
"merchant_country"
:
"string"
,
"api_version"
:
1
,
"api_version_minor"
:
1
,
"allowed_payment_methods"
:
[
{
"type"
:
"CARD"
,
"parameters"
:
{
"allowed_auth_methods"
:
[
"PAN_ONLY"
]
,
"supported_networks"
:
[
"MASTERCARD"
]
,
"billing_address_required"
:
true
,
"assurance_details_required"
:
true
,
"billing_address_parameters"
:
{
"format"
:
"FULL"
}
}
,
"tokenization_specification"
:
{
"type"
:
"PAYMENT_GATEWAY"
,
"parameters"
:
{
"gateway"
:
"string"
,
"gateway_merchant_id"
:
"string"
}
}
}
]
,
"merchant_info"
:
{
"merchant_origin"
:
"string"
,
"merchant_id"
:
"string"
,
"googlepay_partner_domain_verification_jwt"
:
"stringstri"
}
}
}
,
"advanced_cards"
:
{
"can_be_vaulted"
:
true
,
"supports_installments"
:
true
,
"vendors"
:
[
{
"network"
:
"AMEX"
,
"eligible"
:
true
,
"can_be_vaulted"
:
true
,
"branded"
:
true
}
]
}
,
"basic_cards"
:
{
"can_be_vaulted"
:
true
,
"supports_installments"
:
true
,
"guest_enabled"
:
true
,
"supports_inline_presentation_mode"
:
true
}
,
"ach"
:
{
"can_be_vaulted"
:
false
}
,
"blik"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"p24"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"eps"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"bancontact"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"swish"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"klarna"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"mbway"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"boletobancario"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"twint"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"bizum"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"afterpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"zip"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"satispay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"trustly"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"mybank"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"alipay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"wechatpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"grabpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"oxxo_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"multibanco"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"verkkopankki"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"bancomatpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"payu"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"blik_pay_later"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"floa_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"dragonpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"paysera"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"lithuania_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"latvia_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"thailand_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"estonia_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"alfamart"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"doku"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"indonesia_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"indomaret"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"jenius_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"kredivo"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"linkaja"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"ovo"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"paysafecard"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"skrill"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"wero"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"fiuu_cash"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"gopay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"fpx"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"pay_upon_invoice"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"pix_international"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"scalapay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"crypto"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
}
Payment Supplementary Data
The supplementary data.
related_ids
object
(
Related Identifiers
)
Identifiers related to a specific resource.
Copy
Expand all
Collapse all
{
"related_ids"
:
{
"order_id"
:
"string"
,
"authorization_id"
:
"string"
,
"capture_id"
:
"string"
}
}
payment_instruction
Any additional payment instructions to be consider during payment processing. This processing instruction is applicable for Capturing an order or Authorizing an Order.
platform_fees
Array of
objects
(
platform_fee
)
[ 0 .. 1 ] items
An array of various fees, commissions, tips, or donations. This field is only applicable to merchants that been enabled for PayPal Complete Payments Platform for Marketplaces and Platforms capability.
disbursement_mode
string
(
disbursement_mode
)
Default:
"INSTANT"
The funds that are held on behalf of the merchant.
Enum Value
Description
INSTANT
The funds are released to the merchant immediately.
DELAYED
The funds are held for a finite number of days. The actual duration depends on the region and type of integration. You can release the funds through a referenced payout. Otherwise, the funds disbursed automatically after the specified duration.
payee_pricing_tier_id
string
[ 1 .. 20 ] characters
^.*$
This field is only enabled for selected merchants/partners to use and provides the ability to trigger a specific pricing rate/plan for a payment transaction. The list of eligible 'payee_pricing_tier_id' would be provided to you by your Account Manager. Specifying values other than the one provided to you by your account manager would result in an error.
payee_receivable_fx_rate_id
string
[ 1 .. 4000 ] characters
^.*$
FX identifier generated returned by PayPal to be used for payment processing in order to honor FX rate (for eligible integrations) to be used when amount is settled/received into the payee account.
Copy
Expand all
Collapse all
{
"platform_fees"
:
[
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
]
,
"disbursement_mode"
:
"INSTANT"
,
"payee_pricing_tier_id"
:
"string"
,
"payee_receivable_fx_rate_id"
:
"string"
}
payment_instruction
Any additional payments instructions during refund payment processing. This object is only applicable to merchants that have been enabled for PayPal Commerce Platform for Marketplaces and Platforms capability. Please speak to your account manager if you want to use this capability.
platform_fees
Array of
objects
(
platform_fee
)
[ 0 .. 1 ] items
Specifies the amount that the API caller will contribute to the refund being processed. The amount needs to be lower than platform_fees amount originally captured or the amount that is remaining if multiple refunds have been processed. This field is only applicable to merchants that have been enabled for PayPal Commerce Platform for Marketplaces and Platforms capability. Please speak to your account manager if you want to use this capability.
Copy
Expand all
Collapse all
{
"platform_fees"
:
[
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
]
}
payment_method
Set of unique payment methods.
string
(
payment_method
)
Set of unique payment methods.
Enum Value
Description
PAYPAL
PAYPAL
VENMO
VENMO
PAYPAL_CREDIT
PAYPAL_CREDIT
PAYPAL_PAY_LATER
PAYPAL_PAY_LATER
ACH
ACH
Copy
"PAYPAL"
PayPal Account Identifier
The account identifier for a PayPal account.
string
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The account identifier for a PayPal account.
Copy
"stringstrings"
PayPal services member indicator
Flag that indicates if the customer is in the PayPal network. This value will be included in the response if the include_account_details flag is set to "true" in the API request.
boolean
(
PayPal services member indicator
)
Flag that indicates if the customer is in the PayPal network. This value will be included in the response if the include_account_details flag is set to "true" in the API request.
Copy
true
paypal_response
Eligible payment methods.
eligible_methods
object
(
Payment Methods
)
List of payment methods.
supplementary_data
object
(
Supplementary Data
)
Contains supplementary data related to the eligibility check.
Copy
Expand all
Collapse all
{
"eligible_methods"
:
{
"paypal"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"eligible_in_paypal_network"
:
true
,
"recommended"
:
"false"
,
"recommended_priority"
:
1
}
,
"venmo"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"eligible_in_paypal_network"
:
true
,
"recommended"
:
"false"
,
"recommended_priority"
:
1
}
,
"paypal_credit"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"paypal_pay_later"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"ideal"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"apple_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"config"
:
{
"eligible"
:
true
,
"merchant_country"
:
"string"
,
"supported_networks"
:
[
"MASTERCARD"
]
,
"merchant_capabilities"
:
[
"SUPPORTS_CREDIT"
]
,
"token_notification_url"
:
"
http://example.com
"
}
}
,
"google_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"config"
:
{
"eligible"
:
true
,
"merchant_country"
:
"string"
,
"api_version"
:
1
,
"api_version_minor"
:
1
,
"allowed_payment_methods"
:
[
{
"type"
:
"CARD"
,
"parameters"
:
{
"allowed_auth_methods"
:
[
null
]
,
"supported_networks"
:
[
null
]
,
"billing_address_required"
:
true
,
"assurance_details_required"
:
true
,
"billing_address_parameters"
:
{
"format"
:
null
}
}
,
"tokenization_specification"
:
{
"type"
:
"PAYMENT_GATEWAY"
,
"parameters"
:
{
"gateway"
:
null
,
"gateway_merchant_id"
:
null
}
}
}
]
,
"merchant_info"
:
{
"merchant_origin"
:
"string"
,
"merchant_id"
:
"string"
,
"googlepay_partner_domain_verification_jwt"
:
"stringstri"
}
}
}
,
"advanced_cards"
:
{
"can_be_vaulted"
:
true
,
"supports_installments"
:
true
,
"vendors"
:
[
{
"network"
:
"AMEX"
,
"eligible"
:
true
,
"can_be_vaulted"
:
true
,
"branded"
:
true
}
]
}
,
"basic_cards"
:
{
"can_be_vaulted"
:
true
,
"supports_installments"
:
true
,
"guest_enabled"
:
true
,
"supports_inline_presentation_mode"
:
true
}
,
"ach"
:
{
"can_be_vaulted"
:
false
}
,
"blik"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"p24"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"eps"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"bancontact"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"swish"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"klarna"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"mbway"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"boletobancario"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"twint"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"bizum"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"afterpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"zip"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"satispay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"trustly"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"mybank"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"alipay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"wechatpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"grabpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"oxxo_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"multibanco"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"verkkopankki"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"bancomatpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"payu"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"blik_pay_later"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"floa_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"dragonpay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"paysera"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"lithuania_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"latvia_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"thailand_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"estonia_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"alfamart"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"doku"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"indonesia_banks"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"indomaret"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"jenius_pay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"kredivo"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"linkaja"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"ovo"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"paysafecard"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"skrill"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"wero"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"fiuu_cash"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"gopay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"fpx"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"pay_upon_invoice"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"pix_international"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"scalapay"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
,
"crypto"
:
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
}
}
,
"supplementary_data"
:
{
"buyer_country_code"
:
"string"
}
}
Phone
The phone number in its canonical international
E.164 numbering plan format
.
country_code
required
string
(
country_calling_code
)
[ 1 .. 3 ] characters
^[0-9]{1,3}?$
The country calling code (CC), in its canonical international
E.164 numbering plan format
. The combined length of the CC and the national number must not be greater than 15 digits. The national number consists of a national destination code (NDC) and subscriber number (SN).
national_number
required
string
[ 1 .. 14 ] characters
^[0-9]{1,14}?$
The national number, in its canonical international
E.164 numbering plan format
. The combined length of the country calling code (CC) and the national number must not be greater than 15 digits. The national number consists of a national destination code (NDC) and subscriber number (SN).
extension_number
string
[ 1 .. 15 ] characters
^[0-9]{1,15}?$
The extension number.
Copy
{
"country_code"
:
"str"
,
"national_number"
:
"string"
,
"extension_number"
:
"string"
}
platform_fee
The platform or partner fee, commission, or brokerage fee that is associated with the transaction. Not a separate or isolated transaction leg from the external perspective. The platform fee is limited in scope and is always associated with the original payment for the purchase unit.
amount
required
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
payee
object
(
payee_base
)
The details for the merchant who receives the funds and fulfills the order. The merchant is also known as the payee.
Copy
Expand all
Collapse all
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
Preferences
Preferences of merchant/partner consuming the API.
payment_flow
string
(
Payment Flow
)
This field specifies the payment flow, expected to provide a hint about which payment action the customer is intending to perform.
Enum Value
Description
ONE_TIME_PAYMENT
Indicates that a customer is attempting to acquire a product within the context of a purchase. Most often, this will be the standard PayPal Checkout experience.
RECURRING_PAYMENT
Indicates that the customer is in the recurring payment experience.
VAULT_WITH_PAYMENT
Indicates that the customer is entering through checkout and continue to the vaulting experience.
VAULT_WITHOUT_PAYMENT
Indicates that the customer is in the vaulting experience without any purchase.
intent
string
The intent of the payment flow, specifying the purpose of the payment operation.
Enum Value
Description
CAPTURE
The intent to capture payment immediately after customer approval.
AUTHORIZE
The intent to authorize a payment for capture later.
ORDER
The intent to create an order for authorized payments that can be captured later in parts or in full.
TOKENIZE
The intent to tokenize payment details without processing a payment.
SUBSCRIPTION
The intent to process a payment as part of a subscription.
UNKNOWN
Used when the intent is not specified or does not match any known values.
include_account_details
boolean
Default:
"false"
If this value is set to true, response will include confirmation if the customer has PayPal and/or Venmo accounts if they are eligible payment methods. Value defaults to false.
include_vault_tokens
boolean
Default:
"false"
If this value is set to true, response will include vaulted token information if the eligible funding source has any instrument vaulted for the customer. Value defaults to false.
vault
boolean
Default:
"false"
This field determines whether the selected payment method is intended to be stored for future use (vaulted) or used as a one-time payment. Value defaults to false.
payment_source_constraint
object
(
Payment Source Constraint
)
Payment source constraint defines the payment methods that needs to be included/excluded for eligibility assessment. If not passed, all payment methods will be assessed for eligibility.
Copy
Expand all
Collapse all
{
"payment_flow"
:
"ONE_TIME_PAYMENT"
,
"intent"
:
"CAPTURE"
,
"include_account_details"
:
"false"
,
"include_vault_tokens"
:
"false"
,
"vault"
:
"false"
,
"payment_source_constraint"
:
{
"constraint_type"
:
"INCLUDE"
,
"payment_sources"
:
[
"PAYPAL"
]
}
}
processor_response
The processor response information for payment requests, such as direct credit card transactions.
avs_code
string
The address verification code for Visa, Discover, Mastercard, or American Express transactions.
Enum Value
Description
0
For Maestro, all address information matches.
1
For Maestro, none of the address information matches.
2
For Maestro, part of the address information matches.
3
For Maestro, the merchant did not provide AVS information. It was not processed.
4
For Maestro, the address was not checked or the acquirer had no response. The service is not available.
A
For Visa, Mastercard, or Discover transactions, the address matches but the zip code does not match. For American Express transactions, the card holder address is correct.
B
For Visa, Mastercard, or Discover transactions, the address matches. International A.
C
For Visa, Mastercard, or Discover transactions, no values match. International N.
D
For Visa, Mastercard, or Discover transactions, the address and postal code match. International X.
E
For Visa, Mastercard, or Discover transactions, not allowed for Internet or phone transactions. For American Express card holder, the name is incorrect but the address and postal code match.
F
For Visa, Mastercard, or Discover transactions, the address and postal code match. UK-specific X. For American Express card holder, the name is incorrect but the address matches.
G
For Visa, Mastercard, or Discover transactions, global is unavailable. Nothing matches.
I
For Visa, Mastercard, or Discover transactions, international is unavailable. Not applicable.
M
For Visa, Mastercard, or Discover transactions, the address and postal code match. For American Express card holder, the name, address, and postal code match.
N
For Visa, Mastercard, or Discover transactions, nothing matches. For American Express card holder, the address and postal code are both incorrect.
P
For Visa, Mastercard, or Discover transactions, postal international Z. Postal code only.
R
For Visa, Mastercard, or Discover transactions, re-try the request. For American Express, the system is unavailable.
S
For Visa, Mastercard, Discover, or American Express, the service is not supported.
U
For Visa, Mastercard, or Discover transactions, the service is unavailable. For American Express, information is not available. For Maestro, the address is not checked or the acquirer had no response. The service is not available.
W
For Visa, Mastercard, or Discover transactions, whole ZIP code. For American Express, the card holder name, address, and postal code are all incorrect.
X
For Visa, Mastercard, or Discover transactions, exact match of the address and the nine-digit ZIP code. For American Express, the card holder name, address, and postal code are all incorrect.
Y
For Visa, Mastercard, or Discover transactions, the address and five-digit ZIP code match. For American Express, the card holder address and postal code are both correct.
Z
For Visa, Mastercard, or Discover transactions, the five-digit ZIP code matches but no address. For American Express, only the card holder postal code is correct.
Null
For Maestro, no AVS response was obtained.
cvv_code
string
The card verification value code for for Visa, Discover, Mastercard, or American Express.
Enum Value
Description
0
For Maestro, the CVV2 matched.
1
For Maestro, the CVV2 did not match.
2
For Maestro, the merchant has not implemented CVV2 code handling.
3
For Maestro, the merchant has indicated that CVV2 is not present on card.
4
For Maestro, the service is not available.
E
For Visa, Mastercard, Discover, or American Express, error - unrecognized or unknown response.
I
For Visa, Mastercard, Discover, or American Express, invalid or null.
M
For Visa, Mastercard, Discover, or American Express, the CVV2/CSC matches.
N
For Visa, Mastercard, Discover, or American Express, the CVV2/CSC does not match.
P
For Visa, Mastercard, Discover, or American Express, it was not processed.
S
For Visa, Mastercard, Discover, or American Express, the service is not supported.
U
For Visa, Mastercard, Discover, or American Express, unknown - the issuer is not certified.
X
For Visa, Mastercard, Discover, or American Express, no response. For Maestro, the service is not available.
All others
For Visa, Mastercard, Discover, or American Express, error.
response_code
string
Processor response code for the non-PayPal payment processor errors.
Enum Value
Description
1000
PARTIAL_AUTHORIZATION.
1300
INVALID_DATA_FORMAT.
1310
INVALID_AMOUNT.
1312
INVALID_TRANSACTION_CARD_ISSUER_ACQUIRER.
1317
INVALID_CAPTURE_DATE.
1320
INVALID_CURRENCY_CODE.
1330
INVALID_ACCOUNT.
1335
INVALID_ACCOUNT_RECURRING.
1340
INVALID_TERMINAL.
1350
INVALID_MERCHANT.
1352
RESTRICTED_OR_INACTIVE_ACCOUNT.
1360
BAD_PROCESSING_CODE.
1370
INVALID_MCC.
1380
INVALID_EXPIRATION.
1382
INVALID_CARD_VERIFICATION_VALUE.
1384
INVALID_LIFE_CYCLE_OF_TRANSACTION.
1390
INVALID_ORDER.
1393
TRANSACTION_CANNOT_BE_COMPLETED.
5100
GENERIC_DECLINE.
5110
CVV2_FAILURE.
5120
INSUFFICIENT_FUNDS.
5130
INVALID_PIN.
5135
DECLINED_PIN_TRY_EXCEEDED.
5140
CARD_CLOSED.
5150
PICKUP_CARD_SPECIAL_CONDITIONS. Try using another card. Do not retry the same card.
5160
UNAUTHORIZED_USER.
5170
AVS_FAILURE.
5180
INVALID_OR_RESTRICTED_CARD. Try using another card. Do not retry the same card.
5190
SOFT_AVS.
5200
DUPLICATE_TRANSACTION.
5210
INVALID_TRANSACTION.
5400
EXPIRED_CARD.
5500
INCORRECT_PIN_REENTER.
5650
DECLINED_SCA_REQUIRED.
5700
TRANSACTION_NOT_PERMITTED. Outside of scope of accepted business.
5710
TX_ATTEMPTS_EXCEED_LIMIT.
5800
REVERSAL_REJECTED.
5900
INVALID_ISSUE.
5910
ISSUER_NOT_AVAILABLE_NOT_RETRIABLE.
5920
ISSUER_NOT_AVAILABLE_RETRIABLE.
5930
CARD_NOT_ACTIVATED.
5950
DECLINED_DUE_TO_UPDATED_ACCOUNT. External decline as an updated card has been issued.
6300
ACCOUNT_NOT_ON_FILE.
7600
APPROVED_NON_CAPTURE.
7700
ERROR_3DS.
7710
AUTHENTICATION_FAILED.
7800
BIN_ERROR.
7900
PIN_ERROR.
8000
PROCESSOR_SYSTEM_ERROR.
8010
HOST_KEY_ERROR.
8020
CONFIGURATION_ERROR.
8030
UNSUPPORTED_OPERATION.
8100
FATAL_COMMUNICATION_ERROR.
8110
RETRIABLE_COMMUNICATION_ERROR.
8220
SYSTEM_UNAVAILABLE.
9100
DECLINED_PLEASE_RETRY. Retry.
9500
SUSPECTED_FRAUD. Try using another card. Do not retry the same card.
9510
SECURITY_VIOLATION.
9520
LOST_OR_STOLEN. Try using another card. Do not retry the same card.
9530
HOLD_CALL_CENTER. The merchant must call the number on the back of the card. POS scenario.
9540
REFUSED_CARD.
9600
UNRECOGNIZED_RESPONSE_CODE.
0000
APPROVED.
00N7
CVV2_FAILURE_POSSIBLE_RETRY_WITH_CVV.
0100
REFERRAL.
0390
ACCOUNT_NOT_FOUND.
0500
DO_NOT_HONOR.
0580
UNAUTHORIZED_TRANSACTION.
0800
BAD_RESPONSE_REVERSAL_REQUIRED.
0880
CRYPTOGRAPHIC_FAILURE.
0890
UNACCEPTABLE_PIN.
0960
SYSTEM_MALFUNCTION.
0R00
CANCELLED_PAYMENT.
10BR
ISSUER_REJECTED.
PCNR
CONTINGENCIES_NOT_RESOLVED.
PCVV
CVV_FAILURE.
PP06
ACCOUNT_CLOSED. A previously open account is now closed
PPRN
REATTEMPT_NOT_PERMITTED.
PPAD
BILLING_ADDRESS.
PPAB
ACCOUNT_BLOCKED_BY_ISSUER.
PPAE
AMEX_DISABLED.
PPAG
ADULT_GAMING_UNSUPPORTED.
PPAI
AMOUNT_INCOMPATIBLE.
PPAR
AUTH_RESULT.
PPAU
MCC_CODE.
PPAV
ARC_AVS.
PPAX
AMOUNT_EXCEEDED.
PPBG
BAD_GAMING.
PPC2
ARC_CVV.
PPCE
CE_REGISTRATION_INCOMPLETE.
PPCO
COUNTRY.
PPCR
CREDIT_ERROR.
PPCT
CARD_TYPE_UNSUPPORTED.
PPCU
CURRENCY_USED_INVALID.
PPD3
SECURE_ERROR_3DS.
PPDC
DCC_UNSUPPORTED.
PPDI
DINERS_REJECT.
PPDV
AUTH_MESSAGE.
PPDT
DECLINE_THRESHOLD_BREACH.
PPEF
EXPIRED_FUNDING_INSTRUMENT.
PPEL
EXCEEDS_FREQUENCY_LIMIT.
PPER
INTERNAL_SYSTEM_ERROR.
PPEX
EXPIRY_DATE.
PPFE
FUNDING_SOURCE_ALREADY_EXISTS.
PPFI
INVALID_FUNDING_INSTRUMENT.
PPFR
RESTRICTED_FUNDING_INSTRUMENT.
PPFV
FIELD_VALIDATION_FAILED.
PPGR
GAMING_REFUND_ERROR.
PPH1
H1_ERROR.
PPIF
IDEMPOTENCY_FAILURE.
PPII
INVALID_INPUT_FAILURE.
PPIM
ID_MISMATCH.
PPIT
INVALID_TRACE_ID.
PPLR
LATE_REVERSAL.
PPLS
LARGE_STATUS_CODE.
PPMB
MISSING_BUSINESS_RULE_OR_DATA.
PPMC
BLOCKED_Mastercard.
PPMD
DEPRECATED The PPMD value has been deprecated.
PPNC
NOT_SUPPORTED_NRC.
PPNL
EXCEEDS_NETWORK_FREQUENCY_LIMIT.
PPNM
NO_MID_FOUND.
PPNT
NETWORK_ERROR.
PPPH
NO_PHONE_FOR_DCC_TRANSACTION.
PPPI
INVALID_PRODUCT.
PPPM
INVALID_PAYMENT_METHOD.
PPQC
QUASI_CASH_UNSUPPORTED.
PPRE
UNSUPPORT_REFUND_ON_PENDING_BC.
PPRF
INVALID_PARENT_TRANSACTION_STATUS.
PPRR
MERCHANT_NOT_REGISTERED.
PPS0
BANKAUTH_ROW_MISMATCH.
PPS1
BANKAUTH_ROW_SETTLED.
PPS2
BANKAUTH_ROW_VOIDED.
PPS3
BANKAUTH_EXPIRED.
PPS4
CURRENCY_MISMATCH.
PPS5
CREDITCARD_MISMATCH.
PPS6
AMOUNT_MISMATCH.
PPSC
ARC_SCORE.
PPSD
STATUS_DESCRIPTION.
PPSE
AMEX_DENIED.
PPTE
VERIFICATION_TOKEN_EXPIRED.
PPTF
INVALID_TRACE_REFERENCE.
PPTI
INVALID_TRANSACTION_ID.
PPTR
VERIFICATION_TOKEN_REVOKED.
PPTT
TRANSACTION_TYPE_UNSUPPORTED.
PPTV
INVALID_VERIFICATION_TOKEN.
PPUA
USER_NOT_AUTHORIZED.
PPUC
CURRENCY_CODE_UNSUPPORTED.
PPUE
UNSUPPORT_ENTITY.
PPUI
UNSUPPORT_INSTALLMENT.
PPUP
UNSUPPORT_POS_FLAG.
PPUR
UNSUPPORTED_REVERSAL.
PPVC
VALIDATE_CURRENCY.
PPVE
VALIDATION_ERROR.
PPVT
VIRTUAL_TERMINAL_UNSUPPORTED.
payment_advice_code
string
The declined payment transactions might have payment advice codes. The card networks, like Visa and Mastercard, return payment advice codes.
Enum Value
Description
21
For Mastercard, the card holder has been unsuccessful at canceling recurring payment through merchant. Stop recurring payment requests. For Visa, all recurring payments were canceled for the card number requested. Stop recurring payment requests.
22
For Mastercard, merchant does not qualify for product code.
24
For Mastercard, retry after 1 hour.
25
For Mastercard, retry after 24 hours.
26
For Mastercard, retry after 2 days.
27
For Mastercard, retry after 4 days.
28
For Mastercard, retry after 6 days.
29
For Mastercard, retry after 8 days.
30
For Mastercard, retry after 10 days .
40
For Mastercard, consumer non-reloadable prepaid card.
43
For Mastercard, consumer multi-use virtual card number.
01
For Mastercard, expired card account upgrade or portfolio sale conversion. Obtain new account information before next billing cycle.
02
For Mastercard, over credit limit or insufficient funds. Retry the transaction 72 hours later. For Visa, the card holder wants to stop only one specific payment in the recurring payment relationship. The merchant must NOT resubmit the same transaction. The merchant can continue the billing process in the subsequent billing period.
03
For Mastercard, account closed as fraudulent. Obtain another type of payment from customer due to account being closed or fraud. Possible reason: Account closed as fraudulent. For Visa, the card holder wants to stop all recurring payment transactions for a specific merchant. Stop recurring payment requests.
04
For Mastercard, token requirements not fulfilled for this token type.
Copy
{
"avs_code"
:
"A"
,
"cvv_code"
:
"E"
,
"response_code"
:
"0000"
,
"payment_advice_code"
:
"01"
}
Reauthorize Request
Reauthorizes an authorized PayPal account payment, by ID. To ensure that funds are still available, reauthorize a payment after its initial three-day honor period expires. You can reauthorize a payment only once from days four to 29.
If 30 days have transpired since the date of the original authorization, you must create an authorized payment instead of reauthorizing the original authorized payment.
A reauthorized payment itself has a new honor period of three days.
You can reauthorize an authorized payment once. The allowed amount depends on context and geography, for example in US it is up to 115% of the original authorized amount, not to exceed an increase of $75 USD.
Supports only the
amount
request parameter.
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
refund
The refund information.
status
string
(
Refund Status With Details
)
The status of the refund.
Enum Value
Description
CANCELLED
The refund was cancelled.
FAILED
The refund could not be processed.
PENDING
The refund is pending. For more information, see
status_details.reason
.
COMPLETED
The funds for this transaction were debited to the customer's account.
status_details
object
(
refund_status_details
)
The details of the refund status.
id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The PayPal-generated ID for the refund.
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
invoice_id
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The API caller-provided external invoice number for this order. Appears in both the payer's transaction history and the emails that the payer receives.
custom_id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-_.,]*$
The API caller-provided external ID. Used to reconcile API caller-initiated transactions with PayPal transactions. Appears in transaction and settlement reports.
acquirer_reference_number
string
[ 1 .. 36 ] characters
^[a-zA-Z0-9]+$
Reference ID issued for the card transaction. This ID can be used to track the transaction across processors, card brands and issuing banks.
note_to_payer
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The reason for the refund. Appears in both the payer's transaction history and the emails that the payer receives.
seller_payable_breakdown
object
(
Seller Payable Breakdown
)
The breakdown of the refund.
payer
object
(
payee_base
)
The details for the merchant who receives the funds and fulfills the order. The merchant is also known as the payee.
buyer_context
object
(
Buyer Context
)
The buyer context for the refund transaction.
links
Array of
objects
(
Link Description
)
[ 0 .. 32767 ] items
An array of related
HATEOAS links
.
create_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
update_time
string
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
Copy
Expand all
Collapse all
{
"status"
:
"CANCELLED"
,
"status_details"
:
{
"reason"
:
"ECHECK"
}
,
"id"
:
"string"
,
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"invoice_id"
:
"string"
,
"custom_id"
:
"string"
,
"acquirer_reference_number"
:
"string"
,
"note_to_payer"
:
"string"
,
"seller_payable_breakdown"
:
{
"gross_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"paypal_fee"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"paypal_fee_in_receivable_currency"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"net_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"net_amount_in_receivable_currency"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"platform_fees"
:
[
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
]
,
"net_amount_breakdown"
:
[
{
"payable_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"converted_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"exchange_rate"
:
{
"source_currency"
:
"string"
,
"target_currency"
:
"string"
,
"value"
:
"string"
}
}
]
,
"total_refunded_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
}
,
"payer"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
,
"buyer_context"
:
{
"transaction_id"
:
"string"
,
"transaction_details_url"
:
"
http://example.com
"
,
"transaction_create_time"
:
"string"
,
"transaction_update_time"
:
"string"
}
,
"links"
:
[
{
"href"
:
"string"
,
"rel"
:
"string"
,
"method"
:
"GET"
,
"title"
:
"string"
,
"mediaType"
:
"string"
,
"encType"
:
"application/json"
,
"schema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
,
"targetSchema"
:
{
"additionalItems"
:
{ }
,
"dependencies"
:
{ }
,
"items"
:
{ }
,
"definitions"
:
{ }
,
"patternProperties"
:
{ }
,
"properties"
:
{ }
,
"allOf"
:
[
{ }
]
,
"anyOf"
:
[
{ }
]
,
"oneOf"
:
[
{ }
]
,
"not"
:
{ }
,
"links"
:
[
{ }
]
,
"fragmentResolution"
:
"string"
,
"media"
:
{
"type"
:
"string"
,
"binaryEncoding"
:
"string"
}
,
"pathStart"
:
"
http://example.com
"
}
}
]
,
"create_time"
:
"string"
,
"update_time"
:
"string"
}
Refund Request
Refunds a captured payment, by ID. For a full refund, include an empty request body. For a partial refund, include an
amount
object in the request body.
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
custom_id
string
[ 1 .. 127 ] characters
^.*$
The API caller-provided external ID. Used to reconcile API caller-initiated transactions with PayPal transactions. Appears in transaction and settlement reports. The pattern is defined by an external party and supports Unicode.
invoice_id
string
[ 1 .. 127 ] characters
^.*$
The API caller-provided external invoice ID for this order. The pattern is defined by an external party and supports Unicode.
note_to_payer
string
[ 1 .. 255 ] characters
^.*$
The reason for the refund. Appears in both the payer's transaction history and the emails that the payer receives. The pattern is defined by an external party and supports Unicode.
payment_instruction
object
(
payment_instruction
)
Any additional payments instructions during refund payment processing. This object is only applicable to merchants that have been enabled for PayPal Commerce Platform for Marketplaces and Platforms capability. Please speak to your account manager if you want to use this capability.
Copy
Expand all
Collapse all
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"custom_id"
:
"string"
,
"invoice_id"
:
"string"
,
"note_to_payer"
:
"string"
,
"payment_instruction"
:
{
"platform_fees"
:
[
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
]
}
}
refund_status
The refund status with details.
status
string
(
Refund Status With Details
)
The status of the refund.
Enum Value
Description
CANCELLED
The refund was cancelled.
FAILED
The refund could not be processed.
PENDING
The refund is pending. For more information, see
status_details.reason
.
COMPLETED
The funds for this transaction were debited to the customer's account.
status_details
object
(
refund_status_details
)
The details of the refund status.
Copy
Expand all
Collapse all
{
"status"
:
"CANCELLED"
,
"status_details"
:
{
"reason"
:
"ECHECK"
}
}
refund_status_details
The details of the refund status.
reason
string
(
Refund Incomplete Reason
)
The reason why the refund has the
PENDING
or
FAILED
status.
Value
Description
ECHECK
The customer's account is funded through an eCheck, which has not yet cleared.
Copy
{
"reason"
:
"ECHECK"
}
Related Identifiers
Identifiers related to a specific resource.
order_id
string
[ 1 .. 20 ] characters
^[A-Z0-9]+$
Order ID related to the resource.
authorization_id
string
[ 1 .. 20 ] characters
^[A-Z0-9]+$
Authorization ID related to the resource.
capture_id
string
[ 1 .. 20 ] characters
^[A-Z0-9]+$
Capture ID related to the resource.
Copy
{
"order_id"
:
"string"
,
"authorization_id"
:
"string"
,
"capture_id"
:
"string"
}
Response for ACH
Response for ACH payment method.
can_be_vaulted
boolean
Default:
false
Indicates if the payment method can be vaulted or not. A true value indicates the payment method can be vaulted using our vaults product. If false, vaulting is not currently supported for this payment method.
Copy
{
"can_be_vaulted"
:
false
}
Response for PayPal
Response for PayPal.
can_be_vaulted
boolean
Default:
false
Indicates if the payment method can be vaulted or not. A true value indicates the payment method can be vaulted using our vaults product. If false, vaulting is not currently supported for this payment method.
country_code
string
(
country_code-2
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
product_code
string
(
Credit Button Eligibility Button Code
)
The button code corresponding to a particular product or set of products. The values followed are defined by the SDK team.
Enum Value
Description
CREDIT
Open ended credit products.
PAYLATER
Pay Later suite of products.
PAY_IN_3
Pay In 3 suite of products.
PAY_IN_4
Pay In 4 suite of products.
eligible_in_paypal_network
boolean
(
PayPal services member indicator
)
Flag that indicates if the customer is in the PayPal network. This value will be included in the response if the include_account_details flag is set to "true" in the API request.
recommended
boolean
Default:
"false"
Indicates if the payment method is recommended or not. A true value indicates the customer is payment ready and this payment method may be presented upfront.
recommended_priority
integer
[ 1 .. 3 ]
This value is included in the response when recommended is true for a payment method. It indicates the priority of recommendation for payment readiness of eligible payment methods with lowest number taking the highest precedence.
Copy
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"eligible_in_paypal_network"
:
true
,
"recommended"
:
"false"
,
"recommended_priority"
:
1
}
Response for Venmo
Response for Venmo.
can_be_vaulted
boolean
Default:
false
Indicates if the payment method can be vaulted or not. A true value indicates the payment method can be vaulted using our vaults product. If false, vaulting is not currently supported for this payment method.
country_code
string
(
country_code-2
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
product_code
string
(
Credit Button Eligibility Button Code
)
The button code corresponding to a particular product or set of products. The values followed are defined by the SDK team.
Enum Value
Description
CREDIT
Open ended credit products.
PAYLATER
Pay Later suite of products.
PAY_IN_3
Pay In 3 suite of products.
PAY_IN_4
Pay In 4 suite of products.
eligible_in_paypal_network
boolean
(
PayPal services member indicator
)
Flag that indicates if the customer is in the PayPal network. This value will be included in the response if the include_account_details flag is set to "true" in the API request.
recommended
boolean
Default:
"false"
Indicates if the payment method is recommended or not. A true value indicates the customer is payment ready and this payment method may be presented upfront.
recommended_priority
integer
[ 1 .. 3 ]
This value is included in the response when recommended is true for a payment method. It indicates the priority of recommendation for payment readiness of eligible payment methods with lowest number taking the highest precedence.
Copy
{
"can_be_vaulted"
:
false
,
"country_code"
:
"string"
,
"product_code"
:
"CREDIT"
,
"eligible_in_paypal_network"
:
true
,
"recommended"
:
"false"
,
"recommended_priority"
:
1
}
Schema Object for standard headers
Standard headers are generally less restrictive in structure due to historical precedent across browsers, etc. This is a common schema for use in defining most standard headers.
string
(
Schema Object for standard headers
)
[ 1 .. 16000 ] characters
^.*$
Standard headers are generally less restrictive in structure due to historical precedent across browsers, etc. This is a common schema for use in defining most standard headers.
Copy
"string"
Seller Receivable Breakdown
The detailed breakdown of the capture activity. This is not available for transactions that are in pending state.
gross_amount
required
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
paypal_fee
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
paypal_fee_in_receivable_currency
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
net_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
receivable_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
exchange_rate
object
(
exchange_rate
)
The exchange rate that determines the amount to convert from one currency to another currency.
platform_fees
Array of
objects
(
platform_fee
)
[ 0 .. 1 ] items
An array of platform or partner fees, commissions, or brokerage fees that associated with the captured payment.
Copy
Expand all
Collapse all
{
"gross_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"paypal_fee"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"paypal_fee_in_receivable_currency"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"net_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"receivable_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"exchange_rate"
:
{
"source_currency"
:
"string"
,
"target_currency"
:
"string"
,
"value"
:
"string"
}
,
"platform_fees"
:
[
{
"amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"payee"
:
{
"email_address"
:
"string"
,
"merchant_id"
:
"string"
}
}
]
}
seller_protection
The level of protection offered as defined by
PayPal Seller Protection for Merchants
.
status
string
(
Seller Protection Status
)
Indicates whether the transaction is eligible for seller protection. For information, see
PayPal Seller Protection for Merchants
.
Enum Value
Description
ELIGIBLE
Your PayPal balance remains intact if the customer claims that they did not receive an item or the account holder claims that they did not authorize the payment.
PARTIALLY_ELIGIBLE
Your PayPal balance remains intact if the customer claims that they did not receive an item.
NOT_ELIGIBLE
This transaction is not eligible for seller protection.
dispute_categories
Array of
strings
(
dispute_category
)
[ 0 .. 32767 ] items
An array of conditions that are covered for the transaction.
Items
Enum Value
Description
ITEM_NOT_RECEIVED
The payer paid for an item that they did not receive.
UNAUTHORIZED_TRANSACTION
The payer did not authorize the payment.
Copy
Expand all
Collapse all
{
"status"
:
"ELIGIBLE"
,
"dispute_categories"
:
[
"ITEM_NOT_RECEIVED"
]
}
Tokenization Parameters
Parameters for configuring payment tokenization with the gateway.
gateway
string
[ 2 .. 255 ] characters
^[a-zA-Z0-9_-]+$
Payment gateway name.
gateway_merchant_id
string
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The account identifier for a PayPal account.
Copy
{
"gateway"
:
"string"
,
"gateway_merchant_id"
:
"string"
}
Tokenization Specification
Specification for payment method tokenization in Google Pay.
type
string
Tokenization type.
Value
Description
PAYMENT_GATEWAY
Tokenization using a payment gateway.
parameters
object
(
Tokenization Parameters
)
Parameters for configuring payment tokenization with the gateway.
Copy
Expand all
Collapse all
{
"type"
:
"PAYMENT_GATEWAY"
,
"parameters"
:
{
"gateway"
:
"string"
,
"gateway_merchant_id"
:
"string"
}
}
