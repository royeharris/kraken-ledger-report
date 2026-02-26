# KRK Defects and Verification Log
Document Version: v1.1  
Purpose: append-only operational record of defects, fixes, and verification.

---

## How this log is used
- Append-only: no old entries edited or removed
- Each application version must have at least one entry ("No defects" is valid)
- Each entry links back to the Core Functional Reference section(s)

---

## Entry Template (copy for each version)

### Version: __________
- Date:
- Functional objective:
- Defect description (if any):
- Root cause (functional):
- Fix applied:
- Verification steps performed:
- Result (pass/fail):
- Reference to Core Functional Reference section:

---

## Entries

### Version: v4.00-12 (Baseline)
- Date: __________
- Functional objective: Establish baseline for controlled stabilisation and Objective D completion.
- Defect description (known): Statement Summary deposit section can be empty even when deposits exist; Objective D not fully propagated end-to-end.
- Root cause (functional): Summary aggregation/label propagation not consistently aligned across WDT → Statement → Summary for deposits.
- Fix applied: None (baseline capture).
- Verification steps performed: Baseline manual checks; confirmed known issues to be addressed under v4.00-13 Objective D track.
- Result (pass/fail): Baseline accepted for continued work.
- Reference to Core Functional Reference section: Section 5 (Objective D), Section 6 (Deposit Presentation), Section 8 (Checklist).

---

End of document.
