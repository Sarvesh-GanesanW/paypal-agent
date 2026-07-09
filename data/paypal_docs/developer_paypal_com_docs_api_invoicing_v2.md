# Invoices

Source: https://developer.paypal.com/docs/api/invoicing/v2/

Invoices
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
Invoices
post
Create draft invoice
get
List invoices
post
Send invoice
get
Show invoice details
put
Fully update invoice
delete
Delete invoice
post
Search for invoices
post
Cancel sent invoice
post
Send invoice reminder
post
Record payment for invoice
delete
Delete external payment
post
Record refund for invoice
delete
Delete external refund
post
Generate invoice number
post
Generate QR code
get
List templates
post
Create template
get
Show template details
put
Fully update template
delete
Delete template
post
Setup auto reminder configuration.
get
Retrieve an invoice auto reminder configuration
put
Update invoice auto reminder configuration.
get
Get all invoice auto reminder configuration.
post
Suspend invoice auto reminder configuration.
post
Resume invoice auto reminder configuration.
post
Cancel auto reminders for an invoice.
post
Create a recurring invoice series
get
Get recurring invoice series details
put
Update recurring invoice series details
delete
Delete recurring invoice series
post
Activate recurring invoice series
post
Cancel an active recurring invoice series
post
Search recurring invoice series
get
List conditional rules for invoice
post
Create conditional rules
get
Show conditional rule details
put
Fully update conditional rule
delete
Delete conditional rule
Definitions
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
Invoices
(
2
)
API Version v2
?
This API is currently not supported by our SDK
License:
PayPal APIs
Use the Invoicing API to create, send, and manage invoices. You can also use the API or webhooks to track invoice payments. When you send an invoice to a customer, the invoice moves from draft to payable state. PayPal then emails the customer a link to the invoice on the PayPal website. Customers with a PayPal account can log in and pay the invoice with PayPal. Alternatively, customers can pay as a guest with a debit card or credit card. For more information, see the
Invoicing Overview
and the
Invoicing Integration Guide
.
Create draft invoice
post
/v2/invoicing/invoices
Try it
Creates a draft invoice. To move the invoice from a draft to payable state, you must
send the invoice
.
In the JSON request body, include invoice details including merchant information. The
invoice
object must include an
items
array.
Note:
The merchant that you specify in an invoice must have a PayPal account in good standing.
.
Security
Oauth2
Request
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
required
The invoice details which includes all information of the invoice like items, billing information.
primary_recipients
Array of
objects
(
recipient_info
)
[ 0 .. 100 ] items
The billing and shipping information. Includes name, email, address, phone and language.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 0 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
items
Array of
objects
(
item
)
[ 0 .. 100 ] items
An array of invoice line item information.
detail
required
object
(
invoice_detail
)
The details of the invoice. Includes invoice number, date, payment terms, and audit metadata.
invoicer
object
(
invoicer_info
)
The invoicer business information that appears on the invoice.
configuration
object
(
configuration
)
The invoice configuration details. Includes partial payment, tip, and tax calculated after discount.
amount
object
(
amount_summary_detail
)
The invoice amount summary of item total, discount, tax total, and shipping.
settings
object
(
invoice_settings
)
The settings for the invoice.
payments
object
(
payments
)
An array of payments registered against the invoice.
effective_invoice_total
object
(
Money
)
The effective total amount of the invoice after applying conditional rules. The conditional rules include early payment discount, late payment surcharge, and auto cancellation details.
effective_due_amount
object
(
Money
)
The effective due amount of the invoice after applying conditional rules. The conditional rules include early payment discount, late payment surcharge, and auto cancellation details.
refunds
object
(
refunds
)
The invoicing refund details. Includes the refund type, date, amount, and method.
Responses
201
A successful request returns the HTTP
201 Created
status code. A JSON response body that shows invoice details is returned if you set
prefer=return=representation
.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 201 - Create Invoice with Theme
Sample 1 - 201 - Create Invoice with Theme
Copy
Expand all
Collapse all
{
"detail"
:
{
"reference"
:
"deal-ref"
,
"invoice_date"
:
"2025-01-15"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"term"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"payment_term"
:
{
"term_type"
:
"NET_10"
,
"due_date"
:
"2025-01-25"
}
,
"order_details"
:
"Order #12345 placed on January 10, 2025."
,
"project_details"
:
"Website redesign project for client XYZ Corp."
,
"service_details"
:
"Consulting services provided from Jan-Mar 2025."
,
"cancellation_policy"
:
"Services may be cancelled with 14-day notice."
,
"payment_terms"
:
"Payment due within 10 days of invoice date."
,
"return_policy"
:
"All sales are final. No returns accepted after 30 days."
,
"service_agreement"
:
"Services provided as per agreement dated Jan 1, 2025."
,
"tip_presets"
:
[
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
,
{
"percent"
:
"25"
}
]
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"www.test.com"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy- Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"HOME"
}
]
,
"additional_info_value"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"items"
:
[
{
"name"
:
"Yoga Mat"
,
"description"
:
"Elastic mat to practice yoga."
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
}
,
"discount"
:
{
"percent"
:
"5"
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"name"
:
"Yoga t-shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
,
"tax_note"
:
"Reduced tax rate"
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"allow_tip"
:
true
,
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"show_additional_item_fields"
:
true
,
"template_id"
:
"TEMP-19V05281TU309413B"
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
,
"amount"
:
{
"breakdown"
:
{
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
}
}
,
"discount"
:
{
"invoice_discount"
:
{
"percent"
:
"5"
}
}
}
}
,
"settings"
:
{
"invoice_item_settings"
:
[
{
"field_name"
:
"ITEM_DESCRIPTION"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DATE"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"ITEM_TAX"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DISCOUNT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"invoice_additional_settings"
:
[
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"MEMO"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"REFERENCE"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"invoice_policy_and_agreement_settings"
:
[
{
"field_name"
:
"TERMS_AND_CONDITIONS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"PAYMENT_TERMS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"PROJECT_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
}
}
Response samples
201
application/json
multipart/mixed
application/json
Sample 1 - 201 - Create Invoice with Theme
Sample 1 - 201 - Create Invoice with Theme
Copy
Expand all
Collapse all
{
"id"
:
"INV2-Z56S-5LLA-Q52L-CPZ5"
,
"status"
:
"DRAFT"
,
"detail"
:
{
"reference"
:
"deal-ref"
,
"invoice_date"
:
"2025-01-15"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"term"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"payment_term"
:
{
"term_type"
:
"NET_10"
,
"due_date"
:
"2025-01-25"
}
,
"order_details"
:
"Order #12345 placed on January 10, 2025."
,
"project_details"
:
"Website redesign project for client XYZ Corp."
,
"service_details"
:
"Consulting services provided from Jan-Mar 2025."
,
"cancellation_policy"
:
"Services may be cancelled with 14-day notice."
,
"payment_terms"
:
"Payment due within 10 days of invoice date."
,
"return_policy"
:
"All sales are final. No returns accepted after 30 days."
,
"service_agreement"
:
"Services provided as per agreement dated Jan 1, 2025."
,
"tip_presets"
:
[
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
,
{
"percent"
:
"25"
}
]
,
"metadata"
:
{
"create_time"
:
"2025-01-15T08:00:20Z"
,
"recipient_view_url"
:
"
https://www.api-m.paypal.com/invoice/p#Z56S5LLAQ52LCPZ5
"
,
"invoicer_view_url"
:
"
https://www.api-m.paypal.com/invoice/details/INV2-Z56S-5LLA-Q52L-CPZ5
"
}
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"
https://example.com
"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"HOME"
}
]
,
"additional_info_value"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"items"
:
[
{
"name"
:
"Yoga Mat"
,
"description"
:
"Elastic mat to practice yoga."
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"3.27"
,
"tax_note"
:
"Reduced tax rate"
}
}
,
"discount"
:
{
"percent"
:
"5"
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
"2.5"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"name"
:
"Yoga T Shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.34"
,
"tax_note"
:
"Reduced tax rate"
}
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"allow_tip"
:
true
,
"allow_only_pay_by_bank"
:
true
,
"tax_calculated_after_discount"
:
true
,
"show_additional_item_fields"
:
true
,
"tax_inclusive"
:
false
,
"template_id"
:
"TEMP-19V05281TU309413B"
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
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
"74.21"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"60.00"
}
,
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.73"
,
"tax_note"
:
"Reduced tax rate"
}
}
}
,
"discount"
:
{
"item_discount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"-7.50"
}
,
"invoice_discount"
:
{
"percent"
:
"5"
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
"-2.63"
}
}
}
,
"tax_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"4.34"
}
}
}
,
"due_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"74.21"
}
,
"settings"
:
{
"invoice_item_settings"
:
[
{
"field_name"
:
"ITEM_DESCRIPTION"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DATE"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"ITEM_TAX"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DISCOUNT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/send
"
,
"rel"
:
"send"
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/update
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/payments
"
,
"rel"
:
"record-payment"
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/generate-qr-code
"
,
"rel"
:
"qr-code"
,
"method"
:
"POST"
}
]
}
List invoices
get
/v2/invoicing/invoices
Try it
Lists invoices. To filter the invoices that appear in the response, you can specify one or more optional query parameters.
Security
Oauth2
Request
query
Parameters
page
integer
[ 1 .. 1000 ]
Default:
1
The page number to be retrieved, for the list of items. So, a combination of
page=1
and
page_size=20
returns the first 20 invoices. A combination of
page=2
and
page_size=20
returns the next 20 invoices.
page_size
integer
[ 1 .. 100 ]
Default:
20
The maximum number of invoices to return in the response.
total_required
boolean
Default:
false
Indicates whether the to show
total_pages
and
total_items
in the response.
fields
string
[ 0 .. 2147483647 ] characters
^.*$
A comma-separated list of additional fields to return, if available.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
any
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that lists invoices with details.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Copy
{ }
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - List Invoices
Sample 1 - 200 - List Invoices
Copy
Expand all
Collapse all
{
"total_items"
:
2
,
"total_pages"
:
1
,
"items"
:
[
{
"id"
:
"INV2-Z56S-5LLA-Q52L-CPZ5"
,
"status"
:
"DRAFT"
,
"detail"
:
{
"invoice_number"
:
"#123"
,
"reference"
:
"deal-ref"
,
"invoice_date"
:
"2018-11-12"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"term"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"payment_term"
:
{
"term_type"
:
"NET_10"
,
"due_date"
:
"2018-11-22"
}
,
"metadata"
:
{
"create_time"
:
"2018-11-12T08:00:20Z"
,
"recipient_view_url"
:
"
https://www.paypal.com/invoice/p/#Z56S5LLAQ52LCPZ5
"
,
"invoicer_view_url"
:
"
https://www.paypal.com/invoice/details/INV2-Z56S-5LLA-Q52L-CPZ5
"
}
}
,
"invoicer"
:
{
"email_address"
:
"
[email protected]
"
}
,
"primary_recipients"
:
[
{
"billing_info"
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
"amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"74.21"
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/send
"
,
"rel"
:
"send"
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
]
}
,
{
"id"
:
"INV2-NP6M-C9A8-ZBDA-3TEX"
,
"status"
:
"SCHEDULED"
,
"detail"
:
{
"invoice_number"
:
"0001"
,
"invoice_date"
:
"2018-05-14"
,
"currency_code"
:
"USD"
,
"payment_term"
:
{
"due_date"
:
"2018-05-15"
}
,
"metadata"
:
{
"create_time"
:
"2018-05-15T17:24:12Z"
}
}
,
"invoicer"
:
{
"email_address"
:
"
[email protected]
"
}
,
"primary_recipients"
:
[
{
"billing_info"
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
"amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"32.00"
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-NP6M-C9A8-ZBDA-3TEX
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-NP6M-C9A8-ZBDA-3TEX
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-NP6M-C9A8-ZBDA-3TEX
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-NP6M-C9A8-ZBDA-3TEX/payments
"
,
"rel"
:
"record-payment"
,
"method"
:
"POST"
}
]
}
]
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices?page=1&page_size=20&total_required=false
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
Send invoice
post
/v2/invoicing/invoices/{invoice_id}/send
Try it
Sends or schedules an invoice, by ID, to be sent to a customer. The action depends on the invoice issue date:
If the invoice issue date is current or in the past, sends the invoice immediately.
If the invoice issue date is in the future, schedules the invoice to be sent on that date.
To suppress the merchant's email notification, set the
send_to_invoicer
body parameter to
false
. To send the invoice through a share link and not through PayPal, set the
send_to_recipient
parameter to
false
in the
notification
object. The
send_to_recipient
parameter does not apply to a future issue date because the invoice is scheduled to be sent through PayPal on that date.
Notes:
After you send an invoice, resending it has no effect.
To send a notification for updates,
update the invoice
and set the
send_to_recipient
body parameter to
true
.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice to send.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
The email or SMS notification to send to the payer when they send an invoice..
subject
string
[ 0 .. 4000 ] characters
^[\S\s]*$
The subject of the email that is sent as a notification to the recipient.
Note:
User-provided values for this field will not be honored and the subject will always be defaulted to a system-defined value.
note
string
[ 0 .. 4000 ] characters
^[\S\s]*$
A note to the payer.
Note:
User-provided values for this field will not be honored and the note will always be defaulted to a system-defined value.
send_to_invoicer
boolean
Default:
false
Indicates whether to send a copy of the email to the merchant.
send_to_recipient
boolean
Default:
true
Indicates whether to send a copy of the email to the recipient.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 0 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
Responses
202
The server has accepted the request and will execute it at a later time.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 202 - Schedules the invoice when the issue date is in future.
Sample 1 - 202 - Schedules the invoice when the issue date is in future.
Copy
{
"send_to_invoicer"
:
true
}
Response samples
202
application/json
multipart/mixed
application/json
Sample 1 - 202 - Schedules the invoice when the issue date is in future.
Sample 1 - 202 - Schedules the invoice when the issue date is in future.
Copy
{
"href"
:
"
https://api-m.paypal.com/invoice/p#INV2-Z56S-5LLA-Q52L-CPZ5
"
,
"rel"
:
"payer-view"
,
"method"
:
"GET"
}
Show invoice details
get
/v2/invoicing/invoices/{invoice_id}
Try it
Shows details for an invoice, by ID.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice for which to show details.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows invoice details.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
\
-H
'Content-Type: application/json'
Response samples
200
application/json
Sample 1 - 200 - Show Invoice Details with Theme
Sample 1 - 200 - Show Invoice Details with Theme
Copy
Expand all
Collapse all
{
"id"
:
"INV2-Z56S-5LLA-Q52L-CPZ5"
,
"status"
:
"DRAFT"
,
"detail"
:
{
"reference"
:
"deal-ref"
,
"invoice_date"
:
"2025-01-15"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"term"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"payment_term"
:
{
"term_type"
:
"NET_10"
,
"due_date"
:
"2025-01-25"
}
,
"order_details"
:
"Order #12345 placed on January 10, 2025."
,
"project_details"
:
"Website redesign project for client XYZ Corp."
,
"service_details"
:
"Consulting services provided from Jan-Mar 2025."
,
"cancellation_policy"
:
"Services may be cancelled with 14-day notice."
,
"payment_terms"
:
"Payment due within 10 days of invoice date."
,
"return_policy"
:
"All sales are final. No returns accepted after 30 days."
,
"service_agreement"
:
"Services provided as per agreement dated Jan 1, 2025."
,
"tip_presets"
:
[
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
,
{
"percent"
:
"25"
}
]
,
"metadata"
:
{
"create_time"
:
"2025-01-15T08:00:20Z"
,
"recipient_view_url"
:
"
https://www.paypal.com/invoice/p/#Z56S5LLAQ52LCPZ5
"
,
"invoicer_view_url"
:
"
https://www.paypal.com/invoice/details/INV2-Z56S-5LLA-Q52L-CPZ5
"
}
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"
https://example.com
"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"HOME"
}
]
,
"additional_info_value"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"items"
:
[
{
"name"
:
"Yoga Mat"
,
"description"
:
"Elastic mat to practice yoga."
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
,
"tax_note"
:
"Reduced tax rate"
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
"3.27"
}
}
,
"discount"
:
{
"percent"
:
"5"
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
"2.5"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"name"
:
"Yoga T Shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.34"
}
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"allow_tip"
:
true
,
"allow_only_pay_by_bank"
:
true
,
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"show_additional_item_fields"
:
false
,
"template_id"
:
"TEMP-19V05281TU309413B"
,
"has_conditional_rule"
:
true
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
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
"74.21"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"60.00"
}
,
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.73"
}
}
}
,
"discount"
:
{
"item_discount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"-7.50"
}
,
"invoice_discount"
:
{
"percent"
:
"5"
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
"-2.63"
}
}
}
,
"tax_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"4.34"
}
}
}
,
"due_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"74.21"
}
,
"settings"
:
{
"invoice_item_settings"
:
[
{
"field_name"
:
"ITEM_DESCRIPTION"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DATE"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"ITEM_TAX"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DISCOUNT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_additional_settings"
:
[
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"MEMO"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"REFERENCE"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"invoice_policy_and_agreement_settings"
:
[
{
"field_name"
:
"PAYMENT_TERMS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"TERMS_AND_CONDITIONS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"PROJECT_DETAILS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"SERVICE_DETAILS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/send
"
,
"rel"
:
"send"
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/payments
"
,
"rel"
:
"record-payment"
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/generate-qr-code
"
,
"rel"
:
"qr-code"
,
"method"
:
"POST"
}
]
}
Fully update invoice
put
/v2/invoicing/invoices/{invoice_id}
Try it
Fully updates an invoice, by ID. In the JSON request body, include a complete
invoice
object. This call does not support partial updates.
Notes:
API caller can change/modify recipient only 2 times in 72 hours.
.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice to update.
query
Parameters
send_to_recipient
boolean
Default:
true
Indicates whether to send the invoice update notification to the recipient.
send_to_invoicer
boolean
Default:
true
Indicates whether to send the invoice update notification to the merchant.
Request Body schema:
application/json
required
A representation of changes to make in the invoice.
primary_recipients
Array of
objects
(
recipient_info
)
[ 0 .. 100 ] items
The billing and shipping information. Includes name, email, address, phone and language.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 0 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
items
Array of
objects
(
item
)
[ 0 .. 100 ] items
An array of invoice line item information.
detail
required
object
(
invoice_detail
)
The details of the invoice. Includes invoice number, date, payment terms, and audit metadata.
invoicer
object
(
invoicer_info
)
The invoicer business information that appears on the invoice.
configuration
object
(
configuration
)
The invoice configuration details. Includes partial payment, tip, and tax calculated after discount.
amount
object
(
amount_summary_detail
)
The invoice amount summary of item total, discount, tax total, and shipping.
settings
object
(
invoice_settings
)
The settings for the invoice.
payments
object
(
payments
)
An array of payments registered against the invoice.
effective_invoice_total
object
(
Money
)
The effective total amount of the invoice after applying conditional rules. The conditional rules include early payment discount, late payment surcharge, and auto cancellation details.
effective_due_amount
object
(
Money
)
The effective due amount of the invoice after applying conditional rules. The conditional rules include early payment discount, late payment surcharge, and auto cancellation details.
refunds
object
(
refunds
)
The invoicing refund details. Includes the refund type, date, amount, and method.
Responses
200
A successful request returns the HTTP
200 OK
status code. A JSON response body that shows invoice details is returned if you set
prefer=return=representation
.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
Sample 1 - 200 - Update Invoice with Theme
Sample 1 - 200 - Update Invoice with Theme
Copy
Expand all
Collapse all
{
"id"
:
"INV2-C82X-JNN9-Y6S5-CNXW"
,
"status"
:
"DRAFT"
,
"detail"
:
{
"reference"
:
"deal-refernce-update"
,
"invoice_date"
:
"2025-01-15"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"term"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"payment_term"
:
{
"term_type"
:
"NET_10"
,
"due_date"
:
"2025-01-25"
}
,
"order_details"
:
"Updated order #12345 details from Jan 10, 2025."
,
"project_details"
:
"Updated website redesign project for XYZ Corp - added mobile optimization."
,
"service_details"
:
"Additional consulting services Jan-Apr 2025."
,
"cancellation_policy"
:
"Updated: Services may be cancelled with 30-day notice."
,
"payment_terms"
:
"Updated: Payment due within 15 days of invoice date."
,
"return_policy"
:
"Updated: All sales are final. No returns accepted after 15 days."
,
"service_agreement"
:
"Updated: Services provided as per revised agreement dated Feb 1, 2025."
,
"tip_presets"
:
[
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
,
{
"percent"
:
"25"
}
]
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"www.test.com"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"HOME"
}
]
,
"additional_info_value"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"items"
:
[
{
"name"
:
"Yoga Mat"
,
"description"
:
"Elastic mat to practice yoga."
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
,
"tax_note"
:
"Reduced tax rate"
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
"3.27"
}
}
,
"discount"
:
{
"percent"
:
"5"
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
"2.5"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"name"
:
"Yoga t-shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.34"
}
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"allow_tip"
:
true
,
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"show_additional_item_fields"
:
true
,
"template_id"
:
"TEMP-19V05281TU309413B"
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
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
"74.21"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"60.00"
}
,
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.73"
}
}
}
,
"discount"
:
{
"item_discount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"-7.50"
}
,
"invoice_discount"
:
{
"percent"
:
"5"
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
"-2.63"
}
}
}
,
"tax_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"4.34"
}
}
}
,
"settings"
:
{
"invoice_item_settings"
:
[
{
"field_name"
:
"ITEM_DESCRIPTION"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DATE"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"ITEM_TAX"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DISCOUNT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_additional_settings"
:
[
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"MEMO"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"REFERENCE"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_policy_and_agreement_settings"
:
[
{
"field_name"
:
"TERMS_AND_CONDITIONS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"PAYMENT_TERMS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"invoice_details_settings"
:
[
{
"field_name"
:
"SERVICE_DETAILS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
}
}
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Update Invoice with Theme
Sample 1 - 200 - Update Invoice with Theme
Copy
Expand all
Collapse all
{
"id"
:
"INV2-C82X-JNN9-Y6S5-CNXW"
,
"status"
:
"DRAFT"
,
"detail"
:
{
"reference"
:
"deal-refernce-update"
,
"invoice_date"
:
"2025-01-15"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"term"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"payment_term"
:
{
"term_type"
:
"NET_10"
,
"due_date"
:
"2025-01-25"
}
,
"order_details"
:
"Updated order #12345 details from Jan 10, 2025."
,
"project_details"
:
"Updated website redesign project for XYZ Corp - added mobile optimization."
,
"service_details"
:
"Additional consulting services Jan-Apr 2025."
,
"cancellation_policy"
:
"Updated: Services may be cancelled with 30-day notice."
,
"payment_terms"
:
"Updated: Payment due within 15 days of invoice date."
,
"return_policy"
:
"Updated: All sales are final. No returns accepted after 15 days."
,
"service_agreement"
:
"Updated: Services provided as per revised agreement dated Feb 1, 2025."
,
"tip_presets"
:
[
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
,
{
"percent"
:
"25"
}
]
,
"metadata"
:
{
"create_time"
:
"2025-01-15T08:00:20Z"
,
"recipient_view_url"
:
"
https://www.api-m.paypal.com/invoice/p#Z56S5LLAQ52LCPZ5
"
,
"invoicer_view_url"
:
"
https://www.api-m.paypal.com/invoice/details/INV2-Z56S-5LLA-Q52L-CPZ5
"
}
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"
https://example.com
"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"HOME"
}
]
,
"additional_info_value"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"items"
:
[
{
"name"
:
"Yoga Mat"
,
"description"
:
"Elastic mat to practice yoga."
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"3.27"
}
}
,
"discount"
:
{
"percent"
:
"5"
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
"2.5"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"name"
:
"Yoga t-shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.34"
}
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"allow_tip"
:
true
,
"allow_only_pay_by_bank"
:
true
,
"tax_calculated_after_discount"
:
true
,
"show_additional_item_fields"
:
true
,
"tax_inclusive"
:
false
,
"template_id"
:
"TEMP-19V05281TU309413B"
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
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
"74.21"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"60.00"
}
,
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.73"
}
}
}
,
"discount"
:
{
"item_discount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"-7.50"
}
,
"invoice_discount"
:
{
"percent"
:
"5"
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
"-2.63"
}
}
}
,
"tax_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"4.34"
}
}
}
,
"due_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"74.21"
}
,
"settings"
:
{
"invoice_item_settings"
:
[
{
"field_name"
:
"ITEM_DESCRIPTION"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DATE"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"ITEM_TAX"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ITEM_DISCOUNT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/send
"
,
"rel"
:
"send"
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
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/update
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
]
}
Delete invoice
delete
/v2/invoicing/invoices/{invoice_id}
Try it
Deletes a draft or scheduled invoice, by ID. Deletes invoices in the draft or scheduled state only. For invoices that have already been sent, you can
cancel the invoice
. After you delete a draft or scheduled invoice, you can no longer use it or show its details. However, you can reuse its invoice number.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the draft invoice to delete.
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
DELETE https://api-m.sandbox.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
Response samples
204
application/json
Sample 1 - 204 - Delete Invoice
Sample 1 - 204 - Delete Invoice
Copy
{ }
Search for invoices
post
/v2/invoicing/search-invoices
Try it
Searches for and lists invoices that match search criteria. If you pass multiple criteria, the response lists invoices that match all criteria.
Security
Oauth2
Request
query
Parameters
page
integer
[ 1 .. 1000 ]
Default:
1
The page number to be retrieved, for the list of items. So, a combination of
page=1
and
page_size=20
returns the first 20 invoices. A combination of
page=2
and
page_size=20
returns the next 20 invoices.
page_size
integer
[ 1 .. 100 ]
Default:
20
The page size for the search results.
total_required
boolean
Default:
false
Indicates whether the to show
total_pages
and
total_items
in the response.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
The invoice search can be used to retrieve the invoices based on the search parameters.
recipient_email
string
[ 0 .. 254 ] characters
^[\S\s]*$
Filters the search by the email address.
recipient_first_name
string
[ 0 .. 140 ] characters
^[\S\s]*$
Filters the search by the recipient first name.
recipient_last_name
string
[ 0 .. 140 ] characters
^[\S\s]*$
Filters the search by the recipient last name.
recipient_business_name
string
[ 0 .. 300 ] characters
^[\S\s]*$
Filters the search by the recipient business name.
invoice_number
string
[ 0 .. 25 ] characters
^[\S\s]*$
Filters the search by the invoice number.
status
Array of
strings
(
invoice_status
)
[ 0 .. 5 ] items
An array of status values.
Items
Enum Value
Description
DRAFT
The invoice is in draft state. It is not yet sent to the payer.
SENT
The invoice has been sent to the payer. The payment is awaited from the payer.
SCHEDULED
The invoice is scheduled on a future date. It is not yet sent to the payer.
PAID
The payer has paid for the invoice.
MARKED_AS_PAID
The invoice is marked as paid by the invoicer.
CANCELLED
The invoice has been cancelled by the invoicer.
REFUNDED
The invoice has been refunded by the invoicer.
PARTIALLY_PAID
The payer has partially paid for the invoice.
PARTIALLY_REFUNDED
The invoice has been partially refunded by the invoicer.
MARKED_AS_REFUNDED
The invoice is marked as refunded by the invoicer.
UNPAID
The invoicer is yet to receive the payment from the payer for the invoice.
PAYMENT_PENDING
The invoicer is yet to receive the payment for the invoice. It is under pending review.
AUTO_CANCELLED
The invoice was automatically cancelled because the payment was not received within the specified timeframe.
PAID_EXTERNAL
The invoice has been paid through an external system or method outside of the standard PayPal payment flow. This status is set manually, indicating payment was received through other means.
REFUNDED_EXTERNAL
The invoice has been refunded through an external system or method. This status indicates a refund was issued outside of the standard PayPal payment flow.
SHARED
The invoice has been shared with the payer, typically via a link or other method. This status is used to track when an invoice has been distributed but not necessarily sent via PayPal.
reference
string
[ 0 .. 120 ] characters
^[\S\s]*$
The reference data. Includes a Purchase Order (PO) number.
memo
string
[ 0 .. 500 ] characters
^[\S\s]*$
A private bookkeeping memo for the user.
payment_date_range
object
(
Date and Time Range
)
The date and time range. Filters invoices by creation date, invoice date, due date, and payment date.
archived
boolean
Indicates whether to list merchant-archived invoices in the response. Value is:
true
. Response lists only merchant-archived invoices.
false
. Response lists only unarchived invoices.
null
. Response lists all invoices.
fields
Array of
strings
[ 0 .. 5 ] items
A CSV file of fields to return for the user, if available. Because the invoice object can be very large, field filtering is required. Valid collection fields are
items
,
payments
,
refunds
,
additional_recipients_info
, and
attachments
.
currency_code
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
total_amount_range
object
(
amount_range
)
The amount range.
invoice_date_range
object
(
date_range
)
The date range. Filters invoices by creation date, invoice date, due date, and payment date.
due_date_range
object
(
date_range
)
The date range. Filters invoices by creation date, invoice date, due date, and payment date.
creation_date_range
object
(
Date and Time Range
)
The date and time range. Filters invoices by creation date, invoice date, due date, and payment date.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that lists the invoices that match the search criteria.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 200 - Search for Invoices
Sample 1 - 200 - Search for Invoices
Copy
Expand all
Collapse all
{
"total_amount_range"
:
{
"lower_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"upper_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
}
,
"invoice_date_range"
:
{
"start"
:
"2018-06-01"
,
"end"
:
"2018-06-21"
}
}
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Search for Invoices
Sample 1 - 200 - Search for Invoices
Copy
Expand all
Collapse all
{
"total_items"
:
6
,
"total_pages"
:
1
,
"items"
:
[
{
"id"
:
"INV2-Z56S-5LLA-Q52L-CPZ5"
,
"status"
:
"DRAFT"
,
"detail"
:
{
"invoice_number"
:
"#123"
,
"reference"
:
"deal-ref"
,
"invoice_date"
:
"2018-11-12"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"term"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"payment_term"
:
{
"term_type"
:
"NET_10"
,
"due_date"
:
"2018-11-22"
}
,
"metadata"
:
{
"create_time"
:
"2018-11-12T08:00:20Z"
,
"recipient_view_url"
:
"
https://www.api-m.paypal.com/invoice/p#Z56S5LLAQ52LCPZ5
"
,
"invoicer_view_url"
:
"
https://www.api-m.paypal.com/invoice/details/INV2-Z56S-5LLA-Q52L-CPZ5
"
}
}
,
"invoicer"
:
{
"email_address"
:
"
[email protected]
"
}
,
"primary_recipients"
:
[
{
"billing_info"
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
"amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"74.21"
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5
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
]
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/invoices?page=2&page_size=10&total_required=true
"
,
"rel"
:
"next"
,
"method"
:
"POST"
}
]
}
Cancel sent invoice
post
/v2/invoicing/invoices/{invoice_id}/cancel
Try it
Cancels a sent invoice, by ID, and, optionally, sends a notification about the cancellation to the payer, merchant, and CC: emails.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice to cancel.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
required
The email or SMS notification that will be sent to the payer on cancellation.
subject
string
[ 0 .. 4000 ] characters
^[\S\s]*$
The subject of the email that is sent as a notification to the recipient.
Note:
User-provided values for this field will not be honored and the subject will always be defaulted to a system-defined value.
note
string
[ 0 .. 4000 ] characters
^[\S\s]*$
A note to the payer.
Note:
User-provided values for this field will not be honored and the note will always be defaulted to a system-defined value.
send_to_invoicer
boolean
Default:
false
Indicates whether to send a copy of the email to the merchant.
send_to_recipient
boolean
Default:
true
Indicates whether to send a copy of the email to the recipient.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 0 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 204 - Cancel Invoice
Sample 1 - 204 - Cancel Invoice
Copy
Expand all
Collapse all
{
"send_to_invoicer"
:
true
,
"send_to_recipient"
:
true
,
"additional_recipients"
:
[
"
[email protected]
"
]
}
Response samples
204
application/json
Sample 1 - 204 - Cancel Invoice
Sample 1 - 204 - Cancel Invoice
Copy
{ }
Send invoice reminder
post
/v2/invoicing/invoices/{invoice_id}/remind
Try it
Sends a reminder to the payer about an invoice, by ID. In the JSON request body, include a
notification
object that defines the subject of the reminder and other details.
Notes:
API caller can send only 2 reminders in a day.
.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice for which to send a reminder.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
The email or SMS notification that will be sent to the payer for reminder.
subject
string
[ 0 .. 4000 ] characters
^[\S\s]*$
The subject of the email that is sent as a notification to the recipient.
Note:
User-provided values for this field will not be honored and the subject will always be defaulted to a system-defined value.
note
string
[ 0 .. 4000 ] characters
^[\S\s]*$
A note to the payer.
Note:
User-provided values for this field will not be honored and the note will always be defaulted to a system-defined value.
send_to_invoicer
boolean
Default:
false
Indicates whether to send a copy of the email to the merchant.
send_to_recipient
boolean
Default:
true
Indicates whether to send a copy of the email to the recipient.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 0 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 204 - Remind Payer to Pay Invoice
Sample 1 - 204 - Remind Payer to Pay Invoice
Copy
Expand all
Collapse all
{
"send_to_invoicer"
:
true
,
"additional_recipients"
:
[
"
[email protected]
"
,
"
[email protected]
"
]
}
Response samples
204
application/json
Sample 1 - 204 - Remind Payer to Pay Invoice
Sample 1 - 204 - Remind Payer to Pay Invoice
Copy
{ }
Record payment for invoice
post
/v2/invoicing/invoices/{invoice_id}/payments
Try it
Records a payment for the invoice. If no payment is due, the invoice is marked as
PAID
. Otherwise, the invoice is marked as
PARTIALLY PAID
.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice to mark as paid.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
required
The details of the payment to record against the invoice.
payment_id
string
[ 0 .. 22 ] characters
^[\S\s]*$
The ID for a PayPal payment transaction. Required for the
PAYPAL
payment type.
note
string
[ 0 .. 2000 ] characters
^[\S\s]*$
A note associated with an external cash or check payment.
payment_date
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
payment_date_time
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
method
required
string
(
payment_method
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment mode or method through which the invoicer can accept the payment.
Enum Value
Description
BANK_TRANSFER
Payments can be received through bank transfers.
CASH
Payments can be received as cash.
CHECK
Payments can be received as check.
CREDIT_CARD
Payments can be received through credit card payments.
DEBIT_CARD
Payments can be received through debit card payments.
PAYPAL
Payments can be received through paypal payments.
WIRE_TRANSFER
Payments can be received through wire transfer.
OTHER
Payments can be received through other modes.
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
shipping_info
object
(
contact_information
)
The contact information of the user. Includes name and address.
Responses
200
A successful request returns the HTTP
200 Created
status code and a reference to the recorded payment.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 200 - Record Payment for Invoice
Sample 1 - 200 - Record Payment for Invoice
Copy
Expand all
Collapse all
{
"method"
:
"BANK_TRANSFER"
,
"payment_date"
:
"2018-05-01"
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
"10.00"
}
}
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Record Payment for Invoice
Sample 1 - 200 - Record Payment for Invoice
Copy
{
"payment_id"
:
"EXTR-86F38350LX4353815"
}
Delete external payment
delete
/v2/invoicing/invoices/{invoice_id}/payments/{transaction_id}
Try it
Deletes an external payment, by invoice ID and transaction ID.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice from which to delete an external payment transaction.
transaction_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the external payment transaction to delete.
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
DELETE https://api-m.sandbox.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/payments/EXTR-86F38350LX4353815
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
Response samples
204
application/json
Sample 1 - 204 - Delete External Payment
Sample 1 - 204 - Delete External Payment
Copy
{ }
Record refund for invoice
post
/v2/invoicing/invoices/{invoice_id}/refunds
Try it
Records a refund for the invoice. If all payments are refunded, the invoice is marked as
REFUNDED
. Otherwise, the invoice is marked as
PARTIALLY REFUNDED
.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice to mark as refunded.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
required
The details of the refund to record against the invoice.
refund_date
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
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
method
required
string
(
payment_method
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment mode or method through which the invoicer can accept the payments.
Enum Value
Description
BANK_TRANSFER
Payments can be received through bank transfers.
CASH
Payments can be received as cash.
CHECK
Payments can be received as check.
CREDIT_CARD
Payments can be received through credit card payments.
DEBIT_CARD
Payments can be received through debit card payments.
PAYPAL
Payments can be received through paypal payments.
WIRE_TRANSFER
Payments can be received through wire transfer.
OTHER
Payments can be received through other modes.
Responses
200
A successful request returns the HTTP
200 Created
status code and a reference to the recorded refund.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 200 - Record Refund for Invoice
Sample 1 - 200 - Record Refund for Invoice
Copy
Expand all
Collapse all
{
"method"
:
"BANK_TRANSFER"
,
"refund_date"
:
"2018-05-21"
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
"5.00"
}
}
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Record Refund for Invoice
Sample 1 - 200 - Record Refund for Invoice
Copy
{
"refund_id"
:
"EXTR-2LG703375E477444T"
}
Delete external refund
delete
/v2/invoicing/invoices/{invoice_id}/refunds/{transaction_id}
Try it
Deletes an external refund, by invoice ID and transaction ID.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice from which to delete the external refund transaction.
transaction_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the external refund transaction to delete.
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
DELETE https://api-m.sandbox.paypal.com/v2/invoicing/invoices/INV2-Z56S-5LLA-Q52L-CPZ5/refunds/EXTR-2LG703375E477444T
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
Response samples
204
application/json
Sample 1 - 204 - Retry Delete External Refund
Sample 1 - 204 - Retry Delete External Refund
Copy
{ }
Generate invoice number
post
/v2/invoicing/generate-next-invoice-number
Try it
Generates the next invoice number that is available to the merchant. The next invoice number uses the prefix and suffix from the last invoice number and increments the number by one. For example, the next invoice number after
INVOICE-1234
is
INVOICE-1235
.
Security
Oauth2
Request
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Is the fetch type invoice number or id.
fetch_id
boolean
Default:
"false"
Optional to decide the number or ID.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows the next invoice number.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 200 - Generate Next Invoice Id
Sample 1 - 200 - Generate Next Invoice Id
Copy
{
"fetch_id"
:
true
}
Response samples
200
application/json
Sample 1 - 200 - Generate Next Invoice Id
Sample 1 - 200 - Generate Next Invoice Id
Copy
{
"invoice_id"
:
"INV2-Z56S-5LLA-Q52L-CPZ5"
}
Generate QR code
post
/v2/invoicing/invoices/{invoice_id}/generate-qr-code
Try it
Generates a QR code for an invoice, by ID. The QR code is a PNG image in
Base64-encoded
format that corresponds to the invoice ID. You can generate a QR code for an invoice and add it to a paper or PDF invoice. When customers use their mobile devices to scan the QR code, they are redirected to the PayPal mobile payment flow where they can view the invoice and pay online with PayPal or a credit card. Before you get a QR code, you must
create an invoice
and
send an invoice
to move the invoice from a draft to payable state. Do not include an email address if you do not want the invoice emailed.
Security
Oauth2
Request
path
Parameters
invoice_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the invoice for which to generate a QR code.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Optional configuration parameters to adjust QR code width, height and the encoded URL.
width
integer
[ 150 .. 500 ]
Default:
500
The width, in pixels, of the QR code image. Value is from
150
to
500
.
height
integer
[ 150 .. 500 ]
Default:
500
The height, in pixels, of the QR code image. Value is from
150
to
500
.
action
string
[ 0 .. 7 ] characters
(?i)^(pay|details)$
Default:
"pay"
The type of URL for which to generate a QR code. Valid values are
pay
and
details
.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows the QR code as a PNG image.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 200 - Generate QR Code for Invoice
Sample 1 - 200 - Generate QR Code for Invoice
Copy
{
"width"
:
400
,
"height"
:
400
}
Response samples
200
multipart/form-data
Sample 1 - 200 - Generate QR Code for Invoice
Sample 1 - 200 - Generate QR Code for Invoice
Copy
--
95
dbdbed
-
7536
-
4
c24
-
b5ca
-
bcdbc0006612 Content
-
Disposition
:
form
-
data
;
name
=
"image"
Content
-
Type
:
application
/
octet
-
stream iVBORw0KGgoAAAANSUhEUgAAAJYAAACWAQAAAAAUekxPAAABxUlEQVR42u2WMY7kIBBFq0VA1n0BS1yDjCvZF7DxBdxXIuMaSFzAzgiQaz6t9mxLm1AbrCYYy4H1AlT1f9XHxH89lX7Z
/
2
KJKN3CMIW6FCInYplLPtisoU6FTyHzti6RN5tPm
+
5
ixrtTp0uP8g8s744eMS1yxvikNEOJz966GPTLaOL1fmjaxfAkaLCy2t2Hl10sPUIaNY1araFhCat3TbODDPkZ68Ii1sqfX62c1rzP62W8uWG0aiMaxSyvpS4hez2MzXkZg
+
FL4NNCwku
/
XtZ8g
/
Be550
+
Pe9jWj0x41rt1ngZyxzYa
+
NpmDjNMlYx1yhhs2glM8vY3IQ3qGWz9Tqvk7F3cGyYNd3KQDKGSWFGDjFNIZ8yhuWgR8gb5jR8
+
9
bJ8rPUCd3oYbY4VcQqaWSYWRGcdnhnSS
+
D6lhKJIE5
+
JrTXtaquDtzuuypXrV0stRKwLAUzFodnYjxERP28ihtLw8WsbQE7JbxCD9SmxMxfsUYpiZ7lxYWMewltzuqKMz4n13tYi3vl6jW2FJQynBH
+
Za7Zie6sZRhNVXLTkqTmGUE5xSRu5dv3Qz3uYdj0bwkFLGWfxxoJMXx28tO9vu
/
9
oPYF0bR
/
hBeOiwMAAAAAElFTkSuQmCC
--
95
dbdbed
-
7536
-
4
c24
-
b5ca
-
bcdbc0006612
--
List templates
get
/v2/invoicing/templates
Try it
Lists merchant-created templates with associated details. The associated details include the emails, addresses, and phone numbers from the user's PayPal profile.
The user can select which values to show in the business information section of their template.
Security
Oauth2
Request
query
Parameters
fields
string
[ 1 .. 2147483647 ] characters
(?i)^(all|none)$
Default:
"all"
The fields to return in the response. Value is
all
or
none
. To return only the template name, ID, and default attributes, specify
none
.
page
integer
[ 1 .. 1000 ]
Default:
1
The page number to be retrieved, for the list of templates. So, a combination of
page=1
and
page_size=20
returns the first 20 templates. A combination of
page=2
and
page_size=20
returns the next 20 templates.
page_size
integer
[ 1 .. 100 ]
Default:
20
The maximum number of templates to return in the response.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
any
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that lists invoices.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Copy
{ }
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - List Templates
Sample 1 - 200 - List Templates
Copy
Expand all
Collapse all
{
"addresses"
:
[
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
{
"address_line_1"
:
"26303 E 8216 N"
,
"address_line_2"
:
"045608 Ocean Bay Plaza #02"
,
"admin_area_2"
:
"Garden City"
,
"admin_area_1"
:
"NY"
,
"postal_code"
:
"11530"
,
"country_code"
:
"US"
}
]
,
"emails"
:
"
[email protected]
,
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"HOME"
}
,
{
"country_code"
:
"1"
,
"national_number"
:
"3477832250"
,
"phone_type"
:
"MOBILE"
}
,
{
"country_code"
:
"1"
,
"national_number"
:
"3479543267"
,
"phone_type"
:
"FAX"
}
,
{
"country_code"
:
"1"
,
"national_number"
:
"7183514942"
,
"phone_type"
:
"OTHER"
}
]
,
"templates"
:
[
{
"id"
:
"TEMP-19V05281TU309413B"
,
"name"
:
"reference-temp"
,
"description"
:
"Template description"
,
"default_template"
:
true
,
"template_info"
:
{
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
}
,
"detail"
:
{
"reference"
:
"deal-ref"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"terms_and_conditions"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"attachments"
:
[
{
"id"
:
"Screen Shot 2018-11-23 at 16.45.01.png"
,
"reference_url"
:
"
https://exxample.com/invoice/payerView/attachments/RkG9ggQbd4Mwm1tYdcF6uuixfFTFq32bBdbE1VbtQLdKSoS2ZOYpfjw9gPp7eTrZmVaFaDWzixHXm-OXWHbmigHigHzURDxJs8IIKqcqP8jawnBEZcraEAPVMULxf5iTyOSpAUc2ugW0PWdwDbM6mg-guFAUyj3Z98H7htWNjQY95jb9heOlcSXUe.sbDUR9smAszzzJoA1NXT6rEEegwQ&version=1&sig=JNODB0xEayW8txMQm6ZsIwDnd4eh3hd6ijiRLi4ipHE
"
}
]
,
"payment_term"
:
{
"term_type"
:
"NET_10"
}
,
"metadata"
:
{
"create_time"
:
"2018-12-03T03:38:46z"
}
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"www.test.com"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"additional_info"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"additional_recipients"
:
[
"
[email protected]
"
]
,
"items"
:
[
{
"id"
:
"ITEM-9R873787D1610780X"
,
"name"
:
"Yoga Mat"
,
"description"
:
"new watch"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"id"
:
"TAX-9R873787D1610780X"
,
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"3.27"
}
}
,
"discount"
:
{
"percent"
:
"5"
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
"2.5"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"id"
:
"ITEM-4XD34145EH4061035"
,
"name"
:
"Yoga t-shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"id"
:
"TAX-4XD34145EH4061035"
,
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.34"
}
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
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
"74.21"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"60.00"
}
,
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.73"
}
}
}
,
"discount"
:
{
"item_discount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"-7.50"
}
,
"invoice_discount"
:
{
"percent"
:
"5"
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
"-2.63"
}
}
}
,
"tax_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"4.34"
}
}
}
}
,
"settings"
:
{
"template_item_settings"
:
[
{
"field_name"
:
"items.date"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"items.discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.tax"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.description"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.quantity"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_subtotal_settings"
:
[
{
"field_name"
:
"custom"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"shipping"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
}
,
"unit_of_measure"
:
"QUANTITY"
,
"standard_template"
:
false
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
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
,
{
"default_template"
:
true
,
"id"
:
"TEMP-11E67842VH3080617"
,
"name"
:
"Quantity"
,
"description"
:
"Default Template description"
,
"template_info"
:
{
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"email_address"
:
"
[email protected]
"
}
,
"detail"
:
{
"currency_code"
:
"USD"
}
}
,
"standard_template"
:
false
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/templates/TEMP-11E67842VH3080617
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
,
{
"default_template"
:
false
,
"id"
:
"TEMP-6HC14139B8663074X"
,
"description"
:
"Template description 1"
,
"name"
:
"Hours"
,
"template_info"
:
{
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"email_address"
:
"
[email protected]
"
}
,
"detail"
:
{
"currency_code"
:
"USD"
}
}
,
"standard_template"
:
false
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/templates/TEMP-6HC14139B8663074X
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
]
}
Create template
post
/v2/invoicing/templates
Try it
Creates an invoice template. You can use details from this template to create an invoice. You can create up to 50 templates.
Note:
Every merchant starts with three PayPal system templates that are optimized for the unit type billed. The template includes
Quantity
,
Hours
, and
Amount
.
Security
Oauth2
Request
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
required
name
string
[ 1 .. 500 ] characters
^[\S\s]*$
The template name.
Note:
The template name must be unique.
description
string
[ 1 .. 160 ] characters
^[\S\s]*$
The detailed description of the template.
default_template
boolean
Indicates whether this template is the default template. A invoicer can have one default template.
template_info
object
(
template_info
)
The template details. Includes invoicer business information, invoice recipients, items, and configuration.
settings
object
(
template_settings
)
The template settings. Describes which fields to show or hide when you create an invoice.
unit_of_measure
string
(
unit_of_measure
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The unit of measure for the invoiced item.
Enum Value
Description
QUANTITY
The unit of measure is quantity. This invoice template is typically used for physical goods.
HOURS
The unit of measure is hours. This invoice template is typically used for services.
AMOUNT
The unit of measure is amount. This invoice template is typically used when only amount is required.
Responses
201
A successful request returns the HTTP
201 Created
status code. A JSON response body that shows template details is returned if you set
prefer=return=representation
.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 201 - Create Template with Theme
Sample 1 - 201 - Create Template with Theme
Copy
Expand all
Collapse all
{
"description"
:
"Template description"
,
"default_template"
:
true
,
"template_info"
:
{
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"show_additional_item_fields"
:
false
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
,
"detail"
:
{
"reference"
:
"deal-ref"
,
"note"
:
"Thank you for your business."
,
"currency_code"
:
"USD"
,
"terms_and_conditions"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"attachments"
:
[
{
"id"
:
"Screen Shot 2018-11-23 at 16.45.01.png"
,
"reference_url"
:
"
https://api-m.paypal.com/invoice/payerView/attachments/RkG9ggQbd4Mwm1tYdcF6uuixfFTFq32bBdbE1VbtQLdKSoS2ZOYpfjw9gPp7eTrZmVaFaDWzixHXm-OXWHbmigHigHzURDxJs8IIKqcqP8jawnBEZcraEAPVMULxf5iTyOSpAUc2ugW0PWdwDbM6mg-guFAUyj3Z98H7htWNjQY95jb9heOlcSXUe.sbDUR9smAszzzJoA1NXT6rEEegwQ&version=1&sig=JNODB0xEayW8txMQm6ZsIwDnd4eh3hd6ijiRLi4ipHE
"
}
]
,
"payment_term"
:
{
"term_type"
:
"NET_10"
}
,
"service_agreement"
:
"This agreement covers the terms of the provided consulting services."
,
"tip_presets"
:
[
{
"percent"
:
"10"
}
,
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
]
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"www.test.com"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"additional_info"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"additional_recipients"
:
[
"
[email protected]
"
]
,
"items"
:
[
{
"name"
:
"Yoga Mat"
,
"description"
:
"new watch"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
}
,
"discount"
:
{
"percent"
:
"5"
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"name"
:
"Yoga T Shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
,
"tax_note"
:
"Reduced tax rate"
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
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
"74.21"
,
"breakdown"
:
{
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
}
}
,
"discount"
:
{
"invoice_discount"
:
{
"percent"
:
"5"
}
}
}
}
}
,
"settings"
:
{
"template_item_settings"
:
[
{
"field_name"
:
"items.date"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"items.discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.tax"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.description"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.quantity"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_subtotal_settings"
:
[
{
"field_name"
:
"custom"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"shipping"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"PROJECT_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_policy_and_agreement_settings"
:
[
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"PAYMENT_TERMS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"RETURN_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_AGREEMENT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"TERMS_AND_CONDITIONS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_additional_settings"
:
[
{
"field_name"
:
"REFERENCE"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"MEMO"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
}
,
"unit_of_measure"
:
"QUANTITY"
,
"standard_template"
:
false
}
Response samples
201
application/json
multipart/mixed
application/json
Sample 1 - 201 - Create Template with Theme
Sample 1 - 201 - Create Template with Theme
Copy
Expand all
Collapse all
{
"id"
:
"TEMP-19V05281TU309413B"
,
"name"
:
"reference-temp"
,
"description"
:
"Template description"
,
"default_template"
:
true
,
"template_info"
:
{
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"show_additional_item_fields"
:
false
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
,
"detail"
:
{
"reference"
:
"deal-ref"
,
"note"
:
"Thank you for your business."
,
"currency_code"
:
"USD"
,
"terms_and_conditions"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"attachments"
:
[
{
"id"
:
"Screen Shot 2018-11-23 at 16.45.01.png"
,
"reference_url"
:
"
https://api-m.paypal.com/invoice/payerView/attachments/RkG9ggQbd4Mwm1tYdcF6uuixfFTFq32bBdbE1VbtQLdKSoS2ZOYpfjw9gPp7eTrZmVaFaDWzixHXm-OXWHbmigHigHzURDxJs8IIKqcqP8jawnBEZcraEAPVMULxf5iTyOSpAUc2ugW0PWdwDbM6mg-guFAUyj3Z98H7htWNjQY95jb9heOlcSXUe.sbDUR9smAszzzJoA1NXT6rEEegwQ&version=1&sig=JNODB0xEayW8txMQm6ZsIwDnd4eh3hd6ijiRLi4ipHE
"
}
]
,
"payment_term"
:
{
"term_type"
:
"NET_10"
}
,
"tip_presets"
:
[
{
"percent"
:
"10"
}
,
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
]
,
"metadata"
:
{
"create_time"
:
"2018-12-03T03:38:46z"
}
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"www.test.com"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"additional_info"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"additional_recipients"
:
[
"
[email protected]
"
]
,
"items"
:
[
{
"id"
:
"ITEM-9R873787D1610780X"
,
"name"
:
"Yoga Mat"
,
"description"
:
"new watch"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"id"
:
"TAX-9R873787D1610780X"
,
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"3.27"
}
}
,
"discount"
:
{
"percent"
:
"5"
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
"2.5"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"id"
:
"ITEM-4XD34145EH4061035"
,
"name"
:
"Yoga T Shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"id"
:
"TAX-4XD34145EH4061035"
,
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.34"
}
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
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
"74.21"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"60.00"
}
,
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.73"
}
}
}
,
"discount"
:
{
"item_discount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"-7.50"
}
,
"invoice_discount"
:
{
"percent"
:
"5"
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
"-2.63"
}
}
}
,
"tax_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"4.34"
}
}
}
}
,
"settings"
:
{
"template_item_settings"
:
[
{
"field_name"
:
"items.date"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"items.discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.tax"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.description"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.quantity"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_subtotal_settings"
:
[
{
"field_name"
:
"custom"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"shipping"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"PROJECT_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_policy_and_agreement_settings"
:
[
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"PAYMENT_TERMS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"RETURN_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_AGREEMENT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"TERMS_AND_CONDITIONS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_additional_settings"
:
[
{
"field_name"
:
"REFERENCE"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"MEMO"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
}
,
"unit_of_measure"
:
"QUANTITY"
,
"standard_template"
:
false
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
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
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
]
}
Show template details
get
/v2/invoicing/templates/{template_id}
Try it
Shows details for a template, by ID.
Security
Oauth2
Request
path
Parameters
template_id
required
string
[ 1 .. 22 ] characters
^(@default|TEMP-[A-Z0-9]{17})$
The ID of the template for which to show details.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows template details.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
\
-H
'Content-Type: application/json'
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Show Template Details with Theme
Sample 1 - 200 - Show Template Details with Theme
Copy
Expand all
Collapse all
{
"id"
:
"TEMP-19V05281TU309413B"
,
"name"
:
"reference-temp"
,
"description"
:
"Template description"
,
"default_template"
:
true
,
"template_info"
:
{
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"show_additional_item_fields"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
,
"detail"
:
{
"reference"
:
"deal-ref"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"terms_and_conditions"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"attachments"
:
[
{
"id"
:
"Screen Shot 2018-11-23 at 16.45.01.png"
,
"reference_url"
:
"
https://api-m.paypal.com/invoice/payerView/attachments/RkG9ggQbd4Mwm1tYdcF6uuixfFTFq32bBdbE1VbtQLdKSoS2ZOYpfjw9gPp7eTrZmVaFaDWzixHXm-OXWHbmigHigHzURDxJs8IIKqcqP8jawnBEZcraEAPVMULxf5iTyOSpAUc2ugW0PWdwDbM6mg-guFAUyj3Z98H7htWNjQY95jb9heOlcSXUe.sbDUR9smAszzzJoA1NXT6rEEegwQ&version=1&sig=JNODB0xEayW8txMQm6ZsIwDnd4eh3hd6ijiRLi4ipHE
"
}
]
,
"payment_term"
:
{
"term_type"
:
"NET_10"
}
,
"tip_presets"
:
[
{
"percent"
:
"10"
}
,
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
]
,
"service_agreement"
:
"This agreement covers the terms of the provided consulting services."
,
"metadata"
:
{
"create_time"
:
"2018-12-03T03:38:46z"
}
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"www.test.com"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"additional_info"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"additional_recipients"
:
[
"
[email protected]
"
]
,
"items"
:
[
{
"id"
:
"ITEM-9R873787D1610780X"
,
"name"
:
"Yoga Mat"
,
"description"
:
"new watch"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"id"
:
"TAX-9R873787D1610780X"
,
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
,
"tax_note"
:
"Reduced tax rate"
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
"3.27"
}
}
,
"discount"
:
{
"percent"
:
"5"
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
"2.5"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"id"
:
"ITEM-4XD34145EH4061035"
,
"name"
:
"Yoga T Shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"id"
:
"TAX-4XD34145EH4061035"
,
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.34"
}
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
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
"74.21"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"60.00"
}
,
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.73"
}
}
}
,
"discount"
:
{
"item_discount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"-7.50"
}
,
"invoice_discount"
:
{
"percent"
:
"5"
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
"-2.63"
}
}
}
,
"tax_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"4.34"
}
}
}
}
,
"settings"
:
{
"template_item_settings"
:
[
{
"field_name"
:
"items.date"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"items.discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.tax"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.description"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.quantity"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_subtotal_settings"
:
[
{
"field_name"
:
"custom"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"shipping"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"PROJECT_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_policy_and_agreement_settings"
:
[
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"PAYMENT_TERMS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"RETURN_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_AGREEMENT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"TERMS_AND_CONDITIONS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_additional_settings"
:
[
{
"field_name"
:
"REFERENCE"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"MEMO"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
}
,
"unit_of_measure"
:
"QUANTITY"
,
"standard_template"
:
false
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
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
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
]
}
Fully update template
put
/v2/invoicing/templates/{template_id}
Try it
Fully updates a template, by ID. In the JSON request body, include a complete
template
object. This call does not support partial updates.
Security
Oauth2
Request
path
Parameters
template_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the template for which to show details.
Request Body schema:
application/json
required
A representation of changes to make in the template.
name
string
[ 1 .. 500 ] characters
^[\S\s]*$
The template name.
Note:
The template name must be unique.
description
string
[ 1 .. 160 ] characters
^[\S\s]*$
The detailed description of the template.
default_template
boolean
Indicates whether this template is the default template. A invoicer can have one default template.
template_info
object
(
template_info
)
The template details. Includes invoicer business information, invoice recipients, items, and configuration.
settings
object
(
template_settings
)
The template settings. Describes which fields to show or hide when you create an invoice.
unit_of_measure
string
(
unit_of_measure
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The unit of measure for the invoiced item.
Enum Value
Description
QUANTITY
The unit of measure is quantity. This invoice template is typically used for physical goods.
HOURS
The unit of measure is hours. This invoice template is typically used for services.
AMOUNT
The unit of measure is amount. This invoice template is typically used when only amount is required.
Responses
200
A successful request returns the HTTP
200 OK
status code. A JSON response body that shows template details is returned if you set
prefer=return=representation
.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
Sample 1 - 200 - Update Template with Theme
Sample 1 - 200 - Update Template with Theme
Copy
Expand all
Collapse all
{
"description"
:
"Template description updated"
,
"default_template"
:
true
,
"template_info"
:
{
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"show_additional_item_fields"
:
false
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
,
"detail"
:
{
"reference"
:
"deal-reference-value"
,
"note"
:
"Thank you for your business."
,
"currency_code"
:
"USD"
,
"terms_and_conditions"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"attachments"
:
[
{
"id"
:
"Screen Shot 2018-11-23 at 16.45.01.png"
,
"reference_url"
:
"
https://example.com/invoice/payerView/attachments/RkG9ggQbd4Mwm1tYdcF6uuixfFTFq32bBdbE1VbtQLdKSoS2ZOYpfjw9gPp7eTrZmVaFaDWzixHXm-OXWHbmigHigHzURDxJs8IIKqcqP8jawnBEZcraEAPVMULxf5iTyOSpAUc2ugW0PWdwDbM6mg-guFAUyj3Z98H7htWNjQY95jb9heOlcSXUe.sbDUR9smAszzzJoA1NXT6rEEegwQ&version=1&sig=JNODB0xEayW8txMQm6ZsIwDnd4eh3hd6ijiRLi4ipHE
"
}
]
,
"payment_term"
:
{
"term_type"
:
"NET_10"
}
,
"service_agreement"
:
"This agreement covers the terms of the provided consulting services."
,
"tip_presets"
:
[
{
"percent"
:
"10"
}
,
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
]
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"www.test.com"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"additional_info"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"additional_recipients"
:
[
"
[email protected]
"
]
,
"items"
:
[
{
"name"
:
"Yoga Mat"
,
"description"
:
"new watch"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
,
"tax_note"
:
"Reduced tax rate"
}
,
"discount"
:
{
"percent"
:
"5"
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"name"
:
"Yoga T Shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
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
"74.21"
,
"breakdown"
:
{
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
}
}
,
"discount"
:
{
"invoice_discount"
:
{
"percent"
:
"5"
}
}
}
}
}
,
"settings"
:
{
"template_item_settings"
:
[
{
"field_name"
:
"items.date"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"items.discount"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"items.tax"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.description"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.quantity"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_subtotal_settings"
:
[
{
"field_name"
:
"custom"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"shipping"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"PROJECT_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_policy_and_agreement_settings"
:
[
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"PAYMENT_TERMS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"RETURN_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_AGREEMENT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"TERMS_AND_CONDITIONS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_additional_settings"
:
[
{
"field_name"
:
"REFERENCE"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"MEMO"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
}
,
"unit_of_measure"
:
"QUANTITY"
,
"standard_template"
:
false
}
Response samples
200
application/json
Sample 1 - 200 - Update Template with Theme
Sample 1 - 200 - Update Template with Theme
Copy
Expand all
Collapse all
{
"id"
:
"TEMP-19V05281TU309413B"
,
"name"
:
"reference-temp"
,
"description"
:
"Template description updated"
,
"default_template"
:
true
,
"template_info"
:
{
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"show_additional_item_fields"
:
false
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"20.00"
}
}
,
"theme"
:
{
"primary_color"
:
"#4A90D9"
}
}
,
"detail"
:
{
"reference"
:
"deal-reference-value"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you for your business."
,
"terms_and_conditions"
:
"No refunds after 30 days."
,
"memo"
:
"This is a long contract"
,
"attachments"
:
[
{
"id"
:
"Screen Shot 2018-11-23 at 16.45.01.png"
,
"reference_url"
:
"
https://api-m.paypal.com/invoice/payerView/attachments/RkG9ggQbd4Mwm1tYdcF6uuixfFTFq32bBdbE1VbtQLdKSoS2ZOYpfjw9gPp7eTrZmVaFaDWzixHXm-OXWHbmigHigHzURDxJs8IIKqcqP8jawnBEZcraEAPVMULxf5iTyOSpAUc2ugW0PWdwDbM6mg-guFAUyj3Z98H7htWNjQY95jb9heOlcSXUe.sbDUR9smAszzzJoA1NXT6rEEegwQ&version=1&sig=JNODB0xEayW8txMQm6ZsIwDnd4eh3hd6ijiRLi4ipHE
"
}
]
,
"payment_term"
:
{
"term_type"
:
"NET_10"
}
,
"service_agreement"
:
"This agreement covers the terms of the provided consulting services."
,
"tip_presets"
:
[
{
"percent"
:
"10"
}
,
{
"percent"
:
"15"
}
,
{
"percent"
:
"20"
}
]
,
"metadata"
:
{
"create_time"
:
"2018-12-03T03:38:46z"
}
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"David"
,
"surname"
:
"Larusso"
}
,
"address"
:
{
"address_line_1"
:
"1234 First Street"
,
"address_line_2"
:
"337673 Hillside Court"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4085551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"website"
:
"www.test.com"
,
"tax_id"
:
"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy-Jb5SeuGj185MNNw6g"
,
"logo_url"
:
"
https://example.com/logo.PNG
"
,
"additional_notes"
:
"2-4"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
,
"email_address"
:
"
[email protected]
"
,
"phones"
:
[
{
"country_code"
:
"001"
,
"national_number"
:
"4884551234"
,
"phone_type"
:
"MOBILE"
}
]
,
"additional_info"
:
"add-info"
}
,
"shipping_info"
:
{
"name"
:
{
"given_name"
:
"Stephanie"
,
"surname"
:
"Meyers"
}
,
"address"
:
{
"address_line_1"
:
"1234 Main Street"
,
"admin_area_2"
:
"Anytown"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"98765"
,
"country_code"
:
"US"
}
}
}
]
,
"additional_recipients"
:
[
"
[email protected]
"
]
,
"items"
:
[
{
"id"
:
"ITEM-9R873787D1610780X"
,
"name"
:
"Yoga Mat"
,
"description"
:
"new watch"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50.00"
}
,
"tax"
:
{
"id"
:
"TAX-9R873787D1610780X"
,
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"3.27"
}
}
,
"discount"
:
{
"percent"
:
"5"
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
"2.5"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
,
{
"id"
:
"ITEM-4XD34145EH4061035"
,
"name"
:
"Yoga T Shirt"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
,
"tax"
:
{
"id"
:
"TAX-4XD34145EH4061035"
,
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.34"
}
}
,
"discount"
:
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
"5.00"
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
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
"74.21"
,
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"60.00"
}
,
"custom"
:
{
"label"
:
"Packing Charges"
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
"10.00"
}
}
,
"shipping"
:
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
"10.00"
}
,
"tax"
:
{
"name"
:
"Sales Tax"
,
"percent"
:
"7.25"
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
"0.73"
}
}
}
,
"discount"
:
{
"item_discount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"-7.50"
}
,
"invoice_discount"
:
{
"percent"
:
"5"
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
"-2.63"
}
}
}
,
"tax_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"4.34"
}
}
}
}
,
"settings"
:
{
"template_invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"PROJECT_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_policy_and_agreement_settings"
:
[
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"PAYMENT_TERMS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"RETURN_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"SERVICE_AGREEMENT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"TERMS_AND_CONDITIONS"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_item_settings"
:
[
{
"field_name"
:
"items.date"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"items.discount"
,
"display_preference"
:
{
"hidden"
:
true
}
}
,
{
"field_name"
:
"items.tax"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.description"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"items.quantity"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"template_subtotal_settings"
:
[
{
"field_name"
:
"custom"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"discount"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"shipping"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_additional_settings"
:
[
{
"field_name"
:
"REFERENCE"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
,
{
"field_name"
:
"MEMO"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
}
,
"unit_of_measure"
:
"QUANTITY"
,
"standard_template"
:
false
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
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
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
]
}
Delete template
delete
/v2/invoicing/templates/{template_id}
Try it
Deletes a template, by ID.
Security
Oauth2
Request
path
Parameters
template_id
required
string
[ 0 .. 2147483647 ] characters
^.*$
The ID of the template to delete.
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
DELETE https://api-m.sandbox.paypal.com/v2/invoicing/templates/TEMP-19V05281TU309413B
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
Response samples
204
application/json
Sample 1 - 204 - Delete Template
Sample 1 - 204 - Delete Template
Copy
{ }
Setup auto reminder configuration.
post
/v2/invoicing/setup-reminders
Try it
Initializes the auto reminder configuration for a merchant account. This controller resource accepts an optional array of reminder configuration objects. A maximum of two reminder types are supported:
BEFORE_DUE
and
AFTER_DUE
.
Implementation behavior:
If both reminder types are provided in the request payload, both reminders are created using the supplied configuration and are set to
ACTIVE
state.
If only one reminder type is provided, the provided reminder is created using the supplied configuration and is set to
ACTIVE
state. The missing reminder type is automatically created using the default configuration and is set to
INACTIVE
state.
If the request payload is empty, both
BEFORE_DUE
and
AFTER_DUE
reminders are created using the default configuration and are set to
INACTIVE
state.
Default configuration values:
BEFORE_DUE
: interval_unit =
DAY
, interval_value = 2, repetition = 1, send_to_invoicer = false
AFTER_DUE
: interval_unit =
DAY
, interval_value = 2, repetition = 2, send_to_invoicer = false
Note:
After successful execution, both reminder configurations (
BEFORE_DUE
and
AFTER_DUE
) will exist for the merchant account. If reminder configurations already exist for the merchant account, the request fails with a
422 Unprocessable Entity
error.
Security
Oauth2
Request
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Request body for initializing invoice auto reminder configuration. The request may include up to two reminder configurations (BEFORE_DUE and AFTER_DUE), which will be applied to all invoices created by the merchant. If only one reminder type is provided, the missing reminder type will be created using the default configuration in INACTIVE state. If the request body is empty, both reminder types will be created using the default configuration in INACTIVE state. Reminder configurations created using the provided payload are set to ACTIVE state. If reminder configurations already exist for the merchant account, the request fails with a 422 Unprocessable Entity error.
configurations
Array of
objects
(
invoice_reminder_configuration
)
[ 1 .. 2 ] items
An array of invoice auto reminder configurations. The array can contain a maximum of two configurations, one for BEFORE_DUE reminder type and one for AFTER_DUE reminder type.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 200 - Setup auto reminder configuration - Success
Sample 1 - 200 - Setup auto reminder configuration - Success
Copy
Expand all
Collapse all
{
"configurations"
:
[
{
"type"
:
"BEFORE_DUE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
2
}
,
"repetition"
:
1
,
"notification"
:
{
"send_to_invoicer"
:
false
}
}
,
{
"type"
:
"AFTER_DUE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
2
}
,
"repetition"
:
2
,
"notification"
:
{
"send_to_invoicer"
:
false
}
}
]
}
Response samples
200
application/json
Sample 1 - 200 - Setup auto reminder configuration - Success
Sample 1 - 200 - Setup auto reminder configuration - Success
Copy
Expand all
Collapse all
{
"configurations"
:
[
{
"id"
:
"RC-239531651S471944P"
,
"type"
:
"BEFORE_DUE"
,
"status"
:
"ACTIVE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
2
}
,
"repetition"
:
1
,
"metadata"
:
{
"created_time"
:
"2026-01-28T03:31:53Z"
,
"updated_time"
:
"2026-01-28T03:31:53Z"
}
,
"notification"
:
{
"send_to_invoicer"
:
false
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P
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
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P/suspend
"
,
"rel"
:
"suspend"
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
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P/resume
"
,
"rel"
:
"resume"
,
"method"
:
"POST"
}
]
}
,
{
"id"
:
"RC-19C40543NJ101123L"
,
"type"
:
"AFTER_DUE"
,
"status"
:
"ACTIVE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
2
}
,
"repetition"
:
2
,
"metadata"
:
{
"created_time"
:
"2026-01-28T03:31:53Z"
,
"updated_time"
:
"2026-01-28T03:31:53Z"
}
,
"notification"
:
{
"send_to_invoicer"
:
false
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders/RC-19C40543NJ101123L
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
https://api-m.paypal.com/v2/invoicing/reminders/RC-19C40543NJ101123L
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders/RC-19C40543NJ101123L/suspend
"
,
"rel"
:
"suspend"
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
https://api-m.paypal.com/v2/invoicing/reminders/RC-19C40543NJ101123L/resume
"
,
"rel"
:
"resume"
,
"method"
:
"POST"
}
]
}
]
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders
"
,
"rel"
:
"collection"
,
"method"
:
"GET"
}
]
}
Retrieve an invoice auto reminder configuration
get
/v2/invoicing/reminders/{id}
Try it
Retrieves the details of a specific auto reminder configuration by providing its unique configuration ID. This operation returns comprehensive configuration information including the reminder type (BEFORE_DUE or AFTER_DUE), current status, timing interval settings, repetition count, notification preferences, metadata with creation and last update timestamps, and HATEOAS links for performing operations on the configuration.
Security
Oauth2
Request
path
Parameters
id
required
string
= 20 characters
^RC-[A-Z0-9]+$
The ID of the auto reminder configuration to be fetched.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v2/invoicing/reminders/RC-239531651S471944P
\
-H
'Content-Type: application/json'
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
Response samples
200
application/json
Sample 1 - 200 - Get auto reminder configuration - Success
Sample 1 - 200 - Get auto reminder configuration - Success
Copy
Expand all
Collapse all
{
"id"
:
"RC-239531651S471944P"
,
"type"
:
"BEFORE_DUE"
,
"status"
:
"ACTIVE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
2
}
,
"repetition"
:
1
,
"metadata"
:
{
"created_time"
:
"2026-01-28T03:31:53Z"
,
"updated_time"
:
"2026-01-28T03:31:53Z"
}
,
"notification"
:
{
"send_to_invoicer"
:
false
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P
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
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P/suspend
"
,
"rel"
:
"suspend"
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
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P/resume
"
,
"rel"
:
"resume"
,
"method"
:
"POST"
}
]
}
Update invoice auto reminder configuration.
put
/v2/invoicing/reminders/{id}
Try it
Updates an existing auto reminder configuration by providing the configuration ID and the updated settings in the request body. This operation allows modification of reminder timing intervals, repetition counts, and notification preferences. Note that this performs a full update of the configuration, so all required fields must be included in the request.
Security
Oauth2
Request
path
Parameters
id
required
string
= 20 characters
^RC-[A-Z0-9]+$
The ID of the auto reminder configuration to be updated.
header
Parameters
Prefer
string
[ 1 .. 16000 ] characters
^.*$
The Prefer request header field is used to indicate that particular server behavior is preferred by the client but is not required for successful completion of the request. For example, the value 'return=representation' indicates that the client prefers that the API server include an entity representing the current state of the resource in the response to a successful request.
Request Body schema:
application/json
required
The invoice reminder configuration note, frequency and send to invoicer fields to be updated.
type
required
string
(
reminder_type
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The type of the auto reminder configuration.
Enum Value
Description
BEFORE_DUE
Represents the auto reminder configuration for invoices prior to their due date.
AFTER_DUE
Represents the auto reminder configuration for invoices after their due date.
interval
required
object
(
Invoice auto reminder interval
)
Defines the time interval used to determine when a reminder is sent relative to the invoice due date. The interval consists of a unit (for example, DAY) and a numeric value that specifies how many units before or after the due date the reminder is triggered.
repetition
required
integer
[ 1 .. 7 ]
The repetition at which the auto reminder has to be set. Note: For
BEFORE_DUE
reminder type, repetition is always one.
notification
object
(
Notification
)
The email notification to send to the invoicer or payer on auto reminder configuration.
metadata
object
(
Invoice auto reminder configuration metadata.
)
Invoice auto reminder configuration metadata.
Responses
204
A successful request returns the HTTP
204 NO Content
status code.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
Sample 1 - 204 - Update auto reminder configuration - Success (No Content)
Sample 1 - 204 - Update auto reminder configuration - Success (No Content)
Copy
Expand all
Collapse all
{
"type"
:
"BEFORE_DUE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
1
}
,
"repetition"
:
1
}
Response samples
204
application/json
Sample 1 - 204 - Update auto reminder configuration - Success (No Content)
Sample 1 - 204 - Update auto reminder configuration - Success (No Content)
Copy
{ }
Get all invoice auto reminder configuration.
get
/v2/invoicing/reminders
Try it
Retrieves all auto reminder configurations associated with the merchant account. This operation returns both BEFORE_DUE and AFTER_DUE reminder configurations, regardless of their current status (ACTIVE or INACTIVE). Each configuration includes complete details such as timing intervals, repetition counts, notification preferences, status information, creation and update timestamps, and HATEOAS links for managing the configurations.
Security
Oauth2
Request
query
Parameters
type
string
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Filters reminder configurations by reminder type. If not provided, all reminder configurations (BEFORE_DUE and AFTER_DUE) are returned.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v2/invoicing/reminders?type
=
BEFORE_DUE
\
-H
'Content-Type: application/json'
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
Response samples
200
application/json
Sample 1 - 200 - Get auto reminder configurations by type - Success
Sample 1 - 200 - Get auto reminder configurations by type - Success
Copy
Expand all
Collapse all
{
"configurations"
:
[
{
"id"
:
"RC-239531651S471944P"
,
"type"
:
"BEFORE_DUE"
,
"status"
:
"ACTIVE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
2
}
,
"repetition"
:
1
,
"metadata"
:
{
"created_time"
:
"2026-01-28T03:31:53Z"
,
"updated_time"
:
"2026-01-28T03:31:53Z"
}
,
"notification"
:
{
"send_to_invoicer"
:
false
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P
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
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P/suspend
"
,
"rel"
:
"suspend"
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
https://api-m.paypal.com/v2/invoicing/reminders/RC-239531651S471944P/resume
"
,
"rel"
:
"resume"
,
"method"
:
"POST"
}
]
}
]
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/reminders?type=BEFORE_DUE
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
Suspend invoice auto reminder configuration.
post
/v2/invoicing/reminders/{id}/suspend
Try it
Temporarily deactivates an active auto reminder configuration by marking it as inactive. This operation stops all scheduled reminder notifications without deleting the configuration. All configuration settings are preserved and can be reactivated at any time using the resume endpoint. This is useful for temporarily pausing reminders during holidays, business closures, or while making adjustments to reminder strategies. A configuration can only be suspended when it is currently in an active state.
Security
Oauth2
Request
path
Parameters
id
required
string
= 20 characters
^RC-[A-Z0-9]+$
The unique identifier of the auto reminder configuration to be suspended.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
any
Responses
204
A successful request returns the HTTP
204 NO Content
status code.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 204 - Suspend auto reminder configuration - Success
Sample 1 - 204 - Suspend auto reminder configuration - Success
Copy
{ }
Response samples
204
application/json
Sample 1 - 204 - Suspend auto reminder configuration - Success
Sample 1 - 204 - Suspend auto reminder configuration - Success
Copy
{ }
Resume invoice auto reminder configuration.
post
/v2/invoicing/reminders/{id}/resume
Try it
This operation activates the auto reminder configuration. When a suspended configuration is resumed, reminder notifications will be sent for invoices that have invoice-level auto-reminders enabled and still have future scheduled reminder dates. Invoices issued during the suspension period are eligible only if their reminder schedules remain valid. This applies only to invoices with auto-reminders enabled. If reminders were explicitly canceled for an invoice, no reminder notifications will be sent.
Security
Oauth2
Request
path
Parameters
id
required
string
= 20 characters
^RC-[A-Z0-9]+$
The unique identifier of the auto reminder configuration to be reactivated.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
any
Responses
204
A successful request returns the HTTP
204 NO Content
status code.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 204 - Resume auto reminder configuration - Success
Sample 1 - 204 - Resume auto reminder configuration - Success
Copy
{ }
Response samples
204
application/json
Sample 1 - 204 - Resume auto reminder configuration - Success
Sample 1 - 204 - Resume auto reminder configuration - Success
Copy
{ }
Cancel auto reminders for an invoice.
post
/v2/invoicing/invoices/{id}/cancel-reminders
Try it
Cancels all scheduled automatic reminders for a specific invoice. This operation is permanent and cannot be reversed - once reminders are cancelled for an invoice, they cannot be re-enabled. The specified invoice will no longer receive automated reminder notifications, while other invoices continue to follow the active reminder configuration. This is typically used when a customer has requested no further reminders, payment arrangements have been made outside the system, or manual communication is preferred for sensitive situations.
Security
Oauth2
Request
path
Parameters
id
required
string
= 24 characters
^INV2-[A-Z0-9-]+$
The ID of the invoice for which reminders have to be canceled.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
any
Responses
204
A successful request returns the HTTP
204 NO Content
status code.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 204 - Cancel auto reminders for an invoice - Success
Sample 1 - 204 - Cancel auto reminders for an invoice - Success
Copy
{ }
Response samples
204
application/json
Sample 1 - 204 - Cancel auto reminders for an invoice - Success
Sample 1 - 204 - Cancel auto reminders for an invoice - Success
Copy
{ }
Create a recurring invoice series
post
/v2/invoicing/recurring-invoices
Try it
Creates a recurring invoice series that automatically generates and sends invoices to customers on a scheduled basis. The series includes the invoice template, billing frequency, payment terms, recipient information, line items and other invoice configuration. Once activated, invoices are sent according to the configured schedule until the series expires or is cancelled.
Security
Oauth2
Request
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
required
The recurring invoice series configuration including the invoice template, billing frequency, payment terms, recipient information, line items and other invoice configuration.
plan_detail
required
object
(
plan
)
The schedule and frequency configuration that controls when invoices are automatically generated and sent to customers.
recurring_info
required
object
(
recurring_info
)
The complete invoice template information used for generating each invoice in the series, including line items, recipients, and amount calculations.
Responses
200
OK
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 200 - Create recurring invoice series - Success response
Sample 1 - 200 - Create recurring invoice series - Success response
Copy
Expand all
Collapse all
{
"plan_detail"
:
{
"total_cycles"
:
6
,
"frequency"
:
{
"interval_unit"
:
"MONTH"
,
"interval_count"
:
1
}
,
"start_series_date"
:
"2026-01-19"
}
,
"recurring_info"
:
{
"detail"
:
{
"reference"
:
"0001"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you"
,
"terms_and_conditions"
:
"Your terms and conditions"
,
"memo"
:
"Gift pack"
,
"category_code"
:
"SHIPPABLE"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
}
}
,
"primary_recipients"
:
[
{
"billing_info"
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
"items"
:
[
{
"name"
:
"pen"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"2.00"
}
}
}
}
}
Response samples
200
application/json
Sample 1 - 200 - Create recurring invoice series - Success response
Sample 1 - 200 - Create recurring invoice series - Success response
Copy
Expand all
Collapse all
{
"id"
:
"RI-8K163274UC7208201"
,
"status"
:
"DRAFT"
,
"plan_detail"
:
{
"total_cycles"
:
6
,
"frequency"
:
{
"interval_unit"
:
"MONTH"
,
"interval_count"
:
1
}
,
"start_series_date"
:
"2026-01-19"
,
"completed_cycles"
:
0
}
,
"recurring_info"
:
{
"detail"
:
{
"reference"
:
"0001"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you"
,
"terms_and_conditions"
:
"Your terms and conditions"
,
"memo"
:
"Gift pack"
,
"category_code"
:
"SHIPPABLE"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
}
}
,
"primary_recipients"
:
[
{
"billing_info"
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
"items"
:
[
{
"id"
:
"ITEM-3LD558161T864042C"
,
"name"
:
"pen"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"2.00"
}
}
,
"template_id"
:
"TEMP-1B23377148371954V"
}
,
"amount"
:
{
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
,
"discount"
:
{
"invoice_discount"
:
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
"0.00"
}
}
,
"item_discount"
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
}
,
"tax_total"
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
}
,
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
}
,
"metadata"
:
{
"create_time"
:
"2026-01-20T05:17:06Z"
,
"last_update_time"
:
"2026-01-20T05:17:06Z"
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201
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
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201/cancel
"
,
"rel"
:
"cancel"
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
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201/activate
"
,
"rel"
:
"activate"
,
"method"
:
"POST"
}
]
}
Get recurring invoice series details
get
/v2/invoicing/recurring-invoices/{id}
Try it
Shows details for a recurring invoice series by ID.
Security
Oauth2
Request
path
Parameters
id
required
string
= 20 characters
^(RI-)[A-Z0-9]+$
The ID of the recurring series for which to retrieve details.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body containing the complete series details.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v2/invoicing/recurring-invoices/RI-9Y6699772R098892C
\
-H
'Content-Type: application/json'
\
-H
'Authorization: Bearer A21AALq82Dkuikd-KfWyoN1zEdj3pgI3t99_k6F4eozQifxXIbTedxdYNfWmMmF-H_s82ujWeg8Ad_B8cylTajLdgyIuHPuQB'
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Get recurring invoice series - Success response
Sample 1 - 200 - Get recurring invoice series - Success response
Copy
Expand all
Collapse all
{
"id"
:
"RI-9Y6699772R098892C"
,
"status"
:
"DRAFT"
,
"plan_detail"
:
{
"total_cycles"
:
1
,
"frequency"
:
{
"interval_unit"
:
"MONTH"
,
"interval_count"
:
1
}
,
"start_series_date"
:
"2026-01-20"
,
"completed_cycles"
:
0
}
,
"recurring_info"
:
{
"detail"
:
{
"reference"
:
"0001"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you"
,
"terms_and_conditions"
:
"Your terms and conditions"
,
"memo"
:
"Gift pack"
,
"category_code"
:
"SHIPPABLE"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
}
}
,
"primary_recipients"
:
[
{
"billing_info"
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
"items"
:
[
{
"id"
:
"ITEM-69D690885J782781N"
,
"name"
:
"pen"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"2.00"
}
}
,
"template_id"
:
"TEMP-1B23377148371954V"
}
,
"amount"
:
{
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
,
"discount"
:
{
"invoice_discount"
:
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
"0.00"
}
}
,
"item_discount"
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
}
,
"tax_total"
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
}
,
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
}
,
"metadata"
:
{
"create_time"
:
"2026-01-20T09:55:09Z"
,
"last_update_time"
:
"2026-01-20T09:55:09Z"
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-9Y6699772R098892C
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
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-9Y6699772R098892C
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-9Y6699772R098892C
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-9Y6699772R098892C/cancel
"
,
"rel"
:
"cancel"
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
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-9Y6699772R098892C/activate
"
,
"rel"
:
"activate"
,
"method"
:
"POST"
}
]
}
Update recurring invoice series details
put
/v2/invoicing/recurring-invoices/{id}
Try it
Fully updates a recurring invoice series by ID. In the JSON request body, include a complete recurring series object. This call does not support partial updates.
Security
Oauth2
Request
path
Parameters
id
required
string
= 20 characters
^(RI-)[A-Z0-9]+$
The ID of the recurring series to be updated.
Request Body schema:
application/json
required
The recurring invoice series configuration to be updated.
plan_detail
required
object
(
plan
)
The schedule and frequency configuration that controls when invoices are automatically generated and sent to customers.
recurring_info
required
object
(
recurring_info
)
The complete invoice template information used for generating each invoice in the series, including line items, recipients, and amount calculations.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body containing the updated series details.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
Sample 1 - 200 - Update already active recurring invoice series - Success response
Sample 1 - 200 - Update already active recurring invoice series - Success response
Copy
Expand all
Collapse all
{
"plan_detail"
:
{
"total_cycles"
:
8
,
"frequency"
:
{
"interval_unit"
:
"MONTH"
,
"interval_count"
:
2
}
,
"start_series_date"
:
"2026-01-19"
}
,
"recurring_info"
:
{
"detail"
:
{
"reference"
:
"0002"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you"
,
"terms_and_conditions"
:
"Your terms and conditions"
,
"memo"
:
"Gift pack"
,
"category_code"
:
"SHIPPABLE"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
}
}
,
"primary_recipients"
:
[
{
"billing_info"
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
"items"
:
[
{
"name"
:
"pen"
,
"quantity"
:
"2"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"2.00"
}
}
}
}
}
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Update already active recurring invoice series - Success response
Sample 1 - 200 - Update already active recurring invoice series - Success response
Copy
Expand all
Collapse all
{
"id"
:
"RI-9Y6699772R098892C"
,
"status"
:
"ACTIVE"
,
"plan_detail"
:
{
"total_cycles"
:
8
,
"frequency"
:
{
"interval_unit"
:
"MONTH"
,
"interval_count"
:
1
}
,
"start_series_date"
:
"2026-01-19"
,
"completed_cycles"
:
0
}
,
"recurring_info"
:
{
"detail"
:
{
"reference"
:
"0001"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you"
,
"terms_and_conditions"
:
"Your terms and conditions"
,
"memo"
:
"Gift pack"
,
"category_code"
:
"SHIPPABLE"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
}
}
,
"primary_recipients"
:
[
{
"billing_info"
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
"items"
:
[
{
"id"
:
"ITEM-3LD558161T864042C"
,
"name"
:
"pen"
,
"quantity"
:
"1"
,
"unit_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
true
,
"partial_payment"
:
{
"allow_partial_payment"
:
true
,
"minimum_amount_due"
:
{
"currency_code"
:
"USD"
,
"value"
:
"2.00"
}
}
,
"template_id"
:
"TEMP-1B23377148371954V"
}
,
"amount"
:
{
"breakdown"
:
{
"item_total"
:
{
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
,
"discount"
:
{
"invoice_discount"
:
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
"0.00"
}
}
,
"item_discount"
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
}
,
"tax_total"
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
}
,
"currency_code"
:
"USD"
,
"value"
:
"12.00"
}
}
,
"metadata"
:
{
"create_time"
:
"2026-01-20T05:17:06Z"
,
"last_update_time"
:
"2026-01-20T05:17:06Z"
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201
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
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201
"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201/cancel
"
,
"rel"
:
"cancel"
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
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-8K163274UC7208201/activate
"
,
"rel"
:
"activate"
,
"method"
:
"POST"
}
]
}
Delete recurring invoice series
delete
/v2/invoicing/recurring-invoices/{id}
Try it
Deletes a recurring invoice series by ID.
Security
Oauth2
Request
path
Parameters
id
required
string
= 20 characters
^(RI-)[A-Z0-9]+$
The ID of the recurring series to be deleted.
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
DELETE https://api-m.sandbox.paypal.com/v2/invoicing/recurring-invoices/RI-9Y6699772R098892C
\
-H
'Content-Type: application/json'
\
-H
'Authorization: Bearer A21AALq82Dkuikd-KfWyoN1zEdj3pgI3t99_k6F4eozQifxXIbTedxdYNfWmMmF-H_s82ujWeg8Ad_B8cylTajLdgyIuHPuQB'
Response samples
204
application/json
Sample 1 - 204 - Delete recurring invoice series - Success response
Sample 1 - 204 - Delete recurring invoice series - Success response
Copy
{ }
Activate recurring invoice series
post
/v2/invoicing/recurring-invoices/{id}/activate
Try it
Activates a recurring invoice series by ID. Once activated, the system will start sending invoices based on the configured schedule.
Security
Oauth2
Request
path
Parameters
id
required
string
= 20 characters
^(RI-)[A-Z0-9]+$
The ID of the recurring series to activate.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
any
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 204 - Activate recurring invoice series - Success response
Sample 1 - 204 - Activate recurring invoice series - Success response
Copy
{ }
Response samples
204
application/json
Sample 1 - 204 - Activate recurring invoice series - Success response
Sample 1 - 204 - Activate recurring invoice series - Success response
Copy
{ }
Cancel an active recurring invoice series
post
/v2/invoicing/recurring-invoices/{id}/cancel
Try it
Cancels a recurring invoice series by ID.
Security
Oauth2
Request
path
Parameters
id
required
string
= 20 characters
^(RI-)[A-Z0-9]+$
The ID of the recurring series to cancel.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
any
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 204 - Cancel recurring invoice series - Success response
Sample 1 - 204 - Cancel recurring invoice series - Success response
Copy
{ }
Response samples
204
application/json
Sample 1 - 204 - Cancel recurring invoice series - Success response
Sample 1 - 204 - Cancel recurring invoice series - Success response
Copy
{ }
Search recurring invoice series
post
/v2/invoicing/search-recurring-invoices
Try it
Searches for and lists recurring invoice series that match search criteria. Users can search only for the past 3 years.
Security
Oauth2
Request
query
Parameters
page
integer
[ 1 .. 1000 ]
Default:
1
The page number to be retrieved.
page_size
integer
[ 1 .. 100 ]
Default:
20
The maximum number of results to return.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
The search criteria used to retrieve recurring invoice series.
search_text
string
[ 3 .. 800 ] characters
^(?!\s*$).+
Describes the search text, which will be used to check if this particular search_text present in any of the recurring invoice series fields, specified by search_fields.
search_fields
Array of
strings
(
recurring_series_free_text_search_fields
)
[ 1 .. 5 ] items
unique
Describes the set of fields on which the search will be performed.
Note:
If
search_fields
is provided with a single value 'ALL', the search will be performed across all the available fields in [search fields] (/recurring_series_free_text_search_fields.json).
Items
Enum Value
Description
NOTES
Notes associated with the recurring invoices series.
MERCHANT_MEMO
Merchant memo related to the recurring invoices series.
PAYER_REFERENCE_INFO
Payer's reference information.
BILLING_EMAIL
Email address associated with billing.
BILLING_NAME
Name associated with billing.
BILLING_BUSINESS_NAME
Business name associated with billing.
BILLING_PHONE_NUMBER
Phone number associated with billing.
SHIPPING_NAME
Name associated with shipping.
SHIPPING_BUSINESS_NAME
Business name associated with shipping.
SHIPPING_PHONE_NUMBER
Phone number associated with shipping.
ITEM_NAME
Name of the recurring invoices series item.
ITEM_TAX_NAME
Tax name associated with the recurring invoices series item.
ITEM_DISCOUNT_NAME
Discount name associated with the recurring invoices series item.
INVOICE_DISCOUNT_NAME
Discount name associated with the recurring invoices series.
ALL
Search in all available search fields.
search_filters
object
(
Search filters properties.
)
Search filters - to retrieve recurring invoices series.
Note:
This API currently supports only one criterion for range queries, so specify only one of the following criteria: creation_date_range or next_occurrence_date_range.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that lists the recurring invoice series that match the search criteria.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 200 - Search recurring invoices series - Multiple filters.
Sample 1 - 200 - Search recurring invoices series - Multiple filters.
Copy
Expand all
Collapse all
{
"search_filters"
:
{
"creation_date_range"
:
{
"start"
:
"2026-01-01T00:00:00Z"
,
"end"
:
"2026-10-25T23:59:59Z"
}
,
"total_amount_range"
:
{
"lower_amount"
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
"upper_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.00"
}
}
}
}
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Search recurring invoices series - Multiple filters.
Sample 1 - 200 - Search recurring invoices series - Multiple filters.
Copy
Expand all
Collapse all
{
"recurring_invoices"
:
[
{
"id"
:
"RI-2U547903SN493514L"
,
"status"
:
"DRAFT"
,
"plan_detail"
:
{
"total_cycles"
:
1
,
"frequency"
:
{
"interval_unit"
:
"MONTH"
,
"interval_count"
:
1
}
,
"start_series_date"
:
"2026-01-22"
}
,
"recurring_info"
:
{
"detail"
:
{
"reference"
:
"0001"
,
"currency_code"
:
"USD"
,
"note"
:
"Thank you"
,
"memo"
:
"Gift pack"
}
,
"invoicer"
:
{
"name"
:
{
"given_name"
:
"--"
}
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"email_address"
:
"
[email protected]
"
}
,
"shipping_info"
:
{ }
}
]
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
"10.00"
}
}
,
"metadata"
:
{
"create_time"
:
"2026-01-21T20:50:43Z"
}
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-2U547903SN493514L
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
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-2U547903SN493514L
"
,
"rel"
:
"update"
,
"method"
:
"PUT"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-2U547903SN493514L
"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/recurring-invoices/RI-2U547903SN493514L/activate
"
,
"rel"
:
"activate"
,
"method"
:
"POST"
}
]
}
]
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v2/invoicing/search-recurring-invoices?page=1&page_size=10
"
,
"rel"
:
"self"
,
"method"
:
"POST"
}
]
}
List conditional rules for invoice
get
/v2/invoicing/invoices/{id}/conditional-rules
Try it
Retrieves all conditional rules for a given invoice. The response includes a list of conditional rules associated with the invoice, along with their details such as rule type, value, and expiry terms.
Security
Oauth2
Request
path
Parameters
id
required
string
= 24 characters
^INV2-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-...
Show pattern
The ID of the invoice for which to show conditional rule details.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
any
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows conditional rules details for the invoice.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Copy
{ }
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Get conditional rules for the Invoice
Sample 1 - 200 - Get conditional rules for the Invoice
Copy
Expand all
Collapse all
{
"rules"
:
[
{
"conditional_rule_id"
:
"CR-11FF-A725-27C6999C-A699-33CD614E75ED"
,
"conditional_rule_type"
:
"EARLY_PAYMENT_DISCOUNT"
,
"conditional_rule_value_type"
:
"PERCENT"
,
"conditional_rule_value"
:
"5"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"SEVEN_DAYS_AFTER_ISSUE_DATE"
,
"condition_rule_end_date"
:
"2025-03-12"
}
,
"created_time"
:
"2025-01-29T10:15:30Z"
,
"updated_time"
:
"2025-01-29T10:15:30Z"
,
"links"
:
[
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75ED"
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
"rel"
:
"self"
,
"href"
:
"
https://api.paypal.com/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C
"
,
"method"
:
"GET"
}
,
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75ED"
,
"rel"
:
"update"
,
"method"
:
"PUT"
}
,
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75ED"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
]
}
,
{
"conditional_rule_id"
:
"CR-11FF-A725-27C6999C-A699-33CD614E75EC"
,
"conditional_rule_type"
:
"AUTO_CANCEL"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"SPECIFIC_DATE"
,
"condition_rule_end_date"
:
"2025-03-12"
}
,
"created_time"
:
"2025-01-29T10:15:30Z"
,
"updated_time"
:
"2025-01-29T10:15:30Z"
,
"links"
:
[
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75EC"
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
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75EC"
,
"rel"
:
"update"
,
"method"
:
"PUT"
}
,
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75EC"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
]
}
]
,
"links"
:
[
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules"
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
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C"
,
"rel"
:
"invoice"
,
"method"
:
"GET"
}
]
}
Create conditional rules
post
/v2/invoicing/invoices/{id}/conditional-rules
Try it
Creates conditional rules for the invoice.
Security
Oauth2
Request
path
Parameters
id
required
string
= 24 characters
^INV2-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-...
Show pattern
The ID of the invoice for which the conditional rules are to be created.
header
Parameters
PayPal-Request-Id
required
string
[ 1 .. 255 ] characters
^.*$
The server stores keys for 1 hour.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
The conditional rules details which include all information of the rules to apply for the invoice.
Responses
201
A successful request returns the HTTP
201 Created
status code and a JSON response body that shows conditional rules.
Request samples
Payload
cURL
Node.js
Java
Python
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Sample 1 - 201 - Creating conditional rules for invoice
Sample 1 - 201 - Creating conditional rules for invoice
Copy
Expand all
Collapse all
{
"rules"
:
[
{
"conditional_rule_type"
:
"EARLY_PAYMENT_DISCOUNT"
,
"conditional_rule_value_type"
:
"PERCENT"
,
"conditional_rule_value"
:
"5"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"SEVENTY_DAYS_AFTER_ISSUE_DATE"
,
"condition_rule_end_date"
:
"2025-03-12"
}
}
,
{
"conditional_rule_type"
:
"AUTO_CANCEL"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"SPECIFIC_DATE"
,
"condition_rule_end_date"
:
"2025-03-12"
}
}
]
}
Response samples
201
application/json
multipart/mixed
application/json
Sample 1 - 201 - Creating conditional rules for invoice
Sample 1 - 201 - Creating conditional rules for invoice
Copy
Expand all
Collapse all
{
"rules"
:
[
{
"conditional_rule_id"
:
"CR-11FF-A725-27C6999C-A699-33CD614E75EC"
,
"conditional_rule_type"
:
"EARLY_PAYMENT_DISCOUNT"
,
"conditional_rule_value_type"
:
"PERCENT"
,
"conditional_rule_value"
:
"5"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"SEVEN_DAYS_AFTER_ISSUE_DATE"
,
"condition_rule_end_date"
:
"2025-03-12"
}
,
"created_time"
:
"2025-01-29T10:15:30Z"
,
"updated_time"
:
"2025-01-29T10:15:30Z"
,
"links"
:
[
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75E"
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
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75E"
,
"rel"
:
"update"
,
"method"
:
"PUT"
}
,
{
"href"
:
"v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75E"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
]
}
,
{
"conditional_rule_id"
:
"CR-11FF-A725-27C6999C-A699-33CD614E75ED"
,
"conditional_rule_type"
:
"AUTO_CANCEL"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"SPECIFIC_DATE"
,
"condition_rule_end_date"
:
"2025-03-12"
}
,
"created_time"
:
"2025-01-29T10:15:30Z"
,
"updated_time"
:
"2025-01-29T10:15:30Z"
,
"links"
:
[
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75D"
,
"rel"
:
"GET_BY_CR_ID"
,
"method"
:
"GET"
}
,
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75D"
,
"rel"
:
"update"
,
"method"
:
"PUT"
}
,
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75D"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
]
}
]
,
"links"
:
[
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules"
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
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C"
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
Show conditional rule details
get
/v2/invoicing/invoices/{id}/conditional-rules/{conditional_rule_id}
Try it
Shows details for a conditional rule, by invoice ID and conditional rule ID.
Security
Oauth2
Request
path
Parameters
id
required
string
= 24 characters
^INV2-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-...
Show pattern
The ID of the invoice for which to show conditional rule details.
conditional_rule_id
required
string
= 40 characters
^CR-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]...
Show pattern
The conditional rule ID of the invoice for which to retrieve details.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows conditional rule details.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75EC
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
\
-H
'Content-Type: application/json'
Response samples
200
application/json
multipart/mixed
application/json
Sample 1 - 200 - Get conditional rule by id for the Invoice
Sample 1 - 200 - Get conditional rule by id for the Invoice
Copy
Expand all
Collapse all
{
"conditional_rule_id"
:
"CR-11FF-A725-27C6999C-A699-33CD614E75EC"
,
"conditional_rule_type"
:
"EARLY_PAYMENT_DISCOUNT"
,
"conditional_rule_value_type"
:
"PERCENT"
,
"conditional_rule_value"
:
"5"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"SEVEN_DAYS_AFTER_ISSUE_DATE"
,
"condition_rule_end_date"
:
"2025-03-12"
}
,
"created_time"
:
"2025-01-29T10:15:30Z"
,
"updated_time"
:
"2025-01-29T10:15:30Z"
,
"links"
:
[
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75EC"
,
"rel"
:
"replace"
,
"method"
:
"PUT"
}
,
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75EC"
,
"rel"
:
"delete"
,
"method"
:
"DELETE"
}
,
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C"
,
"rel"
:
"up"
,
"method"
:
"GET"
}
,
{
"href"
:
"/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75EC"
,
"rel"
:
"self"
,
"method"
:
"GET_BY_CR_ID"
}
]
}
Fully update conditional rule
put
/v2/invoicing/invoices/{id}/conditional-rules/{conditional_rule_id}
Try it
Fully updates a conditional rule for the invoice, by invoice ID and conditional rule ID. In the JSON request body, include a complete conditional rule object. This call does not support partial updates.
Security
Oauth2
Request
path
Parameters
id
required
string
= 24 characters
^INV2-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-...
Show pattern
The ID of the invoice for which to update the conditional rule.
conditional_rule_id
required
string
= 40 characters
^CR-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]...
Show pattern
The conditional rule ID to update.
Request Body schema:
application/json
required
The conditional rule details which include all information of the rule to apply for the invoice.
conditional_rule_value
string
[ 1 .. 32 ] characters
^(([0-9]+)|(([0-9]+)?[.][0-9]+))$
Represents the value of the conditional rule it can be a percentage or absolute value. In case of absolute value, which might be:
An integer for currencies like
JPY
that are not typically fractional.
A decimal fraction for currencies like
TND
that are subdivided into thousandths.
For the required number of decimal places for a currency code, see
Currency Codes
.
conditional_rule_type
required
string
(
conditional_rule_type
)
[ 1 .. 30 ] characters
^[A-Z0-9_]*$
The type of conditional rule applied to the invoice.
Enum Value
Description
EARLY_PAYMENT_DISCOUNT
A discount applied if the invoice is paid before a specified date or within a certain period after the issue date.
LATE_PAYMENT_SURCHARGE
A surcharge applied if the invoice is paid after the due date or a specified period after the due date.
AUTO_CANCEL
A rule to automatically cancel the invoice if it is not paid by a specified date or a certain period after the due date.
conditional_rule_value_type
string
(
conditional_rule_value_type
)
[ 1 .. 20 ] characters
^[A-Z0-9_]*$
The value type that indicates how the conditional rule value is applied. Use
PERCENT
for a percentage-based discount or
AMOUNT
for an absolute currency value.
Enum Value
Description
PERCENT
Percentage of discount used in invoice item or in an invoice.
AMOUNT
An absolute value of discount used in invoice item or in an invoice based on the currency in invoice.
rule_expiry_terms
required
object
(
conditional_rules
)
The expiry terms that define when the conditional rule becomes inactive.
Responses
204
No Content
Request samples
Payload
cURL
Node.js
Java
Python
application/json
Sample 1 - 204 - Updating conditional rule
Sample 1 - 204 - Updating conditional rule
Copy
Expand all
Collapse all
{
"conditional_rule_type"
:
"EARLY_PAYMENT_DISCOUNT"
,
"conditional_rule_value_type"
:
"PERCENT"
,
"conditional_rule_value"
:
"10"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"SEVEN_DAYS_AFTER_ISSUE_DATE"
,
"condition_rule_end_date"
:
"2025-03-12"
}
}
Response samples
204
application/json
Sample 1 - 204 - Updating conditional rule
Sample 1 - 204 - Updating conditional rule
Copy
{ }
Delete conditional rule
delete
/v2/invoicing/invoices/{id}/conditional-rules/{conditional_rule_id}
Try it
Deletes a conditional rule, by invoice ID and conditional rule ID.
Security
Oauth2
Request
path
Parameters
id
required
string
= 24 characters
^INV2-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-...
Show pattern
The ID of the invoice for which to delete the conditional rule.
conditional_rule_id
required
string
= 40 characters
^CR-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]...
Show pattern
The conditional rule ID to delete.
Responses
204
A successful request returns the HTTP
204 No Content
status code with no JSON response body.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
DELETE https://api-m.sandbox.paypal.com/v2/invoicing/invoices/INV2-S884-EJT6-73AU-QF4C/conditional-rules/CR-11FF-A725-27C6999C-A699-33CD614E75EC
\
-H
'Authorization: Bearer zekwhYgsYYI0zDg0p_Nf5v78VelCfYR0'
\
-H
'Content-Type: application/json'
Response samples
204
application/json
Sample 1 - 204 - Deactivate the conditional rule for the Invoice
Sample 1 - 204 - Deactivate the conditional rule for the Invoice
Copy
{ }
Definitions
Additional Detail
Optional additional business and descriptive details that can be associated with invoices, templates, and other resources.
reference
string
[ 1 .. 120 ] characters
^[\S\s]*$
The reference data. Includes a Purchase Order (PO) number.
note
string
[ 1 .. 4000 ] characters
^[\S\s]*$
A note to the invoice recipient. Also appears on the invoice notification email.
terms_and_conditions
string
[ 1 .. 4000 ] characters
^[\S\s]*$
The general terms of the invoice. Can include return or cancellation policy and other terms and conditions.
memo
string
[ 1 .. 500 ] characters
^[\S\s]*$
A private bookkeeping memo for the user.
attachments
Array of
objects
(
File Reference
)
[ 0 .. 2147483647 ] items
An array of PayPal IDs for the files that are attached to an invoice.
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
tip_presets
Array of
objects
(
tip_preset
)
[ 1 .. 3 ] items
Specifies the predefined tip options configured by the invoicer. These preset values are shown to customers at checkout as suggested tipping amounts, in addition to the option to enter a custom tip.
order_details
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Order details information.
project_details
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Project details information.
service_details
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Service details information.
payment_terms
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Payment terms information.
return_policy
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Return policy information.
cancellation_policy
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Cancellation policy information.
service_agreement
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Service agreement information.
Copy
Expand all
Collapse all
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"tip_presets"
:
[
{
"percent"
:
"19.99"
}
]
,
"order_details"
:
"string"
,
"project_details"
:
"string"
,
"service_details"
:
"string"
,
"payment_terms"
:
"string"
,
"return_policy"
:
"string"
,
"cancellation_policy"
:
"string"
,
"service_agreement"
:
"string"
}
aggregated_discount
The discount. Can be an item- or invoice-level discount, or both. Can be applied as a percent or amount. If you provide both amount and percent, amount takes precedent.
invoice_discount
object
(
discount
)
The discount as a percent or amount at invoice level. The invoice discount amount is subtracted from the item total.
item_discount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
aging_bucket
A single aging bucket containing invoice counts and totals for a specific time range.
from
integer
[ 0 .. 1000 ]
Inclusive lower bound in days; null when not applicable (e.g., NO_DUE).
to
integer
[ 0 .. 1000 ]
Inclusive upper bound in days; null if open-ended (e.g., NET_90+).
count
required
integer
[ 0 .. 2147483647 ]
Number of invoices in this bucket.
label
required
string
(
aging_bucket_label
)
[ 1 .. 100 ] characters
^[A-Z0-9_+]+$
Bucket label representing the aging time range.
Enum Value
Description
NO_DUE
Invoices with no due date or not yet due.
NET_30
Invoices due within 0-30 days.
NET_30_60
Invoices due within 31-60 days.
NET_60_90
Invoices due within 61-90 days.
NET_90
Invoices due more than 90 days.
total
required
object
(
Money
)
Total amount for invoices in this bucket, in the row currency.
Copy
Expand all
Collapse all
{
"from"
:
1000
,
"to"
:
1000
,
"count"
:
2147483647
,
"label"
:
"NO_DUE"
,
"total"
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
aging_bucket_label
Aging bucket label enum representing different time ranges for invoice aging analysis.
string
(
aging_bucket_label
)
[ 1 .. 100 ] characters
^[A-Z0-9_+]+$
Aging bucket label enum representing different time ranges for invoice aging analysis.
Enum Value
Description
NO_DUE
Invoices with no due date or not yet due.
NET_30
Invoices due within 0-30 days.
NET_30_60
Invoices due within 31-60 days.
NET_60_90
Invoices due within 61-90 days.
NET_90
Invoices due more than 90 days.
Copy
"NO_DUE"
aging_report_result_item
A single result item in the aging report representing aging buckets for a specific currency-status combination.
buckets
required
Array of
objects
(
aging_bucket
)
[ 1 .. 20 ] items
Aging buckets with counts and totals for this currency–status pair.
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
Three-letter ISO currency code for this summary item.
status
required
string
(
invoice_statuses_for_aggregation
)
[ 1 .. 100 ] characters
^[A-Z0-9_]+$
Invoice status for this summary item.
Enum Value
Description
OUTSTANDING
Invoices that are sent but not yet paid or only partially paid.
PAID
Invoices that have been fully paid.
Copy
Expand all
Collapse all
{
"buckets"
:
[
{
"from"
:
1000
,
"to"
:
1000
,
"count"
:
2147483647
,
"label"
:
"NO_DUE"
,
"total"
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
"currency"
:
"str"
,
"status"
:
"OUTSTANDING"
}
amount_range
The amount range.
lower_amount
required
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
upper_amount
required
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"lower_amount"
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
"upper_amount"
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
amount_summary_detail
The invoice amount summary of item total, discount, tax total, and shipping.
currency_code
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
amount_with_breakdown
)
The breakdown of the amount. Includes total item amount, total tax amount, custom amount, and shipping and discounts, if any.
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
,
"custom"
:
{
"label"
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
}
}
}
amount_with_breakdown
The breakdown of the amount. Includes total item amount, total tax amount, custom amount, and shipping and discounts, if any.
item_total
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
discount
object
(
aggregated_discount
)
The discount. Can be an item- or invoice-level discount, or both. Can be applied as a percent or amount. If you provide both amount and percent, amount takes precedent.
tax_total
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
shipping
object
(
shipping_cost
)
The shipping fee for all items. Includes tax on shipping.
custom
object
(
custom_amount
)
The custom amount to apply to an invoice. If you include a label, you must include a custom amount.
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
,
"custom"
:
{
"label"
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
}
}
An object representing a specific subscription plan info.
An object representing a specific subscription plan info.
id
string
= 39 characters
^PI-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{8}-[0-9A...
Show pattern
Subscription plan Id. This is a unique Id identifying all the versions in a given set of plans.
name
string
[ 1 .. 125 ] characters
^[A-Za-z0-9_ ]+$
The plan name.
Copy
{
"id"
:
"stringstringstringstringstringstringstr"
,
"name"
:
"string"
}
association_id
It is either a template ID or an invoice ID based on the type provided in the request.
string
(
association_id
)
[ 1 .. 30 ] characters
^(TEMP|INV2)-[A-Z0-9-]+$
It is either a template ID or an invoice ID based on the type provided in the request.
Copy
"string"
association_type
It is an association type, used to fetch theme details.
string
(
association_type
)
[ 1 .. 20 ] characters
^[A-Z0-9_]+$
It is an association type, used to fetch theme details.
Enum Value
Description
TEMPLATE
Fetch theme details for a given template.
INVOICE
Fetch theme details for a given invoice.
Copy
"TEMPLATE"
auto_cancellation
The auto cancellation details for the invoice. If the payer does not pay by the specified date, the invoice is automatically cancelled.
is_applied
boolean
Indicates whether the particular rule is applied or not.
cancel_by_date
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
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
base_configuration
The base configuration details. Includes tax information, tip, and partial payment.
tax_calculated_after_discount
boolean
Default:
true
Indicates whether the tax is calculated before or after a discount. If
false
, the tax is calculated before a discount. If
true
, the tax is calculated after a discount.
tax_inclusive
boolean
Default:
false
Indicates whether the unit price includes tax.
allow_tip
boolean
Default:
false
Indicates whether the invoice enables the customer to enter a tip amount during payment. If
true
, the invoice shows a tip amount field so that the customer can enter a tip amount. If
false
, the invoice does not show a tip amount field.
Note:
This feature is not available for users in
Hong Kong
,
Taiwan
,
India
, or
Japan
.
partial_payment
object
(
partial_payment
)
The partial payment details. Includes the minimum amount that the invoicer wants the payer to pay.
Copy
Expand all
Collapse all
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
batch_date_range
Filters between the start and end dates inclusive.
Both dates cannot be more than 1 month in the past.
Both dates cannot be more than 3 months from current date.
Start date should be before end date.
start_date
required
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
The start date of the range. Cannot be more than 1 month the past. Cannot be more than 3 months in the future. Cannot be after the end date.
end_date
required
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
The end date of the range. Cannot be more than 1 month the past. Cannot be more than 3 months in the future. Cannot be before the start date.
Copy
{
"start_date"
:
"stringstri"
,
"end_date"
:
"stringstri"
}
batch_task_summary
The details about the batch task.
id
string
(
id
)
= 40 characters
^(BAT-)1[0-9A-Z]{3}-[0-9A-Z]{4}-[0-9A-Z]{8}-[...
Show pattern
A unique id used to reference the batch task.
task_type
string
(
task_type
)
[ 1 .. 50 ] characters
^[A-Z0-9_]*$
Task type of the batch task. Used to determine the batch operation/logic to be performed.
Enum Value
Description
RISK_LIMIT_RECENT
Task for processing recent records for the account in Invoicing.
RISK_LIMIT_FULL
Task for processing all records in Invoicing.
task_date
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
The task date as specified by the sender, in
Internet date and time format
. Date cannot be in the past.
Copy
{
"id"
:
"stringstringstringstringstringstringstri"
,
"task_type"
:
"RISK_LIMIT_RECENT"
,
"task_date"
:
"stringstri"
}
billing_info
The billing information of the invoice recipient. Includes name, address, email, phone, and language.
business_name
string
<= 300 characters
Required. The business name of the party.
name
object
(
Name
)
The name of the party.
address
object
(
Portable Postal Address (Medium-Grained)
)
The portable international postal address. Maps to
AddressValidationMetadata
and HTML 5.1
Autofilling form controls: the autocomplete attribute
.
phones
Array of
objects
(
phone_detail
)
The invoice recipient's phone numbers. Extension number is not supported.
additional_info
string
<= 40 characters
Any additional information about the recipient.
email_address
string
(
restrictive_email_address
)
[ 3 .. 254 ] characters
^(?!\.)(?:[A-Za-z0-9!#$&'*\/=?^`{|}~_%+-]|\.(...
Show pattern
The internationalized email address with more restrictive rules. This version restricts the local-part to a dot-atom as defined in
https://www.ietf.org/rfc/rfc5322.txt
. It does not allow for a quoted-string or an obs-local-part.
Allows alphanumeric and RFC-allowed special characters, !#$%&'*+-/=?^_`{|}~
Ensures that the local part does not start with dot (.), have consecutive dots, or end with dot. Ensures that the domain part does not have consecutive dots.
Ensures that the local part does not exceed 64 characters.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
language
string
<
ppaas_common_language_v3
>
(
language
)
[ 2 .. 10 ] characters
^[a-z]{2}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}|[...
Show pattern
The
language tag
for the language in which to localize the error-related strings, such as messages, issues, and suggested actions. The tag is made up of the
ISO 639-2 language code
, the optional
ISO-15924 script tag
, and the
ISO-3166 alpha-2 country code
or
M49 region code
.
Copy
Expand all
Collapse all
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
Business Name
The business name of the party.
business_name
string
<= 300 characters
Required. The business name of the party.
Copy
{
"business_name"
:
"string"
}
Color hex code
This object defines the color hex code.
string
(
Color hex code
)
[ 4 .. 7 ] characters
^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$
This object defines the color hex code.
Copy
"string"
Conditional Rule
The conditional rule associated with an invoice that defines automated actions or adjustments that apply to an invoice based on specific conditions, such as early payment discounts, or auto cancellation.
conditional_rule_value
string
[ 1 .. 32 ] characters
^(([0-9]+)|(([0-9]+)?[.][0-9]+))$
Represents the value of the conditional rule it can be a percentage or absolute value. In case of absolute value, which might be:
An integer for currencies like
JPY
that are not typically fractional.
A decimal fraction for currencies like
TND
that are subdivided into thousandths.
For the required number of decimal places for a currency code, see
Currency Codes
.
discount_id
string
(
Stored Discount ID
)
[ 1 .. 22 ] characters
^DISC-[A-Z0-9]+$
The unique identifier for the stored discount that is created when an early payment discount rule is applied to an invoice.
discount_name
string
[ 1 .. 40 ] characters
^[a-zA-Z0-9\s]+$
Represents the name of the stored discount.
links
Array of
objects
(
Link Description
)
[ 1 .. 8 ] items
HATEOAS links.
conditional_rule_id
string
(
conditional_rule_time_based_uuid
)
= 40 characters
^CR-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]...
Show pattern
The unique identifier for the conditional rule.
conditional_rule_type
required
string
(
conditional_rule_type
)
[ 1 .. 30 ] characters
^[A-Z0-9_]*$
The type of conditional rule applied to the invoice.
Enum Value
Description
EARLY_PAYMENT_DISCOUNT
A discount applied if the invoice is paid before a specified date or within a certain period after the issue date.
LATE_PAYMENT_SURCHARGE
A surcharge applied if the invoice is paid after the due date or a specified period after the due date.
AUTO_CANCEL
A rule to automatically cancel the invoice if it is not paid by a specified date or a certain period after the due date.
conditional_rule_value_type
string
(
conditional_rule_value_type
)
[ 1 .. 20 ] characters
^[A-Z0-9_]*$
The value type that indicates how the conditional rule value is applied. Use
PERCENT
for a percentage-based discount or
AMOUNT
for an absolute currency value.
Enum Value
Description
PERCENT
Percentage of discount used in invoice item or in an invoice.
AMOUNT
An absolute value of discount used in invoice item or in an invoice based on the currency in invoice.
rule_expiry_terms
required
object
(
conditional_rules
)
The expiry terms that define when the conditional rule becomes inactive.
create_time
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
Indicates time of rule creation.
update_time
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
Indicates time of rule update.
Copy
Expand all
Collapse all
{
"conditional_rule_value"
:
"string"
,
"discount_id"
:
"string"
,
"discount_name"
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
}
]
,
"conditional_rule_id"
:
"string"
,
"conditional_rule_type"
:
"EARLY_PAYMENT_DISCOUNT"
,
"conditional_rule_value_type"
:
"PERCENT"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"THREE_DAYS_AFTER_ISSUE_DATE"
,
"condition_rule_end_date"
:
"stringstri"
}
,
"create_time"
:
"stringstringstringst"
,
"update_time"
:
"stringstringstringst"
}
Conditional Rules
The conditional rules associated with an invoice. Conditional rules define automated actions or adjustments that apply to an invoice based on specific conditions, such as early payment discounts, or auto cancellation.
rules
Array of
objects
(
rules
)
[ 1 .. 5 ] items
The list of conditional rules created by the merchant.
links
Array of
objects
(
Link Description
)
[ 1 .. 8 ] items
HATEOAS link of the created resource.
Copy
Expand all
Collapse all
{
"rules"
:
[
{
"conditional_rule_value"
:
"string"
,
"discount_id"
:
"string"
,
"discount_name"
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
}
]
,
"conditional_rule_id"
:
"string"
,
"conditional_rule_type"
:
"EARLY_PAYMENT_DISCOUNT"
,
"conditional_rule_value_type"
:
"PERCENT"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"THREE_DAYS_AFTER_ISSUE_DATE"
,
"condition_rule_end_date"
:
"stringstri"
}
,
"create_time"
:
"stringstringstringst"
,
"update_time"
:
"stringstringstringst"
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
conditional_rule_conditions
Defines the time-based condition that triggers the application of this conditional rule. This is expressed as a period relative to either the invoice issue date (for early payment discounts) or the invoice due date (for late payment surcharges and auto-cancellation).  If the value is 'SPECIFIC_DATE', the 'effective_date' field must be provided to specify the exact date.
string
(
conditional_rule_conditions
)
[ 1 .. 50 ] characters
^[A-Z0-9_]*$
Defines the time-based condition that triggers the application of this conditional rule. This is expressed as a period relative to either the invoice issue date (for early payment discounts) or the invoice due date (for late payment surcharges and auto-cancellation).  If the value is 'SPECIFIC_DATE', the 'effective_date' field must be provided to specify the exact date.
Enum Value
Description
THREE_DAYS_AFTER_ISSUE_DATE
The rule expires 3 days after the invoice issue date. Applicable for early payment discount rules.
SEVEN_DAYS_AFTER_ISSUE_DATE
The rule expires 7 days after the invoice issue date. Applicable for early payment discount rules.
FIFTEEN_DAYS_AFTER_ISSUE_DATE
The rule expires 15 days after the invoice issue date. Applicable for early payment discount rules.
THIRTY_DAYS_AFTER_ISSUE_DATE
The rule expires 30 days after the invoice issue date. Applicable for early payment discount rules.
ONE_DAY_AFTER_DUE_DATE
The rule takes effect 1 day after the invoice due date. Applicable for late payment surcharge and auto-cancellation rules.
SEVEN_DAYS_AFTER_DUE_DATE
The rule takes effect 7 days after the invoice due date. Applicable for late payment surcharge and auto-cancellation rules.
FIFTEEN_DAYS_AFTER_DUE_DATE
The rule takes effect 15 days after the invoice due date. Applicable for late payment surcharge and auto-cancellation rules.
THIRTY_DAYS_AFTER_DUE_DATE
The rule takes effect 30 days after the invoice due date. Applicable for late payment surcharge and auto-cancellation rules.
SPECIFIC_DATE
The rule expires or takes effect on a specific date provided in the
condition_rule_end_date
field. Applicable for all conditional rule types.
Copy
"THREE_DAYS_AFTER_ISSUE_DATE"
conditional_rule_time_based_uuid
A unique identifier for the conditional rule, This ID is generated as a time-based UUID (version 1) to ensure uniqueness and traceability of the rule creation time.
string
(
conditional_rule_time_based_uuid
)
= 40 characters
^CR-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]...
Show pattern
A unique identifier for the conditional rule, This ID is generated as a time-based UUID (version 1) to ensure uniqueness and traceability of the rule creation time.
Copy
"stringstringstringstringstringstringstri"
conditional_rule_type
This enum defines what type of rule is applying for the particular invoice.
string
(
conditional_rule_type
)
[ 1 .. 30 ] characters
^[A-Z0-9_]*$
This enum defines what type of rule is applying for the particular invoice.
Enum Value
Description
EARLY_PAYMENT_DISCOUNT
A discount applied if the invoice is paid before a specified date or within a certain period after the issue date.
LATE_PAYMENT_SURCHARGE
A surcharge applied if the invoice is paid after the due date or a specified period after the due date.
AUTO_CANCEL
A rule to automatically cancel the invoice if it is not paid by a specified date or a certain period after the due date.
Copy
"EARLY_PAYMENT_DISCOUNT"
conditional_rule_value_type
Type of the stored discount. Used to determine whether its percentage or absolute currency value.
string
(
conditional_rule_value_type
)
[ 1 .. 20 ] characters
^[A-Z0-9_]*$
Type of the stored discount. Used to determine whether its percentage or absolute currency value.
Enum Value
Description
PERCENT
Percentage of discount used in invoice item or in an invoice.
AMOUNT
An absolute value of discount used in invoice item or in an invoice based on the currency in invoice.
Copy
"PERCENT"
conditional_rules
The expiry terms that define when a conditional rule on an invoice expires, including the expiry condition and the end date.
rule_expiry_condition
required
string
(
conditional_rule_conditions
)
[ 1 .. 50 ] characters
^[A-Z0-9_]*$
Defines the time-based condition that triggers the application of this conditional rule. This is expressed as a period relative to either the invoice issue date (for early payment discounts) or the invoice due date (for late payment surcharges and auto-cancellation).  If the value is 'SPECIFIC_DATE', the 'effective_date' field must be provided to specify the exact date.
Enum Value
Description
THREE_DAYS_AFTER_ISSUE_DATE
The rule expires 3 days after the invoice issue date. Applicable for early payment discount rules.
SEVEN_DAYS_AFTER_ISSUE_DATE
The rule expires 7 days after the invoice issue date. Applicable for early payment discount rules.
FIFTEEN_DAYS_AFTER_ISSUE_DATE
The rule expires 15 days after the invoice issue date. Applicable for early payment discount rules.
THIRTY_DAYS_AFTER_ISSUE_DATE
The rule expires 30 days after the invoice issue date. Applicable for early payment discount rules.
ONE_DAY_AFTER_DUE_DATE
The rule takes effect 1 day after the invoice due date. Applicable for late payment surcharge and auto-cancellation rules.
SEVEN_DAYS_AFTER_DUE_DATE
The rule takes effect 7 days after the invoice due date. Applicable for late payment surcharge and auto-cancellation rules.
FIFTEEN_DAYS_AFTER_DUE_DATE
The rule takes effect 15 days after the invoice due date. Applicable for late payment surcharge and auto-cancellation rules.
THIRTY_DAYS_AFTER_DUE_DATE
The rule takes effect 30 days after the invoice due date. Applicable for late payment surcharge and auto-cancellation rules.
SPECIFIC_DATE
The rule expires or takes effect on a specific date provided in the
condition_rule_end_date
field. Applicable for all conditional rule types.
condition_rule_end_date
required
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
The calculated end date for the conditional rule based on the rule_expiry_condition. This date indicates when the rule will expire or take effect. Specified in
Internet date and time format
. Only UTC is supported in response. For example,
2025-03-12T00:00:00Z
.
Copy
{
"rule_expiry_condition"
:
"THREE_DAYS_AFTER_ISSUE_DATE"
,
"condition_rule_end_date"
:
"stringstri"
}
configuration
The invoice configuration details. Includes partial payment, tip, and tax calculated after discount.
tax_calculated_after_discount
boolean
Default:
true
Indicates whether the tax is calculated before or after a discount. If
false
, the tax is calculated before a discount. If
true
, the tax is calculated after a discount.
tax_inclusive
boolean
Default:
false
Indicates whether the unit price includes tax.
allow_tip
boolean
Default:
false
Indicates whether the invoice enables the customer to enter a tip amount during payment. If
true
, the invoice shows a tip amount field so that the customer can enter a tip amount. If
false
, the invoice does not show a tip amount field.
Note:
This feature is not available for users in
Hong Kong
,
Taiwan
,
India
, or
Japan
.
partial_payment
object
(
partial_payment
)
The partial payment details. Includes the minimum amount that the invoicer wants the payer to pay.
has_conditional_rule
boolean
Default:
false
Indicates whether conditional pricing rules are applied to the invoice. If
true
, pricing rules (such as discounts or surcharges based on specific conditions) are applied. If
false
, no conditional pricing rules are applied.
save_item_for_future
boolean
Default:
true
Indicates whether the item should be saved for future invoices.
show_additional_item_fields
boolean
Default:
false
Indicates whether items tray should be shown for invoices or not. If
true
, additional fields containing items tray will be shown. If
false
, the items tray will be hidden.
discount_mode_preference
string
(
discount_mode_preference
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Represents the user's preferred mode for creating discounts. Determines whether "One-time discount" or "Save for future invoices" is preselected when creating a new discount.
Enum Value
Description
ONE_TIME
Indicates that the user prefers creating one-time discounts by default.
SAVE_FOR_FUTURE
Indicates that the user prefers saving discounts for future invoices by default.
theme
object
(
Theme configuration
)
The theme configuration for the template. Defines the visual appearance of the invoice buyer experience and email when invoice is created using the template in UI.
Note:
Setting a theme on a template does not automatically carry over to invoices created using this template. To apply a theme to an invoice, set it directly on the invoice configuration.
template_id
string
<= 30 characters
Default:
"PayPal system template"
The template ID. The template determines the layout of the invoice. Includes which fields to show and hide.
Note:
This is an optional field. If you wish to customize the invoice layout using a specific template, provide a valid template ID here. You can either use an existing template ID or create a new template via the create template API and then use the newly created template's ID.
payment_method_overrides
Array of
objects
(
override_payment_method_detail
)
[ 1 .. 15 ] items
The payment method override configurations for the invoice. Defines which payment methods are enabled and any rules that control payment behavior. When provided during invoice creation or update, this array replaces any existing payment method override configuration for the invoice.
Note:
Payment method availability depends on the merchant's country, the buyer's country, and the invoice amount. Override configurations only take effect if the specified payment method is available for the invoice.
Copy
Expand all
Collapse all
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"has_conditional_rule"
:
false
,
"save_item_for_future"
:
true
,
"show_additional_item_fields"
:
false
,
"discount_mode_preference"
:
"ONE_TIME"
,
"theme"
:
{
"primary_color"
:
"string"
}
,
"template_id"
:
"PayPal system template"
,
"payment_method_overrides"
:
[
{
"payment_method_type"
:
"PAY_BY_BANK"
,
"enabled"
:
true
,
"rules"
:
[
{
"rule_type"
:
"EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD"
,
"rule_value"
:
"string"
}
]
}
]
}
configuration
The invoice configuration details. Includes partial payment, tip, and tax calculated after discount.
tax_calculated_after_discount
boolean
Default:
true
Indicates whether the tax is calculated before or after a discount. If
false
, the tax is calculated before a discount. If
true
, the tax is calculated after a discount.
tax_inclusive
boolean
Default:
false
Indicates whether the unit price includes tax.
allow_tip
boolean
Default:
false
Indicates whether the invoice enables the customer to enter a tip amount during payment. If
true
, the invoice shows a tip amount field so that the customer can enter a tip amount. If
false
, the invoice does not show a tip amount field.
Note:
This feature is not available for users in
Hong Kong
,
Taiwan
,
India
, or
Japan
.
partial_payment
object
(
partial_payment
)
The partial payment details. Includes the minimum amount that the invoicer wants the payer to pay.
template_id
string
= 22 characters
^(TEMP-)[A-Z0-9]+$
Default:
"PayPal system template"
The template ID. The template determines the layout of the invoice.
You can either use an existing template ID or create a new template via the create template API and then use the newly created template's ID.
Copy
Expand all
Collapse all
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"template_id"
:
"PayPal system template"
}
Connections
This object contains an array of connection details. It is used to load sync status for a user.
connections
Array of
objects
(
Connections
)
[ 1 .. 1000 ] items
An array of connection-level details.
Copy
Expand all
Collapse all
{
"connections"
:
[
{
"platform_name"
:
"string"
,
"last_sync_status"
:
"IN_PROGRESS"
,
"last_sync_time"
:
"string"
}
]
}
Connections
This lists last sync status and connection platform name.
platform_name
string
[ 1 .. 64 ] characters
^.*$
The name of the platform. This property supports Unicode. The pattern is not provided because the value is defined by an external party.
last_sync_status
string
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The status of the last sync. This property supports Unicode.
Enum Value
Description
IN_PROGRESS
The last sync process has started.
SUCCESS
The last sync process is success.
FAILED
The last sync process failed.
last_sync_time
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
"platform_name"
:
"string"
,
"last_sync_status"
:
"IN_PROGRESS"
,
"last_sync_time"
:
"string"
}
contact_information
The contact information of the user. Includes name and address.
business_name
string
<= 300 characters
Required. The business name of the party.
name
object
(
Name
)
The name of the party.
address
object
(
Portable Postal Address (Medium-Grained)
)
The portable international postal address. Maps to
AddressValidationMetadata
and HTML 5.1
Autofilling form controls: the autocomplete attribute
.
Copy
Expand all
Collapse all
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
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
country_code
The
2-character ISO 3166-1 code
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
2-character ISO 3166-1 code
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
custom_amount
The custom amount to apply to an invoice. If you include a label, you must include a custom amount.
label
required
string
[ 0 .. 50 ] characters
^[\S\s]*$
The label to the custom amount of the invoice.
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
"label"
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
}
Date and Time Range
The date and time range. Filters invoices by creation date, invoice date, due date, and payment date.
start
required
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
end
required
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
"start"
:
"string"
,
"end"
:
"string"
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
date_range
The date range. Filters invoices by creation date, invoice date, due date, and payment date.
start
required
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
end
required
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
{
"start"
:
"string"
,
"end"
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
detail
The details of the invoice like notes, terms and conditions, memo, attachments.
reference
string
[ 1 .. 120 ] characters
^[\S\s]*$
The reference data. Includes a Purchase Order (PO) number.
note
string
[ 1 .. 4000 ] characters
^[\S\s]*$
A note to the invoice recipient. Also appears on the invoice notification email.
terms_and_conditions
string
[ 1 .. 4000 ] characters
^[\S\s]*$
The general terms of the invoice. Can include return or cancellation policy and other terms and conditions.
memo
string
[ 1 .. 500 ] characters
^[\S\s]*$
A private bookkeeping memo for the user.
attachments
Array of
objects
(
File Reference
)
[ 0 .. 2147483647 ] items
An array of PayPal IDs for the files that are attached to an invoice.
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
Copy
Expand all
Collapse all
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
}
discount
The discount as a percent or amount at invoice level. The invoice discount amount is subtracted from the item total.
percent
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
"percent"
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
}
discount_mode_preference
Represents the user's preferred mode for creating discounts. Determines whether "One-time discount" or "Save for future invoices" is preselected when creating a new discount.
string
(
discount_mode_preference
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Represents the user's preferred mode for creating discounts. Determines whether "One-time discount" or "Save for future invoices" is preselected when creating a new discount.
Enum Value
Description
ONE_TIME
Indicates that the user prefers creating one-time discounts by default.
SAVE_FOR_FUTURE
Indicates that the user prefers saving discounts for future invoices by default.
Copy
"ONE_TIME"
display_preference
The display preference of the field.
hidden
boolean
Indicates whether to show or hide the field.
Copy
{
"hidden"
:
true
}
early_payment_discount
The early payment discount for the invoice. If the payer pays before the discount end date, the specified discount is applied.
is_applied
boolean
Indicates whether the particular rule is applied or not.
discount_end_date
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
percent
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
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
<
merchant_common_email_address_v2
>
(
email
)
[ 3 .. 254 ] characters
(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-...
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
<
ppaas_common_email_address_v2
>
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
email_status
List of delivery statuses to be sent as a part of email callback API.
string
(
email_status
)
[ 1 .. 40 ] characters
^[A-Z0-9_]+$
List of delivery statuses to be sent as a part of email callback API.
Enum Value
Description
SENT
Status Sent from Notifications layer.
DELIVERED
Status delivered to the aggregator/vendor/client.
OPENED
Status for the notification opened by the end user.
FAIL_HARD
Status hard failure - Notification cannot be delivered to the end user.
FAIL_SOFT
Status soft failure - This is a temporary failure and can be retried.
CLICKED
Status for push notification clicks.
Copy
"SENT"
entity_id
It is either a merchant ID or an invoice ID based on the type provided in the request.
string
(
entity_id
)
[ 1 .. 30 ] characters
^.*$
It is either a merchant ID or an invoice ID based on the type provided in the request.
Copy
"string"
entity_type
It is an entity type, used to fetch payment method details.
string
(
entity_type
)
[ 1 .. 20 ] characters
^[A-Z0-9_]+$
It is an entity type, used to fetch payment method details.
Enum Value
Description
MERCHANT
Fetch payment method details for a given merchant.
INVOICE
Fetch payment method details for a given invoice.
TEMPLATE
Fetch payment method details for a given template.
Copy
"MERCHANT"
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
"description"
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
}
]
,
"description"
:
"string"
}
Estimate
Estimate information, this contains the information about the estimate like item, amount, billing and shipping information.
id
string
[ 1 .. 30 ] characters
^[A-Z0-9_-]+$
The ID of the estimate.
status
string
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Represents estimate status.
Enum Value
Description
DRAFT
Draft estimate.
SENT
Estimate sent.
CANCELLED
Estimate cancelled.
SHARED
Estimate shared.
ACCEPTED
Estimate accepted.
DELETED
Estimate deleted.
INVOICED
Estimate invoiced.
EXPIRED
Estimate expired.
detail
required
object
(
estimate_detail
)
The details of the estimate. Includes estimate number, date and audit metadata.
invoicer
object
(
invoicer_info
)
The invoicer business information that appears on the invoice.
primary_recipients
Array of
objects
(
recipient_info
)
[ 1 .. 100 ] items
The billing and shipping information. Includes name, email, address, phone and language.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 1 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
items
Array of
objects
(
item
)
[ 1 .. 100 ] items
An array of estimate line item information.
configuration
object
(
configuration
)
The invoice configuration details. Includes partial payment, tip, and tax calculated after discount.
amount
object
(
amount_summary_detail
)
The invoice amount summary of item total, discount, tax total, and shipping.
links
Array of
objects
(
Link Description
)
[ 1 .. 7 ] items
An array of request-related
HATEOAS links
.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"status"
:
"DRAFT"
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"estimate_number"
:
"string"
,
"viewed_by_recipient"
:
true
,
"estimate_date"
:
"string"
,
"estimate_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
,
"expiration_date"
:
"string"
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"cancelled_by"
:
"string"
,
"last_sent_by"
:
"string"
,
"recipient_view_url"
:
"
http://example.com
"
,
"invoicer_view_url"
:
"
http://example.com
"
,
"cancel_time"
:
"string"
,
"first_sent_time"
:
"string"
,
"last_sent_time"
:
"string"
,
"created_by_flow"
:
"MULTIPLE_RECIPIENTS_GROUP"
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
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
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"has_conditional_rule"
:
false
,
"save_item_for_future"
:
true
,
"show_additional_item_fields"
:
false
,
"discount_mode_preference"
:
"ONE_TIME"
,
"theme"
:
{
"primary_color"
:
"string"
}
,
"template_id"
:
"PayPal system template"
,
"payment_method_overrides"
:
[
{
"payment_method_type"
:
"PAY_BY_BANK"
,
"enabled"
:
true
,
"rules"
:
[
{
"rule_type"
:
"EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD"
,
"rule_value"
:
"string"
}
]
}
]
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
,
"custom"
:
{
"label"
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
}
}
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
}
]
}
estimate_detail
The details of the estimate. Includes estimate number, date and audit metadata.
reference
string
[ 1 .. 120 ] characters
^[\S\s]*$
The reference data. Includes a Purchase Order (PO) number.
note
string
[ 1 .. 4000 ] characters
^[\S\s]*$
A note to the invoice recipient. Also appears on the invoice notification email.
terms_and_conditions
string
[ 1 .. 4000 ] characters
^[\S\s]*$
The general terms of the invoice. Can include return or cancellation policy and other terms and conditions.
memo
string
[ 1 .. 500 ] characters
^[\S\s]*$
A private bookkeeping memo for the user.
attachments
Array of
objects
(
File Reference
)
[ 0 .. 2147483647 ] items
An array of PayPal IDs for the files that are attached to an invoice.
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
estimate_number
string
[ 1 .. 127 ] characters
^.+$
The invoice number. Default is the number that is auto-incremented number from the last number.
viewed_by_recipient
boolean
Represents if the estimate is viewed.
estimate_date
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
estimate_term
object
(
estimate_payment_term
)
The payment term of the invoice. Payment can be due upon receipt, a specified date, or in a set number of days.
metadata
object
(
metadata
)
The audit metadata. Captures all invoicing actions on create, send, update, and cancel.
Copy
Expand all
Collapse all
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"estimate_number"
:
"string"
,
"viewed_by_recipient"
:
true
,
"estimate_date"
:
"string"
,
"estimate_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
,
"expiration_date"
:
"string"
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"cancelled_by"
:
"string"
,
"last_sent_by"
:
"string"
,
"recipient_view_url"
:
"
http://example.com
"
,
"invoicer_view_url"
:
"
http://example.com
"
,
"cancel_time"
:
"string"
,
"first_sent_time"
:
"string"
,
"last_sent_time"
:
"string"
,
"created_by_flow"
:
"MULTIPLE_RECIPIENTS_GROUP"
}
}
estimate_free_text_search_fields
Supported estimate free text search fields.
string
(
estimate_free_text_search_fields
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Supported estimate free text search fields.
Enum Value
Description
ESTIMATE_NUMBER
Estimate number.
NOTES
Notes associated with the invoice.
MERCHANT_MEMO
Merchant memo related to the invoice.
PAYER_REFERENCE_INFO
Payer's reference information.
BILLING_EMAIL
Email address associated with billing.
BILLING_NAME
Name associated with billing.
BILLING_BUSINESS_NAME
Business name associated with billing.
BILLING_PHONE_NUMBER
Phone number associated with billing.
SHIPPING_EMAIL
Email address associated with shipping.
SHIPPING_NAME
Name associated with shipping.
SHIPPING_BUSINESS_NAME
Business name associated with shipping.
SHIPPING_PHONE_NUMBER
Phone number associated with shipping.
ITEM_NAME
Name of the invoice item.
ITEM_TAX_NAME
Tax name associated with the invoice item.
ITEM_DISCOUNT_NAME
Discount name associated with the invoice item.
ESTIMATE_DISCOUNT_NAME
Discount name associated with the estimate.
ALL
Search in all available search fields.
Copy
"ESTIMATE_NUMBER"
estimate_payment_term
The payment term of the invoice. Payment can be due upon receipt, a specified date, or in a set number of days.
term_type
string
(
payment_term_type
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment term. Payment can be due upon receipt, a specified date, or in a set number of days.
Enum Value
Description
DUE_ON_RECEIPT
The payment for the invoice is due upon receipt of the invoice.
DUE_ON_DATE_SPECIFIED
The payment for the invoice is due on the date specified in the invoice.
NET_10
The payment for the invoice is due in 10 days.
NET_15
The payment for the invoice is due in 15 days.
NET_30
The payment for the invoice is due in 30 days.
NET_45
The payment for the invoice is due in 45 days.
NET_60
The payment for the invoice is due in 60 days.
NET_90
The payment for the invoice is due in 90 days.
NO_DUE_DATE
The invoice has no payment due date.
conditional_rules
object
(
payment_term_conditional_rules
)
The conditional rules associated with the payment term of the invoice. Includes early payment discount, late payment surcharge, and auto cancellation details.
expiration_date
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
Expand all
Collapse all
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
,
"expiration_date"
:
"string"
}
estimate_status
Supported estimate status.
string
(
estimate_status
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Supported estimate status.
Enum Value
Description
DRAFT
Draft estimate.
SENT
Estimate sent.
CANCELLED
Estimate cancelled.
SHARED
Estimate shared.
ACCEPTED
Estimate accepted.
INVOICED
Estimate invoiced.
EXPIRED
Estimate expired.
Copy
"DRAFT"
estimate_suggestion_fields
Supported estimate suggestion fields.
string
(
estimate_suggestion_fields
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Supported estimate suggestion fields.
Enum Value
Description
ESTIMATE_NUMBER
Number associated with it.
NOTES
Notes associated with the estimate.
MERCHANT_MEMO
Merchant memo related to the estimate.
PAYER_REFERENCE_INFO
Payer's reference information.
BILLING_EMAIL
Email address associated with billing.
BILLING_NAME
Name associated with billing.
BILLING_BUSINESS_NAME
Business name associated with billing.
BILLING_PHONE_NUMBER
Phone number associated with billing.
SHIPPING_EMAIL
Email address associated with shipping.
SHIPPING_NAME
Name associated with shipping.
SHIPPING_BUSINESS_NAME
Business name associated with shipping.
SHIPPING_PHONE_NUMBER
Phone number associated with shipping.
ITEM_NAME
Name of the estimate item.
ALL
This is used to search in all available search fields.
Copy
"ESTIMATE_NUMBER"
estimates
Suggestion object contains the specified text and the field associated with it.
suggested_text
string
[ 3 .. 800 ] characters
^(?!\s*$).+
Represents the text which has been provided in request.
fields
Array of
strings
(
estimate_suggestion_fields
)
[ 1 .. 14 ] items
unique
An array of matched estimate fields.
Items
Enum Value
Description
ESTIMATE_NUMBER
Number associated with it.
NOTES
Notes associated with the estimate.
MERCHANT_MEMO
Merchant memo related to the estimate.
PAYER_REFERENCE_INFO
Payer's reference information.
BILLING_EMAIL
Email address associated with billing.
BILLING_NAME
Name associated with billing.
BILLING_BUSINESS_NAME
Business name associated with billing.
BILLING_PHONE_NUMBER
Phone number associated with billing.
SHIPPING_EMAIL
Email address associated with shipping.
SHIPPING_NAME
Name associated with shipping.
SHIPPING_BUSINESS_NAME
Business name associated with shipping.
SHIPPING_PHONE_NUMBER
Phone number associated with shipping.
ITEM_NAME
Name of the estimate item.
ALL
This is used to search in all available search fields.
Copy
Expand all
Collapse all
{
"suggested_text"
:
"string"
,
"fields"
:
[
"ESTIMATE_NUMBER"
]
}
Feature Object
Represents a feature associated with the invoicing product.
code
string
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The feature code.
subscription_id
string
= 39 characters
^SI-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]...
Show pattern
Unique identifier for the subscription associated with this feature.
status
string
(
The status of the feature.
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Indicates the status of the feature. If this feature is a paywall feature, it reflects the status of the associated subscription.
Enum Value
Description
ACTIVE
Represents the feature is active.
CANCELLED
Represents the feature is cancelled.
PENDING_CANCELLATION
Represents the feature is in pending cancelled state.
PENDING_ACTIVATION
Represents the feature is in pending activation state.
SUSPENDED
Represents the feature is suspended.
REVOKED
Represents the feature has been revoked.
APPROVED
Represents the feature has been approved.
IN_REVIEW
Represents the feature is currently under review.
NEED_DATA
Represents the feature requires additional data.
DENY
Represents the feature has been denied.
INACTIVE
Represents the feature is inactive.
PENDING
Represents the feature is in a pending state.
type
string
(
The type of the feature.
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Indicates the type of the feature.
Enum Value
Description
PAID
Represents the feature is a paid feature.
FREE
Represents the feature is a free feature.
Copy
{
"code"
:
"string"
,
"subscription_id"
:
"stringstringstringstringstringstringstr"
,
"status"
:
"ACTIVE"
,
"type"
:
"PAID"
}
Feedback Classifiers
Allows a client to tag requests for future retrieval.
tags
Array of
strings
[ 1 .. 10 ] items
A set of simple tags.
pairs
required
object
(
A set of regular JSON style properties and values.
)
A set of regular JSON style properties and values.
Copy
Expand all
Collapse all
{
"tags"
:
[
"string"
]
,
"pairs"
:
{
"property1"
:
"string"
,
"property2"
:
"string"
}
}
feedback_data
The details about the feedback.
feedback_id
string
[ 30 .. 45 ] characters
^[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}...
Show pattern
The feedback identifier.
reaction
required
string
(
reaction
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
This indicates the Customer's reaction, which can be a like or dislike.
Enum Value
Description
LIKE
Customer likes the seller/goods/service.
DISLIKE
Customer dislikes the seller/goods/service.
text
string
[ 1 .. 250 ] characters
^[\S\s]*$
Detailed feedback from the customer. The pattern is not provided because this property supports Unicode.
Copy
{
"feedback_id"
:
"stringstringstringstringstring"
,
"reaction"
:
"LIKE"
,
"text"
:
"string"
}
feedback_visibility_updates
Updates the visibility of customer feedback comments, allowing merchants to hide or show specific comments.
feedback_id
required
string
[ 30 .. 45 ] characters
^[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{8}...
Show pattern
The feedback identifier.
is_hidden
required
boolean
Default:
false
Indicates whether the feedback is hidden to the merchant. If
true
, the feedback is hidden. If
false
, the feedback is visible.
Copy
{
"feedback_id"
:
"stringstringstringstringstring"
,
"is_hidden"
:
false
}
Feedbacks Stat
Aggregated feedback associated with an merchant basded on the type.
metric
string
(
metric
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
This indicates the metrics of the each dimensions we are aggregating.
Enum Value
Description
LIKES_COUNT
Total number of likes for the given time period.
DISLIKES_COUNT
Total number of dislikes for the given time period.
TOTAL_FEEDBACK_COUNT
Total number of feedbacks for the given time period.
INVOICES_RATED_PERCENT
Percentage of invoice rated out of sent for the given time period.
value
string
[ 1 .. 10 ] characters
(\d+%?|\d+\.\d+%?)
Value of the metric it could be a number or a number with percentage as well.
change
string
[ 1 .. 10 ] characters
([+-]\d+(\.\d+)?%)
Value of the metric it could be a positive or a negative number with percentage as well.
Copy
{
"metric"
:
"LIKES_COUNT"
,
"value"
:
"string"
,
"change"
:
"string"
}
fetchtype
Is the fetch type invoice number or id.
fetch_id
boolean
Default:
"false"
Optional to decide the number or ID.
Copy
{
"fetch_id"
:
"false"
}
File Reference
The file reference. Can be a file in PayPal MediaServ, PayPal DMS, or other custom store.
id
string
[ 1 .. 255 ] characters
The ID of the referenced file.
reference_url
string
<
uri
>
[ 1 .. 2000 ] characters
The reference URL for the file.
content_type
string
The
Internet Assigned Numbers Authority (IANA) media type of the file
.
size
string
^[0-9]+$
The size of the file, in bytes.
create_time
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
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
Get Record Count
This object contains a total record count and array of start date, end date and record count of records created between those dates.
record_count
integer
[ 0 .. 2147483647 ]
Total number of records for the merchant based on the filter.
start_time
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
end_time
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
"record_count"
:
1250
,
"start_time"
:
"string"
,
"end_time"
:
"string"
}
id
A unique id used to reference the stored discount.
string
(
id
)
[ 1 .. 22 ] characters
^DISC-[A-Z0-9]+$
A unique id used to reference the stored discount.
Copy
"string"
id
A unique id used to reference the batch task.
string
(
id
)
= 40 characters
^(BAT-)1[0-9A-Z]{3}-[0-9A-Z]{4}-[0-9A-Z]{8}-[...
Show pattern
A unique id used to reference the batch task.
Copy
"stringstringstringstringstringstringstri"
invoice
The invoice details which includes all information of the invoice like items, billing information.
id
string
[ 0 .. 30 ] characters
^[\s\S]*$
The ID of the invoice.
parent_id
string
[ 0 .. 30 ] characters
^[\s\S]*$
The parent ID to an invoice that defines the group invoice to which the invoice is related.
primary_recipients
Array of
objects
(
recipient_info
)
[ 0 .. 100 ] items
The billing and shipping information. Includes name, email, address, phone and language.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 0 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
items
Array of
objects
(
item
)
[ 0 .. 100 ] items
An array of invoice line item information.
links
Array of
objects
(
Link Description
)
[ 0 .. 2147483647 ] items
An array of request-related
HATEOAS links
.
status
string
(
invoice_status
)
[ 0 .. 255 ] characters
^[\s\S]*$
The status of the invoice.
Enum Value
Description
DRAFT
The invoice is in draft state. It is not yet sent to the payer.
SENT
The invoice has been sent to the payer. The payment is awaited from the payer.
SCHEDULED
The invoice is scheduled on a future date. It is not yet sent to the payer.
PAID
The payer has paid for the invoice.
MARKED_AS_PAID
The invoice is marked as paid by the invoicer.
CANCELLED
The invoice has been cancelled by the invoicer.
REFUNDED
The invoice has been refunded by the invoicer.
PARTIALLY_PAID
The payer has partially paid for the invoice.
PARTIALLY_REFUNDED
The invoice has been partially refunded by the invoicer.
MARKED_AS_REFUNDED
The invoice is marked as refunded by the invoicer.
UNPAID
The invoicer is yet to receive the payment from the payer for the invoice.
PAYMENT_PENDING
The invoicer is yet to receive the payment for the invoice. It is under pending review.
AUTO_CANCELLED
The invoice was automatically cancelled because the payment was not received within the specified timeframe.
PAID_EXTERNAL
The invoice has been paid through an external system or method outside of the standard PayPal payment flow. This status is set manually, indicating payment was received through other means.
REFUNDED_EXTERNAL
The invoice has been refunded through an external system or method. This status indicates a refund was issued outside of the standard PayPal payment flow.
SHARED
The invoice has been shared with the payer, typically via a link or other method. This status is used to track when an invoice has been distributed but not necessarily sent via PayPal.
detail
required
object
(
invoice_detail
)
The details of the invoice. Includes invoice number, date, payment terms, and audit metadata.
invoicer
object
(
invoicer_info
)
The invoicer business information that appears on the invoice.
configuration
object
(
configuration
)
The invoice configuration details. Includes partial payment, tip, and tax calculated after discount.
amount
object
(
amount_summary_detail
)
The invoice amount summary of item total, discount, tax total, and shipping.
settings
object
(
invoice_settings
)
The settings for the invoice.
due_amount
object
(
Money
)
The due amount, which is the balance amount outstanding after payments.
gratuity
object
(
Money
)
The amount paid by the payer as gratuity to the invoicer.
payments
object
(
payments
)
An array of payments registered against the invoice.
effective_invoice_total
object
(
Money
)
The effective total amount of the invoice after applying conditional rules. The conditional rules include early payment discount, late payment surcharge, and auto cancellation details.
effective_due_amount
object
(
Money
)
The effective due amount of the invoice after applying conditional rules. The conditional rules include early payment discount, late payment surcharge, and auto cancellation details.
refunds
object
(
refunds
)
The invoicing refund details. Includes the refund type, date, amount, and method.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"parent_id"
:
"string"
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
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
}
,
"unit_of_measure"
:
"QUANTITY"
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
"status"
:
"DRAFT"
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"tip_presets"
:
[
{
"percent"
:
"19.99"
}
]
,
"order_details"
:
"string"
,
"project_details"
:
"string"
,
"service_details"
:
"string"
,
"payment_terms"
:
"string"
,
"return_policy"
:
"string"
,
"cancellation_policy"
:
"string"
,
"service_agreement"
:
"string"
,
"invoice_number"
:
"string"
,
"invoice_date"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
,
"due_date"
:
"string"
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"cancelled_by"
:
"string"
,
"last_sent_by"
:
"string"
,
"recipient_view_url"
:
"
http://example.com
"
,
"invoicer_view_url"
:
"
http://example.com
"
,
"cancel_time"
:
"string"
,
"first_sent_time"
:
"string"
,
"last_sent_time"
:
"string"
,
"created_by_flow"
:
"MULTIPLE_RECIPIENTS_GROUP"
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"has_conditional_rule"
:
false
,
"save_item_for_future"
:
true
,
"show_additional_item_fields"
:
false
,
"discount_mode_preference"
:
"ONE_TIME"
,
"theme"
:
{
"primary_color"
:
"string"
}
,
"template_id"
:
"PayPal system template"
,
"payment_method_overrides"
:
[
{
"payment_method_type"
:
"PAY_BY_BANK"
,
"enabled"
:
true
,
"rules"
:
[
{
"rule_type"
:
"EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD"
,
"rule_value"
:
"string"
}
]
}
]
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
,
"custom"
:
{
"label"
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
}
}
}
,
"settings"
:
{
"invoice_item_settings"
:
[
{
"field_name"
:
"ITEM_DESCRIPTION"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_additional_settings"
:
[
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_policy_and_agreement_settings"
:
[
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
}
,
"due_amount"
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
"gratuity"
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
"payments"
:
{
"transactions"
:
[
{
"payment_id"
:
"string"
,
"note"
:
"string"
,
"type"
:
"PAYPAL"
,
"payment_date"
:
"string"
,
"payment_date_time"
:
"string"
,
"method"
:
"BANK_TRANSFER"
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
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"paid_amount"
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
"effective_invoice_total"
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
"effective_due_amount"
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
"refunds"
:
{
"transactions"
:
[
{
"refund_id"
:
"string"
,
"type"
:
"PAYPAL"
,
"refund_date"
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
"method"
:
"BANK_TRANSFER"
}
]
,
"refund_amount"
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
Invoice
The invoice details which includes all information of the invoice like items, billing information.
id
string
[ 1 .. 30 ] characters
^[\s\S]*$
The ID of the invoice.
parent_id
string
[ 1 .. 30 ] characters
^[\s\S]*$
The parent ID to an invoice that defines the group invoice to which the invoice is related.
primary_recipients
Array of
objects
(
recipient_info
)
[ 1 .. 100 ] items
The billing and shipping information. Includes name, email, address, phone and language.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 1 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
items
Array of
objects
(
item
)
[ 1 .. 100 ] items
An array of invoice line item information.
links
Array of
objects
(
Link Description
)
[ 1 .. 2147483647 ] items
An array of request-related
HATEOAS links
.
status
string
(
invoice_status
)
[ 0 .. 255 ] characters
^[\s\S]*$
The status of the invoice.
Enum Value
Description
DRAFT
The invoice is in draft state. It is not yet sent to the payer.
SENT
The invoice has been sent to the payer. The payment is awaited from the payer.
SCHEDULED
The invoice is scheduled on a future date. It is not yet sent to the payer.
PAID
The payer has paid for the invoice.
MARKED_AS_PAID
The invoice is marked as paid by the invoicer.
CANCELLED
The invoice has been cancelled by the invoicer.
REFUNDED
The invoice has been refunded by the invoicer.
PARTIALLY_PAID
The payer has partially paid for the invoice.
PARTIALLY_REFUNDED
The invoice has been partially refunded by the invoicer.
MARKED_AS_REFUNDED
The invoice is marked as refunded by the invoicer.
UNPAID
The invoicer is yet to receive the payment from the payer for the invoice.
PAYMENT_PENDING
The invoicer is yet to receive the payment for the invoice. It is under pending review.
AUTO_CANCELLED
The invoice was automatically cancelled because the payment was not received within the specified timeframe.
PAID_EXTERNAL
The invoice has been paid through an external system or method outside of the standard PayPal payment flow. This status is set manually, indicating payment was received through other means.
REFUNDED_EXTERNAL
The invoice has been refunded through an external system or method. This status indicates a refund was issued outside of the standard PayPal payment flow.
SHARED
The invoice has been shared with the payer, typically via a link or other method. This status is used to track when an invoice has been distributed but not necessarily sent via PayPal.
detail
required
object
(
invoice_detail
)
The details of the invoice. Includes the invoice number, date, payment terms, and audit metadata.
invoicer
object
(
invoicer_info
)
The invoicer information. Includes the business name, email, address, phone, fax, tax ID, additional notes, and logo URL.
configuration
object
(
configuration
)
The invoice configuration details. Includes partial payment, tip, and tax calculated after discount.
amount
object
(
amount_summary_detail
)
The invoice amount summary of item total, discount, tax total and shipping..
due_amount
object
(
Money
)
The due amount, which is the balance amount outstanding after payments.
gratuity
object
(
Money
)
The amount paid by the payer as gratuity to the invoicer.
payments
object
(
payments
)
List of payments registered against the invoice..
refunds
object
(
refunds
)
List of refunds against this invoice. The invoicing refund details includes refund type, date, amount, and method.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"parent_id"
:
"string"
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
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
}
,
"unit_of_measure"
:
"QUANTITY"
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
"status"
:
"DRAFT"
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"tip_presets"
:
[
{
"percent"
:
"19.99"
}
]
,
"order_details"
:
"string"
,
"project_details"
:
"string"
,
"service_details"
:
"string"
,
"payment_terms"
:
"string"
,
"return_policy"
:
"string"
,
"cancellation_policy"
:
"string"
,
"service_agreement"
:
"string"
,
"invoice_number"
:
"string"
,
"invoice_date"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
,
"due_date"
:
"string"
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"cancelled_by"
:
"string"
,
"last_sent_by"
:
"string"
,
"recipient_view_url"
:
"
http://example.com
"
,
"invoicer_view_url"
:
"
http://example.com
"
,
"cancel_time"
:
"string"
,
"first_sent_time"
:
"string"
,
"last_sent_time"
:
"string"
,
"created_by_flow"
:
"MULTIPLE_RECIPIENTS_GROUP"
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"has_conditional_rule"
:
false
,
"save_item_for_future"
:
true
,
"show_additional_item_fields"
:
false
,
"discount_mode_preference"
:
"ONE_TIME"
,
"theme"
:
{
"primary_color"
:
"string"
}
,
"template_id"
:
"PayPal system template"
,
"payment_method_overrides"
:
[
{
"payment_method_type"
:
"PAY_BY_BANK"
,
"enabled"
:
true
,
"rules"
:
[
{
"rule_type"
:
"EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD"
,
"rule_value"
:
"string"
}
]
}
]
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
,
"custom"
:
{
"label"
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
}
}
}
,
"due_amount"
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
"gratuity"
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
"payments"
:
{
"transactions"
:
[
{
"payment_id"
:
"string"
,
"note"
:
"string"
,
"type"
:
"PAYPAL"
,
"payment_date"
:
"string"
,
"payment_date_time"
:
"string"
,
"method"
:
"BANK_TRANSFER"
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
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"paid_amount"
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
"refunds"
:
{
"transactions"
:
[
{
"refund_id"
:
"string"
,
"type"
:
"PAYPAL"
,
"refund_date"
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
"method"
:
"BANK_TRANSFER"
}
]
,
"refund_amount"
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
Invoice auto reminder configuration metadata.
Invoice auto reminder configuration metadata.
created_time
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
Represents the date and time at which this auto reminder configuration was created.
updated_time
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
Represents the date and time at which this auto reminder configuration was last updated.
Copy
{
"created_time"
:
"string"
,
"updated_time"
:
"string"
}
Invoice auto reminder interval
Defines the time interval used to determine when a reminder is sent relative to the invoice due date. The interval consists of a unit (for example, DAY) and a numeric value that specifies how many units before or after the due date the reminder is triggered.
unit
required
string
(
reminder_interval_unit
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Defines the recurrence unit of time for sending automatic reminders.
Value
Description
DAY
Reminders are sent daily.
value
required
integer
[ 1 .. 7 ]
The number of time units before or after the invoice due date when the reminder is sent. Minimum value is 1 and maximum value is 7.
Copy
{
"unit"
:
"DAY"
,
"value"
:
1
}
Invoice Connection Details
Returns invoice connection status with timestamp per invoice.
id
string
[ 1 .. 64 ] characters
^[A-Za-z0-9\-]+$
The ID of the invoice. This property supports Unicode.
connection_status
Array of
objects
(
Connections
)
[ 1 .. 1000 ] items
An array of connection-level details.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"connection_status"
:
[
{
"connections"
:
[
{
"platform_name"
:
"string"
,
"last_sync_status"
:
"IN_PROGRESS"
,
"last_sync_time"
:
"string"
}
]
}
]
}
Invoice Number
The invoice number.
invoice_number
string
[ 1 .. 25 ] characters
^[\S\s]*$
The invoice number. If you omit this value, the default is the auto-incremented number from the last number.
invoice_id
string
[ 1 .. 24 ] characters
^(INV2-)[A-Z0-9\-]{19}$
Resource Id.
Copy
{
"invoice_number"
:
"string"
,
"invoice_id"
:
"string"
}
invoice_additional_setting
The invoice additional setting.
field_name
string
(
invoice_additional_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field names for additional sections in the invoice.
Enum Value
Description
ATTACHMENT
The file attachments added to the invoice.
MEMO
The internal memo in the invoice that is visible only to the invoicer.
REFERENCE
The reference number in the invoice for tracking or correlation.
display_preference
object
(
display_preference
)
The display preference of the field.
Copy
Expand all
Collapse all
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
invoice_additional_settings_field
The field names for additional sections in the invoice.
string
(
invoice_additional_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field names for additional sections in the invoice.
Enum Value
Description
ATTACHMENT
The file attachments added to the invoice.
MEMO
The internal memo in the invoice that is visible only to the invoicer.
REFERENCE
The reference number in the invoice for tracking or correlation.
Copy
"ATTACHMENT"
invoice_auto_reminder_config_setup
Request body for initializing invoice auto reminder configuration. The request may include up to two reminder configurations (BEFORE_DUE and AFTER_DUE), which will be applied to all invoices created by the merchant. If only one reminder type is provided, the missing reminder type will be created using the default configuration in INACTIVE state. If the request body is empty, both reminder types will be created using the default configuration in INACTIVE state. Reminder configurations created using the provided payload are set to ACTIVE state.
configurations
Array of
objects
(
invoice_reminder_configuration
)
[ 1 .. 2 ] items
An array of invoice auto reminder configurations. The array can contain a maximum of two configurations, one for BEFORE_DUE reminder type and one for AFTER_DUE reminder type.
Copy
Expand all
Collapse all
{
"configurations"
:
[
{
"id"
:
"stringstringstringst"
,
"type"
:
"BEFORE_DUE"
,
"status"
:
"ACTIVE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
1
}
,
"repetition"
:
1
,
"notification"
:
{
"send_to_invoicer"
:
false
}
,
"metadata"
:
{
"created_time"
:
"string"
,
"updated_time"
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
}
]
}
]
}
invoice_creation_flow
The frequency at which the invoice is sent:
Multiple recipient. Sent to multiple recipients.
Batch. Sent in a batch.
Regular single. Sent one time to a single recipient.
string
(
invoice_creation_flow
)
[ 0 .. 255 ] characters
^[\s\S]*$
The frequency at which the invoice is sent:
Multiple recipient. Sent to multiple recipients.
Batch. Sent in a batch.
Regular single. Sent one time to a single recipient.
Enum Value
Description
MULTIPLE_RECIPIENTS_GROUP
The invoice sent to multiple recipients.
BATCH
The invoice sent as a batch.
REGULAR_SINGLE
The regular invoice sent to single recipient.
Copy
"MULTIPLE_RECIPIENTS_GROUP"
invoice_detail
The details of the invoice. Includes invoice number, date, payment terms, and audit metadata.
reference
string
[ 1 .. 120 ] characters
^[\S\s]*$
The reference data. Includes a Purchase Order (PO) number.
note
string
[ 1 .. 4000 ] characters
^[\S\s]*$
A note to the invoice recipient. Also appears on the invoice notification email.
terms_and_conditions
string
[ 1 .. 4000 ] characters
^[\S\s]*$
The general terms of the invoice. Can include return or cancellation policy and other terms and conditions.
memo
string
[ 1 .. 500 ] characters
^[\S\s]*$
A private bookkeeping memo for the user.
attachments
Array of
objects
(
File Reference
)
[ 0 .. 2147483647 ] items
An array of PayPal IDs for the files that are attached to an invoice.
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
tip_presets
Array of
objects
(
tip_preset
)
[ 1 .. 3 ] items
Specifies the predefined tip options configured by the invoicer. These preset values are shown to customers at checkout as suggested tipping amounts, in addition to the option to enter a custom tip.
order_details
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Order details information.
project_details
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Project details information.
service_details
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Service details information.
payment_terms
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Payment terms information.
return_policy
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Return policy information.
cancellation_policy
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Cancellation policy information.
service_agreement
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Service agreement information.
invoice_number
string
<= 25 characters
The invoice number. Default is the number that is auto-incremented number from the last number.
invoice_date
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
payment_term
object
(
invoice_payment_term
)
The payment term of the invoice. Payment can be due upon receipt, a specified date, or in a set number of days.
metadata
object
(
metadata
)
The audit metadata. Captures all invoicing actions on create, send, update, and cancel.
Copy
Expand all
Collapse all
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"tip_presets"
:
[
{
"percent"
:
"19.99"
}
]
,
"order_details"
:
"string"
,
"project_details"
:
"string"
,
"service_details"
:
"string"
,
"payment_terms"
:
"string"
,
"return_policy"
:
"string"
,
"cancellation_policy"
:
"string"
,
"service_agreement"
:
"string"
,
"invoice_number"
:
"string"
,
"invoice_date"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
,
"due_date"
:
"string"
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"cancelled_by"
:
"string"
,
"last_sent_by"
:
"string"
,
"recipient_view_url"
:
"
http://example.com
"
,
"invoicer_view_url"
:
"
http://example.com
"
,
"cancel_time"
:
"string"
,
"first_sent_time"
:
"string"
,
"last_sent_time"
:
"string"
,
"created_by_flow"
:
"MULTIPLE_RECIPIENTS_GROUP"
}
}
invoice_details_setting
The invoice details setting.
field_name
string
(
invoice_details_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field names for the invoice details.
Enum Value
Description
ORDER_DETAILS
Order details information in the invoice.
PROJECT_DETAILS
Project details information in the invoice.
SERVICE_DETAILS
Service details information in the invoice.
display_preference
object
(
display_preference
)
The display preference of the field.
Copy
Expand all
Collapse all
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
invoice_details_settings_field
The field names for the invoice details.
string
(
invoice_details_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field names for the invoice details.
Enum Value
Description
ORDER_DETAILS
Order details information in the invoice.
PROJECT_DETAILS
Project details information in the invoice.
SERVICE_DETAILS
Service details information in the invoice.
Copy
"ORDER_DETAILS"
invoice_free_text_search_fields
Supported invoice free text search fields.
string
(
invoice_free_text_search_fields
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Supported invoice free text search fields.
Enum Value
Description
INVOICE_NUMBER
Invoice number.
NOTES
Notes associated with the invoice.
MERCHANT_MEMO
Merchant memo related to the invoice.
PAYER_REFERENCE_INFO
Payer's reference information.
BILLING_EMAIL
Email address associated with billing.
BILLING_NAME
Name associated with billing.
BILLING_BUSINESS_NAME
Business name associated with billing.
BILLING_PHONE_NUMBER
Phone number associated with billing.
SHIPPING_EMAIL
Email address associated with shipping.
SHIPPING_NAME
Name associated with shipping.
SHIPPING_BUSINESS_NAME
Business name associated with shipping.
SHIPPING_PHONE_NUMBER
Phone number associated with shipping.
ITEM_NAME
Name of the invoice item.
ITEM_TAX_NAME
Tax name associated with the invoice item.
ITEM_DISCOUNT_NAME
Discount name associated with the invoice item.
TRANSACTION_ID
Transaction ID associated with the invoice payment.
GROUP_ID
Group ID associated with the invoice.
INVOICE_DISCOUNT_NAME
Discount name associated with the invoice.
ALL
Search in all available search fields (except GROUP_ID).
Copy
"INVOICE_NUMBER"
invoice_item_field
The field name for the invoice item.
string
(
invoice_item_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field name for the invoice item.
Enum Value
Description
ITEM_DESCRIPTION
The description of the item.
ITEM_DATE
The date of the item.
ITEM_TAX
The tax of the item.
ITEM_DISCOUNT
The discount of the item.
Copy
"ITEM_DESCRIPTION"
invoice_item_setting
The invoice item setting.
field_name
string
(
invoice_item_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field name for the invoice item.
Enum Value
Description
ITEM_DESCRIPTION
The description of the item.
ITEM_DATE
The date of the item.
ITEM_TAX
The tax of the item.
ITEM_DISCOUNT
The discount of the item.
display_preference
object
(
display_preference
)
The display preference of the field.
Copy
Expand all
Collapse all
{
"field_name"
:
"ITEM_DESCRIPTION"
,
"display_preference"
:
{
"hidden"
:
true
}
}
invoice_payment_term
The payment term of the invoice. Payment can be due upon receipt, a specified date, or in a set number of days.
term_type
string
(
payment_term_type
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment term. Payment can be due upon receipt, a specified date, or in a set number of days.
Enum Value
Description
DUE_ON_RECEIPT
The payment for the invoice is due upon receipt of the invoice.
DUE_ON_DATE_SPECIFIED
The payment for the invoice is due on the date specified in the invoice.
NET_10
The payment for the invoice is due in 10 days.
NET_15
The payment for the invoice is due in 15 days.
NET_30
The payment for the invoice is due in 30 days.
NET_45
The payment for the invoice is due in 45 days.
NET_60
The payment for the invoice is due in 60 days.
NET_90
The payment for the invoice is due in 90 days.
NO_DUE_DATE
The invoice has no payment due date.
conditional_rules
object
(
payment_term_conditional_rules
)
The conditional rules associated with the payment term of the invoice. Includes early payment discount, late payment surcharge, and auto cancellation details.
due_date
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
Expand all
Collapse all
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
,
"due_date"
:
"string"
}
invoice_policy_and_agreement_setting
The invoice policy and agreement setting.
field_name
string
(
invoice_policy_and_agreement_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field names for the policy and agreement details in the invoice.
Enum Value
Description
CANCELLATION_POLICY
Cancellation policy information in the invoice.
PAYMENT_TERMS
Payment terms information in the invoice.
RETURN_POLICY
Return policy information in the invoice.
SERVICE_AGREEMENT
Service agreement information in the invoice.
TERMS_AND_CONDITIONS
Terms and conditions information in the invoice.
display_preference
object
(
display_preference
)
The display preference of the field.
Copy
Expand all
Collapse all
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
invoice_policy_and_agreement_settings_field
The field names for the policy and agreement details in the invoice.
string
(
invoice_policy_and_agreement_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field names for the policy and agreement details in the invoice.
Enum Value
Description
CANCELLATION_POLICY
Cancellation policy information in the invoice.
PAYMENT_TERMS
Payment terms information in the invoice.
RETURN_POLICY
Return policy information in the invoice.
SERVICE_AGREEMENT
Service agreement information in the invoice.
TERMS_AND_CONDITIONS
Terms and conditions information in the invoice.
Copy
"CANCELLATION_POLICY"
invoice_reminder_configuration
Invoice reminder configuration object to specify the frequency, reminder type and other params related to invoice auto reminder configuration.
id
string
= 20 characters
^RC-[A-Z0-9]+$
Represents the auto reminder configuration id.
type
required
string
(
reminder_type
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The type of the auto reminder configuration.
Enum Value
Description
BEFORE_DUE
Represents the auto reminder configuration for invoices prior to their due date.
AFTER_DUE
Represents the auto reminder configuration for invoices after their due date.
status
string
(
reminder_status
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The status of the auto reminder configuration.
Enum Value
Description
ACTIVE
Specifies the configuration is active.
INACTIVE
Specifies the configuration is inactive.
interval
required
object
(
Invoice auto reminder interval
)
Defines the time interval used to determine when a reminder is sent relative to the invoice due date. The interval consists of a unit (for example, DAY) and a numeric value that specifies how many units before or after the due date the reminder is triggered.
repetition
required
integer
[ 1 .. 7 ]
The repetition at which the auto reminder has to be set. Note: For
BEFORE_DUE
reminder type, repetition is always one.
notification
object
(
Notification
)
The email notification to send to the invoicer or payer on auto reminder configuration.
metadata
object
(
Invoice auto reminder configuration metadata.
)
Invoice auto reminder configuration metadata.
links
Array of
objects
(
Link Description
)
[ 1 .. 4 ] items
An array of request-related
HATEOAS links
.
Copy
Expand all
Collapse all
{
"id"
:
"stringstringstringst"
,
"type"
:
"BEFORE_DUE"
,
"status"
:
"ACTIVE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
1
}
,
"repetition"
:
1
,
"notification"
:
{
"send_to_invoicer"
:
false
}
,
"metadata"
:
{
"created_time"
:
"string"
,
"updated_time"
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
}
]
}
invoice_reminder_configurations
List of invoice reminder configurations.
configurations
Array of
objects
(
invoice_reminder_configuration
)
[ 1 .. 2 ] items
An array of invoice auto reminder configurations.
links
Array of
objects
(
Link Description
)
[ 1 .. 4 ] items
An array of request-related
HATEOAS links
.
Copy
Expand all
Collapse all
{
"configurations"
:
[
{
"id"
:
"stringstringstringst"
,
"type"
:
"BEFORE_DUE"
,
"status"
:
"ACTIVE"
,
"interval"
:
{
"unit"
:
"DAY"
,
"value"
:
1
}
,
"repetition"
:
1
,
"notification"
:
{
"send_to_invoicer"
:
false
}
,
"metadata"
:
{
"created_time"
:
"string"
,
"updated_time"
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
}
]
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
invoice_settings
The settings for the invoice.
invoice_item_settings
Array of
objects
(
invoice_item_setting
)
[ 1 .. 10 ] items
The settings for the invoice items.
invoice_additional_settings
Array of
objects
(
invoice_additional_setting
)
[ 1 .. 10 ] items
The settings for the invoice additional fields.
invoice_policy_and_agreement_settings
Array of
objects
(
invoice_policy_and_agreement_setting
)
[ 1 .. 10 ] items
The settings for the invoice policy and agreement fields.
invoice_details_settings
Array of
objects
(
invoice_details_setting
)
[ 1 .. 10 ] items
The settings for the invoice details fields.
Copy
Expand all
Collapse all
{
"invoice_item_settings"
:
[
{
"field_name"
:
"ITEM_DESCRIPTION"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_additional_settings"
:
[
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_policy_and_agreement_settings"
:
[
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
}
invoice_status
The status of the invoice.
string
(
invoice_status
)
[ 0 .. 255 ] characters
^[\s\S]*$
The status of the invoice.
Enum Value
Description
DRAFT
The invoice is in draft state. It is not yet sent to the payer.
SENT
The invoice has been sent to the payer. The payment is awaited from the payer.
SCHEDULED
The invoice is scheduled on a future date. It is not yet sent to the payer.
PAID
The payer has paid for the invoice.
MARKED_AS_PAID
The invoice is marked as paid by the invoicer.
CANCELLED
The invoice has been cancelled by the invoicer.
REFUNDED
The invoice has been refunded by the invoicer.
PARTIALLY_PAID
The payer has partially paid for the invoice.
PARTIALLY_REFUNDED
The invoice has been partially refunded by the invoicer.
MARKED_AS_REFUNDED
The invoice is marked as refunded by the invoicer.
UNPAID
The invoicer is yet to receive the payment from the payer for the invoice.
PAYMENT_PENDING
The invoicer is yet to receive the payment for the invoice. It is under pending review.
AUTO_CANCELLED
The invoice was automatically cancelled because the payment was not received within the specified timeframe.
PAID_EXTERNAL
The invoice has been paid through an external system or method outside of the standard PayPal payment flow. This status is set manually, indicating payment was received through other means.
REFUNDED_EXTERNAL
The invoice has been refunded through an external system or method. This status indicates a refund was issued outside of the standard PayPal payment flow.
SHARED
The invoice has been shared with the payer, typically via a link or other method. This status is used to track when an invoice has been distributed but not necessarily sent via PayPal.
Copy
"DRAFT"
invoice_statuses_for_aggregation
Status of the invoice enum for aggregation purposes.
string
(
invoice_statuses_for_aggregation
)
[ 1 .. 100 ] characters
^[A-Z0-9_]+$
Status of the invoice enum for aggregation purposes.
Enum Value
Description
OUTSTANDING
Invoices that are sent but not yet paid or only partially paid.
PAID
Invoices that have been fully paid.
Copy
"OUTSTANDING"
invoice_suggestion_fields
Supported invoice suggestion fields.
string
(
invoice_suggestion_fields
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Supported invoice suggestion fields.
Enum Value
Description
INVOICE_NUMBER
Number associated with it.
NOTES
Notes associated with the invoice.
MERCHANT_MEMO
Merchant memo related to the invoice.
PAYER_REFERENCE_INFO
Payer's reference information.
BILLING_EMAIL
Email address associated with billing.
BILLING_NAME
Name associated with billing.
BILLING_BUSINESS_NAME
Business name associated with billing.
BILLING_PHONE_NUMBER
Phone number associated with billing.
SHIPPING_EMAIL
Email address associated with shipping.
SHIPPING_NAME
Name associated with shipping.
SHIPPING_BUSINESS_NAME
Business name associated with shipping.
SHIPPING_PHONE_NUMBER
Phone number associated with shipping.
ITEM_NAME
Name of the invoice item.
TRANSACTION_ID
Transaction ID associated with the invoice payment.
ALL
This is used to search in all available search fields.
Copy
"INVOICE_NUMBER"
invoicer_info
The invoicer business information that appears on the invoice.
business_name
string
<= 300 characters
Required. The business name of the party.
name
object
(
Name
)
The name of the party.
address
object
(
Portable Postal Address (Medium-Grained)
)
The portable international postal address. Maps to
AddressValidationMetadata
and HTML 5.1
Autofilling form controls: the autocomplete attribute
.
phones
Array of
objects
(
phone_detail
)
An array of invoicer's phone numbers. The invoicer can choose to hide the phone number on the invoice.
website
string
<
uri
>
<= 2048 characters
The invoicer's website.
tax_id
string
<= 100 characters
The invoicer's tax ID.
additional_notes
string
<= 400 characters
Any additional information. Includes business hours.
logo_url
string
<
uri
>
<= 2000 characters
The full URL to an external logo image. The logo image must not be larger than 250 pixels wide by 90 pixels high.
email_address
string
(
restrictive_email_address
)
[ 3 .. 254 ] characters
^(?!\.)(?:[A-Za-z0-9!#$&'*\/=?^`{|}~_%+-]|\.(...
Show pattern
The internationalized email address with more restrictive rules. This version restricts the local-part to a dot-atom as defined in
https://www.ietf.org/rfc/rfc5322.txt
. It does not allow for a quoted-string or an obs-local-part.
Allows alphanumeric and RFC-allowed special characters, !#$%&'*+-/=?^_`{|}~
Ensures that the local part does not start with dot (.), have consecutive dots, or end with dot. Ensures that the domain part does not have consecutive dots.
Ensures that the local part does not exceed 64 characters.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
Copy
Expand all
Collapse all
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
invoices
An array of merchant invoices. Includes the total invoices count and
HATEOAS links
for navigation.
total_pages
integer
[ 0 .. 2147483647 ]
The total number of pages that are available for the search criteria.
Note:
Clients MUST NOT assume that the value of total_pages is constant. The value MAY change from one request to the next
total_items
integer
[ 0 .. 2147483647 ]
The total number of invoices that match the search criteria.
Note:
Clients MUST NOT assume that the value of
total_items
is constant. The value MAY change from one request to the next.
items
Array of
objects
(
invoice
)
[ 0 .. 100 ] items
The list of invoices that match the search criteria.
links
Array of
objects
(
Link Description
)
[ 0 .. 2147483647 ] items
An array of request-related
HATEOAS links
.
Copy
Expand all
Collapse all
{
"total_pages"
:
2147483647
,
"total_items"
:
2147483647
,
"items"
:
[
{
"id"
:
"string"
,
"parent_id"
:
"string"
,
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
null
,
"street_name"
:
null
,
"street_type"
:
null
,
"delivery_service"
:
null
,
"building_name"
:
null
,
"sub_building"
:
null
}
}
,
"phones"
:
[
{
"country_code"
:
null
,
"national_number"
:
null
,
"extension_number"
:
null
,
"phone_type"
:
null
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
null
,
"street_name"
:
null
,
"street_type"
:
null
,
"delivery_service"
:
null
,
"building_name"
:
null
,
"sub_building"
:
null
}
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
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
}
,
"unit_of_measure"
:
"QUANTITY"
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
"status"
:
"DRAFT"
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"tip_presets"
:
[
{
"percent"
:
"19.99"
}
]
,
"order_details"
:
"string"
,
"project_details"
:
"string"
,
"service_details"
:
"string"
,
"payment_terms"
:
"string"
,
"return_policy"
:
"string"
,
"cancellation_policy"
:
"string"
,
"service_agreement"
:
"string"
,
"invoice_number"
:
"string"
,
"invoice_date"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
,
"due_date"
:
"string"
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"cancelled_by"
:
"string"
,
"last_sent_by"
:
"string"
,
"recipient_view_url"
:
"
http://example.com
"
,
"invoicer_view_url"
:
"
http://example.com
"
,
"cancel_time"
:
"string"
,
"first_sent_time"
:
"string"
,
"last_sent_time"
:
"string"
,
"created_by_flow"
:
"MULTIPLE_RECIPIENTS_GROUP"
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"has_conditional_rule"
:
false
,
"save_item_for_future"
:
true
,
"show_additional_item_fields"
:
false
,
"discount_mode_preference"
:
"ONE_TIME"
,
"theme"
:
{
"primary_color"
:
"string"
}
,
"template_id"
:
"PayPal system template"
,
"payment_method_overrides"
:
[
{
"payment_method_type"
:
"PAY_BY_BANK"
,
"enabled"
:
true
,
"rules"
:
[
{
"rule_type"
:
null
,
"rule_value"
:
null
}
]
}
]
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
}
,
"custom"
:
{
"label"
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
}
}
}
,
"settings"
:
{
"invoice_item_settings"
:
[
{
"field_name"
:
"ITEM_DESCRIPTION"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_additional_settings"
:
[
{
"field_name"
:
"ATTACHMENT"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_policy_and_agreement_settings"
:
[
{
"field_name"
:
"CANCELLATION_POLICY"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
,
"invoice_details_settings"
:
[
{
"field_name"
:
"ORDER_DETAILS"
,
"display_preference"
:
{
"hidden"
:
true
}
}
]
}
,
"due_amount"
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
"gratuity"
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
"payments"
:
{
"transactions"
:
[
{
"payment_id"
:
"string"
,
"note"
:
"string"
,
"type"
:
"PAYPAL"
,
"payment_date"
:
"string"
,
"payment_date_time"
:
"string"
,
"method"
:
"BANK_TRANSFER"
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
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
:
{
"prefix"
:
null
,
"given_name"
:
null
,
"surname"
:
null
,
"middle_name"
:
null
,
"suffix"
:
null
,
"alternate_full_name"
:
null
,
"full_name"
:
null
}
,
"address"
:
{
"address_line_1"
:
null
,
"address_line_2"
:
null
,
"address_line_3"
:
null
,
"admin_area_4"
:
null
,
"admin_area_3"
:
null
,
"admin_area_2"
:
null
,
"admin_area_1"
:
null
,
"postal_code"
:
null
,
"country_code"
:
null
,
"address_details"
:
{ }
}
}
}
]
,
"paid_amount"
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
"effective_invoice_total"
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
"effective_due_amount"
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
"refunds"
:
{
"transactions"
:
[
{
"refund_id"
:
"string"
,
"type"
:
"PAYPAL"
,
"refund_date"
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
"method"
:
"BANK_TRANSFER"
}
]
,
"refund_amount"
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
invoices
Suggestion object contains the specified text and the field associated with it.
suggested_text
string
[ 3 .. 800 ] characters
^(?!\s*$).+
Represents the text which has been provided in request.
fields
Array of
strings
(
invoice_suggestion_fields
)
[ 1 .. 14 ] items
unique
An array of matched invoice fields.
Items
Enum Value
Description
INVOICE_NUMBER
Number associated with it.
NOTES
Notes associated with the invoice.
MERCHANT_MEMO
Merchant memo related to the invoice.
PAYER_REFERENCE_INFO
Payer's reference information.
BILLING_EMAIL
Email address associated with billing.
BILLING_NAME
Name associated with billing.
BILLING_BUSINESS_NAME
Business name associated with billing.
BILLING_PHONE_NUMBER
Phone number associated with billing.
SHIPPING_EMAIL
Email address associated with shipping.
SHIPPING_NAME
Name associated with shipping.
SHIPPING_BUSINESS_NAME
Business name associated with shipping.
SHIPPING_PHONE_NUMBER
Phone number associated with shipping.
ITEM_NAME
Name of the invoice item.
TRANSACTION_ID
Transaction ID associated with the invoice payment.
ALL
This is used to search in all available search fields.
Copy
Expand all
Collapse all
{
"suggested_text"
:
"string"
,
"fields"
:
[
"INVOICE_NUMBER"
]
}
Invoicing Product Features
Invoicing product features for a merchant.
object
(
Invoicing Product Features
)
Invoicing product features for a merchant.
Copy
{ }
item
An array of invoice line item information. The maximum items for an invoice is
100
.
id
string
[ 0 .. 22 ] characters
^[\S\s]*$
The ID of the invoice line item.
name
required
string
[ 0 .. 200 ] characters
^[\S\s]*$
The item name for the invoice line item.
description
string
[ 0 .. 1000 ] characters
^[\S\s]*$
The item description for the invoice line item.
quantity
required
string
[ 0 .. 14 ] characters
\d+(.\d{1,5})?$
The quantity of the item that the invoicer provides to the payer. Value is from
-1000000
to
1000000
. Supports up to five decimal places.
unit_amount
required
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
tax
object
(
tax
)
The tax information. Includes the tax name and tax rate of invoice items. The tax amount is added to the item total.
item_date
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
discount
object
(
discount
)
The discount as a percent or amount at invoice level. The invoice discount amount is subtracted from the item total.
unit_of_measure
string
(
unit_of_measure
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The unit of measure for the invoiced item. For
AMOUNT
the
unit_amount
and
quantity
are not shown on the invoice.
Note:
If your specify different
unit_of_measure
values for the same invoice, the invoice uses the first value.
Enum Value
Description
QUANTITY
The unit of measure is quantity. This invoice template is typically used for physical goods.
HOURS
The unit of measure is hours. This invoice template is typically used for services.
AMOUNT
The unit of measure is amount. This invoice template is typically used when only amount is required.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
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
}
,
"unit_of_measure"
:
"QUANTITY"
}
language
The
language tag
for the language in which to localize the error-related strings, such as messages, issues, and suggested actions. The tag is made up of the
ISO 639-2 language code
, the optional
ISO-15924 script tag
, and the
ISO-3166 alpha-2 country code
or
M49 region code
.
string
<
ppaas_common_language_v3
>
(
language
)
[ 2 .. 10 ] characters
^[a-z]{2}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}|[...
Show pattern
The
language tag
for the language in which to localize the error-related strings, such as messages, issues, and suggested actions. The tag is made up of the
ISO 639-2 language code
, the optional
ISO-15924 script tag
, and the
ISO-3166 alpha-2 country code
or
M49 region code
.
Copy
"string"
late_payment_surcharge
The late payment surcharge for the invoice. If the payer pays after the surcharge effective date, the specified surcharge is applied.
is_applied
boolean
Indicates whether the particular rule is applied or not.
surcharge_effective_date
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
percent
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
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
layout
Supported invoice layouts.
string
(
layout
)
[ 1 .. 155 ] characters
^[A-Z0-9_]+$
Supported invoice layouts.
Enum Value
Description
CLASSIC
Default classic invoice layout.
BRANDED
Customised invoice layout.
Copy
"CLASSIC"
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
metadata
The audit metadata. Captures all invoicing actions on create, send, update, and cancel.
created_by
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The email address of the account that created the resource.
last_updated_by
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The email address of the account that last edited the resource.
create_time
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
last_update_time
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
cancelled_by
string
The actor who canceled the resource.
last_sent_by
string
The email address of the account that last sent the resource.
recipient_view_url
string
<
uri
>
The URL for the invoice payer view hosted on paypal.com.
invoicer_view_url
string
<
uri
>
The URL for the invoice merchant view hosted on paypal.com.
cancel_time
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
first_sent_time
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
last_sent_time
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
created_by_flow
string
(
invoice_creation_flow
)
[ 0 .. 255 ] characters
^[\s\S]*$
The flow variation that created this invoice.
Enum Value
Description
MULTIPLE_RECIPIENTS_GROUP
The invoice sent to multiple recipients.
BATCH
The invoice sent as a batch.
REGULAR_SINGLE
The regular invoice sent to single recipient.
Copy
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"cancelled_by"
:
"string"
,
"last_sent_by"
:
"string"
,
"recipient_view_url"
:
"
http://example.com
"
,
"invoicer_view_url"
:
"
http://example.com
"
,
"cancel_time"
:
"string"
,
"first_sent_time"
:
"string"
,
"last_sent_time"
:
"string"
,
"created_by_flow"
:
"MULTIPLE_RECIPIENTS_GROUP"
}
metric
This indicates the metrics of the each dimensions we are aggregating.
string
(
metric
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
This indicates the metrics of the each dimensions we are aggregating.
Enum Value
Description
LIKES_COUNT
Total number of likes for the given time period.
DISLIKES_COUNT
Total number of dislikes for the given time period.
TOTAL_FEEDBACK_COUNT
Total number of feedbacks for the given time period.
INVOICES_RATED_PERCENT
Percentage of invoice rated out of sent for the given time period.
Copy
"LIKES_COUNT"
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
notification
The email or SMS notification to send to the invoicer or payer on sending an invoice.
subject
string
[ 0 .. 4000 ] characters
^[\S\s]*$
The subject of the email that is sent as a notification to the recipient.
Note:
User-provided values for this field will not be honored and the subject will always be defaulted to a system-defined value.
note
string
[ 0 .. 4000 ] characters
^[\S\s]*$
A note to the payer.
Note:
User-provided values for this field will not be honored and the note will always be defaulted to a system-defined value.
send_to_invoicer
boolean
Default:
false
Indicates whether to send a copy of the email to the merchant.
send_to_recipient
boolean
Default:
true
Indicates whether to send a copy of the email to the recipient.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 0 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
Copy
Expand all
Collapse all
{
"subject"
:
"string"
,
"note"
:
"string"
,
"send_to_invoicer"
:
false
,
"send_to_recipient"
:
true
,
"additional_recipients"
:
[
"string"
]
}
Notification
The email notification to send to the invoicer or payer on auto reminder configuration.
send_to_invoicer
boolean
Default:
false
Indicates whether to send a copy of the email to the merchant.
Copy
{
"send_to_invoicer"
:
false
}
override_payment_method_detail
The details about a payment method override configured for the invoice via payment method overrides object.
payment_method_type
string
(
override_payment_method_type
)
[ 1 .. 120 ] characters
^[A-Z0-9_]*$
The payment method types that can be configured in the payment method overrides object for invoice payments.
Note:
To use
PAY_BY_BANK
, you must first complete the onboarding process. Visit the
onboarding page
to get started. Once onboarding is complete, you can configure
PAY_BY_BANK
as a payment method.
Value
Description
PAY_BY_BANK
Enables the buyer to pay the invoice directly from their bank account. Available only for US-based merchants and invoices with USD currency.
enabled
boolean
Indicates whether the specified payment method is enabled for the invoice. When set to
true
, the payment method is available for the buyer to use. When set to
false
, the payment method is disabled.
rules
Array of
objects
(
override_payment_method_rule
)
[ 1 .. 10 ] items
The list of payment method override rules applied to the invoice via payment method overrides object. Each rule defines a specific restriction or behavior for the payment method, such as making it the exclusive payment option when the invoice total exceeds a system-defined threshold.
Copy
Expand all
Collapse all
{
"payment_method_type"
:
"PAY_BY_BANK"
,
"enabled"
:
true
,
"rules"
:
[
{
"rule_type"
:
"EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD"
,
"rule_value"
:
"string"
}
]
}
override_payment_method_rule
The details about a payment method override rule applied to the invoice via payment method overrides object.
rule_type
required
string
(
override_payment_method_rule_type
)
[ 1 .. 150 ] characters
^[A-Z0-9_]*$
The type of rule that can be applied to a payment method configured via payment method overrides object on an invoice. Each rule controls how a payment method behaves based on the invoice total.
System-defined threshold limits by payment method:
PAY_BY_BANK - $1000
Value
Description
EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD
When the invoice total exceeds the system-defined threshold, this rule restricts the invoice to accept only the specified payment method and disables all other payment methods. This rule is currently compatible only with the PAY_BY_BANK payment method.
rule_value
required
string
[ 1 .. 100 ] characters
^[a-zA-Z0-9\s,.]+$
The value associated with the payment method override rule. For the
EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD
rule type, set this to
true
to enable the rule or
false
to disable it.
Copy
{
"rule_type"
:
"EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD"
,
"rule_value"
:
"string"
}
override_payment_method_rule_type
The type of rule that can be applied to a payment method configured via payment method overrides object on an invoice. Each rule controls how a payment method behaves based on the invoice total.
System-defined threshold limits by payment method:
PAY_BY_BANK - $1000
string
(
override_payment_method_rule_type
)
[ 1 .. 150 ] characters
^[A-Z0-9_]*$
The type of rule that can be applied to a payment method configured via payment method overrides object on an invoice. Each rule controls how a payment method behaves based on the invoice total.
System-defined threshold limits by payment method:
PAY_BY_BANK - $1000
Value
Description
EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD
When the invoice total exceeds the system-defined threshold, this rule restricts the invoice to accept only the specified payment method and disables all other payment methods. This rule is currently compatible only with the PAY_BY_BANK payment method.
Copy
"EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD"
override_payment_method_type
The payment method types that can be configured in the payment method overrides object for invoice payments.
Note:
To use
PAY_BY_BANK
, you must first complete the onboarding process. Visit the
onboarding page
to get started. Once onboarding is complete, you can configure
PAY_BY_BANK
as a payment method.
string
(
override_payment_method_type
)
[ 1 .. 120 ] characters
^[A-Z0-9_]*$
The payment method types that can be configured in the payment method overrides object for invoice payments.
Note:
To use
PAY_BY_BANK
, you must first complete the onboarding process. Visit the
onboarding page
to get started. Once onboarding is complete, you can configure
PAY_BY_BANK
as a payment method.
Value
Description
PAY_BY_BANK
Enables the buyer to pay the invoice directly from their bank account. Available only for US-based merchants and invoices with USD currency.
Copy
"PAY_BY_BANK"
partial_payment
The partial payment details. Includes the minimum amount that the invoicer expects from the payer.
allow_partial_payment
boolean
Default:
false
Indicates whether the invoice allows a partial payment. If
false
, the invoice must be paid in full. If
true
, the invoice allows partial payments.
Note:
This feature is not available for users in
India
,
Brazil
, or
Israel
.
minimum_amount_due
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
Patch
The JSON patch object to apply partial updates to resources.
op
required
string
The operation.
Enum Value
Description
add
Depending on the target location reference, completes one of these functions:
The target location is an array index
. Inserts a new value into the array at the specified index.
The target location is an object parameter that does not already exist
. Adds a new parameter to the object.
The target location is an object parameter that does exist
. Replaces that parameter's value.
The
value
parameter defines the value to add. For more information, see
4.1. add
.
remove
Removes the value at the target location. For the operation to succeed, the target location must exist. For more information, see
4.2. remove
.
replace
Replaces the value at the target location with a new value. The operation object must contain a
value
parameter that defines the replacement value. For the operation to succeed, the target location must exist. For more information, see
4.3. replace
.
move
Removes the value at a specified location and adds it to the target location. The operation object must contain a
from
parameter, which is a string that contains a JSON pointer value that references the location in the target document from which to move the value. For the operation to succeed, the
from
location must exist. For more information, see
4.4. move
.
copy
Copies the value at a specified location to the target location. The operation object must contain a
from
parameter, which is a string that contains a JSON pointer value that references the location in the target document from which to copy the value. For the operation to succeed, the
from
location must exist. For more information, see
4.5. copy
.
test
Tests that a value at the target location is equal to a specified value. The operation object must contain a
value
parameter that defines the value to compare to the target location's value. For the operation to succeed, the target location must be equal to the
value
value. For test,
equal
indicates that the value at the target location and the value that
value
defines are of the same JSON type. The data type of the value determines how equality is defined:
Type
Considered equal if both values
strings
Contain the same number of Unicode characters and their code points are byte-by-byte equal.
numbers
Are numerically equal.
arrays
Contain the same number of values, and each value is equal to the value at the corresponding position in the other array, by using these type-specific rules.
objects
Contain the same number of parameters, and each parameter is equal to a parameter in the other object, by comparing their keys (as strings) and their values (by using these type-specific rules).
literals (
false
,
true
, and
null
)
Are the same. The comparison is a logical comparison. For example, whitespace between the parameter values of an array is not significant. Also, ordering of the serialization of object parameters is not significant.
For more information, see
4.6. test
.
path
string
The
JSON Pointer
to the target document location at which to complete the operation.
value
any
(
Patch Value
)
The value to apply. The
remove
,
copy
, and
move
operations do not require a value. Since
JSON Patch
allows any type for
value
, the
type
property is not specified.
from
string
The
JSON Pointer
to the target document location from which to move the value. Required for the
move
operation.
Copy
{
"op"
:
"add"
,
"path"
:
"string"
,
"value"
:
null
,
"from"
:
"string"
}
payables_summary_item
A single summary item representing aggregated payables data for a specific currency-status combination.
count
required
integer
[ 0 .. 2147483647 ]
Total number of invoices matching this currency-status combination.
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
Three-letter ISO currency code for this summary item.
status
required
string
(
invoice_statuses_for_aggregation
)
[ 1 .. 100 ] characters
^[A-Z0-9_]+$
Invoice status for this summary item.
Enum Value
Description
OUTSTANDING
Invoices that are sent but not yet paid or only partially paid.
PAID
Invoices that have been fully paid.
total_amount
required
object
(
Money
)
Total monetary amount for invoices in this currency-status combination.
change_percentage
string
<
ppaas_common_percentage_v2
>
(
percentage
)
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
Percentage change in total amount compared to the previous period for this currency-status combination. Null if no previous period data is available.
Copy
Expand all
Collapse all
{
"count"
:
2147483647
,
"currency"
:
"str"
,
"status"
:
"OUTSTANDING"
,
"total_amount"
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
"change_percentage"
:
"string"
}
payables_summary_period
Time period for the summary report.
string
(
payables_summary_period
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Time period for the summary report.
Enum Value
Description
LAST_30_DAYS
Summary for the last 30 days.
THIS_WEEK
Summary for the current week.
THIS_MONTH
Summary for the current month.
THIS_QUARTER
Summary for the current quarter.
THIS_YEAR
Summary for the current year.
CUSTOM
Custom date range specified by from and to parameters.
Copy
"LAST_30_DAYS"
payment_detail
The payment details of the invoice. Includes payment type, method, date, discount, and transaction type.
payment_id
string
[ 0 .. 22 ] characters
^[\S\s]*$
The ID for a PayPal payment transaction. Required for the
PAYPAL
payment type.
note
string
[ 0 .. 2000 ] characters
^[\S\s]*$
A note associated with an external cash or check payment.
type
string
(
payment_type
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment type in an invoicing flow which can be PayPal or an external cash or check payment.
Enum Value
Description
PAYPAL
The payment type is PayPal.
EXTERNAL
The payment type is an external cash or a check payment.
payment_date
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
payment_date_time
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
method
required
string
(
payment_method
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment mode or method through which the invoicer can accept the payment.
Enum Value
Description
BANK_TRANSFER
Payments can be received through bank transfers.
CASH
Payments can be received as cash.
CHECK
Payments can be received as check.
CREDIT_CARD
Payments can be received through credit card payments.
DEBIT_CARD
Payments can be received through debit card payments.
PAYPAL
Payments can be received through paypal payments.
WIRE_TRANSFER
Payments can be received through wire transfer.
OTHER
Payments can be received through other modes.
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
shipping_info
object
(
contact_information
)
The contact information of the user. Includes name and address.
Copy
Expand all
Collapse all
{
"payment_id"
:
"string"
,
"note"
:
"string"
,
"type"
:
"PAYPAL"
,
"payment_date"
:
"string"
,
"payment_date_time"
:
"string"
,
"method"
:
"BANK_TRANSFER"
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
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
payment_method
The payment mode or method through which the invoicer can accept the payments.
string
(
payment_method
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment mode or method through which the invoicer can accept the payments.
Enum Value
Description
BANK_TRANSFER
Payments can be received through bank transfers.
CASH
Payments can be received as cash.
CHECK
Payments can be received as check.
CREDIT_CARD
Payments can be received through credit card payments.
DEBIT_CARD
Payments can be received through debit card payments.
PAYPAL
Payments can be received through paypal payments.
WIRE_TRANSFER
Payments can be received through wire transfer.
OTHER
Payments can be received through other modes.
Copy
"BANK_TRANSFER"
payment_method_detail
The details about payment methods.
payment_method_type
string
(
override_payment_method_type
)
[ 1 .. 120 ] characters
^[A-Z0-9_]*$
The payment method types that can be configured in the payment method overrides object for invoice payments.
Note:
To use
PAY_BY_BANK
, you must first complete the onboarding process. Visit the
onboarding page
to get started. Once onboarding is complete, you can configure
PAY_BY_BANK
as a payment method.
Value
Description
PAY_BY_BANK
Enables the buyer to pay the invoice directly from their bank account. Available only for US-based merchants and invoices with USD currency.
enabled
boolean
Indicates whether the particular payment method is enabled or not.
display_order
integer
[ 1 .. 100 ]
The display order of the payment method.
rules
Array of
objects
(
rules
)
[ 1 .. 10 ] items
The list of payment method rules created by the merchant.
create_time
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
Indicates time of rule creation.
update_time
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
Indicates time of rule updation.
Copy
Expand all
Collapse all
{
"payment_method_type"
:
"PAY_BY_BANK"
,
"enabled"
:
true
,
"display_order"
:
1
,
"rules"
:
[
{
"rule_type"
:
"EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD"
,
"rule_value"
:
"string"
,
"active"
:
true
}
]
,
"create_time"
:
"stringstringstringst"
,
"update_time"
:
"stringstringstringst"
}
payment_reference
The reference to the payment detail.
payment_id
string
[ 1 .. 22 ] characters
^[0-9A-Za-z_-]+$
The ID for the invoice payment.
Copy
{
"payment_id"
:
"string"
}
payment_term
The payment term of the invoice. Payment can be due upon receipt, a specified date, or in a set number of days.
term_type
string
(
payment_term_type
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment term. Payment can be due upon receipt, a specified date, or in a set number of days.
Enum Value
Description
DUE_ON_RECEIPT
The payment for the invoice is due upon receipt of the invoice.
DUE_ON_DATE_SPECIFIED
The payment for the invoice is due on the date specified in the invoice.
NET_10
The payment for the invoice is due in 10 days.
NET_15
The payment for the invoice is due in 15 days.
NET_30
The payment for the invoice is due in 30 days.
NET_45
The payment for the invoice is due in 45 days.
NET_60
The payment for the invoice is due in 60 days.
NET_90
The payment for the invoice is due in 90 days.
NO_DUE_DATE
The invoice has no payment due date.
conditional_rules
object
(
payment_term_conditional_rules
)
The conditional rules associated with the payment term of the invoice. Includes early payment discount, late payment surcharge, and auto cancellation details.
Copy
Expand all
Collapse all
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
}
payment_term_conditional_rules
The conditional rules associated with the payment term of the invoice. Includes early payment discount, late payment surcharge, and auto cancellation details.
early_payment_discount
object
(
early_payment_discount
)
The early payment discount for the invoice. If the payer pays before the discount end date, the specified discount is applied.
late_payment_surcharge
object
(
late_payment_surcharge
)
The late payment surcharge for the invoice. If the payer pays after the surcharge effective date, the specified surcharge is applied.
auto_cancellation
object
(
auto_cancellation
)
The auto cancellation details for the invoice. If the payer does not pay by the specified date, the invoice is automatically cancelled.
Copy
Expand all
Collapse all
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
payment_term_type
The payment term. Payment can be due upon receipt, a specified date, or in a set number of days.
string
(
payment_term_type
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment term. Payment can be due upon receipt, a specified date, or in a set number of days.
Enum Value
Description
DUE_ON_RECEIPT
The payment for the invoice is due upon receipt of the invoice.
DUE_ON_DATE_SPECIFIED
The payment for the invoice is due on the date specified in the invoice.
NET_10
The payment for the invoice is due in 10 days.
NET_15
The payment for the invoice is due in 15 days.
NET_30
The payment for the invoice is due in 30 days.
NET_45
The payment for the invoice is due in 45 days.
NET_60
The payment for the invoice is due in 60 days.
NET_90
The payment for the invoice is due in 90 days.
NO_DUE_DATE
The invoice has no payment due date.
Copy
"DUE_ON_RECEIPT"
payment_type
The payment type. Can be PayPal or an external payment. Includes cash or a check.
string
(
payment_type
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment type. Can be PayPal or an external payment. Includes cash or a check.
Enum Value
Description
PAYPAL
The payment type is PayPal.
EXTERNAL
The payment type is an external cash or a check payment.
Copy
"PAYPAL"
payments
An array of payments registered against the invoice.
transactions
Array of
objects
(
payment_detail
)
[ 0 .. 100 ] items
An array of payment details for the invoice. The payment details of the invoice like payment type, method, date, discount and transaction type.
paid_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"transactions"
:
[
{
"payment_id"
:
"string"
,
"note"
:
"string"
,
"type"
:
"PAYPAL"
,
"payment_date"
:
"string"
,
"payment_date_time"
:
"string"
,
"method"
:
"BANK_TRANSFER"
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
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"paid_amount"
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
PayPal Account Identifier
The account identifier for a PayPal account.
string
<
ppaas_payer_id_v3
>
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The account identifier for a PayPal account.
Copy
"stringstrings"
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
Phone
The phone number, in its canonical international
E.164 numbering plan format
.
national_number
required
string
[ 1 .. 14 ] characters
^[0-9]{1,14}?$
The national number, in its canonical international
E.164 numbering plan format
. The combined length of the country calling code (CC) and the national number must not be greater than 15 digits. The national number consists of a national destination code (NDC) and subscriber number (SN).
Copy
{
"national_number"
:
"string"
}
Phone Type
The phone type.
string
(
Phone Type
)
The phone type.
Enum
:
"FAX"
"HOME"
"MOBILE"
"OTHER"
"PAGER"
Copy
"FAX"
Phone Type
The phone type.
string
(
Phone Type
)
The phone type.
Enum Value
Description
FAX
Fax number.
HOME
Home phone number.
MOBILE
Mobile phone number.
OTHER
Other phone number.
PAGER
Pager number.
Copy
"FAX"
phone_detail
The phone details. Includes the phone number and type.
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
phone_type
required
string
(
Phone Type
)
The phone type.
Enum
:
"FAX"
"HOME"
"MOBILE"
"OTHER"
"PAGER"
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
,
"phone_type"
:
"FAX"
}
plan
The scheduling and recurrence configuration that defines when and how often invoices are automatically generated and sent to customers in a recurring series.
total_cycles
integer
[ 0 .. 99 ]
The total number of billing cycles (invoices) that will be generated in this recurring series. Once all cycles are completed, the series automatically expires. Note: if not set, then the series will be indefinite.
completed_cycles
integer
[ 0 .. 2147483647 ]
The number of billing cycles (invoices) that have already been generated and sent in this recurring series. This counter increments with each invoice sent and helps track progress toward the total cycles.
frequency
required
object
(
plan_frequency
)
The billing frequency that determines the time interval between successive invoice generations. Defines how often invoices are sent to the customer (e.g., weekly, monthly, yearly).
start_series_date
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
The date when the recurring series begins and the first invoice is generated. Must be specified in yyyy-MM-DD format and cannot be a past date. The start date must be either today or a future date. Note: If it is not explicitly passed then the system will assume current date as start series date.
next_occurrence_date
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
The calculated date when the next invoice in the series will be automatically generated and sent. This date is determined based on the frequency and the last invoice sent date.
Copy
Expand all
Collapse all
{
"total_cycles"
:
99
,
"completed_cycles"
:
2147483647
,
"frequency"
:
{
"interval_unit"
:
"DAY"
,
"interval_count"
:
1
}
,
"start_series_date"
:
"stringstri"
,
"next_occurrence_date"
:
"stringstri"
}
plan_frequency
The frequency of the recurring invoice series cycle.
interval_unit
required
string
[ 1 .. 24 ] characters
^[A-Z0-9_]+$
The time unit for the recurring invoice cycle interval. Used together with interval_count to determine the frequency of invoice generation.
Enum Value
Description
DAY
A daily cycle.
WEEK
A weekly cycle.
MONTH
A monthly cycle.
YEAR
A yearly cycle.
interval_count
required
integer
[ 1 .. 52 ]
Default:
1
The number of intervals between each recurring invoice cycle. For example, an interval_count of 2 with interval_unit of MONTH means the invoice recurs every 2 months.
Copy
{
"interval_unit"
:
"DAY"
,
"interval_count"
:
1
}
Portable Postal Address (Medium-Grained)
The portable international postal address. Maps to
AddressValidationMetadata
and HTML 5.1
Autofilling form controls: the autocomplete attribute
.
address_line_1
string
<= 300 characters
The first line of the address. For example, number or street. For example,
173 Drury Lane
. Required for data entry and compliance and risk checks. Must contain the full address.
address_line_2
string
<= 300 characters
The second line of the address. For example, suite or apartment number.
address_line_3
string
<= 100 characters
The third line of the address, if needed. For example, a street complement for Brazil, direction text, such as
next to Walmart
, or a landmark in an Indian address.
admin_area_4
string
<= 100 characters
The neighborhood, ward, or district. Smaller than
admin_area_level_3
or
sub_locality
. Value is:
The postal sorting code for Guernsey and many French territories, such as French Guiana.
The fine-grained administrative levels in China.
admin_area_3
string
<= 100 characters
A sub-locality, suburb, neighborhood, or district. Smaller than
admin_area_level_2
. Value is:
Brazil. Suburb, bairro, or neighborhood.
India. Sub-locality or district. Street name information is not always available but a sub-locality or district can be a very small area.
admin_area_2
string
<= 120 characters
A city, town, or village. Smaller than
admin_area_level_1
.
admin_area_1
string
<= 300 characters
The highest level sub-division in a country, which is usually a province, state, or ISO-3166-2 subdivision. Format for postal delivery. For example,
CA
and not
California
. Value, by country, is:
UK. A county.
US. A state.
Canada. A province.
Japan. A prefecture.
Switzerland. A kanton.
postal_code
string
<= 60 characters
The postal code, which is the zip code or equivalent. Typically required for countries with a postal code or an equivalent. See
postal code
.
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
address_details
object
(
Address Details
)
The non-portable additional address details that are sometimes needed for compliance, risk, or other scenarios where fine-grain address information might be needed. Not portable with common third party and open source. Redundant with core fields.
For example,
address_portable.address_line_1
is usually a combination of
address_details.street_number
,
street_name
, and
street_type
.
Copy
Expand all
Collapse all
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
qr_config
The configuration for a QR code.
width
integer
[ 150 .. 500 ]
Default:
500
The width, in pixels, of the QR code image. Value is from
150
to
500
.
height
integer
[ 150 .. 500 ]
Default:
500
The height, in pixels, of the QR code image. Value is from
150
to
500
.
action
string
[ 0 .. 7 ] characters
(?i)^(pay|details)$
Default:
"pay"
The type of URL for which to generate a QR code. Valid values are
pay
and
details
.
Copy
{
"width"
:
500
,
"height"
:
500
,
"action"
:
"pay"
}
reaction
This indicates the Customer's reaction, which can be a like or dislike.
string
(
reaction
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
This indicates the Customer's reaction, which can be a like or dislike.
Enum Value
Description
LIKE
Customer likes the seller/goods/service.
DISLIKE
Customer dislikes the seller/goods/service.
Copy
"LIKE"
recipient_info
The billing and shipping information. Includes name, email, address, phone, and language.
billing_info
object
(
billing_info
)
The billing information of the invoice recipient. Includes name, address, email, phone, and language.
shipping_info
object
(
contact_information
)
The contact information of the user. Includes name and address.
Copy
Expand all
Collapse all
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
recurring_info
Comprehensive information about a recurring invoice series, including invoice details, participant information, line items, and amount calculations.
primary_recipients
required
Array of
objects
(
recipient_info
)
= 1 items
The primary recipient of the recurring invoices. Contains billing and shipping information including the recipient's name, email address, physical address, phone number, and preferred language.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 1 .. 100 ] items
Additional email addresses to receive carbon copy (CC) notifications when invoices in this series are sent.
items
Array of
objects
(
item
)
[ 1 .. 100 ] items
The line items that will appear on each invoice in the recurring series. Each item includes product or service details, quantity, unit price, and any applicable discounts or taxes.
detail
required
object
(
recurring_series_detail
)
The recurring series configuration details, including payment terms and scheduling information.
invoicer
object
(
invoicer_info
)
The merchant or business information for the party issuing the recurring invoices. Includes business name, contact details (email, address, phone, fax), tax identification number, additional notes, and logo URL.
configuration
object
(
configuration
)
Configuration settings for invoices in this series. Defines whether partial payments are allowed, tip options, and whether tax is calculated before or after applying discounts.
amount
object
(
amount_summary_detail
)
The calculated amount breakdown for each invoice in the series, including subtotal of all items, total discounts applied, tax amounts, and shipping costs. Note: Only invoice-level discount, shipping, and custom amounts are accepted. The rest of the fields are not mandatory and are ignored if set. They are automatically computed irrespective of the values set in the request.
Copy
Expand all
Collapse all
{
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
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
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"template_id"
:
"PayPal system template"
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
,
"custom"
:
{
"label"
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
}
}
}
}
recurring_metadata
Comprehensive audit and tracking metadata that captures key lifecycle events and actions performed on the recurring invoice series, including creation, updates and cancellation.
created_by
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The email address of the account that created the resource.
last_updated_by
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The email address of the account that last edited the resource.
create_time
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
last_update_time
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
canceled_time
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
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"canceled_time"
:
"string"
}
recurring_series
A recurring invoice series that automatically generates and sends invoices to customers on a scheduled basis. Contains all configuration, status, and metadata for the series.
id
string
= 20 characters
^(RI-)[A-Z0-9]+$
The unique identifier for the recurring invoice series. This ID is used to reference and manage the series in all API operations.
status
string
(
recurring_status
)
[ 1 .. 155 ] characters
^[A-Z0-9_]+$
The lifecycle status of a recurring invoice series. Determines the operational state and whether invoices are actively being generated.
Enum Value
Description
DRAFT
The recurring series is in draft state. No invoices are generated or sent until the series is activated. The series configuration can be edited while in draft status.
ACTIVE
The recurring series is active and operational. Invoices are automatically generated and sent to recipients according to the configured schedule and payment plan.
CANCELLED
The recurring series has been canceled and is no longer active. No additional invoices will be generated or sent. This action is typically irreversible.
EXPIRED
The recurring series has reached its scheduled end date or maximum number of invoices and is now expired. No additional invoices will be generated or sent.
links
Array of
objects
(
Link Description
)
[ 1 .. 5 ] items
An array of request-related
HATEOAS links
.
plan_detail
required
object
(
plan
)
The schedule and frequency configuration that controls when invoices are automatically generated and sent to customers.
recurring_info
required
object
(
recurring_info
)
The complete invoice template information used for generating each invoice in the series, including line items, recipients, and amount calculations.
metadata
object
(
recurring_metadata
)
Audit and tracking information for the recurring series, including creation timestamp, last update timestamp and cancellation information if applicable.
Copy
Expand all
Collapse all
{
"id"
:
"stringstringstringst"
,
"status"
:
"DRAFT"
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
"plan_detail"
:
{
"total_cycles"
:
99
,
"completed_cycles"
:
2147483647
,
"frequency"
:
{
"interval_unit"
:
"DAY"
,
"interval_count"
:
1
}
,
"start_series_date"
:
"stringstri"
,
"next_occurrence_date"
:
"stringstri"
}
,
"recurring_info"
:
{
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
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
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"template_id"
:
"PayPal system template"
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
,
"custom"
:
{
"label"
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
}
}
}
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"canceled_time"
:
"string"
}
}
recurring_series_detail
The detailed information for a recurring invoice series, including payment terms and other configuration settings.
reference
string
[ 1 .. 120 ] characters
^[\S\s]*$
The reference data. Includes a Purchase Order (PO) number.
note
string
[ 1 .. 4000 ] characters
^[\S\s]*$
A note to the invoice recipient. Also appears on the invoice notification email.
terms_and_conditions
string
[ 1 .. 4000 ] characters
^[\S\s]*$
The general terms of the invoice. Can include return or cancellation policy and other terms and conditions.
memo
string
[ 1 .. 500 ] characters
^[\S\s]*$
A private bookkeeping memo for the user.
attachments
Array of
objects
(
File Reference
)
[ 0 .. 2147483647 ] items
An array of PayPal IDs for the files that are attached to an invoice.
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
payment_term
object
(
payment_term
)
The payment term of the invoice. Payment can be due upon receipt, a specified date, or in a set number of days.
Copy
Expand all
Collapse all
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
}
}
recurring_series_free_text_search_fields
Supported recurring invoices series free text search fields.
string
(
recurring_series_free_text_search_fields
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Supported recurring invoices series free text search fields.
Enum Value
Description
NOTES
Notes associated with the recurring invoices series.
MERCHANT_MEMO
Merchant memo related to the recurring invoices series.
PAYER_REFERENCE_INFO
Payer's reference information.
BILLING_EMAIL
Email address associated with billing.
BILLING_NAME
Name associated with billing.
BILLING_BUSINESS_NAME
Business name associated with billing.
BILLING_PHONE_NUMBER
Phone number associated with billing.
SHIPPING_NAME
Name associated with shipping.
SHIPPING_BUSINESS_NAME
Business name associated with shipping.
SHIPPING_PHONE_NUMBER
Phone number associated with shipping.
ITEM_NAME
Name of the recurring invoices series item.
ITEM_TAX_NAME
Tax name associated with the recurring invoices series item.
ITEM_DISCOUNT_NAME
Discount name associated with the recurring invoices series item.
INVOICE_DISCOUNT_NAME
Discount name associated with the recurring invoices series.
ALL
Search in all available search fields.
Copy
"NOTES"
recurring_status
The lifecycle status of a recurring invoice series. Determines the operational state and whether invoices are actively being generated.
string
(
recurring_status
)
[ 1 .. 155 ] characters
^[A-Z0-9_]+$
The lifecycle status of a recurring invoice series. Determines the operational state and whether invoices are actively being generated.
Enum Value
Description
DRAFT
The recurring series is in draft state. No invoices are generated or sent until the series is activated. The series configuration can be edited while in draft status.
ACTIVE
The recurring series is active and operational. Invoices are automatically generated and sent to recipients according to the configured schedule and payment plan.
CANCELLED
The recurring series has been canceled and is no longer active. No additional invoices will be generated or sent. This action is typically irreversible.
EXPIRED
The recurring series has reached its scheduled end date or maximum number of invoices and is now expired. No additional invoices will be generated or sent.
Copy
"DRAFT"
refund_detail
The refund details of the invoice. Includes the refund type, date, amount, and method.
refund_id
string
[ 0 .. 22 ] characters
^[\S\s]*$
The ID for a PayPal payment transaction. Required for the
PAYPAL
payment type.
type
string
(
payment_type
)
[ 0 .. 255 ] characters
^[\S\s]*$
The PayPal refund type. Indicates whether the refund was paid through PayPal or externally in the invoicing flow. The record refund method supports the
EXTERNAL
refund type. The
PAYPAL
refund type is supported for backward compatibility.
Enum Value
Description
PAYPAL
The payment type is PayPal.
EXTERNAL
The payment type is an external cash or a check payment.
refund_date
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
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
method
required
string
(
payment_method
)
[ 0 .. 255 ] characters
^[\S\s]*$
The payment mode or method through which the invoicer can accept the payments.
Enum Value
Description
BANK_TRANSFER
Payments can be received through bank transfers.
CASH
Payments can be received as cash.
CHECK
Payments can be received as check.
CREDIT_CARD
Payments can be received through credit card payments.
DEBIT_CARD
Payments can be received through debit card payments.
PAYPAL
Payments can be received through paypal payments.
WIRE_TRANSFER
Payments can be received through wire transfer.
OTHER
Payments can be received through other modes.
Copy
Expand all
Collapse all
{
"refund_id"
:
"string"
,
"type"
:
"PAYPAL"
,
"refund_date"
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
"method"
:
"BANK_TRANSFER"
}
refund_reference
The reference to the refund payment detail.
refund_id
string
[ 1 .. 22 ] characters
^[0-9A-Za-z_-]+$
The ID of the refund of an invoice payment.
Copy
{
"refund_id"
:
"string"
}
refunds
The invoicing refund details. Includes the refund type, date, amount, and method.
transactions
Array of
objects
(
refund_detail
)
[ 0 .. 100 ] items
An array of refund details for the invoice. Includes the refund type, date, amount, and method.
refund_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"transactions"
:
[
{
"refund_id"
:
"string"
,
"type"
:
"PAYPAL"
,
"refund_date"
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
"method"
:
"BANK_TRANSFER"
}
]
,
"refund_amount"
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
reminder_interval_unit
Defines the recurrence unit of time for sending automatic reminders.
string
(
reminder_interval_unit
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Defines the recurrence unit of time for sending automatic reminders.
Value
Description
DAY
Reminders are sent daily.
Copy
"DAY"
reminder_status
The status of the auto reminder configuration.
string
(
reminder_status
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The status of the auto reminder configuration.
Enum Value
Description
ACTIVE
Specifies the configuration is active.
INACTIVE
Specifies the configuration is inactive.
Copy
"ACTIVE"
reminder_type
The type of the auto reminder configuration.
string
(
reminder_type
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The type of the auto reminder configuration.
Enum Value
Description
BEFORE_DUE
Represents the auto reminder configuration for invoices prior to their due date.
AFTER_DUE
Represents the auto reminder configuration for invoices after their due date.
Copy
"BEFORE_DUE"
restrictive_email_address
The internationalized email address with more restrictive rules. This version restricts the local-part to a dot-atom as defined in
https://www.ietf.org/rfc/rfc5322.txt
. It does not allow for a quoted-string or an obs-local-part.
Allows alphanumeric and RFC-allowed special characters, !#$%&'*+-/=?^_`{|}~
Ensures that the local part does not start with dot (.), have consecutive dots, or end with dot. Ensures that the domain part does not have consecutive dots.
Ensures that the local part does not exceed 64 characters.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
string
(
restrictive_email_address
)
[ 3 .. 254 ] characters
^(?!\.)(?:[A-Za-z0-9!#$&'*\/=?^`{|}~_%+-]|\.(...
Show pattern
The internationalized email address with more restrictive rules. This version restricts the local-part to a dot-atom as defined in
https://www.ietf.org/rfc/rfc5322.txt
. It does not allow for a quoted-string or an obs-local-part.
Allows alphanumeric and RFC-allowed special characters, !#$%&'*+-/=?^_`{|}~
Ensures that the local part does not start with dot (.), have consecutive dots, or end with dot. Ensures that the domain part does not have consecutive dots.
Ensures that the local part does not exceed 64 characters.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
Copy
"string"
restrictive_email_address
The internationalized email address with more restrictive rules. This version restricts the local-part to a dot-atom as defined in
https://www.ietf.org/rfc/rfc5322.txt
. It does not allow for a quoted-string or an obs-local-part.
Allows alphanumeric and RFC-allowed special characters, !#$%&'*+-/=?^_`{|}~
Ensures that the local part does not start with dot (.), have consecutive dots, or end with dot. Ensures that the domain part does not have consecutive dots.
Ensures that the local part does not exceed 64 characters.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
string
(
restrictive_email_address
)
[ 3 .. 254 ] characters
^(?!\.)(?:[A-Za-z0-9!#$&'*\/=?^`{|}~_%+-]|\.(...
Show pattern
The internationalized email address with more restrictive rules. This version restricts the local-part to a dot-atom as defined in
https://www.ietf.org/rfc/rfc5322.txt
. It does not allow for a quoted-string or an obs-local-part.
Allows alphanumeric and RFC-allowed special characters, !#$%&'*+-/=?^_`{|}~
Ensures that the local part does not start with dot (.), have consecutive dots, or end with dot. Ensures that the domain part does not have consecutive dots.
Ensures that the local part does not exceed 64 characters.
Note:
Up to 64 characters are allowed before and 255 characters are allowed after the
@
sign. However, the generally accepted maximum length for an email address is 254 characters. The pattern verifies that an unquoted
@
sign exists.
Copy
"string"
rules
The conditional rule fields that define automated actions or adjustments applied by the merchant to an invoice, such as early payment discounts or auto cancellation.
conditional_rule_value
string
[ 1 .. 32 ] characters
^(([0-9]+)|(([0-9]+)?[.][0-9]+))$
Represents the value of the conditional rule it can be a percentage or absolute value. In case of absolute value, which might be:
An integer for currencies like
JPY
that are not typically fractional.
A decimal fraction for currencies like
TND
that are subdivided into thousandths.
For the required number of decimal places for a currency code, see
Currency Codes
.
discount_id
string
(
Stored Discount ID
)
[ 1 .. 22 ] characters
^DISC-[A-Z0-9]+$
The unique identifier for the stored discount that is created when an early payment discount rule is applied to an invoice.
discount_name
string
[ 1 .. 40 ] characters
^[a-zA-Z0-9\s]+$
Represents the name of the stored discount.
links
Array of
objects
(
Link Description
)
[ 1 .. 10 ] items
HATEOAS links.
conditional_rule_id
string
(
conditional_rule_time_based_uuid
)
= 40 characters
^CR-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]...
Show pattern
The unique identifier for the conditional rule.
conditional_rule_type
required
string
(
conditional_rule_type
)
[ 1 .. 30 ] characters
^[A-Z0-9_]*$
The type of conditional rule applied to the invoice.
Enum Value
Description
EARLY_PAYMENT_DISCOUNT
A discount applied if the invoice is paid before a specified date or within a certain period after the issue date.
LATE_PAYMENT_SURCHARGE
A surcharge applied if the invoice is paid after the due date or a specified period after the due date.
AUTO_CANCEL
A rule to automatically cancel the invoice if it is not paid by a specified date or a certain period after the due date.
conditional_rule_value_type
string
(
conditional_rule_value_type
)
[ 1 .. 20 ] characters
^[A-Z0-9_]*$
The value type that indicates how the conditional rule value is applied. Use
PERCENT
for a percentage-based discount or
AMOUNT
for an absolute currency value.
Enum Value
Description
PERCENT
Percentage of discount used in invoice item or in an invoice.
AMOUNT
An absolute value of discount used in invoice item or in an invoice based on the currency in invoice.
rule_expiry_terms
required
object
(
conditional_rules
)
The expiry terms that define when the conditional rule becomes inactive.
create_time
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
Indicates time of rule creation.
update_time
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
Indicates time of rule update.
Copy
Expand all
Collapse all
{
"conditional_rule_value"
:
"string"
,
"discount_id"
:
"string"
,
"discount_name"
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
}
]
,
"conditional_rule_id"
:
"string"
,
"conditional_rule_type"
:
"EARLY_PAYMENT_DISCOUNT"
,
"conditional_rule_value_type"
:
"PERCENT"
,
"rule_expiry_terms"
:
{
"rule_expiry_condition"
:
"THREE_DAYS_AFTER_ISSUE_DATE"
,
"condition_rule_end_date"
:
"stringstri"
}
,
"create_time"
:
"stringstringstringst"
,
"update_time"
:
"stringstringstringst"
}
rules
The details about payment method rules applied by the merchant.
rule_type
required
string
(
override_payment_method_rule_type
)
[ 1 .. 150 ] characters
^[A-Z0-9_]*$
The type of rule that can be applied to a payment method configured via payment method overrides object on an invoice. Each rule controls how a payment method behaves based on the invoice total.
System-defined threshold limits by payment method:
PAY_BY_BANK - $1000
Value
Description
EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD
When the invoice total exceeds the system-defined threshold, this rule restricts the invoice to accept only the specified payment method and disables all other payment methods. This rule is currently compatible only with the PAY_BY_BANK payment method.
rule_value
required
string
[ 1 .. 100 ] characters
^[a-zA-Z0-9\s,.]+$
Represents the value of the payment method rule it can be amount or country.
active
boolean
Default:
true
Indicates whether the rule is active or inactive. Default is true.
Copy
{
"rule_type"
:
"EXCLUSIVE_ABOVE_AMOUNT_THRESHOLD"
,
"rule_value"
:
"string"
,
"active"
:
true
}
Search criteria - to search recurring invoices series.
Search criteria - to search recurring invoices series.
search_text
string
[ 3 .. 800 ] characters
^(?!\s*$).+
Describes the search text, which will be used to check if this particular search_text present in any of the recurring invoice series fields, specified by search_fields.
search_fields
Array of
strings
(
recurring_series_free_text_search_fields
)
[ 1 .. 5 ] items
unique
Describes the set of fields on which the search will be performed.
Note:
If
search_fields
is provided with a single value 'ALL', the search will be performed across all the available fields in [search fields] (/recurring_series_free_text_search_fields.json).
Items
Enum Value
Description
NOTES
Notes associated with the recurring invoices series.
MERCHANT_MEMO
Merchant memo related to the recurring invoices series.
PAYER_REFERENCE_INFO
Payer's reference information.
BILLING_EMAIL
Email address associated with billing.
BILLING_NAME
Name associated with billing.
BILLING_BUSINESS_NAME
Business name associated with billing.
BILLING_PHONE_NUMBER
Phone number associated with billing.
SHIPPING_NAME
Name associated with shipping.
SHIPPING_BUSINESS_NAME
Business name associated with shipping.
SHIPPING_PHONE_NUMBER
Phone number associated with shipping.
ITEM_NAME
Name of the recurring invoices series item.
ITEM_TAX_NAME
Tax name associated with the recurring invoices series item.
ITEM_DISCOUNT_NAME
Discount name associated with the recurring invoices series item.
INVOICE_DISCOUNT_NAME
Discount name associated with the recurring invoices series.
ALL
Search in all available search fields.
search_filters
object
(
Search filters properties.
)
Search filters - to retrieve recurring invoices series.
Note:
This API currently supports only one criterion for range queries, so specify only one of the following criteria: creation_date_range or next_occurrence_date_range.
Copy
Expand all
Collapse all
{
"search_text"
:
"string"
,
"search_fields"
:
[
"NOTES"
]
,
"search_filters"
:
{
"status"
:
[
"DRAFT"
]
,
"archived"
:
true
,
"creation_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"next_occurrence_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"total_amount_range"
:
{
"lower_amount"
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
"upper_amount"
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
"currency_code"
:
"string"
}
}
Search filters properties.
Search filters - to retrieve invoices.
Note:
This API currently supports only one criterion for range queries, so specify only one of the following criteria: invoice_date_range, due_date_range, or payment_date_range.
currency_code
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
status
Array of
strings
(
invoice_status
)
[ 1 .. 5 ] items
unique
An array of invoice status.
Items
Enum Value
Description
DRAFT
The invoice is in draft state. It is not yet sent to the payer.
SENT
The invoice has been sent to the payer. The payment is awaited from the payer.
SCHEDULED
The invoice is scheduled on a future date. It is not yet sent to the payer.
PAID
The payer has paid for the invoice.
MARKED_AS_PAID
The invoice is marked as paid by the invoicer.
CANCELLED
The invoice has been cancelled by the invoicer.
REFUNDED
The invoice has been refunded by the invoicer.
PARTIALLY_PAID
The payer has partially paid for the invoice.
PARTIALLY_REFUNDED
The invoice has been partially refunded by the invoicer.
MARKED_AS_REFUNDED
The invoice is marked as refunded by the invoicer.
UNPAID
The invoicer is yet to receive the payment from the payer for the invoice.
PAYMENT_PENDING
The invoicer is yet to receive the payment for the invoice. It is under pending review.
AUTO_CANCELLED
The invoice was automatically cancelled because the payment was not received within the specified timeframe.
PAID_EXTERNAL
The invoice has been paid through an external system or method outside of the standard PayPal payment flow. This status is set manually, indicating payment was received through other means.
REFUNDED_EXTERNAL
The invoice has been refunded through an external system or method. This status indicates a refund was issued outside of the standard PayPal payment flow.
SHARED
The invoice has been shared with the payer, typically via a link or other method. This status is used to track when an invoice has been distributed but not necessarily sent via PayPal.
archived
boolean
Indicates whether to list merchant-archived invoices in the response. If 'true', the response lists only merchant-archived invoices. If 'false', the response lists only unarchived invoices. If 'null', the response lists all invoices.
creation_date_range
object
(
Date and Time Range
)
The date and time range. Filters invoices by creation date, invoice date, due date, and payment date.
total_amount_range
object
(
amount_range
)
The amount range.
invoice_date_range
object
(
date_range
)
The date range. Filters invoices by creation date, invoice date, due date, and payment date.
due_date_range
object
(
date_range
)
The date range. Filters invoices by creation date, invoice date, due date, and payment date.
payment_date_range
object
(
Date and Time Range
)
The date and time range. Filters invoices by creation date, invoice date, due date, and payment date.
Copy
Expand all
Collapse all
{
"currency_code"
:
"str"
,
"status"
:
[
"DRAFT"
]
,
"archived"
:
true
,
"creation_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"total_amount_range"
:
{
"lower_amount"
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
"upper_amount"
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
"invoice_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"due_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"payment_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
}
Search filters properties.
Search filters - to retrieve estimates.
currency_code
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
status
Array of
strings
(
estimate_status
)
[ 1 .. 5 ] items
unique
An array of estimate status.
Items
Enum Value
Description
DRAFT
Draft estimate.
SENT
Estimate sent.
CANCELLED
Estimate cancelled.
SHARED
Estimate shared.
ACCEPTED
Estimate accepted.
INVOICED
Estimate invoiced.
EXPIRED
Estimate expired.
archived
boolean
Indicates whether to list merchant-archived invoices in the response. If 'true', the response lists only merchant-archived invoices. If 'false', the response lists only unarchived invoices. If 'null', the response lists all invoices.
creation_date_range
object
(
Date and Time Range
)
The date and time range. Filters invoices by creation date, invoice date, due date, and payment date.
total_amount_range
object
(
amount_range
)
The amount range.
estimate_date_range
object
(
date_range
)
The date range. Filters invoices by creation date, invoice date, due date, and payment date.
Copy
Expand all
Collapse all
{
"currency_code"
:
"str"
,
"status"
:
[
"DRAFT"
]
,
"archived"
:
true
,
"creation_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"total_amount_range"
:
{
"lower_amount"
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
"upper_amount"
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
"estimate_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
}
Search filters properties.
Search filters - to retrieve recurring invoices series.
Note:
This API currently supports only one criterion for range queries, so specify only one of the following criteria: creation_date_range or next_occurrence_date_range.
status
Array of
strings
(
recurring_status
)
[ 1 .. 5 ] items
unique
An array of recurring invoice series status.
Items
Enum Value
Description
DRAFT
The recurring series is in draft state. No invoices are generated or sent until the series is activated. The series configuration can be edited while in draft status.
ACTIVE
The recurring series is active and operational. Invoices are automatically generated and sent to recipients according to the configured schedule and payment plan.
CANCELLED
The recurring series has been canceled and is no longer active. No additional invoices will be generated or sent. This action is typically irreversible.
EXPIRED
The recurring series has reached its scheduled end date or maximum number of invoices and is now expired. No additional invoices will be generated or sent.
archived
boolean
Indicates whether to list merchant-archived recurring invoice series in the response. If 'true', the response lists only merchant-archived invoices. If 'false', the response lists only unarchived invoices. If 'null', the response defaults to false.
creation_date_range
object
(
Date and Time Range
)
The date and time range. Filters invoices by creation date, invoice date, due date, and payment date.
next_occurrence_date_range
object
(
date_range
)
The date range. Filters invoices by creation date, invoice date, due date, and payment date.
total_amount_range
object
(
amount_range
)
The amount range.
currency_code
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
Expand all
Collapse all
{
"status"
:
[
"DRAFT"
]
,
"archived"
:
true
,
"creation_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"next_occurrence_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"total_amount_range"
:
{
"lower_amount"
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
"upper_amount"
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
"currency_code"
:
"string"
}
Search recurring invoices series - response object.
An array of merchant recurring invoices series. It includes
HATEOAS links
for navigation.
recurring_invoices
Array of
objects
(
recurring_series
)
[ 1 .. 100 ] items
The list of recurring invoices series that match the search criteria.
links
Array of
objects
(
Link Description
)
[ 1 .. 4 ] items
An array of request-related
HATEOAS links
.
Copy
Expand all
Collapse all
{
"recurring_invoices"
:
[
{
"id"
:
"stringstringstringst"
,
"status"
:
"DRAFT"
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
"plan_detail"
:
{
"total_cycles"
:
99
,
"completed_cycles"
:
2147483647
,
"frequency"
:
{
"interval_unit"
:
"DAY"
,
"interval_count"
:
1
}
,
"start_series_date"
:
"stringstri"
,
"next_occurrence_date"
:
"stringstri"
}
,
"recurring_info"
:
{
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
:
{
"prefix"
:
null
,
"given_name"
:
null
,
"surname"
:
null
,
"middle_name"
:
null
,
"suffix"
:
null
,
"alternate_full_name"
:
null
,
"full_name"
:
null
}
,
"address"
:
{
"address_line_1"
:
null
,
"address_line_2"
:
null
,
"address_line_3"
:
null
,
"admin_area_4"
:
null
,
"admin_area_3"
:
null
,
"admin_area_2"
:
null
,
"admin_area_1"
:
null
,
"postal_code"
:
null
,
"country_code"
:
null
,
"address_details"
:
{ }
}
,
"phones"
:
[
null
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
:
{
"prefix"
:
null
,
"given_name"
:
null
,
"surname"
:
null
,
"middle_name"
:
null
,
"suffix"
:
null
,
"alternate_full_name"
:
null
,
"full_name"
:
null
}
,
"address"
:
{
"address_line_1"
:
null
,
"address_line_2"
:
null
,
"address_line_3"
:
null
,
"admin_area_4"
:
null
,
"admin_area_3"
:
null
,
"admin_area_2"
:
null
,
"admin_area_1"
:
null
,
"postal_code"
:
null
,
"country_code"
:
null
,
"address_details"
:
{ }
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
null
,
"discount_end_date"
:
null
,
"percent"
:
null
,
"amount"
:
null
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
null
,
"surcharge_effective_date"
:
null
,
"percent"
:
null
,
"amount"
:
null
}
,
"auto_cancellation"
:
{
"is_applied"
:
null
,
"cancel_by_date"
:
null
}
}
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"template_id"
:
"PayPal system template"
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
:
null
,
"amount"
:
null
}
,
"item_discount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
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
"shipping"
:
{
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
,
"tax"
:
{
"name"
:
null
,
"tax_note"
:
null
,
"percent"
:
null
,
"amount"
:
null
}
}
,
"custom"
:
{
"label"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
}
}
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
,
"canceled_time"
:
"string"
}
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
search_data
The invoice search parameters.
recipient_email
string
[ 0 .. 254 ] characters
^[\S\s]*$
Filters the search by the email address.
recipient_first_name
string
[ 0 .. 140 ] characters
^[\S\s]*$
Filters the search by the recipient first name.
recipient_last_name
string
[ 0 .. 140 ] characters
^[\S\s]*$
Filters the search by the recipient last name.
recipient_business_name
string
[ 0 .. 300 ] characters
^[\S\s]*$
Filters the search by the recipient business name.
invoice_number
string
[ 0 .. 25 ] characters
^[\S\s]*$
Filters the search by the invoice number.
status
Array of
strings
(
invoice_status
)
[ 0 .. 5 ] items
An array of status values.
Items
Enum Value
Description
DRAFT
The invoice is in draft state. It is not yet sent to the payer.
SENT
The invoice has been sent to the payer. The payment is awaited from the payer.
SCHEDULED
The invoice is scheduled on a future date. It is not yet sent to the payer.
PAID
The payer has paid for the invoice.
MARKED_AS_PAID
The invoice is marked as paid by the invoicer.
CANCELLED
The invoice has been cancelled by the invoicer.
REFUNDED
The invoice has been refunded by the invoicer.
PARTIALLY_PAID
The payer has partially paid for the invoice.
PARTIALLY_REFUNDED
The invoice has been partially refunded by the invoicer.
MARKED_AS_REFUNDED
The invoice is marked as refunded by the invoicer.
UNPAID
The invoicer is yet to receive the payment from the payer for the invoice.
PAYMENT_PENDING
The invoicer is yet to receive the payment for the invoice. It is under pending review.
AUTO_CANCELLED
The invoice was automatically cancelled because the payment was not received within the specified timeframe.
PAID_EXTERNAL
The invoice has been paid through an external system or method outside of the standard PayPal payment flow. This status is set manually, indicating payment was received through other means.
REFUNDED_EXTERNAL
The invoice has been refunded through an external system or method. This status indicates a refund was issued outside of the standard PayPal payment flow.
SHARED
The invoice has been shared with the payer, typically via a link or other method. This status is used to track when an invoice has been distributed but not necessarily sent via PayPal.
reference
string
[ 0 .. 120 ] characters
^[\S\s]*$
The reference data. Includes a Purchase Order (PO) number.
memo
string
[ 0 .. 500 ] characters
^[\S\s]*$
A private bookkeeping memo for the user.
payment_date_range
object
(
Date and Time Range
)
The date and time range. Filters invoices by creation date, invoice date, due date, and payment date.
archived
boolean
Indicates whether to list merchant-archived invoices in the response. Value is:
true
. Response lists only merchant-archived invoices.
false
. Response lists only unarchived invoices.
null
. Response lists all invoices.
fields
Array of
strings
[ 0 .. 5 ] items
A CSV file of fields to return for the user, if available. Because the invoice object can be very large, field filtering is required. Valid collection fields are
items
,
payments
,
refunds
,
additional_recipients_info
, and
attachments
.
currency_code
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
total_amount_range
object
(
amount_range
)
The amount range.
invoice_date_range
object
(
date_range
)
The date range. Filters invoices by creation date, invoice date, due date, and payment date.
due_date_range
object
(
date_range
)
The date range. Filters invoices by creation date, invoice date, due date, and payment date.
creation_date_range
object
(
Date and Time Range
)
The date and time range. Filters invoices by creation date, invoice date, due date, and payment date.
Copy
Expand all
Collapse all
{
"recipient_email"
:
"string"
,
"recipient_first_name"
:
"string"
,
"recipient_last_name"
:
"string"
,
"recipient_business_name"
:
"string"
,
"invoice_number"
:
"string"
,
"status"
:
[
"DRAFT"
]
,
"reference"
:
"string"
,
"memo"
:
"string"
,
"payment_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"archived"
:
true
,
"fields"
:
[
"string"
]
,
"currency_code"
:
"string"
,
"total_amount_range"
:
{
"lower_amount"
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
"upper_amount"
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
"invoice_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"due_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
,
"creation_date_range"
:
{
"start"
:
"string"
,
"end"
:
"string"
}
}
shipping_cost
The shipping fee for all items. Includes tax on shipping.
amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
tax
object
(
tax
)
The tax information. Includes the tax name and tax rate of invoice items. The tax amount is added to the item total.
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
stored_discount
The details about the stored discount.
id
string
(
id
)
= 40 characters
^(BAT-)1[0-9A-Z]{3}-[0-9A-Z]{4}-[0-9A-Z]{8}-[...
Show pattern
A unique id used to reference the batch task.
name
required
string
[ 1 .. 40 ] characters
^[a-zA-Z0-9\s]+$
Represents the name of the stored discount.
value
required
string
[ 1 .. 32 ] characters
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
Represents the value of the stored discount it can be a percentage or absolute value. In case of absolute value, which might be:
An integer for currencies like
JPY
that are not typically fractional.
A decimal fraction for currencies like
TND
that are subdivided into thousandths.
For the required number of decimal places for a currency code, see
Currency Codes
.
type
required
string
(
type
)
[ 1 .. 20 ] characters
^[A-Z0-9_]*$
Type of the stored discount. Used to determine wheather its percentage or absolute currency value.
Enum Value
Description
PERCENT
Percentage of discount used in invoice item or in an invoice.
AMOUNT
An absolute value of discount used in invoice item or in an invoice based on the currency in invoice.
active
boolean
Indicates whether given stored discount is active or not.
created_time
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
Indicates time of stored discount creation.
updated_time
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
Indicates time of stored discount updation.
Copy
{
"id"
:
"stringstringstringstringstringstringstri"
,
"name"
:
"string"
,
"value"
:
"string"
,
"type"
:
"PERCENT"
,
"active"
:
true
,
"created_time"
:
"stringstringstringst"
,
"updated_time"
:
"stringstringstringst"
}
Subscription Info
Detailed information about a subscription.
id
string
= 39 characters
^SI-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]...
Show pattern
Identifier of the subscription.
status
string
(
Subscription status
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The subscription status.
Enum Value
Description
ACTIVE
Represents the subscription is created.
CANCELLED
Represents the subscription is cancelled.
PENDING_CANCELLATION
Represents the subscription is in pending cancelled state.
PENDING_ACTIVATION
Represents the subscription is in pending activation state.
TRIAL
Represents the subscription status is in TRIAL.
plan
object
(
An object representing a specific subscription plan info.
)
An object representing a specific subscription plan info.
next_billing_date_time
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
The subscription plan next billing date time.
Copy
Expand all
Collapse all
{
"id"
:
"stringstringstringstringstringstringstr"
,
"status"
:
"ACTIVE"
,
"plan"
:
{
"id"
:
"stringstringstringstringstringstringstr"
,
"name"
:
"string"
}
,
"next_billing_date_time"
:
"string"
}
Subscription status
The subscription status.
string
(
Subscription status
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The subscription status.
Enum Value
Description
ACTIVE
Represents the subscription is created.
CANCELLED
Represents the subscription is cancelled.
PENDING_CANCELLATION
Represents the subscription is in pending cancelled state.
PENDING_ACTIVATION
Represents the subscription is in pending activation state.
TRIAL
Represents the subscription status is in TRIAL.
Copy
"ACTIVE"
task_type
Task type of the batch task. Used to determine the batch operation/logic to be performed.
string
(
task_type
)
[ 1 .. 50 ] characters
^[A-Z0-9_]*$
Task type of the batch task. Used to determine the batch operation/logic to be performed.
Enum Value
Description
RISK_LIMIT_RECENT
Task for processing recent records for the account in Invoicing.
RISK_LIMIT_FULL
Task for processing all records in Invoicing.
Copy
"RISK_LIMIT_RECENT"
tax
The tax information. Includes the tax name and tax rate of invoice items. The tax amount is added to the item total.
name
required
string
[ 0 .. 100 ] characters
^[\s\S]*$
The name of the tax applied on the invoice items.
tax_note
string
[ 0 .. 40 ] characters
^[\s\S]*$
The tax note used to track the tax related data.
percent
required
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
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
template
The template with invoice details to load with all captured fields.
id
string
[ 0 .. 30 ] characters
^[\S\s]*$
The ID of the template.
name
string
[ 1 .. 500 ] characters
^[\S\s]*$
The template name.
Note:
The template name must be unique.
description
string
[ 1 .. 160 ] characters
^[\S\s]*$
The detailed description of the template.
default_template
boolean
Indicates whether this template is the default template. A invoicer can have one default template.
standard_template
boolean
Indicates whether this template is a invoicer-created custom template. The system generates non-custom templates.
links
Array of
objects
(
Link Description
)
[ 0 .. 2147483647 ] items
An array of request-related
HATEOAS links
.
template_info
object
(
template_info
)
The template details. Includes invoicer business information, invoice recipients, items, and configuration.
settings
object
(
template_settings
)
The template settings. Describes which fields to show or hide when you create an invoice.
unit_of_measure
string
(
unit_of_measure
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The unit of measure for the invoiced item.
Enum Value
Description
QUANTITY
The unit of measure is quantity. This invoice template is typically used for physical goods.
HOURS
The unit of measure is hours. This invoice template is typically used for services.
AMOUNT
The unit of measure is amount. This invoice template is typically used when only amount is required.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"default_template"
:
true
,
"standard_template"
:
true
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
"template_info"
:
{
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
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
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"tip_presets"
:
[
{
"percent"
:
"19.99"
}
]
,
"order_details"
:
"string"
,
"project_details"
:
"string"
,
"service_details"
:
"string"
,
"payment_terms"
:
"string"
,
"return_policy"
:
"string"
,
"cancellation_policy"
:
"string"
,
"service_agreement"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"has_conditional_rule"
:
false
,
"save_item_for_future"
:
true
,
"show_additional_item_fields"
:
false
,
"discount_mode_preference"
:
"ONE_TIME"
,
"theme"
:
{
"primary_color"
:
"string"
}
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
,
"custom"
:
{
"label"
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
}
}
}
,
"due_amount"
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
"settings"
:
{
"template_item_settings"
:
[
{
"field_name"
:
"ITEMS_QUANTITY"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_subtotal_settings"
:
[
{
"field_name"
:
"DISCOUNT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_details_settings"
:
[
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"ORDER_DETAILS"
}
]
,
"template_policy_and_agreement_settings"
:
[
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"CANCELLATION_POLICY"
}
]
,
"template_additional_settings"
:
[
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"ATTACHMENT"
}
]
}
,
"unit_of_measure"
:
"QUANTITY"
}
template_additional_setting
The template additional setting. Includes the field name and display preference.
display_preference
object
(
template_setting_display_preference
)
The template setting display preference.
field_name
string
(
template_additional_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Indicates which field or section of the invoice template this display preference applies to, as defined in
template_additional_settings_field.json
.
Enum Value
Description
ATTACHMENT
The file attachments added to the invoice template.
MEMO
The internal memo in the invoice template that is visible only to the invoicer.
REFERENCE
The reference number in the invoice template for tracking or correlation.
Copy
Expand all
Collapse all
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"ATTACHMENT"
}
template_additional_settings_field
The field names in the invoice template for additional sections, such as reference, attachments, or memo.
string
(
template_additional_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field names in the invoice template for additional sections, such as reference, attachments, or memo.
Enum Value
Description
ATTACHMENT
The file attachments added to the invoice template.
MEMO
The internal memo in the invoice template that is visible only to the invoicer.
REFERENCE
The reference number in the invoice template for tracking or correlation.
Copy
"ATTACHMENT"
template_configuration
The template configuration details. Includes tax information, tip, and partial payment.
tax_calculated_after_discount
boolean
Default:
true
Indicates whether the tax is calculated before or after a discount. If
false
, the tax is calculated before a discount. If
true
, the tax is calculated after a discount.
tax_inclusive
boolean
Default:
false
Indicates whether the unit price includes tax.
allow_tip
boolean
Default:
false
Indicates whether the invoice enables the customer to enter a tip amount during payment. If
true
, the invoice shows a tip amount field so that the customer can enter a tip amount. If
false
, the invoice does not show a tip amount field.
Note:
This feature is not available for users in
Hong Kong
,
Taiwan
,
India
, or
Japan
.
partial_payment
object
(
partial_payment
)
The partial payment details. Includes the minimum amount that the invoicer wants the payer to pay.
has_conditional_rule
boolean
Default:
false
Indicates whether conditional pricing rules are applied to the invoice. If
true
, pricing rules (such as discounts or surcharges based on specific conditions) are applied. If
false
, no conditional pricing rules are applied.
save_item_for_future
boolean
Default:
true
Indicates whether the item should be saved for future invoices.
show_additional_item_fields
boolean
Default:
false
Indicates whether items tray should be shown for invoices or not. If
true
, additional fields containing items tray will be shown. If
false
, the items tray will be hidden.
discount_mode_preference
string
(
discount_mode_preference
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Represents the user's preferred mode for creating discounts. Determines whether "One-time discount" or "Save for future invoices" is preselected when creating a new discount.
Enum Value
Description
ONE_TIME
Indicates that the user prefers creating one-time discounts by default.
SAVE_FOR_FUTURE
Indicates that the user prefers saving discounts for future invoices by default.
theme
object
(
Theme configuration
)
The theme configuration for the template. Defines the visual appearance of the invoice buyer experience and email when invoice is created using the template in UI.
Note:
Setting a theme on a template does not automatically carry over to invoices created using this template. To apply a theme to an invoice, set it directly on the invoice configuration.
Copy
Expand all
Collapse all
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"has_conditional_rule"
:
false
,
"save_item_for_future"
:
true
,
"show_additional_item_fields"
:
false
,
"discount_mode_preference"
:
"ONE_TIME"
,
"theme"
:
{
"primary_color"
:
"string"
}
}
template_detail
The template-related details. Includes notes, terms and conditions, memo, and attachments.
reference
string
[ 1 .. 120 ] characters
^[\S\s]*$
The reference data. Includes a Purchase Order (PO) number.
note
string
[ 1 .. 4000 ] characters
^[\S\s]*$
A note to the invoice recipient. Also appears on the invoice notification email.
terms_and_conditions
string
[ 1 .. 4000 ] characters
^[\S\s]*$
The general terms of the invoice. Can include return or cancellation policy and other terms and conditions.
memo
string
[ 1 .. 500 ] characters
^[\S\s]*$
A private bookkeeping memo for the user.
attachments
Array of
objects
(
File Reference
)
[ 0 .. 2147483647 ] items
An array of PayPal IDs for the files that are attached to an invoice.
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
tip_presets
Array of
objects
(
tip_preset
)
[ 1 .. 3 ] items
Specifies the predefined tip options configured by the invoicer. These preset values are shown to customers at checkout as suggested tipping amounts, in addition to the option to enter a custom tip.
order_details
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Order details information.
project_details
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Project details information.
service_details
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Service details information.
payment_terms
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Payment terms information.
return_policy
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Return policy information.
cancellation_policy
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Cancellation policy information.
service_agreement
string
[ 1 .. 2500 ] characters
^[\S\s]*$
Service agreement information.
payment_term
object
(
payment_term
)
The payment term of the invoice. Payment can be due upon receipt, a specified date, or in a set number of days.
metadata
object
(
template_metadata
)
The audit metadata. Captures all template actions on create and update.
Copy
Expand all
Collapse all
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"tip_presets"
:
[
{
"percent"
:
"19.99"
}
]
,
"order_details"
:
"string"
,
"project_details"
:
"string"
,
"service_details"
:
"string"
,
"payment_terms"
:
"string"
,
"return_policy"
:
"string"
,
"cancellation_policy"
:
"string"
,
"service_agreement"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
}
}
template_details_setting
The template invoice details setting. Includes the field name and display preference for order, project, and service details.
display_preference
object
(
template_setting_display_preference
)
The template setting display preference.
field_name
string
(
template_details_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field name for which to map corresponding display preferences.
Enum Value
Description
ORDER_DETAILS
Order details information in the invoice template.
PROJECT_DETAILS
Project details information in the invoice template.
SERVICE_DETAILS
Service details information in the invoice template.
Copy
Expand all
Collapse all
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"ORDER_DETAILS"
}
template_details_settings_field
The field names for the invoice details in the template.
string
(
template_details_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field names for the invoice details in the template.
Enum Value
Description
ORDER_DETAILS
Order details information in the invoice template.
PROJECT_DETAILS
Project details information in the invoice template.
SERVICE_DETAILS
Service details information in the invoice template.
Copy
"ORDER_DETAILS"
template_display_preference
The template display preference.
hidden
boolean
Default:
false
Indicates whether to show or hide this field.
Copy
{
"hidden"
:
false
}
template_info
The template details. Includes invoicer business information, invoice recipients, items, and configuration.
primary_recipients
Array of
objects
(
recipient_info
)
[ 0 .. 100 ] items
The billing and shipping information. Includes name, email, address, phone, and language.
additional_recipients
Array of
strings
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 0 .. 100 ] items
An array of one or more CC: emails to which notifications are sent. If you omit this parameter, a notification is sent to all CC: email addresses that are part of the invoice.
Note:
Valid values are email addresses in the
additional_recipients
value associated with the invoice.
items
Array of
objects
(
item
)
[ 0 .. 100 ] items
An array of invoice line-item information.
detail
object
(
template_detail
)
The template-related details. Includes notes, terms and conditions, memo, and attachments.
invoicer
object
(
invoicer_info
)
The invoicer business information that appears on the invoice.
configuration
object
(
template_configuration
)
The template configuration details. Includes tax information, tip, and partial payment.
amount
object
(
amount_summary_detail
)
The invoice amount summary of item total, discount, tax total, and shipping.
due_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Copy
Expand all
Collapse all
{
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
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
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"tip_presets"
:
[
{
"percent"
:
"19.99"
}
]
,
"order_details"
:
"string"
,
"project_details"
:
"string"
,
"service_details"
:
"string"
,
"payment_terms"
:
"string"
,
"return_policy"
:
"string"
,
"cancellation_policy"
:
"string"
,
"service_agreement"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
true
,
"discount_end_date"
:
"string"
,
"percent"
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
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
true
,
"surcharge_effective_date"
:
"string"
,
"percent"
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
}
,
"auto_cancellation"
:
{
"is_applied"
:
true
,
"cancel_by_date"
:
"string"
}
}
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"has_conditional_rule"
:
false
,
"save_item_for_future"
:
true
,
"show_additional_item_fields"
:
false
,
"discount_mode_preference"
:
"ONE_TIME"
,
"theme"
:
{
"primary_color"
:
"string"
}
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
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
}
,
"item_discount"
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
"shipping"
:
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
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
}
}
,
"custom"
:
{
"label"
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
}
}
}
,
"due_amount"
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
template_item_field
The field names for the invoice line items in the template.
string
(
template_item_field
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The field names for the invoice line items in the template.
Enum Value
Description
ITEMS_QUANTITY
The quantity of the item in the template that the invoicer provides to the payer. Value is from
-1000000
to
1000000
. Supports up to five decimal places.
ITEMS_DESCRIPTION
The description of the item in the invoice template.
ITEMS_DATE
The date in invoice template when the item or service was provided, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
z
.
ITEMS_DISCOUNT
The item discount in the invoice template. Discount as a percent or amount at invoice level. Invoice discount amount is subtracted from the item total.
ITEMS_TAX
The tax associated with the item in the invoice template. The tax amount is added to the item total. Value is from
0
to
100
. Supports up to five decimal places.
Copy
"ITEMS_QUANTITY"
template_item_setting
The template item setting. Sets a template as the default template or edit template.
field_name
string
(
template_item_field
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The field name in
template_data
for which to map corresponding display preferences.
Enum Value
Description
ITEMS_QUANTITY
The quantity of the item in the template that the invoicer provides to the payer. Value is from
-1000000
to
1000000
. Supports up to five decimal places.
ITEMS_DESCRIPTION
The description of the item in the invoice template.
ITEMS_DATE
The date in invoice template when the item or service was provided, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
z
.
ITEMS_DISCOUNT
The item discount in the invoice template. Discount as a percent or amount at invoice level. Invoice discount amount is subtracted from the item total.
ITEMS_TAX
The tax associated with the item in the invoice template. The tax amount is added to the item total. Value is from
0
to
100
. Supports up to five decimal places.
display_preference
object
(
template_display_preference
)
The display preference.
Copy
Expand all
Collapse all
{
"field_name"
:
"ITEMS_QUANTITY"
,
"display_preference"
:
{
"hidden"
:
false
}
}
template_metadata
The audit metadata. Captures all template actions on create and update.
created_by
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The email address of the account that created the resource.
last_updated_by
string
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The email address of the account that last edited the resource.
create_time
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
last_update_time
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
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
}
template_policy_and_agreement_setting
The template policy and agreement setting. Includes the field name and display preference for policy and agreement related fields.
display_preference
object
(
template_setting_display_preference
)
The template setting display preference.
field_name
string
(
template_policy_and_agreement_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field name for which to map corresponding display preferences.
Enum Value
Description
CANCELLATION_POLICY
Cancellation policy information in the invoice template.
PAYMENT_TERMS
Payment terms information in the invoice template.
RETURN_POLICY
Return policy information in the invoice template.
SERVICE_AGREEMENT
Service agreement information in the invoice template.
TERMS_AND_CONDITIONS
Terms and conditions information in the invoice template.
Copy
Expand all
Collapse all
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"CANCELLATION_POLICY"
}
template_policy_and_agreement_settings_field
The field names for the policy and agreement details in the template.
string
(
template_policy_and_agreement_settings_field
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The field names for the policy and agreement details in the template.
Enum Value
Description
CANCELLATION_POLICY
Cancellation policy information in the invoice template.
PAYMENT_TERMS
Payment terms information in the invoice template.
RETURN_POLICY
Return policy information in the invoice template.
SERVICE_AGREEMENT
Service agreement information in the invoice template.
TERMS_AND_CONDITIONS
Terms and conditions information in the invoice template.
Copy
"CANCELLATION_POLICY"
template_setting_display_preference
The template setting display preference.
hidden
boolean
Indicates whether to show or hide this field.
Copy
{
"hidden"
:
true
}
template_settings
The template settings. Sets a template as the default template or edit template.
template_item_settings
Array of
objects
(
template_item_setting
)
[ 0 .. 2147483647 ] items
The template item headers display preference.
template_subtotal_settings
Array of
objects
(
template_subtotal_setting
)
[ 0 .. 2147483647 ] items
The template subtotal headers display preference.
template_details_settings
Array of
objects
(
template_details_setting
)
[ 0 .. 2147483647 ] items
The template invoice details settings for order, project, and service details.
template_policy_and_agreement_settings
Array of
objects
(
template_policy_and_agreement_setting
)
[ 0 .. 2147483647 ] items
The template policy and agreement settings for terms, cancellation, and return policies.
template_additional_settings
Array of
objects
(
template_additional_setting
)
[ 1 .. 10 ] items
The template additional fields that define display preferences for references, attachments, and memos.
Copy
Expand all
Collapse all
{
"template_item_settings"
:
[
{
"field_name"
:
"ITEMS_QUANTITY"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_subtotal_settings"
:
[
{
"field_name"
:
"DISCOUNT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_details_settings"
:
[
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"ORDER_DETAILS"
}
]
,
"template_policy_and_agreement_settings"
:
[
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"CANCELLATION_POLICY"
}
]
,
"template_additional_settings"
:
[
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"ATTACHMENT"
}
]
}
template_subtotal_field
The field names in the template for discount, shipping, and custom amounts.
string
(
template_subtotal_field
)
[ 1 .. 2147483647 ] characters
^[\S\s]*$
The field names in the template for discount, shipping, and custom amounts.
Enum Value
Description
DISCOUNT
The discount as a percent or amount at invoice level. The invoice discount amount is subtracted from the item total.
SHIPPING
The shipping fee for all items in the invoice template. Also includes the tax on shipping.
CUSTOM
The custom amount to apply to an invoice in the template. If you include a label, you must include the custom amount.
SHIPPING_TAX
The tax on shipping fee for all items in the invoice template.
Copy
"DISCOUNT"
template_subtotal_setting
The template subtotal setting. Includes the field name and display preference.
field_name
string
(
template_subtotal_field
)
[ 1 .. 2147483647 ] characters
^[\S\s]*$
The field name in
template_data
for which to map corresponding display preferences.
Enum Value
Description
DISCOUNT
The discount as a percent or amount at invoice level. The invoice discount amount is subtracted from the item total.
SHIPPING
The shipping fee for all items in the invoice template. Also includes the tax on shipping.
CUSTOM
The custom amount to apply to an invoice in the template. If you include a label, you must include the custom amount.
SHIPPING_TAX
The tax on shipping fee for all items in the invoice template.
display_preference
object
(
template_display_preference
)
The display preference.
Copy
Expand all
Collapse all
{
"field_name"
:
"DISCOUNT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
templates
An array of merchant-created templates with associated details that include the emails, addresses, and phone numbers from the user's PayPal profile.
addresses
Array of
objects
(
Portable Postal Address (Medium-Grained)
)
[ 0 .. 2147483647 ] items
An array of addresses in the user's PayPal profile.
phones
Array of
objects
(
phone_detail
)
[ 0 .. 2147483647 ] items
An array of phone numbers in the user's PayPal profile.
templates
Array of
objects
(
template
)
[ 0 .. 2147483647 ] items
An array of details for each template. If
fields
is
none
, returns only the template name, ID, and default status.
links
Array of
objects
(
Link Description
)
[ 0 .. 2147483647 ] items
An array of request-related
HATEOAS links
.
emails
string
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 3 .. 254 ] characters
^(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za...
Show pattern
An array of emails in the user's PayPal profile.
Copy
Expand all
Collapse all
{
"addresses"
:
[
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
]
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"templates"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"default_template"
:
true
,
"standard_template"
:
true
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
"template_info"
:
{
"primary_recipients"
:
[
{
"billing_info"
:
{
"business_name"
:
"string"
,
"name"
:
{
"prefix"
:
null
,
"given_name"
:
null
,
"surname"
:
null
,
"middle_name"
:
null
,
"suffix"
:
null
,
"alternate_full_name"
:
null
,
"full_name"
:
null
}
,
"address"
:
{
"address_line_1"
:
null
,
"address_line_2"
:
null
,
"address_line_3"
:
null
,
"admin_area_4"
:
null
,
"admin_area_3"
:
null
,
"admin_area_2"
:
null
,
"admin_area_1"
:
null
,
"postal_code"
:
null
,
"country_code"
:
null
,
"address_details"
:
{ }
}
,
"phones"
:
[
null
]
,
"additional_info"
:
"string"
,
"email_address"
:
"string"
,
"language"
:
"string"
}
,
"shipping_info"
:
{
"business_name"
:
"string"
,
"name"
:
{
"prefix"
:
null
,
"given_name"
:
null
,
"surname"
:
null
,
"middle_name"
:
null
,
"suffix"
:
null
,
"alternate_full_name"
:
null
,
"full_name"
:
null
}
,
"address"
:
{
"address_line_1"
:
null
,
"address_line_2"
:
null
,
"address_line_3"
:
null
,
"admin_area_4"
:
null
,
"admin_area_3"
:
null
,
"admin_area_2"
:
null
,
"admin_area_1"
:
null
,
"postal_code"
:
null
,
"country_code"
:
null
,
"address_details"
:
{ }
}
}
}
]
,
"additional_recipients"
:
[
"string"
]
,
"items"
:
[
{
"id"
:
"string"
,
"name"
:
"string"
,
"description"
:
"string"
,
"quantity"
:
"string"
,
"unit_amount"
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
"tax"
:
{
"name"
:
"string"
,
"tax_note"
:
"string"
,
"percent"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
,
"item_date"
:
"string"
,
"discount"
:
{
"percent"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
,
"unit_of_measure"
:
"QUANTITY"
}
]
,
"detail"
:
{
"reference"
:
"string"
,
"note"
:
"string"
,
"terms_and_conditions"
:
"string"
,
"memo"
:
"string"
,
"attachments"
:
[
{
"id"
:
"string"
,
"reference_url"
:
"
http://example.com
"
,
"content_type"
:
"string"
,
"size"
:
"string"
,
"create_time"
:
"string"
}
]
,
"currency_code"
:
"string"
,
"tip_presets"
:
[
{
"percent"
:
"19.99"
}
]
,
"order_details"
:
"string"
,
"project_details"
:
"string"
,
"service_details"
:
"string"
,
"payment_terms"
:
"string"
,
"return_policy"
:
"string"
,
"cancellation_policy"
:
"string"
,
"service_agreement"
:
"string"
,
"payment_term"
:
{
"term_type"
:
"DUE_ON_RECEIPT"
,
"conditional_rules"
:
{
"early_payment_discount"
:
{
"is_applied"
:
null
,
"discount_end_date"
:
null
,
"percent"
:
null
,
"amount"
:
null
}
,
"late_payment_surcharge"
:
{
"is_applied"
:
null
,
"surcharge_effective_date"
:
null
,
"percent"
:
null
,
"amount"
:
null
}
,
"auto_cancellation"
:
{
"is_applied"
:
null
,
"cancel_by_date"
:
null
}
}
}
,
"metadata"
:
{
"created_by"
:
"string"
,
"last_updated_by"
:
"string"
,
"create_time"
:
"string"
,
"last_update_time"
:
"string"
}
}
,
"invoicer"
:
{
"business_name"
:
"string"
,
"name"
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
"address"
:
{
"address_line_1"
:
"string"
,
"address_line_2"
:
"string"
,
"address_line_3"
:
"string"
,
"admin_area_4"
:
"string"
,
"admin_area_3"
:
"string"
,
"admin_area_2"
:
"string"
,
"admin_area_1"
:
"string"
,
"postal_code"
:
"string"
,
"country_code"
:
"st"
,
"address_details"
:
{
"street_number"
:
"string"
,
"street_name"
:
"string"
,
"street_type"
:
"string"
,
"delivery_service"
:
"string"
,
"building_name"
:
"string"
,
"sub_building"
:
"string"
}
}
,
"phones"
:
[
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
,
"phone_type"
:
"FAX"
}
]
,
"website"
:
"
http://example.com
"
,
"tax_id"
:
"string"
,
"additional_notes"
:
"string"
,
"logo_url"
:
"
http://example.com
"
,
"email_address"
:
"string"
}
,
"configuration"
:
{
"tax_calculated_after_discount"
:
true
,
"tax_inclusive"
:
false
,
"allow_tip"
:
false
,
"partial_payment"
:
{
"allow_partial_payment"
:
false
,
"minimum_amount_due"
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
"has_conditional_rule"
:
false
,
"save_item_for_future"
:
true
,
"show_additional_item_fields"
:
false
,
"discount_mode_preference"
:
"ONE_TIME"
,
"theme"
:
{
"primary_color"
:
"string"
}
}
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
"discount"
:
{
"invoice_discount"
:
{
"percent"
:
null
,
"amount"
:
null
}
,
"item_discount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
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
"shipping"
:
{
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
,
"tax"
:
{
"name"
:
null
,
"tax_note"
:
null
,
"percent"
:
null
,
"amount"
:
null
}
}
,
"custom"
:
{
"label"
:
"string"
,
"amount"
:
{
"currency_code"
:
null
,
"value"
:
null
}
}
}
}
,
"due_amount"
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
"settings"
:
{
"template_item_settings"
:
[
{
"field_name"
:
"ITEMS_QUANTITY"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_subtotal_settings"
:
[
{
"field_name"
:
"DISCOUNT"
,
"display_preference"
:
{
"hidden"
:
false
}
}
]
,
"template_details_settings"
:
[
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"ORDER_DETAILS"
}
]
,
"template_policy_and_agreement_settings"
:
[
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"CANCELLATION_POLICY"
}
]
,
"template_additional_settings"
:
[
{
"display_preference"
:
{
"hidden"
:
true
}
,
"field_name"
:
"ATTACHMENT"
}
]
}
,
"unit_of_measure"
:
"QUANTITY"
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
"emails"
:
"string"
}
The status of the feature.
Indicates the status of the feature. If this feature is a paywall feature, it reflects the status of the associated subscription.
string
(
The status of the feature.
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Indicates the status of the feature. If this feature is a paywall feature, it reflects the status of the associated subscription.
Enum Value
Description
ACTIVE
Represents the feature is active.
CANCELLED
Represents the feature is cancelled.
PENDING_CANCELLATION
Represents the feature is in pending cancelled state.
PENDING_ACTIVATION
Represents the feature is in pending activation state.
SUSPENDED
Represents the feature is suspended.
REVOKED
Represents the feature has been revoked.
APPROVED
Represents the feature has been approved.
IN_REVIEW
Represents the feature is currently under review.
NEED_DATA
Represents the feature requires additional data.
DENY
Represents the feature has been denied.
INACTIVE
Represents the feature is inactive.
PENDING
Represents the feature is in a pending state.
Copy
"ACTIVE"
The type of the feature.
Indicates the type of the feature.
string
(
The type of the feature.
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
Indicates the type of the feature.
Enum Value
Description
PAID
Represents the feature is a paid feature.
FREE
Represents the feature is a free feature.
Copy
"PAID"
Theme
This object represents a merchant pre-defined layout and visual representation that defines the appearance of Invoicing buyer view page for branding a merchant.
layout
string
(
layout
)
[ 1 .. 155 ] characters
^[A-Z0-9_]+$
Represent the layout opted by merchant.
Enum Value
Description
CLASSIC
Default classic invoice layout.
BRANDED
Customised invoice layout.
primary_color
string
(
Color hex code
)
[ 4 .. 7 ] characters
^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$
Represents the primary color opted by merchant.
create_time
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
The date and time when the theme is created.
update_time
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
The date and time when the theme is updated.
Copy
{
"layout"
:
"CLASSIC"
,
"primary_color"
:
"string"
,
"create_time"
:
"stringstringstringst"
,
"update_time"
:
"stringstringstringst"
}
Theme configuration
The theme configuration that defines the visual appearance of the invoice buyer experience and email. Pass an empty object to use the default theme.
primary_color
string
[ 4 .. 7 ] characters
^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$
The primary color chosen by the merchant for branding the invoice buyer experience and email. Accepts a hex color code in #RGB or #RRGGBB format.
Copy
{
"primary_color"
:
"string"
}
tip_preset
Defines a tip option that can be presented to the customer as a percentage of the invoice total.
Note:
This preset represents a tip configuration where the percentage value is applied during checkout to calculate the tip amount.
percent
string
[ 1 .. 20 ] characters
^(([0-9]+)|(([0-9]+)?[.][0-9]+))$
The percentage, as a fixed-point, signed decimal number. For example, define a 19.99% interest rate as
19.99
.The tip percentage ranges from 0.00001 to 100.00000 inclusive and supports up to five decimal places.
Copy
{
"percent"
:
"19.99"
}
transmission_type
Indicates the channel of the notification delivery.
string
(
transmission_type
)
[ 1 .. 40 ] characters
^[A-Z0-9_]+$
Indicates the channel of the notification delivery.
Enum Value
Description
SMS
Transmission Type is SMS.
EMAIL
Transmission Type is EMAIL.
PUSH
Transmission Type is PUSH.
PAPER
Transmission Type is PAPER.
HTTP
Transmission Type is HTTP.
Copy
"SMS"
type
Type of the stored discount. Used to determine wheather its percentage or absolute currency value.
string
(
type
)
[ 1 .. 20 ] characters
^[A-Z0-9_]*$
Type of the stored discount. Used to determine wheather its percentage or absolute currency value.
Enum Value
Description
PERCENT
Percentage of discount used in invoice item or in an invoice.
AMOUNT
An absolute value of discount used in invoice item or in an invoice based on the currency in invoice.
Copy
"PERCENT"
unit_of_measure
The unit of measure for the invoiced item.
string
(
unit_of_measure
)
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The unit of measure for the invoiced item.
Enum Value
Description
QUANTITY
The unit of measure is quantity. This invoice template is typically used for physical goods.
HOURS
The unit of measure is hours. This invoice template is typically used for services.
AMOUNT
The unit of measure is amount. This invoice template is typically used when only amount is required.
Copy
"QUANTITY"
uuid
The universally unique identifier (UUID) in
Universally Unique IDentifier (UUID) URN Namespace format
.
string
<
ppaas_uuid_v3
>
(
uuid
)
= 36 characters
^[0-9a-zA-Z]{8}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}...
Show pattern
The universally unique identifier (UUID) in
Universally Unique IDentifier (UUID) URN Namespace format
.
Copy
"stringstringstringstringstringstring"
