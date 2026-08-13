# Deployment

The app deploys as a single CDK stack (`HealthConnectorKioskCdkStack`) that provisions the API,
Lambda functions, DynamoDB tables, Cognito User Pool, and the S3/CloudFront-hosted frontend.

## Environments

The environment is chosen in [app.py](../app.py) via `env_name` (`dev`, `uat`, `prod`) plus the
AWS account/region for that environment. Only one environment block should be active at a time —
comment/uncomment as needed before deploying.

## Backend deploy

```
cdk bootstrap   # once per account/region
cdk deploy
```

This provisions (see [architecture.md](architecture.md) for details):

- API Gateway (`kiosk_health_connector`, stage `prod`)
- Lambda handlers (`health_connector.api_handler`, `health_connector.lambda_kiosk_status`)
- DynamoDB tables (`Kiosk_MOD_Medicaid`, `Kiosk_MOD_Medicaid_History`)
- Cognito User Pool, domain, and app clients
- S3 bucket + CloudFront distribution for the frontend

After deploying, note the outputs you'll need for the frontend config: the API Gateway URL,
Cognito User Pool ID, and Cognito App Client ID.

## Frontend build & publish

The frontend is built locally/CI and pushed into the S3 bucket via the CDK `BucketDeployment`
construct, which reads from `website/dist`.

1. Build and stage the frontend:

   ```
   .\move-dist.bat
   ```

   This builds the Angular app and copies the output into `website/dist`.

2. Re-deploy the stack so the `BucketDeployment` picks up the new files:

   ```
   cdk deploy
   ```

> On a brand-new environment, `website/` won't exist yet — see step 5 in
> [setup.md](setup.md) for the first-deploy workaround (empty folder + temporarily disabling the
> bucket deployment).

## Updating environment config after a redeploy

If a redeploy changes the API Gateway URL, Cognito pool/client IDs, or region, update
`frontend/src/environments/environment.txt` accordingly and rebuild/republish the frontend
(steps above).
