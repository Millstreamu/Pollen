# Testing Rules

Testing protects the product from confident-looking broken code.

## Test Levels

- Unit tests: calculations, validators, parsers, status logic, helpers.
- Service/integration tests: workflows, database updates, state transitions, permissions, transactions.
- Journey tests: user workflows from start to expected outcome.
- UI/screenshot tests: layout, responsive behaviour, visual regressions, empty states.
- Live smoke tests: OAuth, webhooks, external APIs, deployed checks in supported environments only.

## Risk-Based Testing

| Risk | Examples | Required Testing |
|---|---|---|
| Low | copy/styling | typecheck/build if available |
| Normal | CRUD/screens | unit/service tests where practical |
| Business critical | inventory, money, permissions, destructive actions | regression + service/integration tests |
| External integration | APIs, OAuth, webhooks | mocked tests + environment-specific smoke steps |
| Release | milestone closeout | full verification command + report |

## Regression Rule
A bug fix should include a regression test/check or a documented reason why it is not practical.

## Journey Rule
If a feature changes a user workflow, add or update a journey test where practical. A journey test proves the user can complete the workflow and expected state changes occur.

## Environment Honesty
Do not claim a test ran if it did not. If blocked by environment, run closest mocked/local check and document verification steps for the correct environment.

## Suggested Commands
Adapt to project stack:

```bash
npm run typecheck
npm run lint
npm run test
npm run test:journeys
npm run build
npm run check:no-debug
```

or:

```bash
make check
make verify
```
