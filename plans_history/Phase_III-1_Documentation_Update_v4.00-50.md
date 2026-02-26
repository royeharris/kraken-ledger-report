# Phase III-1 Bank Labels: Deposits/Withdrawals Alignment (v4.00-50)

## Objective
Make the **Statement Summary** bank sections deterministic and readable:

- **No GBP+EUR merging** into one line when the institution label is the same.
- **Same labelling scheme for deposits and withdrawals**:
  - `Institution (GBP)`
  - `Institution (EUR)`
- **Rows exist only when activity exists** in the selected period (no zero-value placeholder rows).
- Keep changes **presentation-only** (no changes to reconciliation / valuation logic).

## Canonical Rules

### Rule A — Currency is part of the grouping key
All bank summary aggregation must key on:
- `bankLabelWithCurrency = institutionLabel + " (" + currency + ")"`

This prevents a single label like `Revolut Ltd` from merging GBP and EUR totals.

### Rule B — Rows are created only if there is activity
For each section (Deposits / Withdrawals) and each currency (GBP/EUR):
- If total amount for that currency is **> 0** → emit a row
- If total amount for that currency is **0** → emit no row

If **no rows exist** for the section → show a single message row:
- `No deposits for this period.`
- (Withdrawals already renders a placeholder row if empty.)

### Rule C — Institution label source (no hardcoding)
For **fiat** currencies GBP/EUR:

1. Prefer **transaction evidence** from the selected period:
   - If at least one fiat bank withdrawal exists for that currency, use the cleaned recipient label already derived from `WithdrawStatus.info` (e.g. `Revolut Ltd`).
2. If no fiat withdrawals exist in-period but deposits do exist:
   - Fallback to **address-book configuration** (`krakenAddresses.key`), taking the first two words (e.g. `Revolut Business`, `Revolut B`).
3. Final display label always appends currency:
   - `Revolut Ltd (GBP)` / `Revolut Ltd (EUR)` etc.

This keeps the implementation dynamic and avoids “frequency” heuristics.

## Code Changes (Surgical Checklist)

### 1) `generateStatementSummary(customRecords)`
**Modified**
- Added:
  - `fiatInstitutionByCurrency = { GBP: null, EUR: null }`
- In the fiat withdrawal branch (`asset === "GBP" || asset === "EUR"`):
  - Capture institution label once per currency:
    - `if (!fiatInstitutionByCurrency[asset]) fiatInstitutionByCurrency[asset] = recipient;`
  - Continue to aggregate withdrawals using a currency-suffixed key:
    - `fiatKey = \`\${recipient} (\${asset})\``

**Replaced**
- `depositRows` previously emitted two fixed rows `{asset:"GBP" ...}`, `{asset:"EUR" ...}`.
- Now `depositRows` is computed as rows shaped like the fiat-withdrawal table:
  - `{ recipient, GBP, EUR, EUR_GBP }`
- `depositRows` only includes currencies with `depositTotals[currency] > 0`.

**Added (inside depositRows IIFE)**
- `fallbackInstitutionFromAddressBook(ccy)` which reads:
  - `cacheData.krakenAddresses`
  - matches on normalised asset `ZGBP→GBP`, `ZEUR→EUR`
  - uses `a.key` first two words
  - treats missing `verified` as verified (display-only).

### 2) `renderSummaryTable()`
**Modified**
- S3 (Deposits) table layout changed to match bank withdrawals:
  - Header: `Deposits from Haricom Bank Accounts  GBP | EUR`
  - Columns: `Haricom Bank Account | GBP Amount | EUR Amount | EUR (GBP Eq)`
- Rows:
  - If `summaryRecords.deposits.length > 0` → render rows
  - Else → render `["No deposits for this period.", "-", "-", "-"]`

**Modified**
- `fmt(v, d)` now clamps negative zero:
  - prevents `-0.00` from appearing in summary tables

### 3) Deletions / Retired Logic
**Removed from summary behaviour**
- Deposits summary **no longer** uses:
  - fixed “Currency / Total Amount / GBP Equivalent” rows
  - zero-value currency rows

**Explicitly not used**
- Any “most frequent label per currency” logic (statistical inference) is not part of the solution.

## Validation Checklist

### A) Deposits summary row suppression
1. Select a date range with **GBP deposits only**.
2. Expected:
   - Exactly **one** deposits row: `… (GBP)`
   - **No** EUR row with `0.00`

### B) Withdrawals bank summary row splitting
1. Select a date range with **both GBP and EUR bank withdrawals**.
2. Expected:
   - Two distinct rows, even if institution label is identical:
     - `Revolut Ltd (GBP)`
     - `Revolut Ltd (EUR)`
   - EUR row shows `EUR (GBP Eq)` populated; GBP row shows `-`.

### C) No merged lines
1. Confirm no single row contains both GBP and EUR values for bank withdrawals unless the label is currency-suffixed (it should not happen with this keying).

### D) Stability regression check
1. Verify “Withdrawals to Recipients USDT|XRP” section is unchanged.
2. Verify reconciliation numbers and statement generation still complete.

## Notes for Future Enhancement (Optional)
If Kraken ever exposes a destination `key` for fiat withdrawals in status payloads, the institution source can be upgraded to:
- `WithdrawStatus.key → first two words → + (currency)`
without changing table keying or row suppression rules.


## Additional Fixes in v4.00-50

### 1) Statement Table: Fiat Deposits Labelled as Institution (Currency)
- **Problem:** Fiat deposits (e.g. ZEUR) could resolve from the address book key (e.g. `Revolut B`) while fiat withdrawals resolved from history `info` (e.g. `Revolut Ltd`), causing inconsistency.
- **Fix:** A per-statement-run map `fiatInstitutionByCurrency_stmt` is built from **in-period fiat withdrawals** (`info` / history `info`) and applied to **both**:
  - fiat withdrawals to bank; and
  - fiat deposits from bank.
- **Result:** Statement rows show `Revolut Ltd (EUR)` / `Revolut Ltd (GBP)` consistently for both deposits and withdrawals (when the institution is evidenced by withdrawals in the same period).

### 2) Trades/Withdrawals/Deposits Report: Fiat Recipient Labels Currency-Disambiguated
- **Problem:** Fiat withdrawals in the TWD report could display `Revolut Ltd` without `(GBP)` / `(EUR)`; fiat deposits could have a blank recipient.
- **Fix:** TWD report now forces fiat deposit/withdrawal recipient labels to **always** be `Institution (Currency)`:
  - Prefer `fullRecipient`, else `historyMatch.info`, else `fiatInstitutionByCurrency_twd[Currency]`, else `Bank (Currency)`.
- **Result:** GBP/EUR never merge in downstream summaries, and fiat deposit rows are no longer blank.

### 3) Statement Summary: Deposits Lines Only When Activity Exists
- **Fix:** Deposit summary rows are emitted only when totals > 0 for that currency.
- **Result:** No redundant `EUR` deposit row when there are only GBP deposits; a single “No deposits found for this period.” row appears when both are zero.

## Validation Checklist (v4.00-50)

1. **TWD Report**
   - Fiat bank withdrawals show `Institution (GBP)` and/or `Institution (EUR)` (not plain `Institution`).
   - Fiat deposits have a non-empty recipient label.

2. **Statement Table**
   - Fiat withdrawals show `Institution (GBP)` / `Institution (EUR)`.
   - Fiat deposits show the **same** scheme (not `Revolut B`).

3. **Statement Summary**
   - “Withdrawals to Haricom Bank Accounts” shows **separate rows** for GBP and EUR when both exist.
   - “Deposits from Haricom Bank Accounts”:
     - shows only currencies that have deposits in-range; or
     - shows the “No deposits found for this period.” message when none exist.

4. **Reconciliation**
   - Reconciliation Difference does not regress materially versus v4.00-49 for the same date range.
