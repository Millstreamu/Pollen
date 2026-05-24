# Reporting Rules

Reports make test output and decisions durable for future AI sessions.

## Common Reports
- `docs/ai/reports/latest-check.md`
- `docs/ai/reports/latest-server-run.md`
- `docs/ai/reports/latest-failures.md`
- `docs/ai/reports/known-environment-exceptions.md`
- `docs/ai/reports/debug/<bug>.md`

## Good Reports Include
Date/time, branch/commit if known, commands run, pass/fail summary, important failures, likely affected area, environment limitations, next recommended action.

## Avoid Committing
Huge raw logs without summary, binary artifacts, secrets, sensitive data, noisy generated files, or screenshots with private data.

## Rule
If a latest failure report exists, read it before debugging. Evidence beats guesses.
