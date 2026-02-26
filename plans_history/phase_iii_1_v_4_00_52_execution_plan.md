# Phase III-1 – Version 4.00-52 Execution Plan

## Purpose

This document defines **exact, unambiguous changes required for v4.00-52** to resolve remaining inconsistencies in **Statement Summary deposits**, **Reconciliation**, and **bank-label alignment**, based strictly on the outcomes and failures observed up to v4.00-51.

This document is intended to be handed off to another agent (ChatGPT instance, Antigravity, or similar) for execution **without reinterpretation**.

---

## Current State (v4.00-51 – Verified)

The following are **confirmed facts**, not hypotheses:

1. **Statement table** (the detailed ledger-style table) correctly shows fiat deposits:

   - e.g. `deposit Revolut Ltd (EUR)` with EUR credit values.

2. **Trades / Withdrawals / Deposits (TWD) report**:

   - Fiat withdrawals show `Revolut Ltd (GBP)` / `Revolut Ltd (EUR)` correctly.
   - Fiat deposits show recipients correctly.

3. **Statement Summary – Withdrawals to Bank Accounts**:

   - Correctly split into:
     - `Revolut Ltd (EUR)`
     - `Revolut Ltd (GBP)`

4. **Statement Summary – Deposits from Bank Accounts**:

   - **Incorrect**: shows *"No deposits found for this period"*
   - Even though deposits clearly exist in the Statement table.

5. **Reconciliation Difference table**:

   - **Incorrect** because it consumes the same broken deposit aggregation.
   - Shows deposits from bank accounts as `0.00`, producing a large artificial reconciliation error.

Conclusion: **Deposits exist but are ignored by summary + reconciliation logic**.

---

## Root Cause (Authoritative)

The **Statement Summary deposits** and **Reconciliation deposits-from-bank-accounts** are still aggregating from a **legacy data structure** (e.g. `item.amounts`, asset maps, or pre-statement caches).

They are **not aggregating from the canonical Statement rows** that are already rendered and known to be correct.

> The Statement table is the single source of truth for deposits.

---

## Design Principle for v4.00-52 (Non-negotiable)

1. **Statement Summary and Reconciliation must aggregate from the same Statement rows that are rendered to the user.**
2. No secondary caches, no `amounts` dictionaries, no asset maps.
3. Bank deposits and bank withdrawals must use **identical label semantics**.

---

## Canonical Definitions (Must Be Used)

### Asset Normalisation

```js
function normalizeAsset(a) {
  return String(a || "").replace(/^[ZX]/, "");
}
```

### Fiat Detection

```js
function isFiatCurrency(a) {
  const c = normalizeAsset(a);
  return c === "GBP" || c === "EUR";
}
```

### Bank Label Construction

```js
function fiatBankLabel(base, assetRaw) {
  const c = normalizeAsset(assetRaw);
  const b = (base && String(base).trim()) ? String(base).trim() : "Bank";
  return `${b} (${c})`;
}
```

---

## Required Changes for v4.00-52

### Patch 1 – Statement Summary Deposits (PRIMARY FIX)

**Replace existing deposit-summary aggregation entirely.**

#### Source of truth

- Use **Statement rows** (the same array used to render the Statement table).
- Do **not** use `item.amounts`, `bankDeposits`, or legacy asset maps.

#### Aggregation logic

Pseudo-code:

```js
const bankDepositTotals = {};
let hasDeposits = false;

for (const row of statementRows) {
  if (!row || row.type !== "deposit") continue;
  if (!isFiatCurrency(row.asset)) continue;

  const baseLabel = row.bankInstitution || row.recipient || row.description || "Bank";
  const label = fiatBankLabel(baseLabel, row.asset);

  bankDepositTotals[label] ||= { GBP: 0, EUR: 0, gbpEq: 0 };

  const c = normalizeAsset(row.asset);
  if (c === "GBP") bankDepositTotals[label].GBP += Number(row.amount || 0);
  if (c === "EUR") {
    bankDepositTotals[label].EUR += Number(row.amount || 0);
    bankDepositTotals[label].gbpEq += Number(row.gbpEquivalent || 0);
  }

  hasDeposits = true;
}
```

#### Rendering rules

- Table header **must be**: `Haricom Bank Account`
- Rows:
  - One row per **Institution (Currency)** with non-zero totals.
  - Do **not** show zero rows.
- If `hasDeposits === false`, show:
  > `No deposits found for this period.`

---

### Patch 2 – Reconciliation Table (Mandatory)

The **Reconciliation Difference – Deposits from bank accounts** line must consume the **same totals** calculated above.

```js
let depGBP = 0;
let depEURgbpEq = 0;

for (const v of Object.values(bankDepositTotals)) {
  depGBP += v.GBP;
  depEURgbpEq += v.gbpEq;
}
```

Populate:

- GBP column = `depGBP`
- EUR (GBP Eq) column = `depEURgbpEq`
- Total = `depGBP + depEURgbpEq`

This change alone should eliminate the massive reconciliation error currently visible.

---

### Patch 3 – Header Consistency

Ensure **Statement Summary deposits** uses the same column semantics as **Withdrawals to Bank Accounts**:

- Column 1: `Haricom Bank Account`
- Not `Currency`

---

### Patch 4 – Remove / Disable Legacy Logic (Critical)

The following must **not** be used for deposits anymore:

- `item.amounts` for deposits
- Asset-keyed maps not derived from statement rows
- Any logic that assumes deposits can be inferred without reading the statement rows

This logic should be bypassed or removed to prevent future regressions.

---

## Validation Checklist (v4.00-52)

Use the **same date range** as the screenshots provided.

### Statement Table

- Shows multiple `deposit Revolut Ltd (EUR)` rows with EUR credits.

### Statement Summary – Deposits

- Section is populated (not empty).
- Header reads `Haricom Bank Account`.
- Shows `Revolut Ltd (EUR)` with the correct EUR total.
- No EUR/GBP zero rows.

### Statement Summary – Withdrawals

- Unchanged and still correct.

### Reconciliation Difference

- `Deposits from bank accounts` is **not 0.00**.
- Large artificial reconciliation difference is resolved.

---

## Explicit Non-Goals (Do NOT Do)

- Do NOT introduce frequency-based inference.
- Do NOT guess bank identity.
- Do NOT attempt to rejoin deposits via withdrawal history.
- Do NOT change crypto logic (USDT/XRP).

---

## Versioning

- Internal version string: **v4.00-52**
- Canonical filename remains: `KrakenLedgerReport.html`

---

## Handover Note

This document is complete and self-contained. Another agent should **only** apply the changes exactly as written above and produce **v4.00-52**.

