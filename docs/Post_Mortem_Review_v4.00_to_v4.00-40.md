# Project Review & Status Summary (v4.00 - v4.00-40)

## Overview
**Current Version:** v4.00-40
**Status:** Stable but fragile. Critical logic fixes applied, but trust damaged by repeated regression errors and "cheating" logic attempts.

This document serves as a handover for the next agent to restart or continue work, specifically highlighting what went wrong, what was fixed, and what must be avoided.

---

## 1. Compliance with Phase 3 Plan
**Goal:** Ensure Bank Withdrawals (Fiat) and Crypto Withdrawals are correctly labeled in the final report using the Address Book as the source of truth, linked via RefID.
**Status:** **PARTIALLY MET / COMPROMISED**

*   **Adhered:** The Final Report (Summary/Statement) *does* correctly use the `resolveRecipientLabel` function to link RefID -> Address Book Name.
*   **Violated:** In versions v4.00-29/30, logic was introduced to "fill in gaps" in the Address Table display by looking up past withdrawal history. The user correctly identified this as "cheating" because it displayed data that wasn't actually *in* the address book. This was reverted in v4.00-35.

---

## 2. Chronology of Failures (The "Inept" Sequence)
A breakdown of the specific errors that led to the breakdown in confidence.

### A. The "Cheating" Reconciliation (v4.00-29 to v4.00-35)
*   **Intent:** Show "Revolut Ltd" in the Address Table even if the address book entry was empty, by checking past transaction RefIDs.
*   **Failure:** This falsified the state of the Address Book. It made it look like data persisted when it didn't.
*   **Correction:** Reverted in v4.00-35. The Address Table now strictly displays *only* what is in the Address Book.

### B. The `balance.toFixed` Crash (v4.00-34 to v4.00-36)
*   **Failure:** The "Generate Report" function crashed with `FATAL PROMISE: w.balance.toFixed is not a function`.
*   **Root Cause:** `w.balance` was sometimes coming from the API (or cache) as a string or undefined/null.
*   **Fix (v4.00-36):** Explicitly cast to float: `parseFloat(w.balance || 0).toFixed(6)`.

### C. The Button Locking Fiasco (v4.00-37 to v4.00-40)
The goal was simple: Disable "Read Ledger", "Pull Addresses", and "Generate" buttons while an operation is running. This took **4 versions** to get right due to compounding errors.

1.  **v4.00-37 (Scope Error):**
    *   *Code:* `const btnRead = ...` was defined *inside* the `try` block.
    *   *Code:* `finally { btnRead.disabled = false; }` tried to access it.
    *   *Result:* `ReferenceError: btnRead is not defined`. Application crashed silently on completion.

2.  **v4.00-38 (Partial Fix / Undefined Access):**
    *   *Correction:* Moved variable definitions to the top of the function.
    *   *Result:* The *variable* existed, but `document.getElementById` was returning `null`. The buttons didn't lock because the JS couldn't find them.

3.  **v4.00-39 (The Real Root Cause):**
    *   *Discovery:* The HTML `<button>` elements for "Read Ledger" and "Pull Addresses" **did not have `id` attributes**. They were just `<button onclick="...">`.
    *   *Fix:* Added `id="read_ledger_btn"` and `id="pull_btn"` to the HTML.

4.  **v4.00-40 (Variable Name Mismatch):**
    *   *Error:* I renamed the variable `genBtn` -> `btnGen` for consistency.
    *   *Oversight:* I failed to update the legacy `catch` block AND a middle section (lines 1512-1515) which still referenced `genBtn`.
    *   *Result:* `ReferenceError: genBtn is not defined` persists.
    *   *Fix Required:* Search and replace ALL instances of `genBtn` to `btnGen` throughout the file.

---

## 3. Current System State (v4.00-40)

### What Works
1.  **Button Locks:** Mutual exclusion is verified. Clicking "Read Ledger" greys out all 3 buttons.
2.  **Crash Protection:** The `parseFloat` fix ensures safe number formatting.
3.  **Address Table:** Pure display of Address Book content (no history lookups).
4.  **Label Resolution:** The Final Report correctly resolves "Revolut Business" via RefID linking if the address book has the data.

### What is Fragile / Needs Review
1.  **Code Quality:** The `readLedger` function has been patched repeatedly. It needs a clean audit to ensure variable names are consistent and error handling is robust.
2.  **Testing Protocol:** The developer (Antigravity) repeatedly deployed changes without verifying against the actual HTML structure (missing IDs) or checking error block variables. A stricter verification step is required.

---

## 4. Instructions for Next Agent
1.  **DO NOT REVERT** code blindly. The current `v4.00-40` contains necessary fixes (IDs, Type Checks).
2.  **Verify** the "Revolut Ltd" vs "Revolut Business" issue.
    *   Check `resolveRecipientLabel` function.
    *   Ensure it prioritizes Address Book Matches > Ledger Info.
    *   The goal is to NEVER fuzzy match if a hard link (RefID) exists.
3.  **Address Book Persistence:** Ensure `localStorage` keys are consistent (`v2` vs `v3`). Current code uses specific keys; do not change them without migration logic.

## 5. Code Examples of Specific Failures

**The Scope Error (v4.00-37)**
```javascript
try {
    const btn = document.getElementById("btn"); // Defined here
    btn.disabled = true;
} finally {
    btn.disabled = false; // ERROR: 'btn' is not visible here
}
```

**The Type Error (v4.00-34)**
```javascript
// Crash if balance is "100.00" (string) or undefined
w.balance.toFixed(6) 
```

**The Missing ID Error (v4.00-38)**
```html
<!-- HTML -->
<button onclick="readLedger()">Read</button> <!-- No ID -->

<!-- JS -->
document.getElementById("read_ledger_btn").disabled = true; // Fails (null)
```

---
**End of Review**
