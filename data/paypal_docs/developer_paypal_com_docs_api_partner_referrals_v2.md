# Partner Referrals

Source: https://developer.paypal.com/docs/api/partner-referrals/v2/

Partner Referrals
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
Partner Referrals
post
Create partner referral
get
Show referral data
Definitions
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
Partner Referrals
(
2
)
API Version v2
?
This API is currently not supported by our SDK
Use the Partner Referrals API to add PayPal seller accounts to PayPal Complete Payments Platform for Marketplaces and Platforms.
Important:
This endpoint is available to approved partners only.
Fill out this form
to get approved and a PayPal representative will reach out to you shortly.
For more information about partner integrations and onboarding sellers, see
PayPal Complete Payments Platform for Marketplaces and Platforms.
Create partner referral
post
/v2/customer/partner-referrals
Try it
Creates a partner referral that is shared by the partner or API caller. The partner referral is used to onboard the seller, and contains the seller's personal, business, financial and operations.
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
individual_owners
Array of
objects
(
Individual_owner
)
[ 0 .. 2 ] items
List of owners in the account. There should be only one primary account owner which is mentioned in their role_type.
business_entity
object
(
Business_entity
)
Business entity of the account.
tracking_id
string
[ 1 .. 127 ] characters
The partner's unique identifier for this customer in their system which can be used to track user in PayPal.
operations
required
Array of
objects
(
operation
)
[ 1 .. 5 ] items
An array of operations to perform for the customer while they share their data.
products
Array of
strings
(
product_name
)
[ 1 .. 5 ] items
An array of PayPal products to which the partner wants to onboard the customer.
Items
Enum Value
Description
ALIPAY
Alipay is a China-based payment method that allows customers to complete transactions online using their Alipay wallet. Include only if Alipay alone is required. You can use PPCP if all features are required.
BANCONTACT
Bancontact is a Belgium-based payment method that allows customers to complete transactions online using their bank credentials. Include only if Bancontact alone is required. You can use PPCP if all features are required.
BLIK
Blik is a Poland-based payment method that allows customers to complete transactions online using their bank credentials. Include only if Blik alone is required. You can use PPCP if all features are required.
EPS
EPS is an Austria-based payment method that allows customers to complete transactions online using their bank credentials. Include only if EPS alone is required. You can use PPCP if all features are required.
PPCP
PayPal Complete Payments product, which includes Express Checkout, advanced credit and debit card payments, Apple Pay, and Google Pay. Use PPCP if all features are required.
EXPRESS_CHECKOUT
Express checkout product.
PAYMENT_METHODS
PayPal Alternative Payment Methods product. Include only if Apple Pay or Google Pay or both are required alone. You can use PPCP if all features are required.
ADVANCED_VAULTING
PayPal Advanced Vaulting product. Must be requested along with either EXPRESS_CHECKOUT or PPCP. Include only if ADVANCED_VAULTING alone is required. You can use PPCP if all features are required.
IDEAL
iDEAL is a Netherlands-based payment method that allows customers to complete transactions online using their bank credentials. Include only if iDEAL alone is required. You can use PPCP if all features are required.
MB_WAY
MB Way is a Portugal-based payment method that allows customers to complete transactions online using their MB Way wallet. Include only if MB Way alone is required. You can use PPCP if all features are required.
MULTIBANCO
Multibanco is a Portugal-based payment method that allows customers to complete transactions online using their bank credentials or pay in cash at a bank branch. Include only if Multibanco alone is required. You can use PPCP if all features are required.
PPPLUS
PayPal PLUS product.
PRZELEWY24
Przelewy24 is a Poland-based payment method that allows customers to complete transactions online. Include only if Przelewy24 alone is required. You can use PPCP if all features are required.
SATISPAY
Satispay is an Italy-based payment method that allows customers to complete transactions online using their bank credentials. Include only if Satispay alone is required. You can use PPCP if all features are required.
TRUSTLY
Trustly is a payment method that allows customers from (Austria (AT), Germany (DE), Denmark (DK), Estonia (EE), Spain (ES), Finland (FI), Great Britain (GB), Lithuania (LT), Latvia (LV), Netherlands (NL), Norway (NO), Sweden (SE)) to complete transactions online using their bank credentials. Include only if Trustly alone is required. You can use PPCP if all features are required.
WECHAT_PAY
WeChat Pay is a China-based payment method that allows customers to complete transactions online using their WeChat Pay wallet. Include only if WeChat Pay alone is required. You can use PPCP if all features are required.
WEBSITE_PAYMENT_PRO
PayPal Professional product.
ZETTLE
PayPal Zettle in-person payments product.
HYPERWALLET_PAYOUTS
Hyperwallet payouts product
CRYPTO_PYMTS
Crypto payments product
capabilities
Array of
strings
(
capability_name
)
[ 1 .. 5 ] items
An array of capabilities which the partner wants to enable for the selected products. Supported only when products are specified.
Items
Enum Value
Description
PAYPAL_WALLET_VAULTING_ADVANCED
Enables capability to save payment methods. Supported only when ADVANCED_VAULTING is requested and EXPRESS_CHECKOUT or PPCP is also requested.
PAY_UPON_INVOICE
Enables Pay Upon Invoice (PUI) which is a deferred payment method that allows a buyer to buy now and pay later. Supported only when PAYMENT_METHODS is requested.
APPLE_PAY
Enables Apple Pay capability. Supported only when PAYMENT_METHODS is requested.
GOOGLE_PAY
Enables Google Pay capability. Supported only when PAYMENT_METHODS is requested.
outside_process_dependencies
Array of
any
[ 1 .. 5 ] items
An array of dependent processes.
legal_consents
required
Array of
objects
(
legal_consent
)
[ 1 .. 5 ] items
An array of all consents that the partner has received from this seller. If
SHARE_DATA_CONSENT
is not granted, PayPal does not store customer data.
email
string
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 3 .. 254 ] characters
^.+@[^"\-].+$
Email address of the customer used to create the account.
preferred_language_code
string
<
ppaas_common_language_v3
>
(
language
)
[ 2 .. 10 ] characters
^[a-z]{2}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}))...
Show pattern
The preferred
locale code
to use in the onboarding flow for the customer.
partner_config_override
object
(
partner_configuration_override
)
The configuration property that the partner intends to override for this onboarding request.
financial_instruments
object
(
Financial instrument.
)
Array of financial instruments attached to the customer's account.
payout_attributes
object
(
Payout Attributes
)
Payout specific attributes.
legal_country_code
string
<
ppaas_common_country_code_v2
>
(
country_code
)
= 2 characters
^([A-Z]{2}|C2)$
Legal Country Code.
Responses
201
A successful request returns the HTTP
201 Created
status code and a JSON response body that contains a
HATEOAS link
to show the referral data and an
action_url
to which you redirect the customer in a browser to complete the signup process. The
partner_referral_id
token is appended to the URL.
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
Sample 1 - 201 - Create Partner Referrals - Basic Merchant Referral
Sample 1 - 201 - Create Partner Referrals - Basic Merchant Referral
Copy
Expand all
Collapse all
{
"individual_owners"
:
[
{
"names"
:
[
{
"prefix"
:
"Mr."
,
"given_name"
:
"John"
,
"surname"
:
"Doe"
,
"middle_name"
:
"Middle"
,
"suffix"
:
"Jr."
,
"full_name"
:
"John Middle Doe Jr."
,
"type"
:
"LEGAL"
}
]
,
"citizenship"
:
"US"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"HOME"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692468839"
,
"extension_number"
:
"1234"
,
"type"
:
"MOBILE"
}
]
,
"birth_details"
:
{
"date_of_birth"
:
"1955-12-29"
}
,
"type"
:
"PRIMARY"
}
]
,
"business_entity"
:
{
"business_type"
:
{
"type"
:
"INDIVIDUAL"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"1004"
,
"mcc_code"
:
"8931"
,
"subcategory"
:
"2025"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"US"
,
"incorporation_date"
:
"1986-12-29"
}
,
"names"
:
[
{
"business_name"
:
"Test Enterprise"
,
"type"
:
"LEGAL_NAME"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"
[email protected]
"
}
]
,
"website"
:
"
https://mystore.testenterprises.com
"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"WORK"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692478833"
,
"extension_number"
:
"1234"
,
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"beneficial_owners"
:
{
"individual_beneficial_owners"
:
[
{
"names"
:
[
{
"prefix"
:
"Mr."
,
"given_name"
:
"John"
,
"surname"
:
"Doe"
,
"middle_name"
:
"Middle"
,
"suffix"
:
"Jr."
,
"full_name"
:
"John Middle Doe Jr."
,
"type"
:
"LEGAL"
}
]
,
"citizenship"
:
"US"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"HOME"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692468839"
,
"extension_number"
:
"1234"
,
"type"
:
"MOBILE"
}
]
,
"birth_details"
:
{
"date_of_birth"
:
"1955-12-29"
}
,
"percentage_of_ownership"
:
"50"
}
]
,
"business_beneficial_owners"
:
[
{
"business_type"
:
{
"type"
:
"INDIVIDUAL"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"1004"
,
"mcc_code"
:
"8931"
,
"subcategory"
:
"2025"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"US"
,
"incorporation_date"
:
"1986-12-29"
}
,
"names"
:
[
{
"business_name"
:
"Test Enterprise"
,
"type"
:
"LEGAL_NAME"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"
[email protected]
"
}
]
,
"website"
:
"
https://mystore.testenterprises.com
"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"WORK"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692478833"
,
"extension_number"
:
"1234"
,
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"percentage_of_ownership"
:
"50"
}
]
}
,
"office_bearers"
:
[
{
"names"
:
[
{
"prefix"
:
"Mr."
,
"given_name"
:
"John"
,
"surname"
:
"Doe"
,
"middle_name"
:
"Middle"
,
"suffix"
:
"Jr."
,
"full_name"
:
"John Middle Doe Jr."
,
"type"
:
"LEGAL"
}
]
,
"citizenship"
:
"US"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"HOME"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692468839"
,
"extension_number"
:
"1234"
,
"type"
:
"MOBILE"
}
]
,
"birth_details"
:
{
"date_of_birth"
:
"1955-12-29"
}
,
"role"
:
"DIRECTOR"
}
]
,
"annual_sales_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10000"
}
,
"maximum_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50000"
}
}
,
"average_monthly_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"1000"
}
,
"maximum_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50000"
}
}
,
"purpose_code"
:
"P0104"
}
,
"email"
:
"
[email protected]
"
,
"preferred_language_code"
:
"en-US"
,
"tracking_id"
:
"testenterprices123122"
,
"partner_config_override"
:
{
"return_url"
:
"
https://testenterprises.com/merchantonboarded
"
,
"return_url_description"
:
"the url to return the merchant after the paypal onboarding process."
,
"show_add_credit_card"
:
true
}
,
"operations"
:
[
{
"operation"
:
"API_INTEGRATION"
,
"api_integration_preference"
:
{
"rest_api_integration"
:
{
"integration_type"
:
"THIRD_PARTY"
,
"integration_method"
:
"PAYPAL"
,
"third_party_details"
:
{
"features"
:
[
"REFUND"
,
"PARTNER_FEE"
]
}
}
}
}
]
,
"products"
:
[
"EXPRESS_CHECKOUT"
]
,
"legal_consents"
:
[
{
"type"
:
"SHARE_DATA_CONSENT"
,
"granted"
:
true
}
]
,
"payout_attributes"
:
{
"marketplace"
:
true
,
"kyc_required"
:
true
,
"country_transfer_method_currency_selection"
:
[
{
"country"
:
"US"
,
"transfer_methods"
:
[
{
"transfer_method_type"
:
"BANK_ACCOUNT"
,
"currencies"
:
[
"USD"
,
"CAD"
]
}
,
{
"transfer_method_type"
:
"PAYPAL"
}
]
}
,
{
"country"
:
"CA"
,
"transfer_methods"
:
[
{
"transfer_method_type"
:
"WIRE"
,
"currencies"
:
[
"USD"
,
"CAD"
]
}
,
{
"transfer_method_type"
:
"VENMO"
}
]
}
]
}
}
Response samples
201
application/json
Sample 1 - 201 - Create Partner Referrals - Basic Merchant Referral
Sample 1 - 201 - Create Partner Referrals - Basic Merchant Referral
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
https://uri.paypal.com/v2/customer/partner-referrals/ZjcyODU4ZWYtYTA1OC00ODIwLTk2M2EtOTZkZWQ4NmQwYzI3RU12cE5xa0xMRmk1NWxFSVJIT1JlTFdSbElCbFU1Q3lhdGhESzVQcU9iRT0=
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
https://www.paypal.com/merchantsignup/partner/onboardingentry?token=ZjcyODU4ZWYtYTA1OC00ODIwLTk2M2EtOTZkZWQ4NmQwYzI3RU12cE5xa0xMRmk1NWxFSVJIT1JlTFdSbElCbFU1Q3lhdGhESzVQcU9iRT0=
"
,
"rel"
:
"action_url"
,
"method"
:
"GET"
}
]
}
Show referral data
get
/v2/customer/partner-referrals/{partner_referral_id}
Try it
Shows details by ID for referral data that was shared by the partner or API caller.
Security
Oauth2
Request
path
Parameters
partner_referral_id
required
string
The ID of the partner-referrals data for which to show details.
Responses
200
A successful request returns the HTTP
200 OK
status code and a JSON response body that shows referral data.
Request samples
cURL
Node.js
Java
Python
Copy
curl
-v
-X
GET https://api-m.sandbox.paypal.com/v2/customer/partner-referrals/ZjcyODU4ZWYtYTA1OC00ODIwLTk2M2EtOTZkZWQ4NmQwYzI3RU12cE5xa0xMRmk1NWxFSVJIT1JlTFdSbElCbFU1Q3lhdGhESzVQcU9iRT0
=
\
-H
'Content-Type: application/json'
\
-H
'Authorization: Bearer access_token6V7rbVwmlM1gFZKW_8QtzWXqpcwQ6T5vhEGYNJDAAdn3paCgRpdeMdVYmWzgbKSsECednupJ3Zx5Xd-g'
Response samples
200
application/json
Sample 1 - 200 - Get partner-referrals using partner referral id for internal partners.
Sample 1 - 200 - Get partner-referrals using partner referral id for internal partners.
Copy
Expand all
Collapse all
{
"partner_referral_id"
:
"ZjcyODU4ZWYtYTA1OC00ODIwLTk2M2EtOTZkZWQ4NmQwYzI3RU12cE5xa0xMRmk1NWxFSVJIT1JlTFdSbElCbFU1Q3lhdGhESzVQcU9iRT0="
,
"submitter_payer_id"
:
"RFYUH2QQDGUQU"
,
"submitter_client_id"
:
"B_Az35Q-rHwtlyRATHjMWqlD_S4fCoKbEJ5Ig_kMcf1AMX9NFanKaUqL3M_brrtn-wqxxg7WP2aHJ71Cqg"
,
"referral_data"
:
{
"individual_owners"
:
[
{
"names"
:
[
{
"prefix"
:
"Mr."
,
"given_name"
:
"John"
,
"surname"
:
"Doe"
,
"middle_name"
:
"Middle"
,
"suffix"
:
"Jr."
,
"full_name"
:
"John Middle Doe Jr."
,
"type"
:
"LEGAL"
}
]
,
"citizenship"
:
"US"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"HOME"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692468839"
,
"extension_number"
:
"1234"
,
"type"
:
"MOBILE"
}
]
,
"birth_details"
:
{
"date_of_birth"
:
"1955-12-29"
}
,
"type"
:
"PRIMARY"
}
]
,
"business_entity"
:
{
"business_type"
:
{
"type"
:
"INDIVIDUAL"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"1004"
,
"mcc_code"
:
"8931"
,
"subcategory"
:
"2025"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"US"
,
"incorporation_date"
:
"1986-12-29"
}
,
"names"
:
[
{
"business_name"
:
"Test Enterprise"
,
"type"
:
"LEGAL_NAME"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"
[email protected]
"
}
]
,
"website"
:
"
https://mystore.testenterprises.com
"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"WORK"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692478833"
,
"extension_number"
:
"1234"
,
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"beneficial_owners"
:
{
"individual_beneficial_owners"
:
[
{
"names"
:
[
{
"prefix"
:
"Mr."
,
"given_name"
:
"John"
,
"surname"
:
"Doe"
,
"middle_name"
:
"Middle"
,
"suffix"
:
"Jr."
,
"full_name"
:
"John Middle Doe Jr."
,
"type"
:
"LEGAL"
}
]
,
"citizenship"
:
"US"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"HOME"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692468839"
,
"extension_number"
:
"1234"
,
"type"
:
"MOBILE"
}
]
,
"birth_details"
:
{
"date_of_birth"
:
"1955-12-29"
}
,
"percentage_of_ownership"
:
"50"
}
]
,
"business_beneficial_owners"
:
[
{
"business_type"
:
{
"type"
:
"INDIVIDUAL"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"1004"
,
"mcc_code"
:
"8931"
,
"subcategory"
:
"2025"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"US"
,
"incorporation_date"
:
"1986-12-29"
}
,
"names"
:
[
{
"business_name"
:
"Test Enterprise"
,
"type"
:
"LEGAL_NAME"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"
[email protected]
"
}
]
,
"website"
:
"
https://mystore.testenterprises.com
"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"WORK"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692478833"
,
"extension_number"
:
"1234"
,
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"percentage_of_ownership"
:
"50"
}
]
}
,
"office_bearers"
:
[
{
"names"
:
[
{
"prefix"
:
"Mr."
,
"given_name"
:
"John"
,
"surname"
:
"Doe"
,
"middle_name"
:
"Middle"
,
"suffix"
:
"Jr."
,
"full_name"
:
"John Middle Doe Jr."
,
"type"
:
"LEGAL"
}
]
,
"citizenship"
:
"US"
,
"addresses"
:
[
{
"address_line_1"
:
"One Washington Square"
,
"address_line_2"
:
"Apt 123"
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
"95112"
,
"country_code"
:
"US"
,
"type"
:
"HOME"
}
]
,
"phones"
:
[
{
"country_code"
:
"1"
,
"national_number"
:
"6692468839"
,
"extension_number"
:
"1234"
,
"type"
:
"MOBILE"
}
]
,
"birth_details"
:
{
"date_of_birth"
:
"1955-12-29"
}
,
"role"
:
"DIRECTOR"
}
]
,
"annual_sales_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"10000"
}
,
"maximum_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50000"
}
}
,
"average_monthly_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"1000"
}
,
"maximum_amount"
:
{
"currency_code"
:
"USD"
,
"value"
:
"50000"
}
}
,
"purpose_code"
:
"P0104"
}
,
"email"
:
"
[email protected]
"
,
"preferred_language_code"
:
"en-US"
,
"tracking_id"
:
"testenterprices123122"
,
"partner_config_override"
:
{
"return_url"
:
"
https://testenterprises.com/merchantonboarded
"
,
"return_url_description"
:
"the url to return the merchant after the paypal onboarding process."
,
"show_add_credit_card"
:
true
}
,
"operations"
:
[
{
"operation"
:
"API_INTEGRATION"
,
"api_integration_preference"
:
{
"classic_api_integration"
:
{
"integration_type"
:
"THIRD_PARTY"
,
"third_party_details"
:
{
"permissions"
:
[
"EXPRESS_CHECKOUT"
,
"REFUND"
,
"DIRECT_PAYMENT"
,
"AUTH_CAPTURE"
,
"BUTTON_MANAGER"
,
"ACCOUNT_BALANCE"
,
"TRANSACTION_DETAILS"
]
}
,
"first_party_details"
:
"CERTIFICATE"
}
,
"rest_api_integration"
:
{
"integration_method"
:
"PAYPAL"
,
"integration_type"
:
"THIRD_PARTY"
,
"third_party_details"
:
{
"features"
:
[
"PAYMENT"
,
"REFUND"
,
"PARTNER_FEE"
]
}
}
}
,
"billing_agreement"
:
{
"description"
:
"Billing Agreement Description Field"
,
"billing_experience_preference"
:
{
"experience_id"
:
"string"
,
"billing_context_set"
:
true
}
,
"merchant_custom_data"
:
"PatnerMERCHANT23124"
,
"approval_url"
:
"wttps://www.paypal.com/agreements/approve?ba_token=BA-67944913LE886121E"
,
"ec_token"
:
"EC-1S970363DB536864M"
}
}
]
,
"products"
:
[
"EXPRESS_CHECKOUT"
]
,
"legal_consents"
:
[
{
"type"
:
"SHARE_DATA_CONSENT"
,
"granted"
:
true
}
]
,
"payout_attributes"
:
{
"marketplace"
:
true
,
"kyc_required"
:
true
,
"country_transfer_method_currency_selection"
:
[
{
"country"
:
"US"
,
"transfer_methods"
:
[
{
"transfer_method_type"
:
"BANK_ACCOUNT"
,
"currencies"
:
[
"USD, CAD"
]
}
,
{
"transfer_method_type"
:
"PAYPAL"
}
]
}
,
{
"country"
:
"CA"
,
"transfer_methods"
:
[
{
"transfer_method_type"
:
"WIRE"
,
"currencies"
:
[
"USD, CAD"
]
}
,
{
"transfer_method_type"
:
"VENMO"
}
]
}
]
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
https://uri.paypal.com/v2/customer/partner-referrals/ZjcyODU4ZWYtYTA1OC00ODIwLTk2M2EtOTZkZWQ4NmQwYzI3RU12cE5xa0xMRmk1NWxFSVJIT1JlTFdSbElCbFU1Q3lhdGhESzVQcU9iRT0=
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
https://www.paypal.com/merchantsignup/partner/onboardingentry?token=ZjcyODU4ZWYtYTA1OC00ODIwLTk2M2EtOTZkZWQ4NmQwYzI3RU12cE5xa0xMRmk1NWxFSVJIT1JlTFdSbElCbFU1Q3lhdGhESzVQcU9iRT0=
"
,
"rel"
:
"action_url"
,
"method"
:
"GET"
}
]
}
Definitions
Account
Common account object to hold the account related details of the customer.
individual_owners
Array of
objects
(
Individual_owner
)
[ 0 .. 2 ] items
List of owners in the account. There should be only one primary account owner which is mentioned in their role_type.
business_entity
object
(
Business_entity
)
Business entity of the account.
Copy
Expand all
Collapse all
{
"individual_owners"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"type"
:
"PRIMARY"
}
]
,
"business_entity"
:
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"office_bearers"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"role"
:
"CEO"
}
]
,
"purpose_code"
:
[
"P0104"
]
,
"business_description"
:
"string"
,
"beneficial_owners"
:
{
"individual_beneficial_owners"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
,
"business_beneficial_owners"
:
[
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
}
,
"annual_sales_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"maximum_amount"
:
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
"average_monthly_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"maximum_amount"
:
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
Bank Account
The bank account information.
nick_name
string
[ 1 .. 50 ] characters
^[0-9A-Za-z_-]+$
The user-provided short name for the user's bank account.
account_number
required
string
[ 1 .. 50 ] characters
\d+
The bank account number.
account_type
required
string
[ 1 .. 50 ] characters
^[0-9A-Z_]+$
The type of bank account.
Enum Value
Description
CHECKING
Checking account.
SAVINGS
Savings account.
identifiers
Array of
objects
(
Bank Account Identifier
)
[ 0 .. 20 ] items
An array of instrument institute attributes. Used with the account number to uniquely identify the instrument. Value is:
For banks with IBAN information, the IBAN number.
For banks with BBAN information, the BBAN number.
For banks with both IBAN and BBAN information, the IBAN number.
currency_code
string
<
ppaas_common_currency_code_v2
>
(
currency_code
)
= 3 characters
The primary currency code of the bank account.
branch_location
object
(
Portable Postal Address (Medium-Grained)
)
The branch location, if applicable.
mandate
object
(
Mandate
)
Mandate for this bank account.
Copy
Expand all
Collapse all
{
"nick_name"
:
"string"
,
"account_number"
:
"string"
,
"account_type"
:
"CHECKING"
,
"identifiers"
:
[
{
"type"
:
"BANK_CODE"
,
"value"
:
"string"
}
]
,
"currency_code"
:
"str"
,
"branch_location"
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
"mandate"
:
{
"accepted"
:
true
}
}
Bank Account Identifier
The bank account ID. An ID with
ROUTING_NUMBER_1
is required.
type
string
[ 1 .. 125 ] characters
^[0-9A-Z_-]+$
The bank account ID type.
Enum Value
Description
BANK_CODE
The bank code.
BI_CODE
The BI code.
BRANCH_CODE
Branch code.
ROUTING_NUMBER_1
The bank routing number.
ROUTING_NUMBER_2
The bank routing number.
ROUTING_NUMBER_3
The bank routing number.
SWIFT_CODE
The bank swift code.
INTERMEDIARY_SWIFT_CODE
Swift code.
BBAN
BBAN.
BBAN_ENCRYPTED
BBAN enrypted.
BBAN_HMAC
BBAN HMAC.
AGGREGATOR_YODLEE
Aggregator Yodlee.
value
string
[ 1 .. 125 ] characters
^[A-Za-z0-9-_.+/ =]+
The value of account identifier.
Copy
{
"type"
:
"BANK_CODE"
,
"value"
:
"string"
}
Beneficial_owners
Beneficial owners of the entity.
individual_beneficial_owners
Array of
objects
(
Individual_beneficial_owner
)
[ 0 .. 5 ] items
Individual beneficial owners.
business_beneficial_owners
Array of
objects
(
Business_beneficial_owner
)
[ 0 .. 5 ] items
Business beneficial owners.
Copy
Expand all
Collapse all
{
"individual_beneficial_owners"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
,
"business_beneficial_owners"
:
[
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
}
billing_agreement
The details of the billing agreement between the partner and a seller.
description
string
[ 1 .. 125 ] characters
^.+$
The billing agreement description.
billing_experience_preference
object
(
billing_experience_preference
)
The preference that customizes the billing experience of the customer.
merchant_custom_data
string
[ 1 .. 125 ] characters
^[a-zA-Z0-9-]+$
The custom data for the billing agreement.
approval_url
string
<
uri
>
[ 1 .. 125 ] characters
The URL to which to redirect seller to accept the billing agreement.
ec_token
string
[ 1 .. 50 ] characters
^[0-9A-Z_-]+$
The billing agreement token for the agreement.
Copy
Expand all
Collapse all
{
"description"
:
"string"
,
"billing_experience_preference"
:
{
"experience_id"
:
"string"
,
"billing_context_set"
:
true
}
,
"merchant_custom_data"
:
"string"
,
"approval_url"
:
"
http://example.com
"
,
"ec_token"
:
"string"
}
billing_experience_preference
The preference that customizes the billing experience of the customer.
experience_id
string
[ 1 .. 20 ] characters
^[a-zA-Z0-9-]+$
The ID of the payment web experience profile.
billing_context_set
boolean
Indicates whether the partner has already displayed the billing context to the seller.
Copy
{
"experience_id"
:
"string"
,
"billing_context_set"
:
true
}
Birth details
Date of birth data provided by the user
date_of_birth
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
date of birth, fomrat
Internet date and time format
.
Copy
{
"date_of_birth"
:
"stringstri"
}
business
names
Array of
objects
(
Business name
)
[ 0 .. 5 ] items
Name of the business.
emails
Array of
objects
(
Email of a person orbusiness
)
[ 0 .. 5 ] items
Email addresses of the business.
website
string
<
uri
>
[ 1 .. 50 ] characters
Website of the business.
addresses
Array of
objects
(
Business_address_detail
)
[ 0 .. 5 ] items
List of addresses associated with the business entity.
phones
Array of
objects
(
Phone details
)
[ 0 .. 5 ] items
List of phone number associated with the business.
documents
Array of
objects
(
Business document
)
[ 0 .. 20 ] items
Business Party related Document data collected from the customer.. For example SSN, ITIN, Business registration number that were collected from the user.
business_type
object
(
Business type information
)
Information related to the business like the nature of business, started date etc.
business_industry
object
(
Business industry
)
Information related to the business like the nature of business, started date etc.
business_incorporation
object
(
Business_incorporation
)
Information related to the business like the nature of business, started date etc.
Copy
Expand all
Collapse all
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
}
Business address type
Address type under which the provided address is tagged
string
(
Business address type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Address type under which the provided address is tagged
Value
Description
WORK
The address of the business.
Copy
"WORK"
Business document
The documents associated with the business.
identification_number
string
[ 1 .. 100 ] characters
^[a-zA-Z0-9-]+$
The number for the document. It is the ID number if the document is
ID CARD
, the passport number if the document is
PASSPORT
, etc.
issuing_country_code
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
type
string
(
Document type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The actual type of the document.
Enum Value
Description
SOCIAL_SECURITY_NUMBER
A social security number.
EMPLOYMENT_IDENTIFICATION_NUMBER
The employee identification number.
TAX_IDENTIFICATION_NUMBER
The tax identification number.
PASSPORT_NUMBER
A passport number.
PENSION_FUND_ID
A pension fund ID.
MEDICAL_INSURANCE_ID
A medical insurance ID.
CNPJ
The identification number issued to Brazilian companies by the Department of Federal Revenue of Brazil.
CPF
A Brazilian individual's taxpayer registry identification number.
PAN
The Permanent account number issued by the Indian Income Tax Department.
BUSINESS_REGISTRATION
A unique identifier for business entities issued by the governing agency.
Copy
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
Business industry
The category, subcategory and MCC code of the business.
category
required
string
[ 1 .. 20 ] characters
^\d+$
The customer's business category code. PayPal uses industry standard seller category codes.
mcc_code
required
string
[ 1 .. 20 ] characters
^\d+$
The customer's business seller category code. PayPal uses industry standard seller category codes.
subcategory
required
string
[ 1 .. 20 ] characters
^\d+$
The customer's business subcategory code. PayPal uses industry standard seller subcategory codes.
Copy
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
Business name
Name of the business provided.
business_name
string
<= 300 characters
Required. The business name of the party.
type
required
string
(
The business name type.
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of business name. For example, trading name.
Enum Value
Description
DOING_BUSINESS_AS
The trading name of the business.
LEGAL_NAME
The legal name of the business.
Copy
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
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
Business type
The business types classified
string
(
Business type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The business types classified
Enum Value
Description
ANY_OTHER_BUSINESS_ENTITY
The any other business entity.
ASSOCIATION
The association.
CORPORATION
The corporation.
GENERAL_PARTNERSHIP
The general partnership.
GOVERNMENT
The government.
INDIVIDUAL
The individual.
LIMITED_LIABILITY_PARTNERSHIP
The limited liability partnership.
LIMITED_LIABILITY_PROPRIETORS
The limited liability proprietors.
LIMITED_LIABILITY_PRIVATE_CORPORATION
The limited liability private corporation.
LIMITED_PARTNERSHIP
The limited partnership.
LIMITED_PARTNERSHIP_PRIVATE_CORPORATION
The limited partnership private corporation.
NONPROFIT
The nonprofit.
ONLY_BUY_OR_SEND_MONEY
The only buy and send money.
OTHER_CORPORATE_BODY
The other corporate body.
PARTNERSHIP
The partnership.
PRIVATE_PARTNERSHIP
The private partnership.
PROPRIETORSHIP
The proprietorship.
PROPRIETORSHIP_CRAFTSMAN
The proprietorship craftsman.
PROPRIETORY_COMPANY
The proprietory company.
PRIVATE_CORPORATION
The private corporation.
PUBLIC_COMPANY
The public company.
PUBLIC_CORPORATION
The public corporation.
PUBLIC_PARTNERSHIP
The public partnership.
REGISTERED_COOPERATIVE
Registered Co-operative.
Copy
"ANY_OTHER_BUSINESS_ENTITY"
Business type information
The type and subtype of the business.
type
string
(
Business type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Type of business entity like corporation, sole prop, governmental.
Enum Value
Description
ANY_OTHER_BUSINESS_ENTITY
The any other business entity.
ASSOCIATION
The association.
CORPORATION
The corporation.
GENERAL_PARTNERSHIP
The general partnership.
GOVERNMENT
The government.
INDIVIDUAL
The individual.
LIMITED_LIABILITY_PARTNERSHIP
The limited liability partnership.
LIMITED_LIABILITY_PROPRIETORS
The limited liability proprietors.
LIMITED_LIABILITY_PRIVATE_CORPORATION
The limited liability private corporation.
LIMITED_PARTNERSHIP
The limited partnership.
LIMITED_PARTNERSHIP_PRIVATE_CORPORATION
The limited partnership private corporation.
NONPROFIT
The nonprofit.
ONLY_BUY_OR_SEND_MONEY
The only buy and send money.
OTHER_CORPORATE_BODY
The other corporate body.
PARTNERSHIP
The partnership.
PRIVATE_PARTNERSHIP
The private partnership.
PROPRIETORSHIP
The proprietorship.
PROPRIETORSHIP_CRAFTSMAN
The proprietorship craftsman.
PROPRIETORY_COMPANY
The proprietory company.
PRIVATE_CORPORATION
The private corporation.
PUBLIC_COMPANY
The public company.
PUBLIC_CORPORATION
The public corporation.
PUBLIC_PARTNERSHIP
The public partnership.
REGISTERED_COOPERATIVE
Registered Co-operative.
subtype
string
(
The business sub type.
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The sub classification of the business type.
Enum Value
Description
ASSO_TYPE_INCORPORATED
The asso type incorporated.
ASSO_TYPE_NON_INCORPORATED
The asso type non incorporated.
GOVT_TYPE_ENTITY
The govt type entity.
GOVT_TYPE_EMANATION
The govt type emanation.
GOVT_TYPE_ESTD_COMM
The govt type estd comm.
GOVT_TYPE_ESTD_FC
The govt type estd fc.
GOVT_TYPE_ESTD_ST_TR
The govt type estd st tr.
Copy
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
Business_address_detail
A simple postal address with coarse-grained fields.
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
type
required
string
(
Business address type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The address type under which this is classified. For example, shipping or dropoff.
Value
Description
WORK
The address of the business.
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
,
"type"
:
"WORK"
}
Business_beneficial_owner
The business beneficial owner of the account.
names
Array of
objects
(
Business name
)
[ 0 .. 5 ] items
Name of the business.
emails
Array of
objects
(
Email of a person orbusiness
)
[ 0 .. 5 ] items
Email addresses of the business.
website
string
<
uri
>
[ 1 .. 50 ] characters
Website of the business.
addresses
Array of
objects
(
Business_address_detail
)
[ 0 .. 5 ] items
List of addresses associated with the business entity.
phones
Array of
objects
(
Phone details
)
[ 0 .. 5 ] items
List of phone number associated with the business.
business_type
object
(
Business type information
)
Information related to the business like the nature of business, started date etc.
business_industry
object
(
Business industry
)
Information related to the business like the nature of business, started date etc.
business_incorporation
object
(
Business_incorporation
)
Information related to the business like the nature of business, started date etc.
percentage_of_ownership
string
<
ppaas_common_percentage_v2
>
(
percentage
)
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The percentage of shares this person owns in the company.
Copy
Expand all
Collapse all
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
Business_entity
The business entity of the account.
names
Array of
objects
(
Business name
)
[ 0 .. 5 ] items
Name of the business.
emails
Array of
objects
(
Email of a person orbusiness
)
[ 0 .. 5 ] items
Email addresses of the business.
website
string
<
uri
>
[ 1 .. 50 ] characters
Website of the business.
addresses
Array of
objects
(
Business_address_detail
)
[ 0 .. 5 ] items
List of addresses associated with the business entity.
phones
Array of
objects
(
Phone details
)
[ 0 .. 5 ] items
List of phone number associated with the business.
documents
Array of
objects
(
Business document
)
[ 0 .. 20 ] items
Business Party related Document data collected from the customer.. For example SSN, ITIN, Business registration number that were collected from the user.
business_type
object
(
Business type information
)
Information related to the business like the nature of business, started date etc.
business_industry
object
(
Business industry
)
Information related to the business like the nature of business, started date etc.
business_incorporation
object
(
Business_incorporation
)
Information related to the business like the nature of business, started date etc.
office_bearers
Array of
objects
(
Office Bearers
)
[ 0 .. 5 ] items
List of Directors present as part of the business entity.
purpose_code
Array of
strings
(
purpose_code
)
The account's purpose code.
Items
Enum Value
Description
P0104
Cross border delivery of goods and services.
P0301
Business related travel purchase.
P0801
Hardware consulting.
P0802
Software consulting.
P0803
Data processing consulting.
P0805
Freelance journalism.
P0806
Other information services.
P0902
Licensing revenues.
P1004
Legal.
P1005
Accounting and tax.
P1006
Business and management consultancy.
P1007
Advertising and market research.
P1008
Research and development.
P1009
Architectural services.
business_description
string
[ 1 .. 256 ] characters
The business goals description. For example, a mission statement.
beneficial_owners
object
(
Beneficial_owners
)
List of beneficial owners part of the entity. They can be either a Person or a business entity.
annual_sales_volume_range
object
(
currency_range
)
The range for the total annual sales volume of the business.
average_monthly_volume_range
object
(
currency_range
)
The range for the average monthly volume of the business.
Copy
Expand all
Collapse all
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"office_bearers"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"role"
:
"CEO"
}
]
,
"purpose_code"
:
[
"P0104"
]
,
"business_description"
:
"string"
,
"beneficial_owners"
:
{
"individual_beneficial_owners"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
,
"business_beneficial_owners"
:
[
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
}
,
"annual_sales_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"maximum_amount"
:
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
"average_monthly_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"maximum_amount"
:
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
Business_incorporation
Business incorporation information.
incorporation_country_code
string
<
ppaas_common_country_code_v2
>
(
country_code
)
= 2 characters
^([A-Z]{2}|C2)$
The incorporation country code.
incorporation_date
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
date of incorporation
Copy
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
capability_name
Optional capabilities of the selected PayPal product for which the customer is being onboarded.
string
(
capability_name
)
[ 1 .. 127 ] characters
^[A-Z0-9_]+$
Optional capabilities of the selected PayPal product for which the customer is being onboarded.
Enum Value
Description
PAYPAL_WALLET_VAULTING_ADVANCED
Enables capability to save payment methods. Supported only when ADVANCED_VAULTING is requested and EXPRESS_CHECKOUT or PPCP is also requested.
PAY_UPON_INVOICE
Enables Pay Upon Invoice (PUI) which is a deferred payment method that allows a buyer to buy now and pay later. Supported only when PAYMENT_METHODS is requested.
APPLE_PAY
Enables Apple Pay capability. Supported only when PAYMENT_METHODS is requested.
GOOGLE_PAY
Enables Google Pay capability. Supported only when PAYMENT_METHODS is requested.
Copy
"PAYPAL_WALLET_VAULTING_ADVANCED"
CLASSIC API integration
The integration details for PayPal CLASSIC endpoints.
object
(
CLASSIC API integration
)
The integration details for PayPal CLASSIC endpoints.
Copy
{ }
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
create_referral_data_response
The shared referral data.
links
Array of
objects
(
Links
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
currency_range
The currency range, from the minimum inclusive amount to the maximum inclusive amount.
minimum_amount
object
(
Money
)
The minimum inclusive amount for the range.
maximum_amount
object
(
Money
)
The maximum inclusive amount for the range.
Copy
Expand all
Collapse all
{
"minimum_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"maximum_amount"
:
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
Document
The document object.
id
string
[ 1 .. 20 ] characters
^[0-9A-Z]+$
The encrypted identifier for the document.
labels
Array of
strings
[ 1 .. 50 ] items
The document labels. A document could be classfied to multiple categories. For example, a bill document can be classfified as
BILL DOCUMENT
and
UTILITY DOCUMENT
.
name
string
[ 1 .. 100 ] characters
^[0-9A-Za-z_-]+$
The file name.
identification_number
string
[ 1 .. 100 ] characters
^[a-zA-Z0-9-]+$
The number for the document. It is the ID number if the document is
ID CARD
, the passport number if the document is
PASSPORT
, etc.
files
Array of
objects
(
File Reference
)
[ 1 .. 50 ] items
The files contained in the document. For example, a document could be represented by a front page file and a back page file, etc.
links
Array of
objects
(
Link Description
)
[ 1 .. 10 ] items
The HATEOAS links.
issue_date
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
expiry_date
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
issuing_country_code
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
Expand all
Collapse all
{
"id"
:
"string"
,
"labels"
:
[
"string"
]
,
"name"
:
"string"
,
"identification_number"
:
"string"
,
"files"
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
"issue_date"
:
"string"
,
"expiry_date"
:
"string"
,
"issuing_country_code"
:
"string"
}
Document type
The type of documents.
string
(
Document type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of documents.
Enum Value
Description
SOCIAL_SECURITY_NUMBER
A social security number.
EMPLOYMENT_IDENTIFICATION_NUMBER
The employee identification number.
TAX_IDENTIFICATION_NUMBER
A tax identification number.
PASSPORT_NUMBER
The passport number.
PENSION_FUND_ID
A pension fund ID.
MEDICAL_INSURANCE_ID
The medical insurance ID.
CNPJ
The identification number issued to Brazilian companies by the Department of Federal Revenue of Brazil.
CPF
A Brazilian individual's taxpayer registry identification number.
PAN
The permanent account number issued by the Indian Income Tax Department.
NATIONAL_ID_CARD
A National ID card number.
Copy
"SOCIAL_SECURITY_NUMBER"
Document type
The type of documents.
string
(
Document type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of documents.
Enum Value
Description
SOCIAL_SECURITY_NUMBER
A social security number.
EMPLOYMENT_IDENTIFICATION_NUMBER
The employee identification number.
TAX_IDENTIFICATION_NUMBER
The tax identification number.
PASSPORT_NUMBER
A passport number.
PENSION_FUND_ID
A pension fund ID.
MEDICAL_INSURANCE_ID
A medical insurance ID.
CNPJ
The identification number issued to Brazilian companies by the Department of Federal Revenue of Brazil.
CPF
A Brazilian individual's taxpayer registry identification number.
PAN
The Permanent account number issued by the Indian Income Tax Department.
BUSINESS_REGISTRATION
A unique identifier for business entities issued by the governing agency.
Copy
"SOCIAL_SECURITY_NUMBER"
Email of a person orbusiness
An email address at which the person or business can be contacted.
type
required
string
[ 1 .. 50 ] characters
^[0-9A-Z_]+$
The role of the email address.
Value
Description
CUSTOMER_SERVICE
The email ID to be used to contact the customer service of the business.
email
required
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
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
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
File Reference
The file reference. Can be a file in PayPal MediaServ, PayPal DMS, or another custom store.
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
Financial instrument.
Financial instruments attached to this account.
banks
Array of
objects
(
Bank Account
)
[ 0 .. 5 ] items
An array of banks attached to this managed account.
Copy
Expand all
Collapse all
{
"banks"
:
[
{
"nick_name"
:
"string"
,
"account_number"
:
"string"
,
"account_type"
:
"CHECKING"
,
"identifiers"
:
[
{
"type"
:
"BANK_CODE"
,
"value"
:
"string"
}
]
,
"currency_code"
:
"str"
,
"branch_location"
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
"mandate"
:
{
"accepted"
:
true
}
}
]
}
Individual owner role type
Role of the person party played in the account.
string
(
Individual owner role type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Role of the person party played in the account.
Value
Description
PRIMARY
Primary account holder.
Copy
"PRIMARY"
Individual_beneficial_owner
The individual owner of the account.
names
Array of
objects
(
Person name
)
[ 0 .. 5 ] items
The name of the person.
addresses
Array of
objects
(
Person address detail
)
[ 0 .. 5 ] items
The list of addresses associated with the person.
phones
Array of
objects
(
Phone details
)
[ 0 .. 5 ] items
The list of phone numbers associated with the person.
citizenship
string
<
ppaas_common_country_code_v2
>
(
country_code
)
= 2 characters
^([A-Z]{2}|C2)$
The citizenship country code of the person.
birth_details
object
(
Birth details
)
The person's birth details.
percentage_of_ownership
string
<
ppaas_common_percentage_v2
>
(
percentage
)
^((-?[0-9]+)|(-?([0-9]+)?[.][0-9]+))$
The percentage of shares this person owns in the company.
Copy
Expand all
Collapse all
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
Individual_owner
The individual owner of the account.
names
Array of
objects
(
Person name
)
[ 0 .. 5 ] items
The name of the person.
addresses
Array of
objects
(
Person address detail
)
[ 0 .. 5 ] items
The list of addresses associated with the person.
phones
Array of
objects
(
Phone details
)
[ 0 .. 5 ] items
The list of phone numbers associated with the person.
documents
Array of
objects
(
Person document
)
[ 0 .. 20 ] items
A person's or party's related document data collected from the customer. For example SSN, ITIN, or business registration number collected from the user.
Note:
This field is not applicable for POST
/v2/customer/partner-referrals
API calls.
citizenship
string
<
ppaas_common_country_code_v2
>
(
country_code
)
= 2 characters
^([A-Z]{2}|C2)$
The citizenship country code of the person.
birth_details
object
(
Birth details
)
The person's birth details.
type
string
(
Individual owner role type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The actual role of this user on the account, PRIMARY/SECONDARY.
Value
Description
PRIMARY
Primary account holder.
Copy
Expand all
Collapse all
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"type"
:
"PRIMARY"
}
integration_details
The integration details for the partner and customer relationship. Required if
operation
is
API_INTEGRATION
.
classic_api_integration
object
(
CLASSIC API integration
)
The integration details for PayPal CLASSIC endpoints.
rest_api_integration
object
(
REST API Integration
)
The integration details for PayPal REST endpoints.
Copy
Expand all
Collapse all
{
"classic_api_integration"
:
{ }
,
"rest_api_integration"
:
{
"integration_method"
:
"PAYPAL"
,
"integration_channel"
:
"string"
,
"integration_type"
:
"FIRST_PARTY"
,
"first_party_details"
:
{
"features"
:
[
"PAYOUTS"
]
,
"seller_nonce"
:
"stringstringstringstringstringstringstringst"
}
,
"third_party_details"
:
{
"features"
:
[
"PAYOUTS"
]
,
"signup_mode"
:
"string"
,
"organization"
:
"string"
}
}
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
.
string
<
ppaas_common_language_v3
>
(
language
)
[ 2 .. 10 ] characters
^[a-z]{2}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}))...
Show pattern
The
language tag
for the language in which to localize the error-related strings, such as messages, issues, and suggested actions. The tag is made up of the
ISO 639-2 language code
, the optional
ISO-15924 script tag
, and the
ISO-3166 alpha-2 country code
.
Copy
"string"
legal_consent
The customer-provided consent.
type
required
string
[ 1 .. 127 ] characters
^[0-9A-Z_-]+$
The type of consent.
SHARE_DATA_CONSENT
gives consent to you to share your customer's data with PayPal.
Value
Description
SHARE_DATA_CONSENT
The consent given by the customer to share their data with paypal.
granted
required
boolean
Indicates whether the customer agreed to share this type of data. To give consent, specify
true
. To withhold consent, specify
false
.
Copy
{
"type"
:
"SHARE_DATA_CONSENT"
,
"granted"
:
true
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
link_description
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
link_description
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
Mandate
Seller’s consent to operate on this financial instrument.
accepted
required
boolean
Whether mandate was accepted or not.
Copy
{
"accepted"
:
true
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
Office Bearers
The office bearer associated to the account.
names
Array of
objects
(
Person name
)
[ 0 .. 5 ] items
The name of the person.
addresses
Array of
objects
(
Person address detail
)
[ 0 .. 5 ] items
The list of addresses associated with the person.
phones
Array of
objects
(
Phone details
)
[ 0 .. 5 ] items
The list of phone numbers associated with the person.
documents
Array of
objects
(
Person document
)
[ 0 .. 20 ] items
A person's or party's related document data collected from the customer. For example SSN, ITIN, or business registration number collected from the user.
Note:
This field is not applicable for POST
/v2/customer/partner-referrals
API calls.
citizenship
string
<
ppaas_common_country_code_v2
>
(
country_code
)
= 2 characters
^([A-Z]{2}|C2)$
The citizenship country code of the person.
birth_details
object
(
Birth details
)
The person's birth details.
role
string
(
Role type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The role of the office bearer in the company.
Enum Value
Description
CEO
The ceo.
CHAIRMAN
The chairman.
DIRECTOR
Director of the business
SECRETARY
The secretary.
TREASURER
The treasurer.
TRUSTEE
The trustee.
Copy
Expand all
Collapse all
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"role"
:
"CEO"
}
Offline Oboarding Preference
The preference details for offline onboarding without UI.
object
(
Offline Oboarding Preference
)
The preference details for offline onboarding without UI.
Copy
{ }
operation
The required operation to share data.
operation
required
string
[ 1 .. 255 ] characters
^[0-9A-Z_-]+$
The operation to enable for the customer. To enable the collection of the API permissions that you require to integrate with the customer, specify
API_INTEGRATION
.
BANK_ADDITION
is supported only for the US.
Enum Value
Description
API_INTEGRATION
The operation used by partner request permission for customers api access.
BANK_ADDITION
Captured state of an order.
BILLING_AGREEMENT
The operation to create a billing agreement.
CONTEXTUAL_MARKETING_CONSENT
The operation to create a contextual marketing consent.
api_integration_preference
object
(
integration_details
)
The integration details for the partner and customer relationship. Required if
operation
is
API_INTEGRATION
.
offline_onboarding_preference
object
(
Offline Oboarding Preference
)
The preference details for offline onboarding without UI.
billing_agreement
object
(
billing_agreement
)
The details of the billing agreement between the partner and a seller.
Copy
Expand all
Collapse all
{
"operation"
:
"API_INTEGRATION"
,
"api_integration_preference"
:
{
"classic_api_integration"
:
{ }
,
"rest_api_integration"
:
{
"integration_method"
:
"PAYPAL"
,
"integration_channel"
:
"string"
,
"integration_type"
:
"FIRST_PARTY"
,
"first_party_details"
:
{
"features"
:
[
"PAYOUTS"
]
,
"seller_nonce"
:
"stringstringstringstringstringstringstringst"
}
,
"third_party_details"
:
{
"features"
:
[
"PAYOUTS"
]
,
"signup_mode"
:
"string"
,
"organization"
:
"string"
}
}
}
,
"offline_onboarding_preference"
:
{ }
,
"billing_agreement"
:
{
"description"
:
"string"
,
"billing_experience_preference"
:
{
"experience_id"
:
"string"
,
"billing_context_set"
:
true
}
,
"merchant_custom_data"
:
"string"
,
"approval_url"
:
"
http://example.com
"
,
"ec_token"
:
"string"
}
}
partner_configuration_override
The preference to customize the web experience of the customer by overriding that is set at the Partner's Account.
return_url
string
<
uri
>
[ 1 .. 127 ] characters
The URL to which to redirect the customer upon completion of the onboarding process.
return_url_description
string
[ 1 .. 127 ] characters
^.+$
The description of the return URL.
show_add_credit_card
boolean
Indicates whether to show an add credit card page.
Copy
{
"return_url"
:
"
http://example.com
"
,
"return_url_description"
:
"string"
,
"show_add_credit_card"
:
true
}
Payout Attributes
Payout specific attributes.
marketplace
boolean
If
true
, specifies that the merchant or platform is offering goods or services on behalf of 3rd party sellers.
kyc_required
boolean
If
true
, specifies that the Kyc is required for the merchant.
country_transfer_method_currency_selection
Array of
objects
(
Requested country, transfer method and currency
)
[ 1 .. 50 ] items
Requested country, transfer method and currency.
Copy
Expand all
Collapse all
{
"marketplace"
:
true
,
"kyc_required"
:
true
,
"country_transfer_method_currency_selection"
:
[
{
"transfer_methods"
:
[
{
"transfer_method_type"
:
"BANK_ACCOUNT"
,
"currencies"
:
[
"str"
]
}
]
,
"country"
:
"st"
}
]
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
Person
Details of the person or party.
id
string
[ 1 .. 20 ] characters
^[0-9A-Z]+$
The encrypted party ID.
names
Array of
objects
(
Person name
)
[ 0 .. 5 ] items
The name of the person.
addresses
Array of
objects
(
Person address detail
)
[ 0 .. 5 ] items
The list of addresses associated with the person.
phones
Array of
objects
(
Phone details
)
[ 0 .. 5 ] items
The list of phone numbers associated with the person.
documents
Array of
objects
(
Person document
)
[ 0 .. 20 ] items
A person's or party's related document data collected from the customer. For example SSN, ITIN, or business registration number collected from the user.
Note:
This field is not applicable for POST
/v2/customer/partner-referrals
API calls.
citizenship
string
<
ppaas_common_country_code_v2
>
(
country_code
)
= 2 characters
^([A-Z]{2}|C2)$
The citizenship country code of the person.
birth_details
object
(
Birth details
)
The person's birth details.
Copy
Expand all
Collapse all
{
"id"
:
"string"
,
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
}
Person address detail
A simple postal address with coarse-grained fields.
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
type
required
string
(
Person address type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The address type under which this is classified.
Value
Description
HOME
The home address of the customer.
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
,
"type"
:
"HOME"
}
Person address detail
A simple postal address with coarse-grained fields.
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
type
required
string
(
Person address type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The address type under which this is classified.
Value
Description
HOME
The home address of the customer.
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
,
"type"
:
"HOME"
}
Person address type
The address type under which the provided address is tagged.
string
(
Person address type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The address type under which the provided address is tagged.
Value
Description
HOME
The home address of the customer.
Copy
"HOME"
Person document
The documents associated with the person.
identification_number
string
[ 1 .. 100 ] characters
^[a-zA-Z0-9-]+$
The number for the document. It is the ID number if the document is
ID CARD
, the passport number if the document is
PASSPORT
, etc.
issuing_country_code
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
type
string
(
Document type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The actual type of the document. It could be
ID_CARD
,
PASSPORT
, etc.
Enum Value
Description
SOCIAL_SECURITY_NUMBER
A social security number.
EMPLOYMENT_IDENTIFICATION_NUMBER
The employee identification number.
TAX_IDENTIFICATION_NUMBER
A tax identification number.
PASSPORT_NUMBER
The passport number.
PENSION_FUND_ID
A pension fund ID.
MEDICAL_INSURANCE_ID
The medical insurance ID.
CNPJ
The identification number issued to Brazilian companies by the Department of Federal Revenue of Brazil.
CPF
A Brazilian individual's taxpayer registry identification number.
PAN
The permanent account number issued by the Indian Income Tax Department.
NATIONAL_ID_CARD
A National ID card number.
Copy
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
Person document
The documents associated with the person.
identification_number
string
[ 1 .. 100 ] characters
^[a-zA-Z0-9-]+$
The number for the document. It is the ID number if the document is
ID CARD
, the passport number if the document is
PASSPORT
, etc.
issuing_country_code
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
type
string
(
Document type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The actual type of the document. It could be
ID_CARD
,
PASSPORT
, etc.
Enum Value
Description
SOCIAL_SECURITY_NUMBER
A social security number.
EMPLOYMENT_IDENTIFICATION_NUMBER
The employee identification number.
TAX_IDENTIFICATION_NUMBER
A tax identification number.
PASSPORT_NUMBER
The passport number.
PENSION_FUND_ID
A pension fund ID.
MEDICAL_INSURANCE_ID
The medical insurance ID.
CNPJ
The identification number issued to Brazilian companies by the Department of Federal Revenue of Brazil.
CPF
A Brazilian individual's taxpayer registry identification number.
PAN
The permanent account number issued by the Indian Income Tax Department.
NATIONAL_ID_CARD
A National ID card number.
Copy
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
Person name
The name of the person.
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
type
required
string
(
Person name type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of name. Currently supported values are:
LEGAL
.
Value
Description
LEGAL
Indicates that this name is the legal name of the user.
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
,
"type"
:
"LEGAL"
}
Person name
The name of the person.
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
type
required
string
(
Person name type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of name. Currently supported values are:
LEGAL
.
Value
Description
LEGAL
Indicates that this name is the legal name of the user.
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
,
"type"
:
"LEGAL"
}
Person name type
The person's name type.
string
(
Person name type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The person's name type.
Value
Description
LEGAL
Indicates that this name is the legal name of the user.
Copy
"LEGAL"
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
Phone details
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
type
required
string
(
Phone Type
)
The phone type.
Enum Value
Description
FAX
A fax machine.
HOME
A home phone.
MOBILE
A mobile phone.
OTHER
Other.
PAGER
A pager.
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
"type"
:
"FAX"
}
Phone details
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
type
required
string
(
Phone type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of phone number provided. For example, home, work, or mobile.
Enum Value
Description
CUSTOMER_SERVICE
The customer service phone number.
BUSINESS
The business phone number.
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
"type"
:
"CUSTOMER_SERVICE"
}
Phone details
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
type
required
string
(
Phone Type
)
The phone type.
Enum Value
Description
FAX
A fax machine.
HOME
A home phone.
MOBILE
A mobile phone.
OTHER
Other.
PAGER
A pager.
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
"type"
:
"FAX"
}
Phone number tag
Tag associated with the phone number.
string
(
Phone number tag
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Tag associated with the phone number.
Enum Value
Description
MOBILE
The mobile telephone number.
LANDLINE
The landline telephone number.
Copy
"MOBILE"
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
A fax machine.
HOME
A home phone.
MOBILE
A mobile phone.
OTHER
Other.
PAGER
A pager.
Copy
"FAX"
Phone type
The type of phone number provided. For example, home, work, or mobile.
string
(
Phone type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
The type of phone number provided. For example, home, work, or mobile.
Enum Value
Description
CUSTOMER_SERVICE
The customer service phone number.
BUSINESS
The business phone number.
Copy
"CUSTOMER_SERVICE"
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
product_name
The PayPal product for which the customer is onboarded.
string
(
product_name
)
[ 1 .. 127 ] characters
^[0-9A-Z_-]+$
The PayPal product for which the customer is onboarded.
Enum Value
Description
ALIPAY
Alipay is a China-based payment method that allows customers to complete transactions online using their Alipay wallet. Include only if Alipay alone is required. You can use PPCP if all features are required.
BANCONTACT
Bancontact is a Belgium-based payment method that allows customers to complete transactions online using their bank credentials. Include only if Bancontact alone is required. You can use PPCP if all features are required.
BLIK
Blik is a Poland-based payment method that allows customers to complete transactions online using their bank credentials. Include only if Blik alone is required. You can use PPCP if all features are required.
EPS
EPS is an Austria-based payment method that allows customers to complete transactions online using their bank credentials. Include only if EPS alone is required. You can use PPCP if all features are required.
PPCP
PayPal Complete Payments product, which includes Express Checkout, advanced credit and debit card payments, Apple Pay, and Google Pay. Use PPCP if all features are required.
EXPRESS_CHECKOUT
Express checkout product.
PAYMENT_METHODS
PayPal Alternative Payment Methods product. Include only if Apple Pay or Google Pay or both are required alone. You can use PPCP if all features are required.
ADVANCED_VAULTING
PayPal Advanced Vaulting product. Must be requested along with either EXPRESS_CHECKOUT or PPCP. Include only if ADVANCED_VAULTING alone is required. You can use PPCP if all features are required.
IDEAL
iDEAL is a Netherlands-based payment method that allows customers to complete transactions online using their bank credentials. Include only if iDEAL alone is required. You can use PPCP if all features are required.
MB_WAY
MB Way is a Portugal-based payment method that allows customers to complete transactions online using their MB Way wallet. Include only if MB Way alone is required. You can use PPCP if all features are required.
MULTIBANCO
Multibanco is a Portugal-based payment method that allows customers to complete transactions online using their bank credentials or pay in cash at a bank branch. Include only if Multibanco alone is required. You can use PPCP if all features are required.
PPPLUS
PayPal PLUS product.
PRZELEWY24
Przelewy24 is a Poland-based payment method that allows customers to complete transactions online. Include only if Przelewy24 alone is required. You can use PPCP if all features are required.
SATISPAY
Satispay is an Italy-based payment method that allows customers to complete transactions online using their bank credentials. Include only if Satispay alone is required. You can use PPCP if all features are required.
TRUSTLY
Trustly is a payment method that allows customers from (Austria (AT), Germany (DE), Denmark (DK), Estonia (EE), Spain (ES), Finland (FI), Great Britain (GB), Lithuania (LT), Latvia (LV), Netherlands (NL), Norway (NO), Sweden (SE)) to complete transactions online using their bank credentials. Include only if Trustly alone is required. You can use PPCP if all features are required.
WECHAT_PAY
WeChat Pay is a China-based payment method that allows customers to complete transactions online using their WeChat Pay wallet. Include only if WeChat Pay alone is required. You can use PPCP if all features are required.
WEBSITE_PAYMENT_PRO
PayPal Professional product.
ZETTLE
PayPal Zettle in-person payments product.
HYPERWALLET_PAYOUTS
Hyperwallet payouts product
CRYPTO_PYMTS
Crypto payments product
Copy
"ALIPAY"
purpose_code
The purpose code. Required only for India. For more information, see the Reserve Bank Of India web site. Value is:
P0104
. Cross border delivery of goods and services.
P0301
. Business related travel purchase.
P0801
. Hardware consulting.
P0802
. Software consulting.
P0803
. Data processing consulting.
P0805
. Freelance journalism.
P0806
. Other information services.
P0902
. Licensing revenues.
P1004
. Legal.
P1005
. Accounting and tax.
P1006
. Business and management consultancy.
P1007
. Advertising and market research.
P1008
. Research and development.
P1009
. Architectural services.
string
(
purpose_code
)
[ 1 .. 50 ] characters
^[a-zA-Z0-9]([a-zA-Z0-9_ ])+$
The purpose code. Required only for India. For more information, see the Reserve Bank Of India web site. Value is:
P0104
. Cross border delivery of goods and services.
P0301
. Business related travel purchase.
P0801
. Hardware consulting.
P0802
. Software consulting.
P0803
. Data processing consulting.
P0805
. Freelance journalism.
P0806
. Other information services.
P0902
. Licensing revenues.
P1004
. Legal.
P1005
. Accounting and tax.
P1006
. Business and management consultancy.
P1007
. Advertising and market research.
P1008
. Research and development.
P1009
. Architectural services.
Enum Value
Description
P0104
Cross border delivery of goods and services.
P0301
Business related travel purchase.
P0801
Hardware consulting.
P0802
Software consulting.
P0803
Data processing consulting.
P0805
Freelance journalism.
P0806
Other information services.
P0902
Licensing revenues.
P1004
Legal.
P1005
Accounting and tax.
P1006
Business and management consultancy.
P1007
Advertising and market research.
P1008
Research and development.
P1009
Architectural services.
Copy
"P0104"
referral_data
The customer's referral data that partners share with PayPal.
individual_owners
Array of
objects
(
Individual_owner
)
[ 0 .. 2 ] items
List of owners in the account. There should be only one primary account owner which is mentioned in their role_type.
business_entity
object
(
Business_entity
)
Business entity of the account.
tracking_id
string
[ 1 .. 127 ] characters
The partner's unique identifier for this customer in their system which can be used to track user in PayPal.
operations
required
Array of
objects
(
operation
)
[ 1 .. 5 ] items
An array of operations to perform for the customer while they share their data.
products
Array of
strings
(
product_name
)
[ 1 .. 5 ] items
An array of PayPal products to which the partner wants to onboard the customer.
Items
Enum Value
Description
ALIPAY
Alipay is a China-based payment method that allows customers to complete transactions online using their Alipay wallet. Include only if Alipay alone is required. You can use PPCP if all features are required.
BANCONTACT
Bancontact is a Belgium-based payment method that allows customers to complete transactions online using their bank credentials. Include only if Bancontact alone is required. You can use PPCP if all features are required.
BLIK
Blik is a Poland-based payment method that allows customers to complete transactions online using their bank credentials. Include only if Blik alone is required. You can use PPCP if all features are required.
EPS
EPS is an Austria-based payment method that allows customers to complete transactions online using their bank credentials. Include only if EPS alone is required. You can use PPCP if all features are required.
PPCP
PayPal Complete Payments product, which includes Express Checkout, advanced credit and debit card payments, Apple Pay, and Google Pay. Use PPCP if all features are required.
EXPRESS_CHECKOUT
Express checkout product.
PAYMENT_METHODS
PayPal Alternative Payment Methods product. Include only if Apple Pay or Google Pay or both are required alone. You can use PPCP if all features are required.
ADVANCED_VAULTING
PayPal Advanced Vaulting product. Must be requested along with either EXPRESS_CHECKOUT or PPCP. Include only if ADVANCED_VAULTING alone is required. You can use PPCP if all features are required.
IDEAL
iDEAL is a Netherlands-based payment method that allows customers to complete transactions online using their bank credentials. Include only if iDEAL alone is required. You can use PPCP if all features are required.
MB_WAY
MB Way is a Portugal-based payment method that allows customers to complete transactions online using their MB Way wallet. Include only if MB Way alone is required. You can use PPCP if all features are required.
MULTIBANCO
Multibanco is a Portugal-based payment method that allows customers to complete transactions online using their bank credentials or pay in cash at a bank branch. Include only if Multibanco alone is required. You can use PPCP if all features are required.
PPPLUS
PayPal PLUS product.
PRZELEWY24
Przelewy24 is a Poland-based payment method that allows customers to complete transactions online. Include only if Przelewy24 alone is required. You can use PPCP if all features are required.
SATISPAY
Satispay is an Italy-based payment method that allows customers to complete transactions online using their bank credentials. Include only if Satispay alone is required. You can use PPCP if all features are required.
TRUSTLY
Trustly is a payment method that allows customers from (Austria (AT), Germany (DE), Denmark (DK), Estonia (EE), Spain (ES), Finland (FI), Great Britain (GB), Lithuania (LT), Latvia (LV), Netherlands (NL), Norway (NO), Sweden (SE)) to complete transactions online using their bank credentials. Include only if Trustly alone is required. You can use PPCP if all features are required.
WECHAT_PAY
WeChat Pay is a China-based payment method that allows customers to complete transactions online using their WeChat Pay wallet. Include only if WeChat Pay alone is required. You can use PPCP if all features are required.
WEBSITE_PAYMENT_PRO
PayPal Professional product.
ZETTLE
PayPal Zettle in-person payments product.
HYPERWALLET_PAYOUTS
Hyperwallet payouts product
CRYPTO_PYMTS
Crypto payments product
capabilities
Array of
strings
(
capability_name
)
[ 1 .. 5 ] items
An array of capabilities which the partner wants to enable for the selected products. Supported only when products are specified.
Items
Enum Value
Description
PAYPAL_WALLET_VAULTING_ADVANCED
Enables capability to save payment methods. Supported only when ADVANCED_VAULTING is requested and EXPRESS_CHECKOUT or PPCP is also requested.
PAY_UPON_INVOICE
Enables Pay Upon Invoice (PUI) which is a deferred payment method that allows a buyer to buy now and pay later. Supported only when PAYMENT_METHODS is requested.
APPLE_PAY
Enables Apple Pay capability. Supported only when PAYMENT_METHODS is requested.
GOOGLE_PAY
Enables Google Pay capability. Supported only when PAYMENT_METHODS is requested.
outside_process_dependencies
Array of
any
[ 1 .. 5 ] items
An array of dependent processes.
legal_consents
required
Array of
objects
(
legal_consent
)
[ 1 .. 5 ] items
An array of all consents that the partner has received from this seller. If
SHARE_DATA_CONSENT
is not granted, PayPal does not store customer data.
email
string
<
ppaas_common_email_address_v2
>
(
email_address
)
[ 3 .. 254 ] characters
^.+@[^"\-].+$
Email address of the customer used to create the account.
preferred_language_code
string
<
ppaas_common_language_v3
>
(
language
)
[ 2 .. 10 ] characters
^[a-z]{2}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}))...
Show pattern
The preferred
locale code
to use in the onboarding flow for the customer.
partner_config_override
object
(
partner_configuration_override
)
The configuration property that the partner intends to override for this onboarding request.
financial_instruments
object
(
Financial instrument.
)
Array of financial instruments attached to the customer's account.
payout_attributes
object
(
Payout Attributes
)
Payout specific attributes.
legal_country_code
string
<
ppaas_common_country_code_v2
>
(
country_code
)
= 2 characters
^([A-Z]{2}|C2)$
Legal Country Code.
Copy
Expand all
Collapse all
{
"individual_owners"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"type"
:
"PRIMARY"
}
]
,
"business_entity"
:
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"office_bearers"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"role"
:
"CEO"
}
]
,
"purpose_code"
:
[
"P0104"
]
,
"business_description"
:
"string"
,
"beneficial_owners"
:
{
"individual_beneficial_owners"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
,
"business_beneficial_owners"
:
[
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
}
,
"annual_sales_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"maximum_amount"
:
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
"average_monthly_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"maximum_amount"
:
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
"tracking_id"
:
"string"
,
"operations"
:
[
{
"operation"
:
"API_INTEGRATION"
,
"api_integration_preference"
:
{
"classic_api_integration"
:
{ }
,
"rest_api_integration"
:
{
"integration_method"
:
"PAYPAL"
,
"integration_channel"
:
"string"
,
"integration_type"
:
"FIRST_PARTY"
,
"first_party_details"
:
{
"features"
:
[
"PAYOUTS"
]
,
"seller_nonce"
:
"stringstringstringstringstringstringstringst"
}
,
"third_party_details"
:
{
"features"
:
[
"PAYOUTS"
]
,
"signup_mode"
:
"string"
,
"organization"
:
"string"
}
}
}
,
"offline_onboarding_preference"
:
{ }
,
"billing_agreement"
:
{
"description"
:
"string"
,
"billing_experience_preference"
:
{
"experience_id"
:
"string"
,
"billing_context_set"
:
true
}
,
"merchant_custom_data"
:
"string"
,
"approval_url"
:
"
http://example.com
"
,
"ec_token"
:
"string"
}
}
]
,
"products"
:
[
"ALIPAY"
]
,
"capabilities"
:
[
"PAYPAL_WALLET_VAULTING_ADVANCED"
]
,
"outside_process_dependencies"
:
[
null
]
,
"legal_consents"
:
[
{
"type"
:
"SHARE_DATA_CONSENT"
,
"granted"
:
true
}
]
,
"email"
:
"string"
,
"preferred_language_code"
:
"string"
,
"partner_config_override"
:
{
"return_url"
:
"
http://example.com
"
,
"return_url_description"
:
"string"
,
"show_add_credit_card"
:
true
}
,
"financial_instruments"
:
{
"banks"
:
[
{
"nick_name"
:
"string"
,
"account_number"
:
"string"
,
"account_type"
:
"CHECKING"
,
"identifiers"
:
[
{
"type"
:
"BANK_CODE"
,
"value"
:
"string"
}
]
,
"currency_code"
:
"str"
,
"branch_location"
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
"mandate"
:
{
"accepted"
:
true
}
}
]
}
,
"payout_attributes"
:
{
"marketplace"
:
true
,
"kyc_required"
:
true
,
"country_transfer_method_currency_selection"
:
[
{
"transfer_methods"
:
[
{
"transfer_method_type"
:
"BANK_ACCOUNT"
,
"currencies"
:
[
"str"
]
}
]
,
"country"
:
"st"
}
]
}
,
"legal_country_code"
:
"st"
}
referral_data_response
The share referral data response.
partner_referral_id
string
[ 1 .. 255 ] characters
^[A-Za-z0-9+/=]+$
The ID to access the customer's data shared by the partner with PayPal.
submitter_payer_id
string
[ 1 .. 20 ] characters
^[0-9A-Z]+$
The payer ID of the partner who shared the referral data.
submitter_client_id
string
[ 1 .. 255 ] characters
^[a-zA-Z0-9-_]+$
The client ID of the partner who shared the referral data. This cliend ID will be returned only when the caller is determined as an internal partner, which means the scope of the caller's security context only have "
https://uri.paypal.com/services/customer/partner-referrals
", For more information, see
Api Actor type in Typhoon service
.
links
Array of
objects
(
Links
)
[ 0 .. 2 ] items
An array of request-related
HATEOAS links
.
referral_data
object
(
referral_data
)
The customer's referral data that partners share with PayPal.
Copy
Expand all
Collapse all
{
"partner_referral_id"
:
"string"
,
"submitter_payer_id"
:
"string"
,
"submitter_client_id"
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
"referral_data"
:
{
"individual_owners"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"type"
:
"PRIMARY"
}
]
,
"business_entity"
:
{
"names"
:
[
{
"business_name"
:
"string"
,
"type"
:
"DOING_BUSINESS_AS"
}
]
,
"emails"
:
[
{
"type"
:
"CUSTOMER_SERVICE"
,
"email"
:
"string"
}
]
,
"website"
:
"
http://example.com
"
,
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
"type"
:
"WORK"
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
"type"
:
"CUSTOMER_SERVICE"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"office_bearers"
:
[
{
"names"
:
[
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
,
"type"
:
"LEGAL"
}
]
,
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
"type"
:
"HOME"
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
"type"
:
"FAX"
}
]
,
"documents"
:
[
{
"identification_number"
:
"string"
,
"issuing_country_code"
:
"string"
,
"type"
:
"SOCIAL_SECURITY_NUMBER"
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"role"
:
"CEO"
}
]
,
"purpose_code"
:
[
"P0104"
]
,
"business_description"
:
"string"
,
"beneficial_owners"
:
{
"individual_beneficial_owners"
:
[
{
"names"
:
[
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
"full_name"
:
null
,
"type"
:
null
}
]
,
"addresses"
:
[
{
"address_line_1"
:
null
,
"address_line_2"
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
"type"
:
null
}
]
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
"type"
:
null
}
]
,
"citizenship"
:
"st"
,
"birth_details"
:
{
"date_of_birth"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
,
"business_beneficial_owners"
:
[
{
"names"
:
[
{
"business_name"
:
null
,
"type"
:
null
}
]
,
"emails"
:
[
{
"type"
:
null
,
"email"
:
null
}
]
,
"website"
:
"
http://example.com
"
,
"addresses"
:
[
{
"address_line_1"
:
null
,
"address_line_2"
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
"type"
:
null
}
]
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
"type"
:
null
}
]
,
"business_type"
:
{
"type"
:
"ANY_OTHER_BUSINESS_ENTITY"
,
"subtype"
:
"ASSO_TYPE_INCORPORATED"
}
,
"business_industry"
:
{
"category"
:
"string"
,
"mcc_code"
:
"string"
,
"subcategory"
:
"string"
}
,
"business_incorporation"
:
{
"incorporation_country_code"
:
"st"
,
"incorporation_date"
:
"stringstri"
}
,
"percentage_of_ownership"
:
"string"
}
]
}
,
"annual_sales_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"maximum_amount"
:
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
"average_monthly_volume_range"
:
{
"minimum_amount"
:
{
"currency_code"
:
"str"
,
"value"
:
"string"
}
,
"maximum_amount"
:
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
"tracking_id"
:
"string"
,
"operations"
:
[
{
"operation"
:
"API_INTEGRATION"
,
"api_integration_preference"
:
{
"classic_api_integration"
:
{ }
,
"rest_api_integration"
:
{
"integration_method"
:
"PAYPAL"
,
"integration_channel"
:
"string"
,
"integration_type"
:
"FIRST_PARTY"
,
"first_party_details"
:
{
"features"
:
[
null
]
,
"seller_nonce"
:
"stringstringstringstringstringstringstringst"
}
,
"third_party_details"
:
{
"features"
:
[
null
]
,
"signup_mode"
:
"string"
,
"organization"
:
"string"
}
}
}
,
"offline_onboarding_preference"
:
{ }
,
"billing_agreement"
:
{
"description"
:
"string"
,
"billing_experience_preference"
:
{
"experience_id"
:
"string"
,
"billing_context_set"
:
true
}
,
"merchant_custom_data"
:
"string"
,
"approval_url"
:
"
http://example.com
"
,
"ec_token"
:
"string"
}
}
]
,
"products"
:
[
"ALIPAY"
]
,
"capabilities"
:
[
"PAYPAL_WALLET_VAULTING_ADVANCED"
]
,
"outside_process_dependencies"
:
[
null
]
,
"legal_consents"
:
[
{
"type"
:
"SHARE_DATA_CONSENT"
,
"granted"
:
true
}
]
,
"email"
:
"string"
,
"preferred_language_code"
:
"string"
,
"partner_config_override"
:
{
"return_url"
:
"
http://example.com
"
,
"return_url_description"
:
"string"
,
"show_add_credit_card"
:
true
}
,
"financial_instruments"
:
{
"banks"
:
[
{
"nick_name"
:
"string"
,
"account_number"
:
"string"
,
"account_type"
:
"CHECKING"
,
"identifiers"
:
[
{
"type"
:
"BANK_CODE"
,
"value"
:
"string"
}
]
,
"currency_code"
:
"str"
,
"branch_location"
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
"mandate"
:
{
"accepted"
:
true
}
}
]
}
,
"payout_attributes"
:
{
"marketplace"
:
true
,
"kyc_required"
:
true
,
"country_transfer_method_currency_selection"
:
[
{
"transfer_methods"
:
[
{
"transfer_method_type"
:
"BANK_ACCOUNT"
,
"currencies"
:
[
null
]
}
]
,
"country"
:
"st"
}
]
}
,
"legal_country_code"
:
"st"
}
}
Requested country, transfer method and currency
Requested country, transfer method and currency.
transfer_methods
Array of
objects
(
Requested transfer method and currency for a country
)
[ 1 .. 50 ] items
Requested transfer method and currency for a country.
country
string
<
ppaas_common_country_code_v2
>
(
country_code
)
= 2 characters
^([A-Z]{2}|C2)$
Country.
Copy
Expand all
Collapse all
{
"transfer_methods"
:
[
{
"transfer_method_type"
:
"BANK_ACCOUNT"
,
"currencies"
:
[
"str"
]
}
]
,
"country"
:
"st"
}
Requested transfer method and currency for a country
Requested transfer method and currency for a country.
transfer_method_type
string
[ 1 .. 50 ] characters
^[0-9A-Z_-]+$
Transfer Method type.
Enum Value
Description
BANK_ACCOUNT
Transfer method type- Bank Account
PAYPAL
Transfer method type- Bank Account
VENMO
Transfer method type- Bank Account
WIRE_ACCOUNT
Transfer method type- Bank Account
currencies
Array of
strings
<
ppaas_common_currency_code_v2
>
(
currency_code
)
[ 1 .. 50 ] items
Requested Currencies for a Transfer Method.
Copy
Expand all
Collapse all
{
"transfer_method_type"
:
"BANK_ACCOUNT"
,
"currencies"
:
[
"str"
]
}
REST API Integration
The integration details for PayPal REST endpoints.
integration_method
string
[ 1 .. 255 ] characters
^[0-9A-Z_-]+$
Default:
"PAYPAL"
The REST-credential integration method.
Enum Value
Description
PAYPAL
PayPal integration method.
SDK
Indicates that merchant onboarding will be done via the Embedded SDK.
integration_channel
string
[ 1 .. 128 ] characters
^[A-Z0-9_]+$
The rest api integration channel.
integration_type
required
string
(
Integration Type
)
[ 1 .. 255 ] characters
^[0-9A-Z_-]+$
The type of REST-endpoint integration. To integrate with Braintree v.zero for PayPal REST endpoints, specify
third_party_details
.
Enum Value
Description
FIRST_PARTY
A first-party integration.
THIRD_PARTY
A third-party integration.
first_party_details
object
(
REST First-Party Details
)
The integration details for PayPal first party REST endpoints.
third_party_details
object
(
REST Third-Party Details
)
The integration details for PayPal REST endpoints.
Copy
Expand all
Collapse all
{
"integration_method"
:
"PAYPAL"
,
"integration_channel"
:
"string"
,
"integration_type"
:
"FIRST_PARTY"
,
"first_party_details"
:
{
"features"
:
[
"PAYOUTS"
]
,
"seller_nonce"
:
"stringstringstringstringstringstringstringst"
}
,
"third_party_details"
:
{
"features"
:
[
"PAYOUTS"
]
,
"signup_mode"
:
"string"
,
"organization"
:
"string"
}
}
rest_endpoint_feature
The REST endpoint.
string
(
rest_endpoint_feature
)
[ 1 .. 100 ] characters
^[0-9A-Z_-]+$
The REST endpoint.
Enum Value
Description
PAYOUTS
Payout feature.
PAYMENT
Payment feature.
REFUND
Refund feature.
FUTURE_PAYMENT
Future Payment feature.
DIRECT_PAYMENT
Direct Payment feature.
PARTNER_FEE
Partner fee feature.
DELAY_FUNDS_DISBURSEMENT
Delay funds disbursement feature.
READ_SELLER_DISPUTE
Read seller dispute feature.
UPDATE_SELLER_DISPUTE
update seller dispute feature.
ADVANCED_TRANSACTIONS_SEARCH
Advanced transaction search feature.
SWEEP_FUNDS_EXTERNAL_SINK
Sweep funds external sink feature.
ACCESS_MERCHANT_INFORMATION
Access merchant information feature.
TRACKING_SHIPMENT_READWRITE
Tracking Shipment readwrite feature.
INVOICE_READ_WRITE
Invoice readwrite feature.
DISPUTE_READ_BUYER
Read the buyer disputes.
UPDATE_CUSTOMER_DISPUTES
Update the buyer disputes.
VAULT
Manage the payment methods that my customers save.
BILLING_AGREEMENT
Obtain prior approval for future payments(billing agreements).
USER_PROFILE
Read and update business and user information.
PAYPAL_BALANCE
Read the merchant balance amount.
EXCHANGE_CURRENCY
Read the exchange currency rate for withdraw.
SCREEN_CONTENT
Allow user to screen media/text content.
SCREEN_CONTENT_DECISIONS
Fetch content moderation results.
MEDIA_INVALIDATE_CACHE_READWRITE
Invalidate media cache.
MEDIA_DIGITALASSETS_READWRITE
Allows uploading and searching of media.
MEDIA_DIGITALASSETS_DELETE
Allows deleting media.
COMMERCE_ADMIN
Permission to perform administrative functions using Commerce Admin APIs to manage store.
Copy
"PAYOUTS"
Role type
Role of the person party played in the business.
string
(
Role type
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Role of the person party played in the business.
Enum Value
Description
CEO
The ceo.
CHAIRMAN
The chairman.
DIRECTOR
Director of the business
SECRETARY
The secretary.
TREASURER
The treasurer.
TRUSTEE
The trustee.
Copy
"CEO"
sign up mode
Signup Mode to be used for sellers for third party integration.
string
(
sign up mode
)
[ 1 .. 255 ] characters
Signup Mode to be used for sellers for third party integration.
Copy
"string"
The business name type.
Business name type
string
(
The business name type.
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Business name type
Enum Value
Description
DOING_BUSINESS_AS
The trading name of the business.
LEGAL_NAME
The legal name of the business.
Copy
"DOING_BUSINESS_AS"
The business sub type.
Sub classification of the business type
string
(
The business sub type.
)
[ 1 .. 255 ] characters
^[0-9A-Z_]+$
Sub classification of the business type
Enum Value
Description
ASSO_TYPE_INCORPORATED
The asso type incorporated.
ASSO_TYPE_NON_INCORPORATED
The asso type non incorporated.
GOVT_TYPE_ENTITY
The govt type entity.
GOVT_TYPE_EMANATION
The govt type emanation.
GOVT_TYPE_ESTD_COMM
The govt type estd comm.
GOVT_TYPE_ESTD_FC
The govt type estd fc.
GOVT_TYPE_ESTD_ST_TR
The govt type estd st tr.
Copy
"ASSO_TYPE_INCORPORATED"
version
Represents the version object of the consent.
major
required
integer
[ 0 .. 500 ]
Major version of the consent.
minor
required
integer
[ 0 .. 500 ]
Minor version of the consent.
url
string
<
uri
>
[ 1 .. 2048 ] characters
The URL that point to the document or agreement containing the text of the particular version of consent accepted by the subject entity.
activation_time
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
This is the date and time when the version got/gets activated. Before this time the version is not active and should not be used for any decision making.
Copy
{
"major"
:
500
,
"minor"
:
500
,
"url"
:
"
http://example.com
"
,
"activation_time"
:
"string"
}
