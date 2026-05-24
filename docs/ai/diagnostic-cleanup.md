# Diagnostic Cleanup Rules

Diagnostics are allowed. Debug junk is not.

## Temporary Diagnostics To Remove
- `console.log`, `console.dir`, print debugging
- `debugger`
- temporary trace output
- scratch scripts
- commented-out experiments
- hardcoded debug values
- temporary bypasses
- debug-only UI text
- raw dump files
- files named `tmp-*`, `debug-*`, or `scratch-*` unless approved

## Permanent Diagnostics That May Stay
- structured error logs
- audit/activity records
- health checks
- diagnostic commands
- regression tests
- fixtures
- environment exception reports
- server-run summaries

## Promote or Remove
If only useful for this bug, remove it. If useful for future support, promote it into a documented diagnostic tool.

## Cleanup Checklist
- [ ] Removed temporary logs
- [ ] Removed scratch scripts
- [ ] Removed commented experiments
- [ ] Removed temporary bypasses
- [ ] Removed debug-only UI
- [ ] Kept only intentional permanent diagnostics
- [ ] Added regression test where practical
- [ ] Updated debug report
