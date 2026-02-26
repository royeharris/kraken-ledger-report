# Phase III-1 Bank Labels: Deposits/Withdrawals Alignment (v4.00-49)

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
