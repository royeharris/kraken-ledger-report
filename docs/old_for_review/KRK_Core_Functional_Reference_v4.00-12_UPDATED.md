# KRK Core Functional Reference (Living Document)
Version Anchor: v4.00-12  
Status: Authoritative Functional Reference

---

## 0. Business Context and User Story (Why this exists)

### Who this report is for
This report is produced **for the company’s external accountant**.
It is used for:

- Quarterly VAT returns
- Annual corporate tax assessments
- Statutory reporting to HMRC and Companies House (UK)

From the accountant’s perspective, this report must look and behave like a **bank statement**.

### How Kraken is used in reality
Although Kraken is a crypto exchange, it is **used operationally as a bank**:

- Money is deposited into Kraken (GBP or EUR)
- Deposits are converted into crypto
- Crypto is withdrawn to **individual subcontractors**
- Kraken does not provide bank-style statements

This programme exists to create a **bank-like statement and reconciliation** from Kraken data.

### The core business question this report answers
“Who was paid, how much were they paid, in which period, and does the account reconcile without unexplained differences?”

The accountant mainly cares about:
1. **Withdrawals to individuals** (payments)
2. **Reconciliation differences** (to ensure no funds are missing)

---

## 1. Primary Business Objectives

1. Withdrawals to recipients  
2. Reconciliation integrity  
3. Auditability  
4. Regulatory suitability  

---

## 2. Asset Scope

- Crypto withdrawals: USDT, XRP only
- Fiat deposits: GBP, EUR
- Reporting currency: GBP (or GBP equivalent)

---

## 3. Net Trade Activity

Net Trade Activity explains asset conversions, not payments.

- GBP Net Trade Activity: typically negative
- USDT Net Trade Activity: typically positive

Overall Net Trade Activity across all assets should net to zero.
Large early-period differences are accepted and out of scope.

---

## 4. Core Functional Flow

1. Ledger ingestion
2. WDT Report
3. Kraken Statement
4. Statement Summary
5. Export

---

## 5. Objective D – Fiat Institution Labelling

- Source field: Kraken API `info`
- Label format: `<Institution Name> (<Currency>)`
- Example: `Revolut Ltd. (GBP)`
- Label must propagate unchanged from WDT to Summary

---

## 6. Statement Summary – Deposit Rule

If Statement contains deposits, Summary must show them.

---

## 7. Security Rule

No API keys or secrets in client-visible code.

---

## 8. Version Change Checklist

- Document updated if behaviour changed
- One functional objective only
- Objective D verified
- Summary deposits visible
- Reconciliation reviewed

---

## 9. Known Limits

Early-period reconciliation anomalies accepted.

---

End of document.
