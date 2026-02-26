# Kraken Report Version Baselines for Google Jules

To resolve the recent dramatic increases in statement discrepancy, we have identified three distinct versions of the Kraken Ledger Report application. The discrepancy calculations were functioning perfectly before a targeted effort to fix "Bank Labels" inadvertently broke the logic.

Jules should compare the calculation logic of the current version against the low-discrepancy baseline to identify exactly where the math diverged.

## The 3 Reference Versions

### 1. The Lowest Discrepancy Baseline (The Calculations Blueprint)
* **Version**: `v4.00-52` (and `v4.00-50`)
* **Last Functional Commit**: `25fee0d6bacf7618f15a39b47ba1bc8b4336490b` (Fix v4.00-52: Clean Code Leak)
* **Preceding Validated Commit**: `4bb43f61c897c344662573068004312434f0e9cb` (Deploy v4.00-50: Full Bank Alignment (Validated))
* **Context**: The user continued working past the v3.x series directly on fixing the discrepancy. At `v4.00-50` through `v4.00-52`, the discrepancy logic reached its optimal state ("Full Bank Alignment ... Validated"). **This version's calculation logic must be treated as the mathematical gold standard.** The discrepancy began increasing dramatically immediately *after* this era, when the user initiated the "Bank Label Normalisation" phase (which restarted versioning at `v4.00-01`).

### 2. The Accountant Submission Version
* **Version**: `v3.045-18.11`
* **Commit**: `aaa65b141bdcdf28906eb2f0a6be84bac7636026` (Simplify Reconciliation Footer Text)
* **Context**: This is an older baseline version that was generated into a PDF on Jan 28, 2026, and given to the company accountant. It is satisfactory as a fallback, but does not include the final UI alignments and strict bank UI deposit aggregations perfected in `v4.00-52`.

### 3. The Current Version (Painted into a corner)
* **Version**: `v4.00-13-xx` (Current `HEAD`)
* **Context**: Starting with `v4.00-01`, the user focused exclusively on fixing the "Bank Labels" (Objective D). During this process, they got painted into a corner, and the discrepancy increased dramatically. While this version contains vital bank label bug fixes, its reconciliation logic has strayed from the accurate baseline established in `v4.00-52`.

## Directive for Jules
1. **Diff the Calculation Logic**: Compare `v4.00-52` (`25fee0d`) against Current `HEAD`. Pay close attention to `generateStatementSummary`, trade exclusion/inclusion logic, row-level FX conversions, and the `calculateGbpValue` functions.
2. **Isolate the Regression**: Identify which edits from the label normalisation phase (`v4.00-01` through `v4.00-13`) broke the accurate "Net Trade Activity" valuation and deposit summations.
3. **Merge**: Port the pristine mathematical logic from `v4.00-52` into the current `v4.00-13` architecture seamlessly, retaining the recent Bank Label fixes (Objective D) without disrupting the math.
