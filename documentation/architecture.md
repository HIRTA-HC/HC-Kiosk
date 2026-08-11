# Architecture

## Overview

```
┌─────────────────┐        ┌──────────────────────┐        ┌───────────────────────┐
│  Kiosk hardware  │        │   CloudFront + S3     │        │   Cognito User Pool    │
│  (touchscreen,   │──────▶│   (Angular frontend)  │───────▶│   (login + API auth)  │
│  browser kiosk   │        └──────────────────────┘        └───────────────────────┘
│  mode)           │                    │
└──────────────────┘                    ▼
                              ┌──────────────────────┐
                              │     API Gateway        │
                              │  (Cognito authorizer)  │
                              └──────────────────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐        ┌───────────────────────┐
                              │   Lambda handlers      │──────▶│  DynamoDB              │
                              │  (health_connector.py) │        │  Kiosk_MOD_Medicaid   │
                              └──────────────────────┘        │  Kiosk_MOD_Medicaid_History │
                                         │                     └───────────────────────┘
                                         ▼
                              ┌──────────────────────┐
                              │  Via Trip API          │
                              │  (ride booking/status) │
                              └──────────────────────┘
                                         ▲
                              ┌──────────────────────┐
                              │  Secrets Manager       │
                              │  (Via API credentials) │
                              └──────────────────────┘
```

## Components

- **Frontend (Angular)** — the kiosk UI. Built with Angular 16 + PrimeNG, deployed as static
  assets to an S3 bucket fronted by CloudFront. See [frontend.md](frontend.md).
- **API Gateway** — a single REST API (`kiosk_health_connector`) fronting the Lambda handlers.
  Routes are protected by a Cognito User Pool authorizer, except the OAuth token proxy endpoint.
- **Lambda (`health_connector.py`)** — the active backend handler. Receives booking/status/detail
  requests from the kiosk, calls the Via Trip API, and records trips in DynamoDB. See
  [backend.md](backend.md).
- **Cognito** — one User Pool provides both kiosk operator login (authorization-code / implicit
  grant) and machine-to-machine API clients (client-credentials grant) for partner integrations.
- **DynamoDB** — two tables store trip requests and trip history, keyed by `atms_ride_id`.
- **Secrets Manager** — holds the Via API credentials (`<env>_credentials` secret) that the Lambda
  reads at runtime.
- **CDK (`health_connector_cdk/`)** — defines and deploys all of the above as a single stack,
  parameterized per environment (dev/uat/prod). See [deployment.md](deployment.md).

## Request flow (booking a trip)

1. Rider authenticates on the kiosk (Cognito login / lock screen).
2. Rider walks through the booking steps in the Angular app (pickup → destination → confirm).
3. The frontend calls `POST /kiosk_request` with the trip payload.
4. The Lambda handler calls the Via Trip API to book the ride and writes a record to DynamoDB.
5. The frontend polls `POST /kiosk_request_detail` / `POST /connector_status` for trip status
   updates, which the Lambda proxies from Via.

## Notes on legacy code

- `lambda/flask_app.py` and `lambda/datastore.py` are a legacy standalone Flask/SQLite
  implementation kept for reference; they are **not** deployed by the current CDK stack and are
  out of scope for this documentation.
- Several routes and a "dashboard" Lambda are defined but commented out in the CDK stack — they
  represent deprecated or not-yet-active integrations (Lyft TAPI, MOD-EHR dashboard).
