# Kraken Ledger Report - Project Learnings & Recurring Errors

## Critical Technical Constraints

### 1. Data Types in `readLedger` vs `generateBankReport`
**Context:** The application uses a "Linear Flow" where `readLedger` generates the dataset (`stagingRecords`) which is then consumed by `generateBankReport`.
**Constraint:**
- `stagingRecords` (and `cacheData.withdrawals`) is primarily formatted for **Display** (strings, absolute values).
- `generateBankReport` requires **Raw Signed Numbers** for mathematical operations (sorting, opening balance back-calculation).
**Lesson:**
- ALWAYS store raw numeric values alongside formatted strings in `stagingRecords`.
- **do NOT** rely on `parseFloat(entry.amount)` from a formatted string, as it loses precision or sign.
- **Required Properties** in `stagingRecords`:
  ```javascript
  {
      time: 1735689600,          // Raw Unix Timestamp (Required for Date Filtering)
      rawAmount: -50.25,         // Signed Number (Required for Math)
      rawBalance: 1000.50,       // Number (Required for Opening Bal Calc)
      rawFee: 0.15,              // Number
      // ... formatted strings for display ...
  }
  ```

### 2. Persistence Keys
**Context:** The app saves data to `localStorage`.
**Constraint:**
- The app standardized on **`kraken_v2_`** keys (e.g., `kraken_v2_addresses`, `kraken_v2_history`).
- **Recurring Bug:** New features sometimes accidentally try to load from `kraken_v3_` or other mismatched keys, causing the address book to appear empty after a reload.
**Lesson:**
- Always check `loadLocalData` and `saveLocalData` match the Key Version.

## Recurring Errors & Solutions

### Error: `bal.toFixed is not a function`
- **Symptom:** The Statement Report fails to generate; console shows this error.
- **Cause:** The `balance` or `amount` passed to the generator is a **String** (formatted for display), not a Number.
- **Fix:** Ensure the generator uses `.rawBalance` (Number) instead of `.balance` (String).

### Error: "No transactions found" (despite data existing)
- **Symptom:** Comparison of Date Ranges fails.
- **Cause:** The record object in `stagingRecords` is missing the raw `time` property (Unix Timestamp), or it was converted to a formatted date string.
- **Fix:** Explicitly ensure `time: w.time` is set in `readLedger`.

### UI Buttons Not Working / Unresponsive
- **Symptom:** Clicking buttons does nothing; Console shows syntax errors.
- **Cause:** Often caused by **Clone/Merge patterns** where a variable is declared twice (e.g., `const record = { ... const record = {`).
- **Fix:** Carefully review diffs for duplicate blocks when modifying large functions like `readLedger`.

### Address Book "Wiped" on Reload
- **Symptom:** Address book works in session, but is empty after page reload.
- **Cause:** `saveLocalData` writes to `v2` keys, but `loadLocalData` reads from `v3` keys (or vice-versa).

### Syntax & Merge Artifacts (Duplicate Code / Brackets)
- **Symptom:** UI completely unresponsive; Console shows `Unexpected token` or `Identifier 'record' has already been declared`.
- **Cause:**  AI or Manual Merges effectively "stamping" a code block twice, resulting in:
  ```javascript
  const record = {
    const record = { ... } 
  }
  ```
  Or missing closing brackets `}` at the end of functions after large edits.
- **Fix:**
  - **Always** collapse the modified function in the IDE to ensure the structure is valid before saving.
  - **Strict Verification:** If a tool output shows "Replaced X lines", verify the *edges* of the replacement didn't duplicate the start/end lines.
