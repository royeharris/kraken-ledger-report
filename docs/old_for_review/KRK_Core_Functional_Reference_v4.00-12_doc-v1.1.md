# KRK Core Functional Reference
Application Version Anchor: v4.00-12  
Document Version: v1.1  
Status: Authoritative Functional Reference (Living)

---

## Document versioning rule (important)
- **Application Version Anchor** refers to the software version this document describes.
- **Document Version** refers only to changes in this document.
- This document is **only ever extended or corrected**, never rewritten.
- New document versions must preserve prior agreed content unless explicitly deprecated.

---

## 0. Business Context and Core User Story

### Who this report is for
This report is produced **for the company’s external accountant**.

It is **not** used for quarterly VAT submissions.

It is used as **input to annual corporate tax assessments** to support review of:
- payments to individuals
- reconciliation of balances

The accountant has requested that the report now be produced **quarterly**, purely to reduce year‑end pressure. This does not change its tax purpose.

### Operational reality being modelled
Kraken is operationally used as a **payment bank**, not as a trading platform:

- Funds are deposited into Kraken (GBP or EUR)
- Fiat is converted into crypto
- Crypto is withdrawn to **individual subcontractors**
- Kraken does not provide bank‑style statements or reconciliations

This programme exists to generate a **bank‑like statement and reconciliation** from Kraken data.

### Core business question
“Who was paid, how much were they paid, in which period, and does the account reconcile without unexplained differences?”

Primary accountant concerns:
1. Withdrawals to individuals
2. Reconciliation differences

---

## 1. Primary Business Objectives

1. **Withdrawals to recipients**
   - Clear list of payments to individuals
   - GBP or GBP‑equivalent values
   - Consistent recipient labels

2. **Reconciliation integrity**
   - Opening balance + movements − closing balance ≈ 0
   - Differences must be explainable

3. **Auditability**
   - Summary → Statement → Ledger traceability

---

## 2. Asset Scope

- Crypto withdrawals: **USDT, XRP only**
- Fiat deposits: **GBP, EUR**
- Reporting currency: **GBP**

---

## 3. Net Trade Activity

Net Trade Activity explains **conversions**, not payments.

- GBP typically negative
- USDT typically positive

Across all assets combined, Net Trade Activity should net to zero.
Large discrepancies in early periods (e.g. 2021) are **known but deferred**, not accepted as correct.

---

## 4. Core Functional Flow

1. Ledger ingestion  
2. WDT Report (Withdrawals, Deposits, Transfers)  
3. Kraken Statement  
4. Statement Summary  
5. Export to **Google Sheets**

Errors upstream invalidate downstream outputs.

---

## 5. Objective D – Fiat Institution Labelling

### Source field
Kraken API provides bank identity via a field of the form:
- `*.info` (for example: `something.info`)

Ledger IDs and transaction references **cannot** be used to determine bank identity.

### Label rule
```
<Institution Name> (<Currency>)
```
Example:
```
Revolut Ltd. (GBP)
```

### Propagation rule
The label is assigned in the WDT Report and must propagate unchanged through:
WDT → Statement → Statement Summary

---

## 6. Statement Summary – Deposit Presentation Rule

- Deposits **must appear** in the Statement Summary if present in the Statement.
- Deposit labels must represent the **Haricom bank account**, not currency codes.
- Example deposit label:
```
Revolut Ltd. (EUR)
```

This rule exists to keep deposits consistent with withdrawal presentation.

---

## 7. Security Guardrail

- No API keys or secrets in client‑visible code.
- Google Sheets integration must not expose credentials.

---

## 8. Version Change Checklist (Mandatory)

For **every application version increment**:

- [ ] Single functional objective identified
- [ ] This document updated if behaviour changed
- [ ] Objective D verified end‑to‑end
- [ ] Statement Summary deposits visible
- [ ] Reconciliation reviewed
- [ ] No secrets exposed

---

## 9. Known Deferred Work (Not forgotten)

- Early‑period (e.g. 2021) reconciliation anomalies
- These are **deferred**, not accepted as correct
- May be revisited if historical reporting is required

---

End of document.
