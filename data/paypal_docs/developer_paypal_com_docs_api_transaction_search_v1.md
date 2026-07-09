# Transaction Search

Source: https://developer.paypal.com/docs/api/transaction-search/v1/

Transaction Search
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
Transaction Search
get
List transactions
get
List all balances
get
List all balance and net activity summary
get
List all daily summary
Errors
Definitions
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
Transaction Search
(
1
)
?
This API is currently not supported by our SDK
Use the Transaction Search API to get the history of transactions for a PayPal account. To use the API on behalf of third parties, you must be part of the PayPal partner network. Reach out to your partner manager for the next steps. To enroll in the partner program, see
Partner with PayPal
. For more information about the API, see the
Transaction Search API Integration Guide
.
Note:
To use the API on behalf of third parties, you must be part of the PayPal partner network. Reach out to your partner manager for the next steps. To enroll in the partner program, see
Partner with PayPal
.
List transactions
get
/v1/reporting/transactions
Try it
Lists transactions. Specify one or more query parameters to filter the transaction that appear in the response.
Notes:
If you specify one or more optional query parameters, the
ending_balance
response field is empty.
It takes a maximum of three hours for executed transactions to appear in the list transactions call.
This call lists transaction for the previous three years.
Security
Oauth2
Request
query
Parameters
transaction_id
string
[ 17 .. 19 ] characters
Filters the transactions in the response by a PayPal transaction ID. A valid transaction ID is 17 characters long, except for an
order ID
, which is 19 characters long.
Note:
A transaction ID is not unique in the reporting system. The response can list two transactions with the same ID. One transaction can be balance affecting while the other is non-balance affecting.
transaction_type
string
Filters the transactions in the response by a PayPal transaction event code. See
Transaction event codes
.
transaction_status
string
Filters the transactions in the response by a PayPal transaction status code. Value is:
Status code
Description
D
PayPal or merchant rules denied the transaction.
P
The transaction is pending. The transaction was created but waits for another payment process to complete, such as an ACH transaction, before the status changes to
S
.
S
The transaction successfully completed without a denial and after any pending statuses.
V
A successful transaction was reversed and funds were refunded to the original sender.
transaction_amount
string
Filters the transactions in the response by a gross transaction amount range. Specify the range as
<start-range> TO <end-range>
, where
<start-range>
is the lower limit of the gross PayPal transaction amount and
<end-range>
is the upper limit of the gross transaction amount. Specify the amounts in lower denominations. For example, to search for transactions from $5.00 to $10.05, specify
[500 TO 1005]
.
Note:
The values must be URL encoded.
transaction_currency
string
Filters the transactions in the response by a
three-character ISO-4217 currency code
for the PayPal transaction currency.
start_date
required
string
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
Filters the transactions in the response by a start date and time, in
Internet date and time format
. Seconds are required. Fractional seconds are optional.
end_date
required
string
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
Filters the transactions in the response by an end date and time, in
Internet date and time format
. Seconds are required. Fractional seconds are optional. The maximum supported range is 31 days.
payment_instrument_type
string
Filters the transactions in the response by a payment instrument type. Value is either:
CREDITCARD
. Returns a direct credit card transaction with a corresponding value.
DEBITCARD
. Returns a debit card transaction with a corresponding value.
If you omit this parameter, the API does not apply this filter.
store_id
string
Filters the transactions in the response by a store ID.
terminal_id
string
Filters the transactions in the response by a terminal ID.
fields
string
Default:
"transaction_info"
Indicates which fields appear in the response. Value is a single field or a comma-separated list of fields. The
transaction_info
value returns only the transaction details in the response. To include all fields in the response, specify
fields=all
. Valid fields are:
transaction_info
. The transaction information. Includes the ID of the PayPal account of the payee, the PayPal-generated transaction ID, the PayPal-generated base ID, the PayPal reference ID type, the transaction event code, the date and time when the transaction was initiated and was last updated, the transaction amounts including the PayPal fee, any discounts, insurance, the transaction status, and other information about the transaction.
payer_info
. The payer information. Includes the PayPal customer account ID and the payer's email address, primary phone number, name, country code, address, and whether the payer is verified or unverified.
shipping_info
. The shipping information. Includes the recipient's name, the shipping method for this order, the shipping address for this order, and the secondary address associated with this order.
auction_info
. The auction information. Includes the name of the auction site, the auction site URL, the ID of the customer who makes the purchase in the auction, and the date and time when the auction closes.
cart_info
. The cart information. Includes an array of item details, whether the item amount or the shipping amount already includes tax, and the ID of the invoice for PayPal-generated invoices.
incentive_info
. An array of incentive detail objects. Each object includes the incentive, such as a special offer or coupon, the incentive amount, and the incentive program code that identifies a merchant loyalty or incentive program.
store_info
. The store information. Includes the ID of the merchant store and the terminal ID for the checkout stand in the merchant store.
balance_affecting_records_only
string
Default:
"Y"
Indicates whether the response includes only balance-impacting transactions or all transactions. Value is either:
Y
. The default. The response includes only balance transactions.
N
. The response includes all transactions.
page_size
integer
[ 1 .. 500 ]
Default:
100
The number of items to return in the response. So, the combination of
page=1
and
page_size=20
returns the first 20 items. The combination of
page=2
and
page_size=20
returns the next 20 items.
page
integer
[ 1 .. 2147483647 ]
Default:
1
The zero-relative start index of the entire list of items that are returned in the response. So, the combination of
page=1
and
page_size=20
returns the first 20 items.
header
Parameters
PayPal-Enforce-ISO8601-Format
boolean
Default:
false
To switch between the new (ISO standard) and old date time format and the platform changes, include
PayPal-Enforce-ISO8601-Format
in the header. When this value is set to true, the APIs will support the new date time format and platform changes.
Note:
You can use the same header in the sandbox as well.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that lists transactions .
Request samples
cURL
Node.js
Java
Python
JavaScript
Node.js
Ruby
2 more
Node.js
Ruby
2 more
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v1/reporting/transactions?start_date
=
2022
-04-25T00:00:00-07:00
&
end_date
=
2022
-05-10T23:59:59:59-07:00
&
transaction_id
=
03A84379GE3808324
&
fields
=
all
\
-H
'X-PAYPAL-SECURITY-CONTEXT: {"version":"1.2","actor":{"client_id":"AU67ewLFkviOMY6i9-e-xtDS2gCxhQXHL42yZLfbUu0wT1RQojFo-IXG92wv0hAaZ2ore6grSgmj1VcQ","id":"35740404","auth_claims":["CLIENT_ID_SECRET"],"auth_state":"LOGGEDIN","account_number":"4774069174790210149","encrypted_account_number":"7SRRZ9L73CNY6","party_id":"1480460762532829633","user_type":"API_CALLER"},"auth_token_type":"ACCESS_TOKEN","scopes":["https://uri.paypal.com/services/reporting/search/read"],"client_id":"AU67ewLFkviOMY6i9-e-xtDS2gCxhQXHL42yZLfbUu0wT1RQojFo-IXG92wv0hAaZ2ore6grSgmj1VcQ","app_id":"APP-80W284485P519543T","claims":{"actor_payer_id":"JVH3C98SC4E84","internal_application":"false"},"subjects":[{"subject":{"id":"35762049","auth_claims":["PAYER_ID"],"auth_state":"IDENTIFIED","account_number":"1256692217768566521","encrypted_account_number":"XZXSPECPDZHZU","party_id":"2277051500535724448","user_type":"MERCHANT"},"features":[]}]}'
\
-H
'Content-Type: application/json'
Response samples
200
application/json
Sample 1 - 200 - List PayPal decline transactions
Sample 1 - 200 - List PayPal decline transactions
Copy
Expand all
Collapse all
{
"transaction_details"
:
[
{
"transaction_info"
:
{
"paypal_account_id"
:
"DR5YHAS5Y2FHN"
,
"transaction_id"
:
"03A84379GE3808324"
,
"transaction_event_code"
:
"T0007"
,
"transaction_initiation_date"
:
"2022-05-02T07:24:52Z"
,
"transaction_updated_date"
:
"2022-05-02T07:24:52Z"
,
"transaction_amount"
:
{
"currency_code"
:
"EUR"
,
"value"
:
"105.00"
}
,
"fee_amount"
:
{
"currency_code"
:
"EUR"
,
"value"
:
"-0.40"
}
,
"transaction_status"
:
"S"
,
"transaction_subject"
:
"Description of PU1"
,
"invoice_id"
:
"invoice_id_1651476157"
,
"custom_field"
:
"custom_id_1651476157"
,
"protection_eligibility"
:
"01"
,
"instrument_type"
:
"Direct Debit"
,
"decline_code"
:
"AM04"
}
,
"payer_info"
:
{
"account_id"
:
"DR5YHAS5Y2FHN"
,
"email_address"
:
"
[email protected]
"
,
"address_status"
:
"N"
,
"payer_status"
:
"N"
,
"payer_name"
:
{
"given_name"
:
"DE"
,
"surname"
:
"SEPA"
,
"alternate_full_name"
:
"DE SEPA"
}
,
"country_code"
:
"DE"
}
,
"shipping_info"
:
{
"name"
:
"DE, SEPA"
}
,
"cart_info"
:
{
"item_details"
:
[
{
"item_code"
:
"259483234816"
,
"item_name"
:
"VRLens1"
,
"item_description"
:
"VRLens1"
,
"item_quantity"
:
"1"
,
"item_unit_price"
:
{
"currency_code"
:
"EUR"
,
"value"
:
"55.00"
}
,
"item_amount"
:
{
"currency_code"
:
"EUR"
,
"value"
:
"55.00"
}
,
"total_item_amount"
:
{
"currency_code"
:
"EUR"
,
"value"
:
"55.00"
}
,
"invoice_number"
:
"invoice_id_1651476157"
}
,
{
"item_code"
:
"259483234816"
,
"item_name"
:
"VRLens2"
,
"item_description"
:
"VRLens2"
,
"item_quantity"
:
"1"
,
"item_unit_price"
:
{
"currency_code"
:
"EUR"
,
"value"
:
"50.00"
}
,
"item_amount"
:
{
"currency_code"
:
"EUR"
,
"value"
:
"50.00"
}
,
"total_item_amount"
:
{
"currency_code"
:
"EUR"
,
"value"
:
"50.00"
}
,
"invoice_number"
:
"invoice_id_1651476157"
}
]
}
,
"store_info"
:
{ }
,
"auction_info"
:
{ }
,
"incentive_info"
:
{ }
}
]
,
"start_date"
:
"2022-04-25T00:00:00Z"
,
"end_date"
:
"2022-05-10T23:59:59Z"
,
"last_refreshed_datetime"
:
"2022-05-19T12:06:56Z"
,
"page"
:
1
,
"total_items"
:
1
,
"total_pages"
:
1
,
"links"
:
[
{
"href"
:
"
https://api-m.sandbox.paypal.com/v1/reporting/transactions?fields=all&transaction_id=03A84379GE3808324&end_date=2022-05-10T23%3A59%3A59Z&start_date=2022-04-25T00%3A00%3A00Z&page_size=100&page=1
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
List all balances
get
/v1/reporting/balances
Try it
List all balances. Specify date time to list balances for that time that appear in the response.
Notes:
It takes a maximum of three hours for balances to appear in the list balances call.
This call lists balances upto the previous three years.
Security
Oauth2
Request
query
Parameters
as_of_time
string
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
List balances in the response at the date time provided, will return the last refreshed balance in the system when not provided.
currency_code
string
<
ppaas_common_currency_code_v2
>
= 3 characters
Filters the transactions in the response by a
three-character ISO-4217 currency code
for the PayPal transaction currency.
header
Parameters
PayPal-Enforce-ISO8601-Format
boolean
Default:
false
To switch between the new (ISO standard) and old date time format and the platform changes, include
PayPal-Enforce-ISO8601-Format
in the header. When this value is set to true, the APIs will support the new date time format and platform changes.
Note:
You can use the same header in the sandbox as well.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that lists balances .
Request samples
cURL
Node.js
Java
Python
JavaScript
Node.js
Ruby
2 more
Node.js
Ruby
2 more
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v1/reporting/balances?currency_code
=
ALL
&
as_of_time
=
2021
-02-22T00:00:00-07:00
\
-H
'Authorization: Bearer {{ACCESS_TOKEN}}'
\
-H
'Content-Type: application/json'
Response samples
200
application/json
Sample 1 - 200 - List Balance for currency code
Sample 1 - 200 - List Balance for currency code
Copy
Expand all
Collapse all
{
"balances"
:
[
{
"currency"
:
"USD"
,
"primary"
:
true
,
"total_balance"
:
{
"currency_code"
:
"USD"
,
"value"
:
"300.00"
}
,
"available_balance"
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
"withheld_balance"
:
{
"currency_code"
:
"USD"
,
"value"
:
"200.00"
}
}
]
,
"account_id"
:
"DV77JV8VP82XE"
,
"as_of_time"
:
"2021-02-22T11:35:58Z"
,
"last_refresh_time"
:
"2021-03-03T16:23:30Z"
}
List all balance and net activity summary
get
/v1/reporting/get-balance-net-summary
Try it
List all balance and net activity summary for each currency within a given date range.
Security
Oauth2
Request
query
Parameters
from_date
required
string
= 10 characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
List balances in the response at the date time provided, will return the last refreshed balance in the system when not provided.
to_date
required
string
= 10 characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
List balances in the response at the date time provided, will return the last refreshed balance in the system when not provided.
locale
required
string
[ 5 .. 10 ] characters
^[a-zA-Z]{2}[-|_][a-zA-Z]{2}$
To get the locale of the client.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that lists balance and net activity summary.
Request samples
cURL
Node.js
Java
Python
JavaScript
Node.js
Ruby
2 more
Node.js
Ruby
2 more
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v1/reporting/get-balance-net-summary?from_date
=
2024
-02-01
&
to_date
=
2024
-02-29
&
locale
=
en_US
\
-H
'X-PAYPAL-SECURITY-CONTEXT: {"version":"1.2","actor":{"client_id":"AafBGhBphJ66SHPtbCMTsH1q2HQC2lnf0ER0KWAVSsOqsAtVfnye5Vc8hAOC","id":"245285","auth_claims":["CLIENT_ID_SECRET"],"auth_state":"LOGGEDIN","account_number":"1539671732305563784","encrypted_account_number":"SZEKQNBKSSQ8L","party_id":"1539671732305563784","user_type":"API_CALLER","tenant_context":{"tenant_name":"PayPal","tenant_id":"65B786CC-E0BB-4B20-AC72-C69FF1A65CE2"},"legal_country":"DE"},"auth_token":"A005yNuXYiYS-mj7KfHmQ2LXLAPQpavLQ2wbtvnhDGypJSA","auth_token_type":"ACCESS_TOKEN","global_session_id":"I535cb328-3ba2-4163-bf59-3c4b20d5b623","last_validated":1.648686724428E9,"scopes":["https://uri.paypal.com/services/reporting/dataapiserv/balance-net-activity/read","https://uri.paypal.com/services/reporting/dataapiserv/daily/read"],"client_id":"AafBGhBphJ66SHPtbCMTsH1q2HQC2lnf0ER0KWAVSsOqsAtVfnye5Vc8hAOC","claims":{"subject_payer_id":"6WUPRA7KVSLNC","actor_payer_id":"SZEKQNBKSSQ8L","internal_application":"true","consent_id":"3THxztjeJqIIHROYmYkYn_EMsF5pvfVQFndEU1rQusA"},"edge_authorization":{"policy_decision":"PERMIT","obligations":[]},"subjects":[{"subject":{"public_credential":"
[email protected]
","id":"3339807541","auth_claims":["USERNAME","PASSWORD"],"auth_state":"LOGGEDIN","account_number":"4809087915324943324","encrypted_account_number":"6WUPRA7KVSLNC","party_id":"4809087915324943324","authenticating_user":true,"user_type":"CONSUMER","tenant_context":{"tenant_name":"PAYPAL","tenant_id":"65B786CC-E0BB-4B20-AC72-C69FF1A65CE2"},"authentication_context":{"sca_context":{"status":"IN_PROGRESS","factors":["K"]}},"identity_provider":"urn:idp:paypal","legal_country":"AT"},"features":[]}],"signature":"eyJraWQiOiJhdXRoX3NlY3VyaXR5X2NvbnRleHRfc2lnbl9rZXkiL"}'
Response samples
200
application/json
Sample 1 - 200 - Balance Net Activity Summary
Sample 1 - 200 - Balance Net Activity Summary
Copy
Expand all
Collapse all
{
"last_refresh_date"
:
"2024-06-05"
,
"reconciliation_passed"
:
true
,
"net_activity"
:
{
"columns"
:
[
"activity"
,
"count"
,
"amount"
]
,
"activities"
:
[
{
"net_activity_sum"
:
"1200.0"
,
"fee_sum"
:
"20.0"
,
"activity_details"
:
[
[
"fee"
,
"2"
,
"20.0"
]
,
[
"refund"
,
"2"
,
"1000.0"
]
]
}
,
{
"net_activity_sum"
:
"400.0"
,
"fee_sum"
:
"20.0"
,
"activity_details"
:
[
[
"withdrawal"
,
"2"
,
"100.0"
]
,
[
"sales"
,
"4"
,
"200.0"
]
,
[
"fee"
,
"2"
,
"20.0"
]
]
}
,
{
"net_activity_sum"
:
"200.0"
,
"fee_sum"
:
"10.0"
,
"activity_details"
:
[
[
"fee"
,
"1"
,
"10.0"
]
,
[
"withdrawal"
,
"1"
,
"50.0"
]
,
[
"sales"
,
"2"
,
"100.0"
]
]
}
]
,
"currencies"
:
[
"USD"
,
"CAD"
,
"EUR"
]
}
,
"balance_summary"
:
{
"data"
:
[
[
"USD"
,
"4000.0"
,
"1200.0"
,
"5200.0"
]
,
[
"CAD"
,
"10000.0"
,
"400.0"
,
"10400.0"
]
,
[
"EUR"
,
"5000.0"
,
"200.0"
,
"5200.0"
]
]
,
"columns"
:
[
"currencyCode"
,
"openingBalance"
,
"netActivity"
,
"closingBalance"
]
}
}
List all daily summary
get
/v1/reporting/get-daily-summary
Try it
List all daily summary for each currency within a given date range.
Security
Oauth2
Request
query
Parameters
from_date
required
string
= 10 characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
List balances in the response at the date time provided, will return the last refreshed balance in the system when not provided.
to_date
required
string
= 10 characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
List balances in the response at the date time provided, will return the last refreshed balance in the system when not provided.
locale
required
string
[ 5 .. 10 ] characters
^[a-zA-Z]{2}[-|_][a-zA-Z]{2}$
To get the locale of the client.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that lists balances .
Request samples
cURL
Node.js
Java
Python
JavaScript
Node.js
Ruby
2 more
Node.js
Ruby
2 more
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v1/reporting/get-daily-summary?from_date
=
2024
-02-01
&
to_date
=
2024
-02-29
&
locale
=
en_US
\
-H
'X-PAYPAL-SECURITY-CONTEXT: {"version":"1.2","actor":{"client_id":"AafBGhBphJ66SHPtbCMTsH1q2HQC2lnf0ER0KWAVSsOqsAtVfnye5Vc8hAOC","id":"245285","auth_claims":["CLIENT_ID_SECRET"],"auth_state":"LOGGEDIN","account_number":"1539671732305563784","encrypted_account_number":"SZEKQNBKSSQ8L","party_id":"1539671732305563784","user_type":"API_CALLER","tenant_context":{"tenant_name":"PayPal","tenant_id":"65B786CC-E0BB-4B20-AC72-C69FF1A65CE2"},"legal_country":"DE"},"auth_token":"A005yNuXYiYS-mj7KfHmQ2LXLAPQpavLQ2wbtvnhDGypJSA","auth_token_type":"ACCESS_TOKEN","global_session_id":"I535cb328-3ba2-4163-bf59-3c4b20d5b623","last_validated":1.648686724428E9,"scopes":["https://uri.paypal.com/services/reporting/dataapiserv/balance-net-activity/read","https://uri.paypal.com/services/reporting/dataapiserv/daily/read"],"client_id":"AafBGhBphJ66SHPtbCMTsH1q2HQC2lnf0ER0KWAVSsOqsAtVfnye5Vc8hAOC","claims":{"subject_payer_id":"6WUPRA7KVSLNC","actor_payer_id":"SZEKQNBKSSQ8L","internal_application":"true","consent_id":"3THxztjeJqIIHROYmYkYn_EMsF5pvfVQFndEU1rQusA"},"edge_authorization":{"policy_decision":"PERMIT","obligations":[]},"subjects":[{"subject":{"public_credential":"
[email protected]
","id":"3339807541","auth_claims":["USERNAME","PASSWORD"],"auth_state":"LOGGEDIN","account_number":"4809087915324943324","encrypted_account_number":"6WUPRA7KVSLNC","party_id":"4809087915324943324","authenticating_user":true,"user_type":"CONSUMER","tenant_context":{"tenant_name":"PAYPAL","tenant_id":"65B786CC-E0BB-4B20-AC72-C69FF1A65CE2"},"authentication_context":{"sca_context":{"status":"IN_PROGRESS","factors":["K"]}},"identity_provider":"urn:idp:paypal","legal_country":"AT"},"features":[]}],"signature":"eyJraWQiOiJhdXRoX3NlY3VyaXR5X2NvbnRleHRfc2lnbl9rZXkiL"}'
Response samples
200
application/json
Sample 1 - 200 - Daily Summary
Sample 1 - 200 - Daily Summary
Copy
Expand all
Collapse all
{
"currencies"
:
[
"USD"
,
"CAD"
,
"EUR"
]
,
"summaries"
:
[
{
"activity"
:
[
"timePeriod"
,
"openingBalance"
,
"sales"
,
"fee"
,
"refund"
,
"dispute"
,
"closingBalance"
]
,
"data"
:
[
[
"2024-05-14"
,
"2000.0"
,
"null"
,
"10.0"
,
"500.0"
,
"null"
,
"2600.0"
]
,
[
"2024-05-15"
,
"2000.0"
,
"null"
,
"10.0"
,
"500.0"
,
"null"
,
"2600.0"
]
]
}
,
{
"activity"
:
[
"timePeriod"
,
"openingBalance"
,
"sales"
,
"fee"
,
"refund"
,
"dispute"
,
"withdrawal"
,
"closingBalance"
]
,
"data"
:
[
[
"2024-05-14"
,
"5000.0"
,
"100.0"
,
"10.0"
,
"null"
,
"null"
,
"50.0"
,
"5200.0"
]
,
[
"2024-05-15"
,
"5000.0"
,
"100.0"
,
"10.0"
,
"null"
,
"null"
,
"50.0"
,
"5200.0"
]
]
}
,
{
"activity"
:
[
"timePeriod"
,
"openingBalance"
,
"sales"
,
"fee"
,
"refund"
,
"dispute"
,
"withdrawal"
,
"closingBalance"
]
,
"data"
:
[
[
"2024-05-14"
,
"5000.0"
,
"100.0"
,
"10.0"
,
"null"
,
"null"
,
"50.0"
,
"5200.0"
]
]
}
]
}
Errors
INTERNAL_SERVICE_ERROR
Message:
Internal service error.
Description:
Something unexpected occurred on the server.
INVALID_REQUEST
Message:
Invalid request - see details.
Description:
The request is not well-formed or is syntactically incorrect or violates the schema.
INVALID_RESOURCE_ID
Message:
The resource was not found.
Description:
The requested resource could not be found but may be available in the future. Subsequent requests by the client are permissible.
RESULTSET_TOO_LARGE
Message:
Result set size is greater than the maximum limit. Change the filter criteria and try again.
Description:
The request returned more items than the maximum limit. To reduce the result set, include additional query parameters.
Definitions
account_id
The PayPal payer ID, which is a masked version of the PayPal account number intended for use with third parties. The account number is reversibly encrypted and a proprietary variant of Base32 is used to encode the result.
string
<
ppaas_payer_id_v3
>
(
account_id
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The PayPal payer ID, which is a masked version of the PayPal account number intended for use with third parties. The account number is reversibly encrypted and a proprietary variant of Base32 is used to encode the result.
Copy
"stringstrings"
Auction Information
The auction information.
auction_site
string
[ 1 .. 200 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The name of the auction site.
auction_item_site
string
<
uri
>
[ 1 .. 4000 ] characters
The auction site URL.
auction_buyer_id
string
[ 1 .. 500 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The ID of the buyer who makes the purchase in the auction. This ID might be different from the payer ID provided for the payment.
auction_closing_date
string
<
ppaas_date_time_v3
>
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
"auction_site"
:
"string"
,
"auction_item_site"
:
"
http://example.com
"
,
"auction_buyer_id"
:
"string"
,
"auction_closing_date"
:
"string"
}
Balance Information
The Balance information.
primary
boolean
Optional field representing if the currency is primary currency or not.
currency
required
string
<
ppaas_common_currency_code_v2
>
(
currency_code
)
= 3 characters
Currency Code of the balances listed.
total_balance
required
object
(
Money
)
The total amount in PayPal account. It is the sum of all the other balances.
available_balance
object
(
Money
)
The amount of cash in an Account which is at the customer's disposal. This amount is captured at settlement cutoff time in the user's time zone as defined for the user.
withheld_balance
object
(
Money
)
Balance withheld in the account. The portion of funds that PayPal holds for the customer that is not currently at the customer's disposal.
Copy
Expand all
Collapse all
{
"primary"
:
true
,
"currency"
:
"str"
,
"total_balance"
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
"available_balance"
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
"withheld_balance"
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
Balance Net Activity Summary
The balance and net activity summary details.
reconciliation_passed
boolean
Default:
"true"
Indicates whether the reconciliation of the merchant transaction data has passed.
last_refresh_date
string
<
ppaas_date_notime_v2
>
(
date_no_time
)
= 10 characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The last refresh date for merchant/partner accounting data.
balance_summary
object
(
Balance Summary
)
The balance summaries.
net_activity
object
(
Net Activity Details
)
The net activity details.
Copy
Expand all
Collapse all
{
"reconciliation_passed"
:
"true"
,
"last_refresh_date"
:
"string"
,
"balance_summary"
:
{
"columns"
:
[
"string"
]
,
"data"
:
[
[
"string"
]
]
}
,
"net_activity"
:
{
"currencies"
:
[
"string"
]
,
"columns"
:
[
"string"
]
,
"activities"
:
[
{
"net_activity_sum"
:
"string"
,
"fee_sum"
:
"string"
,
"activity_details"
:
[
[
"string"
]
]
}
]
}
}
Balance Summary
The balance summary for all currencies.
columns
Array of
strings
[ 1 .. 2147483647 ] items
An array of balance summary column names.
data
Array of
strings
[ 1 .. 2147483647 ] items
An array containing array of strings depicting balance summaries data for each currency.
Copy
Expand all
Collapse all
{
"columns"
:
[
"string"
]
,
"data"
:
[
[
"string"
]
]
}
Balances Response
The balances response information.
balances
Array of
objects
(
Balance Information
)
[ 1 .. 200 ] items
An array of balance detail objects.
account_id
string
<
ppaas_payer_id_v3
>
(
account_id
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The PayPal payer ID, which is a masked version of the PayPal account number intended for use with third parties. The account number is reversibly encrypted and a proprietary variant of Base32 is used to encode the result.
as_of_time
string
<
ppaas_date_time_v3
>
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The requested date and time or the last date and time when the balances can be served, in
Internet date and time format
.
last_refresh_time
string
<
ppaas_date_time_v3
>
(
date_time
)
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time when the balances was last refreshed, in
Internet date and time format
.
Copy
Expand all
Collapse all
{
"balances"
:
[
{
"primary"
:
true
,
"currency"
:
"str"
,
"total_balance"
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
"available_balance"
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
"withheld_balance"
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
]
,
"account_id"
:
"stringstrings"
,
"as_of_time"
:
"stringstringstringst"
,
"last_refresh_time"
:
"stringstringstringst"
}
Cart Information
The cart information.
item_details
Array of
objects
(
Item Details
)
[ 1 .. 32767 ] items
An array of item details.
tax_inclusive
boolean
Default:
false
Indicates whether the item amount or the shipping amount already includes tax.
paypal_invoice_id
string
[ 1 .. 127 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The ID of the invoice. Appears for only PayPal-generated invoices.
Copy
Expand all
Collapse all
{
"item_details"
:
[
{
"item_code"
:
"string"
,
"item_name"
:
"string"
,
"item_description"
:
"string"
,
"item_options"
:
"string"
,
"item_quantity"
:
"string"
,
"tax_amounts"
:
[
{
"tax_amount"
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
]
,
"invoice_number"
:
"string"
,
"checkout_options"
:
[
{
"checkout_option_name"
:
"string"
,
"checkout_option_value"
:
"string"
}
]
,
"item_unit_price"
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
"item_amount"
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
"discount_amount"
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
"adjustment_amount"
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
"gift_wrap_amount"
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
"tax_percentage"
:
"string"
,
"basic_shipping_amount"
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
"extra_shipping_amount"
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
"handling_amount"
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
"insurance_amount"
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
"total_item_amount"
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
]
,
"tax_inclusive"
:
false
,
"paypal_invoice_id"
:
"string"
}
Checkout Option
A checkout option as a name-and-value pair.
checkout_option_name
string
[ 1 .. 200 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The checkout option name, such as
color
or
texture
.
checkout_option_value
string
[ 1 .. 200 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The checkout option value. For example, the checkout option
color
might be
blue
or
red
while the checkout option
texture
might be
smooth
or
rippled
.
Copy
{
"checkout_option_name"
:
"string"
,
"checkout_option_value"
:
"string"
}
country_code
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
<
ppaas_common_country_code_v2
>
(
country_code
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
Currency Level Activity Details
The currency level activity details.
net_activity_sum
string
[ 1 .. 32 ] characters
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The gross payment amount at currency level.
fee_sum
string
[ 1 .. 32 ] characters
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The gross fee amount at currency level.
activity_details
Array of
strings
[ 1 .. 2147483647 ] items
An array containing array of strings depicting accounting details (activity, count, and amount) for each record types.
Copy
Expand all
Collapse all
{
"net_activity_sum"
:
"string"
,
"fee_sum"
:
"string"
,
"activity_details"
:
[
[
"string"
]
]
}
currency_code
The
three-character ISO-4217 currency code
that identifies the currency.
string
<
ppaas_common_currency_code_v2
>
(
currency_code
)
= 3 characters
The
three-character ISO-4217 currency code
that identifies the currency.
Copy
"str"
currency_code
The
3-character ISO-4217 currency code
that identifies the currency.
string
<
ppaas_common_currency_code_v2
>
(
currency_code
)
= 3 characters
The
3-character ISO-4217 currency code
that identifies the currency.
Copy
"str"
Daily Summary
The date wise accounting summary details.
currencies
Array of
strings
[ 1 .. 2147483647 ] items
An array of currency.
summaries
Array of
objects
(
Daily Summary Details
)
[ 1 .. 2147483647 ] items
An array of currency wise daily summary.
Copy
Expand all
Collapse all
{
"currencies"
:
[
"string"
]
,
"summaries"
:
[
{
"activity"
:
[
"string"
]
,
"data"
:
[
[
"string"
]
]
}
]
}
Daily Summary Details
The currency wise daily summary data.
activity
Array of
strings
[ 1 .. 2147483647 ] items
An array of record types for each currency.
data
Array of
strings
[ 1 .. 2147483647 ] items
An array containing array of strings depicting daily summaries data for a currency.
Copy
Expand all
Collapse all
{
"activity"
:
[
"string"
]
,
"data"
:
[
[
"string"
]
]
}
date_no_time
The stand-alone date, in
Internet date and time format
. To represent special legal values, such as a date of birth, you should use dates with no associated time or time-zone data. Whenever possible, use the standard
date_time
type. This regular expression does not validate all dates. For example, February 31 is valid and nothing is known about leap years.
string
<
ppaas_date_notime_v2
>
(
date_no_time
)
= 10 characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The stand-alone date, in
Internet date and time format
. To represent special legal values, such as a date of birth, you should use dates with no associated time or time-zone data. Whenever possible, use the standard
date_time
type. This regular expression does not validate all dates. For example, February 31 is valid and nothing is known about leap years.
Copy
"stringstri"
date_time
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
string
<
ppaas_date_time_v3
>
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
email_address
The internationalized email address.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
string
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 3 .. 254 ] characters
^.+@[^"\-].+$
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
The human-readable, unique name of the error.
message
required
string
The message that describes the error.
debug_id
required
string
The PayPal internal ID. Used for correlation purposes.
information_link
string
The information link, or URI, that shows detailed information about this error for the developer.
details
Array of
objects
(
Error Details
)
An array of additional details about the error.
links
Array of
objects
(
Link Description
)
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
"information_link"
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
}
]
}
Error
The error details.
name
required
string
The human-readable, unique name of the error.
message
required
string
The message that describes the error.
debug_id
required
string
The PayPal internal ID. Used for correlation purposes.
information_link
string
The information link, or URI, that shows detailed information about this error for the developer.
details
Array of
objects
(
Error Details
)
An array of additional details about the error.
links
Array of
objects
(
Link Description
)
An array of request-related
HATEOAS links
.
total_items
integer
[ 0 .. 2147483647 ]
The total number of transactions. Valid only for
RESULTSET_TOO_LARGE
.
maximum_items
integer
[ 0 .. 2147483647 ]
The maximum number of transactions. Valid only for
RESULTSET_TOO_LARGE
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
"information_link"
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
}
]
,
"total_items"
:
2147483647
,
"maximum_items"
:
2147483647
}
Error
The error details.
name
required
string
The human-readable, unique name of the error.
message
required
string
The message that describes the error.
debug_id
required
string
The PayPal internal ID. Used for correlation purposes.
information_link
string
The information link, or URI, that shows detailed information about this error for the developer.
details
Array of
objects
(
Error Details
)
An array of additional details about the error.
links
Array of
objects
(
Link Description
)
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
"information_link"
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
}
]
}
Error Details
The error details. Required for client-side
4XX
errors.
field
string
The field that caused the error. If this field is in the body, set this value to the field's JSON pointer value. Required for client-side errors.
value
string
The value of the field that caused the error.
location
string
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
The unique, fine-grained application-level error code.
description
string
The human-readable description for an issue. The description can change over the lifetime of an API, so clients must not depend on this value.
Copy
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
"description"
:
"string"
}
Error Details
The error details. Required for client-side
4XX
errors.
field
string
The field that caused the error. If this field is in the body, set this value to the field's JSON pointer value. Required for client-side errors.
value
string
The value of the field that caused the error.
location
string
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
The unique, fine-grained application-level error code.
description
string
The human-readable description for an issue. The description can change over the lifetime of an API, so clients must not depend on this value.
Copy
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
"description"
:
"string"
}
Incentive Details
The incentive details.
incentive_type
string
[ 1 .. 500 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The type of incentive, such as a special offer or coupon.
incentive_code
string
[ 1 .. 200 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The code that identifies an incentive, such as a coupon.
incentive_program_code
string
[ 1 .. 100 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The incentive program code that identifies a merchant loyalty or incentive program.
incentive_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"incentive_type"
:
"string"
,
"incentive_code"
:
"string"
,
"incentive_program_code"
:
"string"
,
"incentive_amount"
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
Incentive Information
The incentive details.
incentive_details
Array of
objects
(
Incentive Details
)
[ 1 .. 32767 ] items
An array of incentive details.
Copy
Expand all
Collapse all
{
"incentive_details"
:
[
{
"incentive_type"
:
"string"
,
"incentive_code"
:
"string"
,
"incentive_program_code"
:
"string"
,
"incentive_amount"
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
]
}
Item Details
The item details.
item_code
string
[ 1 .. 1000 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
An item code that identifies a merchant's goods or service.
item_name
string
[ 1 .. 200 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The item name.
item_description
string
[ 1 .. 2000 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The item description.
item_options
string
[ 1 .. 4000 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The item options. Describes option choices on the purchase of the item in some detail.
item_quantity
string
[ 1 .. 4000 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The number of purchased units of goods or a service.
tax_amounts
Array of
objects
(
Tax Amount
)
[ 1 .. 32767 ] items
An array of tax amounts levied by a government on the purchase of goods or services.
invoice_number
string
[ 1 .. 200 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The invoice number. An alphanumeric string that identifies a billing for a merchant.
checkout_options
Array of
objects
(
Checkout Option
)
[ 1 .. 32767 ] items
An array of checkout options. Each option has a name and value.
item_unit_price
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
item_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
discount_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
adjustment_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
gift_wrap_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
tax_percentage
string
<
ppaas_common_percentage_v2
>
(
percentage
)
<= 10 characters
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The percentage, as a fixed-point, signed decimal number. For example, define a 19.99% interest rate as
19.99
.
basic_shipping_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
extra_shipping_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
handling_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
insurance_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
total_item_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"item_code"
:
"string"
,
"item_name"
:
"string"
,
"item_description"
:
"string"
,
"item_options"
:
"string"
,
"item_quantity"
:
"string"
,
"tax_amounts"
:
[
{
"tax_amount"
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
]
,
"invoice_number"
:
"string"
,
"checkout_options"
:
[
{
"checkout_option_name"
:
"string"
,
"checkout_option_value"
:
"string"
}
]
,
"item_unit_price"
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
"item_amount"
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
"discount_amount"
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
"adjustment_amount"
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
"gift_wrap_amount"
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
"tax_percentage"
:
"string"
,
"basic_shipping_amount"
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
"extra_shipping_amount"
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
"handling_amount"
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
"insurance_amount"
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
"total_item_amount"
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
Link Description
The request-related
HATEOAS link
information.
href
required
string
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
The
link relation type
, which serves as an ID for a link that unambiguously describes the semantics of the link. See
Link Relations
.
method
string
The HTTP method required to make the related call.
Enum
:
"GET"
"POST"
"PUT"
"DELETE"
"HEAD"
"CONNECT"
"OPTIONS"
"PATCH"
Copy
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
}
Link Description
The request-related
HATEOAS link
information.
href
required
string
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
The
link relation type
, which serves as an ID for a link that unambiguously describes the semantics of the link. See
Link Relations
.
method
string
The HTTP method required to make the related call.
Enum
:
"GET"
"POST"
"PUT"
"DELETE"
"HEAD"
"CONNECT"
"OPTIONS"
"PATCH"
Copy
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
}
Money
The currency and amount for a financial transaction, such as a balance or payment due.
currency_code
required
string
<
ppaas_common_currency_code_v2
>
(
currency_code
)
= 3 characters
The
three-character ISO-4217 currency code
that identifies the currency.
value
required
string
<= 32 characters
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
Money
The currency and amount for a financial transaction, such as a balance or payment due.
currency_code
required
string
<
ppaas_common_currency_code_v2
>
(
currency_code
)
= 3 characters
The
3-character ISO-4217 currency code
that identifies the currency.
value
required
string
<= 32 characters
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
Name
The name of the party.
prefix
string
<= 140 characters
The prefix, or title, to the party's name.
given_name
string
<= 140 characters
When the party is a person, the party's given, or first, name.
surname
string
<= 140 characters
When the party is a person, the party's surname or family name. Also known as the last name. Required when the party is a person. Use also to store multiple surnames including the matronymic, or mother's, surname.
middle_name
string
<= 140 characters
When the party is a person, the party's middle name. Use also to store multiple middle names including the patronymic, or father's, middle name.
suffix
string
<= 140 characters
The suffix for the party's name.
alternate_full_name
string
<= 300 characters
DEPRECATED. The party's alternate name. Can be a business name, nickname, or any other name that cannot be split into first, last name. Required when the party is a business.
full_name
string
<= 300 characters
When the party is a person, the party's full name.
Copy
{
"prefix"
:
"string"
,
"given_name"
:
"string"
,
"surname"
:
"string"
,
"middle_name"
:
"string"
,
"suffix"
:
"string"
,
"alternate_full_name"
:
"string"
,
"full_name"
:
"string"
}
Net Activity Details
The net activity details for all currencies.
currencies
Array of
strings
[ 1 .. 2147483647 ] items
An array of currency.
columns
Array of
strings
[ 1 .. 2147483647 ] items
An array of activity details column.
activities
Array of
objects
(
Currency Level Activity Details
)
[ 1 .. 2147483647 ] items
An array of containing net-activity, fee and record-type values.
Copy
Expand all
Collapse all
{
"currencies"
:
[
"string"
]
,
"columns"
:
[
"string"
]
,
"activities"
:
[
{
"net_activity_sum"
:
"string"
,
"fee_sum"
:
"string"
,
"activity_details"
:
[
[
"string"
]
]
}
]
}
Payer Information
The payer information.
account_id
string
[ 1 .. 13 ] characters
^[a-zA-Z0-9_]*$
The PayPal` customer account ID.
address_status
string
= 1 characters
^[N|Y]$
The address status of the payer. Value is either:
Y
. Verified.
N
. Not verified.
payer_status
string
= 1 characters
^[N|Y]$
The status of the payer. Value is
Y
or
N
.
email_address
string
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 3 .. 254 ] characters
^.+@[^"\-].+$
The email address of the payer.
phone_number
object
(
Phone
)
The primary phone number of the payer.
payer_name
object
(
Name
)
The payer name.
country_code
string
<
ppaas_common_country_code_v2
>
(
country_code
)
= 2 characters
^([A-Z]{2}|C2)$
The
two-character ISO 3166-1 code
that identifies the country or region of the payer.
Note:
The country code for Great Britain is
GB
and not
UK
as used in the top-level domain names for that country. Use the
C2
country code for China worldwide for comparable uncontrolled price (CUP) method, bank card, and cross-border transactions.
address
object
(
Simple Postal Address (Coarse-Grained)
)
The payer address.
Copy
Expand all
Collapse all
{
"account_id"
:
"string"
,
"address_status"
:
"s"
,
"payer_status"
:
"s"
,
"email_address"
:
"string"
,
"phone_number"
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
,
"payer_name"
:
{
"prefix"
:
"string"
,
"given_name"
:
"string"
,
"surname"
:
"string"
,
"middle_name"
:
"string"
,
"suffix"
:
"string"
,
"alternate_full_name"
:
"string"
,
"full_name"
:
"string"
}
,
"country_code"
:
"st"
,
"address"
:
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
}
percentage
The percentage, as a fixed-point, signed decimal number. For example, define a 19.99% interest rate as
19.99
.
string
<
ppaas_common_percentage_v2
>
(
percentage
)
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The percentage, as a fixed-point, signed decimal number. For example, define a 19.99% interest rate as
19.99
.
Copy
"string"
Phone
The phone number, in its canonical international
E.164 numbering plan format
.
country_code
required
string
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
Search Response
The search response information.
transaction_details
Array of
objects
(
Transaction Details
)
[ 1 .. 500 ] items
An array of transaction detail objects.
account_number
string
[ 1 .. 255 ] characters
^[a-zA-Z0-9]*$
The merchant account number.
page
integer
[ 0 .. 2147483647 ]
A zero-relative index of transactions.
total_items
integer
[ 0 .. 2147483647 ]
The total number of transactions as an integer beginning with the specified
page
in the full result and not just in this response.
total_pages
integer
[ 0 .. 2147483647 ]
The total number of pages, as an
integer
, when the
total_items
is divided into pages of the specified
page_size
.
links
Array of
objects
(
Link Description
)
[ 1 .. 32767 ] items
An array of request-related
HATEOAS links
.
start_date
string
<
ppaas_date_time_v3
>
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
end_date
string
<
ppaas_date_time_v3
>
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
last_refreshed_datetime
string
<
ppaas_date_time_v3
>
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
"transaction_details"
:
[
{
"transaction_info"
:
{
"paypal_account_id"
:
"string"
,
"transaction_id"
:
"string"
,
"paypal_reference_id"
:
"string"
,
"paypal_reference_id_type"
:
"ODR"
,
"transaction_event_code"
:
"strin"
,
"transaction_status"
:
"s"
,
"transaction_subject"
:
"string"
,
"transaction_note"
:
"string"
,
"payment_tracking_id"
:
"string"
,
"bank_reference_id"
:
"string"
,
"invoice_id"
:
"string"
,
"custom_field"
:
"string"
,
"protection_eligibility"
:
"st"
,
"credit_term"
:
"string"
,
"payment_method_type"
:
"string"
,
"instrument_type"
:
"string"
,
"instrument_sub_type"
:
"string"
,
"decline_code"
:
"string"
,
"transaction_initiation_date"
:
"string"
,
"transaction_updated_date"
:
"string"
,
"transaction_amount"
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
"fee_amount"
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
"discount_amount"
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
"insurance_amount"
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
"sales_tax_amount"
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
"shipping_amount"
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
"shipping_discount_amount"
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
"shipping_tax_amount"
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
"other_amount"
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
"tip_amount"
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
"ending_balance"
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
"available_balance"
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
"credit_transactional_fee"
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
"credit_promotional_fee"
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
"annual_percentage_rate"
:
"string"
}
,
"payer_info"
:
{
"account_id"
:
"string"
,
"address_status"
:
"s"
,
"payer_status"
:
"s"
,
"email_address"
:
"string"
,
"phone_number"
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
,
"payer_name"
:
{
"prefix"
:
"string"
,
"given_name"
:
"string"
,
"surname"
:
"string"
,
"middle_name"
:
"string"
,
"suffix"
:
"string"
,
"alternate_full_name"
:
"string"
,
"full_name"
:
"string"
}
,
"country_code"
:
"st"
,
"address"
:
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
}
,
"shipping_info"
:
{
"name"
:
"string"
,
"method"
:
"string"
,
"address"
:
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
,
"secondary_shipping_address"
:
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
}
,
"cart_info"
:
{
"item_details"
:
[
{
"item_code"
:
"string"
,
"item_name"
:
"string"
,
"item_description"
:
"string"
,
"item_options"
:
"string"
,
"item_quantity"
:
"string"
,
"tax_amounts"
:
[
{
"tax_amount"
:
null
}
]
,
"invoice_number"
:
"string"
,
"checkout_options"
:
[
{
"checkout_option_name"
:
null
,
"checkout_option_value"
:
null
}
]
,
"item_unit_price"
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
"item_amount"
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
"discount_amount"
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
"adjustment_amount"
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
"gift_wrap_amount"
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
"tax_percentage"
:
"string"
,
"basic_shipping_amount"
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
"extra_shipping_amount"
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
"handling_amount"
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
"insurance_amount"
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
"total_item_amount"
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
]
,
"tax_inclusive"
:
false
,
"paypal_invoice_id"
:
"string"
}
,
"store_info"
:
{
"store_id"
:
"string"
,
"terminal_id"
:
"string"
}
,
"auction_info"
:
{
"auction_site"
:
"string"
,
"auction_item_site"
:
"
http://example.com
"
,
"auction_buyer_id"
:
"string"
,
"auction_closing_date"
:
"string"
}
,
"incentive_info"
:
{
"incentive_details"
:
[
{
"incentive_type"
:
"string"
,
"incentive_code"
:
"string"
,
"incentive_program_code"
:
"string"
,
"incentive_amount"
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
]
}
}
]
,
"account_number"
:
"string"
,
"page"
:
2147483647
,
"total_items"
:
2147483647
,
"total_pages"
:
2147483647
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
}
]
,
"start_date"
:
"string"
,
"end_date"
:
"string"
,
"last_refreshed_datetime"
:
"string"
}
Shipping Information
The shipping information.
name
string
[ 1 .. 500 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The recipient's name.
method
string
[ 1 .. 500 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The shipping method that is associated with this order.
address
object
(
Simple Postal Address (Coarse-Grained)
)
A simple postal address with coarse-grained fields. Do not use for an international address. Use for backward compatibility only. Does not contain phone.
secondary_shipping_address
object
(
Simple Postal Address (Coarse-Grained)
)
A simple postal address with coarse-grained fields. Do not use for an international address. Use for backward compatibility only. Does not contain phone.
Copy
Expand all
Collapse all
{
"name"
:
"string"
,
"method"
:
"string"
,
"address"
:
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
,
"secondary_shipping_address"
:
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
}
Simple Postal Address (Coarse-Grained)
A simple postal address with coarse-grained fields. Do not use for an international address. Use for backward compatibility only. Does not contain phone.
line1
required
string
The first line of the address. For example, number or street.
line2
string
The second line of the address. For example, suite or apartment number.
city
required
string
The city name.
state
string
The
code
for a US state or the equivalent for other countries. Required for transactions if the address is in one of these countries:
Argentina
,
Brazil
,
Canada
,
China
,
India
,
Italy
,
Japan
,
Mexico
,
Thailand
, or
United States
. Maximum length is 40 single-byte characters.
country_code
required
string
<
ppaas_common_country_code_v2
>
(
country_code
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
postal_code
string
The postal code, which is the zip code or equivalent. Typically required for countries with a postal code or an equivalent. See
postal code
.
Copy
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
Store Information
The store information.
store_id
string
[ 1 .. 100 ] characters
^[a-zA-Z0-9_'\-., ":;!?]*$
The ID of a store for a merchant in the system of record.
terminal_id
string
[ 1 .. 60 ] characters
^[a-zA-Z0-9_'\-., ":;!?]*$
The terminal ID for the checkout stand in a merchant store. For example, 45678,FPTestStore1.
Copy
{
"store_id"
:
"string"
,
"terminal_id"
:
"string"
}
Tax Amount
The tax levied by a government on the purchase of goods or services.
tax_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"tax_amount"
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
Transaction Details
The transaction details.
transaction_info
object
(
Transaction Information
)
The transaction information.
payer_info
object
(
Payer Information
)
The payer information.
shipping_info
object
(
Shipping Information
)
The shipping information.
cart_info
object
(
Cart Information
)
The cart information.
store_info
object
(
Store Information
)
The store information.
auction_info
object
(
Auction Information
)
The auction information.
incentive_info
object
(
Incentive Information
)
The incentive details.
Copy
Expand all
Collapse all
{
"transaction_info"
:
{
"paypal_account_id"
:
"string"
,
"transaction_id"
:
"string"
,
"paypal_reference_id"
:
"string"
,
"paypal_reference_id_type"
:
"ODR"
,
"transaction_event_code"
:
"strin"
,
"transaction_status"
:
"s"
,
"transaction_subject"
:
"string"
,
"transaction_note"
:
"string"
,
"payment_tracking_id"
:
"string"
,
"bank_reference_id"
:
"string"
,
"invoice_id"
:
"string"
,
"custom_field"
:
"string"
,
"protection_eligibility"
:
"st"
,
"credit_term"
:
"string"
,
"payment_method_type"
:
"string"
,
"instrument_type"
:
"string"
,
"instrument_sub_type"
:
"string"
,
"decline_code"
:
"string"
,
"transaction_initiation_date"
:
"string"
,
"transaction_updated_date"
:
"string"
,
"transaction_amount"
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
"fee_amount"
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
"discount_amount"
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
"insurance_amount"
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
"sales_tax_amount"
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
"shipping_amount"
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
"shipping_discount_amount"
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
"shipping_tax_amount"
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
"other_amount"
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
"tip_amount"
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
"ending_balance"
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
"available_balance"
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
"credit_transactional_fee"
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
"credit_promotional_fee"
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
"annual_percentage_rate"
:
"string"
}
,
"payer_info"
:
{
"account_id"
:
"string"
,
"address_status"
:
"s"
,
"payer_status"
:
"s"
,
"email_address"
:
"string"
,
"phone_number"
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
,
"payer_name"
:
{
"prefix"
:
"string"
,
"given_name"
:
"string"
,
"surname"
:
"string"
,
"middle_name"
:
"string"
,
"suffix"
:
"string"
,
"alternate_full_name"
:
"string"
,
"full_name"
:
"string"
}
,
"country_code"
:
"st"
,
"address"
:
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
}
,
"shipping_info"
:
{
"name"
:
"string"
,
"method"
:
"string"
,
"address"
:
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
,
"secondary_shipping_address"
:
{
"line1"
:
"string"
,
"line2"
:
"string"
,
"city"
:
"string"
,
"state"
:
"string"
,
"country_code"
:
"st"
,
"postal_code"
:
"string"
}
}
,
"cart_info"
:
{
"item_details"
:
[
{
"item_code"
:
"string"
,
"item_name"
:
"string"
,
"item_description"
:
"string"
,
"item_options"
:
"string"
,
"item_quantity"
:
"string"
,
"tax_amounts"
:
[
{
"tax_amount"
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
]
,
"invoice_number"
:
"string"
,
"checkout_options"
:
[
{
"checkout_option_name"
:
"string"
,
"checkout_option_value"
:
"string"
}
]
,
"item_unit_price"
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
"item_amount"
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
"discount_amount"
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
"adjustment_amount"
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
"gift_wrap_amount"
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
"tax_percentage"
:
"string"
,
"basic_shipping_amount"
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
"extra_shipping_amount"
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
"handling_amount"
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
"insurance_amount"
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
"total_item_amount"
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
]
,
"tax_inclusive"
:
false
,
"paypal_invoice_id"
:
"string"
}
,
"store_info"
:
{
"store_id"
:
"string"
,
"terminal_id"
:
"string"
}
,
"auction_info"
:
{
"auction_site"
:
"string"
,
"auction_item_site"
:
"
http://example.com
"
,
"auction_buyer_id"
:
"string"
,
"auction_closing_date"
:
"string"
}
,
"incentive_info"
:
{
"incentive_details"
:
[
{
"incentive_type"
:
"string"
,
"incentive_code"
:
"string"
,
"incentive_program_code"
:
"string"
,
"incentive_amount"
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
]
}
}
Transaction Information
The transaction information.
paypal_account_id
string
[ 1 .. 24 ] characters
^[a-zA-Z0-9_]*$
The ID of the PayPal account of the counterparty.
transaction_id
string
[ 1 .. 24 ] characters
^[a-zA-Z0-9_]*$
The PayPal-generated transaction ID.
paypal_reference_id
string
[ 1 .. 24 ] characters
^[a-zA-Z0-9_-]*$
The PayPal-generated base ID. PayPal exclusive. Cannot be altered. Defined as a related, pre-existing transaction or event.
paypal_reference_id_type
string
= 3 characters
^[a-zA-Z0-9]*$
The PayPal reference ID type.
Enum Value
Description
ODR
An order ID.
TXN
A transaction ID.
SUB
A subscription ID.
PAP
A pre-approved payment ID.
transaction_event_code
string
[ 1 .. 5 ] characters
^[a-zA-Z0-9]*$
A five-digit transaction event code that classifies the transaction type based on money movement and debit or credit. For example,
T0001
. See
Transaction event codes
.
transaction_status
string
= 1 characters
^[a-zA-Z0-9]*$
A code that indicates the transaction status. Value is:
Status code
Description
D
PayPal or merchant rules denied the transaction.
P
The transaction is pending. The transaction was created but waits for another payment process to complete, such as an ACH transaction, before the status changes to
S
.
S
The transaction successfully completed without a denial and after any pending statuses.
V
A successful transaction was fully reversed and funds were refunded to the original sender.
transaction_subject
string
[ 1 .. 256 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The subject of payment. The payer passes this value to the payee. The payer controls this data through the interface through which he or she sends the data.
transaction_note
string
[ 1 .. 4000 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
A special note that the payer passes to the payee. Might contain special customer requests, such as shipping instructions.
payment_tracking_id
string
[ 1 .. 127 ] characters
^[a-zA-Z0-9_]*$
The payment tracking ID, which is a unique ID that partners specify to either get information about a payment or request a refund.
bank_reference_id
string
[ 1 .. 127 ] characters
^[a-zA-Z0-9_]*$
The bank reference ID. The bank provides this value for an ACH transaction.
invoice_id
string
[ 1 .. 127 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
The invoice ID that is sent by the merchant with the transaction.
Note:
If an invoice ID was sent with the capture request, the value is reported. Otherwise, the invoice ID of the authorizing transaction is reported.
custom_field
string
[ 1 .. 127 ] characters
^[a-zA-Z0-9_'\-., ":;!?|]*$
The merchant-provided custom text.
Note:
Usually, this field includes the unique ID for payments made with MassPay type transaction.
protection_eligibility
string
[ 1 .. 2 ] characters
^[a-zA-Z0-9]*$
Indicates whether the transaction is eligible for protection. Value is:
01
. Eligible.
02
. Not eligible
03
. Partially eligible.
credit_term
string
[ 1 .. 25 ] characters
^[a-zA-Z0-9.]*$
The credit term. The time span covered by the installment payments as expressed in the term length plus the length time unit code.
payment_method_type
string
[ 1 .. 20 ] characters
^[a-zA-Z0-9-]*$
The payment method that was used for a transaction. Value is
PUI
,
installment
, or
mEFT
.
Note:
Appears only for pay upon invoice (PUI), installment, and mEFT transactions. Merchants and partners in the EMEA region can use this attribute to note transactions that attract turn-over tax.
instrument_type
string
[ 1 .. 64 ] characters
^[a-zA-Z0-9-]*$
A high-level classification of the type of financial instrument that was used to fund a payment. The pattern is not provided because the value is defined by an external party. E.g. PayPal, Credit Card, Debit Card, Venmo or
Alternative Payment Methods (APM)
.
instrument_sub_type
string
[ 1 .. 64 ] characters
A finer-grained classification of the financial instrument that was used to fund a payment. For example,
PayPal wallet
for PayPal,
American Express
for a credit card,
Visa
for a Debit Card,
Venmo Wallet
for Venmo,  etc. The pattern is not provided because the value is defined by an external party.
decline_code
string
[ 1 .. 50 ] characters
^[a-zA-Z0-9_'\-., ":;\!?]*$
UDD SEPA Payment Type external decline codes. Value is defined by an external party.
UDD SEPA Decline Code
.
transaction_initiation_date
string
<
ppaas_date_time_v3
>
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
transaction_updated_date
string
<
ppaas_date_time_v3
>
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
transaction_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
fee_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
discount_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
insurance_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
sales_tax_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
shipping_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
shipping_discount_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
shipping_tax_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
other_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
tip_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
ending_balance
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
available_balance
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
credit_transactional_fee
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
credit_promotional_fee
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
annual_percentage_rate
string
<
ppaas_common_percentage_v2
>
(
percentage
)
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The percentage, as a fixed-point, signed decimal number. For example, define a 19.99% interest rate as
19.99
.
Copy
Expand all
Collapse all
{
"paypal_account_id"
:
"string"
,
"transaction_id"
:
"string"
,
"paypal_reference_id"
:
"string"
,
"paypal_reference_id_type"
:
"ODR"
,
"transaction_event_code"
:
"strin"
,
"transaction_status"
:
"s"
,
"transaction_subject"
:
"string"
,
"transaction_note"
:
"string"
,
"payment_tracking_id"
:
"string"
,
"bank_reference_id"
:
"string"
,
"invoice_id"
:
"string"
,
"custom_field"
:
"string"
,
"protection_eligibility"
:
"st"
,
"credit_term"
:
"string"
,
"payment_method_type"
:
"string"
,
"instrument_type"
:
"string"
,
"instrument_sub_type"
:
"string"
,
"decline_code"
:
"string"
,
"transaction_initiation_date"
:
"string"
,
"transaction_updated_date"
:
"string"
,
"transaction_amount"
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
"fee_amount"
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
"discount_amount"
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
"insurance_amount"
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
"sales_tax_amount"
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
"shipping_amount"
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
"shipping_discount_amount"
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
"shipping_tax_amount"
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
"other_amount"
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
"tip_amount"
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
"ending_balance"
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
"available_balance"
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
"credit_transactional_fee"
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
"credit_promotional_fee"
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
"annual_percentage_rate"
:
"string"
}
