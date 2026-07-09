# Disputes

Source: https://developer.paypal.com/docs/api/customer-disputes/v1/

Disputes
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
Disputes
post
Send message about dispute to other party
post
Settle dispute
post
Make offer to resolve dispute
post
Update dispute status
post
Accept claim
post
Provide evidence
post
Acknowledge returned item
get
Show dispute details
patch
Partially update dispute
get
List disputes
post
Appeal dispute
post
Deny offer to resolve dispute
post
Escalate dispute to claim
post
Provide supporting information for dispute
post
Accept offer to resolve dispute
Errors
Definitions
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
Disputes
(
1
)
?
This API is currently not supported by our SDK
Occasionally, something goes wrong with a customer's order. To dispute a charge, a customer can create a dispute with PayPal. PayPal merchants, partners, and external developers can use the PayPal Disputes API to manage customer disputes.
Note:
In the live environment, merchants cannot create disputes but can only respond to customer-created disputes. However, merchants can create disputes in the sandbox environment. When you create an app, enable Disputes in the App feature options section.
A customer can also ask his or her bank or credit card company to dispute and reverse a charge, which is known as a
chargeback
. For more information, see
Disputes, claims, chargebacks, and bank reversals
.
When a customer disputes a charge, you can use this API to provide evidence that the charge is legitimate. To provide evidence or appeal a dispute, you submit a proof of delivery or proof of refund document or notes, which can include logs.
Normally, an agent at PayPal creates a dispute, updates the dispute status, and settles disputes, but now you can run test cases in the sandbox that complete these operations.
Important:
The create, cancel, compute metrics, change reason, and validate eligibility methods are available as a limited-release solution at this time. For more information, reach out to your PayPal account manager.
For details, see
Disputes Overview
documentation.
Send message about dispute to other party
post
/v1/customer/disputes/{id}/send-message
Try it
Sends a message about a dispute, by ID, to the other party in the dispute. Merchants and customers can only send messages if the
dispute_life_cycle_stage
value is
INQUIRY
. For constraints and rules regarding documents that can be attached as part of the message, see
documents
. To send a message, use the
send-message
link in the
HATEOAS links
of the
show dispute details
response and specify the message in the JSON request body. In case the link is not present in the response you can't send a message on the dispute.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to send a message.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
message
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The message sent by the merchant to the other party.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
Request samples
Payload
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Copy
{
"message"
:
"string"
}
Response samples
200
application/json
Sample 1 - 200 - Send Message about Dispute to Other Party
Sample 1 - 200 - Send Message about Dispute to Other Party
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-27803
"
}
]
}
Settle dispute
post
/v1/customer/disputes/{id}/adjudicate
Try it
Important:
This method is for sandbox use only.
Settles a dispute in either the customer's or merchant's favor. Merchants can make this call in the sandbox to complete end-to-end dispute resolution testing, which mimics the dispute resolution that PayPal agents normally complete. To make this call, the dispute
status
must be
UNDER_REVIEW
and
adjudicate
link  should be available in the
HATEOAS links
of the
show dispute details
response.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute to settle.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
adjudication_outcome
required
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The outcome of the adjudication.
Enum Value
Description
BUYER_FAVOR
Resolves the case in the customer's favor. Outcome is set to
RESOLVED_BUYER_FAVOR
.
SELLER_FAVOR
Resolves the case in the merchant's favor. Outcome is set to
RESOLVED_SELLER_FAVOR
.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
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
Sample 1 - 200 - Settle Dispute
Sample 1 - 200 - Settle Dispute
Copy
{
"adjudication_outcome"
:
"BUYER_FAVOR"
}
Response samples
200
application/json
Sample 1 - 200 - Settle Dispute
Sample 1 - 200 - Settle Dispute
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-27803
"
}
]
}
Make offer to resolve dispute
post
/v1/customer/disputes/{id}/make-offer
Try it
Makes an offer to the other party to resolve a dispute, by ID. To make this call, the stage in the dispute lifecycle must be
INQUIRY
. If the customer accepts the offer, PayPal automatically makes a refund. Allowed offer_type values for the request is available in dispute details
allowed response options
object.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to make an offer.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
note
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The merchant's notes about the offer.
invoice_id
string
[ 1 .. 127 ] characters
^.*$
The merchant-provided ID of the invoice for the refund. This optional value maps the refund to an invoice ID in the merchant's system.
offer_amount
object
(
Money
)
The amount proposed to resolve the dispute.
return_shipping_address
object
(
Portable Postal Address (Medium-Grained)
)
The return address for the item. Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason, especially if the refund amount is less than the dispute amount.
return_shipping_address_info
object
(
Return shipping address information
)
Merchant provided information regarding return shipping address.
offer_type
required
string
(
offer_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The merchant-proposed offer type for the dispute.
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount. Buyer acceptance is needed for partial refund offers and dispute is auto closed for full refunds. Include the
offer_amount
but omit the
return_shipping_address
parameters from the make offer request.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount and requires the customer to return the item. Include the
return_shipping_address
parameter and the
offer_amount
parameter in the make offer request.
REFUND_WITH_REPLACEMENT
The merchant must do a refund and then send a replacement item to the customer. This offer type is valid in the inquiry phase when a merchant is willing to refund a specific amount and send the replacement item. Include the
offer_amount
parameter in the make offer request.
REPLACEMENT_WITHOUT_REFUND
The merchant must send a replacement item to the customer with no additional refunds. This offer type is valid in the inquiry phase when a merchant is willing to replace the item without any refund. Omit the
offer_amount
parameter from the make offer request.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
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
Sample 1 - 200 - Make Offer to Resolve Dispute
Sample 1 - 200 - Make Offer to Resolve Dispute
Copy
Expand all
Collapse all
{
"note"
:
"Offer refund with return. The return address should not be saved to profile."
,
"offer_amount"
:
{
"value"
:
"10.00"
,
"currency_code"
:
"USD"
}
,
"offer_type"
:
"REFUND_WITH_RETURN"
,
"return_shipping_address_info"
:
{
"save_to_profile"
:
false
,
"address"
:
{
"address_line_1"
:
"14,Kimberly st"
,
"address_line_2"
:
"Open Road North"
,
"country_code"
:
"US"
,
"admin_area_1"
:
"Gotham City"
,
"admin_area_2"
:
"Gotham"
,
"postal_code"
:
"124566"
}
}
}
Response samples
200
application/json
Sample 1 - 200 - Make Offer to Resolve Dispute
Sample 1 - 200 - Make Offer to Resolve Dispute
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-R-TWP-23605903
"
}
]
}
Update dispute status
post
/v1/customer/disputes/{id}/require-evidence
Try it
Important:
This method is for sandbox use only.
Updates the status of a dispute, by ID, from
UNDER_REVIEW
to either:
WAITING_FOR_BUYER_RESPONSE
WAITING_FOR_SELLER_RESPONSE
This status change enables either the customer or merchant to submit evidence for the dispute. To make this call, the dispute
status
must be
UNDER_REVIEW
and
require-evidence
link  should be available in the
HATEOAS links
of the
show dispute details
response. Specify an
action
value in the JSON request body to indicate whether the status change enables the customer or merchant to submit evidence:
If
action
is
The
status
updates to
BUYER_EVIDENCE
WAITING_FOR_BUYER_RESPONSE
SELLER_EVIDENCE
WAITING_FOR_SELLER_RESPONSE
.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute that requires evidence.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
required
action
required
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The action. Indicates whether the state change enables the customer or merchant to submit evidence.
Enum Value
Description
BUYER_EVIDENCE
Changes the status of the dispute to
WAITING_FOR_BUYER_RESPONSE
.
SELLER_EVIDENCE
Changes the status of the dispute to
WAITING_FOR_SELLER_RESPONSE
.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
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
Sample 1 - 200 - Update Dispute Status
Sample 1 - 200 - Update Dispute Status
Copy
{
"action"
:
"BUYER_EVIDENCE"
}
Response samples
200
application/json
Sample 1 - 200 - Update Dispute Status
Sample 1 - 200 - Update Dispute Status
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-27803
"
}
]
}
Accept claim
post
/v1/customer/disputes/{id}/accept-claim
Try it
Accepts liability for a claim, by ID. When you accept liability for a claim, the dispute closes in the customer’s favor and PayPal automatically refunds money to the customer from the merchant's account. Allowed accept_claim_type values for the request is available in dispute details
allowed response options
object.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to accept a claim.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
note
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The merchant's notes about the claim. PayPal can, but the customer cannot, view these notes.
accept_claim_reason
string
(
accept_claim_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The merchant's reason for acceptance of the customer's claim.
Enum Value
Description
DID_NOT_SHIP_ITEM
Merchant is accepting customer's claim as they could not ship the item back to the customer
TOO_TIME_CONSUMING
Merchant is accepting customer's claim as it is taking too long for merchant to fulfil the order
LOST_IN_MAIL
Merchant is accepting customer's claim as the item is lost in mail or transit
NOT_ABLE_TO_WIN
Merchant is accepting customer's claim as the merchant is not able to find sufficient evidence to win this dispute
COMPANY_POLICY
Merchant is accepting customer’s claims to follow their internal company policy
REASON_NOT_SET
This is the default value merchant can use if none of the above reasons apply
invoice_id
string
[ 1 .. 127 ] characters
^.*$
The merchant-provided ID of the invoice for the refund. This optional value is used to map the refund to an invoice ID in the merchant's system.
return_shipment_info
Array of
objects
(
response_shipment_info
)
[ 1 .. 100 ] items
An array of relevant shipment information for the items.
Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason using the shipment label provided by the merchant.
return_shipping_address
object
(
Portable Postal Address (Medium-Grained)
)
The return address for the item.
Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason, especially if the refund amount is less than the dispute amount.
return_shipping_address_info
object
(
Return shipping address information
)
Merchant provided information regarding return shipping address.
refund_amount
object
(
Money
)
To accept a customer's claim, the amount that the merchant agrees to refund the customer. The subsequent action depends on the amount:
If this amount is less than the customer-requested amount, the dispute updates to require customer acceptance.
If this amount is equal to or greater than the customer-requested amount, this amount is automatically refunded to the customer and the dispute closes.
accept_claim_type
string
(
Accept Claim Type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The refund type proposed by the merchant for the dispute.
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This type is applicable when a merchant is willing to refund the entire dispute amount without any further action from customer. Omit the
refund_amount
and
return_shipping_address
parameters from the
accept claim
call.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This type is applicable when a merchant is willing to refund the dispute amount and requires the customer to return the item. Include the
return_shipping_address
parameter in but omit the
refund_amount
parameter from the
accept claim
call.
PARTIAL_REFUND
The merchant proposes a partial refund for the dispute.This type is applicable when a merchant is willing to refund an amount lesser than dispute amount. Include the
refund_amount
parameter.
REFUND_WITH_RETURN_SHIPMENT_LABEL
The customer must return the item to the merchant and then merchant will refund the money. This type is applicable when a merchant is willing to refund the dispute amount and requires the customer to return the item using the shipment label provided by the merchant. Include the
return_shipment_info
and
return_shipping_address
parameter in but omit the
refund_amount
parameter from the
accept claim
call.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
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
Sample 1 - 200 - Accept Claim with Item Return and provide shipment label
Sample 1 - 200 - Accept Claim with Item Return and provide shipment label
Copy
Expand all
Collapse all
{
"note"
:
"full refund with item return."
,
"return_shipping_address"
:
{
"address_line_1"
:
"14,Kimberly st"
,
"address_line_2"
:
"Open Road North"
,
"country_code"
:
"US"
,
"admin_area_1"
:
"Gotham City"
,
"admin_area_2"
:
"Gotham"
,
"postal_code"
:
"124566"
}
,
"return_shipment_info"
:
[
{
"shipment_label"
:
{
"id"
:
"10-006-01-001-96571189-0702-49ce-a866-faad20e29731"
,
"name"
:
"file1.pdf"
}
,
"tracking_info"
:
{
"carrier_name"
:
"FEDEX"
,
"tracking_number"
:
"122533485"
}
}
]
}
Response samples
200
application/json
Sample 1 - 200 - Accept Claim with Item Return and provide shipment label
Sample 1 - 200 - Accept Claim with Item Return and provide shipment label
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-27803
"
}
]
}
Provide evidence
post
/v1/customer/disputes/{id}/provide-evidence
Try it
Provides evidence for a dispute, by ID. A merchant can provide evidence for disputes with the
WAITING_FOR_SELLER_RESPONSE
status while customers can provide evidence for disputes with the
WAITING_FOR_BUYER_RESPONSE
status. Evidence can be a proof of delivery or proof of refund document or notes, which can include logs. A proof of delivery document includes a tracking number while a proof of refund document includes a refund ID. For other evidence type, notes and documents can be given. Evidences requested from you can be found by checking the type of evidence for the corresponding source under the evidence section of the
show dispute details
response. The source will be
REQUESTED_FROM_SELLER
for evidences requested from the merchant while it will be
REQUESTED_FROM_BUYER
for evidences requested from the customer. For constraints and rules regarding documents, see
documents
.
To make this request, specify the evidence in the JSON request body and use the
provide-evidence
link in the
HATEOAS links
of the
show dispute details
response. In case the link is not present in the response, you can't provide evidence for the dispute. For information about dispute reasons, see
dispute reasons
.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to submit evidence.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
evidences
Array of
objects
(
evidence
)
[ 0 .. 100 ] items
An array of evidences for the dispute.
return_shipping_address
object
(
Portable Postal Address (Medium-Grained)
)
The return address for the item.
Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason..
return_shipping_address_info
object
(
Return shipping address information
)
Merchant provided information regarding return shipping address.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
Request samples
Payload
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
multipart/related
application/json
Copy
Expand all
Collapse all
{
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
Acknowledge returned item
post
/v1/customer/disputes/{id}/acknowledge-return-item
Try it
Acknowledges that the customer returned an item for a dispute, by ID. A merchant can make this request for disputes with the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
reason. Allowed acknowledgement_type values for the request is available in dispute details
allowed response options
object. For constraints and rules regarding documents, see
documents
.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to acknowledge the return of disputed item.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
note
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The merchant provided notes. PayPal can but the consumer cannot view these notes.
evidences
Array of
objects
(
acknowledge_return_item_evidence
)
[ 1 .. 100 ] items
An array of evidence documents.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
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
Sample 1 - 200 - Acknowledge Returned Item
Sample 1 - 200 - Acknowledge Returned Item
Copy
{
"note"
:
"I have received the item back."
,
"acknowledgement_type"
:
"ITEM_RECEIVED"
}
Response samples
200
application/json
Sample 1 - 200 - Acknowledge Returned Item
Sample 1 - 200 - Acknowledge Returned Item
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-000-000-651-454
"
}
]
}
Show dispute details
get
/v1/customer/disputes/{id}
Try it
Shows details for a dispute, by ID.
Note:
The fields that appear in the response depend on the access. For example, if the merchant requests shows dispute details, the customer's email ID does not appear.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to show details.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows dispute details.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-4012
\
-H
'Content-Type: application/json'
\
-H
'Authorization: Bearer A101.OLQiCxMmoVwigKQQDu3CYlamZ1KTKQmhrbAZK85RIy4IiWh9d_up_Nliuq_lfZdU.P3gvkY3PO28akjKYaDorm12QdfK'
Response samples
200
application/json
Sample 1 - 200 - Show Dispute Details with extensions
Sample 1 - 200 - Show Dispute Details with extensions
Copy
Expand all
Collapse all
{
"dispute_id"
:
"PP-D-4012"
,
"create_time"
:
"2019-04-11T04:18:00.000Z"
,
"update_time"
:
"2019-04-21T04:19:08.000Z"
,
"disputed_transactions"
:
[
{
"seller_transaction_id"
:
"3BC38643YC807283D"
,
"create_time"
:
"2019-04-11T04:16:58.000Z"
,
"transaction_status"
:
"REVERSED"
,
"gross_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"192.00"
}
,
"buyer"
:
{
"name"
:
"Lupe Justin"
}
,
"seller"
:
{
"email"
:
"
[email protected]
"
,
"merchant_id"
:
"5U29WL78XSAEL"
,
"name"
:
"Lesley Paul"
}
}
]
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED"
,
"status"
:
"RESOLVED"
,
"dispute_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"96.00"
}
,
"dispute_outcome"
:
{
"outcome_code"
:
"RESOLVED_BUYER_FAVOUR"
,
"amount_refunded"
:
{
"currency_code"
:
"USD"
,
"value"
:
"96.00"
}
}
,
"dispute_life_cycle_stage"
:
"CHARGEBACK"
,
"dispute_channel"
:
"INTERNAL"
,
"messages"
:
[
{
"posted_by"
:
"BUYER"
,
"time_posted"
:
"2019-04-11T04:18:04.000Z"
,
"content"
:
"SNAD case created through automation"
,
"documents"
:
[
{
"name"
:
"SNAD_Issue.pdf"
,
"url"
:
"
https://api-m.paypal.com/v2/content/documents/DIS-010-4c465d94-241c-4e1f-b384-9de78f7200bb/files/1/download
"
}
]
}
]
,
"extensions"
:
{
"merchandize_dispute_properties"
:
{
"issue_type"
:
"SERVICE"
,
"service_details"
:
{
"sub_reasons"
:
[
"INCOMPLETE"
]
,
"purchase_url"
:
"
https://ebay.in
"
}
}
}
,
"offer"
:
{
"buyer_requested_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"96.00"
}
,
"offer_type"
:
"REFUND"
,
"history"
:
[
{
"offer_time"
:
"2019-04-29T07:04:54.000Z"
,
"actor"
:
"SELLER"
,
"event_type"
:
"PROPOSED"
,
"offer_type"
:
"REFUND"
,
"offer_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"96.00"
}
,
"notes"
:
"Full refund offer."
,
"dispute_life_cycle_stage"
:
"CHARGEBACK"
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-4012
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
Partially update dispute
patch
/v1/customer/disputes/{id}
Try it
Partially updates a dispute, by ID. Seller can update the
communication_detail
value or The partner can add the
partner action
information.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to update the communication detail or add the partner action.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Array
([ 0 .. 32767 ] items)
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
Sample 1 - 204 - Partially Update Dispute by adding partner action - Success
Sample 1 - 204 - Partially Update Dispute by adding partner action - Success
Copy
Expand all
Collapse all
[
{
"op"
:
"add"
,
"path"
:
"/partner_actions/-"
,
"value"
:
{
"id"
:
"AMX-22345"
,
"name"
:
"DENY_DISPUTE"
,
"create_time"
:
"2018-01-12T10:41:35.000Z"
,
"reason"
:
"TRANSACTION_MATCHES_BUYER_SPENDING_PATTERN"
,
"status"
:
"PENDING"
}
}
]
Response samples
204
application/json
Sample 1 - 204 - Partially Update Dispute by adding partner action - Success
Sample 1 - 204 - Partially Update Dispute by adding partner action - Success
Copy
{ }
List disputes
get
/v1/customer/disputes
Try it
Lists disputes with a summary set of details, which shows the
dispute_id
,
reason
,
status
,
dispute_state
,
dispute_life_cycle_stage
,
dispute_channel
,
dispute_amount
,
create_time
and
update_time
fields.
To filter the disputes in the response, specify one or more optional query parameters. To limit the number of disputes in the response, specify the
page_size
query parameter.
To list multiple disputes, set these query parameters in the request:
page_size=2
start_time
instead of
disputed_transaction_id
If the response contains more than two disputes, it lists two disputes and includes a HATEOAS link to the next page of results.
Security
Oauth2
Request
query
Parameters
start_time
string
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
Default:
"Current date and time"
DEPRECATED. Please check the alternate field
create_time_after
. Filters the disputes in the response by a creation date and time. The start time must be within the last 180 days. Value is in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
You can specify either but not both the
start_time
and
disputed_transaction_id
query parameters.
disputed_transaction_id
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Filters the disputes in the response by a transaction, by ID.
You can specify either but not both the
start_time
and
disputed_transaction_id
query parameter.
page
integer
[ 1 .. 50 ]
Default:
1
The page number of the results, as a non-zero integer. Enables you to search by page number. Use in combination with the
page_size
.
page_size
integer
[ 1 .. 50 ]
Default:
10
Limits the number of disputes in the response to this value.
next_page_token
string
[ 1 .. 255 ] characters
^[A-Za-z0-9+\/=]+$
Default:
"The first page of data"
DEPRECATED. Please check the alternate field
page
. The token that describes the next page of results to fetch. The
list disputes
call returns this token in the HATEOAS links in the response.
dispute_state
string
[ 1 .. 2000 ] characters
^[0-9A-Z_]+$
Filters the disputes in the response by a state. Separate multiple values with a comma (
,
). When you specify more than one dispute_state, the response lists disputes that belong to any of the specified dispute_state.
create_time_before
string
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time when the dispute was created, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
create_time_after
string
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time when the dispute was created, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
update_time_before
string
<
ppaas_date_time_v3
>
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time when the dispute was last updated, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
. update_time_before must be within the last 180 days and the default is the current time.
update_time_after
string
<
ppaas_date_time_v3
>
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The date and time when the dispute was last updated, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
. update_time_after must be within the last 180 days and the default is the maximum time (180 days) supported.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that lists disputes with a full or summary set of details. Default is a summary set of details, which shows the
dispute_id
,
reason
,
status
,
dispute_amount
,
create_time
, and
update_time
fields for each dispute.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v1/customer/disputes?seller_protection_types
=
SELLER_PROTECTION_INELIGIBLE
\
-H
'Content-Type: application/json'
\
-H
'Authorization: Bearer A101.OLQiCxMmoVwigKQQDu3CYlamZ1KTKQmhrbAZK85RIy4IiWh9d_up_Nliuq_lfZdU.P3gvkY3PO28akjKYaDorm12QdfK'
Response samples
200
application/json
Sample 1 - 200 - Lists Disputes by ineligible seller protection types
Sample 1 - 200 - Lists Disputes by ineligible seller protection types
Copy
Expand all
Collapse all
{
"items"
:
[
{
"dispute_id"
:
"PP-D-208454"
,
"create_time"
:
"2023-07-22T01:34:47.000Z"
,
"update_time"
:
"2023-07-22T02:14:29.000Z"
,
"disputed_transactions"
:
[
{
"buyer_transaction_id"
:
"54M94084LL945391E"
,
"buyer"
:
{
"payer_id"
:
"APFXN3NMGTFEU"
}
,
"seller"
:
{
"merchant_id"
:
"6C6TADF69U7Q6"
}
,
"seller_protection_type"
:
"SELLER_PROTECTION_INELIGIBLE"
,
"seller_protection_eligible"
:
false
}
]
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"status"
:
"RESOLVED"
,
"dispute_state"
:
"RESOLVED"
,
"dispute_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"16.00"
}
,
"outcome"
:
"WON"
,
"dispute_life_cycle_stage"
:
"CHARGEBACK"
,
"dispute_channel"
:
"INTERNAL"
,
"dispute_flow"
:
"OTHER"
,
"links"
:
[
{
"href"
:
"
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-208454
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
"dispute_id"
:
"PP-D-208420"
,
"create_time"
:
"2023-07-21T14:24:12.000Z"
,
"update_time"
:
"2023-07-21T14:29:53.000Z"
,
"disputed_transactions"
:
[
{
"buyer_transaction_id"
:
"59055077FC437070A"
,
"buyer"
:
{
"payer_id"
:
"APFXN3NMGTFEU"
}
,
"seller"
:
{
"merchant_id"
:
"6C6TADF69U7Q6"
}
,
"indicators"
:
[
"ACCELERATED_CHECKOUT_MEMBER_ADD_CARD"
]
,
"seller_protection_type"
:
"SELLER_PROTECTION_INELIGIBLE"
,
"seller_protection_eligible"
:
false
}
]
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"status"
:
"RESOLVED"
,
"dispute_state"
:
"RESOLVED"
,
"dispute_amount"
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
"outcome"
:
"WON"
,
"dispute_life_cycle_stage"
:
"CHARGEBACK"
,
"dispute_channel"
:
"INTERNAL"
,
"dispute_flow"
:
"OTHER"
,
"links"
:
[
{
"href"
:
"
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-208420
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
https://api-m.sandbox.paypal.com/v1/customer/disputes?seller_protection_types=SELLER_PROTECTION_INELIGIBLE
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
https://api-m.sandbox.paypal.com/v1/customer/disputes?seller_protection_types=SELLER_PROTECTION_INELIGIBLE
"
,
"rel"
:
"first"
,
"method"
:
"GET"
}
]
}
Appeal dispute
post
/v1/customer/disputes/{id}/appeal
Try it
Appeals a dispute, by ID. To appeal a dispute, use the
appeal
link in the
HATEOAS links
from the show dispute details response. If this link does not appear, you cannot appeal the dispute. Submit new evidence as a document or notes in the JSON request body. For constraints and rules regarding documents, see
documents
.
To make this request, specify the dispute ID in the URI and specify the evidence in the JSON request body. For information about dispute reasons, see
dispute reasons
.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The PayPal dispute ID.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
evidences
Array of
objects
(
evidence
)
[ 0 .. 100 ] items
An array of evidences for the dispute.
return_shipping_address
object
(
Portable Postal Address (Medium-Grained)
)
The return address for the item.
Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason..
return_shipping_address_info
object
(
Return shipping address information
)
Merchant provided information regarding return shipping address.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
Request samples
Payload
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
Sample 1 - 200 - Appeal Dispute
Sample 1 - 200 - Appeal Dispute
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-27803
"
}
]
}
Deny offer to resolve dispute
post
/v1/customer/disputes/{id}/deny-offer
Try it
Denies an offer that the merchant proposes for a dispute, by ID.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to deny an offer.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
note
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The customer notes about the denial of offer. PayPal can but the merchant cannot view these notes.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
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
Sample 1 - 200 - Deny Offer to Resolve Dispute
Sample 1 - 200 - Deny Offer to Resolve Dispute
Copy
{
"note"
:
"refund offer is very low."
}
Response samples
200
application/json
Sample 1 - 200 - Deny Offer to Resolve Dispute
Sample 1 - 200 - Deny Offer to Resolve Dispute
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-000-000-651-454
"
}
]
}
Escalate dispute to claim
post
/v1/customer/disputes/{id}/escalate
Try it
Escalates the dispute, by ID, to a PayPal claim. To make this call, the stage in the dispute lifecycle must be
INQUIRY
.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute to escalate to a claim.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
note
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The notes about the escalation of the dispute to a claim.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
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
Sample 1 - 200 - Escalate Dispute to Claim
Sample 1 - 200 - Escalate Dispute to Claim
Copy
{
"note"
:
"Escalating to PayPal claim for resolution."
}
Response samples
200
application/json
Sample 1 - 200 - Escalate Dispute to Claim
Sample 1 - 200 - Escalate Dispute to Claim
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-000-000-651-454
"
}
]
}
Provide supporting information for dispute
post
/v1/customer/disputes/{id}/provide-supporting-info
Try it
Provides supporting information for a dispute, by ID. A merchant or buyer can make this request for disputes if they find the
provide-supporting-info
link in the HATEOAS links in the list disputes response. The party can provide the supporting information to PayPal to defend themselves only when the
dispute_life_cycle_stage
is
CHARGEBACK
,
PRE_ARBITRATION
, or
ARBITRATION
. They can provide a note that describes their part with details or upload any supporting documents to support their side. For constraints and rules regarding documents, see
documents
.
To make this request, specify the dispute ID in the URI and specify the notes in the JSON request body. This method differs from the provide evidence method which supports only multipart request, where PayPal asks the concerned party for evidence.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to provide the supporting information.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
notes
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The notes that describe the defense.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that includes a link to the dispute.
Request samples
Payload
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
Copy
{
"notes"
:
"string"
}
Response samples
200
application/json
Sample 1 - 200 - Provide Supporting Information for Dispute
Sample 1 - 200 - Provide Supporting Information for Dispute
Copy
Expand all
Collapse all
{
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
https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-27803
"
}
]
}
Accept offer to resolve dispute
post
/v1/customer/disputes/{id}/accept-offer
Try it
The customer accepts the offer from merchant to resolve a dispute, by ID. PayPal automatically refunds the amount proposed by merchant to the customer.
Security
Oauth2
Request
path
Parameters
id
required
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute for which to accept an offer.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
note
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The customer notes about accepting of offer. PayPal can but the merchant cannot view these notes.
Responses
202
A successfully accepted request returns the HTTP
202 Accepted
status code and a JSON response body that includes a
HATEOAS link
to the ID of the request. The request returns
202 Accepted
status in case money movement for the offer is delayed due to some internal reasons.
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
Sample 1 - 202 - Accept Offer to Resolve Dispute - Accepted (202)
Sample 1 - 202 - Accept Offer to Resolve Dispute - Accepted (202)
Copy
{
"note"
:
"I am ok with the refund offered."
}
Response samples
202
application/json
Sample 1 - 202 - Accept Offer to Resolve Dispute - Accepted (202)
Sample 1 - 202 - Accept Offer to Resolve Dispute - Accepted (202)
Copy
Expand all
Collapse all
{
"links"
:
[
{
"href"
:
"
https://api-m.sandbox.paypal.com/v1/apis/requests/84880ea1-6d89-4ac2-982e-821cce7db87e
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
Errors
ACTION_NOT_ALLOWED_IN_CURRENT_DISPUTE_STATE
Message:
This action is not allowed for this dispute ID. For the allowed actions, see the HATEOAS link in
show dispute details
.
Description:
You cannot complete this action for this dispute ID.
AMOUNT_SHOULD_NOT_BE_PASSED
Message:
For
MERCHANDISE_OR_SERVICE_NOT_RECEIVED
disputes, refund amount cannot be specified in accept claim as this feature is not yet supported in PayPal Dispute system.
Description:
You cannot specify the refund amount in an accept claim call.
AUTHORIZATION_ERROR
Message:
Authorization error occurred.
Description:
An authorization error occurred. Check your credentials.
DATE_CAN_NOT_BE_IN_FUTURE
Message:
The
start_time
is incorrect. The
start_time
must be earlier than the current date and time stamp.
Description:
The specified start time is in the future.
DISPUTE_REASON_NOT_ELIGIBLE
Message:
This dispute reason is not allowed for this transaction. To review the allowed reasons for this transaction, call validate transaction eligibility. Then, retry with one of the allowed reasons.
Description:
The specified dispute reason is not valid.
FUNDING_INSTRUMENT_PREFERENCE_NOT_ALLOWED
Message:
This action is not allowed for this dispute ID.
Description:
You cannot specify the refund funding instrument preference, As this option not present in allowed_action_options.
INSUFFICIENT_FUNDS
Message:
You have insufficient funds in your account to accept a claim for this dispute. Add the appropriate balance to your PayPal account before you accept a claim for this case.
Description:
Your account has insufficient funds for this claim.
INTANGIBLE_ITEM_CANNOT_BE_RETURNED
Message:
Return shipping address cannot be specified in accept claim for intangible item related disputes as this applies only for tangible item related transactions.
Description:
You cannot specify the shipping address in an accept claim call for intangible item-related disputes.
INTERNAL_SERVICE_ERROR
Message:
An internal service error has occurred.
Description:
Resend the request at another time.
INVALID_EVIDENCE_FILE
Message:
The evidence file is not valid. The user can upload up to 50 MB of files for a case. Individual files must be smaller than 10 MB. The supported file formats are JPG, GIF, PNG, and PDF. Correct and retry the request.
Description:
The evidence file is not valid.
INVALID_EVIDENCE_TYPE_PROOF_OF_FULFILLMENT
Message:
The
PROOF_OF_FULFILLMENT
evidence type is not a valid evidence type for this dispute reason and status. Retry the request with a different evidence type.
Description:
This evidence type is not valid for this dispute reason and status.
INVALID_PAGE_SIZE
Message:
The
page_size
is outside the allowed range. A valid
page_size
is from 1 to 50. Retry the request.
Description:
The page size is outside the allowed range.
INVALID_RETURN_SHIPPING_ADDRESS_FORMAT
Message:
The format specified for the return shipping address is not valid. Correct the format and retry. See
accept claim
.
Description:
The shipping address format is not valid.
INVALID_START_TIME_FORMAT
Message:
The
start_time
is not in the correct date and time format. The
start_time
must be in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
. Retry the request with the correct date and time format.
Description:
The start time is not in the correct date and time format.
INVALID_START_TIME_RANGE
Message:
The
start_time
is outside the allowed range. The
start_time
must be within the last 180 days. Retry the request with a valid
start_time
.
Description:
The start time is outside the allowed range.
ITEM_ID_IS_MANDATORY_FOR_MULTIPLE_EVIDENCES
Message:
An item ID is required for this dispute. Provide an item ID for each evidence document. For details, see
provide evidence
.
Description:
An item ID is required.
MANDATORY_PARAMETER_MISSING
Message:
When you create a dispute, a
buyer_transaction_id
is required but it is missing. Retry with a valid
buyer_transaction_id
.
Description:
The customer transaction ID, or
buyer_transaction_id
, is missing.
MISSING_EVIDENCE_INFO
Message:
The evidence information is required but it is missing for this dispute. Retry the request with valid evidence information. For details, see
provide evidence
.
Description:
The evidence information is missing.
MISSING_EVIDENCE_TYPE
Message:
The evidence type is required but it is missing for this dispute. Retry the request with a valid evidence type. For details, see
provide evidence
.
Description:
The evidence type is missing.
MISSING_REASON_CODE
Message:
To add or update a reason code, you must provide a reason code but it is missing. Retry the request with a valid reason code.
Description:
A reason code is missing.
MISSING_REFUND_ID
Message:
For
PROOF_OF_REFUND
, at least one refund ID is required but it is missing. Retry the request with a valid refund ID. For information, For details, see
provide evidence
.
Description:
A refund ID is missing. You specify
PROOF_OF_REFUND
in the
evidence_type
parameter of a
provide evidence
call.
MISSING_RETURN_SHIPPING_ADDRESS
Message:
For
MERCHANDISE_OR_SERVICE_NOT_RECEIVED
cases, return shipping address cannot be specified in accept claim as this applies only for
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
disputes.
Description:
You cannot specify the return shipping address in an accept claim call because the shipping address applies to only
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
disputes.
MISSING_TRACKING_INFO
Message:
For
PROOF_OF_FULFILLMENT
, the tracking number and carrier name are required but they are missing. Retry the request. For information, see
response_tracking_info
.
Description:
The tracking number and carrier name are missing. You specify
PROOF_OF_FULFILLMENT
in the
evidence_type
parameter of a
provide evidence
call.
PERMISSION_DENIED
Message:
You do not have the correct permission for the requested operation.
Description:
You do not have the correct permissions to make this request.
PROVISIONAL_CREDIT_PREFERENCE_NOT_ALLOWED
Message:
This action is not allowed for this dispute ID.
Description:
You cannot specify the provisional credit preference, As this option not present in allowed_action_options.
REFUND_DECLINED_BY_COMPLIANCE_SCANNING
Message:
The refund has been declined by compliance scanning.
Description:
Refund declined by Compliance Scanning.
REFUND_PREFERENCE_MUTUALLY_EXCLUSIVE
Message:
Invalid request - see details.
Description:
You should not provide preference for funding instrument and provisional credit in same request. Any one preference should be passed per request based on allowed_action_options.
RESOURCE_NOT_FOUND_ERROR
Message:
Resource not found.
Description:
The requested resource is not found in the system.
SHIPPING_ADDRESS_SHOULD_NOT_BE_PASSED
Message:
If seller proposed offer is less than buyer requested refund amount, shipping address must be specified for
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
disputes. PayPal may use this in case buyer denies the offer and requests buyer to return the item to resolve the dispute.
Description:
You must specify the shipping address for
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
disputes.
UNKNOWN_ERROR
Message:
Unknown exception occurred.
Description:
An unknown error occurred.
VALIDATION_ERROR
Message:
Invalid request - see details.
Description:
One or more validation errors occurred. See the details for specific validation errors.
Definitions
Accept Claim Type
The refund type proposed by the merchant for the dispute.
string
(
Accept Claim Type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The refund type proposed by the merchant for the dispute.
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This type is applicable when a merchant is willing to refund the entire dispute amount without any further action from customer. Omit the
refund_amount
and
return_shipping_address
parameters from the
accept claim
call.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This type is applicable when a merchant is willing to refund the dispute amount and requires the customer to return the item. Include the
return_shipping_address
parameter in but omit the
refund_amount
parameter from the
accept claim
call.
PARTIAL_REFUND
The merchant proposes a partial refund for the dispute.This type is applicable when a merchant is willing to refund an amount lesser than dispute amount. Include the
refund_amount
parameter.
REFUND_WITH_RETURN_SHIPMENT_LABEL
The customer must return the item to the merchant and then merchant will refund the money. This type is applicable when a merchant is willing to refund the dispute amount and requires the customer to return the item using the shipment label provided by the merchant. Include the
return_shipment_info
and
return_shipping_address
parameter in but omit the
refund_amount
parameter from the
accept claim
call.
Copy
"REFUND"
accept_claim
A request by a merchant to accept a customer's merchandise claim.
note
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The merchant's notes about the claim. PayPal can, but the customer cannot, view these notes.
accept_claim_reason
string
(
accept_claim_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The merchant's reason for acceptance of the customer's claim.
Enum Value
Description
DID_NOT_SHIP_ITEM
Merchant is accepting customer's claim as they could not ship the item back to the customer
TOO_TIME_CONSUMING
Merchant is accepting customer's claim as it is taking too long for merchant to fulfil the order
LOST_IN_MAIL
Merchant is accepting customer's claim as the item is lost in mail or transit
NOT_ABLE_TO_WIN
Merchant is accepting customer's claim as the merchant is not able to find sufficient evidence to win this dispute
COMPANY_POLICY
Merchant is accepting customer’s claims to follow their internal company policy
REASON_NOT_SET
This is the default value merchant can use if none of the above reasons apply
invoice_id
string
[ 1 .. 127 ] characters
^.*$
The merchant-provided ID of the invoice for the refund. This optional value is used to map the refund to an invoice ID in the merchant's system.
return_shipment_info
Array of
objects
(
response_shipment_info
)
[ 1 .. 100 ] items
An array of relevant shipment information for the items.
Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason using the shipment label provided by the merchant.
return_shipping_address
object
(
Portable Postal Address (Medium-Grained)
)
The return address for the item.
Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason, especially if the refund amount is less than the dispute amount.
return_shipping_address_info
object
(
Return shipping address information
)
Merchant provided information regarding return shipping address.
refund_amount
object
(
Money
)
To accept a customer's claim, the amount that the merchant agrees to refund the customer. The subsequent action depends on the amount:
If this amount is less than the customer-requested amount, the dispute updates to require customer acceptance.
If this amount is equal to or greater than the customer-requested amount, this amount is automatically refunded to the customer and the dispute closes.
accept_claim_type
string
(
Accept Claim Type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The refund type proposed by the merchant for the dispute.
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This type is applicable when a merchant is willing to refund the entire dispute amount without any further action from customer. Omit the
refund_amount
and
return_shipping_address
parameters from the
accept claim
call.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This type is applicable when a merchant is willing to refund the dispute amount and requires the customer to return the item. Include the
return_shipping_address
parameter in but omit the
refund_amount
parameter from the
accept claim
call.
PARTIAL_REFUND
The merchant proposes a partial refund for the dispute.This type is applicable when a merchant is willing to refund an amount lesser than dispute amount. Include the
refund_amount
parameter.
REFUND_WITH_RETURN_SHIPMENT_LABEL
The customer must return the item to the merchant and then merchant will refund the money. This type is applicable when a merchant is willing to refund the dispute amount and requires the customer to return the item using the shipment label provided by the merchant. Include the
return_shipment_info
and
return_shipping_address
parameter in but omit the
refund_amount
parameter from the
accept claim
call.
Copy
Expand all
Collapse all
{
"note"
:
"string"
,
"accept_claim_reason"
:
"DID_NOT_SHIP_ITEM"
,
"invoice_id"
:
"string"
,
"return_shipment_info"
:
[
{
"shipment_label"
:
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
,
"tracking_info"
:
{
"carrier_name"
:
"UPS"
,
"carrier_name_other"
:
"string"
,
"tracking_url"
:
"
http://example.com
"
,
"tracking_number"
:
"string"
}
}
]
,
"return_shipping_address"
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
"return_shipping_address_info"
:
{
"save_to_profile"
:
true
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
,
"accept_claim_type"
:
"REFUND"
}
accept_claim
The allowed response options when the merchant is accepting the claim.
accept_claim_types
Array of
strings
(
Accept Claim Type
)
[ 1 .. 10 ] items
The types of refund the merchant can provide the customer.
Items
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This type is applicable when a merchant is willing to refund the entire dispute amount without any further action from customer. Omit the
refund_amount
and
return_shipping_address
parameters from the
accept claim
call.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This type is applicable when a merchant is willing to refund the dispute amount and requires the customer to return the item. Include the
return_shipping_address
parameter in but omit the
refund_amount
parameter from the
accept claim
call.
PARTIAL_REFUND
The merchant proposes a partial refund for the dispute.This type is applicable when a merchant is willing to refund an amount lesser than dispute amount. Include the
refund_amount
parameter.
REFUND_WITH_RETURN_SHIPMENT_LABEL
The customer must return the item to the merchant and then merchant will refund the money. This type is applicable when a merchant is willing to refund the dispute amount and requires the customer to return the item using the shipment label provided by the merchant. Include the
return_shipment_info
and
return_shipping_address
parameter in but omit the
refund_amount
parameter from the
accept claim
call.
Copy
Expand all
Collapse all
{
"accept_claim_types"
:
[
"REFUND"
]
}
accept_claim_reason
The merchant's reason for acceptance of the customer's claim.
string
(
accept_claim_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The merchant's reason for acceptance of the customer's claim.
Enum Value
Description
DID_NOT_SHIP_ITEM
Merchant is accepting customer's claim as they could not ship the item back to the customer
TOO_TIME_CONSUMING
Merchant is accepting customer's claim as it is taking too long for merchant to fulfil the order
LOST_IN_MAIL
Merchant is accepting customer's claim as the item is lost in mail or transit
NOT_ABLE_TO_WIN
Merchant is accepting customer's claim as the merchant is not able to find sufficient evidence to win this dispute
COMPANY_POLICY
Merchant is accepting customer’s claims to follow their internal company policy
REASON_NOT_SET
This is the default value merchant can use if none of the above reasons apply
Copy
"DID_NOT_SHIP_ITEM"
accept_offer
A customer request to accept the offer made by the merchant.
note
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The customer notes about accepting of offer. PayPal can but the merchant cannot view these notes.
Copy
{
"note"
:
"string"
}
acknowledge_return_item
A merchant request to acknowledge receipt of the disputed item that the customer returned.
note
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The merchant provided notes. PayPal can but the consumer cannot view these notes.
evidences
Array of
objects
(
acknowledge_return_item_evidence
)
[ 1 .. 100 ] items
An array of evidence documents.
acknowledgement_type
string
(
acknowledgement_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of acknowledgement given by the merchant.
Enum Value
Description
ITEM_RECEIVED
The merchant has received the item returned by the customer.
ITEM_NOT_RECEIVED
The merchant has not received the item.
DAMAGED
The items returned by the customer were damaged.
EMPTY_PACKAGE_OR_DIFFERENT
The package was empty or the goods were different from what was expected.
MISSING_ITEMS
The package did not have all the items that were expected.
Copy
Expand all
Collapse all
{
"note"
:
"string"
,
"evidences"
:
[
{
"evidence_type"
:
"PROOF_OF_DAMAGE"
,
"documents"
:
[
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
]
}
]
,
"acknowledgement_type"
:
"ITEM_RECEIVED"
}
acknowledge_return_item
The allowed response options when the seller acknowledges that the buyer has returned an item for the dispute.
acknowledgement_types
Array of
strings
(
acknowledgement_type
)
[ 1 .. 10 ] items
The types of response when the merchant acknowledges a returned item.
Items
Enum Value
Description
ITEM_RECEIVED
The merchant has received the item returned by the customer.
ITEM_NOT_RECEIVED
The merchant has not received the item.
DAMAGED
The items returned by the customer were damaged.
EMPTY_PACKAGE_OR_DIFFERENT
The package was empty or the goods were different from what was expected.
MISSING_ITEMS
The package did not have all the items that were expected.
Copy
Expand all
Collapse all
{
"acknowledgement_types"
:
[
"ITEM_RECEIVED"
]
}
acknowledge_return_item_evidence
An evidence submitted by the merchant when acknowledging a returned item.
evidence_type
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The evidence type.
Enum Value
Description
PROOF_OF_DAMAGE
Documentation supporting the claim that the item is damaged.
THIRDPARTY_PROOF_FOR_DAMAGE_OR_SIGNIFICANT_DIFFERENCE
Proof should be provided by an unbiased third-party, such as a dealer, appraiser or another individual or organisation that's qualified in the area of the item in question (other than yourself), and detail the extent of the damage or clearly explain how the item received significantly differs from the item advertised.
DECLARATION
Signed declaration about the information provided.
PROOF_OF_MISSING_ITEMS
Image of open box with returned items and shipping label clearly visible.
PROOF_OF_EMPTY_PACKAGE_OR_DIFFERENT_ITEM
Image of empty box or returned items that are different from what were expected and shipping label clearly visible.
PROOF_OF_ITEM_NOT_RECEIVED
Any proof about the non receipt of the item, such as screenshot of tracking info.
documents
required
Array of
objects
(
document
)
[ 1 .. 100 ] items
An array of evidence documents.
Copy
Expand all
Collapse all
{
"evidence_type"
:
"PROOF_OF_DAMAGE"
,
"documents"
:
[
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
]
}
acknowledgement_type
The type of acknowledgement allowed for the merchant after the customer has returned the item. The merchant can update whether the item was received and is as expected or if the item was not received.
string
(
acknowledgement_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of acknowledgement allowed for the merchant after the customer has returned the item. The merchant can update whether the item was received and is as expected or if the item was not received.
Enum Value
Description
ITEM_RECEIVED
The merchant has received the item returned by the customer.
ITEM_NOT_RECEIVED
The merchant has not received the item.
DAMAGED
The items returned by the customer were damaged.
EMPTY_PACKAGE_OR_DIFFERENT
The package was empty or the goods were different from what was expected.
MISSING_ITEMS
The package did not have all the items that were expected.
Copy
"ITEM_RECEIVED"
action_info
The extended properties for a evidence. Includes additional information such as the action for which the evidence was requested/submitted, and whether the evidence is mandatory.
action
string
[ 1 .. 255 ] characters
^[A-Z_]+$
The action for which the evidence was requested or submitted.
Enum Value
Description
ACKNOWLEDGE_RETURN_ITEM
The evidence corresponds to action
acknowledge_return_item
.
ACCEPT_CLAIM
The evidence corresponds to action
accept_claim
.
PROVIDE_EVIDENCE
The evidence corresponds to action
provide_evidence
.
APPEAL
The evidence corresponds to action
appeal
.
CANCEL
The evidence corresponds to action
cancel
.
CHANGE_REASON
The evidence corresponds to action
change_reason
.
ESCALATE
The evidence corresponds to action
escalate
.
response_option
string
[ 1 .. 255 ] characters
^[A-Z_]+$
The response option for the corresponding action. Possible values:
Acknowledgement Types
Accept Claim types
.
mandatory
boolean
Indicates whether the evidence is mandatory for the corresponding action and response option.
Copy
{
"action"
:
"ACKNOWLEDGE_RETURN_ITEM"
,
"response_option"
:
"string"
,
"mandatory"
:
true
}
adjudicate
A request to settle a dispute in either the customer's or merchant's favor.
adjudication_outcome
required
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The outcome of the adjudication.
Enum Value
Description
BUYER_FAVOR
Resolves the case in the customer's favor. Outcome is set to
RESOLVED_BUYER_FAVOR
.
SELLER_FAVOR
Resolves the case in the merchant's favor. Outcome is set to
RESOLVED_SELLER_FAVOR
.
Copy
{
"adjudication_outcome"
:
"BUYER_FAVOR"
}
adjudication
The Adjudication details for the dispute.
type
required
string
(
adjudication_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of adjudication.
Enum Value
Description
DENY_BUYER
The decision is to deny the buyer for the dispute.
PAYOUT_TO_BUYER
The decision is to payout to the buyer.
PAYOUT_TO_SELLER
The decision is to payout to the seller if the seller was debited earlier.
RECOVER_FROM_SELLER
The decision is to charge the seller for the dispute if the seller was not debited already.
adjudication_time
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
The date and time when the adjudication was done, in
Internet date and time format
.
reason
string
(
adjudication_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the adjudication type.
Enum Value
Description
AMOUNT_DIFFERENCE_EXPECTED_DUE_TO_FEES
Seller submitted proof of correct charge.
BILLING_AGREEMENT_CHANGE_DISCLOSED
Seller had disclosed billing agreement changes upfront.
BILLING_AGREEMENT_CHANGE_NOT_DISCLOSED
Seller had not disclosed billing agreement changes upfront.
BILLING_AGREEMENT_DATE_CHANGE_DISCLOSED
Seller had shared change in billing agreement date upfront.
BILLING_AGREEMENT_DATE_CHANGE_NOT_DISCLOSED
Seller had not shared change in billing agreement date upfront.
BUYER_ATTEMPTED_RETURN
Buyer has attempted to return the item.
BUYER_BILLED_ONLY_ONCE
Buyer was charged only once and did not submit sufficient evidence of duplicate charge.
BUYER_CANCELLED_CASE
Buyer cancelled the case.
BUYER_CANCELLED_SERVICE
Buyer cancelled the service or recurring transaction.
BUYER_FAILED_TO_DESCRIBE_ISSUE
Buyer did not describe the issue to justify the refund.
BUYER_HAS_POSSESSION_OF_THE_MERCHANDISE_OR_SERVICE
Buyer continues to possess the item or has received the service.
BUYER_MADE_NO_ATTEMPT_TO_RESOLVE_WITH_SELLER
Buyer did not attempt to resolve the issue with the seller.
BUYER_NOT_IN_POSSESSION_OF_ITEM_TO_RETURN
Buyer is not in possession of the item to be returned.
BUYER_PROVIDED_CREDIT_RECEIPT
Buyer provided credit receipt or relevant documentation.
BUYER_RECEIVED_DUPLICATE_REFUND
Buyer received the refund twice.
CANCELLED_PER_TERMS_OF_BILLING_AGREEMENT
Billing agreement was cancelled as per agreed terms.
CARD_NOT_STOLEN
Buyer in possession of the card which was reported as stolen or lost.
CARD_NOT_STOLEN_BEFORE_AUTH
Buyer reported card as lost or stolen after the authorization date.
CUSTOMER_RECOGNIZES_TRANSACTION
Buyer recognizes the transaction as valid.
DECISION_BASED_ON_AVAILABLE_INFORMATION
Case decision was made as per available information when specific reasons are not applicable.
DELIVERY_AFTER_EXPECTED_DELIVERY_DATE
Item or service was delivered after the expected delivery date had passed.
DELIVERY_DUE_WITHIN_EXPECTED_DELIVERY_DATE
Delivery of the item or service is due within the expected delivery date.
DELIVERY_OR_SERVICE_REFUSED
Seller refused delivery or service of the item.
DOCUMENTATION_MATCHES_AMOUNT_CHARGED
Documentation provided supports the amount that was charged.
DOCUMENTATION_MATCHES_AMOUNT_IN_PAYPAL_ACCOUNT
Documentation provided supports the amount charged on buyer's account.
DUPLICATE_ADD_FUNDS
Buyer submitted sufficient proof of duplicate charge.
EFFORTLESS_SELLER_PROTECTION
The case is decided based on Protection Policy.
IN_PERSON_DELIVERY
Seller delivered the item in person.
INELIGIBLE_BUYER_PROTECTION_POLICY
The pattern identified does not meet buyer protection eligibility.
INELIGIBLE_SELLER_PROTECTION_POLICY
The pattern identified does not meet seller protection eligibility.
INQUIRY_OFFER_ITEM_REPLACED
Seller agreed to replace the item.
INQUIRY_OFFER_PARTIAL_REFUND
Seller agreed to issue a partial refund to the buyer.
INQUIRY_OFFER_REFUND_WITH_ITEM_RETURN
Seller agreed to issue a refund for item return.
INQUIRY_OFFER_REFUND_WITH_REPLACEMENT
Seller agreed to replace the damaged item along with refunds applicable.
INVALID_APPEAL_REASON
Seller appealed twice for the same reason with invalid reason.
INVALID_CHARGEBACK_SELLER_FAVOUR
The case is decided as invalid based on external network policy.
INVALID_DELIVERY_PROOF
Seller provided invalid proof of delivery.
INVALID_DELIVERY_PROOF_SIGNATURE
Buyer's signature confirmation missing in proof of delivery.
INVALID_DOCUMENTATION
The documentation provided is not valid.
INVALID_PROOF_OF_SHIPMENT
Seller provided invalid proof of shipment.
INVALID_REFUND_PROOF
Seller provided invalid proof of refund.
INVALID_RETURN_DELIVERY_NO_SIGNATURE_PROOF
Seller's signature confirmation missing in proof of return.
INVALID_RETURN_DELIVERY_PROOF
Buyer provided invalid proof of return.
INVALID_TRACKING
Seller provided invalid tracking information.
ITEM_ALTERED_REPAIRED
Item was altered or repaired while in buyer's possession.
ITEM_NOT_AS_ADVERTISED
Item or service provided didn’t match as it was advertised.
ITEM_NOT_AS_DESCRIBED
Item or service provided didn’t match as it was described.
ITEM_NOT_DAMAGED
Item or service provided was not damaged or missing any parts.
ITEM_NOT_DELIVERED
Seller did not deliver the item to the buyer.
ITEM_NOT_RETURNED_TO_SELLER
Item was not returned to seller.
ITEM_NOT_SHIPPED
Seller did not provide verified proof of shipment or delivery.
ITEM_OF_DIFFERENT_QUALITY_OR_QUANTITY
Item sent to the buyer was of different quality, quantity, color, or size.
ITEM_OUT_OF_STOCK_AND_NOT_DELIVERED
Item was not delivered as it was no longer in stock.
ITEM_RETURNED_TO_SELLER
Buyer returned the item to seller.
ITEM_SERVICE_MISREPRESENTED
Seller's listing misrepresented the item.
ITEM_SERVICE_NOT_MISREPRESENTED
Seller's listing accurately represented the item.
ITEM_SERVICE_RECEIVED_BY_BUYER
Buyer received the item or service from the seller.
ITEM_SOLD_AS_DESCRIBED
Item was sold in the condition as described by the seller.
ITEM_VALUE_UNAFFECTED
Item value or usability was not affected significantly.
MULTIPLE_APPEALS_WITH_SAME_REASON
Seller appealed multiple times for the same reason without providing any additional evidence.
NO_DOCUMENTATION_FROM_BUYER
No documentation received from buyer.
NO_DOCUMENTATION_SUPPORTING_DUE_OF_CREDIT
No documentation given to support that credit is due to buyer.
NO_PROOF_OF_DELIVERY
Seller did not provide proof of delivery.
NO_PROOF_OF_DELIVERY_INTANGIBLE
Seller did not provide proof of fulfillment for a service or digital good.
NO_PROTECTION_FOR_DIGITAL_GOODS_SERVICE
Digital goods, services, or other Intangibles not covered under Protection Policies.
NO_RESPONSE_FROM_BUYER
No response from buyer.
NO_RESPONSE_FROM_BUYER_FOR_ADDITIONAL_INFO_REQUEST
No response from buyer to the request for additional information.
NO_SELLER_RESPONSE
No response from seller.
NO_SELLER_RESPONSE_FOR_ADDITIONAL_INFO_REQUEST
Seller did not respond to a request for additional information.
NO_VALID_SHIPMENT_PROOF
Seller did not provide valid proof of shipment.
NOT_A_BILLING_ERROR
No evidence of a billing error.
NOT_AN_UNAUTHORIZED_TRANSACTION
No evidence of unauthorized account access was found.
NOT_DUPLICATE_FUNDS_ADDED_ONCE
Funds only added once and no duplication.
NOT_DUPLICATE_FUNDS_WITHDRAWN_ONCE
Funds only withdrawn once and no duplication.
NOT_SHIPPED_TO_CORRECT_ADDRESS
Seller did not ship to correct address.
PARTIAL_REFUND_ISSUED_FOR_MISSING_ITEMS
Seller issued refund for missing items.
PARTIAL_REFUND_OFFER_ACCEPTED
Buyer accepted the partial refund offer.
PAYMENT_REVERSED_ALREADY
Payment was previously refunded or reversed.
POS_SUBMITTED_INSTEAD_OF_POD
Seller submitted proof of shipment instead of proof of delivery.
PREAUTH_INSTALLMENT_DUE
Pre-authorized installment or balance is due to seller.
PROOF_OF_BILLING_AFTER_CANCELLATION_ACCEPTED
Buyer submitted proof of being billed after the billing agreement was cancelled.
PROOF_OF_DUPLICATE_DENIED_OR_INSUFFICIENT
Buyer submitted proof that this was paid by another payment method.
PROOF_OF_INCORRECT_TRANSACTION_AMOUNT_ACCEPTED
Bank or Credit does not match withdrawal amount on PayPal.
PROOF_OF_PAID_BY_OTHER_MEANS_NOT_SUBMITTED
Buyer did not provide sufficient proof of paying by other means.
PROOF_OF_TRACKING_NOT_SUBMITTED
Buyer did not provide sufficient proof of tracking for returns.
PROTECTED_BY_PAYPAL
This case is covered under Seller protection program.
REPRESENTED_BY_PAYPAL
Paypal covered the cost of the case as decided by policy.
SELLER_ACCEPTED_MULTIPLE_PAYMENTS
Seller received multiple payments for the same purchase.
SELLER_AGREED_REFUND_WITHOUT_RETURN
Seller chose to issue a refund without requiring item to be returned.
SELLER_AGREED_TO_ISSUE_CREDIT
Seller agreed to refund the buyer.
SELLER_ISSUED_CREDIT_TO_BUYER
Seller has earlier issued a credit to the buyer for the same transaction.
SELLER_ISSUED_REFUND
Seller has issued a refund.
SELLER_NOT_REACHABLE
Seller could not be reached to resolve case.
SELLER_RECEIVED_PAYMENT_TWICE_OR_FOR_REPLACEMENT
Seller received the payment twice or received payment for a replacement item.
SELLER_REFUSED_REFUND
Seller declined to issue a refund.
SELLER_REFUSED_RETURN
Seller declined to accept return of the item.
SELLER_SURCHARGED_BUYER
Surcharge was assessed to the buyer.
SERVICE_NOT_COMPLETED_AS_AGREED
Service was not completed by seller as per description in the agreement.
SHIPPING_COMPANY_WONT_SHIP
Shipping company refused to ship the item.
TRACKING_PROOF_NOT_ENOUGH
For an item which was significantly not as described, seller cannot appeal with tracking information.
TRANSACTION_AUTHORIZED_BY_CARDHOLDER
Card holder authorized the use of card for the transaction.
TRANSACTION_CANCELLED_AFTER_AUTHORIZATION_DATE
Transaction was cancelled after the authorization date.
TRANSACTION_CANCELLED_BEFORE_SHIPMENT_SERVICE_DATE
Transaction was cancelled before the shipment or service date.
TRANSACTION_MATCHES_BUYER_SPENDING_PATTERN
Transaction similar to recent spending patterns of buyer.
TRANSACTION_PROCESSED_CORRECTLY
Transaction processed correctly.
TRUSTED_BUYER_PAYOUT
Payout to the buyer decided based on their profile and policy.
UNUSED_SHIPPING_LABEL
Shipping label provided was unused.
VALID_PROOF_OF_DELIVERY
Seller provided valid proof of delivery.
VALID_PROOF_OF_DELIVERY_WITH_SIGNATURE
Seller provided valid proof of delivery with signature confirmation.
VALID_PROOF_OF_REFUND
Seller provided valid proof of refund.
VALID_PROOF_SUPPORTING_CLAIM
Valid proof was provided by buyer that supports the claim.
VALID_RETURN_DELIVERY_PROOF
Buyer provided valid proof of return delivery.
VALID_RETURN_DELIVERY_PROOF_WITH_SIGNATURE
Buyer provided valid proof of return delivery with signature confirmation.
VALID_SHIPMENT_PROOF
Seller provided valid proof of shipment.
VALUE_AFFECTED_SIGNIFICANTLY
The value of item or usability was affected significantly.
PROTECTION_POLICY_APPLIES
The case is decided based on Protection Policy.
SNAD_DELAYED_FILING
The reason as to why the buyer is filing dispute after given specified days.
FUNDS_TRANSFERRED_TO_INCORRECT_RECIPIENT
Funds were not transferred to the correct recipient.
IN_TRANSIT_BEYOND_TIMEFRAME_INVALID_PROOF_OF_SHIPMENT_OR_DELIVERY
Seller provided invalid proof of shipment, delivery shows the item was in transit beyond the allowed timeframe.
INVALID_EVIDENCE
Seller provided invalid evidence, categorized as
OTHER
.
INVALID_PROOF_DELIVERED_TO_UNSPECIFIED_LOCATION
Seller provided invalid proof of shipment, delivery shows the item was delivered to an unspecified location.
INVALID_PROOF_DELIVERED_TO_INCORRECT_ADDRESS
Seller provided invalid proof of shipment, delivery shows the item was delivered to an incorrect address.
INVALID_PROOF_UNABLE_TO_TRACK
Seller provided invalid proof of shipment. The shipment could not be tracked with the information provided.
SHIPPING_ADDRESS_NOT_PRESENT_IN_PROOF_OF_SHIPMENT_OR_DELIVERY
Seller provided invalid proof of shipment since it lacks the correct shipping address.
INVALID_PROOF_ITEM_RETURNED_TO_SENDER
Seller provided invalid proof of shipment which shows the item was returned back to the sender.
DELIVERED_WITHOUT_REQUIRED_SIGNATURE_IN_PROOF_OF_DELIVERY
Proof of delivery provided by the seller is invalid since it is missing the required signature.
NO_SHIPMENT_TRACKING_PROVIDED_IN_PROOF_OF_DELIVERY
Proof of delivery provided by the seller is invalid since since no shipment tracking is provided.
OTHER_ISSUE_WITH_PROOF_OF_SHIPMENT_OR_DELIVERY
Seller provided invalid proof of shipment or delivery.
INSUFFICIENT_EVIDENCE_PROVIDED
Seller did not provide any sufficient evidence.
EVIDENCE_CANNOT_BE_LINKED_TO_TRANSACTION
Evidence provided by the seller is invalid since it could not be linked to the transaction.
EVIDENCE_DOES_NOT_SHOW_FULFILLMENT_OR_CUSTOMER_BENEFIT
Evidence provided by the seller does not demonstrate fulfillment or customer benefit.
SELLER_SHIPPED_OR_FULFILLED_BEYOND_ALLOWED_PERIOD
Order was shipped two days after the dispute was filed, making the evidence invalid.
ITEM_INELIGIBLE_FOR_SELLER_PROTECTION
Item does not meet the requirements for seller protection.
EVIDENCE_DOES_NOT_SHOW_SERVICE_COMPLETED
The evidence provided by the seller does not show that the service was completed as per the service agreement.
VALID_RETURN_SHIPMENT_PROOF
Buyer provided evidence that the item was shipped back for return.
ITEM_EMPTY_BOX
The item sent to the buyer was an empty box.
ITEM_UNUSABLE
The item sent to the buyer was unusable.
ITEM_MISSING_QUANTITY_OR_QUALITY
The item sent to the buyer was missing in quality or quantity.
REFUND_AMOUNT_MISMATCH
The refund amount promised does not match the actual refunded amount.
DUPLICATE_PAYMENT
Multiple payments were processed for the same transaction.
SELLER_PROMISED_REFUND_NOT_ISSUED
The evidence indicates seller promised refund to the buyer but did not issue it.
CUSTOMER_CHARGED_INCORRECT_AMOUNT
The evidence indicates customer was charged an incorrect amount.
DUPLICATE_PAYMENT_BY_OTHER_MEANS
The evidence indicates that the customer was charged multiple times for the same order through different payment methods.
GOODWILL_PAYOUT
Seller did not provide enough evidence. Since the account is in good standing, it will not be debited for the disputed amount this time. The seller has been advised to review the previous
adjudication
under
adjudications
returned as part of the
dispute details
API response for a detailed explanation of why the evidence did not meet requirements.
dispute_life_cycle_stage
string
(
dispute_lifecycle_stage
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The dispute life cycle stage during the adjudication.
Enum Value
Description
INQUIRY
A customer and merchant interact in an attempt to resolve a dispute without escalation to PayPal. Occurs when the customer:
Has not received goods or a service.
Reports that the received goods or service are not as described.
Needs more details, such as a copy of the transaction or a receipt.
CHARGEBACK
A customer or merchant escalates an inquiry to a claim, which authorizes PayPal to investigate the case and make a determination. Occurs only when the dispute channel is
INTERNAL
. This stage is a PayPal dispute lifecycle stage and not a credit card or debit card chargeback. All notes that the customer sends in this stage are visible to PayPal agents only. The customer must wait for PayPal’s response before the customer can take further action. In this stage, PayPal shares dispute details with the merchant, who can complete one of these actions:
Accept the claim.
Submit evidence to challenge the claim.
Make an offer to the customer to resolve the claim.
PRE_ARBITRATION
The first appeal stage for merchants. A merchant can appeal a chargeback if PayPal's decision is not in the merchant's favor. If the merchant does not appeal within the appeal period, PayPal considers the case resolved.
ARBITRATION
The second appeal stage for merchants. A merchant can appeal a dispute for a second time if the first appeal was denied. If the merchant does not appeal within the appeal period, the case returns to a resolved status in pre-arbitration stage.
Copy
{
"type"
:
"DENY_BUYER"
,
"adjudication_time"
:
"string"
,
"reason"
:
"AMOUNT_DIFFERENCE_EXPECTED_DUE_TO_FEES"
,
"dispute_life_cycle_stage"
:
"INQUIRY"
}
adjudication_reason
The reason for the adjudication type.
string
(
adjudication_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the adjudication type.
Enum Value
Description
AMOUNT_DIFFERENCE_EXPECTED_DUE_TO_FEES
Seller submitted proof of correct charge.
BILLING_AGREEMENT_CHANGE_DISCLOSED
Seller had disclosed billing agreement changes upfront.
BILLING_AGREEMENT_CHANGE_NOT_DISCLOSED
Seller had not disclosed billing agreement changes upfront.
BILLING_AGREEMENT_DATE_CHANGE_DISCLOSED
Seller had shared change in billing agreement date upfront.
BILLING_AGREEMENT_DATE_CHANGE_NOT_DISCLOSED
Seller had not shared change in billing agreement date upfront.
BUYER_ATTEMPTED_RETURN
Buyer has attempted to return the item.
BUYER_BILLED_ONLY_ONCE
Buyer was charged only once and did not submit sufficient evidence of duplicate charge.
BUYER_CANCELLED_CASE
Buyer cancelled the case.
BUYER_CANCELLED_SERVICE
Buyer cancelled the service or recurring transaction.
BUYER_FAILED_TO_DESCRIBE_ISSUE
Buyer did not describe the issue to justify the refund.
BUYER_HAS_POSSESSION_OF_THE_MERCHANDISE_OR_SERVICE
Buyer continues to possess the item or has received the service.
BUYER_MADE_NO_ATTEMPT_TO_RESOLVE_WITH_SELLER
Buyer did not attempt to resolve the issue with the seller.
BUYER_NOT_IN_POSSESSION_OF_ITEM_TO_RETURN
Buyer is not in possession of the item to be returned.
BUYER_PROVIDED_CREDIT_RECEIPT
Buyer provided credit receipt or relevant documentation.
BUYER_RECEIVED_DUPLICATE_REFUND
Buyer received the refund twice.
CANCELLED_PER_TERMS_OF_BILLING_AGREEMENT
Billing agreement was cancelled as per agreed terms.
CARD_NOT_STOLEN
Buyer in possession of the card which was reported as stolen or lost.
CARD_NOT_STOLEN_BEFORE_AUTH
Buyer reported card as lost or stolen after the authorization date.
CUSTOMER_RECOGNIZES_TRANSACTION
Buyer recognizes the transaction as valid.
DECISION_BASED_ON_AVAILABLE_INFORMATION
Case decision was made as per available information when specific reasons are not applicable.
DELIVERY_AFTER_EXPECTED_DELIVERY_DATE
Item or service was delivered after the expected delivery date had passed.
DELIVERY_DUE_WITHIN_EXPECTED_DELIVERY_DATE
Delivery of the item or service is due within the expected delivery date.
DELIVERY_OR_SERVICE_REFUSED
Seller refused delivery or service of the item.
DOCUMENTATION_MATCHES_AMOUNT_CHARGED
Documentation provided supports the amount that was charged.
DOCUMENTATION_MATCHES_AMOUNT_IN_PAYPAL_ACCOUNT
Documentation provided supports the amount charged on buyer's account.
DUPLICATE_ADD_FUNDS
Buyer submitted sufficient proof of duplicate charge.
EFFORTLESS_SELLER_PROTECTION
The case is decided based on Protection Policy.
IN_PERSON_DELIVERY
Seller delivered the item in person.
INELIGIBLE_BUYER_PROTECTION_POLICY
The pattern identified does not meet buyer protection eligibility.
INELIGIBLE_SELLER_PROTECTION_POLICY
The pattern identified does not meet seller protection eligibility.
INQUIRY_OFFER_ITEM_REPLACED
Seller agreed to replace the item.
INQUIRY_OFFER_PARTIAL_REFUND
Seller agreed to issue a partial refund to the buyer.
INQUIRY_OFFER_REFUND_WITH_ITEM_RETURN
Seller agreed to issue a refund for item return.
INQUIRY_OFFER_REFUND_WITH_REPLACEMENT
Seller agreed to replace the damaged item along with refunds applicable.
INVALID_APPEAL_REASON
Seller appealed twice for the same reason with invalid reason.
INVALID_CHARGEBACK_SELLER_FAVOUR
The case is decided as invalid based on external network policy.
INVALID_DELIVERY_PROOF
Seller provided invalid proof of delivery.
INVALID_DELIVERY_PROOF_SIGNATURE
Buyer's signature confirmation missing in proof of delivery.
INVALID_DOCUMENTATION
The documentation provided is not valid.
INVALID_PROOF_OF_SHIPMENT
Seller provided invalid proof of shipment.
INVALID_REFUND_PROOF
Seller provided invalid proof of refund.
INVALID_RETURN_DELIVERY_NO_SIGNATURE_PROOF
Seller's signature confirmation missing in proof of return.
INVALID_RETURN_DELIVERY_PROOF
Buyer provided invalid proof of return.
INVALID_TRACKING
Seller provided invalid tracking information.
ITEM_ALTERED_REPAIRED
Item was altered or repaired while in buyer's possession.
ITEM_NOT_AS_ADVERTISED
Item or service provided didn’t match as it was advertised.
ITEM_NOT_AS_DESCRIBED
Item or service provided didn’t match as it was described.
ITEM_NOT_DAMAGED
Item or service provided was not damaged or missing any parts.
ITEM_NOT_DELIVERED
Seller did not deliver the item to the buyer.
ITEM_NOT_RETURNED_TO_SELLER
Item was not returned to seller.
ITEM_NOT_SHIPPED
Seller did not provide verified proof of shipment or delivery.
ITEM_OF_DIFFERENT_QUALITY_OR_QUANTITY
Item sent to the buyer was of different quality, quantity, color, or size.
ITEM_OUT_OF_STOCK_AND_NOT_DELIVERED
Item was not delivered as it was no longer in stock.
ITEM_RETURNED_TO_SELLER
Buyer returned the item to seller.
ITEM_SERVICE_MISREPRESENTED
Seller's listing misrepresented the item.
ITEM_SERVICE_NOT_MISREPRESENTED
Seller's listing accurately represented the item.
ITEM_SERVICE_RECEIVED_BY_BUYER
Buyer received the item or service from the seller.
ITEM_SOLD_AS_DESCRIBED
Item was sold in the condition as described by the seller.
ITEM_VALUE_UNAFFECTED
Item value or usability was not affected significantly.
MULTIPLE_APPEALS_WITH_SAME_REASON
Seller appealed multiple times for the same reason without providing any additional evidence.
NO_DOCUMENTATION_FROM_BUYER
No documentation received from buyer.
NO_DOCUMENTATION_SUPPORTING_DUE_OF_CREDIT
No documentation given to support that credit is due to buyer.
NO_PROOF_OF_DELIVERY
Seller did not provide proof of delivery.
NO_PROOF_OF_DELIVERY_INTANGIBLE
Seller did not provide proof of fulfillment for a service or digital good.
NO_PROTECTION_FOR_DIGITAL_GOODS_SERVICE
Digital goods, services, or other Intangibles not covered under Protection Policies.
NO_RESPONSE_FROM_BUYER
No response from buyer.
NO_RESPONSE_FROM_BUYER_FOR_ADDITIONAL_INFO_REQUEST
No response from buyer to the request for additional information.
NO_SELLER_RESPONSE
No response from seller.
NO_SELLER_RESPONSE_FOR_ADDITIONAL_INFO_REQUEST
Seller did not respond to a request for additional information.
NO_VALID_SHIPMENT_PROOF
Seller did not provide valid proof of shipment.
NOT_A_BILLING_ERROR
No evidence of a billing error.
NOT_AN_UNAUTHORIZED_TRANSACTION
No evidence of unauthorized account access was found.
NOT_DUPLICATE_FUNDS_ADDED_ONCE
Funds only added once and no duplication.
NOT_DUPLICATE_FUNDS_WITHDRAWN_ONCE
Funds only withdrawn once and no duplication.
NOT_SHIPPED_TO_CORRECT_ADDRESS
Seller did not ship to correct address.
PARTIAL_REFUND_ISSUED_FOR_MISSING_ITEMS
Seller issued refund for missing items.
PARTIAL_REFUND_OFFER_ACCEPTED
Buyer accepted the partial refund offer.
PAYMENT_REVERSED_ALREADY
Payment was previously refunded or reversed.
POS_SUBMITTED_INSTEAD_OF_POD
Seller submitted proof of shipment instead of proof of delivery.
PREAUTH_INSTALLMENT_DUE
Pre-authorized installment or balance is due to seller.
PROOF_OF_BILLING_AFTER_CANCELLATION_ACCEPTED
Buyer submitted proof of being billed after the billing agreement was cancelled.
PROOF_OF_DUPLICATE_DENIED_OR_INSUFFICIENT
Buyer submitted proof that this was paid by another payment method.
PROOF_OF_INCORRECT_TRANSACTION_AMOUNT_ACCEPTED
Bank or Credit does not match withdrawal amount on PayPal.
PROOF_OF_PAID_BY_OTHER_MEANS_NOT_SUBMITTED
Buyer did not provide sufficient proof of paying by other means.
PROOF_OF_TRACKING_NOT_SUBMITTED
Buyer did not provide sufficient proof of tracking for returns.
PROTECTED_BY_PAYPAL
This case is covered under Seller protection program.
REPRESENTED_BY_PAYPAL
Paypal covered the cost of the case as decided by policy.
SELLER_ACCEPTED_MULTIPLE_PAYMENTS
Seller received multiple payments for the same purchase.
SELLER_AGREED_REFUND_WITHOUT_RETURN
Seller chose to issue a refund without requiring item to be returned.
SELLER_AGREED_TO_ISSUE_CREDIT
Seller agreed to refund the buyer.
SELLER_ISSUED_CREDIT_TO_BUYER
Seller has earlier issued a credit to the buyer for the same transaction.
SELLER_ISSUED_REFUND
Seller has issued a refund.
SELLER_NOT_REACHABLE
Seller could not be reached to resolve case.
SELLER_RECEIVED_PAYMENT_TWICE_OR_FOR_REPLACEMENT
Seller received the payment twice or received payment for a replacement item.
SELLER_REFUSED_REFUND
Seller declined to issue a refund.
SELLER_REFUSED_RETURN
Seller declined to accept return of the item.
SELLER_SURCHARGED_BUYER
Surcharge was assessed to the buyer.
SERVICE_NOT_COMPLETED_AS_AGREED
Service was not completed by seller as per description in the agreement.
SHIPPING_COMPANY_WONT_SHIP
Shipping company refused to ship the item.
TRACKING_PROOF_NOT_ENOUGH
For an item which was significantly not as described, seller cannot appeal with tracking information.
TRANSACTION_AUTHORIZED_BY_CARDHOLDER
Card holder authorized the use of card for the transaction.
TRANSACTION_CANCELLED_AFTER_AUTHORIZATION_DATE
Transaction was cancelled after the authorization date.
TRANSACTION_CANCELLED_BEFORE_SHIPMENT_SERVICE_DATE
Transaction was cancelled before the shipment or service date.
TRANSACTION_MATCHES_BUYER_SPENDING_PATTERN
Transaction similar to recent spending patterns of buyer.
TRANSACTION_PROCESSED_CORRECTLY
Transaction processed correctly.
TRUSTED_BUYER_PAYOUT
Payout to the buyer decided based on their profile and policy.
UNUSED_SHIPPING_LABEL
Shipping label provided was unused.
VALID_PROOF_OF_DELIVERY
Seller provided valid proof of delivery.
VALID_PROOF_OF_DELIVERY_WITH_SIGNATURE
Seller provided valid proof of delivery with signature confirmation.
VALID_PROOF_OF_REFUND
Seller provided valid proof of refund.
VALID_PROOF_SUPPORTING_CLAIM
Valid proof was provided by buyer that supports the claim.
VALID_RETURN_DELIVERY_PROOF
Buyer provided valid proof of return delivery.
VALID_RETURN_DELIVERY_PROOF_WITH_SIGNATURE
Buyer provided valid proof of return delivery with signature confirmation.
VALID_SHIPMENT_PROOF
Seller provided valid proof of shipment.
VALUE_AFFECTED_SIGNIFICANTLY
The value of item or usability was affected significantly.
PROTECTION_POLICY_APPLIES
The case is decided based on Protection Policy.
SNAD_DELAYED_FILING
The reason as to why the buyer is filing dispute after given specified days.
FUNDS_TRANSFERRED_TO_INCORRECT_RECIPIENT
Funds were not transferred to the correct recipient.
IN_TRANSIT_BEYOND_TIMEFRAME_INVALID_PROOF_OF_SHIPMENT_OR_DELIVERY
Seller provided invalid proof of shipment, delivery shows the item was in transit beyond the allowed timeframe.
INVALID_EVIDENCE
Seller provided invalid evidence, categorized as
OTHER
.
INVALID_PROOF_DELIVERED_TO_UNSPECIFIED_LOCATION
Seller provided invalid proof of shipment, delivery shows the item was delivered to an unspecified location.
INVALID_PROOF_DELIVERED_TO_INCORRECT_ADDRESS
Seller provided invalid proof of shipment, delivery shows the item was delivered to an incorrect address.
INVALID_PROOF_UNABLE_TO_TRACK
Seller provided invalid proof of shipment. The shipment could not be tracked with the information provided.
SHIPPING_ADDRESS_NOT_PRESENT_IN_PROOF_OF_SHIPMENT_OR_DELIVERY
Seller provided invalid proof of shipment since it lacks the correct shipping address.
INVALID_PROOF_ITEM_RETURNED_TO_SENDER
Seller provided invalid proof of shipment which shows the item was returned back to the sender.
DELIVERED_WITHOUT_REQUIRED_SIGNATURE_IN_PROOF_OF_DELIVERY
Proof of delivery provided by the seller is invalid since it is missing the required signature.
NO_SHIPMENT_TRACKING_PROVIDED_IN_PROOF_OF_DELIVERY
Proof of delivery provided by the seller is invalid since since no shipment tracking is provided.
OTHER_ISSUE_WITH_PROOF_OF_SHIPMENT_OR_DELIVERY
Seller provided invalid proof of shipment or delivery.
INSUFFICIENT_EVIDENCE_PROVIDED
Seller did not provide any sufficient evidence.
EVIDENCE_CANNOT_BE_LINKED_TO_TRANSACTION
Evidence provided by the seller is invalid since it could not be linked to the transaction.
EVIDENCE_DOES_NOT_SHOW_FULFILLMENT_OR_CUSTOMER_BENEFIT
Evidence provided by the seller does not demonstrate fulfillment or customer benefit.
SELLER_SHIPPED_OR_FULFILLED_BEYOND_ALLOWED_PERIOD
Order was shipped two days after the dispute was filed, making the evidence invalid.
ITEM_INELIGIBLE_FOR_SELLER_PROTECTION
Item does not meet the requirements for seller protection.
EVIDENCE_DOES_NOT_SHOW_SERVICE_COMPLETED
The evidence provided by the seller does not show that the service was completed as per the service agreement.
VALID_RETURN_SHIPMENT_PROOF
Buyer provided evidence that the item was shipped back for return.
ITEM_EMPTY_BOX
The item sent to the buyer was an empty box.
ITEM_UNUSABLE
The item sent to the buyer was unusable.
ITEM_MISSING_QUANTITY_OR_QUALITY
The item sent to the buyer was missing in quality or quantity.
REFUND_AMOUNT_MISMATCH
The refund amount promised does not match the actual refunded amount.
DUPLICATE_PAYMENT
Multiple payments were processed for the same transaction.
SELLER_PROMISED_REFUND_NOT_ISSUED
The evidence indicates seller promised refund to the buyer but did not issue it.
CUSTOMER_CHARGED_INCORRECT_AMOUNT
The evidence indicates customer was charged an incorrect amount.
DUPLICATE_PAYMENT_BY_OTHER_MEANS
The evidence indicates that the customer was charged multiple times for the same order through different payment methods.
GOODWILL_PAYOUT
Seller did not provide enough evidence. Since the account is in good standing, it will not be debited for the disputed amount this time. The seller has been advised to review the previous
adjudication
under
adjudications
returned as part of the
dispute details
API response for a detailed explanation of why the evidence did not meet requirements.
Copy
"AMOUNT_DIFFERENCE_EXPECTED_DUE_TO_FEES"
adjudication_type
The type of adjudication.
string
(
adjudication_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of adjudication.
Enum Value
Description
DENY_BUYER
The decision is to deny the buyer for the dispute.
PAYOUT_TO_BUYER
The decision is to payout to the buyer.
PAYOUT_TO_SELLER
The decision is to payout to the seller if the seller was debited earlier.
RECOVER_FROM_SELLER
The decision is to charge the seller for the dispute if the seller was not debited already.
Copy
"DENY_BUYER"
Agreed Refund Details
Details of Agreed Refund between customer and merchant.
merchant_agreed_refund
boolean
Indicates whether merchant has agreed to refund the buyer or not.
merchant_agreed_refund_time
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
The date and time proposed by merchant to provide the refund, in
Internet date and time format
.
Copy
{
"merchant_agreed_refund"
:
true
,
"merchant_agreed_refund_time"
:
"stringstringstringst"
}
allowed_response_options
The allowed response options for the buyer/seller update actions.
acknowledge_return_item
object
(
acknowledge_return_item
)
The allowed response options when the seller acknowledges that the buyer has returned an item for the dispute.
accept_claim
object
(
accept_claim
)
The allowed response options when the merchant is accepting the claim.
make_offer
object
(
make_offer
)
The allowed response options when the merchant makes offer to the customer.
Copy
Expand all
Collapse all
{
"acknowledge_return_item"
:
{
"acknowledgement_types"
:
[
"ITEM_RECEIVED"
]
}
,
"accept_claim"
:
{
"accept_claim_types"
:
[
"REFUND"
]
}
,
"make_offer"
:
{
"offer_types"
:
[
"REFUND"
]
}
}
billing_disputes_properties
The billing issue details.
duplicate_transaction
object
(
duplication_transaction
)
The duplicate transaction details.
incorrect_transaction_amount
object
(
incorrect_transaction_amount
)
The incorrect transaction amount details.
payment_by_other_means
object
(
payment_by_other_means
)
The payment by other means details.
credit_not_processed
object
(
credit_not_processed
)
The credit not processed details.
canceled_recurring_billing
object
(
canceled_recurring_billing
)
The recurring billing canceled details.
Copy
Expand all
Collapse all
{
"duplicate_transaction"
:
{
"received_duplicate"
:
true
,
"original_transaction"
:
{
"buyer_transaction_id"
:
"string"
,
"seller_transaction_id"
:
"string"
,
"reference_id"
:
"string"
,
"transaction_status"
:
"COMPLETED"
,
"invoice_number"
:
"string"
,
"custom"
:
"string"
,
"items"
:
[
{
"item_id"
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
"item_quantity"
:
"string"
,
"partner_transaction_id"
:
"string"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"notes"
:
"string"
,
"item_type"
:
"PRODUCT"
,
"dispute_amount"
:
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
"create_time"
:
"stringstringstringst"
,
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
"gross_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"buyer"
:
{
"name"
:
"string"
}
,
"seller"
:
{
"merchant_id"
:
"string"
,
"name"
:
"string"
,
"email"
:
"string"
}
}
}
,
"incorrect_transaction_amount"
:
{
"correct_transaction_amount"
:
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
"correct_transaction_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"correct_transaction_time"
:
"stringstringstringst"
}
,
"payment_by_other_means"
:
{
"charge_different_from_original"
:
true
,
"received_duplicate"
:
true
,
"payment_method"
:
"CASH"
,
"payment_instrument_suffix"
:
"stri"
}
,
"credit_not_processed"
:
{
"issue_type"
:
"PRODUCT"
,
"agreed_refund_details"
:
{
"merchant_agreed_refund"
:
true
,
"merchant_agreed_refund_time"
:
"stringstringstringst"
}
,
"expected_refund"
:
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
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
,
"product_details"
:
{
"description"
:
"string"
,
"product_received"
:
"YES"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
,
"product_received_time"
:
"string"
,
"expected_delivery_date"
:
"string"
,
"return_details"
:
{
"mode"
:
"SHIPPED"
,
"receipt"
:
true
,
"return_confirmation_number"
:
"string"
,
"returned"
:
true
,
"return_time"
:
"stringstringstringst"
}
}
,
"service_details"
:
{
"description"
:
"string"
,
"service_started"
:
"YES"
,
"note"
:
"string"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
}
}
,
"canceled_recurring_billing"
:
{
"expected_refund"
:
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
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
}
}
buyer
The details for the customer who funds the payment. For example, the customer's first name, last name, and email address.
name
string
[ 1 .. 2000 ] characters
^[^~!@#$%^*()_{}:|\t\n/]+$
The customer's name.
Copy
{
"name"
:
"string"
}
canceled_recurring_billing
The recurring billing canceled details.
expected_refund
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
cancellation_details
object
(
cancellation_details
)
The cancellation details.
Copy
Expand all
Collapse all
{
"expected_refund"
:
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
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
}
cancellation_details
The cancellation details.
cancellation_number
string
[ 1 .. 127 ] characters
^.*$
The cancellation number.
cancelled
boolean
Indicates whether the dispute was canceled.
cancellation_mode
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Indicates the mode used for order cancellation.
Enum Value
Description
CANCELLED_PAYPAL_BILLING_AGREEMENT
Cancelled the billing agreement.
WEBSITE
The item was cancelled on the merchant's website.
PHONE
The item was cancelled through either phone or fax.
EMAIL
The item was cancelled through either email or text message.
WRITTEN
The item was cancelled via written communication.
IN_PERSON
The item was cancelled in person.
cancellation_date
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
The date and time of the cancellation, in
Internet date and time format
.
Copy
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
cancellation_reason
The reason the customer cancelled the dispute.
string
(
cancellation_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason the customer cancelled the dispute.
Enum Value
Description
ITEM_RECEIVED
The customer already received the item.
REFUND_RECEIVED
The customer already received a refund for the item.
OTHER
The customer cancelled the dispute for another reason. If OTHER is specified, customer needs to specify more information in the notes field.
SHIPMENT_INFO_RECEIVED
The customer received the provided shipping tracking information and agrees to cancel.
REPLACEMENT_RECEIVED
The customer received the item replacement and agrees to cancel.
Copy
"ITEM_RECEIVED"
communication_details
The contact details that a merchant provides to the customer to use to share their evidence documents.
note
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The merchant provided notes that are visible to both the customer and PayPal.
email
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
The email address that is provided by the merchant where the customer can share the evidences.
time_posted
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
The date and time when the contact details were posted, in
Internet date and time format
.
Copy
{
"note"
:
"string"
,
"email"
:
"string"
,
"time_posted"
:
"stringstringstringst"
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
credit_not_processed
The credit not processed details.
issue_type
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The issue type.
Enum Value
Description
PRODUCT
The product has an issue.
SERVICE
The service has an issue.
agreed_refund_details
object
(
Agreed Refund Details
)
Details of Agreed Refund between customer and merchant.
expected_refund
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
cancellation_details
object
(
cancellation_details
)
The cancellation details.
product_details
object
(
product_details
)
The product information.
service_details
object
(
service_details
)
The service details.
Copy
Expand all
Collapse all
{
"issue_type"
:
"PRODUCT"
,
"agreed_refund_details"
:
{
"merchant_agreed_refund"
:
true
,
"merchant_agreed_refund_time"
:
"stringstringstringst"
}
,
"expected_refund"
:
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
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
,
"product_details"
:
{
"description"
:
"string"
,
"product_received"
:
"YES"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
,
"product_received_time"
:
"string"
,
"expected_delivery_date"
:
"string"
,
"return_details"
:
{
"mode"
:
"SHIPPED"
,
"receipt"
:
true
,
"return_confirmation_number"
:
"string"
,
"returned"
:
true
,
"return_time"
:
"stringstringstringst"
}
}
,
"service_details"
:
{
"description"
:
"string"
,
"service_started"
:
"YES"
,
"note"
:
"string"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
}
}
Crypto trade details
The Crypto trade details.
trade_id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9]+$
The Trade id for the crypto-currency order.
Copy
{
"trade_id"
:
"string"
}
Cryptocurrency
The details needed to represent a specific cryptocurrency balance, such as its symbol and quantity.
asset_symbol
required
string
(
cryptocurrency_symbol
)
[ 1 .. 10 ] characters
^[0-9A-Za-z]{1,10}$
The cryptocurrency symbol or code ticker options. Assigned by liquidity providers and exchanges.
Enum Value
Description
BTC
The ticker symbol for
Bitcoin
.
https://en.wikipedia.org/wiki/Bitcoin
.
ETH
The ticker symbol for
Ethereum
.
https://en.wikipedia.org/wiki/Ethereum
.
BCH
The ticker symbol for
Bitcoin Cash
.
https://en.wikipedia.org/wiki/Bitcoin_Cash
.
LTC
The ticker symbol for
Litecoin
.
https://en.wikipedia.org/wiki/Litecoin
.
PYUSD
The ticker symbol for
PayPal Coin
.
https://engineering.paypalcorp.com/confluence/display/BCDC/PayPal+Digital+Coin+%28PPDC%29+-+USDP+-+Top+Down+View+of+Requirements
.
LINK
The ticker symbol for
Chainlink
.
https://en.wikipedia.org/wiki/Chainlink_(blockchain)
.
SOL
The ticker symbol for
Solana
.
https://en.wikipedia.org/wiki/Solana_(blockchain_platform)
.
MATIC
The ticker symbol for Polygon.
quantity
required
string
(
cryptocurrency_quantity
)
[ 1 .. 40 ] characters
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The quantity of a cryptocurrency asset. This is a decimal number with a scale defined for each cryptocurrency by its founders. For example, Bitcoin (BTC) has 8 as its scale, Ethereum (ETH) has 18 as its scale. The PayPal Cryptocurrency platform handles the scale to 8 digits for Bitcoin. including its forks or offshoots, as well as Ethereum.
quantity_in_subunits
string
(
Cryptocurrency Quantity Subunits
)
[ 1 .. 81 ] characters
^-?[0-9]+$
The quantity of a cryptocurrency asset in the currency's sub units.
Amount is an integer in a string format.
Floating point should be avoided to avoid precision errors. For example:
Bitcoin(BTC) has 8 decimals,
so 1 BTC will be represented as 100000000 (1 followed by 8 zeroes).
Ethereum(ETH) has 18 decimals,
so 1 ETH will be represented as 1000000000000000000 (1 followed by 18 zeroes).
decimals
integer
(
Decimals
)
[ 0 .. 40 ]
The number of decimal digits supported by this cryptocurrency. For example, for Bitcoin this value is 8 because there are 10^8 satoshis in one Bitcoin and for Ethereum it's 18 since there are 10^18 wei in one Ether.
Copy
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
Cryptocurrency Quantity Subunits
The quantity of a cryptocurrency asset in the currency's sub units.
Amount is an integer in a string format.
Floating point should be avoided to avoid precision errors. For example:
Bitcoin(BTC) has 8 decimals,
so 1 BTC will be represented as 100000000 (1 followed by 8 zeroes).
Ethereum(ETH) has 18 decimals,
so 1 ETH will be represented as 1000000000000000000 (1 followed by 18 zeroes).
string
(
Cryptocurrency Quantity Subunits
)
[ 1 .. 81 ] characters
^-?[0-9]+$
The quantity of a cryptocurrency asset in the currency's sub units.
Amount is an integer in a string format.
Floating point should be avoided to avoid precision errors. For example:
Bitcoin(BTC) has 8 decimals,
so 1 BTC will be represented as 100000000 (1 followed by 8 zeroes).
Ethereum(ETH) has 18 decimals,
so 1 ETH will be represented as 1000000000000000000 (1 followed by 18 zeroes).
Copy
"string"
cryptocurrency_quantity
The quantity of a cryptocurrency asset. This is a decimal number with a scale defined for each cryptocurrency by its founders. For example, Bitcoin (BTC) has 8 as its scale, Ethereum (ETH) has 18 as its scale. The PayPal Cryptocurrency platform handles the scale to 8 digits for Bitcoin. including its forks or offshoots, as well as Ethereum.
string
(
cryptocurrency_quantity
)
[ 1 .. 40 ] characters
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The quantity of a cryptocurrency asset. This is a decimal number with a scale defined for each cryptocurrency by its founders. For example, Bitcoin (BTC) has 8 as its scale, Ethereum (ETH) has 18 as its scale. The PayPal Cryptocurrency platform handles the scale to 8 digits for Bitcoin. including its forks or offshoots, as well as Ethereum.
Copy
"string"
cryptocurrency_symbol
The cryptocurrency symbol or code ticker options. Assigned by liquidity providers and exchanges.
string
(
cryptocurrency_symbol
)
[ 1 .. 10 ] characters
^[0-9A-Za-z]{1,10}$
The cryptocurrency symbol or code ticker options. Assigned by liquidity providers and exchanges.
Enum Value
Description
BTC
The ticker symbol for
Bitcoin
.
https://en.wikipedia.org/wiki/Bitcoin
.
ETH
The ticker symbol for
Ethereum
.
https://en.wikipedia.org/wiki/Ethereum
.
BCH
The ticker symbol for
Bitcoin Cash
.
https://en.wikipedia.org/wiki/Bitcoin_Cash
.
LTC
The ticker symbol for
Litecoin
.
https://en.wikipedia.org/wiki/Litecoin
.
PYUSD
The ticker symbol for
PayPal Coin
.
https://engineering.paypalcorp.com/confluence/display/BCDC/PayPal+Digital+Coin+%28PPDC%29+-+USDP+-+Top+Down+View+of+Requirements
.
LINK
The ticker symbol for
Chainlink
.
https://en.wikipedia.org/wiki/Chainlink_(blockchain)
.
SOL
The ticker symbol for
Solana
.
https://en.wikipedia.org/wiki/Solana_(blockchain_platform)
.
MATIC
The ticker symbol for Polygon.
Copy
"BTC"
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
Decimals
The number of decimal digits supported by this cryptocurrency. For example, for Bitcoin this value is 8 because there are 10^8 satoshis in one Bitcoin and for Ethereum it's 18 since there are 10^18 wei in one Ether.
integer
(
Decimals
)
[ 0 .. 40 ]
The number of decimal digits supported by this cryptocurrency. For example, for Bitcoin this value is 8 because there are 10^8 satoshis in one Bitcoin and for Ethereum it's 18 since there are 10^18 wei in one Ether.
Copy
40
deny_offer
A customer request to deny the offer made by the merchant.
note
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The customer notes about the denial of offer. PayPal can but the merchant cannot view these notes.
Copy
{
"note"
:
"string"
}
dispute
The dispute details.
dispute_id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute.
disputed_transactions
Array of
objects
(
transaction_info
)
[ 1 .. 1000 ] items
An array of transactions for which disputes were created.
external_reason_code
string
[ 1 .. 2000 ] characters
^[A-Za-z0-9._-]+$
The code that identifies the reason for the credit card chargeback. Each card issuer follows their own standards for defining reason type, code, and its format. For more details about the external reason code, see the card issue site. Available for only unbranded transactions.
adjudications
Array of
objects
(
adjudication
)
[ 1 .. 10 ] items
The Teammate Adjudication details for the dispute.
money_movements
Array of
objects
(
money_movement
)
[ 1 .. 50 ] items
DEPRECATED The Money movement details for the dispute.
fund_movements
Array of
objects
(
fund_movement
)
[ 1 .. 50 ] items
The movements of fund due to the dispute.
messages
Array of
objects
(
message
)
[ 1 .. 1000 ] items
An array of customer- or merchant-posted messages for the dispute.
evidences
Array of
objects
(
evidence
)
[ 1 .. 100 ] items
An array of evidence documents.
supporting_info
Array of
objects
(
supporting_info
)
[ 1 .. 100 ] items
An array of all the supporting information that are associated to this dispute.
links
Array of
objects
(
Link Description
)
[ 1 .. 10 ] items
An array of request-related
HATEOAS links
.
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
The date and time when the dispute was created, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
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
The date and time when the dispute was last updated, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
reason
string
(
reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the item-level dispute. For information about the required information for each dispute reason and associated evidence type, see
dispute reasons
.
Enum Value
Description
MERCHANDISE_OR_SERVICE_NOT_RECEIVED
The customer did not receive the merchandise or service.
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
The customer reports that the merchandise or service is not as described.
UNAUTHORISED
The customer did not authorize purchase of the merchandise or service.
CREDIT_NOT_PROCESSED
The refund or credit was not processed for the customer.
DUPLICATE_TRANSACTION
The transaction was a duplicate.
INCORRECT_AMOUNT
The customer was charged an incorrect amount.
PAYMENT_BY_OTHER_MEANS
The customer paid for the transaction through other means.
CANCELED_RECURRING_BILLING
The customer was being charged for a subscription or a recurring transaction that was canceled.
PROBLEM_WITH_REMITTANCE
A problem occurred with the remittance.
OTHER
Other.
status
string
(
status
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The overall status of the dispute, constant for all the parties involved at anytime during the dispute lifecycle.
Enum Value
Description
OPEN
The dispute is open.
WAITING_FOR_BUYER_RESPONSE
The dispute is waiting for a response from the customer.
WAITING_FOR_SELLER_RESPONSE
The dispute is waiting for a response from the merchant.
UNDER_REVIEW
The dispute is under review with PayPal.
RESOLVED
The dispute is resolved.
OTHER
The default status if the dispute does not have one of the other statuses.
dispute_amount
object
(
Money
)
The amount in the transaction that the customer originally disputed. Because customers can sometimes dispute only part of the payment, the disputed amount might be different from the total gross or net amount of the original transaction.
dispute_asset
object
(
Cryptocurrency
)
The asset in the transaction that the customer disputed.
fee_policy
object
(
Fee Policy
)
Policy that determines whether the fee needs to be charged, retained or returned while moving the money as part of dispute process.
dispute_outcome
object
(
dispute_outcome
)
The outcome of a dispute.
dispute_life_cycle_stage
string
(
dispute_lifecycle_stage
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The stage in the dispute lifecycle.
Enum Value
Description
INQUIRY
A customer and merchant interact in an attempt to resolve a dispute without escalation to PayPal. Occurs when the customer:
Has not received goods or a service.
Reports that the received goods or service are not as described.
Needs more details, such as a copy of the transaction or a receipt.
CHARGEBACK
A customer or merchant escalates an inquiry to a claim, which authorizes PayPal to investigate the case and make a determination. Occurs only when the dispute channel is
INTERNAL
. This stage is a PayPal dispute lifecycle stage and not a credit card or debit card chargeback. All notes that the customer sends in this stage are visible to PayPal agents only. The customer must wait for PayPal’s response before the customer can take further action. In this stage, PayPal shares dispute details with the merchant, who can complete one of these actions:
Accept the claim.
Submit evidence to challenge the claim.
Make an offer to the customer to resolve the claim.
PRE_ARBITRATION
The first appeal stage for merchants. A merchant can appeal a chargeback if PayPal's decision is not in the merchant's favor. If the merchant does not appeal within the appeal period, PayPal considers the case resolved.
ARBITRATION
The second appeal stage for merchants. A merchant can appeal a dispute for a second time if the first appeal was denied. If the merchant does not appeal within the appeal period, the case returns to a resolved status in pre-arbitration stage.
dispute_channel
string
(
dispute_channel
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The channel where the customer created the dispute.
Enum Value
Description
INTERNAL
The customer contacts PayPal to file a dispute with the merchant.
EXTERNAL
The customer contacts their card issuer or bank to request a refund.
ALERT
Pre-chargeback alert when customer contacts their card issuer to request a refund.
extensions
object
(
extensions
)
The extended properties for the dispute. Includes additional information for a dispute category, such as billing disputes, the original transaction ID, and the correct amount.
buyer_response_due_date
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
The date and time by when the customer must respond to the dispute, in
Internet date and time format
. If the customer does not respond by this date and time, the dispute is closed in the merchant's favor. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
seller_response_due_date
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
The date and time by when the merchant must respond to the dispute, in
Internet date and time format
. If the merchant does not respond by this date and time, the dispute is closed in the customer's favor. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
offer
object
(
offer
)
The merchant-proposed offer for a dispute.
refund_details
object
(
response_refund_details
)
The refund details.
communication_details
object
(
communication_details
)
The contact details that a merchant provides to the customer to use to share their evidence documents.
allowed_response_options
object
(
allowed_response_options
)
The allowed response options for the buyer/seller update actions.
Copy
Expand all
Collapse all
{
"dispute_id"
:
"string"
,
"disputed_transactions"
:
[
{
"buyer_transaction_id"
:
"string"
,
"seller_transaction_id"
:
"string"
,
"reference_id"
:
"string"
,
"transaction_status"
:
"COMPLETED"
,
"invoice_number"
:
"string"
,
"custom"
:
"string"
,
"items"
:
[
{
"item_id"
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
"item_quantity"
:
"string"
,
"partner_transaction_id"
:
"string"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"notes"
:
"string"
,
"item_type"
:
"PRODUCT"
,
"dispute_amount"
:
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
"create_time"
:
"stringstringstringst"
,
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
"gross_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"buyer"
:
{
"name"
:
"string"
}
,
"seller"
:
{
"merchant_id"
:
"string"
,
"name"
:
"string"
,
"email"
:
"string"
}
}
]
,
"external_reason_code"
:
"string"
,
"adjudications"
:
[
{
"type"
:
"DENY_BUYER"
,
"adjudication_time"
:
"string"
,
"reason"
:
"AMOUNT_DIFFERENCE_EXPECTED_DUE_TO_FEES"
,
"dispute_life_cycle_stage"
:
"INQUIRY"
}
]
,
"money_movements"
:
[
{
"affected_party"
:
"SELLER"
,
"type"
:
"DEBIT"
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
"asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"initiated_time"
:
"string"
,
"reason"
:
"DISPUTE_SETTLEMENT_FEE"
}
]
,
"fund_movements"
:
[
{
"party"
:
"SELLER"
,
"type"
:
"DEBIT"
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
"asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"initiated_time"
:
"string"
,
"reason"
:
"REVERSED_TRANSACTION_FEE"
}
]
,
"messages"
:
[
{
"posted_by"
:
"BUYER"
,
"content"
:
"string"
,
"documents"
:
[
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
]
,
"time_posted"
:
"stringstringstringst"
}
]
,
"evidences"
:
[
{
"evidence_type"
:
"PROOF_OF_FULFILLMENT"
,
"documents"
:
[
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
]
,
"notes"
:
"string"
,
"source"
:
"REQUESTED_FROM_BUYER"
,
"item_id"
:
"string"
,
"evidence_info"
:
{
"tracking_info"
:
[
{
"carrier_name"
:
"UPS"
,
"carrier_name_other"
:
"string"
,
"tracking_url"
:
"
http://example.com
"
,
"tracking_number"
:
"string"
}
]
,
"refund_ids"
:
[
"string"
]
}
,
"date"
:
"stringstringstringst"
,
"item_type"
:
"PRODUCT"
,
"action_info"
:
{
"action"
:
"ACKNOWLEDGE_RETURN_ITEM"
,
"response_option"
:
"string"
,
"mandatory"
:
true
}
,
"dispute_life_cycle_stage"
:
"INQUIRY"
}
]
,
"supporting_info"
:
[
{
"notes"
:
"string"
,
"documents"
:
[
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
]
,
"source"
:
"SUBMITTED_BY_BUYER"
,
"provided_time"
:
"stringstringstringst"
,
"dispute_life_cycle_stage"
:
"INQUIRY"
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
,
"create_time"
:
"stringstringstringst"
,
"update_time"
:
"stringstringstringst"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"status"
:
"OPEN"
,
"dispute_amount"
:
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
"dispute_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"fee_policy"
:
{ }
,
"dispute_outcome"
:
{
"outcome_code"
:
"RESOLVED_BUYER_FAVOUR"
,
"outcome_reason"
:
"AMOUNT_DIFFERENCE_EXPECTED_DUE_TO_FEES"
,
"amount_refunded"
:
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
"asset_refunded"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
}
,
"dispute_life_cycle_stage"
:
"INQUIRY"
,
"dispute_channel"
:
"INTERNAL"
,
"extensions"
:
{
"merchant_contacted"
:
true
,
"buyer_contacted_channel"
:
"string"
,
"merchant_contacted_outcome"
:
"NO_RESPONSE"
,
"merchant_contacted_time"
:
"string"
,
"merchant_contacted_mode"
:
"WEBSITE"
,
"buyer_contacted_time"
:
"string"
,
"billing_dispute_properties"
:
{
"duplicate_transaction"
:
{
"received_duplicate"
:
true
,
"original_transaction"
:
{
"buyer_transaction_id"
:
"string"
,
"seller_transaction_id"
:
"string"
,
"reference_id"
:
"string"
,
"transaction_status"
:
"COMPLETED"
,
"invoice_number"
:
"string"
,
"custom"
:
"string"
,
"items"
:
[
{
"item_id"
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
"item_quantity"
:
"string"
,
"partner_transaction_id"
:
"string"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"notes"
:
"string"
,
"item_type"
:
"PRODUCT"
,
"dispute_amount"
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
]
,
"create_time"
:
"stringstringstringst"
,
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
"gross_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"buyer"
:
{
"name"
:
"string"
}
,
"seller"
:
{
"merchant_id"
:
"string"
,
"name"
:
"string"
,
"email"
:
"string"
}
}
}
,
"incorrect_transaction_amount"
:
{
"correct_transaction_amount"
:
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
"correct_transaction_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"correct_transaction_time"
:
"stringstringstringst"
}
,
"payment_by_other_means"
:
{
"charge_different_from_original"
:
true
,
"received_duplicate"
:
true
,
"payment_method"
:
"CASH"
,
"payment_instrument_suffix"
:
"stri"
}
,
"credit_not_processed"
:
{
"issue_type"
:
"PRODUCT"
,
"agreed_refund_details"
:
{
"merchant_agreed_refund"
:
true
,
"merchant_agreed_refund_time"
:
"stringstringstringst"
}
,
"expected_refund"
:
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
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
,
"product_details"
:
{
"description"
:
"string"
,
"product_received"
:
"YES"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
,
"product_received_time"
:
"string"
,
"expected_delivery_date"
:
"string"
,
"return_details"
:
{
"mode"
:
"SHIPPED"
,
"receipt"
:
true
,
"return_confirmation_number"
:
"string"
,
"returned"
:
true
,
"return_time"
:
"stringstringstringst"
}
}
,
"service_details"
:
{
"description"
:
"string"
,
"service_started"
:
"YES"
,
"note"
:
"string"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
}
}
,
"canceled_recurring_billing"
:
{
"expected_refund"
:
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
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
}
}
,
"merchandize_dispute_properties"
:
{
"issue_type"
:
"PRODUCT"
,
"product_details"
:
{
"description"
:
"string"
,
"product_received"
:
"YES"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
,
"product_received_time"
:
"string"
,
"expected_delivery_date"
:
"string"
,
"return_details"
:
{
"mode"
:
"SHIPPED"
,
"receipt"
:
true
,
"return_confirmation_number"
:
"string"
,
"returned"
:
true
,
"return_time"
:
"stringstringstringst"
}
}
,
"service_details"
:
{
"description"
:
"string"
,
"service_started"
:
"YES"
,
"note"
:
"string"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
}
,
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
,
"return_shipping_address"
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
,
"reported_source"
:
"EMAIL"
}
,
"buyer_response_due_date"
:
"stringstringstringst"
,
"seller_response_due_date"
:
"stringstringstringst"
,
"offer"
:
{
"history"
:
[
{
"actor"
:
"BUYER"
,
"event_type"
:
"PROPOSED"
,
"notes"
:
"string"
,
"offer_time"
:
"stringstringstringst"
,
"offer_type"
:
"REFUND"
,
"offer_amount"
:
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
"dispute_life_cycle_stage"
:
"INQUIRY"
}
]
,
"buyer_requested_amount"
:
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
"seller_offered_amount"
:
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
"offer_type"
:
"REFUND"
}
,
"refund_details"
:
{
"transactions"
:
[
{
"id"
:
"string"
,
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
"create_time"
:
"stringstringstringst"
}
]
,
"allowed_refund_amount"
:
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
"communication_details"
:
{
"note"
:
"string"
,
"email"
:
"string"
,
"time_posted"
:
"stringstringstringst"
}
,
"allowed_response_options"
:
{
"acknowledge_return_item"
:
{
"acknowledgement_types"
:
[
"ITEM_RECEIVED"
]
}
,
"accept_claim"
:
{
"accept_claim_types"
:
[
"REFUND"
]
}
,
"make_offer"
:
{
"offer_types"
:
[
"REFUND"
]
}
}
}
dispute_channel
The channel where the customer created the dispute.
string
(
dispute_channel
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The channel where the customer created the dispute.
Enum Value
Description
INTERNAL
The customer contacts PayPal to file a dispute with the merchant.
EXTERNAL
The customer contacts their card issuer or bank to request a refund.
ALERT
Pre-chargeback alert when customer contacts their card issuer to request a refund.
Copy
"INTERNAL"
dispute_info
The dispute summary information.
dispute_id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID of the dispute.
links
Array of
objects
(
Link Description
)
[ 1 .. 10 ] items
An array of request-related
HATEOAS links
.
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
The date and time when the dispute was created, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
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
The date and time when the dispute was last updated, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
reason
string
(
reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the item-level dispute. For information about the required information for each dispute reason and associated evidence type, see
dispute reasons
.
Enum Value
Description
MERCHANDISE_OR_SERVICE_NOT_RECEIVED
The customer did not receive the merchandise or service.
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
The customer reports that the merchandise or service is not as described.
UNAUTHORISED
The customer did not authorize purchase of the merchandise or service.
CREDIT_NOT_PROCESSED
The refund or credit was not processed for the customer.
DUPLICATE_TRANSACTION
The transaction was a duplicate.
INCORRECT_AMOUNT
The customer was charged an incorrect amount.
PAYMENT_BY_OTHER_MEANS
The customer paid for the transaction through other means.
CANCELED_RECURRING_BILLING
The customer was being charged for a subscription or a recurring transaction that was canceled.
PROBLEM_WITH_REMITTANCE
A problem occurred with the remittance.
OTHER
Other.
status
string
(
status
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The overall status of the dispute, constant for all the parties involved at anytime during the dispute lifecycle.
Enum Value
Description
OPEN
The dispute is open.
WAITING_FOR_BUYER_RESPONSE
The dispute is waiting for a response from the customer.
WAITING_FOR_SELLER_RESPONSE
The dispute is waiting for a response from the merchant.
UNDER_REVIEW
The dispute is under review with PayPal.
RESOLVED
The dispute is resolved.
OTHER
The default status if the dispute does not have one of the other statuses.
dispute_state
string
(
dispute_state
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The user specific state of the dispute, could vary between parties during the dispute lifecycle.
Enum Value
Description
OPEN_INQUIRIES
The dispute is open.
REQUIRED_ACTION
The dispute is waiting for a response.
REQUIRED_OTHER_PARTY_ACTION
The dispute is waiting for a response from other party.
UNDER_PAYPAL_REVIEW
The dispute is under review with PayPal.
APPEALABLE
The dispute can be appealed.
RESOLVED
The dispute is resolved.
dispute_amount
object
(
Money
)
The amount in the transaction that the customer originally disputed. Because customers can sometimes dispute only part of the payment, the disputed amount might be different from the total gross or net amount of the original transaction.
dispute_asset
object
(
Cryptocurrency
)
The asset in the transaction that the customer disputed.
dispute_life_cycle_stage
string
(
dispute_lifecycle_stage
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The stage in the dispute lifecycle.
Enum Value
Description
INQUIRY
A customer and merchant interact in an attempt to resolve a dispute without escalation to PayPal. Occurs when the customer:
Has not received goods or a service.
Reports that the received goods or service are not as described.
Needs more details, such as a copy of the transaction or a receipt.
CHARGEBACK
A customer or merchant escalates an inquiry to a claim, which authorizes PayPal to investigate the case and make a determination. Occurs only when the dispute channel is
INTERNAL
. This stage is a PayPal dispute lifecycle stage and not a credit card or debit card chargeback. All notes that the customer sends in this stage are visible to PayPal agents only. The customer must wait for PayPal’s response before the customer can take further action. In this stage, PayPal shares dispute details with the merchant, who can complete one of these actions:
Accept the claim.
Submit evidence to challenge the claim.
Make an offer to the customer to resolve the claim.
PRE_ARBITRATION
The first appeal stage for merchants. A merchant can appeal a chargeback if PayPal's decision is not in the merchant's favor. If the merchant does not appeal within the appeal period, PayPal considers the case resolved.
ARBITRATION
The second appeal stage for merchants. A merchant can appeal a dispute for a second time if the first appeal was denied. If the merchant does not appeal within the appeal period, the case returns to a resolved status in pre-arbitration stage.
dispute_channel
string
(
dispute_channel
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The channel where the customer created the dispute.
Enum Value
Description
INTERNAL
The customer contacts PayPal to file a dispute with the merchant.
EXTERNAL
The customer contacts their card issuer or bank to request a refund.
ALERT
Pre-chargeback alert when customer contacts their card issuer to request a refund.
buyer_response_due_date
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
The date and time by when the customer must respond to the dispute, in
Internet date and time format
. If the customer does not respond by this date and time, the dispute is closed in the merchant's favor. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
seller_response_due_date
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
The date and time by when the merchant must respond to the dispute, in
Internet date and time format
. If the merchant does not respond by this date and time, the dispute is closed in the customer's favor. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
Copy
Expand all
Collapse all
{
"dispute_id"
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
"stringstringstringst"
,
"update_time"
:
"stringstringstringst"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"status"
:
"OPEN"
,
"dispute_state"
:
"OPEN_INQUIRIES"
,
"dispute_amount"
:
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
"dispute_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"dispute_life_cycle_stage"
:
"INQUIRY"
,
"dispute_channel"
:
"INTERNAL"
,
"buyer_response_due_date"
:
"stringstringstringst"
,
"seller_response_due_date"
:
"stringstringstringst"
}
dispute_lifecycle_stage
The stage in the dispute lifecycle.
string
(
dispute_lifecycle_stage
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The stage in the dispute lifecycle.
Enum Value
Description
INQUIRY
A customer and merchant interact in an attempt to resolve a dispute without escalation to PayPal. Occurs when the customer:
Has not received goods or a service.
Reports that the received goods or service are not as described.
Needs more details, such as a copy of the transaction or a receipt.
CHARGEBACK
A customer or merchant escalates an inquiry to a claim, which authorizes PayPal to investigate the case and make a determination. Occurs only when the dispute channel is
INTERNAL
. This stage is a PayPal dispute lifecycle stage and not a credit card or debit card chargeback. All notes that the customer sends in this stage are visible to PayPal agents only. The customer must wait for PayPal’s response before the customer can take further action. In this stage, PayPal shares dispute details with the merchant, who can complete one of these actions:
Accept the claim.
Submit evidence to challenge the claim.
Make an offer to the customer to resolve the claim.
PRE_ARBITRATION
The first appeal stage for merchants. A merchant can appeal a chargeback if PayPal's decision is not in the merchant's favor. If the merchant does not appeal within the appeal period, PayPal considers the case resolved.
ARBITRATION
The second appeal stage for merchants. A merchant can appeal a dispute for a second time if the first appeal was denied. If the merchant does not appeal within the appeal period, the case returns to a resolved status in pre-arbitration stage.
Copy
"INQUIRY"
dispute_outcome
The outcome of a dispute.
outcome_code
string
(
dispute_outcome_code
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The outcome of a resolved dispute.
Enum Value
Description
RESOLVED_BUYER_FAVOUR
The dispute was resolved in the customer's favor.
RESOLVED_SELLER_FAVOUR
The dispute was resolved in the merchant's favor.
RESOLVED_WITH_PAYOUT
PayPal provided the merchant or customer with protection and the case is resolved.
CANCELED_BY_BUYER
The customer canceled the dispute.
ACCEPTED
DEPRECATED. PayPal accepted the dispute.
DENIED
DEPRECATED. PayPal denied the dispute.
NONE
A dispute was created for the same transaction ID, and the previous dispute was closed without any decision.
outcome_reason
string
(
adjudication_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The justification for the adjudication outcome.
Enum Value
Description
AMOUNT_DIFFERENCE_EXPECTED_DUE_TO_FEES
Seller submitted proof of correct charge.
BILLING_AGREEMENT_CHANGE_DISCLOSED
Seller had disclosed billing agreement changes upfront.
BILLING_AGREEMENT_CHANGE_NOT_DISCLOSED
Seller had not disclosed billing agreement changes upfront.
BILLING_AGREEMENT_DATE_CHANGE_DISCLOSED
Seller had shared change in billing agreement date upfront.
BILLING_AGREEMENT_DATE_CHANGE_NOT_DISCLOSED
Seller had not shared change in billing agreement date upfront.
BUYER_ATTEMPTED_RETURN
Buyer has attempted to return the item.
BUYER_BILLED_ONLY_ONCE
Buyer was charged only once and did not submit sufficient evidence of duplicate charge.
BUYER_CANCELLED_CASE
Buyer cancelled the case.
BUYER_CANCELLED_SERVICE
Buyer cancelled the service or recurring transaction.
BUYER_FAILED_TO_DESCRIBE_ISSUE
Buyer did not describe the issue to justify the refund.
BUYER_HAS_POSSESSION_OF_THE_MERCHANDISE_OR_SERVICE
Buyer continues to possess the item or has received the service.
BUYER_MADE_NO_ATTEMPT_TO_RESOLVE_WITH_SELLER
Buyer did not attempt to resolve the issue with the seller.
BUYER_NOT_IN_POSSESSION_OF_ITEM_TO_RETURN
Buyer is not in possession of the item to be returned.
BUYER_PROVIDED_CREDIT_RECEIPT
Buyer provided credit receipt or relevant documentation.
BUYER_RECEIVED_DUPLICATE_REFUND
Buyer received the refund twice.
CANCELLED_PER_TERMS_OF_BILLING_AGREEMENT
Billing agreement was cancelled as per agreed terms.
CARD_NOT_STOLEN
Buyer in possession of the card which was reported as stolen or lost.
CARD_NOT_STOLEN_BEFORE_AUTH
Buyer reported card as lost or stolen after the authorization date.
CUSTOMER_RECOGNIZES_TRANSACTION
Buyer recognizes the transaction as valid.
DECISION_BASED_ON_AVAILABLE_INFORMATION
Case decision was made as per available information when specific reasons are not applicable.
DELIVERY_AFTER_EXPECTED_DELIVERY_DATE
Item or service was delivered after the expected delivery date had passed.
DELIVERY_DUE_WITHIN_EXPECTED_DELIVERY_DATE
Delivery of the item or service is due within the expected delivery date.
DELIVERY_OR_SERVICE_REFUSED
Seller refused delivery or service of the item.
DOCUMENTATION_MATCHES_AMOUNT_CHARGED
Documentation provided supports the amount that was charged.
DOCUMENTATION_MATCHES_AMOUNT_IN_PAYPAL_ACCOUNT
Documentation provided supports the amount charged on buyer's account.
DUPLICATE_ADD_FUNDS
Buyer submitted sufficient proof of duplicate charge.
EFFORTLESS_SELLER_PROTECTION
The case is decided based on Protection Policy.
IN_PERSON_DELIVERY
Seller delivered the item in person.
INELIGIBLE_BUYER_PROTECTION_POLICY
The pattern identified does not meet buyer protection eligibility.
INELIGIBLE_SELLER_PROTECTION_POLICY
The pattern identified does not meet seller protection eligibility.
INQUIRY_OFFER_ITEM_REPLACED
Seller agreed to replace the item.
INQUIRY_OFFER_PARTIAL_REFUND
Seller agreed to issue a partial refund to the buyer.
INQUIRY_OFFER_REFUND_WITH_ITEM_RETURN
Seller agreed to issue a refund for item return.
INQUIRY_OFFER_REFUND_WITH_REPLACEMENT
Seller agreed to replace the damaged item along with refunds applicable.
INVALID_APPEAL_REASON
Seller appealed twice for the same reason with invalid reason.
INVALID_CHARGEBACK_SELLER_FAVOUR
The case is decided as invalid based on external network policy.
INVALID_DELIVERY_PROOF
Seller provided invalid proof of delivery.
INVALID_DELIVERY_PROOF_SIGNATURE
Buyer's signature confirmation missing in proof of delivery.
INVALID_DOCUMENTATION
The documentation provided is not valid.
INVALID_PROOF_OF_SHIPMENT
Seller provided invalid proof of shipment.
INVALID_REFUND_PROOF
Seller provided invalid proof of refund.
INVALID_RETURN_DELIVERY_NO_SIGNATURE_PROOF
Seller's signature confirmation missing in proof of return.
INVALID_RETURN_DELIVERY_PROOF
Buyer provided invalid proof of return.
INVALID_TRACKING
Seller provided invalid tracking information.
ITEM_ALTERED_REPAIRED
Item was altered or repaired while in buyer's possession.
ITEM_NOT_AS_ADVERTISED
Item or service provided didn’t match as it was advertised.
ITEM_NOT_AS_DESCRIBED
Item or service provided didn’t match as it was described.
ITEM_NOT_DAMAGED
Item or service provided was not damaged or missing any parts.
ITEM_NOT_DELIVERED
Seller did not deliver the item to the buyer.
ITEM_NOT_RETURNED_TO_SELLER
Item was not returned to seller.
ITEM_NOT_SHIPPED
Seller did not provide verified proof of shipment or delivery.
ITEM_OF_DIFFERENT_QUALITY_OR_QUANTITY
Item sent to the buyer was of different quality, quantity, color, or size.
ITEM_OUT_OF_STOCK_AND_NOT_DELIVERED
Item was not delivered as it was no longer in stock.
ITEM_RETURNED_TO_SELLER
Buyer returned the item to seller.
ITEM_SERVICE_MISREPRESENTED
Seller's listing misrepresented the item.
ITEM_SERVICE_NOT_MISREPRESENTED
Seller's listing accurately represented the item.
ITEM_SERVICE_RECEIVED_BY_BUYER
Buyer received the item or service from the seller.
ITEM_SOLD_AS_DESCRIBED
Item was sold in the condition as described by the seller.
ITEM_VALUE_UNAFFECTED
Item value or usability was not affected significantly.
MULTIPLE_APPEALS_WITH_SAME_REASON
Seller appealed multiple times for the same reason without providing any additional evidence.
NO_DOCUMENTATION_FROM_BUYER
No documentation received from buyer.
NO_DOCUMENTATION_SUPPORTING_DUE_OF_CREDIT
No documentation given to support that credit is due to buyer.
NO_PROOF_OF_DELIVERY
Seller did not provide proof of delivery.
NO_PROOF_OF_DELIVERY_INTANGIBLE
Seller did not provide proof of fulfillment for a service or digital good.
NO_PROTECTION_FOR_DIGITAL_GOODS_SERVICE
Digital goods, services, or other Intangibles not covered under Protection Policies.
NO_RESPONSE_FROM_BUYER
No response from buyer.
NO_RESPONSE_FROM_BUYER_FOR_ADDITIONAL_INFO_REQUEST
No response from buyer to the request for additional information.
NO_SELLER_RESPONSE
No response from seller.
NO_SELLER_RESPONSE_FOR_ADDITIONAL_INFO_REQUEST
Seller did not respond to a request for additional information.
NO_VALID_SHIPMENT_PROOF
Seller did not provide valid proof of shipment.
NOT_A_BILLING_ERROR
No evidence of a billing error.
NOT_AN_UNAUTHORIZED_TRANSACTION
No evidence of unauthorized account access was found.
NOT_DUPLICATE_FUNDS_ADDED_ONCE
Funds only added once and no duplication.
NOT_DUPLICATE_FUNDS_WITHDRAWN_ONCE
Funds only withdrawn once and no duplication.
NOT_SHIPPED_TO_CORRECT_ADDRESS
Seller did not ship to correct address.
PARTIAL_REFUND_ISSUED_FOR_MISSING_ITEMS
Seller issued refund for missing items.
PARTIAL_REFUND_OFFER_ACCEPTED
Buyer accepted the partial refund offer.
PAYMENT_REVERSED_ALREADY
Payment was previously refunded or reversed.
POS_SUBMITTED_INSTEAD_OF_POD
Seller submitted proof of shipment instead of proof of delivery.
PREAUTH_INSTALLMENT_DUE
Pre-authorized installment or balance is due to seller.
PROOF_OF_BILLING_AFTER_CANCELLATION_ACCEPTED
Buyer submitted proof of being billed after the billing agreement was cancelled.
PROOF_OF_DUPLICATE_DENIED_OR_INSUFFICIENT
Buyer submitted proof that this was paid by another payment method.
PROOF_OF_INCORRECT_TRANSACTION_AMOUNT_ACCEPTED
Bank or Credit does not match withdrawal amount on PayPal.
PROOF_OF_PAID_BY_OTHER_MEANS_NOT_SUBMITTED
Buyer did not provide sufficient proof of paying by other means.
PROOF_OF_TRACKING_NOT_SUBMITTED
Buyer did not provide sufficient proof of tracking for returns.
PROTECTED_BY_PAYPAL
This case is covered under Seller protection program.
REPRESENTED_BY_PAYPAL
Paypal covered the cost of the case as decided by policy.
SELLER_ACCEPTED_MULTIPLE_PAYMENTS
Seller received multiple payments for the same purchase.
SELLER_AGREED_REFUND_WITHOUT_RETURN
Seller chose to issue a refund without requiring item to be returned.
SELLER_AGREED_TO_ISSUE_CREDIT
Seller agreed to refund the buyer.
SELLER_ISSUED_CREDIT_TO_BUYER
Seller has earlier issued a credit to the buyer for the same transaction.
SELLER_ISSUED_REFUND
Seller has issued a refund.
SELLER_NOT_REACHABLE
Seller could not be reached to resolve case.
SELLER_RECEIVED_PAYMENT_TWICE_OR_FOR_REPLACEMENT
Seller received the payment twice or received payment for a replacement item.
SELLER_REFUSED_REFUND
Seller declined to issue a refund.
SELLER_REFUSED_RETURN
Seller declined to accept return of the item.
SELLER_SURCHARGED_BUYER
Surcharge was assessed to the buyer.
SERVICE_NOT_COMPLETED_AS_AGREED
Service was not completed by seller as per description in the agreement.
SHIPPING_COMPANY_WONT_SHIP
Shipping company refused to ship the item.
TRACKING_PROOF_NOT_ENOUGH
For an item which was significantly not as described, seller cannot appeal with tracking information.
TRANSACTION_AUTHORIZED_BY_CARDHOLDER
Card holder authorized the use of card for the transaction.
TRANSACTION_CANCELLED_AFTER_AUTHORIZATION_DATE
Transaction was cancelled after the authorization date.
TRANSACTION_CANCELLED_BEFORE_SHIPMENT_SERVICE_DATE
Transaction was cancelled before the shipment or service date.
TRANSACTION_MATCHES_BUYER_SPENDING_PATTERN
Transaction similar to recent spending patterns of buyer.
TRANSACTION_PROCESSED_CORRECTLY
Transaction processed correctly.
TRUSTED_BUYER_PAYOUT
Payout to the buyer decided based on their profile and policy.
UNUSED_SHIPPING_LABEL
Shipping label provided was unused.
VALID_PROOF_OF_DELIVERY
Seller provided valid proof of delivery.
VALID_PROOF_OF_DELIVERY_WITH_SIGNATURE
Seller provided valid proof of delivery with signature confirmation.
VALID_PROOF_OF_REFUND
Seller provided valid proof of refund.
VALID_PROOF_SUPPORTING_CLAIM
Valid proof was provided by buyer that supports the claim.
VALID_RETURN_DELIVERY_PROOF
Buyer provided valid proof of return delivery.
VALID_RETURN_DELIVERY_PROOF_WITH_SIGNATURE
Buyer provided valid proof of return delivery with signature confirmation.
VALID_SHIPMENT_PROOF
Seller provided valid proof of shipment.
VALUE_AFFECTED_SIGNIFICANTLY
The value of item or usability was affected significantly.
PROTECTION_POLICY_APPLIES
The case is decided based on Protection Policy.
SNAD_DELAYED_FILING
The reason as to why the buyer is filing dispute after given specified days.
FUNDS_TRANSFERRED_TO_INCORRECT_RECIPIENT
Funds were not transferred to the correct recipient.
IN_TRANSIT_BEYOND_TIMEFRAME_INVALID_PROOF_OF_SHIPMENT_OR_DELIVERY
Seller provided invalid proof of shipment, delivery shows the item was in transit beyond the allowed timeframe.
INVALID_EVIDENCE
Seller provided invalid evidence, categorized as
OTHER
.
INVALID_PROOF_DELIVERED_TO_UNSPECIFIED_LOCATION
Seller provided invalid proof of shipment, delivery shows the item was delivered to an unspecified location.
INVALID_PROOF_DELIVERED_TO_INCORRECT_ADDRESS
Seller provided invalid proof of shipment, delivery shows the item was delivered to an incorrect address.
INVALID_PROOF_UNABLE_TO_TRACK
Seller provided invalid proof of shipment. The shipment could not be tracked with the information provided.
SHIPPING_ADDRESS_NOT_PRESENT_IN_PROOF_OF_SHIPMENT_OR_DELIVERY
Seller provided invalid proof of shipment since it lacks the correct shipping address.
INVALID_PROOF_ITEM_RETURNED_TO_SENDER
Seller provided invalid proof of shipment which shows the item was returned back to the sender.
DELIVERED_WITHOUT_REQUIRED_SIGNATURE_IN_PROOF_OF_DELIVERY
Proof of delivery provided by the seller is invalid since it is missing the required signature.
NO_SHIPMENT_TRACKING_PROVIDED_IN_PROOF_OF_DELIVERY
Proof of delivery provided by the seller is invalid since since no shipment tracking is provided.
OTHER_ISSUE_WITH_PROOF_OF_SHIPMENT_OR_DELIVERY
Seller provided invalid proof of shipment or delivery.
INSUFFICIENT_EVIDENCE_PROVIDED
Seller did not provide any sufficient evidence.
EVIDENCE_CANNOT_BE_LINKED_TO_TRANSACTION
Evidence provided by the seller is invalid since it could not be linked to the transaction.
EVIDENCE_DOES_NOT_SHOW_FULFILLMENT_OR_CUSTOMER_BENEFIT
Evidence provided by the seller does not demonstrate fulfillment or customer benefit.
SELLER_SHIPPED_OR_FULFILLED_BEYOND_ALLOWED_PERIOD
Order was shipped two days after the dispute was filed, making the evidence invalid.
ITEM_INELIGIBLE_FOR_SELLER_PROTECTION
Item does not meet the requirements for seller protection.
EVIDENCE_DOES_NOT_SHOW_SERVICE_COMPLETED
The evidence provided by the seller does not show that the service was completed as per the service agreement.
VALID_RETURN_SHIPMENT_PROOF
Buyer provided evidence that the item was shipped back for return.
ITEM_EMPTY_BOX
The item sent to the buyer was an empty box.
ITEM_UNUSABLE
The item sent to the buyer was unusable.
ITEM_MISSING_QUANTITY_OR_QUALITY
The item sent to the buyer was missing in quality or quantity.
REFUND_AMOUNT_MISMATCH
The refund amount promised does not match the actual refunded amount.
DUPLICATE_PAYMENT
Multiple payments were processed for the same transaction.
SELLER_PROMISED_REFUND_NOT_ISSUED
The evidence indicates seller promised refund to the buyer but did not issue it.
CUSTOMER_CHARGED_INCORRECT_AMOUNT
The evidence indicates customer was charged an incorrect amount.
DUPLICATE_PAYMENT_BY_OTHER_MEANS
The evidence indicates that the customer was charged multiple times for the same order through different payment methods.
GOODWILL_PAYOUT
Seller did not provide enough evidence. Since the account is in good standing, it will not be debited for the disputed amount this time. The seller has been advised to review the previous
adjudication
under
adjudications
returned as part of the
dispute details
API response for a detailed explanation of why the evidence did not meet requirements.
amount_refunded
object
(
Money
)
The amount that either the merchant or PayPal refunds the customer.
asset_refunded
object
(
Cryptocurrency
)
The asset that either the merchant or PayPal refunds the customer.
Copy
Expand all
Collapse all
{
"outcome_code"
:
"RESOLVED_BUYER_FAVOUR"
,
"outcome_reason"
:
"AMOUNT_DIFFERENCE_EXPECTED_DUE_TO_FEES"
,
"amount_refunded"
:
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
"asset_refunded"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
}
dispute_outcome_code
The outcome of a resolved dispute.
string
(
dispute_outcome_code
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The outcome of a resolved dispute.
Enum Value
Description
RESOLVED_BUYER_FAVOUR
The dispute was resolved in the customer's favor.
RESOLVED_SELLER_FAVOUR
The dispute was resolved in the merchant's favor.
RESOLVED_WITH_PAYOUT
PayPal provided the merchant or customer with protection and the case is resolved.
CANCELED_BY_BUYER
The customer canceled the dispute.
ACCEPTED
DEPRECATED. PayPal accepted the dispute.
DENIED
DEPRECATED. PayPal denied the dispute.
NONE
A dispute was created for the same transaction ID, and the previous dispute was closed without any decision.
Copy
"RESOLVED_BUYER_FAVOUR"
dispute_search
An array of disputes. Includes links that enable you to navigate through the response.
items
Array of
objects
(
dispute_info
)
[ 1 .. 100 ] items
An array of disputes that match the filter criteria. Sorted in latest to earliest creation time order.
links
Array of
objects
(
Link Description
)
[ 1 .. 10 ] items
An array of request-related
HATEOAS links
.
Copy
Expand all
Collapse all
{
"items"
:
[
{
"dispute_id"
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
"stringstringstringst"
,
"update_time"
:
"stringstringstringst"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"status"
:
"OPEN"
,
"dispute_state"
:
"OPEN_INQUIRIES"
,
"dispute_amount"
:
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
"dispute_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"dispute_life_cycle_stage"
:
"INQUIRY"
,
"dispute_channel"
:
"INTERNAL"
,
"buyer_response_due_date"
:
"stringstringstringst"
,
"seller_response_due_date"
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
dispute_source
The dispute source through which customer initiated the dispute.
string
(
dispute_source
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The dispute source through which customer initiated the dispute.
Enum Value
Description
EMAIL
The dispute is initiated through a email communication.
WEB
The dispute is filed directly on paypal website.
CHAT
The dispute is initiated through a chat communication.
IVR
The dispute is initiated through automated phone system.
PHONE
The dispute is initiated through a phone call from user.
MOBILE_APP
The dispute is filed directly on paypal application on mobile.
MOBILE_WEB
The dispute is filed directly on paypal mobile web page.
API
The dispute is filed directly through API request.
Copy
"EMAIL"
dispute_state
The user specific state of the dispute, could vary between parties during the dispute lifecycle.
string
(
dispute_state
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The user specific state of the dispute, could vary between parties during the dispute lifecycle.
Enum Value
Description
OPEN_INQUIRIES
The dispute is open.
REQUIRED_ACTION
The dispute is waiting for a response.
REQUIRED_OTHER_PARTY_ACTION
The dispute is waiting for a response from other party.
UNDER_PAYPAL_REVIEW
The dispute is under review with PayPal.
APPEALABLE
The dispute can be appealed.
RESOLVED
The dispute is resolved.
Copy
"OPEN_INQUIRIES"
document
An uploaded document as a binary object that supports a dispute.
name
string
[ 1 .. 2000 ] characters
^[A-Za-z0-9-_,\s]+[.]{1}[A-Za-z]+$
The document name.
url
string
<
uri
>
The downloadable URL for the document for which the client has access.
Note:
Document download may require some configuration setup and available as a limited release at this time. For more information, reach out to your PayPal account manager.
.
Copy
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
duplication_transaction
The duplicate transaction details.
received_duplicate
boolean
If
true
, indicates that a duplicate transaction was received.
original_transaction
object
(
transaction_info
)
The transaction details for the original transaction, when the dispute reason is
DUPLICATE_TRANSACTION
. Currently, contains only the date and amount.
Copy
Expand all
Collapse all
{
"received_duplicate"
:
true
,
"original_transaction"
:
{
"buyer_transaction_id"
:
"string"
,
"seller_transaction_id"
:
"string"
,
"reference_id"
:
"string"
,
"transaction_status"
:
"COMPLETED"
,
"invoice_number"
:
"string"
,
"custom"
:
"string"
,
"items"
:
[
{
"item_id"
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
"item_quantity"
:
"string"
,
"partner_transaction_id"
:
"string"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"notes"
:
"string"
,
"item_type"
:
"PRODUCT"
,
"dispute_amount"
:
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
"create_time"
:
"stringstringstringst"
,
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
"gross_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"buyer"
:
{
"name"
:
"string"
}
,
"seller"
:
{
"merchant_id"
:
"string"
,
"name"
:
"string"
,
"email"
:
"string"
}
}
}
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
escalate
A merchant request to escalate a dispute, by ID, to a PayPal claim.
note
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The notes about the escalation of the dispute to a claim.
Copy
{
"note"
:
"string"
}
escalate_response
The response for escalate action.
links
Array of
objects
(
Link Description
)
[ 1 .. 10 ] items
An array of request-related
HATEOAS links
.
Copy
Expand all
Collapse all
{
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
evidence
A merchant- or customer-submitted evidence document. evidence_info is expected for PROOF_OF_FULFILLMENT,PROOF_OF_REFUND and PROOF_OF_RETURN evidence types. documents and notes can be given for rest of the evidence types.
evidence_type
string
(
evidence_type
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The evidence type.
Enum Value
Description
PROOF_OF_FULFILLMENT
Proof of fulfillment should be a copy of the actual shipping label on the package that shows the destination address and the shipping company's stamp to verify the shipment date.
PROOF_OF_REFUND
Proof of refund issued to the buyer
PROOF_OF_DELIVERY_SIGNATURE
Proof of delivery signature.
PROOF_OF_RECEIPT_COPY
Copy of original receipt or invoice.
RETURN_POLICY
Copy of terms and conditions,contract or store return policy
BILLING_AGREEMENT
Copy of billing agreement.
PROOF_OF_RESHIPMENT
Proof of reshipment should be a copy of the actual shipping label on the package that shows the destination address and the shipping company's stamp to verify the reshipment date.
ITEM_DESCRIPTION
A copy of the original description of the item or service
POLICE_REPORT
Copy of the police report filed.
AFFIDAVIT
More information has to be provided about the claim using the affidavit.
PAID_WITH_OTHER_METHOD
Document showing item/service was paid by another payment method.
COPY_OF_CONTRACT
Copy of contract if applicable.
TERMINAL_ATM_RECEIPT
Copy of terminal/ATM receipt.
PRICE_DIFFERENCE_REASON
Explanation of what the price difference is related to (increased tip amount, shipping charges, taxes, etc).
SOURCE_CONVERSION_RATE
Source of expected conversion rate or fee.
BANK_STATEMENT
Bank/Credit statement showing withdrawal transaction.
CREDIT_DUE_REASON
The credit due reason.
REQUEST_CREDIT_RECEIPT
The request credit receipt.
PROOF_OF_RETURN
Proof of shipment or postage that shows you returned this item to your seller and should be a copy of the actual shipping label used.
CREATE
Additional evidence information during case creation.
CHANGE_REASON
The evidence related to the reason change.
PROOF_OF_REFUND_OUTSIDE_PAYPAL
Document should show that the seller issued a refund outside Paypal.
RECEIPT_OF_MERCHANDISE
Check with buyer if item Delivered (seller provided Proof of Shipping)
CUSTOMS_DOCUMENT
Document confirming that the item has been confiscated.
CUSTOMS_FEE_RECEIPT
Custom fees receipt paid by the buyer
INFORMATION_ON_RESOLUTION
Any resolution reached with the seller should be communicated to PayPal.
ADDITIONAL_INFORMATION_OF_ITEM
Any additional information of the item purchased.
DETAILS_OF_PURCHASE
Specific details of a purchase made under a particular transaction has to be given.
PROOF_OF_SIGNIFICANT_DIFFERENCE
More information required on how the item was damaged or was significantly different from the item advertised.
PROOF_OF_SOFTWARE_OR_SERVICE_NOT_AS_DESCRIBED
Any screenshot or download/usage log showing that the software or service was unavailable or non-functional.
PROOF_OF_CONFISCATION
Documentation from a third party or organization that evaluated this item that confirms they confiscated it.
PROOF_OF_DAMAGE
Documentation supporting the claim that the item is damaged.
COPY_OF_LAW_ENFORCEMENT_AGENCY_REPORT
Report filed with a law enforcement agency or government organization. Examples of such agencies are -  Internet Crime Complaint Center (
www.ic3.gov
), state Consumer Protection office, state police or a Federal law enforcement agency such as the FBI or Postal Inspection Service.
ADDITIONAL_PROOF_OF_SHIPMENT
Additional proof of shipment  such as a packing list, detailed invoice, or shipping manifest to confirm that all items have been shipped. Include carrier name and tracking number if available.
PROOF_OF_DENIAL_BY_CARRIER
Documentation from the carrier should confirm the reason why they refuse to ship the item in question and the extent of the original damage.
THIRDPARTY_PROOF_FOR_DAMAGE_OR_SIGNIFICANT_DIFFERENCE
Proof should be provided by an unbiased third-party, such as a dealer, appraiser or another individual or organisation that's qualified in the area of the item in question (other than yourself), and detail the extent of the damage or clearly explain how the item received significantly differs from the item advertised.
VALID_SUPPORTING_DOCUMENT
The document you have provided doesn't support your claim that the item is Significantly Not as Described. Please provide a document to clearly show how the item received significantly differs from the item advertised.
LEGIBLE_SUPPORTING_DOCUMENT
The document you have provided is illegible, unclear, or too dark to read.  Please provide a document that is legible and clear to read.
RETURN_TRACKING_INFORMATION
Online tracking information for remaining items that have to be shipped to the seller.
DELIVERY_RECEIPT
Confirmation that the item has been received.
PROOF_OF_INSTORE_RECEIPT
In-store receipt or online verification should clearly show that the buyer picked up the item.
ADDITIONAL_TRACKING_INFORMATION
Tracking information should include the carrier name,  online tracking number and the website where the shipment can be tracked.
PROOF_OF_SHIPMENT_POSTAGE
Proof of shipment or postage should be a copy of the actual shipping label on the package that shows the destination address and the carrier's stamp to verify the shipment date.
ONLINE_TRACKING_INFORMATION
Online tracking information to confirm delivery of item.
PROOF_OF_INSTORE_REFUND
Proof should be an in-store refund receipt or company documentation that clearly shows a completed refund for the transaction.
PROOF_FOR_SOFTWARE_OR_SERVICE_DELIVERED
Proof should be compelling evidence to prove that the item or service was as described  and was delivered to the buyer. Include information such as transaction ID, invoice ID, name or email to associate the evidence with the buyer along with date and time of the delivery.
RETURN_ADDRESS_FOR_SHIPPING
Return address is required for the buyer to ship  the merchandise back to the seller.
COPY_OF_THE_EPARCEL_MANIFEST
To validate a claim,  a copy of the eparcel manifest showing the buyer's address from Australia Post is required.
COPY_OF_SHIPPING_MANIFEST
The shipping manifest must show the buyer's address and can be obtained from the carrier.
APPEAL_AFFIDAVIT
Appeal affidavit is needed to make an appeal for any case outcome.
RECEIPT_OF_REPLACEMENT
Check with buyer if the replacement of the item sent by the seller was received
COPY_OF_DRIVERS_LICENSE
Need Copy of Drivers license.
ACCOUNT_CHANGE_INFORMATION
Additional Details about how account was accessed/what was changed.
DELIVERY_ADDRESS
Address where item was supposed to be delivered.
CONFIRMATION_OF_RESOLUTION
Confirmation that item was received and issue resolved.
MERCHANT_RESPONSE
Copy of merchant's response when the resolution was attempted.
PERMISSION_DESCRIPTION
A Detailed description about the account or card level permission given to another person.
STATUS_OF_MERCHANDISE
Details of the merchandise's current location.
LOST_CARD_DETAILS
Details of where and when the card was lost/stolen?.
LAST_VALID_TRANSACTION_DETAILS
Details of the last valid transaction made on the card.
ADDITIONAL_PROOF_OF_RETURN
Document to confirm that the item to be returned to the seller has been shipped.
DECLARATION
Signed declaration about the information provided.
PROOF_OF_MISSING_ITEMS
Image of open box with returned items and shipping label clearly visible.
PROOF_OF_EMPTY_PACKAGE_OR_DIFFERENT_ITEM
Image of empty box or returned items that are different from what were expected and shipping label clearly visible.
PROOF_OF_ITEM_NOT_RECEIVED
Any proof about the non receipt of the item, such as screenshot of tracking info.
ORDER_DETAILS
Order details or photos of the item/service/booking/digital download available on the website.
LISTING_URL
The website URLs of the item/service/booking/digital download.
SHIPPING_INSURANCE
Insurance information of the shipped item.
BUYER_RESPONSE
Copy of the buyer response or any other document showing buyer's understanding of the item/service/booking/digital download purchased.
PHOTOS_OF_SHIPPED_ITEM
Photos of the item that were shipped to the buyer.
OTHER
Other.
CANCELLATION_DETAILS
Cancellation details information, for example- cancellation date, cancellation number.
MERCHANT_CONTACT_DETAILS
Merchant contacted details information, for example- merchant contacted time, mode of contacting.
ITEM_DETAILS
Item related details information, for example- expected delivery date.
CORRECT_RECIPIENT_INFORMATION
Proof of the correct recipient name, email or phone.
EXPLANATION_OF_FUNDS_NOT_DELIVERED
Details on why the funds were not delivered to the correct recipient.
CONFIRMATION_OF_RECALL
Details of the recall confirmation from the customer.
COMMUNICATION_WITH_THE_SENDER
Messages or conversations exchanged with the sender.
PAYMENT_REASON
The reason or intent behind making the payment.
PROOF_OF_EXPECTED_DELIVERY_DATE
Any correspondence or documentation that provides the buyer with a proof of the anticipated date when a purchased item will be delivered.
DELIVERY_DELAY_COMMUNICATION
Any notification sent to the customer informing them that the expected delivery of an item has been delayed.
ADDITIONAL_SCAM_DETAILS
Any other details that suggest suspicious or fraudulent activity.
REASON_FOR_LATE_OPENING
Explanation for delayed reporting or response to the issue.
COMMUNICATION_WITH_THE_RECIPIENT
Messages or conversations exchanged with the recipient.
EFFORTS_TO_VERIFY_RECIPIENT
Steps taken to confirm the recipient’s identity or legitimacy.
documents
Array of
objects
(
document
)
[ 1 .. 100 ] items
An array of evidence documents.
notes
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
Any evidence-related notes.
source
string
[ 1 .. 255 ] characters
^[A-Z_]+$
The source of the evidence.
Enum Value
Description
REQUESTED_FROM_BUYER
PayPal requested evidence from the customer.
REQUESTED_FROM_SELLER
PayPal requested evidence from the merchant.
SUBMITTED_BY_BUYER
Evidence was submitted by the customer.
SUBMITTED_BY_SELLER
Evidence was submitted by the merchant.
SUBMITTED_BY_PARTNER
Evidence was submitted by the partner.
item_id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9]+$
The item ID. If the merchant provides multiple pieces of evidence and the transaction has multiple item IDs, the merchant can use this value to associate a piece of evidence with an item ID.
evidence_info
object
(
evidence_info
)
The evidence-related information.
date
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
The date and time when the evidence was received, in
Internet date and time format
.
item_type
string
(
item_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The item type for which the evidence is requested or submitted.
Enum Value
Description
PRODUCT
The product has an issue.
SERVICE
The service has an issue.
BOOKING
The booking has an issue.
DIGITAL_DOWNLOAD
The digital download has an issue.
action_info
object
(
action_info
)
The action details for the information. Includes additional information such as the action for which the evidence was requested/submitted, and whether the evidence is mandatory for the corresponding action.
dispute_life_cycle_stage
string
(
dispute_lifecycle_stage
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The dispute life cycle stage for the evidence.
Enum Value
Description
INQUIRY
A customer and merchant interact in an attempt to resolve a dispute without escalation to PayPal. Occurs when the customer:
Has not received goods or a service.
Reports that the received goods or service are not as described.
Needs more details, such as a copy of the transaction or a receipt.
CHARGEBACK
A customer or merchant escalates an inquiry to a claim, which authorizes PayPal to investigate the case and make a determination. Occurs only when the dispute channel is
INTERNAL
. This stage is a PayPal dispute lifecycle stage and not a credit card or debit card chargeback. All notes that the customer sends in this stage are visible to PayPal agents only. The customer must wait for PayPal’s response before the customer can take further action. In this stage, PayPal shares dispute details with the merchant, who can complete one of these actions:
Accept the claim.
Submit evidence to challenge the claim.
Make an offer to the customer to resolve the claim.
PRE_ARBITRATION
The first appeal stage for merchants. A merchant can appeal a chargeback if PayPal's decision is not in the merchant's favor. If the merchant does not appeal within the appeal period, PayPal considers the case resolved.
ARBITRATION
The second appeal stage for merchants. A merchant can appeal a dispute for a second time if the first appeal was denied. If the merchant does not appeal within the appeal period, the case returns to a resolved status in pre-arbitration stage.
Copy
Expand all
Collapse all
{
"evidence_type"
:
"PROOF_OF_FULFILLMENT"
,
"documents"
:
[
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
]
,
"notes"
:
"string"
,
"source"
:
"REQUESTED_FROM_BUYER"
,
"item_id"
:
"string"
,
"evidence_info"
:
{
"tracking_info"
:
[
{
"carrier_name"
:
"UPS"
,
"carrier_name_other"
:
"string"
,
"tracking_url"
:
"
http://example.com
"
,
"tracking_number"
:
"string"
}
]
,
"refund_ids"
:
[
"string"
]
}
,
"date"
:
"stringstringstringst"
,
"item_type"
:
"PRODUCT"
,
"action_info"
:
{
"action"
:
"ACKNOWLEDGE_RETURN_ITEM"
,
"response_option"
:
"string"
,
"mandatory"
:
true
}
,
"dispute_life_cycle_stage"
:
"INQUIRY"
}
evidence_info
The evidence-related information.
tracking_info
Array of
objects
(
response_tracking_info
)
[ 1 .. 10 ] items
An array of relevant tracking information for the transaction involved in this dispute.
refund_ids
Array of
strings
[ 1 .. 100 ] items
An array of refund IDs for the transaction involved in this dispute.
Copy
Expand all
Collapse all
{
"tracking_info"
:
[
{
"carrier_name"
:
"UPS"
,
"carrier_name_other"
:
"string"
,
"tracking_url"
:
"
http://example.com
"
,
"tracking_number"
:
"string"
}
]
,
"refund_ids"
:
[
"string"
]
}
evidence_type
The evidence type.
string
(
evidence_type
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The evidence type.
Enum Value
Description
PROOF_OF_FULFILLMENT
Proof of fulfillment should be a copy of the actual shipping label on the package that shows the destination address and the shipping company's stamp to verify the shipment date.
PROOF_OF_REFUND
Proof of refund issued to the buyer
PROOF_OF_DELIVERY_SIGNATURE
Proof of delivery signature.
PROOF_OF_RECEIPT_COPY
Copy of original receipt or invoice.
RETURN_POLICY
Copy of terms and conditions,contract or store return policy
BILLING_AGREEMENT
Copy of billing agreement.
PROOF_OF_RESHIPMENT
Proof of reshipment should be a copy of the actual shipping label on the package that shows the destination address and the shipping company's stamp to verify the reshipment date.
ITEM_DESCRIPTION
A copy of the original description of the item or service
POLICE_REPORT
Copy of the police report filed.
AFFIDAVIT
More information has to be provided about the claim using the affidavit.
PAID_WITH_OTHER_METHOD
Document showing item/service was paid by another payment method.
COPY_OF_CONTRACT
Copy of contract if applicable.
TERMINAL_ATM_RECEIPT
Copy of terminal/ATM receipt.
PRICE_DIFFERENCE_REASON
Explanation of what the price difference is related to (increased tip amount, shipping charges, taxes, etc).
SOURCE_CONVERSION_RATE
Source of expected conversion rate or fee.
BANK_STATEMENT
Bank/Credit statement showing withdrawal transaction.
CREDIT_DUE_REASON
The credit due reason.
REQUEST_CREDIT_RECEIPT
The request credit receipt.
PROOF_OF_RETURN
Proof of shipment or postage that shows you returned this item to your seller and should be a copy of the actual shipping label used.
CREATE
Additional evidence information during case creation.
CHANGE_REASON
The evidence related to the reason change.
PROOF_OF_REFUND_OUTSIDE_PAYPAL
Document should show that the seller issued a refund outside Paypal.
RECEIPT_OF_MERCHANDISE
Check with buyer if item Delivered (seller provided Proof of Shipping)
CUSTOMS_DOCUMENT
Document confirming that the item has been confiscated.
CUSTOMS_FEE_RECEIPT
Custom fees receipt paid by the buyer
INFORMATION_ON_RESOLUTION
Any resolution reached with the seller should be communicated to PayPal.
ADDITIONAL_INFORMATION_OF_ITEM
Any additional information of the item purchased.
DETAILS_OF_PURCHASE
Specific details of a purchase made under a particular transaction has to be given.
PROOF_OF_SIGNIFICANT_DIFFERENCE
More information required on how the item was damaged or was significantly different from the item advertised.
PROOF_OF_SOFTWARE_OR_SERVICE_NOT_AS_DESCRIBED
Any screenshot or download/usage log showing that the software or service was unavailable or non-functional.
PROOF_OF_CONFISCATION
Documentation from a third party or organization that evaluated this item that confirms they confiscated it.
PROOF_OF_DAMAGE
Documentation supporting the claim that the item is damaged.
COPY_OF_LAW_ENFORCEMENT_AGENCY_REPORT
Report filed with a law enforcement agency or government organization. Examples of such agencies are -  Internet Crime Complaint Center (
www.ic3.gov
), state Consumer Protection office, state police or a Federal law enforcement agency such as the FBI or Postal Inspection Service.
ADDITIONAL_PROOF_OF_SHIPMENT
Additional proof of shipment  such as a packing list, detailed invoice, or shipping manifest to confirm that all items have been shipped. Include carrier name and tracking number if available.
PROOF_OF_DENIAL_BY_CARRIER
Documentation from the carrier should confirm the reason why they refuse to ship the item in question and the extent of the original damage.
THIRDPARTY_PROOF_FOR_DAMAGE_OR_SIGNIFICANT_DIFFERENCE
Proof should be provided by an unbiased third-party, such as a dealer, appraiser or another individual or organisation that's qualified in the area of the item in question (other than yourself), and detail the extent of the damage or clearly explain how the item received significantly differs from the item advertised.
VALID_SUPPORTING_DOCUMENT
The document you have provided doesn't support your claim that the item is Significantly Not as Described. Please provide a document to clearly show how the item received significantly differs from the item advertised.
LEGIBLE_SUPPORTING_DOCUMENT
The document you have provided is illegible, unclear, or too dark to read.  Please provide a document that is legible and clear to read.
RETURN_TRACKING_INFORMATION
Online tracking information for remaining items that have to be shipped to the seller.
DELIVERY_RECEIPT
Confirmation that the item has been received.
PROOF_OF_INSTORE_RECEIPT
In-store receipt or online verification should clearly show that the buyer picked up the item.
ADDITIONAL_TRACKING_INFORMATION
Tracking information should include the carrier name,  online tracking number and the website where the shipment can be tracked.
PROOF_OF_SHIPMENT_POSTAGE
Proof of shipment or postage should be a copy of the actual shipping label on the package that shows the destination address and the carrier's stamp to verify the shipment date.
ONLINE_TRACKING_INFORMATION
Online tracking information to confirm delivery of item.
PROOF_OF_INSTORE_REFUND
Proof should be an in-store refund receipt or company documentation that clearly shows a completed refund for the transaction.
PROOF_FOR_SOFTWARE_OR_SERVICE_DELIVERED
Proof should be compelling evidence to prove that the item or service was as described  and was delivered to the buyer. Include information such as transaction ID, invoice ID, name or email to associate the evidence with the buyer along with date and time of the delivery.
RETURN_ADDRESS_FOR_SHIPPING
Return address is required for the buyer to ship  the merchandise back to the seller.
COPY_OF_THE_EPARCEL_MANIFEST
To validate a claim,  a copy of the eparcel manifest showing the buyer's address from Australia Post is required.
COPY_OF_SHIPPING_MANIFEST
The shipping manifest must show the buyer's address and can be obtained from the carrier.
APPEAL_AFFIDAVIT
Appeal affidavit is needed to make an appeal for any case outcome.
RECEIPT_OF_REPLACEMENT
Check with buyer if the replacement of the item sent by the seller was received
COPY_OF_DRIVERS_LICENSE
Need Copy of Drivers license.
ACCOUNT_CHANGE_INFORMATION
Additional Details about how account was accessed/what was changed.
DELIVERY_ADDRESS
Address where item was supposed to be delivered.
CONFIRMATION_OF_RESOLUTION
Confirmation that item was received and issue resolved.
MERCHANT_RESPONSE
Copy of merchant's response when the resolution was attempted.
PERMISSION_DESCRIPTION
A Detailed description about the account or card level permission given to another person.
STATUS_OF_MERCHANDISE
Details of the merchandise's current location.
LOST_CARD_DETAILS
Details of where and when the card was lost/stolen?.
LAST_VALID_TRANSACTION_DETAILS
Details of the last valid transaction made on the card.
ADDITIONAL_PROOF_OF_RETURN
Document to confirm that the item to be returned to the seller has been shipped.
DECLARATION
Signed declaration about the information provided.
PROOF_OF_MISSING_ITEMS
Image of open box with returned items and shipping label clearly visible.
PROOF_OF_EMPTY_PACKAGE_OR_DIFFERENT_ITEM
Image of empty box or returned items that are different from what were expected and shipping label clearly visible.
PROOF_OF_ITEM_NOT_RECEIVED
Any proof about the non receipt of the item, such as screenshot of tracking info.
ORDER_DETAILS
Order details or photos of the item/service/booking/digital download available on the website.
LISTING_URL
The website URLs of the item/service/booking/digital download.
SHIPPING_INSURANCE
Insurance information of the shipped item.
BUYER_RESPONSE
Copy of the buyer response or any other document showing buyer's understanding of the item/service/booking/digital download purchased.
PHOTOS_OF_SHIPPED_ITEM
Photos of the item that were shipped to the buyer.
OTHER
Other.
CANCELLATION_DETAILS
Cancellation details information, for example- cancellation date, cancellation number.
MERCHANT_CONTACT_DETAILS
Merchant contacted details information, for example- merchant contacted time, mode of contacting.
ITEM_DETAILS
Item related details information, for example- expected delivery date.
CORRECT_RECIPIENT_INFORMATION
Proof of the correct recipient name, email or phone.
EXPLANATION_OF_FUNDS_NOT_DELIVERED
Details on why the funds were not delivered to the correct recipient.
CONFIRMATION_OF_RECALL
Details of the recall confirmation from the customer.
COMMUNICATION_WITH_THE_SENDER
Messages or conversations exchanged with the sender.
PAYMENT_REASON
The reason or intent behind making the payment.
PROOF_OF_EXPECTED_DELIVERY_DATE
Any correspondence or documentation that provides the buyer with a proof of the anticipated date when a purchased item will be delivered.
DELIVERY_DELAY_COMMUNICATION
Any notification sent to the customer informing them that the expected delivery of an item has been delayed.
ADDITIONAL_SCAM_DETAILS
Any other details that suggest suspicious or fraudulent activity.
REASON_FOR_LATE_OPENING
Explanation for delayed reporting or response to the issue.
COMMUNICATION_WITH_THE_RECIPIENT
Messages or conversations exchanged with the recipient.
EFFORTS_TO_VERIFY_RECIPIENT
Steps taken to confirm the recipient’s identity or legitimacy.
Copy
"PROOF_OF_FULFILLMENT"
evidences
A merchant or customer request to provide evidence for a dispute.
evidences
Array of
objects
(
evidence
)
[ 0 .. 100 ] items
An array of evidences for the dispute.
return_shipping_address
object
(
Portable Postal Address (Medium-Grained)
)
The return address for the item.
Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason..
return_shipping_address_info
object
(
Return shipping address information
)
Merchant provided information regarding return shipping address.
Copy
Expand all
Collapse all
{
"evidences"
:
[
{
"evidence_type"
:
"PROOF_OF_FULFILLMENT"
,
"documents"
:
[
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
]
,
"notes"
:
"string"
,
"source"
:
"REQUESTED_FROM_BUYER"
,
"item_id"
:
"string"
,
"evidence_info"
:
{
"tracking_info"
:
[
{
"carrier_name"
:
"UPS"
,
"carrier_name_other"
:
"string"
,
"tracking_url"
:
"
http://example.com
"
,
"tracking_number"
:
"string"
}
]
,
"refund_ids"
:
[
"string"
]
}
,
"date"
:
"stringstringstringst"
,
"item_type"
:
"PRODUCT"
,
"action_info"
:
{
"action"
:
"ACKNOWLEDGE_RETURN_ITEM"
,
"response_option"
:
"string"
,
"mandatory"
:
true
}
,
"dispute_life_cycle_stage"
:
"INQUIRY"
}
]
,
"return_shipping_address"
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
"return_shipping_address_info"
:
{
"save_to_profile"
:
true
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
extensions
The extended properties for the dispute. Includes additional information for a dispute category, such as billing disputes, the original transaction ID, and the correct amount.
merchant_contacted
boolean
Indicates that the merchant was contacted.
buyer_contacted_channel
string
[ 1 .. 255 ] characters
^.*$
The channel through which the buyer contacted the partner to file a dispute. Partners that allow buyers to create dispute from multiple channels can use this field to help identify which channel was used for each individual dispute.
merchant_contacted_outcome
string
(
merchant_contacted_outcome
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The outcome when the customer has contacted the merchant.
Enum Value
Description
NO_RESPONSE
The merchant did not respond to the customer.
FIXED
The merchant agreed to fix the issue but did not fix it yet.
RESPONDED
The merchant has responded.
NOT_FIXED
The merchant could not fix the issue.
merchant_contacted_time
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
The date and time when merchant was contacted.
merchant_contacted_mode
string
(
merchant_contacted_outcome
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The method used to contact the merchant.
Enum Value
Description
WEBSITE
The merchant was contacted through his website.
PHONE
The merchant was contacted through either phone or fax.
EMAIL
The merchant was contacted through either email or text message.
WRITTEN
The merchant was contacted through a written communication.
IN_PERSON
The merchant was contacted in person.
buyer_contacted_time
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
The date and time when the buyer contacted the partner to file a dispute, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
billing_dispute_properties
object
(
billing_disputes_properties
)
The billing issue details.
merchandize_dispute_properties
object
(
merchandise_dispute_properties
)
The customer-provided merchandise issue details for the dispute.
reported_source
string
(
dispute_source
)
[ 1 .. 255 ] characters
^[A-Z0-9_]+$
The dispute source through which customer initiated the dispute.
Enum Value
Description
EMAIL
The dispute is initiated through a email communication.
WEB
The dispute is filed directly on paypal website.
CHAT
The dispute is initiated through a chat communication.
IVR
The dispute is initiated through automated phone system.
PHONE
The dispute is initiated through a phone call from user.
MOBILE_APP
The dispute is filed directly on paypal application on mobile.
MOBILE_WEB
The dispute is filed directly on paypal mobile web page.
API
The dispute is filed directly through API request.
Copy
Expand all
Collapse all
{
"merchant_contacted"
:
true
,
"buyer_contacted_channel"
:
"string"
,
"merchant_contacted_outcome"
:
"NO_RESPONSE"
,
"merchant_contacted_time"
:
"string"
,
"merchant_contacted_mode"
:
"WEBSITE"
,
"buyer_contacted_time"
:
"string"
,
"billing_dispute_properties"
:
{
"duplicate_transaction"
:
{
"received_duplicate"
:
true
,
"original_transaction"
:
{
"buyer_transaction_id"
:
"string"
,
"seller_transaction_id"
:
"string"
,
"reference_id"
:
"string"
,
"transaction_status"
:
"COMPLETED"
,
"invoice_number"
:
"string"
,
"custom"
:
"string"
,
"items"
:
[
{
"item_id"
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
"item_quantity"
:
"string"
,
"partner_transaction_id"
:
"string"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"notes"
:
"string"
,
"item_type"
:
"PRODUCT"
,
"dispute_amount"
:
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
"create_time"
:
"stringstringstringst"
,
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
"gross_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"buyer"
:
{
"name"
:
"string"
}
,
"seller"
:
{
"merchant_id"
:
"string"
,
"name"
:
"string"
,
"email"
:
"string"
}
}
}
,
"incorrect_transaction_amount"
:
{
"correct_transaction_amount"
:
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
"correct_transaction_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"correct_transaction_time"
:
"stringstringstringst"
}
,
"payment_by_other_means"
:
{
"charge_different_from_original"
:
true
,
"received_duplicate"
:
true
,
"payment_method"
:
"CASH"
,
"payment_instrument_suffix"
:
"stri"
}
,
"credit_not_processed"
:
{
"issue_type"
:
"PRODUCT"
,
"agreed_refund_details"
:
{
"merchant_agreed_refund"
:
true
,
"merchant_agreed_refund_time"
:
"stringstringstringst"
}
,
"expected_refund"
:
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
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
,
"product_details"
:
{
"description"
:
"string"
,
"product_received"
:
"YES"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
,
"product_received_time"
:
"string"
,
"expected_delivery_date"
:
"string"
,
"return_details"
:
{
"mode"
:
"SHIPPED"
,
"receipt"
:
true
,
"return_confirmation_number"
:
"string"
,
"returned"
:
true
,
"return_time"
:
"stringstringstringst"
}
}
,
"service_details"
:
{
"description"
:
"string"
,
"service_started"
:
"YES"
,
"note"
:
"string"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
}
}
,
"canceled_recurring_billing"
:
{
"expected_refund"
:
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
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
}
}
,
"merchandize_dispute_properties"
:
{
"issue_type"
:
"PRODUCT"
,
"product_details"
:
{
"description"
:
"string"
,
"product_received"
:
"YES"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
,
"product_received_time"
:
"string"
,
"expected_delivery_date"
:
"string"
,
"return_details"
:
{
"mode"
:
"SHIPPED"
,
"receipt"
:
true
,
"return_confirmation_number"
:
"string"
,
"returned"
:
true
,
"return_time"
:
"stringstringstringst"
}
}
,
"service_details"
:
{
"description"
:
"string"
,
"service_started"
:
"YES"
,
"note"
:
"string"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
}
,
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
,
"return_shipping_address"
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
,
"reported_source"
:
"EMAIL"
}
Fee Policy
Policy that determines whether the fee needs to be charged, retained or returned while moving the money as part of dispute process.
object
(
Fee Policy
)
Policy that determines whether the fee needs to be charged, retained or returned while moving the money as part of dispute process.
Copy
{ }
fund_movement
This section contains the details about the fund movement of the parties ,time , direction and the reason for it.
party
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The affected party in the money movement.
Enum Value
Description
SELLER
The money movement is related to the seller.
BUYER
The money movement is related to the buyer.
type
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of the money movement.
Enum Value
Description
DEBIT
The money movement is a debit transaction.
CREDIT
The money movement is a credit transaction.
amount
object
(
Money
)
The amount transferred as part of the money movement.
asset
object
(
Cryptocurrency
)
The asset transferred as part of the money movement.
initiated_time
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
The date and time when the money movement was initiated, in
Internet date and time format
.
reason
string
(
fund_movement_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the fund movement.
Enum Value
Description
REVERSED_TRANSACTION_FEE
The fee amount reimbursed to the seller as part of the dispute resolution process.
DISPUTE_SETTLEMENT
The money movement is for dispute settlement.
DISPUTE_FEE
The money movement is for dispute fee which PayPal charges to sellers for facilitating the online dispute resolution process for transactions that are processed either through a buyer’s PayPal account or through a PayPal guest checkout.
CHARGEBACK_FEE
The money movement is for chargeback fee which PayPal charges to sellers for facilitating the chargeback process for transactions that are not processed either through a buyer’s PayPal account or through a guest checkout, and where the buyer pursues a chargeback for the transaction with their card issuer.
Copy
Expand all
Collapse all
{
"party"
:
"SELLER"
,
"type"
:
"DEBIT"
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
"asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"initiated_time"
:
"string"
,
"reason"
:
"REVERSED_TRANSACTION_FEE"
}
fund_movement_reason
The reason for the fund movement.
string
(
fund_movement_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the fund movement.
Enum Value
Description
REVERSED_TRANSACTION_FEE
The fee amount reimbursed to the seller as part of the dispute resolution process.
DISPUTE_SETTLEMENT
The money movement is for dispute settlement.
DISPUTE_FEE
The money movement is for dispute fee which PayPal charges to sellers for facilitating the online dispute resolution process for transactions that are processed either through a buyer’s PayPal account or through a PayPal guest checkout.
CHARGEBACK_FEE
The money movement is for chargeback fee which PayPal charges to sellers for facilitating the chargeback process for transactions that are not processed either through a buyer’s PayPal account or through a guest checkout, and where the buyer pursues a chargeback for the transaction with their card issuer.
Copy
"REVERSED_TRANSACTION_FEE"
incorrect_transaction_amount
The incorrect transaction amount details.
correct_transaction_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
correct_transaction_asset
object
(
Cryptocurrency
)
The correct asset quantity of the transaction.
correct_transaction_time
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
The date and time when the customer created the transaction, in
Internet date and time format
.
Copy
Expand all
Collapse all
{
"correct_transaction_amount"
:
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
"correct_transaction_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"correct_transaction_time"
:
"stringstringstringst"
}
item_info
The information for a purchased item in a disputed transaction.
item_id
string
[ 1 .. 255 ] characters
^.*$
The item ID. If the merchant provides multiple pieces of evidence and the transaction has multiple item IDs, the merchant can use this value to associate a piece of evidence with an item ID.
item_name
string
[ 1 .. 2000 ] characters
^.*$
The item name.
item_description
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The item description.
item_quantity
string
[ 1 .. 10 ] characters
^[1-9][0-9]{0,9}$
The count of the item in the dispute. Must be a whole number.
partner_transaction_id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9]+$
The ID of the transaction in the partner system. The partner transaction ID is returned at an item level because the partner might show different transactions for different items in the cart.
reason
string
(
reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the item-level dispute. For information about the required information for each dispute reason and associated evidence type, see
dispute reasons
.
Enum Value
Description
MERCHANDISE_OR_SERVICE_NOT_RECEIVED
The customer did not receive the merchandise or service.
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
The customer reports that the merchandise or service is not as described.
UNAUTHORISED
The customer did not authorize purchase of the merchandise or service.
CREDIT_NOT_PROCESSED
The refund or credit was not processed for the customer.
DUPLICATE_TRANSACTION
The transaction was a duplicate.
INCORRECT_AMOUNT
The customer was charged an incorrect amount.
PAYMENT_BY_OTHER_MEANS
The customer paid for the transaction through other means.
CANCELED_RECURRING_BILLING
The customer was being charged for a subscription or a recurring transaction that was canceled.
PROBLEM_WITH_REMITTANCE
A problem occurred with the remittance.
OTHER
Other.
notes
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
Any notes provided with the item.
item_type
string
(
item_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of the item which has the issue.
Enum Value
Description
PRODUCT
The product has an issue.
SERVICE
The service has an issue.
BOOKING
The booking has an issue.
DIGITAL_DOWNLOAD
The digital download has an issue.
dispute_amount
object
(
Money
)
The amount of the item in the dispute.
Copy
Expand all
Collapse all
{
"item_id"
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
"item_quantity"
:
"string"
,
"partner_transaction_id"
:
"string"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"notes"
:
"string"
,
"item_type"
:
"PRODUCT"
,
"dispute_amount"
:
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
item_type
The type of the item which has the issue.
string
(
item_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of the item which has the issue.
Enum Value
Description
PRODUCT
The product has an issue.
SERVICE
The service has an issue.
BOOKING
The booking has an issue.
DIGITAL_DOWNLOAD
The digital download has an issue.
Copy
"PRODUCT"
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
[ 0 .. 2147483647 ] characters
^[\S\s]*$
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
[ 0 .. 2147483647 ] characters
^[\S\s]*$
The media type, as defined by
RFC 2046
. Describes the link target.
encType
string
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
The schema that describes the request data.
targetSchema
object
(
Link Schema
)
The schema that describes the link target.
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
Additional Items
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
Pattern Properties
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
All Of Item
)
An array of sub-schemas. The data must validate against all sub-schemas.
anyOf
Array of
objects
(
Any Of Item
)
An array of sub-schemas. The data must validate against one or more sub-schemas.
oneOf
Array of
objects
(
One Of Item
)
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
Link
)
An array of links.
fragmentResolution
string
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
make_offer
A merchant request to make an offer to resolve a dispute.
note
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The merchant's notes about the offer.
invoice_id
string
[ 1 .. 127 ] characters
^.*$
The merchant-provided ID of the invoice for the refund. This optional value maps the refund to an invoice ID in the merchant's system.
offer_amount
object
(
Money
)
The amount proposed to resolve the dispute.
return_shipping_address
object
(
Portable Postal Address (Medium-Grained)
)
The return address for the item. Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason, especially if the refund amount is less than the dispute amount.
return_shipping_address_info
object
(
Return shipping address information
)
Merchant provided information regarding return shipping address.
offer_type
required
string
(
offer_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The merchant-proposed offer type for the dispute.
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount. Buyer acceptance is needed for partial refund offers and dispute is auto closed for full refunds. Include the
offer_amount
but omit the
return_shipping_address
parameters from the make offer request.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount and requires the customer to return the item. Include the
return_shipping_address
parameter and the
offer_amount
parameter in the make offer request.
REFUND_WITH_REPLACEMENT
The merchant must do a refund and then send a replacement item to the customer. This offer type is valid in the inquiry phase when a merchant is willing to refund a specific amount and send the replacement item. Include the
offer_amount
parameter in the make offer request.
REPLACEMENT_WITHOUT_REFUND
The merchant must send a replacement item to the customer with no additional refunds. This offer type is valid in the inquiry phase when a merchant is willing to replace the item without any refund. Omit the
offer_amount
parameter from the make offer request.
Copy
Expand all
Collapse all
{
"note"
:
"string"
,
"invoice_id"
:
"string"
,
"offer_amount"
:
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
"return_shipping_address"
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
"return_shipping_address_info"
:
{
"save_to_profile"
:
true
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
,
"offer_type"
:
"REFUND"
}
make_offer
The allowed response options when the merchant makes offer to the customer.
offer_types
Array of
strings
(
offer_type
)
[ 1 .. 10 ] items
The types of offer the merchant can offer the customer.
Items
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount. Buyer acceptance is needed for partial refund offers and dispute is auto closed for full refunds. Include the
offer_amount
but omit the
return_shipping_address
parameters from the make offer request.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount and requires the customer to return the item. Include the
return_shipping_address
parameter and the
offer_amount
parameter in the make offer request.
REFUND_WITH_REPLACEMENT
The merchant must do a refund and then send a replacement item to the customer. This offer type is valid in the inquiry phase when a merchant is willing to refund a specific amount and send the replacement item. Include the
offer_amount
parameter in the make offer request.
REPLACEMENT_WITHOUT_REFUND
The merchant must send a replacement item to the customer with no additional refunds. This offer type is valid in the inquiry phase when a merchant is willing to replace the item without any refund. Omit the
offer_amount
parameter from the make offer request.
Copy
Expand all
Collapse all
{
"offer_types"
:
[
"REFUND"
]
}
merchandise_dispute_properties
The customer-provided merchandise issue details for the dispute.
issue_type
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The issue type.
Enum Value
Description
PRODUCT
The product has an issue.
SERVICE
The service has an issue.
product_details
object
(
product_details
)
The product information.
service_details
object
(
service_details
)
The service details.
cancellation_details
object
(
cancellation_details
)
The cancellation details.
return_shipping_address
object
(
Portable Postal Address (Medium-Grained)
)
The return address for the item. Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason.
Copy
Expand all
Collapse all
{
"issue_type"
:
"PRODUCT"
,
"product_details"
:
{
"description"
:
"string"
,
"product_received"
:
"YES"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
,
"product_received_time"
:
"string"
,
"expected_delivery_date"
:
"string"
,
"return_details"
:
{
"mode"
:
"SHIPPED"
,
"receipt"
:
true
,
"return_confirmation_number"
:
"string"
,
"returned"
:
true
,
"return_time"
:
"stringstringstringst"
}
}
,
"service_details"
:
{
"description"
:
"string"
,
"service_started"
:
"YES"
,
"note"
:
"string"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
}
,
"cancellation_details"
:
{
"cancellation_number"
:
"string"
,
"cancelled"
:
true
,
"cancellation_mode"
:
"CANCELLED_PAYPAL_BILLING_AGREEMENT"
,
"cancellation_date"
:
"string"
}
,
"return_shipping_address"
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
merchant_contacted_outcome
The outcome when the customer has contacted the merchant.
string
(
merchant_contacted_outcome
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The outcome when the customer has contacted the merchant.
Enum Value
Description
NO_RESPONSE
The merchant did not respond to the customer.
FIXED
The merchant agreed to fix the issue but did not fix it yet.
RESPONDED
The merchant has responded.
NOT_FIXED
The merchant could not fix the issue.
Copy
"NO_RESPONSE"
merchant_contacted_outcome
The method used to contact the merchant.
string
(
merchant_contacted_outcome
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The method used to contact the merchant.
Enum Value
Description
WEBSITE
The merchant was contacted through his website.
PHONE
The merchant was contacted through either phone or fax.
EMAIL
The merchant was contacted through either email or text message.
WRITTEN
The merchant was contacted through a written communication.
IN_PERSON
The merchant was contacted in person.
Copy
"WEBSITE"
message
A customer- or merchant-posted message for the dispute.
posted_by
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Indicates whether the customer, merchant, or dispute arbiter posted the message.
Enum Value
Description
BUYER
The customer posted the message.
SELLER
The merchant posted the message.
ARBITER
The arbiter of the dispute posted the message.
content
string
[ 0 .. 2000 ] characters
^(.|\r?\n)*$
The message text.
documents
Array of
objects
(
document
)
[ 1 .. 10 ] items
An array of metadata for the documents which contains any additional info about the message posted.
time_posted
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
The date and time when the message was posted, in
Internet date and time format
.
Copy
Expand all
Collapse all
{
"posted_by"
:
"BUYER"
,
"content"
:
"string"
,
"documents"
:
[
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
]
,
"time_posted"
:
"stringstringstringst"
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
money_movement
The Money movement details with party.
affected_party
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The affected party in the money movement.
Enum Value
Description
SELLER
The money movement is related to the seller.
BUYER
The money movement is related to the buyer.
type
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of the money movement.
Enum Value
Description
DEBIT
The money movement is a debit transaction.
CREDIT
The money movement is a credit transaction.
amount
object
(
Money
)
The amount transferred as part of the money movement.
asset
object
(
Cryptocurrency
)
The asset transferred as part of the money movement.
initiated_time
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
The date and time when the money movement was initiated, in
Internet date and time format
.
reason
string
(
money_movement_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the money movement.
Enum Value
Description
DISPUTE_SETTLEMENT_FEE
The fee is for dispute settlement.
DISPUTE_SETTLEMENT
The money movement is for dispute settlement.
DISPUTE_FEE
The money movement is for dispute fee which PayPal charges to sellers for facilitating the online dispute resolution process for transactions that are processed either through a buyer’s PayPal account or through a PayPal guest checkout.
CHARGEBACK_FEE
The money movement is for chargeback fee which PayPal charges to sellers for facilitating the chargeback process for transactions that are not processed either through a buyer’s PayPal account or through a guest checkout, and where the buyer pursues a chargeback for the transaction with their card issuer.
Copy
Expand all
Collapse all
{
"affected_party"
:
"SELLER"
,
"type"
:
"DEBIT"
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
"asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"initiated_time"
:
"string"
,
"reason"
:
"DISPUTE_SETTLEMENT_FEE"
}
money_movement_reason
The reason for the money movement.
string
(
money_movement_reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the money movement.
Enum Value
Description
DISPUTE_SETTLEMENT_FEE
The fee is for dispute settlement.
DISPUTE_SETTLEMENT
The money movement is for dispute settlement.
DISPUTE_FEE
The money movement is for dispute fee which PayPal charges to sellers for facilitating the online dispute resolution process for transactions that are processed either through a buyer’s PayPal account or through a PayPal guest checkout.
CHARGEBACK_FEE
The money movement is for chargeback fee which PayPal charges to sellers for facilitating the chargeback process for transactions that are not processed either through a buyer’s PayPal account or through a guest checkout, and where the buyer pursues a chargeback for the transaction with their card issuer.
Copy
"DISPUTE_SETTLEMENT_FEE"
offer
The merchant-proposed offer for a dispute.
history
Array of
objects
(
offer_history
)
[ 1 .. 1000 ] items
An array of history information for an offer.
buyer_requested_amount
object
(
Money
)
The customer-requested refund for this dispute.
seller_offered_amount
object
(
Money
)
The merchant-offered refund for this dispute.
offer_type
string
(
offer_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The merchant-proposed offer type for the dispute.
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount. Buyer acceptance is needed for partial refund offers and dispute is auto closed for full refunds. Include the
offer_amount
but omit the
return_shipping_address
parameters from the make offer request.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount and requires the customer to return the item. Include the
return_shipping_address
parameter and the
offer_amount
parameter in the make offer request.
REFUND_WITH_REPLACEMENT
The merchant must do a refund and then send a replacement item to the customer. This offer type is valid in the inquiry phase when a merchant is willing to refund a specific amount and send the replacement item. Include the
offer_amount
parameter in the make offer request.
REPLACEMENT_WITHOUT_REFUND
The merchant must send a replacement item to the customer with no additional refunds. This offer type is valid in the inquiry phase when a merchant is willing to replace the item without any refund. Omit the
offer_amount
parameter from the make offer request.
Copy
Expand all
Collapse all
{
"history"
:
[
{
"actor"
:
"BUYER"
,
"event_type"
:
"PROPOSED"
,
"notes"
:
"string"
,
"offer_time"
:
"stringstringstringst"
,
"offer_type"
:
"REFUND"
,
"offer_amount"
:
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
"dispute_life_cycle_stage"
:
"INQUIRY"
}
]
,
"buyer_requested_amount"
:
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
"seller_offered_amount"
:
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
"offer_type"
:
"REFUND"
}
offer_history
The offer history.
actor
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The event-related actor.
Enum Value
Description
BUYER
The actor is the customer.
SELLER
The actor is the merchant.
event_type
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of the history event.
Enum Value
Description
PROPOSED
The merchant or customer proposed an offer.
ACCEPTED
The merchant or customer accepted the offer.
DENIED
The merchant or customer rejected the offer.
notes
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The user submitted notes.
offer_time
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
The date and time when the event occurred, in
Internet date and time format
.
offer_type
string
(
offer_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The merchant-proposed offer type for the dispute.
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount. Buyer acceptance is needed for partial refund offers and dispute is auto closed for full refunds. Include the
offer_amount
but omit the
return_shipping_address
parameters from the make offer request.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount and requires the customer to return the item. Include the
return_shipping_address
parameter and the
offer_amount
parameter in the make offer request.
REFUND_WITH_REPLACEMENT
The merchant must do a refund and then send a replacement item to the customer. This offer type is valid in the inquiry phase when a merchant is willing to refund a specific amount and send the replacement item. Include the
offer_amount
parameter in the make offer request.
REPLACEMENT_WITHOUT_REFUND
The merchant must send a replacement item to the customer with no additional refunds. This offer type is valid in the inquiry phase when a merchant is willing to replace the item without any refund. Omit the
offer_amount
parameter from the make offer request.
offer_amount
object
(
Money
)
The offer amount.
dispute_life_cycle_stage
string
(
dispute_lifecycle_stage
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The dispute life cycle stage during the offer event.
Enum Value
Description
INQUIRY
A customer and merchant interact in an attempt to resolve a dispute without escalation to PayPal. Occurs when the customer:
Has not received goods or a service.
Reports that the received goods or service are not as described.
Needs more details, such as a copy of the transaction or a receipt.
CHARGEBACK
A customer or merchant escalates an inquiry to a claim, which authorizes PayPal to investigate the case and make a determination. Occurs only when the dispute channel is
INTERNAL
. This stage is a PayPal dispute lifecycle stage and not a credit card or debit card chargeback. All notes that the customer sends in this stage are visible to PayPal agents only. The customer must wait for PayPal’s response before the customer can take further action. In this stage, PayPal shares dispute details with the merchant, who can complete one of these actions:
Accept the claim.
Submit evidence to challenge the claim.
Make an offer to the customer to resolve the claim.
PRE_ARBITRATION
The first appeal stage for merchants. A merchant can appeal a chargeback if PayPal's decision is not in the merchant's favor. If the merchant does not appeal within the appeal period, PayPal considers the case resolved.
ARBITRATION
The second appeal stage for merchants. A merchant can appeal a dispute for a second time if the first appeal was denied. If the merchant does not appeal within the appeal period, the case returns to a resolved status in pre-arbitration stage.
Copy
Expand all
Collapse all
{
"actor"
:
"BUYER"
,
"event_type"
:
"PROPOSED"
,
"notes"
:
"string"
,
"offer_time"
:
"stringstringstringst"
,
"offer_type"
:
"REFUND"
,
"offer_amount"
:
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
"dispute_life_cycle_stage"
:
"INQUIRY"
}
offer_type
The merchant-proposed offer type for the dispute.
string
(
offer_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The merchant-proposed offer type for the dispute.
Enum Value
Description
REFUND
The merchant must refund the customer without any item replacement or return. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount. Buyer acceptance is needed for partial refund offers and dispute is auto closed for full refunds. Include the
offer_amount
but omit the
return_shipping_address
parameters from the make offer request.
REFUND_WITH_RETURN
The customer must return the item to the merchant and then merchant will refund the money. This offer type is valid in the inquiry phase and occurs when a merchant is willing to refund a specific amount and requires the customer to return the item. Include the
return_shipping_address
parameter and the
offer_amount
parameter in the make offer request.
REFUND_WITH_REPLACEMENT
The merchant must do a refund and then send a replacement item to the customer. This offer type is valid in the inquiry phase when a merchant is willing to refund a specific amount and send the replacement item. Include the
offer_amount
parameter in the make offer request.
REPLACEMENT_WITHOUT_REFUND
The merchant must send a replacement item to the customer with no additional refunds. This offer type is valid in the inquiry phase when a merchant is willing to replace the item without any refund. Omit the
offer_amount
parameter from the make offer request.
Copy
"REFUND"
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
Patch Request
An array of JSON patch objects to apply partial updates to resources.
Array
([ 0 .. 32767 ] items)
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
Expand all
Collapse all
[
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
]
payment_by_other_means
The payment by other means details.
charge_different_from_original
boolean
If
true
, indicates that a charge was made that is different from the original charge.
received_duplicate
boolean
If
true
, indicates that a duplicate transaction was received.
payment_method
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The payment method.
Enum Value
Description
CASH
The payment method was cash.
CREDIT_CARD
The payment method was a credit card.
CHECK
The payment method was a check.
PAYPAL
The payment method was PayPal.
DEBIT_CARD
The payment method was a debit card.
GIFT_CARD
The payment method was a gift card.
BANK_TRANSFER
The payment method was through bank transfer.
payment_instrument_suffix
string
[ 2 .. 4 ] characters
^.*$
Last 2-4 characters of the payment instrument. For payment_method CHECK, payment_instrument_suffix entered must be of minimum length 2-4 characters. For payment_method CREDIT_CARD, DEBIT_CARD, GIFT_CARD, BANK_TRANSFER, payment_instrument_suffix entered must be of length 4.
Copy
{
"charge_different_from_original"
:
true
,
"received_duplicate"
:
true
,
"payment_method"
:
"CASH"
,
"payment_instrument_suffix"
:
"stri"
}
Phone
The phone number in its canonical international
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
product_details
The product information.
description
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The product description.
product_received
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Indicates whether the product was, or was not, received or returned.
Enum Value
Description
YES
The product was received.
NO
The product was not received.
RETURNED
The product was returned.
sub_reasons
Array of
strings
[ 1 .. 10 ] items
An array of sub-reasons for the product issue.
purchase_url
string
<
uri
>
The URL where the customer purchased the product.
product_received_time
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
The date and time when product was delivered.
expected_delivery_date
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
The expected delivery date and time of the product.
return_details
object
(
return_details
)
The return details for the product.
Copy
Expand all
Collapse all
{
"description"
:
"string"
,
"product_received"
:
"YES"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
,
"product_received_time"
:
"string"
,
"expected_delivery_date"
:
"string"
,
"return_details"
:
{
"mode"
:
"SHIPPED"
,
"receipt"
:
true
,
"return_confirmation_number"
:
"string"
,
"returned"
:
true
,
"return_time"
:
"stringstringstringst"
}
}
provide_supporting_info_request
The provide supporting information request details.
notes
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The notes that describe the defense.
Copy
{
"notes"
:
"string"
}
reason
The reason for the item-level dispute. For information about the required information for each dispute reason and associated evidence type, see
dispute reasons
.
string
(
reason
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason for the item-level dispute. For information about the required information for each dispute reason and associated evidence type, see
dispute reasons
.
Enum Value
Description
MERCHANDISE_OR_SERVICE_NOT_RECEIVED
The customer did not receive the merchandise or service.
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
The customer reports that the merchandise or service is not as described.
UNAUTHORISED
The customer did not authorize purchase of the merchandise or service.
CREDIT_NOT_PROCESSED
The refund or credit was not processed for the customer.
DUPLICATE_TRANSACTION
The transaction was a duplicate.
INCORRECT_AMOUNT
The customer was charged an incorrect amount.
PAYMENT_BY_OTHER_MEANS
The customer paid for the transaction through other means.
CANCELED_RECURRING_BILLING
The customer was being charged for a subscription or a recurring transaction that was canceled.
PROBLEM_WITH_REMITTANCE
A problem occurred with the remittance.
OTHER
Other.
Copy
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
Refund funding instrument
The details of the funding instrument.
object
(
Refund funding instrument
)
The details of the funding instrument.
Copy
{ }
Refund Transaction
The refund transaction details.
id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9]+$
The ID of the transaction for the refund or recovery.
gross_amount
object
(
Money
)
The gross amount of the refund.
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
The date and time of the refund in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
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
"create_time"
:
"stringstringstringst"
}
require_evidence_request
Sandbox only. Updates the state of a dispute, by ID, to either
WAITING_FOR_BUYER_RESPONSE
or
WAITING_FOR_SELLER_RESPONSE
. This state change enables either the customer or merchant to submit evidence for the dispute. Specify an
action
value in the JSON request body to indicate whether the state change enables the customer or merchant to submit evidence.
action
required
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The action. Indicates whether the state change enables the customer or merchant to submit evidence.
Enum Value
Description
BUYER_EVIDENCE
Changes the status of the dispute to
WAITING_FOR_BUYER_RESPONSE
.
SELLER_EVIDENCE
Changes the status of the dispute to
WAITING_FOR_SELLER_RESPONSE
.
Copy
{
"action"
:
"BUYER_EVIDENCE"
}
response_refund_details
The refund details.
transactions
Array of
objects
(
Refund Transaction
)
[ 1 .. 100 ] items
An array of refund transactions associated with the dispute.
allowed_refund_amount
object
(
Money
)
The maximum refundable amount.
Copy
Expand all
Collapse all
{
"transactions"
:
[
{
"id"
:
"string"
,
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
"create_time"
:
"stringstringstringst"
}
]
,
"allowed_refund_amount"
:
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
response_shipment_info
The shipment information.
shipment_label
required
object
(
document
)
The shipment label provided by the merchant.
tracking_info
required
object
(
response_tracking_info
)
Relevant tracking information for the transaction involved in this dispute.
Copy
Expand all
Collapse all
{
"shipment_label"
:
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
,
"tracking_info"
:
{
"carrier_name"
:
"UPS"
,
"carrier_name_other"
:
"string"
,
"tracking_url"
:
"
http://example.com
"
,
"tracking_number"
:
"string"
}
}
response_tracking_info
The tracking information.
carrier_name
required
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The name of the shipment carrier for the transaction for this dispute.
Enum Value
Description
UPS
United Parcel Service of America, Inc.
.
USPS
United States Postal Service (USPS)
.
FEDEX
Federal Express.
AIRBORNE_EXPRESS
Airborne Express.
DHL
DHL Express.
AIRSURE
Airsure.
ROYAL_MAIL
Royal Mail.
PARCELFORCE
Parcel Force.
SWIFTAIR
Swift Air.
OTHER
Other.
UK_PARCELFORCE
Parcelforce UK.
UK_ROYALMAIL_SPECIAL
Royal Mail Special Delivery UK.
UK_ROYALMAIL_RECORDED
Royal Mail Recorded UK.
UK_ROYALMAIL_INT_SIGNED
Royal Mail International Signed.
UK_ROYALMAIL_AIRSURE
Royal Mail AirSure UK.
UK_UPS
United Parcel Service UK.
UK_FEDEX
Federal Express UK.
UK_AIRBORNE_EXPRESS
Airborne Express UK.
UK_DHL
DHL UK.
UK_OTHER
Other - UK.
UK_CANNOT_PROV_TRACK
Cannot provide tracking UK.
UK_CANNOT_PROVIDE_TRACKING
Cannot provide tracking - UK.
CA_CANADA_POST
Canada Post
.
CA_PUROLATOR
Purolator Canada.
CA_CANPAR
Canpar Courier Canada.
CA_LOOMIS
Loomis Express Canada.
CA_TNT
TNT Express Canada.
TNT
TNT Global.
CA_OTHER
Other - Canada.
CA_CANNOT_PROV_TRACK
Cannot provide tracking Canada.
DE_DP_DHL_WITHIN_EUROPE
DHL Parcel Europe.
DE_DP_DHL_T_AND_T_EXPRESS
DHL T and T Express.
DE_DHL_DP_INTL_SHIPMENTS
DHL DP International shipments.
CA_CANNOT_PROVIDE_TRACKING
Cannot provide tracking - Canada.
DE_GLS
General Logistics Systems (GLS) Germany
.
DE_DPD_DELISTACK
DPD Tracking Germany.
DE_HERMES
Hermes Germany.
DE_UPS
United Parcel Service Germany.
DE_FEDEX
Federal Express Germany.
DE_TNT
TNT Germany.
DE_OTHER
Other - Germany.
FR_CHRONOPOST
Chronopost France.
FR_COLIPOSTE
Coliposte France.
FR_DHL
DHL France.
FR_UPS
United Parcel Service France.
FR_FEDEX
Federal Express France.
FR_TNT
TNT France.
FR_GLS
General Logistics Systems (GLS) France
.
FR_OTHER
Other - France.
IT_POSTE_ITALIA
Poste Italia.
IT_DHL
DHL Italy.
IT_UPS
United Parcel Service Italy.
IT_FEDEX
Federal Express Italy.
IT_TNT
TNT Italy
.
IT_GLS
General Logistics Systems (GLS) Italy
.
IT_OTHER
Other Italy.
AU_AUSTRALIA_POST_EP_PLAT
Australia Post EP Plat.
AU_AUSTRALIA_POST_EPARCEL
Australia Post Eparcel.
AU_AUSTRALIA_POST_EMS
Australia Post EMS.
AU_DHL
DHL Australia.
AU_STAR_TRACK_EXPRESS
StarTrack Express Australia.
AU_UPS
United Parcel Service Australia.
AU_FEDEX
Federal Express Australia.
AU_TNT
TNT Australia.
AU_TOLL_IPEC
Toll IPEC Australia.
AU_OTHER
Other - Australia.
FR_SUIVI
Suivi FedEx France.
IT_EBOOST_SDA
Poste Italiane SDA.
ES_CORREOS_DE_ESPANA
Correos de Espana.
ES_DHL
DHL Spain.
ES_UPS
United Parcel Service Spain.
ES_FEDEX
Federal Express Spain.
ES_TNT
TNT Spain.
ES_OTHER
Other - Spain.
AT_AUSTRIAN_POST_EMS
EMS Express Mail Service Austria.
AT_AUSTRIAN_POST_PPRIME
Austrian Post Prime.
BE_CHRONOPOST
Chronopost Belgium.
BE_TAXIPOST
Taxi Post.
CH_SWISS_POST_EXPRES
Swiss Post Express.
CH_SWISS_POST_PRIORITY
Swiss Post Priority.
CN_CHINA_POST
China Post.
HK_HONGKONG_POST
Hong Kong Post.
IE_AN_POST_SDS_EMS
Post SDS EMS Express Mail Service Ireland.
IE_AN_POST_SDS_PRIORITY
Post SDS Priority Ireland.
IE_AN_POST_REGISTERED
Post Registered Ireland.
IE_AN_POST_SWIFTPOST
Swift Post Ireland.
IN_INDIAPOST
India Post.
JP_JAPANPOST
Japan Post.
KR_KOREA_POST
Korea Post.
NL_TPG
TPG Post Netherlands.
SG_SINGPOST
SingPost Singapore.
TW_CHUNGHWA_POST
Chunghwa POST Taiwan.
CN_CHINA_POST_EMS
China Post EMS Express Mail Service.
CN_FEDEX
Federal Express China.
CN_TNT
TNT China.
CN_UPS
United Parcel Service China.
CN_OTHER
Other - China.
NL_TNT
TNT Netherlands.
NL_DHL
DHL Netherlands.
NL_UPS
United Parcel Service Netherlands.
NL_FEDEX
Federal Express Netherlands.
NL_KIALA
KIALA Netherlands.
BE_KIALA
Kiala Point Belgium.
PL_POCZTA_POLSKA
Poczta Polska.
PL_POCZTEX
Pocztex.
PL_GLS
General Logistics Systems Poland.
PL_MASTERLINK
Masterlink Poland.
PL_TNT
TNT Express Poland.
PL_DHL
DHL Portugal.
PL_UPS
United Parcel Service Poland.
PL_FEDEX
Federal Express Poland.
JP_SAGAWA_KYUU_BIN
Sagawa Kyuu Bin Japan.
JP_NITTSU_PELICAN_BIN
Nittsu Pelican Bin Japan.
JP_KURO_NEKO_YAMATO_UNYUU
Kuro Neko Yamato Unyuu Japan.
JP_TNT
TNT Japan.
JP_DHL
DHL Japan.
JP_UPS
United Parcel Service Japan.
JP_FEDEX
Federal Express Japan.
NL_PICKUP
Pickup Netherlands.
NL_INTANGIBLE
Intangible Netherlands.
NL_ABC_MAIL
ABC Mail Netherlands.
HK_FOUR_PX_EXPRESS
4PX Express Hong Kong.
HK_FLYT_EXPRESS
Flyt Express Hong Kong.
US_ASCENDIA
Ascendia US.
US_ENSENDA
Ensenda US.
US_GLOBEGISTICS
Globeistics US.
US_ONTRAC
Ontrac US.
RRDONNELLEY
RR Donnelley.
ASENDIA_UK
Asendia UK.
UK_COLLECTPLUS
CollectPlus UK
.
UK_DPD
DPD UK.
UK_HERMESWORLD
Hermesworld UK.
UK_INTERLINK_EXPRESS
Interlink Express UK.
UK_TNT
TNT UK.
UK_UK_MAIL
UK Mail
.
UK_YODEL
Yodel UK
.
BUYLOGIC
Buylogic
.
CN_EMS
EMS China.
CHINA_POST
China Post.
CNEXPS
CN Express China.
CPACKET
Cpacket.
CUCKOOEXPRESS
Cuckoo Express.
CN_EC
EC China.
CN_EMPS
EMPS China.
DE_ASENDIA
Asendia Germany.
UK_DELTEC
Deltec UK.
DE_DEUTSCHE
Deutsche Germany.
DE_DPD
DPD Germany.
RABEN_GROUP
Raben Group.
GLOBAL_TNT
TNT Global.
ADSONE
ADSone Cumulus
.
AU_AU_POST
Australian Postal Corporation
.
BONDSCOURIERS
Bonds Couriers.
COURIERS_PLEASE
Couriers Please.
DTDC_AU
DTDC Australia.
AU_FASTWAY
Fastway Australia.
HUNTER_EXPRESS
Hunter Express.
SENDLE
Sendle.
AUS_TOLL
Toll Australia.
TOLL
Toll
.
UBI_LOGISTICS
UBI Logistics.
OMNIPARCEL
Omni Parcel.
QUANTIUM
Quantium.
CN_SF_EXPRESS
SF Express China.
SEKOLOGISTICS
Seko Logistics.
HK_TAQBIN
TA-Q-BIN Parcel Hong Kong.
GB_APC
APC Overnight UK
.
CA_CANPAR_COURIER
Canpar Courier Canada.
GLOBAL_ESTES
Estes Global.
CA_GREYHOUND
Greyhound Canada.
PUROLATOR
Purolator.
US_RL
RL US.
IT_BRT
BRT Corriere Espresso Italy
.
DMM_NETWORK
DMM Network.
IT_FERCAM
Fercam Italy.
HERMES_IT
Hermes Italy.
IT_POSTE_ITALIANE
Poste Italiane.
IT_SDA
SDA Express Courier.
IT_SGT
SGT Corriere Espresso Italy.
GLOBAL_SKYNET
Skynet Global.
FR_BERT
Bert France
.
FR_COLIS
Colis France.
FR_GEODIS
Geodis France.
FR_LAPOSTE
Laposte France.
FR_TELIWAY
Teliway France.
DPD_POLAND
DPD Poland.
INPOST_PACZKOMATY
InPost Paczkomaty.
POL_POCZTA
Poczta Poland.
POL_SIODEMKA
Siodemka Poland.
ESP_CORREOS
Sociedad Estatal Correos y Telégrafos
.
ES_CORREOS
Sociedad Estatal Correos y Telégrafos
.
ESP_NACEX
Nacex Spain
.
ESP_ASM
Parcel Monitor Spain
.
ESP_REDUR
Redur Spain
.
CBL_LOGISTICA
CBL Logística
.
EKART
Ekart.
IND_DELHIVERY
Delhivery India
.
IND_BLUEDART
Blue Dart Express DHL
.
IND_DTDC
DTDC India.
IND_PROFESSIONAL_COURIERS
Professional Couriers India.
IND_REDEXPRESS
Red Express India.
IND_XPRESSBEES
XpressBees India.
IND_DOTZOT
DotZot India
.
THA_KERRY
Kerry Thailand.
SENDIT
SendIt.
ACOMMERCE
aCommerce
.
NINJAVAN_THAI
Ninjavan Thailand.
NIM_EXPRESS
Nim Express
.
THA_THAILAND_POST
Thailand Post.
THA_DYNAMIC_LOGISTICS
Dynamic Logistics Thailand.
ALPHAFAST
Alphafast.
FASTRAK_TH
Fastrak Thailand.
EPARCEL_KR
EParcel Korea.
CJ_KOREA_THAI
CJ Logistics in Thailand
.
RINCOS
Rincos.
KOR_KOREA_POST
Korea Post.
KOR_CJ
CJ Korea.
KOR_ECARGO
Ecargo Korea.
SREKOREA
SRE Korea
.
ROCKETPARCEL
Rocket Parcel International
.
BG_BULGARIAN_POST
Bulgarian Post
.
JPN_JAPAN_POST
Japan Post
.
JPN_YAMATO
Yamato Japan.
JPN_SAGAWA
Sagawa Japan.
TUR_PTT
PTT Turkey.
AUT_AUSTRIAN_POST
Austrian Post.
AU_AUSTRIAN_POST
Austrian Post.
RUSSIAN_POST
Russian Post.
BEL_DHL
DHL Belgium.
FR_MONDIAL
Mondial France.
EU_BPOST
bpost
.
LANDMARK_GLOBAL
Landmark Global.
IDN_POS
Indonesia Post.
IDN_POS_INT
Indonesia Post International.
IDN_JNE
JNE Indonesia.
IDN_PANDU
Pandu Indonesia.
RPX
RPX International.
IDN_TIKI
Tiki Indonesia.
IDN_LION_PARCEL
Lion Parcel Indonesia.
NINJAVAN_ID
Ninjavan Indonesia.
IDN_WAHANA
Wahana Indonesia.
IDN_FIRST_LOGISTICS
First Logistics Indonesia.
UK_AN_POST
AddressPay UK
.
DPD
DPD Global.
UK_FASTWAY
Fastway UK.
UK_NIGHTLINE
Nightline UK.
WISELOADS
Wiseloads.
GR_ELTA
Elta Greece.
GRC_ACS
ACS Greece.
GR_GENIKI
Geniki Greece.
NINJAVAN_PHILIPPINES
Ninja Van Philippines.
PHL_XEND_EXPRESS
Xend Express Philippines.
PHL_LBC
LBC Philippines.
PHL_JAMEXPRESS
JamExpress Philippines.
PHL_AIRSPEED
Airspeed Philippines.
PHL_RAF
RAF Philippines.
DIRECTLOG
Directlog.
BRA_CORREIOS
Correios Brazil.
NLD_DHL
DHL Netherlands.
NLD_POSTNL
PostNL Netherlands
.
NLD_GLS
General Logistics Systems (GLS) Netherlands
.
NLD_TRANSMISSION
Transmission Netherlands.
CORREOS_DE_MEXICO
Mex Post Correos de Mexico
.
MEX_ESTAFETA
Estafeta Mexico
.
MEX_SENDA
Senda Mexico.
MEX_REDPACK
Redpack Mexico.
MEX_AEROFLASH
Aeroflash Mexico.
NATIONWIDE_MY
Nationwide Malaysia.
MYS_MYS_POST
Pos Malaysia
.
MYS_TAQBIN
TA-Q-BIN Parcel Malaysia.
MYS_SKYNET
Skynet Malaysia.
MYS_CITYLINK
Citylink Malaysia.
MYS_AIRPAK
Airpak Malaysia.
NINJAVAN_MY
Ninjavan Malaysia.
KANGAROO_MY
Kangaroo Express Malaysia.
VNM_VIETNAM_POST
Vietnam Post.
VNPOST_EMS
Post EMS Vietnam.
PRT_INT_SEUR
Internationational Seur Portugal
.
PRT_CTT
CTT Expresso Portugal
.
PRT_CHRONOPOST
Chronopost Portugal.
PRT_SEUR
Seur Portugal
.
ADICIONAL
Adicional.
LTU_LIETUVOS
Lietuvos paštas Lithuania.
DPEX
DPEX Worldwide
.
LWE_HK
LWE Hong Kong.
SG_SG_POST
Singapore Post.
SG_TAQBIN
TA-Q-BIN Parcel Singapore.
SG_NINJAVAN
Ninjavan Singapore.
SG_ZALORA
Zalora Singapore.
JET_SHIP
Jetship.
SG_PARCELPOST
Parcel Post Singapore.
CHE_SWISS_POST
Swiss Post.
ASENDIA_HK
Asendia Hong Kong.
HUN_MAGYAR
Magyar Posta
.
POSTNORD_LOGISTICS
Post Nord Logistics.
SWE_DIRECTLINK
Direct Link Sweden
.
SWE_POSTNORD
PostNord Sverige
.
SWE_DB
DB Schenker Sweden
.
CZE_CESKA
Česká pošta
.
NZ_NZ_POST
New Zealand Post Limited (NZ)
.
NZ_COURIER_POST
CourierPost New Zealand
.
FASTWAY_NZ
Fastway New Zealand.
TW_TAIWAN_POST
Chunghwa Post
.
SPREADEL
Spreadel.
ARE_EMIRATES_POST
Emirates Post Group
.
AXL
AXL Express & Logistics.
CYP_CYPRUS_POST
Cyprus Post
.
HRV_HRVATSKA
Hrvatska Pošta
.
NOR_POSTEN
Posten Norge
.
RAM
JP RAM Shipping
.
THECOURIERGUY
The Courier Guy
.
ZA_FASTWAY
fastway New Zealand
DPE_EXPRESS
DPE Express.
POSTI
Posti.
MATKAHUOLTO
Matkahuoloto.
GLOBAL_DHL
DHL Global.
ARG_CORREO
Correo Argentino
.
ARG_OCA
OCA Argentia
.
POST_SERBIA
Post of Serbia
.
BH_POSTA
BH POŠTA
.
CORREOS_CHILE
CorreosChile.
APR_72
APR 72.
CORREOS_DE_COSTA_RICA
Correos de Costa Rica
.
POSTUR_IS
Postur.
SPEEDEXCOURIER
Speedex Courier.
ROU_POSTA
Poșta Română
.
UKR_NOVA
Nova Poshta
.
UKR_POSHTA
Ukrposhta - Ukraine's National Post
.
NGA_NIPOST
Nigerian Postal Service
.
NG_COURIERPLUS
Courier Plus Nigeria
.
ESHOPWORLD
EShopWorld.
WEBINTERPRET
WebInterpret.
HERMES
Hermes.
ABC_MAIL
ABC Mail.
ARAMEX
Aramex.
YANWEN
Yanwen Express
.
INTERNATIONAL_BRIDGE
International Bridge.
SFC_LOGISTICS
SFC Logistics
.
BQC_EXPRESS
BQC Express.
ONE_WORLD
One World.
IT_REGISTER_MAIL
Registered Mail Italy.
WINIT
WinIt.
CONTINENTAL
Continental.
EFS
Enterprise Freight Systems (EFS)
.
PANTOS
Pantos.
RELAIS_COLIS
Relais Colis
.
US_DHL_EXPRESS
DHL Express US.
US_DHL_PARCEL
DHL Parcel US.
US_DHL_ECOMMERCE
DHL eCommerce US
.
US_DHL_GLOBALFORWARDING
DHL Global Forwarding US.
UK_DHL_EXPRESS
DHL Express UK.
UK_DHL_PARCEL
DHL Parcel UK.
UK_DHL_GLOBALFORWARDING
DHL Global Forwarding UK.
CN_DHL_EXPRESS
DHL Express Canada.
CN_DHL_ECOMMERCE
DHL eCommerce China.
CN_DHL_GLOBALFORWARDING
DHL Global Forwarding China.
DE_DHL_EXPRESS
DHL Express Germany.
DE_DHL_PARCEL
DHL Parcel Germany.
DE_DHL_PACKET
DHL Packet Germany.
DE_DHL_ECOMMERCE
DHL eCommerce Germany.
DE_DHL_GLOBALFORWARDING
DHL Global Forwarding Germany.
DE_DHL_DEUTSCHEPOST
DHL Deutschepost Germany.
AU_DHL_EXPRESS
DHL Express Australia.
AU_DHL_ECOMMERCE
DHL eCommerce Australia.
AU_DHL_GLOBALFORWARDING
DHL Global Forwarding Australia.
HK_DHL_EXPRESS
DHL Express Hong Kong.
HK_DHL_ECOMMERCE
DHL eCommerce Hong Kong.
HK_DHL_GLOBALFORWARDING
DHL Global Forwarding Hong Kong.
CA_DHL_EXPRESS
DHL Express Canada.
CA_DHL_ECOMMERCE
DHL eCommerce Canada.
CA_DHL_GLOBALFORWARDING
DHL Global Forwarding Canada.
IT_DHL_EXPRESS
DHL Express Italy.
IT_DHL_ECOMMERCE
DHL eCommerce Italy.
IT_DHL_GLOBALFORWARDING
DHL Global Forwarding Italy.
FR_DHL_EXPRESS
DHL Express France.
FR_DHL_PARCEL
DHL Parcel France.
FR_DHL_GLOBALFORWARDING
DHL Global Forwarding France.
PL_DHL_EXPRESS
DHL Express Poland.
PL_DHL_PARCEL
DHL Parcel Poland.
PL_DHL_GLOBALFORWARDING
DHL Global Forwarding Poland
ABC_PACKAGE
ABC Package Express
.
AN_POST
An Post Ireland
.
APC_OVERNIGHT
APC Overnight
.
ASM_ES
ASM Tracking Spain
.
AUPOST_CN
Logistics in China
.
ACOMMMERCE
aCommerce
.
ADICIONAL_PT
Adicional Logistics Portugal
.
AIR_21
Air 21.
AIRBORNE_EXPRESS_UK
Airborne Express UK.
AIRPAK_MY
Airpak Malaysia.
AIRSPEED
Airspeed.
ASENDIA_DE
Asendia Germany.
ASENDIA_US
Asendia USA
.
AUSTRALIA_POST
Australia Post.
TOLL_AU
Toll Australia.
AUSTRIAN_POST_EXPRESS
Austrian Post Express.
AUSTRIAN_POST
Austrian Post Registered.
B_TWO_C_EUROPE
B2C Europe.
BERT
Groupe Bert
.
BPOST
BPost.
BRT_IT
BRT Bartolini.
BLUEDART
Bluedart.
BONDS_COURIERS
Bonds Couriers.
BPOST_INT
bpost International
.
BULGARIAN_POST
Bulgarian Post.
CJ_LOGISTICS
CJ Logistics
.
CJ_INT_MY
CJ Malaysia International.
CJ_MY
CJ Malaysia.
CJ_TH
CJ Thailand.
CANADA_POST
Canada Post.
CANPAR
Canpar Express
.
CESKA_CZ
Česká Pošta
.
CHRONOPOST_FR
Chronopost France
.
CHRONOPOST_PT
Chronopost Portugal
.
CHUNGHWA_POST
Chunghwa Post.
CITYLINK_MY
CityLink Malaysia.
COLIPOSTE
Coliposte.
COLIS
Colis France.
COLLECTPLUS
CollectPlus
.
CORREOS_AG
Correos Argentina.
CORREOS_BR
Correos Brazil.
CORREOS_CL
Correos Chile.
CORREOS_CR
Correos De Costa Rica.
CORREOS_MX
Correos De Mexico.
CORREOS_ES
Correos De Spain.
CORREOS_EXPRESS
Correos Express.
COURIERPLUS
Courier Plus.
COURIER_POST
Courier Post.
CYPRUS_POST_CYP
Cyprus Post.
DBSCHENKER_SE
DB Schenker Sweden.
DHL_ES
DHL Spain.
DHL_ACTIVE_TRACING
DHL Active Tracing.
DHL_AU
DHL Australia.
DHL_BENELUX
DHL Benelux.
DHL_DEUTSCHE_POST
DHL Deutsche Post.
DHL_FR
DHL France.
DHL_GLOBAL_ECOMMERCE
DHL Global eCommerce.
DHL_HK
DHL HonKong
DHL_IT
DHL Italy.
DHL_JP
DHL Japan.
DHL_NL
DHL Netherlands.
DHL_PACKET
DHL Packet.
DHL_PARCEL_NL
DHL Parcel Netherlands.
DHL_PARCEL_ES
DHL Parcel Spain.
DHL_PL
DHL Poland.
DHL_SG
DHL Singapore.
DHL_UK
DHL UK.
DHL_GLOBAL_MAIL_ASIA
DHL eCommerce Asia.
DHL_GLOBAL_MAIL
DHL eCommerce US.
DHL_AT
DHL Austria.
DPD_DELISTRACK
DPD Delistrack.
DPD_FR
DPD France.
DPD_DE
DPD Germany.
DPD_HK
DPD Hong Kong.
DPD_IR
DPD Ireland.
DPD_LOCAL_REF
DPD Local Reference.
DPD_LOCAL
DPD Local.
DPD_PL
DPD Poland.
DPD_RO
DPD Romania.
DPD_RU
DPD Russia.
DPD_UK
DPD UK.
DTDC_EXPRESS
DTDC Express Global
.
DTDC_IN
DTDC India
.
DAWN_WING
Dawn Wing.
DELHIVERY_IN
Delhivery India
.
DELTEC_DE
Deltec Germany.
DELTEC_UK
Deltec UK.
DEUTSCHE_DE
Deutsche Post
.
DIRECTLINK_SE
Direct Link Sweden
.
DIRECTLOG_BR
Directlog.
DOTZOT
Dotzot.
EC_CN
EC China.
ELTA_GR
ELTA Greece.
EMPS_CN
EMPS China.
EMS_CN
EMS China.
ECARGO
Ecargo.
EMIRATES_POST
Emirates Post.
ENSENDA
Ensenda USA.
ESTAFETA
Estafeta.
ESTES
Estes.
FERCAM_IT
FERCAM Logistics & Transport.
FLYT_EXPRESS
FLYT Express.
FASTRACK
FastTrack Thailand.
FASTWAY_US
Fastway USA.
FASTWAY_ZA
Fastway South Africa.
FASTWAY_UK
Fastway UK.
FASTWAY_AU
Fastway Australia.
FIRST_LOGISITCS
First Logistics.
FOUR_PX_EXPRESS
4PX Express.
GEODIS
GEODIS - Distribution & Express.
GLS_CZ
GLS Czech Republic
.
GLS_FR
GLS France
.
GLS_DE
GLS Germany
.
GLS_IT
GLS Italy
.
GLS_NL
GLS Netherlands
.
GLS_ES
GLS Spain
.
GLS
GLS
.
ACS_GR
Parcel Monitor Greece
.
GENIKI_GR
Geniki Greece.
GLOBEGISTICS
Globegistics USA.
GREYHOUND
Greyhound.
HERMES_DE
Hermes Germany.
HERMESWORLD_UK
HermesWorld UK.
HK_POST
Hong Kong Post.
HRVATSKA_HR
Hrvatska Pošta
.
HUAHAN_EXPRESS
Huahan Express.
IMX
IMX France.
ITIS
ITIS International Courier Tracking
.
INDIA_POST
India Post.
INTERLINK
Interlink Express.
INT_SEUR
International Seur.
INT_SUER
International Seur.
ISRAEL_POST
Israel Post.
JNE_IDN
JNE Indonesia.
JAMEXPRESS_PH
Jam Express.
JAPAN_POST
Japan Post.
JP_POST
Japan Post.
JETSHIP_MY
Jet Ship Malaysia.
JETSHIP_SG
JetShip Singapore.
KERRY_EXPRESS_VN
Kerry Express Vietnam.
KERRY_EXPRESS_HK
Kerry Express Hong Kong.
KERRY_EXPRESS_TH
Kerry Express Thailand.
KIALA
Kiala.
KOREA_POST
Korea Post.
CJ_KR
CJ Logistics Korea
.
LAPOSTE
LA Poste.
LBC_PH
LBC Express.
LIETUVOS_LT
Lietuvos Pastas.
LION_PARCEL
Lion Parcel.
LOGISTICSWORLDWIDE_HK
Logistics Worldwide Hong Kong
.
LOGISTICSWORLDWIDE_KR
Logistics Worldwide Korea
.
LOGISTICSWORLDWIDE_MY
Logistics Worldwide Malaysia
.
LOOMIS
Loomis.
MONDIAL
Mondial Relay
.
MAGYAR_HU
Magyar Posta
.
MALAYSIA_POST
Pos Malaysia Berhad
.
MASTERLINK
Masterlink.
AEROFLASH
Mexico Aeroflash.
REDPACK
Mexico Redpack.
SENDA_MX
Mexico Senda Express.
MONDIAL_BE
Mondial Belgium.
MYHERMES
MyHermes UK.
NACEX_ES
Nacex Spain
.
NATIONWIDE
Nationwide Carrier and Logistics Services
.
NZ_POST
New Zealand Post.
NIPOST_NG
Nigerian Postal Service
.
NIGHTLINE_UK
Nightline UK.
NINJAVAN_PH
Ninjavan Philippines.
NINJAVAN_SG
Ninjavan Singapore.
NOVA_POSHTA_INT
Nova Poshta International.
NOVA_POSHTA
Nova Poshta.
OCA_AR
OCA Argentina
.
ONTRAC
OnTrac.
PTT_POST
PTT Posta.
PANDU
Pandu Logistics.
PARCELPOST_SG
Parcel Post Singapore.
POCZTA_POLSKA
Poczta Polska
.
POCZTEX
Pocztex.
CTT_PT
CTT Expresso Portugal
.
SEUR_PT
Seur Portugal
.
POS_ID
Pos Indonesia Domestic.
POS_INT
Pos Indonesia International.
POSTNL_INT_3_S
Koninklijke PostNL
.
POSTNL
PostNL.
POSTNL_INT
PostNl International.
POSTNORD_LOGISTICS_DK
PostNord Logistics Denmark.
POSTNORD_LOGISTICS_SE
PostNord Logistics Sweden.
POSTNORD_LOGISTICS_GLOBAL
PostNord Logistics.
POSTA_RO
Posta Romana.
POSTE_ITALIANE
Poste Italiane.
POSTEN_NORGE
Posten Norge.
PROFESSIONAL_COURIERS
Professional Couriers.
RAF_PH
RAF Philippines.
RL_US
RL Carriers.
RPD_2_MAN
RPD2man Deliveries.
RPX_ID
RPX Indonesia.
REDEXPRESS
Red Express.
REDUR_ES
Redur Spain.
REGISTER_MAIL_IT
Registered Mail Italy.
RELAIS_COLIS_FR
Relais Colis.
ROCKET_PARCEL
Rocket Parcel International.
SDA_IT
SDA Italy.
SF_EXPRESS
SF Express
.
SFC_EXPRESS
SFC Express.
SGT_IT
SGT Corriere Espresso.
SRE_KOREA
SRE Korea.
SAGAWA
Sagawa.
SAGAWA_JP
Sagawa.
POST_SERBIA_CS
Serbia Post.
SINGPOST
Singapore Post.
SIODEMKA
Siodemka.
SKYNET_WORLDWIDE
SkyNet Worldwide Express
.
SKYNET_MY
Skynet Malaysia.
SKYNET_UAE
SkyNet Worldwide Express Dubai, UAE
.
SKYNET_UK
SkyNet Worldwide Express UK
.
SEUR_ES
Seur Spain
.
STARTRACK_EXPRESS
Star Track Express.
STARTRACK
Star Track.
SWISS_POST
Swiss Post.
TNT_AU
TNT Australia.
TNT_CN
TNT China.
TNT_CLICK_IT
TNT Click Italy.
TNT_FR
TNT France.
TNT_DE
TNT Germany.
TNT_IT
TNT Italy.
TNT_JP
TNT Japan.
TNT_NL
TNT Netherlands.
TNT_PL
TNT Poland.
TNT_ES
TNT Spain.
TNT_UK
TNT UK.
TPG
TPG International & Domestic Express
.
TAIWAN_POST_TW
Taiwan Post.
TAQBIN_HK
TA-Q-BIN Parcel Hong Kong.
TAQBIN_MY
TA-Q-BIN Parcel Malaysia.
TAQBIN_SG
TA-Q-BIN Parcel Singapore.
TAXIPOST
TaxiPost.
TELIWAY
Teliway.
THAILAND_POST
Thailand Post.
THE_COURIER_GUY
The Courier Guy.
TIKI_ID
Tiki.
TOLL_IPEC
Toll IPEC.
TWO_GO
2GO.
TRANSMISSION
Transmission Netherlands.
UK_MAIL
UK Mail.
UPS_MI
UPS Mail Innovations.
VIETNAM_POST
Vietnam Post.
WAHANA_ID
Wahana Express Indonesia
.
XEND_EXPRESS_PH
Xend Express.
XPRESSBEES
Xpress Bees.
YAMATO
Yamato Japan.
YANWEN_CN
Yanwen China.
YODEL
Yodel.
UPS_CANADA
UPS Canada.
UPS_MAIL_INNOVATIONS
UPS Mail Innovations.
DE_DELTEC
Deltec Germany.
DE_INTERNATIONALSEUR
International Seur Germany.
FR_DPD
DPD France.
FR_IMX
IMX France.
IT_IMX
IMX Italy.
AU_DTDC
DTDC Australia.
AU_SENDLE
Sendle Australia.
AU_SKYNET
Skynet Australia.
ES_GLS
General Logistics Systems (GLS) Spain
.
ES_INTERNATIONALSEUR
Seur International Spain
.
ES_IMX
IMX Spain.
CN_HUAHANEXPRESS
Huahan Express China.
LOCAL_PICKUP
Local Pickup.
HK_DPEX
DPEX Worldwide Hong Kong
.
HK_KERRYEXPRESS
Kerry Express Hong Kong.
HK_LOGISTICSWORLDWIDEEXPRESS
Logistics Worldwide Express Hong Kong.
HK_RPX
RPX Hong Kong.
HK_SPREADEL
Spreadel Hong Kong.
IN_SPREADEL
Spreadel IN.
TH_CJ
CJ Thailand.
KR_LOGISTICSWORLDWIDE
Logistics Worldwide Korea
.
AT_DHL
DHL Austria.
BE_IMX
IMX Belgium.
MY_LOGISTICSWORLDWIDE
Logistics Worldwide Malaysia
.
MY_JETSHIP
Jetship Malaysia.
SG_DHL
DHL Singapore.
SG_SPREADEL
Spreadel Singapore.
POSTAROMANA
Romanian Post
.
US_PUROLATOR
Purolator US
.
US_FASTWAY
Fastway US.
CHRONOPOST
Chronopost
.
CORREOS_DE_ESPANA
Correos de Espana
.
DEUTSCHE_POST_DHL
Deutsche Post DHL
.
EBOOST_SDA
Posteitaliane
.
HONGKONG_POST
Hong Kong Post.
INTANGIBLE_DIGITAL_SERVICES
Intangible Digital Services.
LA_POSTE
La Poste
.
LA_POSTE_SUIVI
La Poste Suivi
.
NEKO_YAMATO_UNYUU
Yamato Transport Co.
.
NITTSU_PELICAN_BIN
Nippon Express
.
POSTE_ITALIA
Posteitaliane
.
SAGAWA_KYUU_BIN
Sagawa Express Co.
.
STAR_TRACK_EXPRESS
Star Track Express
.
US_DTDC
DTDC US.
US_STARTRACK
Star Track US.
ISR_ISRAEL_POST
Israel Post
.
BE_MONDIAL
Mondial Belgium.
B_2_CEUROPE
B2C Europe
.
PHL_2_GO
2GO Shipping Philippines.
PHL_AIR_21
Air 21 Philippines.
PT_SPANISH_SEUR
Internationational Seur Spanish Portugal
.
ES_SPANISH_SEUR
Seur Spain
.
SG_DPEX
DPEX Worldwide Singapore
.
CH_IMX
IMX Switzerland.
DHLG
DHLG.
RUSTON
Ruston
MIKROPAKKET
Mikropakket
XPOST
Xpost.ph
PAN_ASIA
Pan-Asia International
PARCELONE
PARCEL ONE
SPEEDEE
Spee-Dee Delivery
VENIPAK
Venipak
CROSHOT
Croshot
SHREENANDANCOURIER
SHREE NANDAN COURIER
EPST_GLBL
ePost Global
NEWGISTICS
Newgistics
POST_SLOVENIA
Post of Slovenia
JERSEY_POST
Jersey Post
WMG
WMG Delivery
BOMBINOEXP
Bombino Express Pvt
XQ_EXPRESS
XQ Express
FURDECO
Furdeco
LEGION_EXPRESS
Legion Express
YDH_EXPRESS
YDH express
LHT_EXPRESS
LHT Express
SOUTH_AFRICAN_POST_OFFICE
South African Post Office
GRUPO
Grupo ampm
SPOTON
SPOTON Logistics Pvt Ltd
DIMERCO
Dimerco Express Group
INTERPARCEL_UK
Interparcel UK
ABCUSTOM
AB Custom Group
IND_DELIVREE
deliverE
GLOBAL_ABF
ABF Freight
CN_BESTEXPRESS
Best Express
DX_SFTP
DX (SFTP)
PICKUPP_MYS
PICK UPP
XPERT_DELIVERY
Xpert Delivery
FMX
FMX
HELLMANN
Hellmann Worldwide Logistics
DHL_REFR
DHl (Reference number)
SHIP_IT_ASIA
Ship It Asia
KERRY_ECOMMERCE
Kerry eCommerce
GOJEK
Gojek
FRETERAPIDO
Frete Rapido
YODEL_INTNL
Yodel International
CFL_LOGISTICS
CFL Logistics
PITNEY_BOWES
Pitney Bowes
ZA_SPECIALISED_FREIGHT
Specialised Freight
JANCO
Janco Ecommerce
XPRESSEN_DK
Xpressen courier
YTO
YTO Express
RPD2MAN
RPD2man Deliveries
SEUR_SP_API
Spanish Seur API
DELIVERYONTIME
DELIVERYONTIME LOGISTICS PVT LTD
WISE_EXPRESS
Wise Express
JINSUNG
JINSUNG TRADING
JTEXPRESS_VN
J&T Express Vietnam
CHUKOU1
Chukou1
TRANS_KARGO
Trans Kargo Internasional
FEDEX_INTL_MLSERV
FedEx International MailService
SWISHIP_DE
Swiship DE
IVOY_WEBHOOK
Ivoy courier
AIRMEE_WEBHOOK
Airmee couriers
VAMOX
VAMOX
FIRSTMILE
FirstMile
AMS_GRP
AMS Group
FASTWAY_IR
Fastway Ireland
HH_EXP
Hua Han Logistics
HRPARCEL
HR Parcel
MYS_MYPOST_ONLINE
Mypostonline
GESWL
GESWL Express
BLUESTAR
Blue Star
TIPSA
TIPSA courier
CDEK_TR
CDEK TR
KGMHUB
KGM Hub
INTEXPRESS
Internet Express
DESCARTES
Innovel courier
OVERSE_EXP
Overseas Express
ONECLICK
One click delivery services
ROADRUNNER_FREIGHT
Roadbull Logistics
GLS_CROTIA
GLS Croatia
TOURLINE
tourline
MRW_FTP
MRW courier
BH_WORLDWIDE
B&H Worldwide
BLUEX
Blue Express
DYLT
Daylight Transport
OCS
OCS ANA Group
YINGNUO_LOGISTICS
yingnuo logistics
SIN_GLBL
Sin Global Express
TUFFNELLS_REFERENCE
Tuffnells Parcels Express- Reference
CJPACKET
CJ Packet
MILKMAN
Milkman courier
FIEGE_NL
Fiege Netherlands
ASIGNA
ASIGNA courier
ONEWORLDEXPRESS
One World Express
LTIANEXP
LTIAN EXP
KWE_GLOBAL
KWE Global
CTC_EXPRESS
CTC Express
LAO_POST
Lao Post
EU_IMX
IMX Mail
GLS_SLOV
GLS General Logistics Systems Slovakia s.r.o.
AMAZON
Amazon Shipping
MORE_LINK
Morelink
JX
JX courier
MYS_EMS
Malaysia Post EMS / Pos Laju
EASY_MAIL
Easy Mail
ADUIEPYLE
A Duie Pyle
GB_PANTHER
Panther
SG_DETRACK
Detrack
EXPRESSSALE
Expresssale
DICOM
GLS Logistic Systems Canada Ltd./Dicom
MATDESPATCH
Matdespatch
TRUNKRS_WEBHOOK
Trunkrs courier
WESTBANK_COURIER
West Bank Courier
MBW
MBW Courier Inc.
KHM_CAMBODIA_POST
Cambodia Post
FEDEX_CROSSBORDER
FedEx Cross Border
JANIO
Janio Asia
SINOTRANS
Sinotrans
BRT_IT_PARCELID
BRT Bartolini(Parcel ID)
A1POST
A1Post
DHL_SUPPLY_CHAIN
DHL Supply Chain APAC
TAZMANIAN_FREIGHT
Tazmanian Freight Systems
TOPYOU
TopYou
PALEXPRESS
PAL Express Limited
SAIA_FREIGHT
Saia LTL Freight
CN_WEDO
WeDo Logistics
FULFILLME
Fulfillme
SG_QXPRESS
Qxpress
UPS_REFERENCE
UPS Reference
NHANS_SOLUTIONS
Nhans Solutions
CARIBOU
Caribou
LOCUS_WEBHOOK
Locus courier
DSV
DSV courier
CN_GOFLY
GoFly
COORDINADORA
Coordinadora
P2P_TRC
P2P TrakPak
ANDREANI
Grupo logistico Andreani
DIRECTPARCELS
Direct Parcels
DOORA
Doora Logistics
FEDEX_POLAND
FedEx® Poland Domestic
INTERPARCEL_NZ
Interparcel New Zealand
XDP_UK_REFERENCE
XDP Express Reference
ETOMARS
Etomars
CN_JCEX
JCEX courier
IND_ECOM
Ecom Express
FAR_INTERNATIONAL
FAR international
ESP_ENVIALIA
Envialia
IDEXPRESS
IDEX courier
GANGBAO
GANGBAO Supplychain
SMSA_EXPRESS
SMSA Express
NEWAY
Neway Transport
DEX_I
DEX-I courier
DESIGNERTRANSPORT_WEBHOOK
Designer Transport
BUDBEE_WEBHOOK
Budbee courier
GLS_SLOVEN
GLS Slovenia
PARCELLED_IN
Parcelled.in
COPA_COURIER
Copa Airlines Courier
GSI_EXPRESS
GSI EXPRESS
CON_WAY
Con-way Freight
BROUWER_TRANSPORT
Brouwer Transport en Logistiek
TOLL_NZ
Toll New Zealand
CPEX
Captain Express International
ECHO
Echo courier
FEDEX_FR
FedEx® Freight
XDE_WEBHOOK
Ximex Delivery Express
TOLOS
Tolos courier
BORDEREXPRESS
Border Express
GIAO_HANG
Giao hàng nhanh
MAILPLUS_JPN
MailPlus (Japan)
GEODIS_ESPACE
Geodis E-space
TNT_UK_REFR
TNT UK Reference
DOORDASH_WEBHOOK
DoorDash
KEC
KEC courier
CJ_HK_INTERNATIONAL
CJ Logistics International(Hong Kong)
HELTHJEM
Helthjem
ZA_COURIERIT
Courier IT
SFB2C
SF International
FREIGHTQUOTE
Freightquote by C.H. Robinson
FR_EXAPAQ
DPD France (formerly exapaq)
LANDMARK_GLOBAL_REFERENCE
Landmark Global Reference
PARCEL2GO
Parcel2Go
DELNEXT
Delnext
TCK_EXPRESS
TCK Express
ENDEAVOUR_DELIVERY
Endeavour Delivery
NANJINGWOYUAN
Nanjing Woyuan
HEPPNER_FR
Heppner France
PICKRR
Pickrr
FONSEN
Fonsen Logistics
APC_OVERNIGHT_CONNUM
APC Overnight Consignment
STAR_TRACK_NEXT_FLIGHT
Star Track Next Flight
UPS_FREIGHT
UPS Freight
DAJIN
Shanghai Aqrum Chemical Logistics Co.Ltd
POSTA_PLUS
Posta Plus
CEVA
CEVA LOGISTICS
ORANGE_DS
OrangeDS (Orange Distribution Solutions Inc)
ANSERX
ANSERX courier
JS_EXPRESS
JS EXPRESS
PADTF
padtf.com
GAC
GAC
EZSHIP
EZship
GEIS
Geis CZ
SYPOST
Sunyou Post
AMAZON_SHIP_MCF
Amazon Shipping + Amazon MCF
SF_EX
SF Express
YUSEN
Yusen Logistics
ESP_MRW
MRW spain
BRING
Bring
PAGO
Pago Logistics
AO_COURIER
AO Logistics
GBA
GBA Services Ltd
DIAMOND_EUROGISTICS
Diamond Eurogistics Limited
NEWEGGEXPRESS
Newegg Express
LALAMOVE
Lalamove
SPEEDCOURIERS_GR
Speed Couriers
CORPORATECOURIERS_WEBHOOK
Corporate Couriers
FORRUN
forrun Pvt Ltd (Arpatech Venture)
PICKUP
Pickupp
BOND
Bond courier
ECMS
ECMS International Logistics Co.
INTELIPOST
Intelipost (TMS for LATAM)
SK_POSTA
Slovenska pošta
FLASHEXPRESS
Flash Express
FETCHR_WEBHOOK
Mena 360 (Fetchr)
CN_STO
STO Express
SEKO_SFTP
SEKO Worldwide
THEDELIVERYGROUP
TDG – The Delivery Group
CELLO_SQUARE
Cello Square
HOME_DELIVERY_SOLUTIONS
Home Delivery Solutions Ltd
DPD_HGRY
DPD Hungary
KERRYTTC_VN
Kerry Express (Vietnam) Co Ltd
TARRIVE
TONDA GLOBAL
JOYING_BOX
Joying Box
COLLIVERY
MDS Collivery Pty (Ltd)
TOTAL_EXPRESS
Total Express
ZJS_EXPRESS
ZJS International
STARKEN
STARKEN couriers
MAINFREIGHT
Mainfreight
IND_FIRSTFLIGHT
First Flight Couriers
BE_BPOST
Bpost (
www.bpost.be
)
DEMANDSHIP
DemandShip
CN_DPEX
DPEX
ACSWORLDWIDE
ACS Worldwide Express
LOGISTERS
Logisters
GOGLOBALPOST
Global Post
AMSTAN
Amstan Logistics
OKAYPARCEL
OkayParcel
I_DIKA
i-dika
ENVIALIA_REFERENCE
Envialia Reference
PAACK_WEBHOOK
Paack courier
GRAB_WEBHOOK
Grab courier
PARCELPOINT
Parcelpoint
ICUMULUS
iCumulus
FDSEXPRESS
FDSEXPRESS
DAIGLOBALTRACK
DAI Post
CNDEXPRESS
CND Express
GLOBAL_IPARCEL
i-parcel
AMAZON_FBA_SWISHIP
Swiship UK
WYNGS
Wyngs
YURTICI_KARGO
Yurtici Kargo
CN_PAYPAL_PACKAGE
PayPal Package
PARCEL_2_POST
Parcel To Post
ZYLLEM
Zyllem
VIA_EXPRESS
Viaxpress
WIZMO
Wizmo
TIGFREIGHT
TIG Freight
PIL_LOGISTICS
PIL Logistics (China) Co.
ZTO_EXPRESS
ZTO Express
HEPPNER
Heppner Internationale Spedition GmbH & Co.
GENERAL_OVERNIGHT
Go!Express and logistics
HAPPY2POINT
Happy 2ThePoint
ARCO_SPEDIZIONI
Arco Spedizioni SP
CHITCHATS
Chit Chats
IML
IML courier
SMOOTH
Smooth Couriers
INTEL_VALLEY
Intel-Valley Supply chain (ShenZhen) Co. Ltd
CLE_LOGISTICS
CL E-Logistics Solutions Limited
FIEGE
Fiege Logistics
MX_CARGO
M&X cargo
ZIINGFINALMILE
Ziing Final Mile Inc
TCS
TCS courier
DAYTON_FREIGHT
Dayton Freight
ROADBULL
Red Carpet Logistics
YODEL_DIR
Yodel Direct
STONE3PL
STONE3PL
PARCELPAL_WEBHOOK
ParcelPal
DHL_ECOMERCE_ASA
DHL eCommerce Asia (API)
SIMPLYPOST
J&T Express Singapore
KY_EXPRESS
Kua Yue Express
SHENZHEN
shenzhen 1st International Logistics(Group)Co
UC_EXPRE
ucexpress
US_LASERSHIP
LaserShip
DIDADI
DIDADI Logistics tech
DYNALOGIC
Dynamic Logistics
DBSCHENKER_B2B
DB Schenker B2B
MXE
MXE Express
PFCEXPRESS
PFC Express
WHISTL
Whistl
CAE_DELIVERS
CAE Delivers
WEPOST
WePost Sdn Bhd
ALLIEDEXPRESS
Allied Express
SHIPPIT
Shippit
DDEXPRESS
DD Express Courier
ARAMEX_AU
Aramex Australia (formerly Fastway AU)
TFM
TFM Xpress
BNEED
Bneed courier
M_XPRESS
M Xpress Sdn Bhd
HK_TGX
Kerry Express Hong Kong
LATVIJAS_PASTS
Latvijas Pasts
HDB_BOX
Haidaibao (BOX)
VIAEUROPE
ViaEurope
CORREO_UY
Correo Uruguayo
CLEVY_LINKS
Clevy Links
IBEONE
Beone Logistics
J_NET
J-Net
RCL
Red Carpet Logistics
6LS
6ls.com
CGS_EXPRESS
CGS Express
BLR_BELPOST
Belpost
BIRDSYSTEM
BirdSystem
DOBROPOST
DobroPost
SAP_EXPRESS
SAP EXPRESS
WEASHIP
Weaship
SONICTL
Sonic Transportation & Logistics
KWT
Shenzhen Jinghuada Logistics Co.
AFLLOG_FTP
AFL LOGISTICS
IND_SAFEEXPRESS
Safexpress
TOPHATTEREXPRESS
Tophatter Express
SEINO
Seino
MGLOBAL
PT MGLOBAL LOGISTICS INDONESIA
SZENDEX
SZENDEX
AVERITT
Averitt Express
DBSCHENKER_SV
DB Schenker Sweden
LEADER
leader
AO_DEUTSCHLAND
AO Deutschland
2EBOX
2ebox courier
EU_FLEET_SOLUTIONS
EU Fleet Solutions
SG_SPEEDPOST
Singapore Speedpost
PCFCORP
PCF Final Mile
AERONET
Aeronet couriers
LINKBRIDGE
Link Bridge(BeiJing)international logistics co.
DE_DEUTSCHE_POST_DHL_WITHIN_EUROPE_TRACKNET
Deutsche Post DHL
PRIMAMULTICIPTA
PT Prima Multi Cipta
ISR_POST_DOMESTIC
Israel Post Domestic
COUREX
Urbanfox
ZAJIL_EXPRESS
Zajil Express Company
BESTWAYPARCEL
Best Way Parcel
COLLECTCO
CollectCo
AEX
AEX Group
JTEXPRESS
J&T EXPRESS MALAYSIA
FEDEX_UK
FedEx® UK
USHIP
uShip courier
ROUTIFIC_WEBHOOK
Routific
GLOBAL_EXPRESS
Tai Wan Global Business
BRT_IT_SENDER_REF
BRT Bartolini(Sender Reference)
GLOBAVEND
Globavend
PIXSELL
PIXSELL LOGISTICS
SHIPTOR
Shiptor
CDEK
CDEK courier
VNM_VIETTELPOST
ViettelPost
PHL_AIR21
AIR21 courier
PALLET_NETWORK
The Pallet Network
CJ_CENTURY
CJ Century
UK_XDP
XDP Express
GSO
GSO(GLS-USA)
VIWO
VIWO IoT
SKYBOX
SKYBOX
PAPER_EXPRESS
Paper Express
KERRYTJ
Kerry TJ Logistics
NTLOGISTICS_VN
Nhat Tin Logistics
SDH_SCM
lightning monkey
PALLETWAYS
Palletways
NOX_NACHTEXPRESS
Innight Express Germany GmbH (nox NachtExpress)
ZINC
Zinc courier
DPE_SOUTH_AFRC
DPE South Africa
LOGISTIKA
Logistika
CELERITAS
Celeritas Transporte
PRESSIODE
Pressio
SHREE_MARUTI
Shree Maruti Courier Services Pvt Ltd
PARCELINKLOGISTICS
Parcelink Logistics
EFEX
eFEx (E-Commerce Fulfillment & Express)
LOTTE
Lotte Global Logistics
LONESTAR
Lone Star Overnight
GB_NORSK
Norsk Global
APRISAEXPRESS
Aprisa Express
BEL_RS
BEL North Russia
OSM_WORLDWIDE
OSM Worldwide
SAILPOST
SAILPOST
MAILAMERICAS
MailAmericas
WESTGATE_GL
Westgate Global
DTD_EXPR
DTD Express
ALFATREX
AlfaTrex
THABIT_LOGISTICS
Thabit Logistics
PROMEDDELIVERY
ProMed Delivery
PAQUETEXPRESS
Paquetexpress
NEWZEALAND_COURIERS
NEW ZEALAND COURIERS
LIEFERY
liefery
JOOM_LOGIS
Joom Logistics
STRECK_TRANSPORT
Streck Transport
HCT_LOGISTICS
HCT LOGISTICS CO.LTD.
CARRY_FLAP
Carry-Flap Co.
PONY_EXPRESS
Pony express
US_OLD_DOMINION
Old Dominion Freight Line
ANICAM_BOX
ANICAM BOX EXPRESS
ALWAYS_EXPRESS
Always Express
WANBEXPRESS
WanbExpress
AUS_STARTRACK
StarTrack (startrack.com.au)
GBS_BROKER
GBS-Broker
STALLIONEXPRESS
Stallion Express
RAIDEREX
RaidereX
ALLJOY
ALLJOY SUPPLY CHAIN
SHOPFANS
ShopfansRU LLC
KYUNGDONG_PARCEL
Kyungdong Parcel
CHAMPION_LOGISTICS
Champion Logistics
PICKUPP_SGP
PICK UPP (Singapore)
DEALERSEND
DealerSend
MORNING_EXPRESS
Morning Express
NACEX
NACEX
THENILE_WEBHOOK
SortHub courier
JOCOM
Jocom
HOLISOL
Holisol
LBCEXPRESS_FTP
LBC EXPRESS INC.
CSE
CSE courier
TFORCE_FINALMILE
TForce Final Mile
KURASI
KURASI
GEMWORLDWIDE
GEM Worldwide
SHIP_GATE
ShipGate
USF_REDDAWAY
USF Reddaway
SHIPTER
SHIPTER
NATIONAL_SAMEDAY
National Sameday
APG
APG eCommerce Solutions
CN_BOXC
BoxC courier
YUNEXPRESS
YunExpress
INTEGRA2_FTP
Integra2
CAINIAO
AliExpress Standard Shipping
ECOSCOOTING
ECOSCOOTING
DMS_MATRIX
DMSMatrix
MAINWAY
Mainway
ASENDIA_USA
Asendia USA
PAPERFLY
Paperfly Private Limited
HOUNDEXPRESS
Hound Express
3JMSLOGISTICS
3JMS Logistics
EP_BOX
EP-Box courier
BOX_BERRY
Boxberry courier
LICCARDI_EXPRESS
LICCARDI EXPRESS COURIER
PLUS_LOG_UK
Plus UK Logistics
FULFILLA
Fulfilla
SKY_POSTAL
SkyPostal
ASE
ASE KARGO
CNWANGTONG
cnwangtong
PITTOHIO
PITT OHIO
MAIL_PLUS
MailPlus
XPO_LOGISTICS
XPO logistics
WNDIRECT
wnDirect
CLOUDWISH_ASIA
Cloudwish Asia
ZELERIS
Zeleris
MARA_XPRESS
Mara Xpress
GIO_EXPRESS
Gio Express
OCS_WORLDWIDE
OCS WORLDWIDE
DESTINY
Destiny Transportation
ARK_LOGISTICS
ARK Logistics
DE_DPD_DELISTRACK
DPD Germany
COMET_TECH
CometTech
DHL_PARCEL_RU
DHL Parcel Russia
AQUILINE
Aquiline
PILOT_FREIGHT
Pilot Freight Services
TNT_REFR
TNT Reference
QWINTRY
Qwintry Logistics
DANSKE_FRAGT
Danske Fragtaend
SHREE_ANJANI_COURIER
Shree Anjani Courier
CARRIERS
Carriers courier
AIR_CANADA_GLOBAL
Rivo (Air canada)
PRESIDENT_TRANS
PRESIDENT TRANSNET CORP
STEPFORWARDFS
STEP FORWARD FREIGHT SERVICE CO LTD
ESHIPPING
Eshipping
SHREETIRUPATI
SHREE TIRUPATI COURIER SERVICES PVT. LTD.
HX_EXPRESS
HX Express
INDOPAKET
INDOPAKET
CN_17POST
17 Post Service
K1_EXPRESS
K1 Express
CJ_GLS
CJ GLS
MYS_GDEX
GDEX courier
NATIONEX
Nationex courier
CN_EQUICK
Equick China
ANJUN
Anjun couriers
VIRTRANSPORT
VIR Transport
FARGOOD
FarGood
SMG_EXPRESS
SMG Direct
RZYEXPRESS
RZY Express
SEFL
Southeastern Freight Lines
HIPSHIPPER
Hipshipper
HDB
Haidaibao
RPXLOGISTICS
RPX Logistics
MIKROPAKKET_BE
Mikropakket Belgium
KUEHNE
Kuehne + Nagel
IT_NEXIVE
Nexive (TNT Post Italy)
PTS
PTS courier
ETS_EXPRESS
RETS express
SWISS_POST_FTP
Swiss Post FTP
COLIS_PRIVE
Colis Privé
FASTRK_SERV
Fastrak Services
4_72
4-72 Entregando
US_YRC
YRC courier
CN_YUNDA
Yunda Express
POSTNL_INTL_3S
PostNL International 3S
AAA_COOPER
AAA Cooper
ELIAN_POST
Yilian (Elian) Supply Chain
CUBYN
Cubyn
SAU_SAUDI_POST
Saudi Post
360LION
360 Lion Express
ABXEXPRESS_MY
ABX Express
NINJAVAN_WB
Ninjavan Webhook
ESP_PACKLINK
Packlink
IND_JAYONEXPRESS
Jayon Express (JEX)
GB_ARROW
Arrow XL
ZES_EXPRESS
Eshun international Logistic
IND_GOJAVAS
GoJavas
ZEPTO_EXPRESS
ZeptoExpress
SKYNET_ZA
Skynet World Wide Express South Africa
KPOST
Korea Post
ZEEK_2_DOOR
Zeek2Door
DHL_FREIGHT
DHL Freight
BLUECARE
Bluecare Express Ltd
BLINKLASTMILE
Blink
POSTA_UKR
UkrPoshta
LOGISTYX_TRANSGROUP
Transgroup courier
JINDOUYUN
jindouyun courier
CHROBINSON
C.H. Robinson Worldwide
TRACKON
Trackon Couriers Pvt. Ltd
CN_POST56
Post56
GB_TUFFNELLS
Tuffnells Parcels Express
COURANT_PLUS
Courant Plus
SCUDEX_EXPRESS
Scudex Express
SHIPENTEGRA
ShipEntegra
TRUMPCARD
TRUMPCARD LLC
CHOIR_EXP
Choir Express Indonesia
ETOTAL
eTotal Solution Limited
COPE
Cope Sensitive Freight
SFPLUS_WEBHOOK
Zeek courier
IND_GATI
Gati-KWE
HERMES_2MANN_HANDLING
Hermes Einrichtungs Service GmbH & Co. KG
CN_WISHPOST
WishPost
GLOBALTRANZ
GlobalTranz
HKD
Qingdao HKD International Logistics
UDS
United Delivery Service
BJSHOMEDELIVERY
BJS Distribution courier
YAKIT
Yakit courier
LEXSHIP
LexShip
OMNIVA
Omniva
SUTTON
Sutton Transport
COSTMETICSNOW
Cosmetics Now
PANTHER_REFERENCE
Panther Reference
SFCSERVICE
SFC Service
PFLOGISTICS
PFL
LTL
LTL COURIER
LOOMIS_EXPRESS
Loomis Express
PARKNPARCEL
Park N Parcel
SPRING_GDS
Spring GDS
GLS_ITALY
GLS Italy
ECEXPRESS
ECexpress
LINE
Line Clear Express & Logistics Sdn Bhd
INTERPARCEL_AU
Interparcel Australia
GEL_EXPRESS
Gel Express Logistik
AGILITY
Agility
XL_EXPRESS
XL Express
ADERONLINE
Ader couriers
DIRECTCOURIERS
Direct Couriers
PLANZER
Planzer Group
NOX_NIGHT_TIME_EXPRESS
NOX NightTimeExpress
SENDING
Sending Transporte Urgente y Comunicacion
HUODULL
Huodull
carrier_name_other
string
[ 1 .. 2000 ] characters
^.*$
The name of carrier in free-form text for unavailable carriers. This field is mandatory when
carrier_name
is
OTHER
.
tracking_url
string
<
uri
>
The URL to track the dispute-related transaction shipment.
tracking_number
required
string
[ 1 .. 255 ] characters
^.*$
The number to track the dispute-related transaction shipment.
Copy
{
"carrier_name"
:
"UPS"
,
"carrier_name_other"
:
"string"
,
"tracking_url"
:
"
http://example.com
"
,
"tracking_number"
:
"string"
}
Return shipping address information
Merchant provided information regarding return shipping address.
save_to_profile
boolean
The merchant's preference to save the return shipping address to their account profile.
address
object
(
Portable Postal Address (Medium-Grained)
)
The return address for the item. Required when the customer must return an item to the merchant for the
MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED
dispute reason, especially if the refund amount is less than the dispute amount.
Copy
Expand all
Collapse all
{
"save_to_profile"
:
true
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
return_details
The return details for the product.
mode
string
[ 1 .. 255 ] characters
^[A-Z_]+$
The method that the customer used to return the product.
Enum Value
Description
SHIPPED
The customer shipped the product back to the merchant.
IN_PERSON
The customer returned the item to the merchant in person.
receipt
boolean
Indicates whether customer has the return receipt.
return_confirmation_number
string
[ 1 .. 255 ] characters
^[A-Za-z0-9:\-]+$
The confirmation number for the item return.
returned
boolean
If
true
, indicates that the item was returned but the seller refused to accept the return and if
false
, indicates the item was not attempted to return.
return_time
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
The date and time when the product was returned,
Internet date and time format
.
Copy
{
"mode"
:
"SHIPPED"
,
"receipt"
:
true
,
"return_confirmation_number"
:
"string"
,
"returned"
:
true
,
"return_time"
:
"stringstringstringst"
}
Scam Context.
The scam context for a dispute.
purchase_url
string
<
uri
>
The URL where the customer purchased the product.
payment_reason
string
[ 1 .. 512 ] characters
^(.|\r?\n)*$
The purpose of this payment.
notes
string
[ 1 .. 1024 ] characters
^(.|\r?\n)*$
Any additional information that may support the case.
expected_delivery_time
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
The expected delivery date and time of the item.
Copy
{
"purchase_url"
:
"
http://example.com
"
,
"payment_reason"
:
"string"
,
"notes"
:
"string"
,
"expected_delivery_time"
:
"string"
}
seller
The details for the merchant who receives the funds and fulfills the order. For example, merchant ID, and contact email address.
merchant_id
string
[ 1 .. 255 ] characters
^[0-9A-Za-z]+$
The PayPal account ID for the merchant.
name
string
[ 1 .. 2000 ] characters
^[^~!@#$%^*()_{}:|\t\n/]+$
The name of the merchant.
email
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
The email address for the merchant's PayPal account.
Copy
{
"merchant_id"
:
"string"
,
"name"
:
"string"
,
"email"
:
"string"
}
send_message
The merchant request to send a message to the other party.
message
required
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The message sent by the merchant to the other party.
Copy
{
"message"
:
"string"
}
service_details
The service details.
description
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The service description.
service_started
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Indicates whether the service was started or cancelled.
Enum Value
Description
YES
The service was started.
NO
The service was not started.
CANCELLED
The service was cancelled.
note
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
The customer specified note about the service usage.
sub_reasons
Array of
strings
[ 1 .. 10 ] items
An array of sub-reasons for the service issue.
purchase_url
string
<
uri
>
The URL of the merchant or marketplace site where the customer purchased the service.
Copy
Expand all
Collapse all
{
"description"
:
"string"
,
"service_started"
:
"YES"
,
"note"
:
"string"
,
"sub_reasons"
:
[
"string"
]
,
"purchase_url"
:
"
http://example.com
"
}
status
The overall status of the dispute, constant for all the parties involved at anytime during the dispute lifecycle.
string
(
status
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The overall status of the dispute, constant for all the parties involved at anytime during the dispute lifecycle.
Enum Value
Description
OPEN
The dispute is open.
WAITING_FOR_BUYER_RESPONSE
The dispute is waiting for a response from the customer.
WAITING_FOR_SELLER_RESPONSE
The dispute is waiting for a response from the merchant.
UNDER_REVIEW
The dispute is under review with PayPal.
RESOLVED
The dispute is resolved.
OTHER
The default status if the dispute does not have one of the other statuses.
Copy
"OPEN"
subsequent_action
The subsequent action.
links
Array of
objects
(
Link Description
)
[ 1 .. 10 ] items
An array of request-related
HATEOAS links
.
Copy
Expand all
Collapse all
{
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
supporting_info
A merchant- or customer-submitted supporting information.
notes
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
Any supporting notes.
documents
Array of
objects
(
document
)
[ 1 .. 100 ] items
An array of metadata for the documents which were uploaded as supporting information for the dispute.
source
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The source of the Information.
Enum Value
Description
SUBMITTED_BY_BUYER
Information was submitted by the customer.
SUBMITTED_BY_SELLER
Information was submitted by the merchant.
SUBMITTED_BY_PARTNER
Information was submitted by the partner.
provided_time
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
The date and time when the information was received, in
Internet date and time format
.
dispute_life_cycle_stage
string
(
dispute_lifecycle_stage
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The dispute life cycle stage for the supporting info.
Enum Value
Description
INQUIRY
A customer and merchant interact in an attempt to resolve a dispute without escalation to PayPal. Occurs when the customer:
Has not received goods or a service.
Reports that the received goods or service are not as described.
Needs more details, such as a copy of the transaction or a receipt.
CHARGEBACK
A customer or merchant escalates an inquiry to a claim, which authorizes PayPal to investigate the case and make a determination. Occurs only when the dispute channel is
INTERNAL
. This stage is a PayPal dispute lifecycle stage and not a credit card or debit card chargeback. All notes that the customer sends in this stage are visible to PayPal agents only. The customer must wait for PayPal’s response before the customer can take further action. In this stage, PayPal shares dispute details with the merchant, who can complete one of these actions:
Accept the claim.
Submit evidence to challenge the claim.
Make an offer to the customer to resolve the claim.
PRE_ARBITRATION
The first appeal stage for merchants. A merchant can appeal a chargeback if PayPal's decision is not in the merchant's favor. If the merchant does not appeal within the appeal period, PayPal considers the case resolved.
ARBITRATION
The second appeal stage for merchants. A merchant can appeal a dispute for a second time if the first appeal was denied. If the merchant does not appeal within the appeal period, the case returns to a resolved status in pre-arbitration stage.
Copy
Expand all
Collapse all
{
"notes"
:
"string"
,
"documents"
:
[
{
"name"
:
"string"
,
"url"
:
"
http://example.com
"
}
]
,
"source"
:
"SUBMITTED_BY_BUYER"
,
"provided_time"
:
"stringstringstringst"
,
"dispute_life_cycle_stage"
:
"INQUIRY"
}
transaction_info
The information about the disputed transaction.
buyer_transaction_id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID, as seen by the customer, for this transaction.
seller_transaction_id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-]+$
The ID, as seen by the merchant, for this transaction.
reference_id
string
[ 1 .. 255 ] characters
^.*$
The ID, as seen by the partner, for this transaction.
transaction_status
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The transaction status.
Enum Value
Description
COMPLETED
The transaction processing completed.
UNCLAIMED
The items in the transaction are unclaimed. If they are not claimed within 30 days, the funds are returned to the sender.
DENIED
The transaction was denied.
FAILED
The transaction failed.
HELD
The transaction is on hold.
PENDING
The transaction is waiting to be processed.
PARTIALLY_REFUNDED
The payment for the transaction was partially refunded.
REFUNDED
The payment for the transaction was successfully refunded.
REVERSED
The payment for the transaction was reversed due to a chargeback or other reversal type.
CANCELLED
The transaction is cancelled.
invoice_number
string
[ 1 .. 127 ] characters
^[A-Za-z0-9:\-|]+$
The ID of the invoice for the payment.
custom
string
[ 1 .. 2000 ] characters
^(.|\r?\n)*$
A free-text field that is entered by the merchant during checkout.
items
Array of
objects
(
item_info
)
[ 1 .. 100 ] items
An array of items that were purchased as part of the transaction.
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
The date and time when the transaction was created, in
Internet date and time format
. For example,
yyyy
-
MM
-
dd
T
HH
:
mm
:
ss
.
SSS
Z
.
gross_amount
object
(
Money
)
The gross amount of the transaction.
gross_asset
object
(
Cryptocurrency
)
The gross asset of the transaction.
buyer
object
(
buyer
)
The details for the customer who funds the payment. For example, the customer's first name, last name, and email address.
seller
object
(
seller
)
The details for the merchant who receives the funds and fulfills the order. For example, merchant ID, and contact email address.
Copy
Expand all
Collapse all
{
"buyer_transaction_id"
:
"string"
,
"seller_transaction_id"
:
"string"
,
"reference_id"
:
"string"
,
"transaction_status"
:
"COMPLETED"
,
"invoice_number"
:
"string"
,
"custom"
:
"string"
,
"items"
:
[
{
"item_id"
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
"item_quantity"
:
"string"
,
"partner_transaction_id"
:
"string"
,
"reason"
:
"MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
,
"notes"
:
"string"
,
"item_type"
:
"PRODUCT"
,
"dispute_amount"
:
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
"create_time"
:
"stringstringstringst"
,
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
"gross_asset"
:
{
"asset_symbol"
:
"BTC"
,
"quantity"
:
"string"
,
"quantity_in_subunits"
:
"string"
,
"decimals"
:
40
}
,
"buyer"
:
{
"name"
:
"string"
}
,
"seller"
:
{
"merchant_id"
:
"string"
,
"name"
:
"string"
,
"email"
:
"string"
}
}
