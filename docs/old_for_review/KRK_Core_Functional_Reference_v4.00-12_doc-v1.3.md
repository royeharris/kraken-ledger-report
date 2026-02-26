# KRK Core Functional Reference
Application Version Anchor: v4.00-12  
Document Version: v1.3  
Status: Authoritative Functional Reference (Living)

---

## Preamble: how this document is used

This is the **single comprehensive reference** for:
- business purpose of the programme
- what the programme must do (end-to-end)
- hard rules that must not be broken
- how changes are controlled

This document is designed so that a new agent or developer can understand intent **without reading chat history**.

### How this document evolves
- Updates are **delta-only**
- Existing agreed content is preserved
- No rewrites unless explicitly requested
- Deprecated material must be marked clearly

### When to update this document
This document must be updated whenever:
- a functional rule changes
- a label, calculation, or reconciliation rule changes
- behaviour changes due to a defect fix
- a new application version is created

---

## 0. Business Context and Core User Story

[Content unchanged from v1.2]

---

## 5. Objective D – Fiat Institution Labelling (Acceptance Rules)

Objective D is considered **complete** only when all of the following are true:

1. Fiat deposits and withdrawals are labelled using Kraken address metadata (`*.info` or equivalent).
2. Label format is exactly:
   `<Institution Name> (<Currency>)`
3. The same label appears unchanged in:
   - WDT Report
   - Kraken Statement
   - Statement Summary
4. Statement Summary deposit section:
   - is never empty when deposits exist
   - uses institution labels (not currency codes)

If any rule fails, Objective D is **not complete** and the same base version must continue with a fix counter increment.

---

## Appendix B: Version Change Record (Required for every release)

For every application version, append a new entry here.

### Version: __________
- Date:
- Functional objective (one sentence):
- Base version or fix counter:
- Sections of this document affected:
- Verification performed:
- Result (pass/fail):
- Notes:

---

## Document Change Log

- v1.3: added Version Change Record template; added explicit Objective D acceptance rules; clarified update obligations.

---

End of document.
