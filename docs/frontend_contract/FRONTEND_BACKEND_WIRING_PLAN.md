# Frontend Backend Wiring Plan

This plan describes a later backend integration. It is not implemented in the current audit task.

## Current Demo-Data Path

Current public build behavior:

1. Route loaders in `src/routes/*.tsx` call query option factories from `src/lib/traceops/queries.ts`.
2. `queries.ts` calls methods on `traceops` from `src/lib/traceops/client.ts`.
3. `client.ts` returns bundled demo objects from `src/lib/traceops/demo-data.ts`.
4. `src/lib/traceops/types.ts` defines the read models consumed by the UI.
5. `src/lib/traceops/demo-mode.ts` forces `isPublicDemoMode = true` and provides public-safe demo slugs and banner text.

There is no API base URL, no backend `fetch()` path, and no environment-driven backend switch today. `isUsingMockBackend` is always true.

## Later Backend Mode

Backend mode should be opt-in. The public build should continue using bundled demo data unless explicit environment variables enable backend reads.

Recommended behavior:

- Default: demo mode, no backend calls.
- Backend mode: only enabled when both an explicit mode flag and a base URL are present.
- Public/demo safety: even when a backend exists, public demo deployments should request public-safe data or keep using local demo data.

Recommended client decision:

```ts
const backendEnabled =
  import.meta.env.VITE_TRACEOPS_DATA_MODE === "backend" &&
  Boolean(import.meta.env.VITE_TRACEOPS_API_BASE_URL);
```

## Required Env Vars

Suggested future variables:

- `VITE_TRACEOPS_DATA_MODE`: `demo` or `backend`; defaults to `demo`.
- `VITE_TRACEOPS_API_BASE_URL`: base URL for FastAPI, for example `http://localhost:8000`.
- `VITE_TRACEOPS_PUBLIC_DEMO`: `true` or `false`; defaults to `true` for public builds.

Optional later variables:

- `VITE_TRACEOPS_API_TIMEOUT_MS`: client-side timeout for read requests.
- `VITE_TRACEOPS_DEMO_TENANT`: public demo tenant or profile if the backend serves multiple safe demo datasets.

Do not add auth tokens to Vite-exposed env vars. Any future private/authenticated mode needs a separate security design because `VITE_*` values are exposed to the browser bundle.

## Fallback Behavior

Recommended fallback rules:

- If `VITE_TRACEOPS_DATA_MODE` is absent or `demo`, use bundled demo data.
- If `VITE_TRACEOPS_DATA_MODE=backend` but `VITE_TRACEOPS_API_BASE_URL` is missing, fail closed to demo data and keep the public-safe banner.
- If backend requests fail in a public demo deployment, fallback to bundled demo data and show mock/demo status.
- If backend requests fail in a private deployment, prefer a visible load error over silently mixing private and demo data, unless product requirements explicitly allow fallback.

Avoid partial mixed state. For example, do not show backend applications with local demo evidence unless that is deliberately designed and labeled.

## Safety Rules

Future wiring must preserve these rules:

- Do not add real company names in public mode.
- Do not add recruiter names in public mode.
- Do not add private interview details or exact private dates in public mode.
- Do not add private slugs in public mode.
- Do not remove public-safe demo mode as the default.
- Do not make backend API calls by default.
- Do not invent production claims.
- Do not push to `main`.
- Do not derive policy, classification, risk, or safe-claim state in React.
- Keep blocked evidence from being used in safe talking points.

## Files Likely Needing Edits Later

Likely integration files:

- `src/lib/traceops/client.ts`: add backend/demo client switch and `fetch` helpers.
- `src/lib/traceops/queries.ts`: likely unchanged unless query keys need mode or tenant scoping.
- `src/lib/traceops/types.ts`: keep aligned with FastAPI response models.
- `src/lib/traceops/demo-mode.ts`: make public demo mode env-aware only after safety requirements are finalized.
- `src/components/app-sidebar.tsx`: render backend/demo status from the selected client mode.
- `src/components/app-shell.tsx`: keep public-safe banner behavior explicit.
- `src/routes/*.tsx`: should need little or no change if API responses match `docs/API_CONTRACT_FROM_UI.md`.

Supporting files that may need later updates:

- `vite.config.ts`: only if env handling or dev proxying is needed.
- `scripts/scan-public-safety.ts`: extend checks if backend-mode fixtures or generated artifacts are added.
- `.env.example`: document required backend-mode env vars when wiring starts.

## Suggested Implementation Sequence Later

1. Add `.env.example` with safe defaults.
2. Add a small API fetch wrapper in `src/lib/traceops/client.ts`.
3. Keep existing demo methods as fallback/default.
4. Implement one endpoint at a time against the contract.
5. Add runtime validation before trusting backend responses.
6. Verify public mode performs no backend requests.
7. Verify private/backend mode does not display demo labels unless intentionally configured.
