# sf-botmart-integration-sample
A simple example service of developer botmart integration

### Verify Endpoint
`Headers`
> Authorization

`Body`
> {

> "license": "LICENSE_CODE",

> "discord": "DISCORD_ID",

> "secret_key": "YOUR_SECRET_KEY"

> }

`[200] Success Response`
> {

> "require_renewal": RENEWAL_BOOLEAN,

> "expire_datetime": "yyyy-mm-dd hh:mm UTC",

> }

`[401] Unauthorized (Invalid API Key)`
`[404] Not Found (No such license found)`



### Transfer Endpoint
`Headers`
> Authorization

`Body`
> {

> "from_license": "LICENSE_CODE",

> "from_discord": "FROM_DISCORD_ID",

> "to_discord": "TO_DISCORD_ID",

> "otp" : "OPTIONAL_OTP_CODE",

> "secret_key": "YOUR_SECRET_KEY"

> }

`[200] Success Response`
> {

> "license": "NEW_LICENSE_CODE",

> "discord": "TO_DISCORD_ID"

> }

`[401] Unauthorized (Invalid API Key)`
`[404] Not Found (No such license found)`

### Plan Endpoint
`Headers`
> None

`Body`
> None

`[200] Success Reponse`
> {

> "plans" : ["Lifetime", "plan2"]

> }
