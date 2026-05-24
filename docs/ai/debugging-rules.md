# Debugging Rules

Humans report symptoms. AI owns reproduction, diagnosis, repair, verification, cleanup, and documentation.

## No Human-Assisted Debugging

The human may provide observed behaviour, expected behaviour, screenshots/logs already available, reproduction steps if known, and product-behaviour clarification.

The AI must not ask the human to run commands, inspect files, paste snippets, check the database, test hypotheses, confirm terminal output, or try code changes manually.

## Debugging Loop

1. Read bug report and relevant rules.
2. Read latest evidence reports if they exist.
3. Inspect relevant code.
4. Reproduce where practical.
5. Add failing test or diagnostic if useful.
6. Identify root cause.
7. Fix the smallest root cause.
8. Add regression coverage where practical.
9. Remove temporary diagnostics.
10. Run verification.
11. Write/update debug report.
12. Update bug plan/progress/known issues as needed.

## No Random Fixes
Do not apply unrelated changes hoping one works. If unclear, add targeted logs/assertions, reproduction scripts, focused tests, or data-flow tracing.

## Reproduction Requirement
A bug fix should include at least one: failing unit test, service/integration test, journey test, UI/screenshot test, diagnostic reproduction script, or documented reason reproduction is not practical.

## Bug Plans
For multi-step bugs, create a bug plan from `docs/ai/templates/bugfix-plan-template.md` in `docs/ai/bugfix-plans/active/`. Implement one milestone at a time.
