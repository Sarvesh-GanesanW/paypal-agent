# Subscriptions

Source: https://developer.paypal.com/docs/api/subscriptions/v1/

Subscriptions
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
Subscriptions
post
Create plan
get
List plans
get
Show plan details
patch
Update plan
post
Activate plan
post
Deactivate plan
post
Update pricing
post
Create subscription
get
List subscriptions
get
Show subscription details
patch
Update subscription
post
Revise plan or quantity of subscription
post
Suspend subscription
post
Cancel subscription
post
Activate subscription
post
Capture authorized payment on subscription
get
List transactions for subscription
Definitions
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
Subscriptions
(
1
)
?
This API is currently not supported by our SDK
You can use billing plans and subscriptions to create subscriptions that process recurring PayPal payments for physical or digital goods, or services. A plan includes pricing and billing cycle information that defines the amount and frequency of charge for a subscription. You can also define a fixed plan, such as a $5 basic plan or a volume- or graduated-based plan with pricing tiers based on the quantity purchased. For more information, see
Subscriptions Overview
.
Create plan
post
/v1/billing/plans
Try it
Creates a plan that defines pricing and billing cycle details for subscriptions.
Security
Oauth2
Request
header
Parameters
Prefer
string
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
PayPal-Request-Id
string
The server stores keys for 72 hours.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
product_id
required
string
= 22 characters
^PROD-[A-Z0-9]*$
The ID of the product created through Catalog Products API.
name
required
string
[ 1 .. 127 ] characters
^.*$
The plan name.
status
string
[ 1 .. 24 ] characters
^[A-Z_]+$
Default:
"ACTIVE"
The initial state of the plan. Allowed input values are CREATED and ACTIVE.
Enum Value
Description
CREATED
The plan was created. You cannot create subscriptions for a plan in this state.
INACTIVE
The plan is inactive.
ACTIVE
The plan is active. You can only create subscriptions for a plan in this state.
description
string
[ 1 .. 127 ] characters
^.*$
The detailed description of the plan.
billing_cycles
required
Array of
objects
(
billing_cycle
)
[ 1 .. 12 ] items
An array of billing cycles for trial billing and regular billing. A plan can have at most two trial cycles and only one regular cycle.
quantity_supported
boolean
Default:
false
Indicates whether you can subscribe to this plan by providing a quantity for the goods or service.
payment_preferences
required
object
(
payment_preferences
)
The payment preferences for a subscription.
merchant_preferences
object
(
merchant_preferences
)
The merchant preferences for a subscription.
taxes
object
(
taxes
)
The tax details.
Responses
201
A successful request returns the HTTP
201 Created
status code and a JSON response body that shows billing plan details.
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
Sample 1 - 201 - Create Flat Plan
Sample 1 - 201 - Create Flat Plan
Copy
Expand all
Collapse all
{
"product_id"
:
"PROD-XXCD1234QWER65782"
,
"name"
:
"Video Streaming Service Plan"
,
"description"
:
"Video Streaming Service basic plan"
,
"status"
:
"ACTIVE"
,
"billing_cycles"
:
[
{
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
"tenure_type"
:
"TRIAL"
,
"sequence"
:
1
,
"total_cycles"
:
2
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"value"
:
"3"
,
"currency_code"
:
"USD"
}
}
}
,
{
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
"tenure_type"
:
"TRIAL"
,
"sequence"
:
2
,
"total_cycles"
:
3
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"value"
:
"6"
,
"currency_code"
:
"USD"
}
}
}
,
{
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
"tenure_type"
:
"REGULAR"
,
"sequence"
:
3
,
"total_cycles"
:
12
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"value"
:
"10"
,
"currency_code"
:
"USD"
}
}
}
]
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee"
:
{
"value"
:
"10"
,
"currency_code"
:
"USD"
}
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
3
}
,
"taxes"
:
{
"percentage"
:
"10"
,
"inclusive"
:
false
}
}
Response samples
201
application/json
Sample 1 - 201 - Create Flat Plan
Sample 1 - 201 - Create Flat Plan
Copy
Expand all
Collapse all
{
"id"
:
"P-5ML4271244454362WXNWU5NQ"
,
"product_id"
:
"PROD-XXCD1234QWER65782"
,
"name"
:
"Video Streaming Service Plan"
,
"description"
:
"Video Streaming Service basic plan"
,
"status"
:
"ACTIVE"
,
"billing_cycles"
:
[
{
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
"tenure_type"
:
"TRIAL"
,
"sequence"
:
1
,
"total_cycles"
:
2
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"value"
:
"3"
,
"currency_code"
:
"USD"
}
,
"version"
:
1
,
"create_time"
:
"2020-05-27T12:13:51Z"
,
"update_time"
:
"2020-05-27T12:13:51Z"
}
}
,
{
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
"tenure_type"
:
"TRIAL"
,
"sequence"
:
2
,
"total_cycles"
:
3
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"currency_code"
:
"USD"
,
"value"
:
"6"
}
,
"version"
:
1
,
"create_time"
:
"2020-05-27T12:13:51Z"
,
"update_time"
:
"2020-05-27T12:13:51Z"
}
}
,
{
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
"tenure_type"
:
"REGULAR"
,
"sequence"
:
3
,
"total_cycles"
:
12
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10"
}
,
"version"
:
1
,
"create_time"
:
"2020-05-27T12:13:51Z"
,
"update_time"
:
"2020-05-27T12:13:51Z"
}
}
]
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee"
:
{
"value"
:
"10"
,
"currency_code"
:
"USD"
}
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
3
}
,
"taxes"
:
{
"percentage"
:
"10"
,
"inclusive"
:
false
}
,
"create_time"
:
"2020-05-27T12:13:51Z"
,
"update_time"
:
"2020-05-27T12:13:51Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-5ML4271244454362WXNWU5NQ
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
https://api-m.paypal.com/v1/billing/plans/P-5ML4271244454362WXNWU5NQ
"
,
"rel"
:
"edit"
,
"method"
:
"PATCH"
}
,
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-5ML4271244454362WXNWU5NQ/deactivate
"
,
"rel"
:
"deactivate"
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
https://api-m.paypal.com/v1/billing/plans/P-5ML4271244454362WXNWU5NQ/update-pricing-schemes
"
,
"rel"
:
"edit"
,
"method"
:
"POST"
}
]
}
List plans
get
/v1/billing/plans
Try it
Lists billing plans.
Security
Oauth2
Request
query
Parameters
product_id
string
[ 6 .. 50 ] characters
Filters the response by a Product ID.
page_size
integer
[ 1 .. 20 ]
Default:
10
The number of items to return in the response.
page
integer
[ 1 .. 100000 ]
Default:
1
A non-zero integer which is the start index of the entire list of items to return in the response. The combination of
page=1
and
page_size=20
returns the first 20 items. The combination of
page=2
and
page_size=20
returns the next 20 items.
total_required
boolean
Default:
false
Indicates whether to show the total count in the response.
header
Parameters
Prefer
string
Default:
return=minimal
The preferred server response upon successful completion of the request. Value is:
return=minimal
. The server returns a minimal response to optimize communication between the API caller and the server. A minimal response includes the
id
,
name
,
description
and HATEOAS links.
return=representation
. The server returns a complete resource representation, including the current state of the resource.
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
status code and a JSON response body that lists billing plans.
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
Sample 1 - 200 - Get the list of plan in descending order
Sample 1 - 200 - Get the list of plan in descending order
Copy
Expand all
Collapse all
{
"plans"
:
[
{
"id"
:
"P-9CT60829WM695623HL7QGYOI"
,
"name"
:
"Netflix Plan 17012019"
,
"status"
:
"ACTIVE"
,
"description"
:
"Netflix basic plan"
,
"usage_type"
:
"LICENSED"
,
"create_time"
:
"2020-12-23T07:08:40Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-9CT60829WM695623HL7QGYOI
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
"id"
:
"P-7CE83846EJ264184CL7QHL3I"
,
"name"
:
"Netflix Plan 17012019"
,
"status"
:
"CREATED"
,
"description"
:
"Netflix basic plan"
,
"usage_type"
:
"LICENSED"
,
"create_time"
:
"2020-12-23T07:06:08Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-7CE83846EJ264184CL7QHL3I
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
"id"
:
"P-1HG35083DU289225LL7QIDKA"
,
"name"
:
"Netflix Plan 17012019"
,
"status"
:
"ACTIVE"
,
"description"
:
"Netflix basic plan"
,
"usage_type"
:
"LICENSED"
,
"create_time"
:
"2020-12-22T06:41:26Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-1HG35083DU289225LL7QIDKA
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
"id"
:
"P-5V279629EP569145RL7QZKFQ"
,
"name"
:
"Netflix Plan 17012019"
,
"status"
:
"CREATED"
,
"description"
:
"Netflix basic plan"
,
"usage_type"
:
"LICENSED"
,
"create_time"
:
"2020-12-21T11:06:16Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-5V279629EP569145RL7QZKFQ
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
"id"
:
"P-69D48725TK8139022L7ROYYA"
,
"name"
:
"Netflix Plan 17012019"
,
"status"
:
"ACTIVE"
,
"description"
:
"Netflix basic plan"
,
"usage_type"
:
"LICENSED"
,
"create_time"
:
"2020-12-21T10:16:13Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-69D48725TK8139022L7ROYYA
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
"id"
:
"P-87R81207W88552156L7ROZ6A"
,
"name"
:
"Netflix Plan 17012019"
,
"status"
:
"ACTIVE"
,
"description"
:
"Netflix basic plan"
,
"usage_type"
:
"LICENSED"
,
"create_time"
:
"2020-12-21T09:34:49Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-87R81207W88552156L7ROZ6A
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
https://api-m.paypal.com/v1/billing/plans?page_size=10&page=1
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
Show plan details
get
/v1/billing/plans/{id}
Try it
Shows details for a plan, by ID.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the plan.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows plan details.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v1/billing/plans/P-5ML4271244454362WXNWU5NQ
\
-H
'Authorization: Bearer access_token6V7rbVwmlM1gFZKW_8QtzWXqpcwQ6T5vhEGYNJDAAdn3paCgRpdeMdVYmWzgbKSsECednupJ3Zx5Xd-g'
\
-H
'Content-Type: application/json'
\
-H
'Accept: application/json'
Response samples
200
application/json
Sample 1 - 200 - Get Plan details for flat plan
Sample 1 - 200 - Get Plan details for flat plan
Copy
Expand all
Collapse all
{
"id"
:
"P-5ML4271244454362WXNWU5NQ"
,
"product_id"
:
"PROD-XXCD1234QWER65782"
,
"name"
:
"Basic Plan"
,
"description"
:
"Basic Plan"
,
"status"
:
"ACTIVE"
,
"billing_cycles"
:
[
{
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
"tenure_type"
:
"TRIAL"
,
"sequence"
:
1
,
"total_cycles"
:
2
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"currency_code"
:
"USD"
,
"value"
:
"3"
}
,
"version"
:
1
,
"create_time"
:
"2020-05-27T12:13:51Z"
,
"update_time"
:
"2020-05-27T12:13:51Z"
}
}
,
{
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
"tenure_type"
:
"TRIAL"
,
"sequence"
:
2
,
"total_cycles"
:
3
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"currency_code"
:
"USD"
,
"value"
:
"6"
}
,
"version"
:
1
,
"create_time"
:
"2020-05-27T12:13:51Z"
,
"update_time"
:
"2020-05-27T12:13:51Z"
}
}
,
{
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
"tenure_type"
:
"REGULAR"
,
"sequence"
:
3
,
"total_cycles"
:
12
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"value"
:
"10"
,
"currency_code"
:
"USD"
}
,
"status"
:
"ACTIVE"
,
"version"
:
1
,
"create_time"
:
"2020-05-27T12:13:51Z"
,
"update_time"
:
"2020-05-27T12:13:51Z"
}
}
]
,
"taxes"
:
{
"percentage"
:
"10"
,
"inclusive"
:
false
}
,
"create_time"
:
"2020-05-27T12:13:51Z"
,
"update_time"
:
"2020-05-27T12:13:51Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-5ML4271244454362WXNWU5NQ
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
https://api-m.paypal.com/v1/billing/plans/P-5ML4271244454362WXNWU5NQ
"
,
"rel"
:
"edit"
,
"method"
:
"PATCH"
}
,
{
"href"
:
"
https://api-m.paypal.com/v1/billing/plans/P-5ML4271244454362WXNWU5NQ/deactivate
"
,
"rel"
:
"deactivate"
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
https://api-m.paypal.com/v1/billing/plans/P-5ML4271244454362WXNWU5NQ/update-pricing-schemes
"
,
"rel"
:
"edit"
,
"method"
:
"POST"
}
]
}
Update plan
patch
/v1/billing/plans/{id}
Try it
Updates a plan with the
CREATED
or
ACTIVE
status. For an
INACTIVE
plan, you can make only status updates.
You can patch these attributes and objects:
Attribute or object
Operations
description
replace
payment_preferences.auto_bill_outstanding
replace
taxes.percentage
replace
payment_preferences.payment_failure_threshold
replace
payment_preferences.setup_fee
replace
payment_preferences.setup_fee_failure_action
replace
name
replace
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the plan.
Request Body schema:
application/json
Array
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
Sample 1 - 204 - Patch a plan
Sample 1 - 204 - Patch a plan
Copy
Expand all
Collapse all
[
{
"op"
:
"replace"
,
"path"
:
"/payment_preferences/payment_failure_threshold"
,
"value"
:
7
}
,
{
"op"
:
"replace"
,
"path"
:
"/name"
,
"value"
:
"Updated Video Streaming Service Plan"
}
]
Response samples
204
application/json
Sample 1 - 204 - Patch a plan
Sample 1 - 204 - Patch a plan
Copy
{ }
Activate plan
post
/v1/billing/plans/{id}/activate
Try it
Activates a plan, by ID.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the plan.
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
Sample 1 - 204 - Activate Plan
Sample 1 - 204 - Activate Plan
Copy
{ }
Response samples
204
application/json
Sample 1 - 204 - Activate Plan
Sample 1 - 204 - Activate Plan
Copy
{ }
Deactivate plan
post
/v1/billing/plans/{id}/deactivate
Try it
Deactivates a plan, by ID.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the plan.
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
Sample 1 - 204 - Deactivate Plan
Sample 1 - 204 - Deactivate Plan
Copy
{ }
Response samples
204
application/json
Sample 1 - 204 - Deactivate Plan
Sample 1 - 204 - Deactivate Plan
Copy
{ }
Update pricing
post
/v1/billing/plans/{id}/update-pricing-schemes
Try it
Updates pricing for a plan. For example, you can update a regular billing cycle from $5 per month to $7 per month.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID for the plan.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
pricing_schemes
required
Array of
objects
(
update_pricing_scheme_request
)
[ 1 .. 99 ] items
An array of pricing schemes.
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
Sample 1 - 204 - Add multiple tiered pricing schemes
Sample 1 - 204 - Add multiple tiered pricing schemes
Copy
Expand all
Collapse all
{
"pricing_schemes"
:
[
{
"billing_cycle_sequence"
:
1
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"value"
:
"50"
,
"currency_code"
:
"USD"
}
}
}
,
{
"billing_cycle_sequence"
:
2
,
"pricing_scheme"
:
{
"fixed_price"
:
{
"value"
:
"100"
,
"currency_code"
:
"USD"
}
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"1"
,
"ending_quantity"
:
"1000"
,
"amount"
:
{
"value"
:
"150"
,
"currency_code"
:
"USD"
}
}
,
{
"starting_quantity"
:
"1001"
,
"amount"
:
{
"value"
:
"250"
,
"currency_code"
:
"USD"
}
}
]
}
}
]
}
Response samples
204
application/json
Sample 1 - 204 - Add multiple tiered pricing schemes
Sample 1 - 204 - Add multiple tiered pricing schemes
Copy
{ }
Create subscription
post
/v1/billing/subscriptions
Try it
Creates a subscription.
Security
Oauth2
Request
header
Parameters
Prefer
string
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
PayPal-Request-Id
string
The server stores keys for 72 hours.
PayPal-Client-Metadata-Id
string
[ 1 .. 36 ] characters
The PayPal Client Metadata Id(CMID) is used to provide device-specific information to PayPal's risk engine. This is crucial for transactions that require device-specific risk assessments. Merchants typically use the Paypal SDK that automatically submits the CMID or they use tools like Fraudnet JS for web or Magnes JS for mobile to generate the CMID on the frontend and then pass it to the API as part of the request headers.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
plan_id
required
string
= 26 characters
^P-[A-Z0-9]*$
The ID of the plan.
quantity
string
[ 1 .. 32 ] characters
^([0-9]+|([0-9]+)?[.][0-9]+)$
The quantity of the product in the subscription.
auto_renewal
boolean
Default:
false
DEPRECATED. Indicates whether the subscription auto-renews after the billing cycles complete.
custom_id
string
[ 1 .. 127 ] characters
^[\x20-\x7E]+
The custom id for the subscription. Can be invoice id.
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
Default:
"Current time"
The date and time when the subscription started, in
Internet date and time format
.
shipping_amount
object
(
Money
)
The shipping charges.
subscriber
object
<
payer_v1
>
(
subscriber_request
)
The subscriber request information .
application_context
object
(
application_context
)
DEPRECATED. The application context, which customizes the payer experience during the subscription approval process with PayPal.
plan
object
(
plan_override
)
An inline plan object to customise the subscription. You can override plan level default attributes by providing customised values for the subscription in this object.
Responses
201
A successful request returns the HTTP
201 Created
status code and a JSON response body that shows subscription details.
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
Sample 1 - 201 - Create Subscription for Plan
Sample 1 - 201 - Create Subscription for Plan
Copy
Expand all
Collapse all
{
"plan_id"
:
"P-5ML4271244454362WXNWU5NQ"
,
"start_time"
:
"2018-11-01T00:00:00Z"
,
"quantity"
:
"20"
,
"shipping_amount"
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
"subscriber"
:
{
"name"
:
{
"given_name"
:
"John"
,
"surname"
:
"Doe"
}
,
"email_address"
:
"
[email protected]
"
,
"shipping_address"
:
{
"name"
:
{
"full_name"
:
"John Doe"
}
,
"address"
:
{
"address_line_1"
:
"2211 N First Street"
,
"address_line_2"
:
"Building 17"
,
"admin_area_2"
:
"San Jose"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"95131"
,
"country_code"
:
"US"
}
}
}
,
"application_context"
:
{
"brand_name"
:
"walmart"
,
"locale"
:
"en-US"
,
"shipping_preference"
:
"SET_PROVIDED_ADDRESS"
,
"user_action"
:
"SUBSCRIBE_NOW"
,
"payment_method"
:
{
"payer_selected"
:
"PAYPAL"
,
"payee_preferred"
:
"IMMEDIATE_PAYMENT_REQUIRED"
}
,
"return_url"
:
"
https://example.com/returnUrl
"
,
"cancel_url"
:
"
https://example.com/cancelUrl
"
}
}
Response samples
201
application/json
Sample 1 - 201 - Create Subscription for Plan
Sample 1 - 201 - Create Subscription for Plan
Copy
Expand all
Collapse all
{
"id"
:
"I-BW452GLLEP1G"
,
"status"
:
"APPROVAL_PENDING"
,
"status_update_time"
:
"2018-12-10T21:20:49Z"
,
"plan_id"
:
"P-5ML4271244454362WXNWU5NQ"
,
"plan_overridden"
:
false
,
"start_time"
:
"2018-11-01T00:00:00Z"
,
"quantity"
:
"20"
,
"shipping_amount"
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
"subscriber"
:
{
"name"
:
{
"given_name"
:
"John"
,
"surname"
:
"Doe"
}
,
"email_address"
:
"
[email protected]
"
,
"payer_id"
:
"2BBBB8YJQSCCC"
,
"shipping_address"
:
{
"name"
:
{
"full_name"
:
"John Doe"
}
,
"address"
:
{
"address_line_1"
:
"2211 N First Street"
,
"address_line_2"
:
"Building 17"
,
"admin_area_2"
:
"San Jose"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"95131"
,
"country_code"
:
"US"
}
}
}
,
"create_time"
:
"2018-12-10T21:20:49Z"
,
"links"
:
[
{
"href"
:
"
https://www.paypal.com/webapps/billing/subscriptions?ba_token=BA-2M539689T3856352J
"
,
"rel"
:
"approve"
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
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G
"
,
"rel"
:
"edit"
,
"method"
:
"PATCH"
}
,
{
"href"
:
"
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G
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
List subscriptions
get
/v1/billing/subscriptions
Try it
List all subscriptions for merchant account.
Security
Oauth2
Request
query
Parameters
plan_ids
string
[ 3 .. 1890 ]
Filters the response by list of plan IDs. Filter supports upto
70
plan IDs. URLs should not exceed a length of
2000
characters.
statuses
string
[ 1 .. 70 ] characters
^[A-Z_,]+$
Filters the response by list of subscription statuses.
created_after
string
<
ppaas_date_time_v3
>
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
Filters the response by subscription creation start time for a range of subscriptions.
created_before
string
<
ppaas_date_time_v3
>
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
Filters the response by subscription creation end time for a range of subscriptions.
status_updated_before
string
<
ppaas_date_time_v3
>
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
Filters the response by status update start time for a range of subscriptions.
status_updated_after
string
<
ppaas_date_time_v3
>
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
Filters the response by status update end time for a range of subscriptions.
filter
string
[ 0 .. 100 ] characters
Filter the response using complex expressions that could use comparison operators like ge, gt, le, lt and logical operators such as 'and' and 'or'.
page_size
integer
[ 1 .. 20 ]
Default:
10
The number of items to return in the response.
page
integer
[ 1 .. 10000000 ]
Default:
1
A non-zero integer which is the start index of the entire list of items to return in the response. The combination of
page=1
and
page_size=20
returns the first 20 items. The combination of
page=2
and
page_size=20
returns the next 20 items.
customer_ids
Array of
strings
[ 1 .. 10 ] items
Filters the response by comma separated vault customer IDs (FSS subscriptions only).
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
status code and a JSON response body that lists the subscriptions.
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
Sample 1 - 200 - Get the list of all subscriptions FSS
Sample 1 - 200 - Get the list of all subscriptions FSS
Copy
Expand all
Collapse all
{
"subscriptions"
:
[
{
"status"
:
"ACTIVE"
,
"status_change_note"
:
"Items back in stock"
,
"status_update_time"
:
"2025-07-30T22:10:24Z"
,
"id"
:
"I-EXAU4TK3PGT8"
,
"plan_id"
:
"P-0JM77213960387536NCFE5AQ"
,
"start_time"
:
"2025-07-30T17:10:25Z"
,
"quantity"
:
"1"
,
"shipping_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"0.0"
}
,
"subscriber"
:
{
"email_address"
:
"
[email protected]
"
,
"name"
:
{
"given_name"
:
"Sanity"
,
"surname"
:
"Test"
}
,
"tenant"
:
"PAYPAL"
,
"shipping_address"
:
{
"name"
:
{
"given_name"
:
"Mit"
,
"surname"
:
"Token Sanity"
}
,
"address"
:
{
"address_line_1"
:
"2211 N First Street"
,
"address_line_2"
:
"Building 10"
,
"admin_area_2"
:
"San Jose"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"95131"
,
"country_code"
:
"US"
}
}
,
"payment_source"
:
{
"card"
:
{
"name"
:
"John Doe"
,
"last_digits"
:
"1026"
,
"brand"
:
"VISA"
,
"attributes"
:
{
"vault"
:
{
"id"
:
"93a92571rv649072p"
,
"customer"
:
{
"id"
:
"CEhQvabkXs"
}
}
}
,
"expiry"
:
"2026-02"
}
}
}
,
"billing_info"
:
{
"outstanding_balance"
:
{
"currency_code"
:
"USD"
,
"value"
:
"0.0"
}
,
"cycle_executions"
:
[
{
"tenure_type"
:
"TRIAL"
,
"sequence"
:
1
,
"cycles_completed"
:
1
,
"cycles_remaining"
:
0
,
"current_pricing_scheme_version"
:
1
,
"total_cycles"
:
1
}
,
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
2
,
"cycles_completed"
:
0
,
"cycles_remaining"
:
100
,
"current_pricing_scheme_version"
:
1
,
"total_cycles"
:
100
}
]
,
"last_payment"
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
"5.0"
}
,
"time"
:
"2025-07-30T17:10:32Z"
}
,
"next_billing_time"
:
"2025-07-31T10:00:00Z"
,
"final_payment_time"
:
"2025-11-07T10:00:00Z"
,
"failed_payments_count"
:
0
}
,
"create_time"
:
"2025-07-30T17:10:28Z"
,
"update_time"
:
"2025-07-30T22:10:24Z"
,
"plan_overridden"
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
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-EXAU4TK3PGT8/cancel
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
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-EXAU4TK3PGT8
"
,
"rel"
:
"edit"
,
"method"
:
"PATCH"
}
,
{
"href"
:
"
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-EXAU4TK3PGT8
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
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-EXAU4TK3PGT8/suspend
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
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-EXAU4TK3PGT8/capture
"
,
"rel"
:
"capture"
,
"method"
:
"POST"
}
]
}
,
{
"status"
:
"ACTIVE"
,
"status_change_note"
:
"Items back in stock"
,
"status_update_time"
:
"2025-07-30T22:10:24Z"
,
"id"
:
"I-BW452GLLEP1G"
,
"plan_id"
:
"P-5ML4271244454362WXNWU5NQ"
,
"start_time"
:
"2025-07-30T17:10:25Z"
,
"quantity"
:
"1"
,
"shipping_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"0.0"
}
,
"subscriber"
:
{
"email_address"
:
"
[email protected]
"
,
"name"
:
{
"given_name"
:
"Sanity"
,
"surname"
:
"Test"
}
,
"tenant"
:
"PAYPAL"
,
"shipping_address"
:
{
"name"
:
{
"given_name"
:
"Mit"
,
"surname"
:
"Token Sanity"
}
,
"address"
:
{
"address_line_1"
:
"2211 N First Street"
,
"address_line_2"
:
"Building 10"
,
"admin_area_2"
:
"San Jose"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"95131"
,
"country_code"
:
"US"
}
}
,
"payment_source"
:
{
"card"
:
{
"name"
:
"John Doe"
,
"last_digits"
:
"1026"
,
"brand"
:
"VISA"
,
"attributes"
:
{
"vault"
:
{
"id"
:
"93a92571rv649072p"
,
"customer"
:
{
"id"
:
"CEhQvabkXs"
}
}
}
,
"expiry"
:
"2026-02"
}
}
}
,
"billing_info"
:
{
"outstanding_balance"
:
{
"currency_code"
:
"USD"
,
"value"
:
"0.0"
}
,
"cycle_executions"
:
[
{
"tenure_type"
:
"TRIAL"
,
"sequence"
:
1
,
"cycles_completed"
:
1
,
"cycles_remaining"
:
0
,
"current_pricing_scheme_version"
:
1
,
"total_cycles"
:
1
}
,
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
2
,
"cycles_completed"
:
0
,
"cycles_remaining"
:
100
,
"current_pricing_scheme_version"
:
1
,
"total_cycles"
:
100
}
]
,
"last_payment"
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
"5.0"
}
,
"time"
:
"2025-07-30T17:10:32Z"
}
,
"next_billing_time"
:
"2025-07-31T10:00:00Z"
,
"final_payment_time"
:
"2025-11-07T10:00:00Z"
,
"failed_payments_count"
:
0
}
,
"create_time"
:
"2025-07-30T17:10:28Z"
,
"update_time"
:
"2025-07-30T22:10:24Z"
,
"plan_overridden"
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
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/cancel
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
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G
"
,
"rel"
:
"edit"
,
"method"
:
"PATCH"
}
,
{
"href"
:
"
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G
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
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/suspend
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
https://api.sandbox.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/capture
"
,
"rel"
:
"capture"
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
https://api-m.paypal.com/v1/billing/subscriptions?page_size=10&page=1&customer_ids=kmHnwzGFRA
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
Show subscription details
get
/v1/billing/subscriptions/{id}
Try it
Shows details for a subscription, by ID.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the subscription.
query
Parameters
fields
string
[ 1 .. 100 ] characters
List of fields that are to be returned in the response. Possible value for fields are last_failed_payment and plan.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows subscription details.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G
\
-H
'Authorization: Bearer access_token6V7rbVwmlM1gFZKW_8QtzWXqpcwQ6T5vhEGYNJDAAdn3paCgRpdeMdVYmWzgbKSsECednupJ3Zx5Xd-g'
\
-H
'Content-Type: application/json'
\
-H
'Accept: application/json'
Response samples
200
application/json
Sample 1 - 200 - Get active subscription details
Sample 1 - 200 - Get active subscription details
Copy
Expand all
Collapse all
{
"id"
:
"I-BW452GLLEP1G"
,
"plan_id"
:
"P-5ML4271244454362WXNWU5NQ"
,
"start_time"
:
"2019-04-10T07:00:00Z"
,
"quantity"
:
"20"
,
"shipping_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10.0"
}
,
"subscriber"
:
{
"shipping_address"
:
{
"name"
:
{
"full_name"
:
"John Doe"
}
,
"address"
:
{
"address_line_1"
:
"2211 N First Street"
,
"address_line_2"
:
"Building 17"
,
"admin_area_2"
:
"San Jose"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"95131"
,
"country_code"
:
"US"
}
}
,
"name"
:
{
"given_name"
:
"John"
,
"surname"
:
"Doe"
}
,
"email_address"
:
"
[email protected]
"
,
"payer_id"
:
"2BBBB8YJQSCCC"
}
,
"billing_info"
:
{
"outstanding_balance"
:
{
"currency_code"
:
"USD"
,
"value"
:
"1.0"
}
,
"cycle_executions"
:
[
{
"tenure_type"
:
"TRIAL"
,
"sequence"
:
1
,
"cycles_completed"
:
0
,
"cycles_remaining"
:
2
,
"total_cycles"
:
2
}
,
{
"tenure_type"
:
"TRIAL"
,
"sequence"
:
2
,
"cycles_completed"
:
0
,
"cycles_remaining"
:
3
,
"total_cycles"
:
3
}
,
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
3
,
"cycles_completed"
:
0
,
"cycles_remaining"
:
12
,
"total_cycles"
:
12
}
]
,
"last_payment"
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
"1.15"
}
,
"time"
:
"2019-04-09T10:27:20Z"
}
,
"next_billing_time"
:
"2019-04-10T10:00:00Z"
,
"failed_payments_count"
:
0
}
,
"create_time"
:
"2019-04-09T10:26:04Z"
,
"update_time"
:
"2019-04-09T10:27:27Z"
,
"links"
:
[
{
"href"
:
"
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/cancel
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
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G
"
,
"rel"
:
"edit"
,
"method"
:
"PATCH"
}
,
{
"href"
:
"
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G
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
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/suspend
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
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/capture
"
,
"rel"
:
"capture"
,
"method"
:
"POST"
}
]
,
"status"
:
"ACTIVE"
,
"status_update_time"
:
"2019-04-09T10:27:27Z"
}
Update subscription
patch
/v1/billing/subscriptions/{id}
Try it
Updates a subscription which could be in
ACTIVE
or
SUSPENDED
status. You can override plan level default attributes by providing customised values for plan path in the patch request.
You cannot update attributes that have already completed (Example - trial cycles can’t be updated if completed).
Once overridden, changes to plan resource will not impact subscription.
Any price update will not impact billing cycles within next 10 days (Applicable only for subscriptions funded by PayPal account).
Following are the fields eligible for patch.
Attribute or object
Operations
billing_info.outstanding_balance
replace
custom_id
add,replace
plan.billing_cycles[@sequence==n].
pricing_scheme.fixed_price
add,replace
plan.billing_cycles[@sequence==n].
pricing_scheme.tiers
replace
plan.billing_cycles[@sequence==n].
total_cycles
replace
plan.payment_preferences.
auto_bill_outstanding
replace
plan.payment_preferences.
payment_failure_threshold
replace
plan.taxes.inclusive
add,replace
plan.taxes.percentage
add,replace
shipping_amount
add,replace
start_time
replace
subscriber.shipping_address
add,replace
subscriber.payment_source (for subscriptions funded
by card payments)
replace
Security
Oauth2
Request
path
Parameters
id
required
string
The ID for the subscription.
Request Body schema:
application/json
Array
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
Sample 1 - 204 - Patch subscription level plan attributes
Sample 1 - 204 - Patch subscription level plan attributes
Copy
Expand all
Collapse all
[
{
"op"
:
"replace"
,
"path"
:
"/plan/billing_cycles/@sequence==1/pricing_scheme/fixed_price"
,
"value"
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
{
"op"
:
"replace"
,
"path"
:
"/plan/billing_cycles/@sequence==2/pricing_scheme/tiers"
,
"value"
:
[
{
"starting_quantity"
:
"1"
,
"ending_quantity"
:
"1000"
,
"amount"
:
{
"value"
:
"500"
,
"currency_code"
:
"USD"
}
}
,
{
"starting_quantity"
:
"1001"
,
"amount"
:
{
"value"
:
"2000"
,
"currency_code"
:
"USD"
}
}
]
}
,
{
"op"
:
"replace"
,
"path"
:
"/plan/payment_preferences/auto_bill_outstanding"
,
"value"
:
true
}
,
{
"op"
:
"replace"
,
"path"
:
"/plan/payment_preferences/payment_failure_threshold"
,
"value"
:
1
}
,
{
"op"
:
"replace"
,
"path"
:
"/plan/taxes/percentage"
,
"value"
:
"10"
}
]
Response samples
204
application/json
Sample 1 - 204 - Patch subscription level plan attributes
Sample 1 - 204 - Patch subscription level plan attributes
Copy
{ }
Revise plan or quantity of subscription
post
/v1/billing/subscriptions/{id}/revise
Try it
Updates the quantity of the product or service in a subscription. You can also use this method to switch the plan and update the
shipping_amount
,
shipping_address
values for the subscription. This type of update requires the buyer's consent.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the subscription.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
plan_id
string
= 26 characters
^P-[A-Z0-9]*$
The unique PayPal-generated ID for the plan.
quantity
string
[ 1 .. 32 ] characters
^([0-9]+|([0-9]+)?[.][0-9]+)$
The quantity of the product or service in the subscription.
shipping_amount
object
(
Money
)
The shipping charges.
shipping_address
object
(
shipping_detail
)
The shipping address of the subscriber.
application_context
object
(
application_context
)
The application context, which customizes the payer experience during the subscription approval process with PayPal.
plan
object
(
plan_override
)
An inline plan object to customise the subscription. You can override plan level default attributes by providing customised values for the subscription in this object. Any existing overrides will not be carried forward during subscription revise.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows subscription details.
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
Sample 1 - 200 - Upgrade/downgrade subscription - Change Plan
Sample 1 - 200 - Upgrade/downgrade subscription - Change Plan
Copy
Expand all
Collapse all
{
"plan_id"
:
"P-5ML4271244454362WXNWU5NQ"
,
"shipping_amount"
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
"shipping_address"
:
{
"name"
:
{
"full_name"
:
"John Doe"
}
,
"address"
:
{
"address_line_1"
:
"2211 N First Street"
,
"address_line_2"
:
"Building 17"
,
"admin_area_2"
:
"San Jose"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"95131"
,
"country_code"
:
"US"
}
}
,
"application_context"
:
{
"brand_name"
:
"walmart"
,
"locale"
:
"en-US"
,
"shipping_preference"
:
"SET_PROVIDED_ADDRESS"
,
"payment_method"
:
{
"payer_selected"
:
"PAYPAL"
,
"payee_preferred"
:
"IMMEDIATE_PAYMENT_REQUIRED"
}
,
"return_url"
:
"
https://example.com/returnUrl
"
,
"cancel_url"
:
"
https://example.com/cancelUrl
"
}
}
Response samples
200
application/json
Sample 1 - 200 - Upgrade/downgrade subscription - Change Plan
Sample 1 - 200 - Upgrade/downgrade subscription - Change Plan
Copy
Expand all
Collapse all
{
"plan_id"
:
"P-5ML4271244454362WXNWU5NQ"
,
"plan_overridden"
:
false
,
"shipping_amount"
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
"shipping_address"
:
{
"name"
:
{
"full_name"
:
"John Doe"
}
,
"address"
:
{
"address_line_1"
:
"2211 N First Street"
,
"address_line_2"
:
"Building 17"
,
"admin_area_2"
:
"San Jose"
,
"admin_area_1"
:
"CA"
,
"postal_code"
:
"95131"
,
"country_code"
:
"US"
}
}
,
"links"
:
[
{
"href"
:
"
https://www.paypal.com/webapps/billing/subscriptions/update?ba_token=BA-2M539689T3856352J
"
,
"rel"
:
"approve"
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
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G
"
,
"rel"
:
"edit"
,
"method"
:
"PATCH"
}
,
{
"href"
:
"
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G
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
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/cancel
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
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/suspend
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
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/capture
"
,
"rel"
:
"capture"
,
"method"
:
"POST"
}
]
}
Suspend subscription
post
/v1/billing/subscriptions/{id}/suspend
Try it
Suspends the subscription.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the subscription.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
reason
required
string
[ 1 .. 128 ] characters
^.*$
The reason for suspension of the Subscription.
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
Sample 1 - 204 - Suspend an existing subscription
Sample 1 - 204 - Suspend an existing subscription
Copy
{
"reason"
:
"Item out of stock"
}
Response samples
204
application/json
Sample 1 - 204 - Suspend an existing subscription
Sample 1 - 204 - Suspend an existing subscription
Copy
{ }
Cancel subscription
post
/v1/billing/subscriptions/{id}/cancel
Try it
Cancels the subscription.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the subscription.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
reason
required
string
[ 1 .. 128 ] characters
^.*$
The reason for the cancellation of a subscription.
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
Sample 1 - 204 - Cancel an existing subscription
Sample 1 - 204 - Cancel an existing subscription
Copy
{
"reason"
:
"Not satisfied with the service"
}
Response samples
204
application/json
Sample 1 - 204 - Cancel an existing subscription
Sample 1 - 204 - Cancel an existing subscription
Copy
{ }
Activate subscription
post
/v1/billing/subscriptions/{id}/activate
Try it
Activates the subscription.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the subscription.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
reason
string
[ 1 .. 128 ] characters
^.*$
The reason for activation of a subscription. Required to reactivate the subscription.
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
Sample 1 - 204 - Suspend an existing subscription
Sample 1 - 204 - Suspend an existing subscription
Copy
{
"reason"
:
"Reactivating the subscription"
}
Response samples
204
application/json
Sample 1 - 204 - Suspend an existing subscription
Sample 1 - 204 - Suspend an existing subscription
Copy
{ }
Capture authorized payment on subscription
post
/v1/billing/subscriptions/{id}/capture
Try it
Captures an authorized payment from the subscriber on the subscription.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the subscription.
header
Parameters
PayPal-Request-Id
string
The server stores keys for 72 hours.
Request Body schema:
application/json
multipart/related
multipart/form-data
multipart/mixed
application/json
note
required
string
[ 1 .. 128 ] characters
^.*$
The reason or note for the subscription charge.
capture_type
required
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The type of capture.
Value
Description
OUTSTANDING_BALANCE
The outstanding balance that the subscriber must clear.
amount
required
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
Responses
202
Request Accepted.
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
Sample 1 - 202 - Capture Payment for Subscription
Sample 1 - 202 - Capture Payment for Subscription
Copy
Expand all
Collapse all
{
"note"
:
"Charging as the balance reached the limit"
,
"capture_type"
:
"OUTSTANDING_BALANCE"
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
"100"
}
}
Response samples
202
application/json
Sample 1 - 202 - Capture Payment for Subscription
Sample 1 - 202 - Capture Payment for Subscription
Copy
{ }
List transactions for subscription
get
/v1/billing/subscriptions/{id}/transactions
Try it
Lists transactions for a subscription.
Security
Oauth2
Request
path
Parameters
id
required
string
The ID of the subscription.
query
Parameters
start_time
required
string
<
ppaas_date_time_v3
>
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The start time of the range of transactions to list.
end_time
required
string
<
ppaas_date_time_v3
>
[ 20 .. 64 ] characters
^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|...
Show pattern
The end time of the range of transactions to list.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows subscription details.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/transactions?start_time
=
2018
-01-21T07:50:20.940Z
&
end_time
=
2018
-08-21T07:50:20.940Z
\
-H
'Authorization: Bearer access_token6V7rbVwmlM1gFZKW_8QtzWXqpcwQ6T5vhEGYNJDAAdn3paCgRpdeMdVYmWzgbKSsECednupJ3Zx5Xd-g'
\
-H
'Content-Type: application/json'
\
-H
'Accept: application/json'
Response samples
200
application/json
Sample 1 - 200 - Get subscription payments for the given subscription
Sample 1 - 200 - Get subscription payments for the given subscription
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
"TRFGHNJKOIIOJKL"
,
"status"
:
"COMPLETED"
,
"payer_email"
:
"
[email protected]
"
,
"payer_name"
:
{
"given_name"
:
"John"
,
"surname"
:
"Doe"
}
,
"amount_with_breakdown"
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
"10.00"
}
,
"fee_amount"
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
"net_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"9.00"
}
}
,
"time"
:
"2018-03-16T07:40:20.940Z"
}
,
{
"id"
:
"VDFG45345FFGS"
,
"status"
:
"COMPLETED"
,
"payer_email"
:
"
[email protected]
"
,
"payer_name"
:
{
"given_name"
:
"Jhonny"
,
"surname"
:
"Cat"
}
,
"amount_with_breakdown"
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
"15.00"
}
,
"fee_amount"
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
"net_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"14.00"
}
}
,
"time"
:
"2018-08-21T07:50:20.940Z"
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
https://api-m.paypal.com/v1/billing/subscriptions/I-BW452GLLEP1G/transactions?start_time=2018-01-21T07:50:20.940Z&end_time=2018-08-21T07:50:20.940Z
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
Definitions
A URL details of an institution
This contains the URL details for the instrument. This is to be used by User Interfaces to render appropriate experience when card art images cannot be retrieved.
type
string
(
URL type
)
[ 1 .. 100 ] characters
^[0-9A-Z_]+$
Type of a URL e.g. terms & conditions or settings etc.
Enum Value
Description
SETTINGS
Settings URL Type.
TERMS_AND_CONDITIONS
Terms & Conditions URL Type.
url
string
<
uri
>
(
url
)
Institution specific URL.
Copy
{
"type"
:
"SETTINGS"
,
"url"
:
"
http://example.com
"
}
amount_with_breakdown
The breakdown details for the amount. Includes the gross, tax, fee, and shipping amounts.
gross_amount
required
object
(
Money
)
The amount for this transaction.
total_item_amount
object
(
Money
)
The item total for the transaction.
fee_amount
object
(
Money
)
The fee details for the transaction.
shipping_amount
object
(
Money
)
The shipping amount for the transaction.
tax_amount
object
(
Money
)
The tax amount for the transaction.
net_amount
object
(
Money
)
The net amount that the payee receives for this transaction in their PayPal account. The net amount is computed as
gross_amount
minus the
paypal_fee
.
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
}
application_context
The application context, which customizes the payer experience during the subscription approval process with PayPal.
brand_name
string
[ 1 .. 127 ] characters
^.*$
The label that overrides the business name in the PayPal account on the PayPal site.
shipping_preference
string
[ 1 .. 24 ] characters
^[A-Z_]+$
Default:
"GET_FROM_FILE"
The location from which the shipping address is derived.
Enum Value
Description
GET_FROM_FILE
Get the customer-provided shipping address on the PayPal site.
NO_SHIPPING
Redacts the shipping address from the PayPal site. Recommended for digital goods.
SET_PROVIDED_ADDRESS
Get the merchant-provided address. The customer cannot change this address on the PayPal site. If merchant does not pass an address, customer can choose the address on PayPal pages.
user_action
string
[ 1 .. 24 ] characters
^[A-Z_]+$
Default:
"SUBSCRIBE_NOW"
Configures the label name to
Continue
or
Subscribe Now
for subscription consent experience.
Enum Value
Description
CONTINUE
After you redirect the customer to the PayPal subscription consent page, a
Continue
button appears. Use this option when you want to control the activation of the subscription and do not want PayPal to activate the subscription.
SUBSCRIBE_NOW
After you redirect the customer to the PayPal subscription consent page, a
Subscribe Now
button appears. Use this option when you want PayPal to activate the subscription.
return_url
required
string
<
uri
>
[ 10 .. 4000 ] characters
The URL where the customer is redirected after the customer approves the payment.
cancel_url
required
string
<
uri
>
[ 10 .. 4000 ] characters
The URL where the customer is redirected after the customer cancels the payment.
locale
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
The BCP 47-formatted locale of pages that the PayPal payment experience shows. PayPal supports a five-character code. For example,
da-DK
,
he-IL
,
id-ID
,
ja-JP
,
no-NO
,
pt-BR
,
ru-RU
,
sv-SE
,
th-TH
,
zh-CN
,
zh-HK
, or
zh-TW
.
payment_method
object
(
payment_method
)
The customer and merchant payment preferences. Currently only PAYPAL payment method is supported.
Copy
Expand all
Collapse all
{
"brand_name"
:
"string"
,
"shipping_preference"
:
"GET_FROM_FILE"
,
"user_action"
:
"CONTINUE"
,
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
,
"locale"
:
"string"
,
"payment_method"
:
{
"payee_preferred"
:
"UNRESTRICTED"
}
}
application_context
The application context, which customizes the payer experience during the subscription approval process with PayPal.
brand_name
string
[ 1 .. 127 ] characters
^.*$
The label that overrides the business name in the PayPal account on the PayPal site.
shipping_preference
string
[ 1 .. 24 ] characters
^[A-Z_]+$
Default:
"GET_FROM_FILE"
The location from which the shipping address is derived.
Enum Value
Description
GET_FROM_FILE
Get the customer-provided shipping address on the PayPal site.
NO_SHIPPING
Redacts the shipping address from the PayPal site. Recommended for digital goods.
SET_PROVIDED_ADDRESS
Get the merchant-provided address. The customer cannot change this address on the PayPal site. If merchant does not pass an address, customer can choose the address on PayPal pages.
return_url
required
string
<
uri
>
[ 10 .. 4000 ] characters
The URL where the customer is redirected after the customer approves the payment.
cancel_url
required
string
<
uri
>
[ 10 .. 4000 ] characters
The URL where the customer is redirected after the customer cancels the payment.
locale
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
The BCP 47-formatted locale of pages that the PayPal payment experience shows. PayPal supports a five-character code. For example,
da-DK
,
he-IL
,
id-ID
,
ja-JP
,
no-NO
,
pt-BR
,
ru-RU
,
sv-SE
,
th-TH
,
zh-CN
,
zh-HK
, or
zh-TW
.
payment_method
object
(
payment_method
)
The customer and merchant payment preferences. Currently only PAYPAL payment method is supported.
Copy
Expand all
Collapse all
{
"brand_name"
:
"string"
,
"shipping_preference"
:
"GET_FROM_FILE"
,
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
,
"locale"
:
"string"
,
"payment_method"
:
{
"payee_preferred"
:
"UNRESTRICTED"
}
}
authentication_response
Results of Authentication such as 3D Secure.
liability_shift
string
(
liability_shift
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Liability shift indicator. The outcome of the issuer's authentication.
Enum Value
Description
NO
Liability is with the merchant.
POSSIBLE
Liability may shift to the card issuer.
UNKNOWN
The authentication system is not available.
three_d_secure
object
(
three_d_secure_authentication_response
)
Results of 3D Secure Authentication.
Copy
Expand all
Collapse all
{
"liability_shift"
:
"NO"
,
"three_d_secure"
:
{
"authentication_status"
:
"Y"
,
"enrollment_status"
:
"Y"
}
}
balance_response
The PayPal Balance to fund a payment.
id
string
[ 1 .. 16 ] characters
^([0-9A-Z]+-?[0-9A-Z]+)$
The PayPal-generated ID for the Balance Funding Instrument.
Copy
{
"id"
:
"string"
}
billing_cycle
The billing cycle details.
tenure_type
required
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The tenure type of the billing cycle. In case of a plan having trial cycle, only 2 trial cycles are allowed per plan.
Enum Value
Description
REGULAR
A regular billing cycle.
TRIAL
A trial billing cycle.
sequence
required
integer
[ 1 .. 99 ]
The order in which this cycle is to run among other billing cycles. For example, a trial billing cycle has a
sequence
of
1
while a regular billing cycle has a
sequence
of
2
, so that trial cycle runs before the regular cycle.
total_cycles
integer
[ 0 .. 999 ]
Default:
1
The number of times this billing cycle gets executed. Trial billing cycles can only be executed a finite number of times (value between
1
and
999
for
total_cycles
). Regular billing cycles can be executed infinite times (value of
0
for
total_cycles
) or a finite number of times (value between
1
and
999
for
total_cycles
).
pricing_scheme
object
(
pricing_scheme
)
The active pricing scheme for this billing cycle. A free trial billing cycle does not require a pricing scheme.
frequency
required
object
(
frequency
)
The frequency details for this billing cycle.
Copy
Expand all
Collapse all
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
1
,
"total_cycles"
:
1
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
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
}
billing_cycle_override
The billing cycle details to override at subscription level. The subscription billing cycle definition has to adhere to the plan billing cycle definition.
sequence
required
integer
[ 1 .. 99 ]
The order in which this cycle is to run among other billing cycles. For example, a trial billing cycle has a
sequence
of
1
while a regular billing cycle has a
sequence
of
2
, so that trial cycle runs before the regular cycle.
total_cycles
integer
[ 0 .. 999 ]
The number of times this billing cycle gets executed. Trial billing cycles can only be executed a finite number of times (value between
1
and
999
for
total_cycles
). Regular billing cycles can be executed infinite times (value of
0
for
total_cycles
) or a finite number of times (value between
1
and
999
for
total_cycles
).
pricing_scheme
object
(
pricing_scheme
)
The active pricing scheme for this billing cycle. A free trial billing cycle does not require a pricing scheme.
Copy
Expand all
Collapse all
{
"sequence"
:
1
,
"total_cycles"
:
999
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
}
bin_details
Bank Identification Number (BIN) details used to fund a payment.
bin
string
[ 1 .. 25 ] characters
^[0-9]+$
The Bank Identification Number (BIN) signifies the number that is being used to identify the granular level details (except the PII information) of the card.
issuing_bank
string
[ 1 .. 64 ] characters
The issuer of the card instrument.
products
Array of
strings
[ 1 .. 256 ] items
The type of card product assigned to the BIN by the issuer. These values are defined by the issuer and may change over time. Some examples include: PREPAID_GIFT, CONSUMER, CORPORATE.
bin_country_code
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
two-character ISO-3166-1 country code
of the bank.
Copy
Expand all
Collapse all
{
"bin"
:
"string"
,
"issuing_bank"
:
"string"
,
"products"
:
[
"string"
]
,
"bin_country_code"
:
"string"
}
Capability
The financial instrument (FI) capabilities.
name
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Capability name.
Enum Value
Description
INSTALLMENT
Indicates if instrument is installment capable.
PINLESS_DEBIT
Capability indicates if instrument is Pinless Debit capable.
CAPTURE
Capability indicates if instrument is Capture capable.
TOKEN
Capability indicates if instrument is TOKEN capable.
DEBIT
Capability indicates if instrument is DEBIT capable.
CREDIT
Capability indicates if instrument is CREDIT capable.
FAST_FUND_CROSSBORDER
Capability indicates instrument is fast fund capable for cross border transactions.
FAST_FUND_DOMESTIC
Capability indicates instrument is fast fund capable for domestic transactions.
CURRENCY_CHANGEABLE
Capability indicates instrument is eligible for Currency Change.
AUTO_DEBIT_CARD
Capability indicates instrument is debit card provisioning capable.
NO_VERIFICATION
Capability indicates instrument is no verification.
DESCRIPTOR
Capability indicates instrument supports 'descriptor' related capability. Descriptor aka Soft Descriptor is the wording which appears in the financial instrument's statement/account history during an activity with financial instrument.
ADDRESS_VERIFICATION
Capability indicates instrument supports address verification.
ADD_FUNDS
Capability indicates instrument supports add funds.
AUTH
Capability indicates instrument is auth functionality capable.
CHECK_DIGIT_VERIFICATION
Capability indicates instrument is check digit verification capable.
CONFIRM_INSTRUMENT_DETAILS
Capability indicates instrument is confirm instrument details capable.
GET_INSTRUMENT_DETAILS
Capability indicates instrument is get instrument details capable.
REFUND
Capability indicates instrument is refund capable.
WIRE_WITHDRAWAL
Capability indicates instrument is wire withdrawal capable.
WITHDRAWAL
Capability indicates instrument is withdrawal capable.
EKYC
Capability indicates instrument supports eKYC authentication process.
EXTERNAL_LOGIN
Capability indicates instrument is enternal login capable.
REAL_TIME_BALANCE
Capability indicates instrument supports Real Time Balance (RTB or Open Banking) checks for bank instrument.
CANCEL_NOT_SUPPORTED_ON_REFUND
Capability indicates instrument cancel on refund is not supported.
CAPTURE_NON_REAL_TIME
Capability indicates instrument is non real time capture operation capable.
CAPTURE_REAL_TIME
Capability indicates instrument is real time capture operation capable.
CHARGE
Capability indicates instrument is charge capable.
EXCESSIVE_CAPTURE
Capability indicates instrument is excessive capture operation capable.
INITIAL_BALANCE_INQUIRY
Capability indicates instrument is initial balance inquiry operation capable.
INSTANT_VERIFICATION_CHECK
Capability indicates the operation is an instant or immediate verification of a consumers bank account balance and consumer contact information.
INSTORE_REDEMPTION
Capability indicates the operation is an in-store redemption.
NEED_SETTLEMENT
Capability indicates the operation needs a settlement.
NO_SETTLEMENT
Capability indicates the operation doesn't need a settlement.
ONE_DIMENSIONAL_CA128
Capability indicates the operation supports one-dimensional (1D or linear) barcode CA128 scanning.
ONE_DIMENSIONAL_PDF417
Capability indicates the operation supports one-dimensional (1D or linear) barcode app PDF417 scanning.
ONE_DIMENSIONAL_QRCODE
Capability indicates the operation supports one-dimensional (1D or linear) QR code scanning.
TWO_DIMENSIONAL_CA128
Capability indicates the operation supports two-dimensional (1D or linear) barcode CA128 scanning.
TWO_DIMENSIONAL_PDF417
Capability indicates the operation supports two-dimensional (1D or linear) barcode app PDF417 scanning.
TWO_DIMENSIONAL_QRCODE
Capability indicates the operation supports two-dimensional (1D or linear) QR code scanning.
ONLINE_REDEMPTION
Capability indicates the operation is an online redemption.
ORIGINAL_CREDIT_TRANSACTION
Capability indicates the operation is an original credit transaction.
REALTIME_BALANCE_INQUIRY
Capability indicates the operation is a real-time balance inquiry.
REFUND_NON_REAL_TIME
Capability indicates the operation is a refund in non-real-time.
REFUND_REAL_TIME
Capability indicates the operation is a refund in real-time.
RELOADABLE
Capability indicates the operation is a reloadable transaction.
SUPPORT_ALL_MERCHANTS
Capability indicates the operation supports all merchants.
SUPPORT_BARCODE_SCAN
Capability indicates the operation supports barcode scanning.
ASYNC_INSTANT_PAYMENT
Capability indicates instrument supports asynchronous instant payments which typically happens in two steps. The first step represents payment initiation from PayPal, and second step represents callback coming in from an external processor.
US_NON_RESIDENT_ACCOUNT
Identify if US Bank account holder has residence address outside US, used for marking the transaction as IAT (International ACH Transfer).
mode
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The supported financial instrument (FI) mode.
Enum Value
Description
NON_REAL_TIME
Non real time mode.
REAL_TIME
Real time mode.
networks
Array of
objects
(
Network
)
[ 1 .. 100 ] items
Networks for the Financial instrument.
capability_initiator
string
(
capability_initiator
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Initiator of money movement.
Enum Value
Description
PAYPAL
Indicates PayPal initiate the money movement.
EXTERNAL
Indicates the money movement initiate from the external.
operation_type
string
(
Operation Type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Operation type.
Enum Value
Description
CAPABILITY_OP_SINK
CAPABILITY_OP_SINK.
CAPABILITY_OP_SOURCE
CAPABILITY_OP_SOURCE.
CAPABILITY_OP_READ
CAPABILITY_OP_READ.
READ
READ.
SINK
SINK.
SOURCE
SOURCE.
Copy
Expand all
Collapse all
{
"name"
:
"INSTALLMENT"
,
"mode"
:
"NON_REAL_TIME"
,
"networks"
:
[
{
"preferred"
:
true
,
"cross_border_transaction_supported"
:
true
,
"supported_currencies"
:
[
"str"
]
,
"transfer_type"
:
"WIRE"
,
"mandate_enforcement"
:
"SEPA"
,
"network_rules"
:
[
"string"
]
,
"name"
:
"ACCEL"
}
]
,
"capability_initiator"
:
"PAYPAL"
,
"operation_type"
:
"CAPABILITY_OP_SINK"
}
capability_initiator
Initiator of money movement.
string
(
capability_initiator
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Initiator of money movement.
Enum Value
Description
PAYPAL
Indicates PayPal initiate the money movement.
EXTERNAL
Indicates the money movement initiate from the external.
Copy
"PAYPAL"
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
Copy
{
"status"
:
"COMPLETED"
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
Copy
{
"status"
:
"COMPLETED"
}
capture_status_details
The details of the captured payment status.
reason
string
(
Capture Incomplete Reason
)
[ 1 .. 64 ] characters
^[A-Z_]+$
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
card
The payment card to use to fund a payment. Can be a credit or debit card.
name
string
[ 1 .. 300 ] characters
^.{1,300}$
The card holder's name as it appears on the card.
number
string
[ 13 .. 19 ] characters
^[0-9]{13,19}$
The primary account number (PAN) for the payment card.
security_code
string
[ 3 .. 4 ] characters
^[0-9]{3,4}$
The three- or four-digit security code of the card. Also known as the CVV, CVC, CVN, CVE, or CID. This parameter cannot be present in the request when
payment_initiator=MERCHANT
.
expiry
string
(
date_year_month
)
= 7 characters
^[0-9]{4}-(0[1-9]|1[0-2])$
The card expiration year and month, in
Internet date format
For example: 2028-04
type
string
(
card_type
)
[ 1 .. 255 ] characters
^[A-Z_]+$
The payment card type.
Enum Value
Description
CREDIT
A credit card.
DEBIT
A debit card.
PREPAID
A Prepaid card.
STORE
A store card.
UNKNOWN
Card type cannot be determined.
brand
string
(
card_brand
)
[ 1 .. 255 ] characters
^[A-Z_]+$
The card brand or network. Typically used in the response.
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
UNKNOWN
UNKNOWN payment network.
billing_address
object
(
Portable Postal Address (Medium-Grained)
)
The billing address for this card. Supports only the
address_line_1
,
address_line_2
,
admin_area_1
,
admin_area_2
,
postal_code
, and
country_code
properties.
attributes
object
(
card_attributes
)
Additional attributes associated with the use of this card.
Copy
Expand all
Collapse all
{
"name"
:
"string"
,
"number"
:
"stringstrings"
,
"security_code"
:
"stri"
,
"expiry"
:
"string"
,
"type"
:
"CREDIT"
,
"brand"
:
"VISA"
,
"billing_address"
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
}
,
"attributes"
:
{
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
,
"vault"
:
{
"store_in_vault"
:
"ON_SUCCESS"
}
,
"verification"
:
{
"method"
:
"SCA_ALWAYS"
}
}
}
card
The payment card to use to fund a payment. Can be a credit or debit card.
name
string
[ 1 .. 300 ] characters
^.{1,300}$
The card holder's name as it appears on the card.
number
string
[ 13 .. 19 ] characters
^[0-9]{13,19}$
The primary account number (PAN) for the payment card.
security_code
string
[ 3 .. 4 ] characters
^[0-9]{3,4}$
The three- or four-digit security code of the card. Also known as the CVV, CVC, CVN, CVE, or CID. This parameter cannot be present in the request when
payment_initiator=MERCHANT
.
expiry
string
(
date_year_month
)
= 7 characters
^[0-9]{4}-(0[1-9]|1[0-2])$
The card expiration year and month, in
Internet date format
For example: 2028-04
type
string
(
card_type
)
[ 1 .. 255 ] characters
^[A-Z_]+$
The payment card type.
Enum Value
Description
CREDIT
A credit card.
DEBIT
A debit card.
PREPAID
A Prepaid card.
STORE
A store card.
UNKNOWN
Card type cannot be determined.
brand
string
(
card_brand
)
[ 1 .. 255 ] characters
^[A-Z_]+$
The card brand or network. Typically used in the response.
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
UNKNOWN
UNKNOWN payment network.
billing_address
object
(
Portable Postal Address (Medium-Grained)
)
The billing address for this card. Supports only the
address_line_1
,
address_line_2
,
admin_area_1
,
admin_area_2
,
postal_code
, and
country_code
properties.
attributes
object
(
card_attributes
)
Additional attributes associated with the use of this card.
Copy
Expand all
Collapse all
{
"name"
:
"string"
,
"number"
:
"stringstrings"
,
"security_code"
:
"stri"
,
"expiry"
:
"string"
,
"type"
:
"CREDIT"
,
"brand"
:
"VISA"
,
"billing_address"
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
}
,
"attributes"
:
{
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
,
"vault"
:
{
"store_in_vault"
:
"ON_SUCCESS"
}
,
"verification"
:
{
"method"
:
"SCA_ALWAYS"
}
}
}
Card Verification
The API caller can opt in to verify the card through PayPal offered verification services (e.g. Smart Dollar Auth, 3DS).
method
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Default:
"SCA_WHEN_REQUIRED"
The method used for card verification.
Enum Value
Description
SCA_ALWAYS
Selecting this option will attempt to force a strong customer authentication for the authorization/transaction. In countries where SCA has been defined and implemented it will result in a contingency and HATEOAS link being returned.  The API caller should redirect the payer to that link so that they can authenticate themselves against their issuing bank or other entity. As noted, the HATEOAS link is only available in all regions where strong authentication is supported, (e.g. in European countries where 3DS is live). Merchants can use this setting as an additional layer of security if they choose to. In all cases, when an authorization is requested the AVS/CVV results will be returned in the response.
SCA_WHEN_REQUIRED
This is the default. When an authorization or transaction is attempted this option will return a contingency and HATEOAS link only when local regulations require strong customer authentication, (e.g. 3DS in countries and use cases where it is mandated). The API caller should redirect the payer to the link so that they can authenticate themselves. In all cases, when an authorization is requested the AVS/CVV results will be returned in the response.
3D_SECURE
The contingency surfaced as an additional security layer that helps prevent unauthorized card-not-present transactions and protects the merchant from exposure to fraud.
AVS_CVV
Places a temporary hold on the card to ensure its validity. This process protects the merchant from exposure to fraud. This verification method will confirm that the address information or CVV included matches what the issuing bank has on file for the associated card, ensuring that only authorized card users are able to make purchases from you.
Copy
{
"method"
:
"SCA_ALWAYS"
}
card_attributes
Additional attributes associated with the use of this card.
customer
object
(
card_customer
)
The details about a customer in PayPal's system of record.
vault
object
(
vault_instruction_base
)
Instruction to vault the card based on the specified strategy.
verification
object
(
Card Verification
)
Instruction to optionally verify the card based on the specified strategy.
Copy
Expand all
Collapse all
{
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
,
"vault"
:
{
"store_in_vault"
:
"ON_SUCCESS"
}
,
"verification"
:
{
"method"
:
"SCA_ALWAYS"
}
}
card_attributes_response
Additional attributes associated with the use of this card.
vault
object
(
card_vault_response
)
The details about a saved Card payment source.
Copy
Expand all
Collapse all
{
"vault"
:
{
"id"
:
"string"
,
"status"
:
"VAULTED"
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
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
}
}
card_brand
The card network or brand. Applies to credit, debit, gift, and payment cards.
string
(
card_brand
)
[ 1 .. 255 ] characters
^[A-Z_]+$
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
UNKNOWN
UNKNOWN payment network.
Copy
"VISA"
card_customer
The details about a customer in PayPal's system of record.
id
string
(
merchant_partner_customer_id
)
[ 1 .. 22 ] characters
^[0-9a-zA-Z_-]+$
The unique ID for a customer generated by PayPal.
email_address
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
Email address of the buyer as provided to the merchant or on file with the merchant. Email Address is required if you are processing the transaction using PayPal Guest Processing which is offered to select partners and merchants. For all other use cases we do not expect partners/merchant to send email_address of their customer.
phone
object
(
phone_with_type
)
The phone number of the buyer as provided to the merchant or on file with the merchant. The
phone.phone_number
supports only
national_number
.
merchant_customer_id
string
[ 1 .. 64 ] characters
^[0-9a-zA-Z-_.^*$@#]+$
Merchants and partners may already have a data-store where their customer information is persisted. Use merchant_customer_id to associate the PayPal-generated customer.id to your representation of a customer.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
card_from_request
Representation of card details as received in the request.
last_digits
string
[ 2 .. 4 ] characters
[0-9]{2,}
The last digits of the payment card.
expiry
string
(
date_year_month
)
= 7 characters
^[0-9]{4}-(0[1-9]|1[0-2])$
The card expiration year and month, in
Internet date format
.
Copy
{
"last_digits"
:
"stri"
,
"expiry"
:
"string"
}
card_response
The payment card to use to fund a payment. Card can be a credit or debit card.
name
string
[ 2 .. 300 ] characters
The card holder's name as it appears on the card.
last_digits
string
[0-9]{2,}
The last digits of the payment card.
available_networks
Array of
strings
(
card_brand
)
[ 1 .. 256 ] items
Array of brands or networks associated with the card.
Items
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
UNKNOWN
UNKNOWN payment network.
from_request
object
(
card_from_request
)
Representation of card details as received in the request.
stored_credential
object
(
card_stored_credential
)
Provides additional details to process a payment using a
card
that has been stored or is intended to be stored (also referred to as stored_credential or card-on-file).
Parameter compatibility:
payment_type=ONE_TIME
is compatible only with
payment_initiator=CUSTOMER
.
usage=FIRST
is compatible only with
payment_initiator=CUSTOMER
.
previous_transaction_reference
or
previous_network_transaction_reference
is compatible only with
payment_initiator=MERCHANT
.
Only one of the parameters -
previous_transaction_reference
and
previous_network_transaction_reference
- can be present in the request.
brand
string
(
card_brand
)
[ 1 .. 255 ] characters
^[A-Z_]+$
The card brand or network. Typically used in the response.
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
UNKNOWN
UNKNOWN payment network.
type
string
(
card_type
)
[ 1 .. 255 ] characters
^[A-Z_]+$
The payment card type.
Enum Value
Description
CREDIT
A credit card.
DEBIT
A debit card.
PREPAID
A Prepaid card.
STORE
A store card.
UNKNOWN
Card type cannot be determined.
authentication_result
object
(
authentication_response
)
Results of Authentication such as 3D Secure.
attributes
object
(
card_attributes_response
)
Additional attributes associated with the use of this card.
expiry
string
(
date_year_month
)
= 7 characters
^[0-9]{4}-(0[1-9]|1[0-2])$
The card expiration year and month, in
Internet date format
.
bin_details
object
(
bin_details
)
Bank Identification Number (BIN) details used to fund a payment.
Copy
Expand all
Collapse all
{
"name"
:
"string"
,
"last_digits"
:
"string"
,
"available_networks"
:
[
"VISA"
]
,
"from_request"
:
{
"last_digits"
:
"stri"
,
"expiry"
:
"string"
}
,
"stored_credential"
:
{
"payment_initiator"
:
"CUSTOMER"
,
"payment_type"
:
"ONE_TIME"
,
"usage"
:
"FIRST"
,
"previous_network_transaction_reference"
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
"acquirer_reference_number"
:
"string"
,
"network"
:
"VISA"
}
}
,
"brand"
:
"VISA"
,
"type"
:
"CREDIT"
,
"authentication_result"
:
{
"liability_shift"
:
"NO"
,
"three_d_secure"
:
{
"authentication_status"
:
"Y"
,
"enrollment_status"
:
"Y"
}
}
,
"attributes"
:
{
"vault"
:
{
"id"
:
"string"
,
"status"
:
"VAULTED"
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
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
}
}
,
"expiry"
:
"string"
,
"bin_details"
:
{
"bin"
:
"string"
,
"issuing_bank"
:
"string"
,
"products"
:
[
"string"
]
,
"bin_country_code"
:
"string"
}
}
card_response_with_billing_address
The payment card used to fund the payment. Card can be a credit or debit card.
name
string
[ 2 .. 300 ] characters
The card holder's name as it appears on the card.
last_digits
string
[0-9]{2,}
The last digits of the payment card.
available_networks
Array of
strings
(
card_brand
)
[ 1 .. 256 ] items
Array of brands or networks associated with the card.
Items
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
UNKNOWN
UNKNOWN payment network.
from_request
object
(
card_from_request
)
Representation of card details as received in the request.
stored_credential
object
(
card_stored_credential
)
Provides additional details to process a payment using a
card
that has been stored or is intended to be stored (also referred to as stored_credential or card-on-file).
Parameter compatibility:
payment_type=ONE_TIME
is compatible only with
payment_initiator=CUSTOMER
.
usage=FIRST
is compatible only with
payment_initiator=CUSTOMER
.
previous_transaction_reference
or
previous_network_transaction_reference
is compatible only with
payment_initiator=MERCHANT
.
Only one of the parameters -
previous_transaction_reference
and
previous_network_transaction_reference
- can be present in the request.
brand
string
(
card_brand
)
[ 1 .. 255 ] characters
^[A-Z_]+$
The card brand or network. Typically used in the response.
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
UNKNOWN
UNKNOWN payment network.
type
string
(
card_type
)
[ 1 .. 255 ] characters
^[A-Z_]+$
The payment card type.
Enum Value
Description
CREDIT
A credit card.
DEBIT
A debit card.
PREPAID
A Prepaid card.
STORE
A store card.
UNKNOWN
Card type cannot be determined.
authentication_result
object
(
authentication_response
)
Results of Authentication such as 3D Secure.
attributes
object
(
card_attributes_response
)
Additional attributes associated with the use of this card.
expiry
string
(
date_year_month
)
= 7 characters
^[0-9]{4}-(0[1-9]|1[0-2])$
The card expiration year and month, in
Internet date format
.
bin_details
object
(
bin_details
)
Bank Identification Number (BIN) details used to fund a payment.
billing_address
object
(
Portable Postal Address (Medium-Grained)
)
The portable international postal address. Maps to
AddressValidationMetadata
and HTML 5.1
Autofilling form controls: the autocomplete attribute
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
Currency code of the given instrument
Copy
Expand all
Collapse all
{
"name"
:
"string"
,
"last_digits"
:
"string"
,
"available_networks"
:
[
"VISA"
]
,
"from_request"
:
{
"last_digits"
:
"stri"
,
"expiry"
:
"string"
}
,
"stored_credential"
:
{
"payment_initiator"
:
"CUSTOMER"
,
"payment_type"
:
"ONE_TIME"
,
"usage"
:
"FIRST"
,
"previous_network_transaction_reference"
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
"acquirer_reference_number"
:
"string"
,
"network"
:
"VISA"
}
}
,
"brand"
:
"VISA"
,
"type"
:
"CREDIT"
,
"authentication_result"
:
{
"liability_shift"
:
"NO"
,
"three_d_secure"
:
{
"authentication_status"
:
"Y"
,
"enrollment_status"
:
"Y"
}
}
,
"attributes"
:
{
"vault"
:
{
"id"
:
"string"
,
"status"
:
"VAULTED"
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
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
}
}
,
"expiry"
:
"string"
,
"bin_details"
:
{
"bin"
:
"string"
,
"issuing_bank"
:
"string"
,
"products"
:
[
"string"
]
,
"bin_country_code"
:
"string"
}
,
"billing_address"
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
}
,
"currency_code"
:
"string"
}
card_stored_credential
Provides additional details to process a payment using a
card
that has been stored or is intended to be stored (also referred to as stored_credential or card-on-file).
Parameter compatibility:
payment_type=ONE_TIME
is compatible only with
payment_initiator=CUSTOMER
.
usage=FIRST
is compatible only with
payment_initiator=CUSTOMER
.
previous_transaction_reference
or
previous_network_transaction_reference
is compatible only with
payment_initiator=MERCHANT
.
Only one of the parameters -
previous_transaction_reference
and
previous_network_transaction_reference
- can be present in the request.
payment_initiator
required
string
(
payment_initiator
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The person or party who initiated or triggered the payment.
Enum Value
Description
CUSTOMER
Payment is initiated with the active engagement of the customer. e.g. a customer checking out on a merchant website.
MERCHANT
Payment is initiated by merchant on behalf of the customer without the active engagement of customer. e.g. a merchant charging the monthly payment of a subscription to the customer.
payment_type
required
string
(
stored_payment_source_payment_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Indicates the type of the stored payment_source payment.
Enum Value
Description
ONE_TIME
One Time payment such as online purchase or donation. (e.g. Checkout with one-click).
RECURRING
Payment which is part of a series of payments with fixed or variable amounts, following a fixed time interval. (e.g. Subscription payments).
UNSCHEDULED
Payment which is part of a series of payments that occur on a non-fixed schedule and/or have variable amounts. (e.g. Account Topup payments).
usage
string
(
stored_payment_source_usage_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Default:
"DERIVED"
Indicates if this is a
first
or
subsequent
payment using a stored payment source (also referred to as stored credential or card on file).
Enum Value
Description
FIRST
Indicates the Initial/First payment with a payment_source that is intended to be stored upon successful processing of the payment.
SUBSEQUENT
Indicates a payment using a stored payment_source which has been successfully used previously for a payment.
DERIVED
Indicates that PayPal will derive the value of
FIRST
or
SUBSEQUENT
based on data available to PayPal.
previous_network_transaction_reference
object
(
network_transaction_reference
)
Reference values used by the card network to identify a transaction.
Copy
Expand all
Collapse all
{
"payment_initiator"
:
"CUSTOMER"
,
"payment_type"
:
"ONE_TIME"
,
"usage"
:
"FIRST"
,
"previous_network_transaction_reference"
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
"acquirer_reference_number"
:
"string"
,
"network"
:
"VISA"
}
}
card_type
Type of card. i.e Credit, Debit and so on.
string
(
card_type
)
[ 1 .. 255 ] characters
^[A-Z_]+$
Type of card. i.e Credit, Debit and so on.
Enum Value
Description
CREDIT
A credit card.
DEBIT
A debit card.
PREPAID
A Prepaid card.
STORE
A store card.
UNKNOWN
Card type cannot be determined.
Copy
"CREDIT"
card_vault_response
The details about a saved Card payment source.
id
string
[ 1 .. 255 ] characters
The PayPal-generated ID for the saved payment source.
status
string
(
Vault Status
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The vault status.
Enum Value
Description
VAULTED
The payment source has been saved in your customer's vault. This vault status reflects
/v3/vault
status.
CREATED
DEPRECATED. The payment source has been saved in your customer's vault. This status applies to deprecated integration patterns and will not be returned for v3/vault integrations.
APPROVED
Customer has approved the action of saving the specified payment_source into their vault. Use v3/vault/payment-tokens with given setup_token to save the payment source in the vault
links
Array of
objects
(
Link Description
)
[ 1 .. 10 ] items
An array of request-related HATEOAS links.
customer
object
(
card_customer
)
The details about a customer in PayPal's system of record.
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
"VAULTED"
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
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
}
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
currency_decimal_precision
The decimal precision to be used for a currency.
integer
(
currency_decimal_precision
)
[ 0 .. 50 ]
The decimal precision to be used for a currency.
Copy
50
customer
The details about a customer in PayPal's system of record.
id
string
(
merchant_partner_customer_id
)
[ 1 .. 22 ] characters
^[0-9a-zA-Z_-]+$
The unique ID for a customer generated by PayPal.
Copy
{
"id"
:
"string"
}
customer
The details about a customer in PayPal's system of record.
id
string
(
merchant_partner_customer_id
)
[ 1 .. 22 ] characters
^[0-9a-zA-Z_-]+$
The unique ID for a customer generated by PayPal.
email_address
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
Email address of the buyer as provided to the merchant or on file with the merchant. Email Address is required if you are processing the transaction using PayPal Guest Processing which is offered to select partners and merchants. For all other use cases we do not expect partners/merchant to send email_address of their customer.
phone
object
(
phone_with_type
)
The phone number of the buyer as provided to the merchant or on file with the merchant. The
phone.phone_number
supports only
national_number
.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
}
cycle_execution
The regular and trial execution details for a billing cycle.
tenure_type
required
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The type of the billing cycle.
Enum Value
Description
REGULAR
A regular billing cycle.
TRIAL
A trial billing cycle.
sequence
required
integer
[ 0 .. 99 ]
The order in which to run this cycle among other billing cycles.
cycles_completed
required
integer
[ 0 .. 9999 ]
The number of billing cycles that have completed.
cycles_remaining
integer
[ 0 .. 9999 ]
For a finite billing cycle, cycles_remaining is the number of remaining cycles. For an infinite billing cycle, cycles_remaining is set as 0.
current_pricing_scheme_version
integer
[ 1 .. 99 ]
The active pricing scheme version for the billing cycle.
total_cycles
integer
[ 0 .. 999 ]
The number of times this billing cycle gets executed. Trial billing cycles can only be executed a finite number of times (value between
1
and
999
for
total_cycles
). Regular billing cycles can be executed infinite times (value of
0
for
total_cycles
) or a finite number of times (value between
1
and
999
for
total_cycles
).
Copy
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
99
,
"cycles_completed"
:
9999
,
"cycles_remaining"
:
9999
,
"current_pricing_scheme_version"
:
1
,
"total_cycles"
:
999
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
date_year_month
The year and month, in ISO-8601
YYYY-MM
date format. See
Internet date and time format
.
string
(
date_year_month
)
= 7 characters
^[0-9]{4}-(0[1-9]|1[0-2])$
The year and month, in ISO-8601
YYYY-MM
date format. See
Internet date and time format
.
Copy
"strings"
date_year_month
The year and month, in ISO-8601
YYYY-MM
date format. See
Internet date and time format
.
string
(
date_year_month
)
= 7 characters
^[0-9]{4}-(0[1-9]|1[0-2])$
The year and month, in ISO-8601
YYYY-MM
date format. See
Internet date and time format
.
Copy
"strings"
Denomination Type
The type of the denomination.
string
(
Denomination Type
)
[ 1 .. 128 ] characters
^[0-9A-Z_]+$
The type of the denomination.
Enum Value
Description
CURRENCY
The currency denomination type.
REWARDS_CURRENCY
The rewards currency denomination type.
Copy
"CURRENCY"
description
A statement that describes the information of a field. Unicode is supported.
string
(
description
)
[ 1 .. 256 ] characters
A statement that describes the information of a field. Unicode is supported.
Copy
"string"
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
enrolled
Status of Authentication eligibility.
string
(
enrolled
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Status of Authentication eligibility.
Enum Value
Description
Y
Yes. The bank is participating in 3-D Secure protocol and will return the ACSUrl.
N
No. The bank is not participating in 3-D Secure protocol.
U
Unavailable. The DS or ACS is not available for authentication at the time of the request.
B
Bypass. The merchant authentication rule is triggered to bypass authentication.
Copy
"Y"
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
Evaluate funding option api response.
The resource object that specifies the evaluate funding options api response which returns the evaluated eligible funding options that can be used by the buyer for billing agreement or subscription sign-up.
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
}
]
}
external_reference_id
Holds the external reference identifier of the instrument.
string
(
external_reference_id
)
[ 1 .. 256 ] characters
^.+$
Holds the external reference identifier of the instrument.
Copy
"string"
failed_payment_details
The details for the failed payment of the subscription.
reason_code
string
[ 1 .. 120 ] characters
^[A-Z_]+$
The reason code for the payment failure.
Enum Value
Description
PAYMENT_DENIED
PayPal declined the payment due to one or more customer issues.
INTERNAL_SERVER_ERROR
An internal server error has occurred.
PAYEE_ACCOUNT_RESTRICTED
The payee account is not in good standing and cannot receive payments.
PAYER_ACCOUNT_RESTRICTED
The payer account is not in good standing and cannot make payments.
PAYER_CANNOT_PAY
Payer cannot pay for this transaction.
SENDING_LIMIT_EXCEEDED
The transaction exceeds the payer's sending limit.
TRANSACTION_RECEIVING_LIMIT_EXCEEDED
The transaction exceeds the receiver's receiving limit.
CURRENCY_MISMATCH
The transaction is declined due to a currency mismatch.
amount
required
object
(
Money
)
The failed payment amount.
time
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
The date and time when the failed payment was made, in
Internet date and time format
.
next_payment_retry_time
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
The time when the retry attempt for the failed payment occurs, in
Internet date and time format
.
Copy
Expand all
Collapse all
{
"reason_code"
:
"PAYMENT_DENIED"
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
"time"
:
"string"
,
"next_payment_retry_time"
:
"string"
}
float_value
The float value. Also allows for negative values needed for rewards/balances.
string
(
float_value
)
[ 1 .. 50 ] characters
^(-?[0-9]+([.][0-9]*)?|[.][0-9]+)$
The float value. Also allows for negative values needed for rewards/balances.
Copy
"string"
frequency
The frequency of the billing cycle.
interval_unit
required
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The interval at which the subscription is charged or billed.
Enum Value
Description
DAY
A daily billing cycle.
WEEK
A weekly billing cycle.
MONTH
A monthly billing cycle.
YEAR
A yearly billing cycle.
interval_count
integer
[ 1 .. 365 ]
Default:
1
The number of intervals after which a subscriber is billed. For example, if the
interval_unit
is
DAY
with an
interval_count
of
2
, the subscription is billed once every two days. The following table lists the maximum allowed values for the
interval_count
for each
interval_unit
:
Interval unit
Maximum interval count
DAY
365
WEEK
52
MONTH
12
YEAR
1
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
Full Name
The full name of the party, for example, the name of a cardholder.
name
string
[ 1 .. 300 ] characters
The full representation of a name, for example,
Mr. J. Smith
.
Copy
{
"name"
:
"string"
}
Full Name with orthography
Full Name of an entity, use this in cases like native name on a bank account.
name
required
string
[ 1 .. 300 ] characters
The full representation of a name, for example,
Mr. J. Smith
.
orthography
string
(
Orthography Type
)
= 4 characters
^[A-Z][a-z]{3}$
The script in which the name is provided like English, Kanji, etc.
Enum Value
Description
Zyyy
The orthography cannot be determined.
Zzzz
The orthography is unknown.
Kana
An angular form of Japanese writing for words of foreign origin.
Cyrl
The Slavic languages alphabet. Used in eastern Europe.
Arab
The Arabic language alphabet.
Armn
The Armenian alphabet.
Beng
The Bengali alphabet. Used in eastern India.
Cans
The Unified Canadian Aboriginal Syllabics alphabet.
Deva
The Devanagari (Nagari) alphabet.
Ethi
The Ethiopic alphabet.
Geor
The Georgian (Mkhedruli and Mtavruli) alphabet.
Grek
The Greek alphabet.
Gujr
The Gujurati language alphabet. Used in western India.
Guru
The Gurmukhi alphabet. Used in the northern Indian state of Punjab.
Hani
The Han (Hanzi, Kanji, Hanja) alphabet.
Hebr
The Hebrew alphabet.
Java
The Javanese alphabet.
Jpan
The Japanese (alias for Han + Hiragana + Katakana) alphabet.
Khmr
The Khmer alphabet.
Knda
The Kannada alphabet. Used in the southern Indian state of Karnataka.
Kore
Korean (alias for Hangul + Han).
Laoo
The Lao alphabet.
Latn
The Latin alphabet.
Mlym
The Malayalam alphabet. Used in the southern Indian state of Kerala.
Mong
The Mongolian alphabet.
Mymr
The Myanmar (Burmese) alphabet.
Orya
The Oriya (Odia) alphabet. Used in the eastern Indian state of Odisha.
Sinh
The Sinhala alphabet.
Sund
The Sundanese alphabet.
Syrc
The Syriac alphabet.
Taml
The Tamil alphabet. Used in the southern Indian state of Tamilnadu.
Telu
The Telugu language alphabet. Used in the southern Indian state of Andhra pradesh.
Thaa
The Thaana (Maldivian) alphabet.
Thai
The Thai alphabet. Used in Thailand.
Tibt
The Tibetan alphabet.
Yiii
The Yi alphabet.
Copy
{
"name"
:
"string"
,
"orthography"
:
"Zyyy"
}
hmac
The instrument account number in HMAC format.
string
(
hmac
)
[ 1 .. 256 ] characters
^[A-Za-z0-9-_.+=/\[\]]+$
The instrument account number in HMAC format.
Copy
"string"
Image category
The display category for an image.
string
(
Image category
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The display category for an image.
Enum Value
Description
PRIMARY
The image is intended to display a financial institution.
WALLET
The image is intended to display a financial institution wallet.
THUMBNAIL
The image is intended for thumbnail display.
REWARD
The image is intended to display a reward program.
PAYMENT_TOKEN
The image is intended to display a payment token program.
STACK_VIEW
The image is intended for stack view display.
Copy
"PRIMARY"
Image location type
The type of image location.
string
(
Image location type
)
[ 1 .. 100 ] characters
^[0-9A-Z_]+$
The type of image location.
Enum Value
Description
INTERNAL
The image is located in the PayPal Content Delivery Network (CDN).
EXTERNAL
The image is located outside of PayPal.
Copy
"INTERNAL"
Institution art details
Institution art details including image content and metadata.
original_mime_type
string
[ 1 .. 255 ] characters
^[A-Za-z0-9-_.+/=\s]*
The original image format specified in Web MIME Type form. For example, a PNG image would be represented as
image/png
. Clients should use the mime type's extension to generate the full CDN image URL.
original_width
integer
[ 0 .. 2147483647 ]
The width of the original image in pixels.
original_height
integer
[ 0 .. 2147483647 ]
The height of the original image in pixels.
background_color
string
[ 1 .. 32 ] characters
^[A-Za-z0-9-_.+/=\s]+
The background color of the UI or display space for the card, in CSS-style hexadecimal format, such as 0x0f21a2.
foreground_color
string
[ 1 .. 32 ] characters
^[A-Za-z0-9-_.+/=\s]+
The foreground color of the UI or display space for the card, in CSS-style hexadecimal format, such as 0x0f21a2.
label_color
string
[ 1 .. 32 ] characters
^[A-Za-z0-9-_.+/=\s]+
The label color of the UI or display space for the card, in CSS-style hexadecimal format, such as 0x0f21a2.
location_type
string
(
Image location type
)
[ 1 .. 100 ] characters
^[0-9A-Z_]+$
Type of image location.
Enum Value
Description
INTERNAL
The image is located in the PayPal Content Delivery Network (CDN).
EXTERNAL
The image is located outside of PayPal.
image_path
string
<
uri
>
(
url
)
The image's location.
path_format_type
string
(
Path format
)
[ 1 .. 100 ] characters
^[0-9A-Z_]+$
The path format for this image link.
Enum Value
Description
ABSOLUTE
Complete path is given not the CDN.
PARTIAL
Partial path is given e.g. CDN and a specific size can be requested.
Copy
{
"original_mime_type"
:
"string"
,
"original_width"
:
2147483647
,
"original_height"
:
2147483647
,
"background_color"
:
"string"
,
"foreground_color"
:
"string"
,
"label_color"
:
"string"
,
"location_type"
:
"INTERNAL"
,
"image_path"
:
"
http://example.com
"
,
"path_format_type"
:
"ABSOLUTE"
}
Institution art images content
Contains image details along with how image has been categorized.
image_details
Array of
objects
(
Institution art details
)
[ 1 .. 50 ] items
Institution Art Details including image content and metadata.
image_classification
string
[ 1 .. 32 ] characters
^[A-Z]+$
Describes source of image.
Enum Value
Description
NETWORK
Indicates network issued image.
PAN
Indicates PAN specific image.
ISSUER
Indicates ISSUER image.
BIN
Indicates BIN image.
category
string
(
Image category
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
A category of all the images.
Enum Value
Description
PRIMARY
The image is intended to display a financial institution.
WALLET
The image is intended to display a financial institution wallet.
THUMBNAIL
The image is intended for thumbnail display.
REWARD
The image is intended to display a reward program.
PAYMENT_TOKEN
The image is intended to display a payment token program.
STACK_VIEW
The image is intended for stack view display.
Copy
Expand all
Collapse all
{
"image_details"
:
[
{
"original_mime_type"
:
"string"
,
"original_width"
:
2147483647
,
"original_height"
:
2147483647
,
"background_color"
:
"string"
,
"foreground_color"
:
"string"
,
"label_color"
:
"string"
,
"location_type"
:
"INTERNAL"
,
"image_path"
:
"
http://example.com
"
,
"path_format_type"
:
"ABSOLUTE"
}
]
,
"image_classification"
:
"NETWORK"
,
"category"
:
"PRIMARY"
}
Instrument state
The wallet instrument state. Indicates whether the financial instrument (FI) is available for payments and verification.
string
(
Instrument state
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The wallet instrument state. Indicates whether the financial instrument (FI) is available for payments and verification.
Enum Value
Description
ACTIVE
FI State active.
BLOCKED
FI State blocked. Should not be exposed externally.
INACTIVE
FI State inactive.
ON_HOLD
FI State on hold. Should not be exposed externally.
REMOVED
FI State removed.
NOT_CREATED
FI State not created.
CLOSED
FI State closed.
Copy
"ACTIVE"
instrument_id
The identifier of the instrument.
string
(
instrument_id
)
[ 1 .. 256 ] characters
^[A-Za-z0-9-_.+=]+$
The identifier of the instrument.
Copy
"string"
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
last_payment_details
The details for the last payment.
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
amount
required
object
(
Money
)
The last payment amount.
time
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
The date and time when the last payment was made, in
Internet date and time format
.
Copy
Expand all
Collapse all
{
"status"
:
"COMPLETED"
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
"time"
:
"string"
}
liability_shift
Liability shift indicator. The outcome of the issuer's authentication.
string
(
liability_shift
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Liability shift indicator. The outcome of the issuer's authentication.
Enum Value
Description
NO
Liability is with the merchant.
POSSIBLE
Liability may shift to the card issuer.
UNKNOWN
The authentication system is not available.
Copy
"NO"
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
List of network names
The capability network.
string
(
List of network names
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The capability network.
Enum Value
Description
ACCEL
Indicates ACCEL network support for given instrument.
AMEX
Indicates AMEX network support for given instrument..
BACS
Indicates BACS network support for given instrument.
BML
Indicates BML network support for given instrument.
CB_NATIONALE
Indicates CB_NATIONALE network support for given instrument.
CET
Indicates CET network support for given instrument.
CETELEM
Indicates CETELEM network support for given instrument.
CHAPS
Indicates CHAPS network support for given instrument.
CHASENET
Indicates CHASENET network support for given instrument.
CHINA_UNION_PAY
Indicates CHINA_UNION_PAY network support for given instrument.
COFIDIS
Indicates COFIDIS network support for given instrument.
COFINOGA
Indicates COFINOGA network support for given instrument.
DELTA
Indicates DELTA network support for given instrument.
DINERS
Indicates DINERS network support for given instrument.
DISCOVER
Indicates DISCOVER network support for given instrument.
EFTPOS
Indicates EFTPOS network support for given instrument.
ELECTRON
Indicates ELECTRON network support for given instrument.
ELO
Indicates ELO network support for given instrument.
FPS
Indicates FPS network support for given instrument.
GE
Indicates GE network support for given instrument.
HIPER
Indicates HIPER network support for given instrument.
HIPERCARD
Indicates HIPERCARD network support for given instrument.
IAV_YODLEE
Indicates IAV_YODLEE network support for given instrument.
JCB
Indicates JCB network support for given instrument.
LOCAL
Indicates LOCAL network support for given instrument.
MAESTRO
Indicates MAESTRO network support for given instrument.
MASTER_CARD
Indicates MASTER_CARD network support for given instrument.
NYCE
Indicates NYCE network support for given instrument.
OPEN_WALLET
Indicates OPEN_WALLET network support for given instrument.
PAYPAL
Indicates PAYPAL network support for given instrument.
POSTEPAY
Indicates POSTEPAY network support for given instrument.
PULSE
Indicates PULSE network support for given instrument.
PWMB
Indicates PWMB network support for given instrument.
RUPAY
Indicates RUPAY network support for given instrument.
SAN
Indicates SAN network support for given instrument.
SEPA
Indicates SEPA network support for given instrument.
SEPA_COR1
Indicates SEPA_COR1 network support for given instrument.
SEPA_CORE
Indicates SEPA_CORE network support for given instrument.
SOLO
Indicates SOLO network support for given instrument.
SSG
Indicates SSG network support for given instrument.
STAR
Indicates STAR network support for given instrument.
STAR_FINANZ
Indicates STAR_FINANZ network support for given instrument.
STAR_ACCESS
Indicates STAR_ACCESS network support for given instrument.
SWITCH
Indicates SWITCH network support for given instrument.
VISA
Indicates VISA network support for given instrument.
WIRE
Indicates WIRE network support for given instrument.
FASTER_CLEARING
Indicates FASTER_CLEARING network support for given instrument.
SYNCHRONY_FINANCIAL_SUPPORT
Indicates Synchrony Financial network support for given instrument.
REAL_TIME_PAYMENTS
Indicates REAL_TIME_PAYMENTS network support for given instrument.
Copy
"ACCEL"
merchant_partner_customer_id
The unique ID for a customer generated by PayPal.
string
(
merchant_partner_customer_id
)
[ 1 .. 22 ] characters
^[0-9a-zA-Z_-]+$
The unique ID for a customer generated by PayPal.
Copy
"string"
merchant_preferences
The merchant preferences for a subscription.
return_url
string
<
uri
>
[ 10 .. 4000 ] characters
The URL where the customer is redirected after the customer approves the payment.
cancel_url
string
<
uri
>
[ 10 .. 4000 ] characters
The URL where the customer is redirected after the customer cancels the payment.
Copy
{
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
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
given_name
string
<= 140 characters
When the party is a person, the party's given, or first, name.
surname
string
<= 140 characters
When the party is a person, the party's surname or family name. Also known as the last name. Required when the party is a person. Use also to store multiple surnames including the matronymic, or mother's, surname.
Copy
{
"given_name"
:
"string"
,
"surname"
:
"string"
}
Name
The name of the party.
full_name
string
<= 300 characters
When the party is a person, the party's full name.
Copy
{
"full_name"
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
"full_name"
:
"string"
}
Name
The name of the party.
given_name
string
<= 140 characters
When the party is a person, the party's given, or first, name.
surname
string
<= 140 characters
When the party is a person, the party's surname or family name. Also known as the last name. Required when the party is a person. Use also to store multiple surnames including the matronymic, or mother's, surname.
Copy
{
"given_name"
:
"string"
,
"surname"
:
"string"
}
Network
The capability network.
preferred
boolean
Indicates whether the network is the preferred network to complete the operation.
cross_border_transaction_supported
boolean
Is cross border transaction supported.
supported_currencies
Array of
strings
<
ppaas_common_currency_code_v2
>
(
currency_code
)
[ 1 .. 100 ] items
Supported currencies for the instrument.
transfer_type
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Transfer type for particular network.
Enum Value
Description
WIRE
Transfer type wire.
ELECTRONIC
Transfer type electronic.
INSTANT
Transfer type Instant.
STANDARD
Transfer type Standard.
mandate_enforcement
string
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Mandate enforcement for the network.
Enum Value
Description
SEPA
Mandate enforcement.
ELECTRONIC
Mandate enforcement.
network_rules
Array of
strings
[ 1 .. 100 ] items
Specific rules associated with Network.
name
string
(
List of network names
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The capability Network.
Enum Value
Description
ACCEL
Indicates ACCEL network support for given instrument.
AMEX
Indicates AMEX network support for given instrument..
BACS
Indicates BACS network support for given instrument.
BML
Indicates BML network support for given instrument.
CB_NATIONALE
Indicates CB_NATIONALE network support for given instrument.
CET
Indicates CET network support for given instrument.
CETELEM
Indicates CETELEM network support for given instrument.
CHAPS
Indicates CHAPS network support for given instrument.
CHASENET
Indicates CHASENET network support for given instrument.
CHINA_UNION_PAY
Indicates CHINA_UNION_PAY network support for given instrument.
COFIDIS
Indicates COFIDIS network support for given instrument.
COFINOGA
Indicates COFINOGA network support for given instrument.
DELTA
Indicates DELTA network support for given instrument.
DINERS
Indicates DINERS network support for given instrument.
DISCOVER
Indicates DISCOVER network support for given instrument.
EFTPOS
Indicates EFTPOS network support for given instrument.
ELECTRON
Indicates ELECTRON network support for given instrument.
ELO
Indicates ELO network support for given instrument.
FPS
Indicates FPS network support for given instrument.
GE
Indicates GE network support for given instrument.
HIPER
Indicates HIPER network support for given instrument.
HIPERCARD
Indicates HIPERCARD network support for given instrument.
IAV_YODLEE
Indicates IAV_YODLEE network support for given instrument.
JCB
Indicates JCB network support for given instrument.
LOCAL
Indicates LOCAL network support for given instrument.
MAESTRO
Indicates MAESTRO network support for given instrument.
MASTER_CARD
Indicates MASTER_CARD network support for given instrument.
NYCE
Indicates NYCE network support for given instrument.
OPEN_WALLET
Indicates OPEN_WALLET network support for given instrument.
PAYPAL
Indicates PAYPAL network support for given instrument.
POSTEPAY
Indicates POSTEPAY network support for given instrument.
PULSE
Indicates PULSE network support for given instrument.
PWMB
Indicates PWMB network support for given instrument.
RUPAY
Indicates RUPAY network support for given instrument.
SAN
Indicates SAN network support for given instrument.
SEPA
Indicates SEPA network support for given instrument.
SEPA_COR1
Indicates SEPA_COR1 network support for given instrument.
SEPA_CORE
Indicates SEPA_CORE network support for given instrument.
SOLO
Indicates SOLO network support for given instrument.
SSG
Indicates SSG network support for given instrument.
STAR
Indicates STAR network support for given instrument.
STAR_FINANZ
Indicates STAR_FINANZ network support for given instrument.
STAR_ACCESS
Indicates STAR_ACCESS network support for given instrument.
SWITCH
Indicates SWITCH network support for given instrument.
VISA
Indicates VISA network support for given instrument.
WIRE
Indicates WIRE network support for given instrument.
FASTER_CLEARING
Indicates FASTER_CLEARING network support for given instrument.
SYNCHRONY_FINANCIAL_SUPPORT
Indicates Synchrony Financial network support for given instrument.
REAL_TIME_PAYMENTS
Indicates REAL_TIME_PAYMENTS network support for given instrument.
Copy
Expand all
Collapse all
{
"preferred"
:
true
,
"cross_border_transaction_supported"
:
true
,
"supported_currencies"
:
[
"str"
]
,
"transfer_type"
:
"WIRE"
,
"mandate_enforcement"
:
"SEPA"
,
"network_rules"
:
[
"string"
]
,
"name"
:
"ACCEL"
}
network_transaction_reference
Reference values used by the card network to identify a transaction.
id
required
string
[ 9 .. 36 ] characters
^[a-zA-Z0-9-_@.:&+=*^'~#!$%()]+$
Transaction reference id returned by the scheme. For Visa and Amex, this is the "Tran id" field in response. For MasterCard, this is the "BankNet reference id" field in response. For Discover, this is the "NRID" field in response. The pattern we expect for this field from Visa/Amex/CB/Discover is numeric, Mastercard/BNPP is alphanumeric and Paysecure is alphanumeric with special character -.
date
string
= 4 characters
^[0-9]+$
The date that the transaction was authorized by the scheme. This field may not be returned for all networks. MasterCard refers to this field as "BankNet reference date.
acquirer_reference_number
string
[ 1 .. 36 ] characters
^[a-zA-Z0-9]+$
Reference ID issued for the card transaction. This ID can be used to track the transaction across processors, card brands and issuing banks.
network
string
(
card_brand
)
[ 1 .. 255 ] characters
^[A-Z_]+$
Name of the card network through which the transaction was routed.
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
UNKNOWN
UNKNOWN payment network.
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
"acquirer_reference_number"
:
"string"
,
"network"
:
"VISA"
}
Operation Type
The Operation.
string
(
Operation Type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The Operation.
Enum Value
Description
CAPABILITY_OP_SINK
CAPABILITY_OP_SINK.
CAPABILITY_OP_SOURCE
CAPABILITY_OP_SOURCE.
CAPABILITY_OP_READ
CAPABILITY_OP_READ.
READ
READ.
SINK
SINK.
SOURCE
SOURCE.
Copy
"CAPABILITY_OP_SINK"
Orthography Type
The orthography type based on the ISO 15924 names for scripts. Scipts are chosen based on
most widely used writing systems
.
string
(
Orthography Type
)
= 4 characters
^[A-Z][a-z]{3}$
The orthography type based on the ISO 15924 names for scripts. Scipts are chosen based on
most widely used writing systems
.
Enum Value
Description
Zyyy
The orthography cannot be determined.
Zzzz
The orthography is unknown.
Kana
An angular form of Japanese writing for words of foreign origin.
Cyrl
The Slavic languages alphabet. Used in eastern Europe.
Arab
The Arabic language alphabet.
Armn
The Armenian alphabet.
Beng
The Bengali alphabet. Used in eastern India.
Cans
The Unified Canadian Aboriginal Syllabics alphabet.
Deva
The Devanagari (Nagari) alphabet.
Ethi
The Ethiopic alphabet.
Geor
The Georgian (Mkhedruli and Mtavruli) alphabet.
Grek
The Greek alphabet.
Gujr
The Gujurati language alphabet. Used in western India.
Guru
The Gurmukhi alphabet. Used in the northern Indian state of Punjab.
Hani
The Han (Hanzi, Kanji, Hanja) alphabet.
Hebr
The Hebrew alphabet.
Java
The Javanese alphabet.
Jpan
The Japanese (alias for Han + Hiragana + Katakana) alphabet.
Khmr
The Khmer alphabet.
Knda
The Kannada alphabet. Used in the southern Indian state of Karnataka.
Kore
Korean (alias for Hangul + Han).
Laoo
The Lao alphabet.
Latn
The Latin alphabet.
Mlym
The Malayalam alphabet. Used in the southern Indian state of Kerala.
Mong
The Mongolian alphabet.
Mymr
The Myanmar (Burmese) alphabet.
Orya
The Oriya (Odia) alphabet. Used in the eastern Indian state of Odisha.
Sinh
The Sinhala alphabet.
Sund
The Sundanese alphabet.
Syrc
The Syriac alphabet.
Taml
The Tamil alphabet. Used in the southern Indian state of Tamilnadu.
Telu
The Telugu language alphabet. Used in the southern Indian state of Andhra pradesh.
Thaa
The Thaana (Maldivian) alphabet.
Thai
The Thai alphabet. Used in Thailand.
Tibt
The Tibetan alphabet.
Yiii
The Yi alphabet.
Copy
"Zyyy"
pares_status
Transactions status result identifier. The outcome of the issuer's authentication.
string
(
pares_status
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Transactions status result identifier. The outcome of the issuer's authentication.
Enum Value
Description
Y
Successful authentication.
N
Failed authentication / account not verified / transaction denied.
U
Unable to complete authentication.
A
Successful attempts transaction.
C
Challenge required for authentication.
R
Authentication rejected (merchant must not submit for authorization).
D
Challenge required; decoupled authentication confirmed.
I
Informational only; 3DS requestor challenge preference acknowledged.
Copy
"Y"
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
Path format
Provides path format for the image.
string
(
Path format
)
[ 1 .. 100 ] characters
^[0-9A-Z_]+$
Provides path format for the image.
Enum Value
Description
ABSOLUTE
Complete path is given not the CDN.
PARTIAL
Partial path is given e.g. CDN and a specific size can be requested.
Copy
"ABSOLUTE"
payee_payment_method_preference
The merchant-preferred payment methods.
string
(
payee_payment_method_preference
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Default:
"UNRESTRICTED"
The merchant-preferred payment methods.
Enum Value
Description
UNRESTRICTED
Accepts any type of payment from the customer.
IMMEDIATE_PAYMENT_REQUIRED
Accepts only immediate payment from the customer. For example, credit card, PayPal balance, or instant ACH. Ensures that at the time of capture, the payment does not have the
pending
status.
Copy
"UNRESTRICTED"
payer
The customer who approves and pays for the order. The customer is also known as the payer.
email_address
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
The email address of the payer.
payer_id
string
<
ppaas_payer_id_v3
>
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The PayPal-assigned ID for the payer.
name
object
(
Name
)
The name of the payer. Supports only the
given_name
and
surname
properties.
Copy
Expand all
Collapse all
{
"email_address"
:
"string"
,
"payer_id"
:
"string"
,
"name"
:
{
"given_name"
:
"string"
,
"surname"
:
"string"
}
}
payer
The customer who approves and pays for the order. The customer is also known as the payer.
email_address
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
The email address of the payer.
payer_id
string
<
ppaas_payer_id_v3
>
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The PayPal-assigned ID for the payer.
name
object
(
Name
)
The name of the payer. Supports only the
given_name
and
surname
properties.
phone
object
(
phone_with_type
)
The phone number of the customer. Available only when you enable the
Contact Telephone Number
option in the
Profile & Settings
for the merchant's PayPal account. The
phone.phone_number
supports only
national_number
.
Copy
Expand all
Collapse all
{
"email_address"
:
"string"
,
"payer_id"
:
"string"
,
"name"
:
{
"given_name"
:
"string"
,
"surname"
:
"string"
}
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
}
payer_base
The customer who approves and pays for the order. The customer is also known as the payer.
email_address
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
The email address of the payer.
payer_id
string
<
ppaas_payer_id_v3
>
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The PayPal-assigned ID for the payer.
Copy
{
"email_address"
:
"string"
,
"payer_id"
:
"string"
}
payment_initiator
The person or party who initiated or triggered the payment.
string
(
payment_initiator
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The person or party who initiated or triggered the payment.
Enum Value
Description
CUSTOMER
Payment is initiated with the active engagement of the customer. e.g. a customer checking out on a merchant website.
MERCHANT
Payment is initiated by merchant on behalf of the customer without the active engagement of customer. e.g. a merchant charging the monthly payment of a subscription to the customer.
Copy
"CUSTOMER"
payment_method
The customer and merchant payment preferences.
payee_preferred
string
(
payee_payment_method_preference
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Default:
"UNRESTRICTED"
The merchant-preferred payment methods.
Enum Value
Description
UNRESTRICTED
Accepts any type of payment from the customer.
IMMEDIATE_PAYMENT_REQUIRED
Accepts only immediate payment from the customer. For example, credit card, PayPal balance, or instant ACH. Ensures that at the time of capture, the payment does not have the
pending
status.
Copy
{
"payee_preferred"
:
"UNRESTRICTED"
}
payment_preferences
The payment preferences for a subscription.
auto_bill_outstanding
boolean
Default:
true
Indicates whether to automatically bill the outstanding amount in the next billing cycle.
setup_fee_failure_action
string
[ 1 .. 24 ] characters
^[A-Z_]+$
Default:
"CANCEL"
The action to take on the subscription if the initial payment for the setup fails.
Enum Value
Description
CONTINUE
Continues the subscription if the initial payment for the setup fails.
CANCEL
Cancels the subscription if the initial payment for the setup fails.
payment_failure_threshold
integer
[ 0 .. 999 ]
Default:
0
The maximum number of payment failures before a subscription is suspended. For example, if
payment_failure_threshold
is
2
, the subscription automatically updates to the
SUSPEND
state if two consecutive payments fail.
setup_fee
object
(
Money
)
The initial set-up fee for the service.
Copy
Expand all
Collapse all
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
0
,
"setup_fee"
:
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
payment_preferences_override
The payment preferences to override at subscription level.
auto_bill_outstanding
boolean
Indicates whether to automatically bill the outstanding amount in the next billing cycle.
setup_fee_failure_action
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The action to take on the subscription if the initial payment for the setup fails.
Enum Value
Description
CONTINUE
Continues the subscription if the initial payment for the setup fails.
CANCEL
Cancels the subscription if the initial payment for the setup fails.
payment_failure_threshold
integer
[ 0 .. 999 ]
The maximum number of payment failures before a subscription is suspended. For example, if
payment_failure_threshold
is
2
, the subscription automatically updates to the
SUSPEND
state if two consecutive payments fail.
setup_fee
object
(
Money
)
The initial set-up fee for the service.
Copy
Expand all
Collapse all
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
999
,
"setup_fee"
:
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
payment_source
The payment source definition. To be eligible to create subscription using debit or credit card, you will need to sign up here (
https://www.paypal.com/bizsignup/entry/product/ppcp
). Please note, its available only for non-3DS cards and for merchants in US and AU regions.
card
object
(
card
)
The payment card to use to fund a payment. Can be a credit or debit card.
Copy
Expand all
Collapse all
{
"card"
:
{
"name"
:
"string"
,
"number"
:
"stringstrings"
,
"security_code"
:
"stri"
,
"expiry"
:
"string"
,
"type"
:
"CREDIT"
,
"brand"
:
"VISA"
,
"billing_address"
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
}
,
"attributes"
:
{
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
,
"vault"
:
{
"store_in_vault"
:
"ON_SUCCESS"
}
,
"verification"
:
{
"method"
:
"SCA_ALWAYS"
}
}
}
}
payment_source_response
The payment source used to fund the payment.
card
object
(
card_response_with_billing_address
)
The payment card used to fund the payment. Card can be a credit or debit card.
Copy
Expand all
Collapse all
{
"card"
:
{
"name"
:
"string"
,
"last_digits"
:
"string"
,
"available_networks"
:
[
"VISA"
]
,
"from_request"
:
{
"last_digits"
:
"stri"
,
"expiry"
:
"string"
}
,
"stored_credential"
:
{
"payment_initiator"
:
"CUSTOMER"
,
"payment_type"
:
"ONE_TIME"
,
"usage"
:
"FIRST"
,
"previous_network_transaction_reference"
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
"acquirer_reference_number"
:
"string"
,
"network"
:
"VISA"
}
}
,
"brand"
:
"VISA"
,
"type"
:
"CREDIT"
,
"authentication_result"
:
{
"liability_shift"
:
"NO"
,
"three_d_secure"
:
{
"authentication_status"
:
"Y"
,
"enrollment_status"
:
"Y"
}
}
,
"attributes"
:
{
"vault"
:
{
"id"
:
"string"
,
"status"
:
"VAULTED"
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
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
}
}
,
"expiry"
:
"string"
,
"bin_details"
:
{
"bin"
:
"string"
,
"issuing_bank"
:
"string"
,
"products"
:
[
"string"
]
,
"bin_country_code"
:
"string"
}
,
"billing_address"
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
}
,
"currency_code"
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
paypal_wallet_customer
The details about a customer in PayPal's system of record.
id
string
(
merchant_partner_customer_id
)
[ 1 .. 22 ] characters
^[0-9a-zA-Z_-]+$
The unique ID for a customer generated by PayPal.
merchant_customer_id
string
[ 1 .. 64 ] characters
^[0-9a-zA-Z-_.^*$@#]+$
Merchants and partners may already have a data-store where their customer information is persisted. Use merchant_customer_id to associate the PayPal-generated customer.id to your representation of a customer.
Copy
{
"id"
:
"string"
,
"merchant_customer_id"
:
"string"
}
paypal_wallet_customer
The details about a customer in PayPal's system of record.
id
string
(
merchant_partner_customer_id
)
[ 1 .. 22 ] characters
^[0-9a-zA-Z_-]+$
The unique ID for a customer generated by PayPal.
merchant_customer_id
string
[ 1 .. 64 ] characters
^[0-9a-zA-Z-_.^*$@#]+$
Merchants and partners may already have a data-store where their customer information is persisted. Use merchant_customer_id to associate the PayPal-generated customer.id to your representation of a customer.
Copy
{
"id"
:
"string"
,
"merchant_customer_id"
:
"string"
}
paypal_wallet_vault_response
The details about a saved PayPal Wallet payment source.
id
string
[ 1 .. 255 ] characters
The PayPal-generated ID for the saved payment source.
status
string
(
Vault Status
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The vault status.
Enum Value
Description
VAULTED
The payment source has been saved in your customer's vault. This vault status reflects
/v3/vault
status.
CREATED
DEPRECATED. The payment source has been saved in your customer's vault. This status applies to deprecated integration patterns and will not be returned for v3/vault integrations.
APPROVED
Customer has approved the action of saving the specified payment_source into their vault. Use v3/vault/payment-tokens with given setup_token to save the payment source in the vault
customer
object
(
paypal_wallet_customer
)
The details about a customer in PayPal's system of record.
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
"VAULTED"
,
"customer"
:
{
"id"
:
"string"
,
"merchant_customer_id"
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
Copy
{
"country_code"
:
"str"
,
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
phone_with_type
The phone information.
phone_type
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
phone_number
required
object
(
Phone
)
The phone number, in its canonical international
E.164 numbering plan format
. Supports only the
national_number
property.
Copy
Expand all
Collapse all
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
plan
The plan details.
id
string
= 26 characters
^P-[A-Z0-9]*$
The unique PayPal-generated ID for the plan.
product_id
string
= 22 characters
^PROD-[A-Z0-9]*$
The ID for the product.
name
string
[ 1 .. 127 ] characters
^.*$
The plan name.
status
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The plan status.
Enum Value
Description
CREATED
The plan was created. You cannot create subscriptions for a plan in this state.
INACTIVE
The plan is inactive.
ACTIVE
The plan is active. You can only create subscriptions for a plan in this state.
description
string
[ 1 .. 127 ] characters
^.*$
The detailed description of the plan.
billing_cycles
Array of
objects
(
billing_cycle
)
[ 1 .. 12 ] items
An array of billing cycles for trial billing and regular billing. A plan can have at most two trial cycles and only one regular cycle.
quantity_supported
boolean
Default:
false
Indicates whether you can subscribe to this plan by providing a quantity for the goods or service.
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
payment_preferences
object
(
payment_preferences
)
The payment preferences for a subscription.
merchant_preferences
object
(
merchant_preferences
)
The merchant preferences for a subscription.
taxes
object
(
taxes
)
The tax details.
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
The date and time when the plan was created, in
Internet date and time format
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
The date and time when the plan was last updated, in
Internet date and time format
.
Copy
Expand all
Collapse all
{
"id"
:
"stringstringstringstringst"
,
"product_id"
:
"stringstringstringstri"
,
"name"
:
"string"
,
"status"
:
"CREATED"
,
"description"
:
"string"
,
"billing_cycles"
:
[
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
1
,
"total_cycles"
:
1
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
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
}
]
,
"quantity_supported"
:
false
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
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
0
,
"setup_fee"
:
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
"merchant_preferences"
:
{
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
}
,
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
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
plan
The plan details.
product_id
string
= 22 characters
^PROD-[A-Z0-9]*$
The ID for the product.
name
string
[ 1 .. 127 ] characters
^.*$
The plan name.
description
string
[ 1 .. 127 ] characters
^.*$
The detailed description of the plan.
billing_cycles
Array of
objects
(
billing_cycle
)
[ 1 .. 12 ] items
An array of billing cycles for trial billing and regular billing. A plan can have at most two trial cycles and only one regular cycle.
quantity_supported
boolean
Default:
false
Indicates whether you can subscribe to this plan by providing a quantity for the goods or service.
payment_preferences
object
(
payment_preferences
)
The payment preferences for a subscription.
merchant_preferences
object
(
merchant_preferences
)
The merchant preferences for a subscription.
taxes
object
(
taxes
)
The tax details.
Copy
Expand all
Collapse all
{
"product_id"
:
"stringstringstringstri"
,
"name"
:
"string"
,
"description"
:
"string"
,
"billing_cycles"
:
[
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
1
,
"total_cycles"
:
1
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
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
}
]
,
"quantity_supported"
:
false
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
0
,
"setup_fee"
:
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
"merchant_preferences"
:
{
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
}
,
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
}
plan_collection
The list of plans with details.
plans
Array of
objects
(
plan
)
[ 0 .. 32767 ] items
An array of plans.
total_items
integer
[ 0 .. 500000000 ]
The total number of items.
total_pages
integer
[ 0 .. 100000000 ]
The total number of pages.
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
"plans"
:
[
{
"id"
:
"stringstringstringstringst"
,
"product_id"
:
"stringstringstringstri"
,
"name"
:
"string"
,
"status"
:
"CREATED"
,
"description"
:
"string"
,
"billing_cycles"
:
[
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
1
,
"total_cycles"
:
1
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
null
,
"ending_quantity"
:
null
,
"amount"
:
null
}
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
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
}
]
,
"quantity_supported"
:
false
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
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
0
,
"setup_fee"
:
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
"merchant_preferences"
:
{
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
}
,
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
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
]
,
"total_items"
:
500000000
,
"total_pages"
:
100000000
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
plan_override
An inline plan object to customise the subscription. You can override plan level default attributes by providing customised values for the subscription in this object.
billing_cycles
Array of
objects
(
billing_cycle_override
)
[ 1 .. 12 ] items
An array of billing cycles for trial billing and regular billing. The subscription billing cycle definition has to adhere to the plan billing cycle definition.
payment_preferences
object
(
payment_preferences_override
)
The payment preferences to override at subscription level.
taxes
object
(
taxes_override
)
The tax details.
Copy
Expand all
Collapse all
{
"billing_cycles"
:
[
{
"sequence"
:
1
,
"total_cycles"
:
999
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
}
]
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
999
,
"setup_fee"
:
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
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
}
plan_request
The create plan request details.
product_id
required
string
= 22 characters
^PROD-[A-Z0-9]*$
The ID of the product created through Catalog Products API.
name
required
string
[ 1 .. 127 ] characters
^.*$
The plan name.
status
string
[ 1 .. 24 ] characters
^[A-Z_]+$
Default:
"ACTIVE"
The initial state of the plan. Allowed input values are CREATED and ACTIVE.
Enum Value
Description
CREATED
The plan was created. You cannot create subscriptions for a plan in this state.
INACTIVE
The plan is inactive.
ACTIVE
The plan is active. You can only create subscriptions for a plan in this state.
description
string
[ 1 .. 127 ] characters
^.*$
The detailed description of the plan.
billing_cycles
required
Array of
objects
(
billing_cycle
)
[ 1 .. 12 ] items
An array of billing cycles for trial billing and regular billing. A plan can have at most two trial cycles and only one regular cycle.
quantity_supported
boolean
Default:
false
Indicates whether you can subscribe to this plan by providing a quantity for the goods or service.
payment_preferences
required
object
(
payment_preferences
)
The payment preferences for a subscription.
merchant_preferences
object
(
merchant_preferences
)
The merchant preferences for a subscription.
taxes
object
(
taxes
)
The tax details.
Copy
Expand all
Collapse all
{
"product_id"
:
"stringstringstringstri"
,
"name"
:
"string"
,
"status"
:
"CREATED"
,
"description"
:
"string"
,
"billing_cycles"
:
[
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
1
,
"total_cycles"
:
1
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
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
}
]
,
"quantity_supported"
:
false
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
0
,
"setup_fee"
:
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
"merchant_preferences"
:
{
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
}
,
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
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
The first line of the address, such as number and street, for example,
173 Drury Lane
. Needed for data entry, and Compliance and Risk checks. This field needs to pass the full address.
address_line_2
string
<= 300 characters
The second line of the address, for example, a suite or apartment number.
admin_area_2
string
<= 120 characters
A city, town, or village. Smaller than
admin_area_level_1
.
admin_area_1
string
<= 300 characters
The highest-level sub-division in a country, which is usually a province, state, or ISO-3166-2 subdivision. This data is formatted for postal delivery, for example,
CA
and not
California
. Value, by country, is:
UK. A county.
US. A state.
Canada. A province.
Japan. A prefecture.
Switzerland. A
kanton
.
postal_code
string
<= 60 characters
The postal code, which is the ZIP code or equivalent. Typically required for countries with a postal code or an equivalent. See
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
{
"address_line_1"
:
"string"
,
"address_line_2"
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
The first line of the address, such as number and street, for example,
173 Drury Lane
. Needed for data entry, and Compliance and Risk checks. This field needs to pass the full address.
address_line_2
string
<= 300 characters
The second line of the address, for example, a suite or apartment number.
admin_area_2
string
<= 120 characters
A city, town, or village. Smaller than
admin_area_level_1
.
admin_area_1
string
<= 300 characters
The highest-level sub-division in a country, which is usually a province, state, or ISO-3166-2 subdivision. This data is formatted for postal delivery, for example,
CA
and not
California
. Value, by country, is:
UK. A county.
US. A state.
Canada. A province.
Japan. A prefecture.
Switzerland. A
kanton
.
postal_code
string
<= 60 characters
The postal code, which is the ZIP code or equivalent. Typically required for countries with a postal code or an equivalent. See
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
{
"address_line_1"
:
"string"
,
"address_line_2"
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
The first line of the address, such as number and street, for example,
173 Drury Lane
. Needed for data entry, and Compliance and Risk checks. This field needs to pass the full address.
address_line_2
string
<= 300 characters
The second line of the address, for example, a suite or apartment number.
admin_area_2
string
<= 120 characters
A city, town, or village. Smaller than
admin_area_level_1
.
admin_area_1
string
<= 300 characters
The highest-level sub-division in a country, which is usually a province, state, or ISO-3166-2 subdivision. This data is formatted for postal delivery, for example,
CA
and not
California
. Value, by country, is:
UK. A county.
US. A state.
Canada. A province.
Japan. A prefecture.
Switzerland. A
kanton
.
postal_code
string
<= 60 characters
The postal code, which is the ZIP code or equivalent. Typically required for countries with a postal code or an equivalent. See
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
{
"address_line_1"
:
"string"
,
"address_line_2"
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
The first line of the address, such as number and street, for example,
173 Drury Lane
. Needed for data entry, and Compliance and Risk checks. This field needs to pass the full address.
address_line_2
string
<= 300 characters
The second line of the address, for example, a suite or apartment number.
admin_area_2
string
<= 120 characters
A city, town, or village. Smaller than
admin_area_level_1
.
admin_area_1
string
<= 300 characters
The highest-level sub-division in a country, which is usually a province, state, or ISO-3166-2 subdivision. This data is formatted for postal delivery, for example,
CA
and not
California
. Value, by country, is:
UK. A county.
US. A state.
Canada. A province.
Japan. A prefecture.
Switzerland. A
kanton
.
postal_code
string
<= 60 characters
The postal code, which is the ZIP code or equivalent. Typically required for countries with a postal code or an equivalent. See
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
{
"address_line_1"
:
"string"
,
"address_line_2"
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
The first line of the address, such as number and street, for example,
173 Drury Lane
. Needed for data entry, and Compliance and Risk checks. This field needs to pass the full address.
address_line_2
string
<= 300 characters
The second line of the address, for example, a suite or apartment number.
admin_area_2
string
<= 120 characters
A city, town, or village. Smaller than
admin_area_level_1
.
admin_area_1
string
<= 300 characters
The highest-level sub-division in a country, which is usually a province, state, or ISO-3166-2 subdivision. This data is formatted for postal delivery, for example,
CA
and not
California
. Value, by country, is:
UK. A county.
US. A state.
Canada. A province.
Japan. A prefecture.
Switzerland. A
kanton
.
postal_code
string
<= 60 characters
The postal code, which is the ZIP code or equivalent. Typically required for countries with a postal code or an equivalent. See
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
{
"address_line_1"
:
"string"
,
"address_line_2"
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
}
pricing_scheme
The pricing scheme details.
version
integer
[ 0 .. 999 ]
The version of the pricing scheme.
pricing_model
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The pricing model for tiered plan. The
tiers
parameter is required.
Enum Value
Description
VOLUME
A volume pricing model.
TIERED
A tiered pricing model.
tiers
Array of
objects
(
pricing_tier
)
[ 1 .. 32 ] items
An array of pricing tiers which are used for billing volume/tiered plans. pricing_model field has to be specified.
fixed_price
object
(
Money
)
The fixed amount to charge for the subscription. The changes to fixed amount are applicable to both existing and future subscriptions. For existing subscriptions, payments within 10 days of price change are not affected.
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
The date and time when this pricing scheme was created, in
Internet date and time format
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
The date and time when this pricing scheme was last updated, in
Internet date and time format
.
Copy
Expand all
Collapse all
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
pricing_tier
The pricing tier details.
starting_quantity
required
string
[ 1 .. 32 ] characters
^([0-9]+|([0-9]+)?[.][0-9]+)$
The starting quantity for the tier.
ending_quantity
string
[ 1 .. 32 ] characters
^([0-9]+|([0-9]+)?[.][0-9]+)$
The ending quantity for the tier. Optional for the last tier.
amount
required
object
(
Money
)
The pricing amount for the tier.
Copy
Expand all
Collapse all
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
provider
The rewards provider which acts as a gateway to the rewards issuer, for example, the financial instruments' aggregator for multiple banks.
string
(
provider
)
[ 1 .. 256 ] characters
^[0-9a-zA-Z_]+$
The rewards provider which acts as a gateway to the rewards issuer, for example, the financial instruments' aggregator for multiple banks.
Copy
"string"
Reasons for disallowing a funding option.
Reasons for disallowing a funding option.
string
(
Reasons for disallowing a funding option.
)
[ 1 .. 50 ] characters
^[A-Z_]+$
Reasons for disallowing a funding option.
Enum Value
Description
CUSTOM_REASON
Generic bucket.
DISALLOWED_DUE_TO_INCOMPLETE_COMMERCIAL_ENTITY_REGISTRATION
Disallowed due to incomplete entity registration.
UNSUPPORTED_FOR_GAMING
Disallowed because gaming is not supported.
DISALLOWED_DUE_TO_UNSUPPORTED_PROCESSING
Disallowed because processing is not supported.
UNSUPPORTED_CURRENCY_CODE
Disallowed because currency code is not supported.
DISALLOWED_DUE_TO_UNSUPPORTED_MCC
Disallowed because MCC is not supported.
Copy
"CUSTOM_REASON"
Redemption type
The rewards redemption type.
string
(
Redemption type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The rewards redemption type.
Enum Value
Description
STATEMENT_CREDIT
Indicates that authorization should be performed on the card whenever the rewards are used in the transaction.
REAL_TIME
Indicates that authorization should be performed on the rewards instrument.
STATEMENT_CREDIT_WITH_CHOICE
The statement credit redemption with choice to specify the amount.
Copy
"STATEMENT_CREDIT"
Rewards Account
A rewards account resource.
account_number
string
[ 1 .. 256 ] characters
^[A-Za-z0-9-_.+/=]+$
The permanent account number (PAN) for card with which this rewards account is associated or the account number of the rewards account, like Honey Gold rewards. And pattern supports JWT, Plain(account number of the instrument), Encrypted.
capabilities
Array of
objects
(
Capability
)
[ 1 .. 100 ] items
Capabilities for the rewards account.
networks
Array of
objects
(
Network
)
[ 1 .. 100 ] items
Networks support for the rewards account.
institution_images
Array of
objects
(
Institution art images content
)
[ 1 .. 100 ] items
Institution images and related image details (as card art).
urls
Array of
objects
(
A URL details of an institution
)
[ 1 .. 40 ] items
Provides all the URLs applicable for the rewards program, for example, settings and terms & conditions. Because for different rewards programs, URLs may vary, they are user wallet's attribute.
registration_id
string
(
external_reference_id
)
[ 1 .. 256 ] characters
^.+$
The registration ID or external identifier.
expiration_date
string
(
date_year_month
)
= 7 characters
^[0-9]{4}-(0[1-9]|1[0-2])$
The rewards expiry date, in
YYYY-MM
format.
issuer
object
(
Rewards issuer details
)
The issuer of the rewards account.
balance
object
(
Rewards Denomination details
)
The rewards denomination details.
beneficiary_name
object
(
Name
)
The beneficiary name on the rewards account.
redemption_type
string
(
Redemption type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The rewards redemption type like STATEMENT_CREDIT or REAL_TIME.
Enum Value
Description
STATEMENT_CREDIT
Indicates that authorization should be performed on the card whenever the rewards are used in the transaction.
REAL_TIME
Indicates that authorization should be performed on the rewards instrument.
STATEMENT_CREDIT_WITH_CHOICE
The statement credit redemption with choice to specify the amount.
status
string
(
Status of the Instrument
)
[ 1 .. 12 ] characters
^[A-Z_]+$
Status of the rewards account.
Enum Value
Description
OPEN
Status of the instrument - OPEN. Instrument is available for transactions.
CLOSED
Status of the instrument - CLOSED. Instrument is unavailable for transactions.
type
string
(
Rewards account type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Type of rewards account.
Enum Value
Description
STANDALONE
Indicates rewards account, like Honey Gold, that is independent of a specific instrument.
INSTRUMENT_RELATED
A rewards account that is associated with an external card.
Copy
Expand all
Collapse all
{
"account_number"
:
"string"
,
"capabilities"
:
[
{
"name"
:
"INSTALLMENT"
,
"mode"
:
"NON_REAL_TIME"
,
"networks"
:
[
{
"preferred"
:
true
,
"cross_border_transaction_supported"
:
true
,
"supported_currencies"
:
[
"str"
]
,
"transfer_type"
:
"WIRE"
,
"mandate_enforcement"
:
"SEPA"
,
"network_rules"
:
[
"string"
]
,
"name"
:
"ACCEL"
}
]
,
"capability_initiator"
:
"PAYPAL"
,
"operation_type"
:
"CAPABILITY_OP_SINK"
}
]
,
"networks"
:
[
{
"preferred"
:
true
,
"cross_border_transaction_supported"
:
true
,
"supported_currencies"
:
[
"str"
]
,
"transfer_type"
:
"WIRE"
,
"mandate_enforcement"
:
"SEPA"
,
"network_rules"
:
[
"string"
]
,
"name"
:
"ACCEL"
}
]
,
"institution_images"
:
[
{
"image_details"
:
[
{
"original_mime_type"
:
"string"
,
"original_width"
:
2147483647
,
"original_height"
:
2147483647
,
"background_color"
:
"string"
,
"foreground_color"
:
"string"
,
"label_color"
:
"string"
,
"location_type"
:
"INTERNAL"
,
"image_path"
:
"
http://example.com
"
,
"path_format_type"
:
"ABSOLUTE"
}
]
,
"image_classification"
:
"NETWORK"
,
"category"
:
"PRIMARY"
}
]
,
"urls"
:
[
{
"type"
:
"SETTINGS"
,
"url"
:
"
http://example.com
"
}
]
,
"registration_id"
:
"string"
,
"expiration_date"
:
"strings"
,
"issuer"
:
{
"name"
:
{
"name"
:
"string"
,
"orthography"
:
"Zyyy"
}
,
"provider"
:
"string"
,
"sponsor_id"
:
"string"
,
"sponsor_account_id"
:
"string"
,
"sponsor_instrument_type"
:
"string"
,
"country_code"
:
"st"
,
"display_name"
:
{
"name"
:
"string"
,
"orthography"
:
"Zyyy"
}
,
"customer_support_email"
:
"string"
,
"product_description"
:
"string"
}
,
"balance"
:
{
"balance_eligible"
:
true
,
"monetary"
:
true
,
"rewards_program_currency_code"
:
"string"
,
"rewards_program_denomination_value"
:
"string"
,
"type"
:
"CURRENCY"
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
"conversion_factor"
:
"string"
,
"target_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"denomination_type_description"
:
"string"
,
"minimum_target_currency_rewards_spend"
:
"string"
,
"maximum_target_currency_rewards_spend"
:
"string"
,
"program_currency_decimal_precision"
:
50
,
"target_currency_decimal_precision"
:
50
,
"target_currency_rounding_mode"
:
"UP"
,
"program_currency_rounding_mode"
:
"UP"
,
"balance_snapshot_key"
:
"string"
,
"target_currency_code"
:
"string"
}
,
"beneficiary_name"
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
"full_name"
:
"string"
}
,
"redemption_type"
:
"STATEMENT_CREDIT"
,
"status"
:
"OPEN"
,
"type"
:
"STANDALONE"
}
Rewards account type
Type of rewards account.
string
(
Rewards account type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Type of rewards account.
Enum Value
Description
STANDALONE
Indicates rewards account, like Honey Gold, that is independent of a specific instrument.
INSTRUMENT_RELATED
A rewards account that is associated with an external card.
Copy
"STANDALONE"
Rewards Denomination details
The rewards denomination details.
balance_eligible
boolean
The flag to represent the rewards eligibility. Added for Chase Pay®.
monetary
boolean
The flag to indicate whether the rewards are monetary or not.
rewards_program_currency_code
string
[ 1 .. 32 ] characters
^[0-9A-Za-z_]+$
The currency code for rewards program example CBB, MI2, WPTS, TYP, Cash, Points etc. This is not ISO currency code.
rewards_program_denomination_value
string
[ 1 .. 32 ] characters
^(-?[0-9A-Za-z.+-]+)$
The Denomination value for rewards program.
type
string
(
Denomination Type
)
[ 1 .. 128 ] characters
^[0-9A-Z_]+$
The denomination type.
Enum Value
Description
CURRENCY
The currency denomination type.
REWARDS_CURRENCY
The rewards currency denomination type.
amount
object
(
Money
)
The amount.
conversion_factor
string
(
float_value
)
[ 1 .. 50 ] characters
^(-?[0-9]+([.][0-9]*)?|[.][0-9]+)$
The conversion factor.
target_amount
object
(
Money
)
The target amount
denomination_type_description
string
(
description
)
[ 1 .. 256 ] characters
The denomination type description. This can contain information like ThankYou Points.
minimum_target_currency_rewards_spend
string
(
float_value
)
[ 1 .. 50 ] characters
^(-?[0-9]+([.][0-9]*)?|[.][0-9]+)$
The minimum rewards to spend in the target currency.
maximum_target_currency_rewards_spend
string
(
float_value
)
[ 1 .. 50 ] characters
^(-?[0-9]+([.][0-9]*)?|[.][0-9]+)$
The maximum rewards to spend in the target currency.
program_currency_decimal_precision
integer
(
currency_decimal_precision
)
[ 0 .. 50 ]
The decimal precision to be used for the program currency.
target_currency_decimal_precision
integer
(
currency_decimal_precision
)
[ 0 .. 50 ]
The decimal precision to be used for the target currency.
target_currency_rounding_mode
string
(
rounding_mode
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The rounding mode to be applied to the target currency.
Enum Value
Description
UP
Round away from zero.
DOWN
Round toward zero.
HALF_UP
Round toward nearest neighbor unless both neighbors are equidistant. If equidistant, round up.
HALF_DOWN
Round toward nearest neighbor unless both neighbors are equidistant. If equidistant, round down.
HALF_EVEN
Round toward the nearest neighbor unless both neighbors are equidistant. If equidistant, round toward the even neighbor.
UNNECESSARY
Because the requested operation has an exact result, no rounding is necessary.
program_currency_rounding_mode
string
(
rounding_mode
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The rounding mode to be applied to the program currency.
Enum Value
Description
UP
Round away from zero.
DOWN
Round toward zero.
HALF_UP
Round toward nearest neighbor unless both neighbors are equidistant. If equidistant, round up.
HALF_DOWN
Round toward nearest neighbor unless both neighbors are equidistant. If equidistant, round down.
HALF_EVEN
Round toward the nearest neighbor unless both neighbors are equidistant. If equidistant, round toward the even neighbor.
UNNECESSARY
Because the requested operation has an exact result, no rounding is necessary.
balance_snapshot_key
string
(
snapshot_key
)
[ 1 .. 128 ] characters
^.+$
This is a unique number generated by Issuer for each account rewards request. Applicable for any statement credit redemption cases like ChasePay. The key which ties back to the snapshot of the rewards balance that's used for the transaction.
target_currency_code
string
<
ppaas_common_currency_code_v2
>
(
currency_code
)
= 3 characters
The primary
ISO 4217
3-letter alphabetic code that represents the target currency for reward instrument.
Copy
Expand all
Collapse all
{
"balance_eligible"
:
true
,
"monetary"
:
true
,
"rewards_program_currency_code"
:
"string"
,
"rewards_program_denomination_value"
:
"string"
,
"type"
:
"CURRENCY"
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
"conversion_factor"
:
"string"
,
"target_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"denomination_type_description"
:
"string"
,
"minimum_target_currency_rewards_spend"
:
"string"
,
"maximum_target_currency_rewards_spend"
:
"string"
,
"program_currency_decimal_precision"
:
50
,
"target_currency_decimal_precision"
:
50
,
"target_currency_rounding_mode"
:
"UP"
,
"program_currency_rounding_mode"
:
"UP"
,
"balance_snapshot_key"
:
"string"
,
"target_currency_code"
:
"string"
}
Rewards issuer details
The rewards account issuer related details.
name
object
(
Full Name with orthography
)
Issuer name.
provider
string
(
provider
)
[ 1 .. 256 ] characters
^[0-9a-zA-Z_]+$
The rewards provider which acts as a gateway to the rewards issuer, for example, the financial instruments' aggregator for multiple banks.
sponsor_id
string
(
sponsor_id
)
[ 1 .. 32 ] characters
^[0-9A-Z]+(?:-[0-9A-Z]+)*$
Encrypted identifier of the rewards sponsor or institution that manages the payment instrument.
sponsor_account_id
string
(
sponsor_account_id
)
[ 1 .. 256 ] characters
^[A-Za-z0-9-_.+/=]+$
The encrypted identifier of the main account of the rewards sponsor.
sponsor_instrument_type
string
(
sponsor_instrument_type
)
[ 1 .. 256 ] characters
^[A-Za-z0-9-_.+/=]+$
The sponsor-supported payment instrument type.
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
Country Code of the Issuer.
display_name
object
(
Full Name with orthography
)
The issuer name of the rewards to be displayed to the user.
customer_support_email
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
This issuer's customer support email address.
product_description
string
(
description
)
[ 1 .. 256 ] characters
This is the card issuer's product and brand information, for example, Costco Anywhere Visa® Card by Citi.
Copy
Expand all
Collapse all
{
"name"
:
{
"name"
:
"string"
,
"orthography"
:
"Zyyy"
}
,
"provider"
:
"string"
,
"sponsor_id"
:
"string"
,
"sponsor_account_id"
:
"string"
,
"sponsor_instrument_type"
:
"string"
,
"country_code"
:
"st"
,
"display_name"
:
{
"name"
:
"string"
,
"orthography"
:
"Zyyy"
}
,
"customer_support_email"
:
"string"
,
"product_description"
:
"string"
}
rounding_mode
The rounding modes for a given rewards program currency.
string
(
rounding_mode
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The rounding modes for a given rewards program currency.
Enum Value
Description
UP
Round away from zero.
DOWN
Round toward zero.
HALF_UP
Round toward nearest neighbor unless both neighbors are equidistant. If equidistant, round up.
HALF_DOWN
Round toward nearest neighbor unless both neighbors are equidistant. If equidistant, round down.
HALF_EVEN
Round toward the nearest neighbor unless both neighbors are equidistant. If equidistant, round toward the even neighbor.
UNNECESSARY
Because the requested operation has an exact result, no rounding is necessary.
Copy
"UP"
shipping_detail
The shipping details.
type
string
(
Fulfillment Type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
A classification for the method of purchase fulfillment (e.g shipping, in-store pickup, etc). Either
type
or
options
may be present, but not both.
Enum Value
Description
SHIPPING
The payer intends to receive the items at a specified address.
PICKUP_IN_PERSON
DEPRECATED. Please use "PICKUP_FROM_PERSON" instead.
PICKUP_IN_STORE
The payer intends to pick up the item(s) from the payee's physical store. Also termed as BOPIS, "Buy Online, Pick-up in Store". Seller protection is provided with this option.
PICKUP_FROM_PERSON
The payer intends to pick up the item(s) from the payee in person. Also termed as BOPIP, "Buy Online, Pick-up in Person". Seller protection is not available, since the payer is receiving the item from the payee in person, and can validate the item prior to payment.
options
Array of
objects
(
shipping_option
)
[ 0 .. 10 ] items
An array of shipping options that the payee or merchant offers to the payer to ship or pick up their items.
name
object
(
Name
)
The name of the person to whom to ship the items. Supports only the
full_name
property.
email_address
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
The email address of the recipient of the shipped items, which may belong to either the payer, or an alternate contact, for delivery.
phone_number
object
(
Phone
)
The phone number of the recipient of the shipped items, which may belong to either the payer, or an alternate contact, for delivery. [Format - canonical international
E.164 numbering plan
]
address
object
(
Portable Postal Address (Medium-Grained)
)
The address of the person to whom to ship the items. Supports only the
address_line_1
,
address_line_2
,
admin_area_1
,
admin_area_2
,
postal_code
, and
country_code
properties.
Copy
Expand all
Collapse all
{
"type"
:
"SHIPPING"
,
"options"
:
[
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
]
,
"name"
:
{
"full_name"
:
"string"
}
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
}
}
shipping_option
The options that the payee or merchant offers to the payer to ship or pick up their items.
id
required
string
<= 127 characters
A unique ID that identifies a payer-selected shipping option.
label
required
string
<= 127 characters
A description that the payer sees, which helps them choose an appropriate shipping option. For example,
Free Shipping
,
USPS Priority Shipping
,
Expédition prioritaire USPS
, or
USPS yōuxiān fā huò
. Localize this description to the payer's locale.
selected
required
boolean
If the API request sets
selected = true
, it represents the shipping option that the payee or merchant expects to be pre-selected for the payer when they first view the
shipping.options
in the PayPal Checkout experience. As part of the response if a
shipping.option
contains
selected=true
, it represents the shipping option that the payer selected during the course of checkout with PayPal. Only one
shipping.option
can be set to
selected=true
.
type
string
(
shipping_type
)
A classification for the method of purchase fulfillment.
Enum Value
Description
SHIPPING
The payer intends to receive the items at a specified address.
PICKUP
DEPRECATED. To ensure that seller protection is correctly assigned, please use 'PICKUP_IN_STORE' or 'PICKUP_FROM_PERSON' instead. Currently, this field indicates that the payer intends to pick up the items at a specified address (ie. a store address).
PICKUP_IN_STORE
The payer intends to pick up the item(s) from the payee's physical store. Also termed as BOPIS, "Buy Online, Pick-up in Store". Seller protection is provided with this option.
PICKUP_FROM_PERSON
The payer intends to pick up the item(s) from the payee in person. Also termed as BOPIP, "Buy Online, Pick-up in Person". Seller protection is not available, since the payer is receiving the item from the payee in person, and can validate the item prior to payment.
amount
object
(
Money
)
The shipping cost for the selected option.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
shipping_type
A classification for the method of purchase fulfillment.
string
(
shipping_type
)
A classification for the method of purchase fulfillment.
Enum Value
Description
SHIPPING
The payer intends to receive the items at a specified address.
PICKUP
DEPRECATED. To ensure that seller protection is correctly assigned, please use 'PICKUP_IN_STORE' or 'PICKUP_FROM_PERSON' instead. Currently, this field indicates that the payer intends to pick up the items at a specified address (ie. a store address).
PICKUP_IN_STORE
The payer intends to pick up the item(s) from the payee's physical store. Also termed as BOPIS, "Buy Online, Pick-up in Store". Seller protection is provided with this option.
PICKUP_FROM_PERSON
The payer intends to pick up the item(s) from the payee in person. Also termed as BOPIP, "Buy Online, Pick-up in Person". Seller protection is not available, since the payer is receiving the item from the payee in person, and can validate the item prior to payment.
Copy
"SHIPPING"
snapshot_key
This is a unique number generated by Issuer for each account rewards request.
string
(
snapshot_key
)
[ 1 .. 128 ] characters
^.+$
This is a unique number generated by Issuer for each account rewards request.
Copy
"string"
sponsor_account_id
The encrypted identifier of the sponsor's main account.
string
(
sponsor_account_id
)
[ 1 .. 256 ] characters
^[A-Za-z0-9-_.+/=]+$
The encrypted identifier of the sponsor's main account.
Copy
"string"
sponsor_id
Encrypted Sponsor identifier of issuer/institution which manages the payment token which controls characteristics of the instrument and is associated with how the instrument is processed.
string
(
sponsor_id
)
[ 1 .. 32 ] characters
^[0-9A-Z]+(?:-[0-9A-Z]+)*$
Encrypted Sponsor identifier of issuer/institution which manages the payment token which controls characteristics of the instrument and is associated with how the instrument is processed.
Copy
"string"
sponsor_instrument_type
The issuer-supported payment instrument type.
string
(
sponsor_instrument_type
)
[ 1 .. 256 ] characters
^[A-Za-z0-9-_.+/=]+$
The issuer-supported payment instrument type.
Copy
"string"
Status of the Instrument
Status of the instrument, indicates whether it is available for clients.
string
(
Status of the Instrument
)
[ 1 .. 12 ] characters
^[A-Z_]+$
Status of the instrument, indicates whether it is available for clients.
Enum Value
Description
OPEN
Status of the instrument - OPEN. Instrument is available for transactions.
CLOSED
Status of the instrument - CLOSED. Instrument is unavailable for transactions.
Copy
"OPEN"
store_in_vault_instruction
Defines how and when the payment source gets vaulted.
string
(
store_in_vault_instruction
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Defines how and when the payment source gets vaulted.
Value
Description
ON_SUCCESS
Defines that the payment_source will be vaulted only when at least one authorization or capture using that payment_source is successful.
Copy
"ON_SUCCESS"
stored_payment_source_payment_type
Indicates the type of the stored payment_source payment.
string
(
stored_payment_source_payment_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Indicates the type of the stored payment_source payment.
Enum Value
Description
ONE_TIME
One Time payment such as online purchase or donation. (e.g. Checkout with one-click).
RECURRING
Payment which is part of a series of payments with fixed or variable amounts, following a fixed time interval. (e.g. Subscription payments).
UNSCHEDULED
Payment which is part of a series of payments that occur on a non-fixed schedule and/or have variable amounts. (e.g. Account Topup payments).
Copy
"ONE_TIME"
stored_payment_source_usage_type
Indicates if this is a
first
or
subsequent
payment using a stored payment source (also referred to as stored credential or card on file).
string
(
stored_payment_source_usage_type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Default:
"DERIVED"
Indicates if this is a
first
or
subsequent
payment using a stored payment source (also referred to as stored credential or card on file).
Enum Value
Description
FIRST
Indicates the Initial/First payment with a payment_source that is intended to be stored upon successful processing of the payment.
SUBSEQUENT
Indicates a payment using a stored payment_source which has been successfully used previously for a payment.
DERIVED
Indicates that PayPal will derive the value of
FIRST
or
SUBSEQUENT
based on data available to PayPal.
Copy
"FIRST"
subscriber
The subscriber response information.
email_address
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
The email address of the payer.
payer_id
string
<
ppaas_payer_id_v3
>
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The PayPal-assigned ID for the payer.
name
object
(
Name
)
The name of the payer. Supports only the
given_name
and
surname
properties.
shipping_address
object
(
shipping_detail
)
The shipping details.
payment_source
object
(
payment_source_response
)
The payment source used to fund the payment.
Copy
Expand all
Collapse all
{
"email_address"
:
"string"
,
"payer_id"
:
"string"
,
"name"
:
{
"given_name"
:
"string"
,
"surname"
:
"string"
}
,
"shipping_address"
:
{
"type"
:
"SHIPPING"
,
"options"
:
[
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
]
,
"name"
:
{
"full_name"
:
"string"
}
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
}
}
,
"payment_source"
:
{
"card"
:
{
"name"
:
"string"
,
"last_digits"
:
"string"
,
"available_networks"
:
[
"VISA"
]
,
"from_request"
:
{
"last_digits"
:
"stri"
,
"expiry"
:
"string"
}
,
"stored_credential"
:
{
"payment_initiator"
:
"CUSTOMER"
,
"payment_type"
:
"ONE_TIME"
,
"usage"
:
"FIRST"
,
"previous_network_transaction_reference"
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
"acquirer_reference_number"
:
"string"
,
"network"
:
"VISA"
}
}
,
"brand"
:
"VISA"
,
"type"
:
"CREDIT"
,
"authentication_result"
:
{
"liability_shift"
:
"NO"
,
"three_d_secure"
:
{
"authentication_status"
:
"Y"
,
"enrollment_status"
:
"Y"
}
}
,
"attributes"
:
{
"vault"
:
{
"id"
:
"string"
,
"status"
:
"VAULTED"
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
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
null
}
}
,
"merchant_customer_id"
:
"string"
}
}
}
,
"expiry"
:
"string"
,
"bin_details"
:
{
"bin"
:
"string"
,
"issuing_bank"
:
"string"
,
"products"
:
[
"string"
]
,
"bin_country_code"
:
"string"
}
,
"billing_address"
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
}
,
"currency_code"
:
"string"
}
}
}
subscriber_request
The subscriber request information .
email_address
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
The email address of the payer.
payer_id
string
<
ppaas_payer_id_v3
>
(
PayPal Account Identifier
)
= 13 characters
^[2-9A-HJ-NP-Z]{13}$
The PayPal-assigned ID for the payer.
name
object
(
Name
)
The name of the payer. Supports only the
given_name
and
surname
properties.
phone
object
(
phone_with_type
)
The phone number of the customer. Available only when you enable the
Contact Telephone Number
option in the
Profile & Settings
for the merchant's PayPal account. The
phone.phone_number
supports only
national_number
.
shipping_address
object
(
shipping_detail
)
The shipping details.
payment_source
object
(
payment_source
)
The payment source definition. To be eligible to create subscription using debit or credit card, you will need to sign up here (
https://www.paypal.com/bizsignup/entry/product/ppcp
). Please note, its available only for non-3DS cards and for merchants in US and AU regions.
Copy
Expand all
Collapse all
{
"email_address"
:
"string"
,
"payer_id"
:
"string"
,
"name"
:
{
"given_name"
:
"string"
,
"surname"
:
"string"
}
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"shipping_address"
:
{
"type"
:
"SHIPPING"
,
"options"
:
[
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
]
,
"name"
:
{
"full_name"
:
"string"
}
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
}
}
,
"payment_source"
:
{
"card"
:
{
"name"
:
"string"
,
"number"
:
"stringstrings"
,
"security_code"
:
"stri"
,
"expiry"
:
"string"
,
"type"
:
"CREDIT"
,
"brand"
:
"VISA"
,
"billing_address"
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
}
,
"attributes"
:
{
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"merchant_customer_id"
:
"string"
}
,
"vault"
:
{
"store_in_vault"
:
"ON_SUCCESS"
}
,
"verification"
:
{
"method"
:
"SCA_ALWAYS"
}
}
}
}
}
subscription
The subscription details.
status
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The status of the subscription.
Enum Value
Description
APPROVAL_PENDING
The subscription is created but not yet approved by the buyer.
APPROVED
The buyer has approved the subscription.
ACTIVE
The subscription is active.
SUSPENDED
The subscription is suspended.
CANCELLED
The subscription is cancelled.
EXPIRED
The subscription is expired.
status_change_note
string
[ 1 .. 128 ] characters
^.*$
The reason or notes for the status of the subscription.
status_update_time
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
id
string
[ 3 .. 50 ] characters
The PayPal-generated ID for the subscription.
plan_id
string
[ 3 .. 50 ] characters
The ID of the plan.
quantity
string
[ 1 .. 32 ] characters
^([0-9]+|([0-9]+)?[.][0-9]+)$
The quantity of the product in the subscription.
custom_id
string
[ 1 .. 127 ] characters
^[\x20-\x7E]+
The custom id for the subscription. Can be invoice id.
plan_overridden
boolean
Indicates whether the subscription has overridden any plan attributes.
links
Array of
objects
(
Link Description
)
An array of request-related
HATEOAS links
.
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
shipping_amount
object
(
Money
)
The currency and amount for a financial transaction, such as a balance or payment due.
subscriber
object
<
payer_v1
>
(
subscriber
)
The subscriber response information.
billing_info
object
(
subscription_billing_info
)
The billing details for the subscription. If the subscription was or is active, these fields are populated.
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
The date and time, in
Internet date and time format
. Seconds are required while fractional seconds are optional.
Note:
The regular expression provides guidance but does not reject all invalid dates.
plan
object
(
plan
)
Inline plan details.
Copy
Expand all
Collapse all
{
"status"
:
"APPROVAL_PENDING"
,
"status_change_note"
:
"string"
,
"status_update_time"
:
"string"
,
"id"
:
"string"
,
"plan_id"
:
"string"
,
"quantity"
:
"string"
,
"custom_id"
:
"string"
,
"plan_overridden"
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
"start_time"
:
"string"
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
"subscriber"
:
{
"email_address"
:
"string"
,
"payer_id"
:
"string"
,
"name"
:
{
"given_name"
:
"string"
,
"surname"
:
"string"
}
,
"shipping_address"
:
{
"type"
:
"SHIPPING"
,
"options"
:
[
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
]
,
"name"
:
{
"full_name"
:
"string"
}
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
}
}
,
"payment_source"
:
{
"card"
:
{
"name"
:
"string"
,
"last_digits"
:
"string"
,
"available_networks"
:
[
"VISA"
]
,
"from_request"
:
{
"last_digits"
:
"stri"
,
"expiry"
:
"string"
}
,
"stored_credential"
:
{
"payment_initiator"
:
"CUSTOMER"
,
"payment_type"
:
"ONE_TIME"
,
"usage"
:
"FIRST"
,
"previous_network_transaction_reference"
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
"acquirer_reference_number"
:
"string"
,
"network"
:
"VISA"
}
}
,
"brand"
:
"VISA"
,
"type"
:
"CREDIT"
,
"authentication_result"
:
{
"liability_shift"
:
"NO"
,
"three_d_secure"
:
{
"authentication_status"
:
"Y"
,
"enrollment_status"
:
"Y"
}
}
,
"attributes"
:
{
"vault"
:
{
"id"
:
"string"
,
"status"
:
"VAULTED"
,
"links"
:
[
{
"href"
:
null
,
"rel"
:
null
,
"method"
:
null
}
]
,
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
null
,
"phone_number"
:
null
}
,
"merchant_customer_id"
:
"string"
}
}
}
,
"expiry"
:
"string"
,
"bin_details"
:
{
"bin"
:
"string"
,
"issuing_bank"
:
"string"
,
"products"
:
[
"string"
]
,
"bin_country_code"
:
"string"
}
,
"billing_address"
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
}
,
"currency_code"
:
"string"
}
}
}
,
"billing_info"
:
{
"cycle_executions"
:
[
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
99
,
"cycles_completed"
:
9999
,
"cycles_remaining"
:
9999
,
"current_pricing_scheme_version"
:
1
,
"total_cycles"
:
999
}
]
,
"failed_payments_count"
:
999
,
"outstanding_balance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"last_payment"
:
{
"status"
:
"COMPLETED"
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
"time"
:
"string"
}
,
"next_billing_time"
:
"string"
,
"final_payment_time"
:
"string"
,
"last_failed_payment"
:
{
"reason_code"
:
"PAYMENT_DENIED"
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
"time"
:
"string"
,
"next_payment_retry_time"
:
"string"
}
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
"plan"
:
{
"product_id"
:
"stringstringstringstri"
,
"name"
:
"string"
,
"description"
:
"string"
,
"billing_cycles"
:
[
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
1
,
"total_cycles"
:
1
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
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
}
]
,
"quantity_supported"
:
false
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
0
,
"setup_fee"
:
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
"merchant_preferences"
:
{
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
}
,
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
}
}
subscription_activate_request
The activate subscription request details.
reason
string
[ 1 .. 128 ] characters
^.*$
The reason for activation of a subscription. Required to reactivate the subscription.
Copy
{
"reason"
:
"string"
}
subscription_billing_info
The billing details for the subscription. If the subscription was or is active, these fields are populated.
cycle_executions
Array of
objects
(
cycle_execution
)
[ 0 .. 3 ] items
The trial and regular billing executions.
failed_payments_count
required
integer
[ 0 .. 999 ]
The number of consecutive payment failures. Resets to
0
after a successful payment. If this reaches the
payment_failure_threshold
value, the subscription updates to the
SUSPENDED
state.
outstanding_balance
required
object
(
Money
)
The total pending bill amount, to be paid by the subscriber.
last_payment
object
(
last_payment_details
)
The details for the last payment of the subscription.
next_billing_time
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
The next date and time for billing this subscription, in
Internet date and time format
.
final_payment_time
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
The date and time when the final billing cycle occurs, in
Internet date and time format
.
last_failed_payment
object
(
failed_payment_details
)
The details for the last failed payment of the subscription.
Copy
Expand all
Collapse all
{
"cycle_executions"
:
[
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
99
,
"cycles_completed"
:
9999
,
"cycles_remaining"
:
9999
,
"current_pricing_scheme_version"
:
1
,
"total_cycles"
:
999
}
]
,
"failed_payments_count"
:
999
,
"outstanding_balance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"last_payment"
:
{
"status"
:
"COMPLETED"
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
"time"
:
"string"
}
,
"next_billing_time"
:
"string"
,
"final_payment_time"
:
"string"
,
"last_failed_payment"
:
{
"reason_code"
:
"PAYMENT_DENIED"
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
"time"
:
"string"
,
"next_payment_retry_time"
:
"string"
}
}
subscription_cancel_request
The cancel subscription request details.
reason
required
string
[ 1 .. 128 ] characters
^.*$
The reason for the cancellation of a subscription.
Copy
{
"reason"
:
"string"
}
subscription_capture_request
The charge amount from the subscriber.
note
required
string
[ 1 .. 128 ] characters
^.*$
The reason or note for the subscription charge.
capture_type
required
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The type of capture.
Value
Description
OUTSTANDING_BALANCE
The outstanding balance that the subscriber must clear.
amount
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
"note"
:
"string"
,
"capture_type"
:
"OUTSTANDING_BALANCE"
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
subscription_collection
The list of subscriptions.
subscriptions
Array of
objects
(
subscription
)
[ 0 .. 32767 ] items
An array of subscriptions.
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
"subscriptions"
:
[
{
"status"
:
"APPROVAL_PENDING"
,
"status_change_note"
:
"string"
,
"status_update_time"
:
"string"
,
"id"
:
"string"
,
"plan_id"
:
"string"
,
"quantity"
:
"string"
,
"custom_id"
:
"string"
,
"plan_overridden"
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
"start_time"
:
"string"
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
"subscriber"
:
{
"email_address"
:
"string"
,
"payer_id"
:
"string"
,
"name"
:
{
"given_name"
:
"string"
,
"surname"
:
"string"
}
,
"shipping_address"
:
{
"type"
:
"SHIPPING"
,
"options"
:
[
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
]
,
"name"
:
{
"full_name"
:
"string"
}
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
}
}
,
"payment_source"
:
{
"card"
:
{
"name"
:
"string"
,
"last_digits"
:
"string"
,
"available_networks"
:
[
"VISA"
]
,
"from_request"
:
{
"last_digits"
:
"stri"
,
"expiry"
:
"string"
}
,
"stored_credential"
:
{
"payment_initiator"
:
"CUSTOMER"
,
"payment_type"
:
"ONE_TIME"
,
"usage"
:
"FIRST"
,
"previous_network_transaction_reference"
:
{
"id"
:
null
,
"date"
:
null
,
"acquirer_reference_number"
:
null
,
"network"
:
null
}
}
,
"brand"
:
"VISA"
,
"type"
:
"CREDIT"
,
"authentication_result"
:
{
"liability_shift"
:
"NO"
,
"three_d_secure"
:
{
"authentication_status"
:
null
,
"enrollment_status"
:
null
}
}
,
"attributes"
:
{
"vault"
:
{
"id"
:
null
,
"status"
:
null
,
"links"
:
[ ]
,
"customer"
:
null
}
}
,
"expiry"
:
"string"
,
"bin_details"
:
{
"bin"
:
"string"
,
"issuing_bank"
:
"string"
,
"products"
:
[
null
]
,
"bin_country_code"
:
"string"
}
,
"billing_address"
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
}
,
"currency_code"
:
"string"
}
}
}
,
"billing_info"
:
{
"cycle_executions"
:
[
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
99
,
"cycles_completed"
:
9999
,
"cycles_remaining"
:
9999
,
"current_pricing_scheme_version"
:
1
,
"total_cycles"
:
999
}
]
,
"failed_payments_count"
:
999
,
"outstanding_balance"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"last_payment"
:
{
"status"
:
"COMPLETED"
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
"time"
:
"string"
}
,
"next_billing_time"
:
"string"
,
"final_payment_time"
:
"string"
,
"last_failed_payment"
:
{
"reason_code"
:
"PAYMENT_DENIED"
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
"time"
:
"string"
,
"next_payment_retry_time"
:
"string"
}
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
"plan"
:
{
"product_id"
:
"stringstringstringstri"
,
"name"
:
"string"
,
"description"
:
"string"
,
"billing_cycles"
:
[
{
"tenure_type"
:
"REGULAR"
,
"sequence"
:
1
,
"total_cycles"
:
1
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
null
]
,
"fixed_price"
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
"create_time"
:
"string"
,
"update_time"
:
"string"
}
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
}
]
,
"quantity_supported"
:
false
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
0
,
"setup_fee"
:
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
"merchant_preferences"
:
{
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
}
,
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
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
subscription_request
The create subscription request details.
plan_id
required
string
= 26 characters
^P-[A-Z0-9]*$
The ID of the plan.
quantity
string
[ 1 .. 32 ] characters
^([0-9]+|([0-9]+)?[.][0-9]+)$
The quantity of the product in the subscription.
auto_renewal
boolean
Default:
false
DEPRECATED. Indicates whether the subscription auto-renews after the billing cycles complete.
custom_id
string
[ 1 .. 127 ] characters
^[\x20-\x7E]+
The custom id for the subscription. Can be invoice id.
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
Default:
"Current time"
The date and time when the subscription started, in
Internet date and time format
.
shipping_amount
object
(
Money
)
The shipping charges.
subscriber
object
<
payer_v1
>
(
subscriber_request
)
The subscriber request information .
application_context
object
(
application_context
)
DEPRECATED. The application context, which customizes the payer experience during the subscription approval process with PayPal.
plan
object
(
plan_override
)
An inline plan object to customise the subscription. You can override plan level default attributes by providing customised values for the subscription in this object.
Copy
Expand all
Collapse all
{
"plan_id"
:
"stringstringstringstringst"
,
"quantity"
:
"string"
,
"auto_renewal"
:
false
,
"custom_id"
:
"string"
,
"start_time"
:
"string"
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
"subscriber"
:
{
"email_address"
:
"string"
,
"payer_id"
:
"string"
,
"name"
:
{
"given_name"
:
"string"
,
"surname"
:
"string"
}
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
"string"
}
}
,
"shipping_address"
:
{
"type"
:
"SHIPPING"
,
"options"
:
[
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
]
,
"name"
:
{
"full_name"
:
"string"
}
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
}
}
,
"payment_source"
:
{
"card"
:
{
"name"
:
"string"
,
"number"
:
"stringstrings"
,
"security_code"
:
"stri"
,
"expiry"
:
"string"
,
"type"
:
"CREDIT"
,
"brand"
:
"VISA"
,
"billing_address"
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
}
,
"attributes"
:
{
"customer"
:
{
"id"
:
"string"
,
"email_address"
:
"string"
,
"phone"
:
{
"phone_type"
:
"FAX"
,
"phone_number"
:
{
"national_number"
:
null
}
}
,
"merchant_customer_id"
:
"string"
}
,
"vault"
:
{
"store_in_vault"
:
"ON_SUCCESS"
}
,
"verification"
:
{
"method"
:
"SCA_ALWAYS"
}
}
}
}
}
,
"application_context"
:
{
"brand_name"
:
"string"
,
"shipping_preference"
:
"GET_FROM_FILE"
,
"user_action"
:
"CONTINUE"
,
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
,
"locale"
:
"string"
,
"payment_method"
:
{
"payee_preferred"
:
"UNRESTRICTED"
}
}
,
"plan"
:
{
"billing_cycles"
:
[
{
"sequence"
:
1
,
"total_cycles"
:
999
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
}
]
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
999
,
"setup_fee"
:
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
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
}
}
subscription_revise_request
The request to update the quantity of the product or service in a subscription. You can also use this method to switch the plan and update the
shipping_amount
and
shipping_address
values for the subscription. This type of update requires the buyer's consent.
plan_id
string
= 26 characters
^P-[A-Z0-9]*$
The unique PayPal-generated ID for the plan.
quantity
string
[ 1 .. 32 ] characters
^([0-9]+|([0-9]+)?[.][0-9]+)$
The quantity of the product or service in the subscription.
shipping_amount
object
(
Money
)
The shipping charges.
shipping_address
object
(
shipping_detail
)
The shipping address of the subscriber.
application_context
object
(
application_context
)
The application context, which customizes the payer experience during the subscription approval process with PayPal.
plan
object
(
plan_override
)
An inline plan object to customise the subscription. You can override plan level default attributes by providing customised values for the subscription in this object. Any existing overrides will not be carried forward during subscription revise.
Copy
Expand all
Collapse all
{
"plan_id"
:
"stringstringstringstringst"
,
"quantity"
:
"string"
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
"shipping_address"
:
{
"type"
:
"SHIPPING"
,
"options"
:
[
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
]
,
"name"
:
{
"full_name"
:
"string"
}
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
}
}
,
"application_context"
:
{
"brand_name"
:
"string"
,
"shipping_preference"
:
"GET_FROM_FILE"
,
"return_url"
:
"
http://example.com
"
,
"cancel_url"
:
"
http://example.com
"
,
"locale"
:
"string"
,
"payment_method"
:
{
"payee_preferred"
:
"UNRESTRICTED"
}
}
,
"plan"
:
{
"billing_cycles"
:
[
{
"sequence"
:
1
,
"total_cycles"
:
999
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
}
]
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
999
,
"setup_fee"
:
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
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
}
}
subscription_revise_request
The request to update the quantity of the product or service in a subscription. You can also use this method to switch the plan and update the
shipping_amount
and
shipping_address
values for the subscription. This type of update requires the buyer's consent.
plan_id
string
= 26 characters
^P-[A-Z0-9]*$
The unique PayPal-generated ID for the plan.
quantity
string
[ 1 .. 32 ] characters
^([0-9]+|([0-9]+)?[.][0-9]+)$
The quantity of the product or service in the subscription.
shipping_amount
object
(
Money
)
The shipping charges.
shipping_address
object
(
shipping_detail
)
The shipping address of the subscriber.
plan
object
(
plan_override
)
An inline plan object to customise the subscription. You can override plan level default attributes by providing customised values for the subscription in this object. Any existing overrides will not be carried forward during subscription revise.
Copy
Expand all
Collapse all
{
"plan_id"
:
"stringstringstringstringst"
,
"quantity"
:
"string"
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
"shipping_address"
:
{
"type"
:
"SHIPPING"
,
"options"
:
[
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
]
,
"name"
:
{
"full_name"
:
"string"
}
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
}
}
,
"plan"
:
{
"billing_cycles"
:
[
{
"sequence"
:
1
,
"total_cycles"
:
999
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
}
]
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
999
,
"setup_fee"
:
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
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
}
}
subscription_revise_response
The response to a request to update the quantity of the product or service in a subscription. You can also use this method to switch the plan and update the
shipping_amount
and
shipping_address
values for the subscription. This type of update requires the buyer's consent.
plan_id
string
= 26 characters
^P-[A-Z0-9]*$
The unique PayPal-generated ID for the plan.
quantity
string
[ 1 .. 32 ] characters
^([0-9]+|([0-9]+)?[.][0-9]+)$
The quantity of the product or service in the subscription.
shipping_amount
object
(
Money
)
The shipping charges.
shipping_address
object
(
shipping_detail
)
The shipping address of the subscriber.
plan
object
(
plan_override
)
An inline plan object to customise the subscription. You can override plan level default attributes by providing customised values for the subscription in this object. Any existing overrides will not be carried forward during subscription revise.
plan_overridden
boolean
Indicates whether the subscription has overridden any plan attributes.
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
"plan_id"
:
"stringstringstringstringst"
,
"quantity"
:
"string"
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
"shipping_address"
:
{
"type"
:
"SHIPPING"
,
"options"
:
[
{
"id"
:
"string"
,
"label"
:
"string"
,
"selected"
:
true
,
"type"
:
"SHIPPING"
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
]
,
"name"
:
{
"full_name"
:
"string"
}
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
}
}
,
"plan"
:
{
"billing_cycles"
:
[
{
"sequence"
:
1
,
"total_cycles"
:
999
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
}
]
,
"payment_preferences"
:
{
"auto_bill_outstanding"
:
true
,
"setup_fee_failure_action"
:
"CONTINUE"
,
"payment_failure_threshold"
:
999
,
"setup_fee"
:
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
"taxes"
:
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
}
,
"plan_overridden"
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
}
subscription_status
The subscription status details.
status
string
[ 1 .. 24 ] characters
^[A-Z_]+$
The status of the subscription.
Enum Value
Description
APPROVAL_PENDING
The subscription is created but not yet approved by the buyer.
APPROVED
The buyer has approved the subscription.
ACTIVE
The subscription is active.
SUSPENDED
The subscription is suspended.
CANCELLED
The subscription is cancelled.
EXPIRED
The subscription is expired.
status_change_note
string
[ 1 .. 128 ] characters
^.*$
The reason or notes for the status of the subscription.
status_update_time
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
"status"
:
"APPROVAL_PENDING"
,
"status_change_note"
:
"string"
,
"status_update_time"
:
"string"
}
subscription_suspend_request
The suspend subscription request details.
reason
required
string
[ 1 .. 128 ] characters
^.*$
The reason for suspension of the Subscription.
Copy
{
"reason"
:
"string"
}
tax_info
The tax ID of the customer. The customer is also known as the payer. Both
tax_id
and
tax_id_type
are required.
tax_id
required
string
[ 1 .. 14 ] characters
([a-zA-Z0-9])
The customer's tax ID value.
tax_id_type
required
string
[ 1 .. 14 ] characters
^[A-Z0-9_]+$
The customer's tax ID type.
Enum Value
Description
BR_CPF
The individual tax ID type, typically is 11 characters long.
BR_CNPJ
The business tax ID type, typically is 14 characters long.
Copy
{
"tax_id"
:
"string"
,
"tax_id_type"
:
"BR_CPF"
}
taxes
The tax details.
inclusive
boolean
Default:
true
Indicates whether the tax was already included in the billing amount.
percentage
required
string
<
ppaas_common_percentage_v2
>
(
percentage
)
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The tax percentage on the billing amount.
Copy
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
taxes_override
The tax details.
inclusive
boolean
Indicates whether the tax was already included in the billing amount.
percentage
string
<
ppaas_common_percentage_v2
>
(
percentage
)
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The tax percentage on the billing amount.
Copy
{
"inclusive"
:
true
,
"percentage"
:
"string"
}
The reason code that is associated with current instrument state
The reason code that is associated with current instrument state. Use this code to get more information about the financial instrument (FI) state.
string
(
The reason code that is associated with current instrument state
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The reason code that is associated with current instrument state. Use this code to get more information about the financial instrument (FI) state.
Enum Value
Description
INACTIVE_DUE_TO_EXPIRY
Reason is inactive due to expiry.
INACTIVE_DUE_TO_HARD_BUSINESS_FAILURE
Reason is inactive due to hard business failure.
INACTIVE_DUE_TO_SOFT_BUSINESS_FAILURE
Reason is inactive due to soft business failure.
NEARING_EXPIRY
Reason is nearing  of the instrument expiry.
NOT_APPLICABLE
Reason is not applicable.
ON_HOLD_DUE_TO_PENDING_AUTHORIZATION
Reason is on hold due to pending authorization.
ON_HOLD_DUE_TO_PENDING_CONFIRMATION
Reason is on hold due to pending confirmation.
INACTIVE_DUE_TO_PENDING_ORIGINAL_USER_CHECK
Reason is inactive due to pending original user check.
INACTIVE_DUE_TO_UNENROLL
Reason is inactive due to enroll status reason.
Copy
"INACTIVE_DUE_TO_EXPIRY"
three_d_secure_authentication_response
Results of 3D Secure Authentication.
authentication_status
string
(
pares_status
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The outcome of the issuer's authentication.
Enum Value
Description
Y
Successful authentication.
N
Failed authentication / account not verified / transaction denied.
U
Unable to complete authentication.
A
Successful attempts transaction.
C
Challenge required for authentication.
R
Authentication rejected (merchant must not submit for authorization).
D
Challenge required; decoupled authentication confirmed.
I
Informational only; 3DS requestor challenge preference acknowledged.
enrollment_status
string
(
enrolled
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Status of authentication eligibility.
Enum Value
Description
Y
Yes. The bank is participating in 3-D Secure protocol and will return the ACSUrl.
N
No. The bank is not participating in 3-D Secure protocol.
U
Unavailable. The DS or ACS is not available for authentication at the time of the request.
B
Bypass. The merchant authentication rule is triggered to bypass authentication.
Copy
{
"authentication_status"
:
"Y"
,
"enrollment_status"
:
"Y"
}
ThreeDS Contingency Reason Type
Identifies the reason of 3DS contingency.
string
(
ThreeDS Contingency Reason Type
)
[ 1 .. 25 ] characters
^[0-9A-Z_]+$
Identifies the reason of 3DS contingency.
Enum Value
Description
MANDATED
A mandate or regulation requires 3DS.
NON_MANDATED
A reason other than a mandate or merchant request.
MERCHANT_REQUESTED
A merchant requested 3DS explicitly.
SOFT_DECLINE
Soft decline by processor indicating 3DS required.
DATA_ONLY_3DS
A merchant shares only the transaction data with the Issuer through the 3DS rail, without presenting a challenge to the cardholder.
Copy
"MANDATED"
ThreeDS Contingency Source Type
Identifies the source of 3DS contingency.
string
(
ThreeDS Contingency Source Type
)
[ 1 .. 20 ] characters
^[0-9A-Z_]+$
Identifies the source of 3DS contingency.
Enum Value
Description
CARD
Due to the state of the card in the wallet. i.e. the card needs 3DS confirmation.
TRANSACTION
Due to the transaction context, not due to the card state.
RISK
Due to Risk decisioning, not due to card state or transaction context.
AUTHORIZATION
Identified as 3DS required during authorization.
Copy
"CARD"
Time Duration
The
ISO-8601-formatted
length of time in years, months, weeks, days, hours, minutes, and seconds.
Note:
The format is
P
y
Y
m
M
d
DT
h
H
m
M
s
S
. When an amount is zero, you can omit it. Because week cannot co-exist with other time components in ISO-8601 duration, specify
P7D
. Make provisions to incorporate the effects of daylight savings time.
For more information, see
durations
.
string
<
ppaas_common_time_duration_v2
>
(
Time Duration
)
^P([0-9]+Y)?([0-9]+M)?([0-9]+W)?([0-9]+D)?(T(...
Show pattern
The
ISO-8601-formatted
length of time in years, months, weeks, days, hours, minutes, and seconds.
Note:
The format is
P
y
Y
m
M
d
DT
h
H
m
M
s
S
. When an amount is zero, you can omit it. Because week cannot co-exist with other time components in ISO-8601 duration, specify
P7D
. Make provisions to incorporate the effects of daylight savings time.
For more information, see
durations
.
Copy
"string"
transaction
The transaction details.
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
id
required
string
[ 3 .. 50 ] characters
The PayPal-generated transaction ID.
amount_with_breakdown
required
object
(
amount_with_breakdown
)
The breakdown details for the amount. Includes the gross, tax, fee, and shipping amounts.
payer_name
object
(
Name
)
The name of the customer.
payer_email
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
The email ID of the customer.
time
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
The date and time when the transaction was processed, in
Internet date and time format
.
Copy
Expand all
Collapse all
{
"status"
:
"COMPLETED"
,
"id"
:
"string"
,
"amount_with_breakdown"
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
"full_name"
:
"string"
}
,
"payer_email"
:
"string"
,
"time"
:
"string"
}
transactions_list
The list transactions for a subscription request details.
transactions
Array of
objects
(
transaction
)
[ 0 .. 32767 ] items
An array of transactions.
total_items
integer
[ 0 .. 500000000 ]
The total number of items.
total_pages
integer
[ 0 .. 100000000 ]
The total number of pages.
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
"transactions"
:
[
{
"status"
:
"COMPLETED"
,
"id"
:
"string"
,
"amount_with_breakdown"
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
"full_name"
:
"string"
}
,
"payer_email"
:
"string"
,
"time"
:
"string"
}
]
,
"total_items"
:
500000000
,
"total_pages"
:
100000000
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
update_pricing_scheme_request
The update pricing scheme request details.
billing_cycle_sequence
required
integer
[ 1 .. 99 ]
The billing cycle sequence.
pricing_scheme
required
object
(
pricing_scheme
)
The pricing scheme details.
Copy
Expand all
Collapse all
{
"billing_cycle_sequence"
:
1
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
}
update_pricing_schemes_list_request
The update pricing scheme request details.
pricing_schemes
required
Array of
objects
(
update_pricing_scheme_request
)
[ 1 .. 99 ] items
An array of pricing schemes.
Copy
Expand all
Collapse all
{
"pricing_schemes"
:
[
{
"billing_cycle_sequence"
:
1
,
"pricing_scheme"
:
{
"version"
:
999
,
"pricing_model"
:
"VOLUME"
,
"tiers"
:
[
{
"starting_quantity"
:
"string"
,
"ending_quantity"
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
]
,
"fixed_price"
:
{
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
"string"
,
"update_time"
:
"string"
}
}
]
}
url
Describes the URL.
string
<
uri
>
(
url
)
Describes the URL.
Copy
"
http://example.com
"
URL type
Type associated with an institution URL.
string
(
URL type
)
[ 1 .. 100 ] characters
^[0-9A-Z_]+$
Type associated with an institution URL.
Enum Value
Description
SETTINGS
Settings URL Type.
TERMS_AND_CONDITIONS
Terms & Conditions URL Type.
Copy
"SETTINGS"
vault_id
The identifier for the vaulted instrument.
string
(
vault_id
)
[ 26 .. 41 ] characters
^[0-9A-Za-z-]+$
The identifier for the vaulted instrument.
Copy
"stringstringstringstringst"
vault_instruction_base
Basic vault instruction specification that can be extended by specific payment sources that supports vaulting.
store_in_vault
string
(
store_in_vault_instruction
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Defines how and when the payment source gets vaulted.
Value
Description
ON_SUCCESS
Defines that the payment_source will be vaulted only when at least one authorization or capture using that payment_source is successful.
Copy
{
"store_in_vault"
:
"ON_SUCCESS"
}
vault_response
The details about a saved payment source.
id
string
[ 1 .. 255 ] characters
The PayPal-generated ID for the saved payment source.
status
string
(
Vault Status
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The vault status.
Enum Value
Description
VAULTED
The payment source has been saved in your customer's vault. This vault status reflects
/v3/vault
status.
CREATED
DEPRECATED. The payment source has been saved in your customer's vault. This status applies to deprecated integration patterns and will not be returned for v3/vault integrations.
APPROVED
Customer has approved the action of saving the specified payment_source into their vault. Use v3/vault/payment-tokens with given setup_token to save the payment source in the vault
links
Array of
objects
(
Link Description
)
[ 1 .. 10 ] items
An array of request-related HATEOAS links.
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
"VAULTED"
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
vault_response
The details about a saved payment source.
id
string
[ 1 .. 255 ] characters
The PayPal-generated ID for the saved payment source.
status
string
(
Vault Status
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The vault status.
Enum Value
Description
VAULTED
The payment source has been saved in your customer's vault. This vault status reflects
/v3/vault
status.
CREATED
DEPRECATED. The payment source has been saved in your customer's vault. This status applies to deprecated integration patterns and will not be returned for v3/vault integrations.
APPROVED
Customer has approved the action of saving the specified payment_source into their vault. Use v3/vault/payment-tokens with given setup_token to save the payment source in the vault
Copy
{
"id"
:
"string"
,
"status"
:
"VAULTED"
}
