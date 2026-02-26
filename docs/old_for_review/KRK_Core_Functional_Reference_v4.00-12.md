# KRK Core Functional Reference (Living Document)
Version Anchor: v4.00-12
Status: Authoritative Functional Reference

---

## 1. Purpose of this Document

This document is the single authoritative description of:
- What the Kraken Ledger Report programme is supposed to do
- How the core functionality is realised
- What rules and guardrails must not be broken
- What is known to be correct vs what is still uncertain

It exists to prevent loss of direction, repeated defects, and undocumented changes.

If code and this document disagree, this document takes precedence until deliberately updated.

---

## 2. Programme Objective (Business View)

The Kraken Ledger Report application transforms raw Kraken ledger data into:
- Reconciled transaction reports
- Formal statements
- Aggregated summaries suitable for accounting and tax analysis

The system must be deterministic:
The same inputs must always produce the same outputs.

Traceability from raw ledger to final summary is mandatory.

---

## 3. Core Functional Flow (Critical Path)

The system operates strictly in this sequence:

1. Ledger ingestion
   - Raw Kraken ledger data is loaded
   - No interpretation beyond parsing

2. WDT Report (Withdrawals, Deposits, Transfers)
   - First derived report
   - Normalises ledger entries into understandable movements
   - Assigns labels for fiat institutions (Objective D)

3. Kraken Statement
   - Time-bounded transaction record
   - Built strictly from WDT-derived rows
   - This is the authoritative transaction list

4. Statement Summary
   - Aggregation layer
   - Derived only from Statement rows
   - Produces totals for deposits, withdrawals, fees, balances

5. Export (e.g. Google Sheets)
   - Presentation only
   - Must not alter calculations or labels

If any stage is wrong, all downstream stages are invalid.

---

## 4. Objective D – Fiat Institution Labelling (Contract)

### 4.1 Objective

Ensure consistent and correct labelling of fiat deposits and withdrawals across:
- WDT Report
- Kraken Statement
- Statement Summary

### 4.2 Source of Truth

Kraken does not reliably expose bank identity via:
- Ledger reference IDs
- Transaction IDs
- Addresses

The only reliable source is the Kraken API `something.info` field.

Examples:
- Revolut.Revolut Ltd.
- Barclays.Barclays PLC

### 4.3 Label Construction Rule

For every fiat deposit or withdrawal:

Format:
<Institution Name> (<Currency>)

Examples:
- Revolut.Revolut Ltd. (GBP)
- Barclays.Barclays PLC (EUR)

### 4.4 Propagation Rule

Once assigned:
- The label must not change
- The same label must propagate unchanged through:
  WDT → Statement → Statement Summary

No downstream reinterpretation is permitted.

---

## 5. Statement Summary – Deposit Visibility Rule

Required behaviour:
- If the Statement contains deposit rows, the Summary deposit section must not be empty
- Deposits must be derived by scanning Statement rows directly

Known issue:
- This defect occurred in v4.00-12 and was a primary stabilisation focus

Any change affecting Summary logic must explicitly confirm deposit visibility.

---

## 6. Security Guardrail

- No API keys or secrets may be embedded in client-visible code
- Google Sheets integration must not expose credentials

This is mandatory.

---

## 7. What Must Not Change Without Explicit Review

- Source of fiat institution identity (`something.info`)
- Label format and propagation
- Statement Summary derivation source (Statement rows only)
- One-pass FX conversion rules

---

## 8. Known Uncertainties (Explicit)

The following are understood but not yet fully consolidated:
- Edge-case fiat reversals
- Interaction between trades and summaries
- Export formatting edge cases

These are explicitly provisional.

---

## 9. Change Control Rules

- One functional change per iteration
- Every change must state which section of this document it affects
- This document must be updated before or alongside code changes

---

End of document.
