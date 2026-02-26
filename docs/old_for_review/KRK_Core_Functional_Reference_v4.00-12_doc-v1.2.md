# KRK Core Functional Reference
Application Version Anchor: v4.00-12  
Document Version: v1.2  
Status: Authoritative Functional Reference (Living)

---

## Preamble: how this document is used

This is the **single comprehensive reference** for:
- business purpose of the programme
- what the programme must do (end-to-end)
- hard rules that must not be broken
- how changes are controlled

This document is written so that a new agent or developer can understand the intent **without reading chat history**.

### What “authoritative” means
If the code and this document disagree, this document is treated as correct **until** this document is deliberately updated.

### How updates must be made (non-negotiable)
Updates must follow these rules:

1. **Apply a delta**: add or correct text, do not rewrite the document.
2. **Preserve prior agreed content**: remove or replace content only if explicitly marked as deprecated.
3. **Record what changed**: add an entry to the “Document Change Log” section.
4. **Increment Document Version**: e.g., v1.2 → v1.3.
5. **No “silent” changes**: every change must be described.

### When to update this document
Update this document whenever **any** of the following happens:
- a rule changes (even slightly)
- a label format changes
- a calculation or reconciliation approach changes
- a defect fix changes behaviour (even if it is “just a bug fix”)
- a new output column, section, or report is added
- a version number is increased

### Prompt to use when requesting an update
Copy/paste this when asking an agent (or ChatGPT) to update the document:

“Update `KRK Core Functional Reference` by **applying a delta only**.  
Preserve all existing agreed content.  
Add new material in the appropriate section.  
If any old content must change, mark it as **Deprecated** with a reason.  
Increment Document Version and update the Document Change Log.”

---

## 0. Business Context and Core User Story

### Who this report is for
This report is produced **for the company’s external accountant**.

It is used as **input to annual corporate tax assessments**, focusing on:
- payments to individuals (subcontractors)
- reconciliation confidence (no unexplained differences)

The accountant has requested that the report be produced **quarterly** to reduce year-end pressure, but the purpose remains corporate tax assessment support.

### How Kraken is used in reality
Although Kraken is a crypto exchange, it is used operationally as a **payment bank**:

- funds are deposited (GBP or EUR)
- deposits are converted into crypto
- crypto is withdrawn to individual subcontractors
- Kraken does not provide bank-style statements or reconciliations

This programme exists to generate a **bank-like statement and reconciliation** from Kraken data.

### Core business question
“Who was paid, how much were they paid, in which period, and does the account reconcile without unexplained differences?”

Primary accountant concerns:
1. withdrawals to individuals (payments)
2. reconciliation differences (to ensure nothing unexplained is missing)

---

## 1. Primary Business Objectives

1. **Withdrawals to recipients**
   - clear list of payments to individuals
   - GBP or GBP-equivalent values
   - consistent recipient labels

2. **Reconciliation integrity**
   - opening balance + movements − closing balance ≈ 0
   - differences must be explainable

3. **Auditability**
   - Summary → Statement → Ledger traceability

---

## 2. Asset Scope

- Crypto withdrawals used for payments: **USDT, XRP**
- Fiat deposits: **GBP, EUR**
- Reporting currency: **GBP**

---

## 3. Net Trade Activity

Net Trade Activity explains **conversions**, not payments.

- GBP typically negative (GBP converted to crypto)
- USDT typically positive (USDT created to fund withdrawals)

Across all assets combined, Net Trade Activity should net to zero.
Large discrepancies in early periods (e.g. 2021) are **known and deferred**, not accepted as correct.

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

### Source field (as implemented in the code)
The current code builds the bank label from Kraken address records using:
- `a.key` or `a.info` (whichever is present)  
and appends the fiat currency in brackets.  
This is explicitly described in the v4.00-12 code. 【turn5file10†Kraken_Ledger_Report_v4.00-12_COMBINED_FIX_API_CONFIG_AND_STATEMENT.html†L64-L73】

Important practical rule:
- Ledger IDs and transaction references cannot reliably determine bank identity.
- Bank identity comes from the address / funding metadata returned by Kraken.

### Label rule
```
<Institution Name> (<Currency>)
```
Example:
```
Revolut Ltd. (GBP)
```

### Propagation rule
The label is assigned in the WDT/Statement building step and must propagate unchanged through:
WDT → Statement → Statement Summary

---

## 6. Statement Summary – Deposit Presentation Rule

- Deposits must appear in the Statement Summary if present in the Statement.
- Deposit labels must represent the **Haricom bank account**, not currency codes.
- Example deposit label:
```
Revolut Ltd. (EUR)
```

---

## 7. Security Guardrail

- No API keys or secrets in client-visible code.
- Google Sheets integration must not expose credentials.

---

## 8. Version Change Checklist (Mandatory)

For **every application version increment**:

- [ ] single functional objective identified
- [ ] this document updated if behaviour changed
- [ ] Objective D verified end-to-end (if Objective D is in scope)
- [ ] Statement Summary deposits visible
- [ ] reconciliation reviewed
- [ ] no secrets exposed

---

## 9. Known Deferred Work (Not forgotten)

- Early-period (e.g. 2021) reconciliation anomalies
- Deferred, not accepted as correct
- May be revisited if historical reporting is required

---

## Appendix A: Accountant-facing summary (for sharing)

This report exists because Kraken is being used like a bank to pay subcontractors, but Kraken does not provide bank-style statements.

The report provides:
- a clear list of payments (withdrawals) to individuals in the reporting period
- values in GBP or GBP equivalent
- a reconciliation summary that demonstrates that opening balance plus movements equals closing balance, with negligible unexplained differences

---

## Document Change Log

- v1.2: added preamble (how to use/update), added update prompt, added accountant-facing appendix, clarified Objective D “as implemented” wording, kept all prior rules.

---

End of document.
