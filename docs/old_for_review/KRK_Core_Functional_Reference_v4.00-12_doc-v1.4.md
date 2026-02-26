# KRK Core Functional Reference
Application Version Anchor: v4.00-12  
Document Version: v1.4  
Status: Authoritative Functional Reference (Living)

---

## Preamble: how this document is used

This is the **single comprehensive reference** for:
- business purpose of the programme
- what the programme must do (end-to-end)
- hard rules that must not be broken
- how changes are controlled
- how agents and functional review are managed

This document is designed so that a new agent or developer can understand intent **without reading chat history**.

### What “authoritative” means
If the code and this document disagree, this document is treated as correct **until** this document is deliberately updated.

### How updates must be made (non-negotiable)
1. **Apply a delta only**: add or correct text; do not rewrite sections.
2. **Preserve prior agreed content**: remove/replace only if explicitly marked **Deprecated** with a reason.
3. **Record the change** in the Document Change Log.
4. **Increment Document Version** (v1.4 → v1.5).
5. **No silent changes**: every change must be described.

### When to update this document
Update this document whenever any of the following happens:
- a label format or propagation rule changes
- a calculation/reconciliation rule changes
- a defect fix changes behaviour (even if “just a bug fix”)
- a new output column/section/report is added
- a version number is increased
- a new hotfix branch/version is created

### Prompt to use when requesting an update
Copy/paste:

“Update `KRK Core Functional Reference` by applying a **delta only**.  
Preserve all existing agreed content.  
Add new material in the appropriate section.  
If old content must change, mark it as **Deprecated** with a reason.  
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

## 5. Objective D – Fiat Institution Labelling (Hard rule + acceptance)

### Source field (as implemented in the code)
The current code builds the bank label from Kraken address records using:
- `a.key` or `a.info` (whichever is present)
and appends the fiat currency in brackets.

Practical rule:
- Ledger IDs and transaction references cannot reliably determine bank identity.
- Bank identity comes from the address/funding metadata returned by Kraken.

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

### Objective D acceptance rules
Objective D is complete only when all of the following are true:

1. **Fiat withdrawals to bank accounts** appear in Statement Summary when present in Statement.
2. **Fiat deposits from bank accounts** appear in Statement Summary when present in Statement.
3. Labels are built from Kraken address metadata (`a.key` / `a.info`), and **do not merge across currencies**.
4. Label format is exactly: `<Institution Name> (<Currency>)`.
5. The same labels appear unchanged in **WDT**, **Statement**, and **Statement Summary**.
6. Edge-case display is correct:
   - if no deposits exist in the date range, show a clear “No deposits in this period” message
   - if no withdrawals exist in the date range, show a clear “No withdrawals in this period” message

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
- [ ] Statement Summary deposits visible (when deposits exist)
- [ ] Statement Summary “No deposits/No withdrawals” messaging correct (when applicable)
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

## Appendix B: Version Change Record (Required for every release)

Append a new entry here for every application version.

### Version: v4.00-12 (Baseline)
- Date: __________
- Functional objective (one sentence): Baseline version anchored for controlled stabilisation and Objective D completion work.
- Base version or fix counter: v4.00-12
- Sections of this document affected: Entire document (baseline reference)
- Verification performed: Baseline smoke checks + known issue notes
- Result (pass/fail): Baseline accepted / known defects deferred
- Notes: Objective D not yet complete; Statement Summary deposits issue known in this baseline.

### Version: v4.00-13 (Objective D completion) — Placeholder
- Date: __________
- Functional objective (one sentence): Objective D completion for GBP/EUR bank deposits and withdrawals with consistent labels across WDT/Statement/Summary.
- Base version or fix counter: v4.00-13-00 (start)
- Sections of this document affected: Section 5 (Objective D), Section 6 (Deposit Presentation), Section 8 (Checklist)
- Verification performed: Objective D acceptance rules + edge-case checks
- Result (pass/fail): __________
- Notes: __________

---

## Appendix C: Agent Obligations (Mandatory)

An agent must:

1. Restate the functional objective in one sentence (from this document).
2. List exactly which files will be changed.
3. Make the smallest possible change; **no refactoring**, no cleanup.
4. Work on one objective only; no “while here” edits.
5. Verify against the acceptance rules and checklist.
6. Update:
   - this core document (delta-only) if behaviour changed
   - the Defects & Verification Log for the version
7. Stop once acceptance passes; do not add extra features.

If any item cannot be met, the agent must stop and ask.

---

## Appendix D: Functional Consultant Responsibilities (Mandatory)

For each functionality / version:

1. Define the functional objective (one sentence).
2. Confirm acceptance criteria (what must be visible in outputs).
3. Approve the base version number for the functionality (e.g., v4.00-13).
4. Review outputs (WDT, Statement, Summary) and decide:
   - pass → move to next base version
   - fail → increment fix counter and continue
   - out of scope → defer explicitly and record
5. Approve Version Change Record and Log entry for the version.

---

## Document Change Log

- v1.4: added Agent Obligations and Functional Consultant Responsibilities; added baseline Version Change Record entries for v4.00-12 and placeholder for v4.00-13; added explicit edge-case display rules and checklist items.

---

End of document.
