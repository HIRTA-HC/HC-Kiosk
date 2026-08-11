# Local Development Setup

## Prerequisites

- Python 3.12
- Node.js and npm
- [Angular CLI](https://angular.io/cli) (`npm install -g @angular/cli`)
- Docker (required for CDK to bundle the Lambda dependencies)
- AWS CLI, configured with credentials that have access to the target account
  (`aws configure`)

## 1. Clone and open the project

```
git clone <repo-url>
cd HC-Kiosk
```

## 2. Backend / CDK environment

Create and activate a virtual environment, then install dependencies:

```
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

In [app.py](../app.py), set the AWS account ID, region, and `env_name` (`dev`, `uat`, or `prod`)
for the environment you're deploying to.

## 3. Secrets

Create a secret named `<env>_credentials` in AWS Secrets Manager (matching the `env_name` used in
`app.py`) containing:

- `via_auth_url`
- `via_client_id`
- `via_client_secret`
- `via_api_key`
- `via_api_url`

## 4. Frontend dependencies

```
cd frontend
npm install
```

## 5. First-time deploy bootstrap

The CDK stack deploys the frontend build output from `website/dist`. On a brand-new environment
that folder won't exist yet, so for the *first* deploy:

1. Create an empty `website/` folder at the repo root if it doesn't already exist.
2. Comment out the S3 bucket deployment step in
   [health_connector_cdk_stack.py](../health_connector_cdk/health_connector_cdk_stack.py) so the
   stack can deploy without frontend assets.

See [deployment.md](deployment.md) for the full deploy sequence, including how to build the
frontend and re-enable the bucket deployment afterward.

## 6. Frontend environment config

After the backend stack is deployed, create
`frontend/src/environments/environment.txt` (or the appropriate `environment.*.ts` file) based on
`environment_sample.txt`, filling in the values produced by the deploy (API Gateway URL, Cognito
User Pool ID/Client ID, region, etc.).

## 7. Create a kiosk operator user

Create a user in the Cognito User Pool via the AWS Console or CLI. New users start in a
`FORCE_CHANGE_PASSWORD` state — set a permanent password with:

```
aws cognito-idp admin-set-user-password --user-pool-id <user_pool_id> --username <username> --password <new_password> --permanent
```

## Next steps

- [deployment.md](deployment.md) — build and deploy the frontend and backend stack
- [frontend.md](frontend.md) / [backend.md](backend.md) — understand the app structure
