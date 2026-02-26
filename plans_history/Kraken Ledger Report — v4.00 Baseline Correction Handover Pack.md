# Kraken Ledger Report — v4.00 Baseline Correction Handover Pack

## Purpose
Create a single, consistent, agent-ready set of essentials to deliver documented corrections on **Kraken_Ledger_Report_v4.00.html** (baseline) while enforcing a strict **NO-REFACTOR** constraint. This pack is suitable for handover to any implementation agent (e.g., ChatGPT, Antigravity/OpenCode) and for historical record keeping.

## Baseline Artefacts
- **Implementation baseline (immutable):** `Kraken_Ledger_Report_v4.00.html`
- **Authority / constraints:** `KRK_Versioning_Rules_v4.000.md`, `KRK_Project_Planning_and_Context_v4.000.md`
- **Behavioural intent:** `KRK_User_Manual_v4.000.md`, `KRK_Technical_Notes_v4.000.md`
- **Defects/corrections authority:** `Post_Mortem_Review_v4.00_to_v4.00-40.md`, `Phase_II_Rebuild_Technical_Checklist.pdf`, `Phase_II_Handover.pdf`
- **Phase III-1 correction instructions:** `Phase_III-1_Documentation_Update_v4.00-51.md`, `phase_iii_1_v_4_00_52_execution_plan_updated.md`, `Phase_III-1_Bank_Withdrawal_Label_Normalisation_Execution_Plan(updated).md`

## Non-Negotiable Constraint
### NO REFACTORING (absolute)
No changes are permitted that are not strictly required to implement a documented correction.

Disallowed (non-exhaustive):
- Renaming variables/functions/IDs/labels
- Reformatting, linting, whitespace cleanup
- Reordering logic for readability
- Extracting/merging functions, abstractions, DRY changes
- Removing “unused” code unless explicitly documented
- Any performance/UX “improvements” not documented

Any change that violates the above invalidates the iteration.

## What “1, 2, 3” Refers To
1. **DEFECT mapping (read-only):** locate the exact code area(s) in v4.00 HTML responsible for a documented defect (e.g., “Generate Ledger” issue), without changing code.
2. **Agent prompt drafting:** produce exact, constraint-driven prompts to apply a single documented fix (minimal patch), and to push the iteration to GitHub.
3. **One-page workflow MD:** a concise operational flow for iteration, testing via GitHub Pages, and traceability.

This handover pack includes all three.

---

# Operating Workflow (Stage-wise)

## Stage 0 — Freeze Baseline (one-time)
Goal: protect v4.00 as immutable reference.
- Store `Kraken_Ledger_Report_v4.00.html` on a protected branch (example: `baseline/v4.00`).
- Record date/version and mark as **known-defective controlled baseline**.

## Stage 1 — Prepare (no code changes)
Goal: ensure authority and constraints are locked.
- Confirm the authoritative document set above.
- Create/retain this Handover Pack as the single operational reference.

## Stage 2 — Map Defects to Code (read-only inspection)
Goal: for each documented defect, produce a precise code location map.

For each defect:
- Identify the UI trigger (e.g., **Generate Ledger** button handler).
- Identify functions involved (ledger build, classification, aggregation, rendering).
- Capture: function names, surrounding comment markers, and line ranges.
- Produce a short mapping note (template below).

### Mapping Note Template
- Defect ID:
- Trigger:
- Expected behaviour (documentation anchor):
- Current behaviour (observed symptom only, no speculation):
- Code locations:
  - File: Kraken_Ledger_Report_v4.00.html
  - Functions/sections:
  - Line ranges:
- Minimal correction intent (plain language):

## Stage 3 — Single-Defect Patch Iteration (minimal change)
Goal: produce one testable HTML file per defect.

Rules:
- Exactly **one defect per iteration**.
- Edit only the smallest local region necessary.
- Do not touch unrelated behaviour.

Naming convention (example):
- `Kraken_Ledger_Report_v4.00-01_DEFECT-001.html`

In-file header comment (required):
```html
<!--
Version: 4.00-01
Defect: DEFECT-001
Source: Phase III-1 execution documentation
Constraint: NO REFACTOR
Purpose: GitHub Pages testing
-->
```

## Stage 4 — Push to GitHub for Testing (GitHub Pages)
Goal: every iteration becomes testable via a GitHub URL.
- Create branch: `fix/DEFECT-001` (example)
- Commit only the new HTML file.
- Push.
- Test using GitHub Pages URL.

## Stage 5 — Validate and Decide
- Run validation checklist (below).
- If pass: proceed to next defect.
- If fail: return to Stage 3 (same defect) with a new iteration number.

## Stage 6 — Consolidate Versions (after multiple fixes)
Only after all targeted defects pass validation:
- Merge branches into a new version (e.g., v4.01).
- Maintain traceability from each defect iteration.

---

# Validation Checklists

## Pre-Change Checklist (must pass before editing)
- Defect is explicitly documented in authoritative sources.
- Correction intent is explicitly described (Phase II/III-1 materials).
- Mapping note exists with precise code location(s).
- Change scope is limited to a single defect.
- NO-REFACTOR constraint acknowledged in the change record.

## Post-Change Checklist (must pass before GitHub push)
- Only the minimal required code area is changed.
- No renaming/reformatting/logic reorder.
- No console errors at load or during ledger generation.
- “Generate Ledger” completes and output aligns with documented expectations.
- No regression in unrelated reports/summaries.
- Iteration header comment present in HTML.

## GitHub Pages Test Checklist (must pass after push)
- GitHub Pages URL loads the correct iteration.
- Test case set executed (ledger generation + bank label normalisation scenarios).
- Results recorded in a short test note for the iteration.

---

# Defect Register (Essentials)

## DEFECT-001 — Ledger Generation (v4.00)
- Trigger: click **Generate Ledger**
- Status: known defect in v4.00 baseline
- Correction authority: Phase III-1 execution documentation
- Action: Stage 2 mapping required before patching

## DEFECT-002 — Bank Withdrawal Label Normalisation
- Scope: bank withdrawal labels; normalisation rules per Phase III-1 plan
- Action: mapping + minimal patch iteration(s)

## OBJECTIVE D — Bank Label Normalisation (Authoritative)

### Scope
Applies to **bank-related deposits and withdrawals** involving Haricom bank accounts, and any bank address-book entries configured for **GBP or EUR**.

### Authoritative rule (agreed, Phase III-1)
- The **bank identifier** must be taken from the Kraken address book record matched to the ledger entry.
- The identifying string may appear in:
  - `address.key` (preferred)
  - `address.info` (fallback only if `key` is absent)
- Append the **fiat currency** in brackets based on the address configuration:
  - `Revolut Ltd. (GBP)`
  - `Revolut Ltd. (EUR)`
  - `Barclays Limited (GBP)`

### End-to-end propagation rule
Labels must be normalised **once, at TWD construction time**, and then flow unchanged through:
1. **TWD report** (Trades / Withdrawals / Deposits)
2. **Statement report** (derived from TWD)
3. **Statement summary** (derived from Statement)

No downstream relabelling is permitted.

### Constraints
- GBP and EUR only (no other assets).
- NO refactor of matching logic, storage, or rendering pipelines.
- Minimal, localised line edits only.

### Acceptance criteria
- The same bank label (including currency suffix) appears identically in:
  - TWD report
  - Statement report
  - Statement summary
- Deposits and withdrawals to Haricom bank accounts are consistently labelled.


(Additional defects may be appended strictly from authoritative sources.)

---

# Agent Prompts (Copy/Paste)

## Prompt A — Read-only DEFECT Mapping (Stage 2)
```
Task: Map documented defects to exact code locations in Kraken_Ledger_Report_v4.00.html.

Constraints:
- NO code edits
- NO refactoring suggestions
- Provide only: function/section names, line ranges, and trigger paths

Focus defects:
- DEFECT-001: Generate Ledger produces incorrect/failed ledger
- DEFECT-002: Bank withdrawal label normalisation per Phase III-1 plan

Output:
- A mapping note per defect using the provided template.
```

## Prompt B — Apply Minimal Fix (Stage 3)
```
Task: Apply a documented correction to an existing HTML file.

ABSOLUTE CONSTRAINTS:
- NO refactoring of any kind
- NO renaming
- NO formatting changes
- NO logic reordering
- Change ONLY what is required for the documented defect

Input file:
Kraken_Ledger_Report_v4.00.html

Defect:
DEFECT-001 — Generate Ledger incorrect/failed ledger output

Correction authority:
Phase III-1 execution documentation and updates

Output:
A single updated HTML file named:
Kraken_Ledger_Report_v4.00-01_DEFECT-001.html

Also add/maintain the required HTML header comment documenting version, defect, source, and NO-REFACTOR.
```

## Prompt C — Push Iteration to GitHub (Stage 4)
```
Task: Push a single updated HTML iteration to GitHub for GitHub Pages testing.

Repository: <REPO_NAME>
Branch: fix/DEFECT-001

Commit ONLY this file:
Kraken_Ledger_Report_v4.00-01_DEFECT-001.html

Commit message:
"Fix DEFECT-001: Ledger generation correction (NO REFACTOR)"

Constraints:
- Do not modify any other files
- Do not reformat content
- Confirm the GitHub Pages URL that serves the updated file
```

---

# Minimal Iteration Record Template (per GitHub push)
- Iteration file:
- Branch:
- Defect:
- Documentation anchors:
- Change summary (1–3 bullet points):
- Validation result:
- GitHub Pages URL:

---

# Next Actions
1. Create Stage 2 mapping notes for DEFECT-001 and DEFECT-002 (read-only).
2. Generate first minimal patch iteration for DEFECT-001.
3. Push to GitHub branch `fix/DEFECT-001` and test via GitHub Pages.

