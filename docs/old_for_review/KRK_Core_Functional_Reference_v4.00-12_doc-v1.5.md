# KRK Core Functional Reference
Application Version Anchor: v4.00-12  
Document Version: v1.5  
Status: Authoritative Functional Reference (Living)

---

## Preamble: how this document is used

This is the **single comprehensive reference** for:
- business purpose of the programme
- what the programme must do (end-to-end)
- hard rules that must not be broken
- how changes are controlled
- how agents and functional review are managed

This document is written so a new agent or reviewer can understand intent **without chat history**.

### How updates must be made
- Apply a **delta only**
- Preserve all agreed content
- No rewrites unless explicitly requested
- Mark removals as **Deprecated**
- Increment **Document Version**
- Record changes in the Document Change Log

---

## 0. Business Context and Core User Story
(unchanged from v1.4)

---

## 1–9. Core sections
(All unchanged from v1.4)

---

## Appendix A: Accountant-facing summary
(unchanged from v1.4)

---

## Appendix B: Version Change Record

### Version: v4.00-12 (Baseline)
(Status unchanged)

### Version: v4.00-13-00 (Objective D – start)

- Date: __________
- Functional objective:
  Objective D completion for GBP and EUR bank deposits and withdrawals, ensuring consistent institution labels across WDT Report, Kraken Statement, and Statement Summary, with correct handling when deposits or withdrawals are absent.
- Base version or fix counter: v4.00-13-00
- Sections affected:
  Section 5 (Objective D), Section 6 (Deposit Presentation), Appendix E (Test Matrix)
- Verification required:
  Objective D acceptance rules + edge-case test matrix
- Result: __________
- Notes:
  Initial implementation attempt.

---

## Appendix C: Agent Obligations
(unchanged from v1.4)

---

## Appendix D: Functional Consultant Responsibilities
(unchanged from v1.4)

---

## Appendix E: Test Matrix (Mandatory for Objective D)

The following scenarios **must be tested and recorded** for Objective D.

### Core scenarios
1. GBP deposit + GBP withdrawal to bank account
2. EUR deposit + EUR withdrawal to bank account
3. Mixed GBP and EUR deposits
4. Mixed GBP and EUR withdrawals

### Edge scenarios
5. Deposits exist, no withdrawals
   - Summary shows deposits
   - “No withdrawals in this period” message shown
6. Withdrawals exist, no deposits
   - Summary shows withdrawals
   - “No deposits in this period” message shown
7. Only GBP bank activity (no EUR)
8. Only EUR bank activity (no GBP)

### Propagation checks (all scenarios)
- Same label appears unchanged in:
  - WDT Report
  - Kraken Statement
  - Statement Summary
- Labels do not merge across currencies

---

## Appendix F: Hotfix Handling (Operational Rule)

### When a hotfix is required
A hotfix is required when:
- a security issue is discovered
- a regression breaks existing functionality
- an unrelated critical defect appears during feature work

### Hotfix version pattern
If working on:
- `v4.00-13-02`

Hotfix versions must be:
- `v4.00-13-02-hotfix-00`
- `v4.00-13-02-hotfix-01`
…

### Hotfix rules
- Fix only the urgent issue
- Do not expand scope
- Record hotfix in:
  - Version Change Record
  - Defects & Verification Log
- After hotfix passes, resume feature track:
  - `v4.00-13-03`

---

## Document Change Log

- v1.5: added Test Matrix (Appendix E); added Hotfix Handling (Appendix F); fully prepared Version Change Record for v4.00-13-00.

---

End of document.
