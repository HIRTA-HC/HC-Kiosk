# Backend

The active backend is a single Lambda source tree (`lambda/`), deployed by the CDK stack in
[health_connector_cdk_stack.py](../health_connector_cdk/health_connector_cdk_stack.py).

> `lambda/flask_app.py` and `lambda/datastore.py` are a legacy standalone Flask/SQLite
> implementation and are not deployed — they're not covered here.

## Lambda functions

| CDK construct | Handler | Purpose |
|---|---|---|
| `HealthConnectorKioskApiHandler` | `health_connector.api_handler` | Main request router — booking, trip details |
| `HealthConnectorKioskStatus` | `health_connector.lambda_kiosk_status` | Trip status checks (delegates to `api_handler`) |

Both share the same code and DynamoDB table access; they're split into separate Lambdas mainly to
give the status-check path its own timeout budget (10 minutes vs. 1 minute for the primary
handler).

## API routes

All routes below sit behind the API Gateway Cognito authorizer except the OAuth token proxy.

| Route | Method | Handler logic |
|---|---|---|
| `/oauth2/token` | POST | Proxies directly to the Cognito User Pool's `/oauth2/token` endpoint |
| `/kiosk_request` | POST | Books a trip via the Via Trip API, records it in DynamoDB |
| `/kiosk_request_detail` | POST | Fetches details for a given `trip_id` from Via |
| `/connector_status` | POST | Checks trip status via Via |

`health_connector.api_handler` dispatches on `event['requestContext']['resourcePath']` — see
[health_connector.py](../lambda/health_connector.py) for the full switch. A few routes
(`/v1/tapi/*`, `/via_webhook`) are legacy/inactive and return `404` or a no-op.

## Data storage

Two DynamoDB tables, both keyed by `atms_ride_id`:

- **`Kiosk_MOD_Medicaid`** — active trip requests.
- **`Kiosk_MOD_Medicaid_History`** — trip history, with a GSI on `update_time` for querying by
  recency.

The Lambda handlers are granted read/write access to both tables via CDK.

## Secrets

The Via API credentials are read from AWS Secrets Manager at runtime (secret name
`<env>_credentials` — see [setup.md](setup.md)):

- `via_auth_url`, `via_client_id`, `via_client_secret`, `via_api_key`, `via_api_url`

The Lambda execution role is granted `secretsmanager:GetSecretValue` /
`secretsmanager:DescribeSecret` on all secrets.

## Auth

A single Cognito User Pool serves two purposes:

- **Kiosk operator / rider login** — authorization-code and implicit grant flows, used by the
  Angular frontend.
- **Machine-to-machine API clients** (`Lyft`, `Pompano`, `Via`) — client-credentials grant, for
  partner integrations that call the API directly.

The API Gateway authorizer validates the `Authorization` header against this pool for all
protected routes.
