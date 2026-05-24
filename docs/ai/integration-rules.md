# Integration Rules

For APIs, OAuth, webhooks, external services, third-party platforms, and background sync.

## Mock First
1. Define internal data model.
2. Create fixtures.
3. Build parser/mapper tests.
4. Build service using fake/mock client.
5. Test errors/retries/duplicates.
6. Add real client.
7. Verify live behaviour only in supported environment.

## External Data Is Untrusted
Handle missing fields, unknown statuses, duplicates, partial responses, changed schemas, API errors, rate limits, auth failures, and timeouts.

## Store External IDs
Store provider/source, external ID, external updated timestamp if useful, sync status, and last sync result. Use uniqueness constraints where possible.

## No Silent Write-Back
Do not write to external systems automatically unless explicitly scoped. Prefer import → review → apply manually → log result.

## Job/Sync Logs
External integration actions should log job type, provider, status, attempts, error, started/completed timestamps, affected records.

## Environment Limits
If live test is blocked, use fixtures/mocks, write environment exception, and provide Codespace/CI/manual steps. Do not claim full live verification.
