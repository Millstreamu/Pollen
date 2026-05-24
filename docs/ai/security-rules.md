# Security Rules

These generic rules do not replace a professional security review for high-risk systems.

## Managed Security First
Prefer managed systems for auth, password reset, OAuth, sessions, payments, and secrets. Do not invent password hashing, token formats, encryption, auth protocols, or payment flows unless explicitly required and reviewed.

## Server Trust Rule
Never trust frontend-provided `user_id`, `account_id`, `workspace_id`, `role`, `isAdmin`, prices, permissions, ownership, or calculated totals. The server derives identity and permissions from trusted session/data.

## Ownership Checks
Private records must be fetched/modified with ownership constraints, not by ID alone.

## Secrets
Never expose secrets in frontend code, logs, screenshots, reports, or committed files. Do not commit real `.env` files, service role keys, OAuth secrets, database passwords, or API tokens.

## Destructive Actions
Require auth, ownership, validation, logging where important, and soft delete/archive where practical.

## Input Validation
Validate server-side: required fields, types, allowed values, ownership, permissions, state transitions, numeric ranges, file types/sizes.

## High-Risk Areas
Auth, permissions, payments, health/legal/private data, file uploads, external write-back, destructive bulk actions, admin panels, background jobs. Require explicit scope, tests, and verification.
