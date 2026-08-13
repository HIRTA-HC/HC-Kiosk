# Kiosk

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Kiosk</h3>

  <p align="center">
    Documentation for Health Connector's kiosk can be found in the repository's <a href="https://github.com/HIRTA-HC/HC-Kiosk/wiki"><strong>Wiki Page»</strong></a>.
    <br />
    <a href="https://github.com/HIRTA-HC/HC-Kiosk"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>

# HIRTA Health Connector Kiosk — Documentation

The Health Connector Kiosk is a touch-screen kiosk application that lets riders book and check
non-emergency medical transportation trips through HIRTA. It runs on an Angular frontend served from S3/CloudFront, backed by an AWS
Lambda + API Gateway + DynamoDB stack.

## Contents

- [Architecture](architecture.md) — how the pieces fit together
- [Setup](setup.md) — get a local dev environment running
- [Deployment](deployment.md) — deploy the CDK stack and publish the frontend
- [Frontend](frontend.md) — Angular app structure and key flows
- [Backend](backend.md) — Lambda handlers, API routes, and data storage
- [User Guide](user-guide/README.md) — how kiosk operators and riders use the app

## Repo layout

| Path | Purpose |
|---|---|
| `frontend/` | Angular kiosk UI |
| `lambda/` | Backend Lambda source (`health_connector.py` is the active handler) |
| `health_connector_cdk/` | AWS CDK stack definition |
| `app.py` | CDK app entry point / environment selection |
| `website/dist/` | Built frontend assets staged for S3 deployment |
| `Kiosk_setup.txt` | Original raw setup notes (superseded by [setup.md](setup.md)) |

