# Safety-Critical Rules

Use for code that can corrupt important data, expose private data, affect money, trigger external actions, or perform destructive operations.

## Service Layer Rule
Risky data-changing workflows go through explicit backend/service functions. Do not scatter critical state changes across UI components or route handlers.

## Transaction Rule
If a workflow changes multiple related records, perform it atomically where supported. Either all changes succeed or none do.

## Audit Rule
Important state changes should create traceable records where applicable: activity log, audit log, movement record, payment event, sync event, job log.

## Duplicate Action Rule
Prevent double processing: completing twice, receiving twice, charging twice, importing same external record twice, double-click/retry issues. Use state checks or idempotency keys where appropriate.

## Failure Rule
Consider validation failure, external API failure, job retry, double click, partial success, and rollback.

## Required Tests
Success, invalid input, permission/ownership failure, duplicate prevention, rollback where applicable, and audit/log records where applicable.

## No Hidden Automation
Do not silently send money, order goods, update external systems, delete data, email customers, publish content, or change live stock/prices unless explicitly scoped and protected.
