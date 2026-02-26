# KRK Development Workflow Script (Plain Language)
Document Version: v1.0  
Purpose: step-by-step method to implement one functionality (e.g., Objective D) without losing control.

---

## 1. What counts as “one functionality”
One functionality is one business change that can be described in one sentence, for example:
- “Objective D: bank labels appear consistently in WDT, Statement, and Statement Summary.”

A functionality is complete only when the validation steps (Section 4) pass.

---

## 2. Version numbering rule (simple and consistent)

### Base version
A base version number (e.g., **4.00-13**) is reserved for one functionality.

### Fix counter
While working on that same functionality, append a fix counter:
- 4.00-13-00  (first attempt)
- 4.00-13-01  (first fix)
- 4.00-13-02  (second fix)
…

When the functionality is proven working, move to the next base version:
- 4.00-14-00 (next functionality starts)

Rule of thumb:
- **New base version** = new functionality goal
- **Increment fix counter** = defect fixing for the same functionality goal

---

## 3. Every iteration must follow the same small cycle

### Step 1 — State the goal (one sentence)
Write this in the Defects/Verification log:
- “Goal: …”

### Step 2 — Update the Core Functional Reference first (if behaviour is changing)
If the change affects rules, labels, or outputs, update the core reference before coding.

### Step 3 — Make the smallest possible code change
One change only. No cleanup. No refactor.

### Step 4 — Run the validation steps (Section 4)
If anything fails, do not start a new feature.
Fix the failure under the same base version by incrementing the fix counter.

### Step 5 — Record what happened
Append one entry to the Defects/Verification log:
- version
- what changed
- what was checked
- pass/fail
- notes

### Step 6 — Publish for testing
Push the new HTML version so it can be tested by refreshing the GitHub Pages URL.

---

## 4. Validation steps (minimum checks every time)

### A. Objective D checks (end-to-end)
1. Generate the WDT report.
2. Find a fiat deposit and a fiat withdrawal.
3. Confirm the label is in this format:
   - Institution name + currency in brackets
   - Example: “Revolut Ltd. (GBP)”
4. Generate the Statement and confirm the same labels appear unchanged.
5. Generate the Statement Summary and confirm:
   - Deposit section is not empty when deposits exist
   - Deposit labels represent the Haricom bank account (institution + currency)

### B. Reconciliation check
1. In Statement Summary, review the reconciliation table.
2. Confirm differences are negligible or explainable.

### C. Security check
1. Confirm no keys/secrets exist in client-visible code.
2. If Google Sheets export is used, confirm authentication is not exposing credentials.

---

## 5. How to request an implementation from an agent (copy/paste)
Use this exact prompt (keep it strict):

“Work only on functionality: [ONE SENTENCE GOAL].
Do not refactor.
Before coding, restate the goal and list the exact files to be changed.
After coding, describe what changed and run through the validation steps.
If a validation step fails, fix it before moving on.
Update the Core Functional Reference and Defects/Verification log for this version.”

---

End of document.
