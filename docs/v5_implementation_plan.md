# Kraken Reports V5.00:# implementation_plan_v5_roadmap

This plan acts as a collection of bug fixes and enhancements required before a final **v5.00** release. Interim changes are released under the **v4.10-xx** branch.

## Context & Validated Baseline
The V4.10-00 baseline has been validated across the full date range (account open to 22 Feb 2026).
The reconciliation difference across 5.5 years of crypto and fiat activity is **£28.44** — less than 0.5% variance.
This confirms:
* Crypto unit balances are computed with absolute precision.
* The only source of imprecision is the dynamic calculation of **GBP equivalent** values for crypto assets, which are subject to historical FX and trade-rate fluctuations.

### Critical Output Path (for the Accountant)
The two documents that matter are produced in this order:
1. **Kraken Statement** — a bank-statement-style chronological ledger.
2. **Statement Summary** — the final reconciliation summary showing opening/closing balances, fees, trade activity, and the Reconciliation Difference section.

---

## Priority 1: Fiat Deposit Labels
**Context**: The Kraken API provides no originating bank name for fiat deposits — it only returns a generic string. The label must therefore be user-configured at runtime, because:
- When only one source bank exists (e.g., Revolut Ltd), a specific label is accurate and useful.
- When a second bank is introduced (e.g., Santander Business GBP account), using a specific label would be incorrect — the label must fall back to the generic `"Deposit"`.

**Design**:
* Add a new **"Fiat Deposit Label"** control to the existing **API Config** section of the UI.
* Saved to `localStorage` (persisted alongside API keys), loaded on startup.
* The control has two states via a dropdown:
  1. **`Generic ("Deposit")`** — Applied to all fiat deposits. Use when multiple source banks are in the date range.
  2. **`Specific (Enter Own Text)`** — Reveals a free-text input field. User types the exact label (e.g., `Revolut Ltd`, `Santander Business`). Applied uniformly to all fiat deposits in the date range.
* No hard-coded values. The text field is blank by default; the user enters the label manually.
* The GBP equivalent for each deposit is already calculated dynamically. This change is label-only.

**Trigger for switching**: When a Santander Business GBP deposit first appears in a date range alongside Revolut, switch to `Generic`. For historical date ranges with a single known source, use `Specific`.

**Future consideration**: If Google Sheets integration is later added as a data source, bank names could potentially be resolved dynamically from there. This is deferred.

### 1a. Statement Summary Disclaimer Comment (Currency-Only Labels)
When the deposits heading resolves to a currency-only form — i.e. **"Total Deposits (EUR)"** or **"Total Deposits (GBP)"** — it means all fiat deposits for that currency are being summed without distinguishing the originating bank account. In this case a disclaimer note must appear beneath the deposits section in the Statement Summary.

**Design**:
* Detect when the deposit label is of the form `"Total Deposits (EUR)"` or `"Total Deposits (GBP)"` (i.e. no specific bank has been selected; deposits are grouped by currency only).
* Immediately below the deposits subtotal row, render a styled footnote, for example:
  > *Note: Kraken does not record the source bank account for fiat deposits. This must be obtained from the individual Haricom Limited bank account statements (for example, Revolut Business and Santander Business).*
* The note should be visually distinct (italic, muted colour, smaller font) so it reads as a footnote rather than a data row.
* The note must **not** appear when a specific bank account label is active (i.e. the Specific option is selected and a label has been entered), because in that case the source is already identified.

---

## Priority 2: Ledger Extraction Progress Display
**Context**: The `Read Ledger` API call fetches records in batches of 50. For large date ranges (e.g., 100+ records), the user sees only a static "Fetching..." message. The internal trace log already tracks batch progress but it is not surfaced.

**Design**:
* While `readLedger()` is fetching, update the status banner in real time with the current batch position: e.g., `Fetching Ledger... (50 of 111)`.
* On first batch response, the total count becomes known — update immediately.
* On completion of the final batch, display: `Ledger fetch complete (111 of 111)`.
* No new UI elements required — inject into the existing status message.

---

## Priority 3: Summary Dashboard Refactor (Logical Flow)
**Context**: The "Number of Records" summary panel is a disorganised block. It does not reflect the sequence of steps the user follows to produce a report, making it hard to read at a glance.

**Design**: Restructure the flexbox layout to flow **left to right**, matching the production sequence:

| Phase | Label | Values shown |
|-------|-------|--------------|
| 1 — Auth | Addresses | Count of address book entries pulled |
| 2 — Fetch | Ledger Records | Total raw ledger entries read from API |
| 3 — Process | Deposits / Trades / Withdrawals | Fiat deposits · Fiat→Crypto trades · Crypto→Fiat trades · Crypto withdrawals · Fiat withdrawals |
| 4 — Generate | Reports | Record counts for: Statement Report · Trade/Withdrawal Report |

**Additional fix**: Record counts must reset to zero automatically whenever the date range changes, so the display is never stale. Currently this does not happen — old counts persist until a new ledger read completes.

---

## Priority 4: Reconciliation Summary Label Clarity
**Context**: The row label `Calculated Closing` is ambiguous. Users (including accountants) do not immediately understand that this figure is derived through GBP equivalency conversion, or why a small discrepancy exists.

**Design**:
* Rename the row: `Calculated Closing` → `Calculated Closing (GBP equivalent)`
* Update the explanatory sub-text beneath the table to read:
  > *"Crypto asset balances are calculated with absolute unit precision. The Reconciliation Difference arises solely from the dynamic calculation of historical GBP fiat equivalencies for crypto assets, and is not a data error."*
* Add a second dynamically computed line immediately below the above, in this format:
  > *"The reconciliation difference is £[DIFF_AMOUNT], which represents [X.XX]% of the total GBP equivalent calculated (£[TOTAL_GBP])."*
  * `DIFF_AMOUNT` = the absolute value of the Total (GBP) Reconciliation Difference cell.
  * `TOTAL_GBP` = the sum of all GBP equivalent values across the reporting period (i.e., the sum of deposits, withdrawals, trades, and fees as expressed in GBP).
  * `X.XX%` = `(DIFF_AMOUNT / TOTAL_GBP) × 100`, formatted to 2 decimal places.
  * Both amounts formatted as currency (e.g., `£28.44`). The percentage gives immediate context on accuracy.

---

## Priority 5: Collapsible Section Header Bug
**Context**: Some collapsible sections display a redundant second header immediately below the main clickable header, rather than the section's content.

**Design**: Each collapsible section must have exactly one clickable header that reveals the content on click. No duplicate or repeated heading text should appear within the revealed content area.

---

## Priority 6: Duplicate Google OAuth Client ID Field (Cosmetic)
**Context**: In the API Configuration panel, the **"Google OAuth Client ID"** label and input field are rendered twice in succession. On inspection of the HTML, both `<div>` blocks are identical — same `id="googleOAuthClientId"`, same placeholder, same attributes. Because `document.getElementById()` always returns the **first** matching element, the second block is completely unreachable by the save/load JavaScript. The value entered in either field is correctly stored and loaded via the first element. This was previously fixed but appears to have been reverted.

**Design**: Remove the **second** duplicate `<div class="col-md-6">` block (the one that appears below the first) so that exactly one `Google OAuth Client ID` label and input field remains. No JavaScript changes are needed.

---

## Formalized Agent Directives
These rules apply to all future implementation work and must be re-read before any coding session begins.

* **Directive 1 (Strict Scope Adherence)**: Never bundle unsanctioned features or logic changes alongside a requested fix or investigation. If something is not in the scope of the explicit objective, it must not be touched.
* **Directive 2 (Explicit Authorization Required)**: All uncertainties, assumptions, or design questions must halt execution and be raised with the user before any code is written. Internal guessing is not permitted.
* **Directive 3 (Make Mistakes Once)**: Past errors are logged. If a structural mistake is made, execute `git reset --hard` to the last approved commit immediately upon user instruction, rather than manually unpicking changes.
* **Directive 4 (Ask, Don't Assume)**: If the scope of a user request is ambiguous, ask a single, specific clarifying question. Do not attempt to infer intent from context alone.

---

## Known Bugs (Discovered 23 Feb 2026)

### Bug A: "Haricom Bank (GBP)" — Hardcoded Fallback Label
**Symptom**: In any date range containing no fiat (GBP/EUR) withdrawals (e.g., old ranges with XRP-only activity), the Deposits section of the Statement Summary shows `"Haricom Bank (GBP)"` as the bank account label instead of a meaningful name.

**Root Cause** (`generateStatementSummary`, line ~4530):
```
const inst = fiatInstitutionByCurrency[ccy] || "Haricom Bank";
```
The object `fiatInstitutionByCurrency` is only populated when a fiat **withdrawal** is processed in the date range. If no fiat withdrawals exist, both entries remain `null` and the hardcoded string `"Haricom Bank"` is used as the fallback.

**Resolution**: Resolved by Priority 1 (Fiat Deposit Label config). Once the user-configurable label is implemented, the hardcoded `"Haricom Bank"` fallback can be replaced with the user's chosen label (or `"Deposit"` if generic mode is selected).

---

## Phase 2: Staged Fiat Label Refinement

The refinement of fiat labels will be handled in three distinct stages to ensure clarity and avoid regressions.

### Stage 1: Decouple Naming Logic [DONE]
*   **Goal**: Stop the cross-contamination between withdrawals and deposits. 
*   **Action**: In `generateStatementSummary`, remove the code that caches the first-seen withdrawal recipient name for use in the deposits section.
*   **Result**: The Deposits section will no longer be affected by what the system finds in the withdrawals data. This is the prerequisite for fixing Bug C and Bug B.

### Stage 2: Fix Bug C (Withdrawal Labels)
*   **Goal**: Ensure fiat withdrawals show the correct institution (e.g., `"Revolut Ltd"`) instead of the generic `"Withdrawal (EUR)"` in the **Withdrawals** section.
*   **Action**: Update the withdrawal name resolution to prioritize the `"key"` (the label assigned in Kraken) from the `WithdrawStatus` API.
*   **Result**: Withdrawals will correctly display your assigned account labels.

### Stage 3: Fix Bug B + Generic Deposit Labels
*   **Goal**: Finalize the **Deposits** section with clear, generic labels since source bank data is unavailable.
*   **Bug B Symptom**: The generic `"Withdrawal (EUR)"` (or any bank name) incorrectly appearing as a deposit label.
*   **Action**: Fully implement the generic labels (e.g., `"Deposits (GBP)"`, `"Deposits (EUR)"`) for all deposit rows. Provide user configuration if specific labels are desired.
*   **Result**: A clean, consistent display for deposits that accurately reflects the available data.

---

### Bug C: "Withdrawal (EUR)" Appearing in the Withdrawals Section
**Symptom**: In the **Withdrawals to Haricom Bank Accounts GBP | EUR** section of the Statement Summary, a row labelled `"Withdrawal (EUR)"` appears as the bank account name, alongside the correct `"Revolut Ltd (GBP)"` row.

**Corrected Assessment**: For fiat withdrawals, Kraken *must* have a destination "wallet address" or bank account link. The generic bank name (e.g., `"Revolut Ltd"`, `"Santander Business"`) is available within the Kraken API (often in the `info` or linked address fields). The symptom occurs when the system fails to correctly map the withdrawal record to its known bank destination, falling back instead to a generic `"Withdrawal (CCY)"` string.

**Root Cause**: The current resolution logic in `generateBankReport` and `generateStatementSummary` sometimes defaults to the raw ledger `info` string when an address book match isn't found, but it fails to recognize that a generic banker name is almost always available in the withdrawal records or can be resolved from the address book if handled simply.

**Resolution**: Simplify and prioritize bank name resolution for fiat withdrawals:
*   Ensure that for any fiat withdrawal, the generic bank name (e.g., `"Revolut Ltd"`) is extracted from the Kraken API data as the primary label.
*   Prioritize: `Address Book Label` > `Generic Bank Name (from API)` > `Currency-based Fallback`.
*   Avoid complex "lookback" or "fallback" logic that produces generic `"Withdrawal"` labels when the bank name is known to Kraken.
*   This ensures consistency with the Statement and WTD reports, which already successfully use these labels.

---

## HOTFIX v4.10-01 — Rate Fetch Timeout & Cache Persistence (24 Feb 2026)

> **Urgency: Critical.** The report is unusable for large date ranges without this fix.

**Symptoms**:
- "Fetching rates… 3/138" — the counter stalls and never progresses to completion.
- Resetting and retrying produces the same result every time.

**Root Causes**:
1. No timeout on API `fetch()` calls — a single slow/hung request blocks the entire sequential loop indefinitely.
2. Kraken OHLC API was always attempted first, including for dates > 1 year old — even though it never returns usable historical data for those dates. Each attempt costs ~60–90 seconds via the Google Apps Script proxy.
3. `ratesCache` was in-memory only — every page load or Reset forced a full re-fetch of all dates from scratch.

**Fix applied in `v4.10-01-HOTFIX-RATE-FETCH`**:
1. `fetchWithTimeout()` wrapper — 8-second hard timeout on all rate API calls inside `getKrakenRate()`.
2. Kraken OHLC skipped entirely for dates > 365 days old; goes directly to CryptoCompare + Frankfurter.
3. `ratesCache` persisted to `localStorage` under the version-agnostic key `kraken_rates_cache` after each date is fetched (incremental — if interrupted, progress is not lost).
4. On startup, `kraken_rates_cache` is loaded first, then overlaid with the versioned cache if present — so cached rates survive a version bump.
5. Reset now clears `kraken_rates_cache` from `localStorage` alongside all other keys.
