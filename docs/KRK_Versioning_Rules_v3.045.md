# Versioning and Release Packaging Rules

## Goals
- Deterministic history of small changes.
- Each deployed change is uniquely identifiable.
- Bug-fix iterations do not consume main version numbers unnecessarily.

## Scheme
- Main feature releases: v3.044, v3.045, v3.046, ...
- Bug-fix subreleases: v3.044-1, v3.044-2, v3.044-3, ...

## When to use subreleases
- A defect is found after deploying v3.044, but the change scope remains the same feature set.
- Multiple quick iterations required to stabilise the same release.

## When to advance main version
- A new feature or functional requirement is introduced after stabilising the prior version.

## Operational rules
- Every GitHub push increments version (main or subrelease).
- `APP_VERSION` is the single source of truth; header and trace must display the same value.
- Each patch deliverable must include:
  - One updated HTML file.
  - One repo-root command block with cp + git add/commit/push.


## Patch version increments
- Each deployed patch increments the visible app version by **0.001** (example: 3.044 → 3.045).
- The same version must be updated in:
  - The header label (top-left).
  - The first line of the trace banner (for copied logs).
