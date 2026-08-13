# Frontend

Angular 16 single-page app (PrimeNG UI, ngx-translate for i18n) that runs in kiosk mode on a
touchscreen device.

## Structure

```
frontend/src/app/
├── app.module.ts             # root module
├── app-routing.module.ts     # route table (see below)
├── core/
│   ├── guards/                # AppAuthGuard — protects the booking flow
│   ├── services/
│   │   ├── app.auth.service.ts        # Cognito login/session handling
│   │   ├── app.data.service.ts        # calls to the backend API (kiosk_request, etc.)
│   │   ├── app.interceptor.service.ts # attaches auth headers to outgoing requests
│   │   ├── app.ticketservice.service.ts
│   │   ├── app.speech.service.ts      # text-to-speech / accessibility
│   │   ├── app.notifications.service.ts
│   │   ├── timeout.service.ts         # idle/inactivity handling (kiosk "are you still there?")
│   │   ├── google-maps-api.service.ts
│   │   └── google-analytics.service.ts
│   └── config/                # HTTP options, app-level config
├── layout/
│   ├── app.layout.component.*        # shell layout for the authenticated flow
│   ├── app.login/                    # login screen
│   ├── app.topbar/
│   ├── lockscreen/                   # kiosk lock screen
│   └── app.steps/                    # the booking wizard
│       ├── account-book-trip/
│       ├── destination/
│       ├── pickup/
│       └── account-check-trip/
├── directive/ngx-touch-keyboard/     # on-screen keyboard for kiosk touch input
├── shared/                           # shared models, pipes, module
└── assets/
    ├── i18n/ (en.json, es.json)      # translations
    └── images/
```

## Routes

| Path | Component | Notes |
|---|---|---|
| `/login` | `AppLoginComponent` | Cognito login |
| `/cognito-login` | `CognitoCallbackComponent` | OAuth redirect handler |
| `/lockscreen` | `LockscreenComponent` | Kiosk lock/idle screen |
| `/account-book-trip` | `AccountBookTripComponent` | Booking flow, step 1 (behind `AppAuthGuard`) |
| `/destination` | `DestinationComponent` | Booking flow, step 2 |
| `/pickup` | `PickupComponent` | Booking flow, step 3 |
| `/account-check-trip` | `AccountCheckTripComponent` | Check status of an existing trip |

Routes under the root layout are protected by `AppAuthGuard`; unmatched paths redirect to `/`.

## Talking to the backend

`app.data.service.ts` wraps the three API calls the kiosk makes (all POST, relative to
`environment.api_url` — see [backend.md](backend.md) for what each does):

- `kiosk_request` — book a trip
- `kiosk_request_detail` — get details for a booked trip
- `connector_status` — check trip status

`app.interceptor.service.ts` attaches the Cognito auth token to these requests.

## Environment configuration

Each deploy target needs `frontend/src/environments/environment.txt` (see
`environment_sample.txt` for the template), which includes:

- `api_url` — the API Gateway base URL
- `cognito_client_id`, `cognito_user_pool_id`, `cognito_token_use` — auth config
- `google_maps_api_key`, map bounding box (`southwestLat/Lng`, `northeastLat/Lng`) — used to
  restrict the pickup/destination map to the service area
- `kiosk_lat` / `kiosk_lng` / `kiosk_address` / `trip_origin` — the physical kiosk's location
- `user_max_time` / `user_max_time_warn` — idle timeout behavior (lock screen prompts)

## Build

```
cd frontend
npm install
npm run build      # ng build
npm start          # ng serve, for local dev
```

`move-dist.bat` (repo root) builds the app and copies the output into `website/dist` for
deployment — see [deployment.md](deployment.md).
