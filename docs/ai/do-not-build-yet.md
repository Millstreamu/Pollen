# Deferred Work / Do Not Build Yet

Deferred work is intentionally blocked, delayed, or awaiting prerequisites.

## Status Values
- `blocked`: Do not build.
- `deferred`: Not current milestone.
- `candidate`: May be planned soon, but not buildable.
- `unlocked`: Can be built if a scoped issue exists.
- `in-progress`: Currently being built.
- `done`: Completed.

## Unlock Rule
Codex may work on an item only when status is `unlocked` or `in-progress`, the current task explicitly scopes it, unlock conditions are satisfied or waived in a decision record, and acceptance criteria define the allowed version.

If Codex thinks an item should be unlocked, suggest an unlock issue. Do not implement it.

## Deferred Item Template

```md
## <Feature Name>

Status: deferred  
Earliest milestone: Post-V1  
Current rule: Do not build.

### Why deferred
...

### Unlock conditions
- [ ] condition one
- [ ] condition two

### First allowed version
...

### Still not allowed
...
```

## Current Deferred Items

Add project-specific deferred items here.
