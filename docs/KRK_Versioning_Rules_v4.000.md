# Versioning and Release Packaging Rules (v4.000)

## Goals
- Deterministic history of changes.
- Each deployed change is uniquely identifiable.
- **Strict increments of 0.001** for every release.

## Scheme
- **Strict Format**: `vX.YYY` (e.g., `v4.000`, `v4.001`, `v4.002`).
- **Prohibited**:
    - No "A/B" suffixes (e.g., `v4.000-A`).
    - No dash suffixes (e.g., `v4.000-1`).
    - No variations.

## Operational Rules
1.  **Strict Increment**: Every GitHub push / release MUST increment the version by **0.001**.
    - `v4.000` -> `v4.001` -> `v4.002`.
2.  **Single Source of Truth**: `APP_VERSION` in the code is the master.
3.  **Display**: The version must appear identically in:
    - The Application Header (top-left).
    - The Trace Log (first line).

## Patch Delivery
- Each deliverable must include:
    - One updated HTML file (`Kraken Ledger Report.html`).
    - One repo-root command block (`cp`, `git add`, `git commit`, `git push`).
