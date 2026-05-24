# Development Process

This repo uses an AI-native process:

> Spec → Scan → Simplify → Slice → Verify → Clean → Freeze → Ship

## Spec
Every meaningful task needs goal, user value, scope, out-of-scope, acceptance criteria, tests/checks required, risks, and relevant rule files.

## Scan
Before coding, inspect relevant files, existing patterns, project memory, known issues, deferred work, and latest reports if debugging. Do not code from assumptions.

## Simplify
Ask: what is the simplest safe solution? What is the advanced option? Does this task truly need the advanced option? What is easiest to test and maintain? What can break? What can be deferred?

## Slice
Build one vertical slice: one workflow, one bug, one feature, or one milestone. Do not combine unrelated work.

## Verify
Run appropriate checks. At minimum where available: typecheck, lint, targeted tests, full tests, build. Risky changes need regression/integration/journey tests.

## Clean
Remove temporary debug output, scratch scripts, commented experiments, unused code, and unused dependencies. Keep only intentional permanent diagnostics.

## Freeze
Once acceptance criteria pass, stop feature work. Classify remaining work as required, optional, or deferred.

## Ship
Update progress log, completion status, known issues, decision records, and reports where required. Provide the finish report.

## AI-Native Truths
The repo is memory. The task file is source of truth. Tests are evidence. Reports are evidence. Chat history is not durable context.
