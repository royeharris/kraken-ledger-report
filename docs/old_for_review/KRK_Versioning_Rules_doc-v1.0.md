# KRK Versioning Rules (Application)
Document Version: v1.0  
Purpose: consistent, human-friendly version numbering for controlled development and urgent hotfixes.

---

## 1. Concepts

- **Base version**: reserved for one functionality goal.
  Example: `v4.00-13` = “Objective D completion”.

- **Fix counter**: used while stabilising that same functionality goal.
  Example: `v4.00-13-00`, `v4.00-13-01`, `v4.00-13-02`.

- **Hotfix**: urgent fix unrelated to the current functionality goal.
  Hotfixes must not change scope or trigger new feature work.

---

## 2. Standard pattern (functionality work)

- Start functionality: `v4.00-13-00`
- Fix attempts: `v4.00-13-01`, `v4.00-13-02`, ...
- Functionality complete → next base version:
  `v4.00-14-00`

Rule:
- New base version = new functional objective.
- Fix counter increment = defect fixing for the same objective.

---

## 3. Hotfix pattern (urgent unrelated defect)

If working on `v4.00-13-02` and an unrelated urgent defect appears:

- Create hotfix versions under the same base/fix, with a hotfix suffix:
  - `v4.00-13-02-hotfix-00`
  - `v4.00-13-02-hotfix-01`
  - `v4.00-13-02-hotfix-02`

When the hotfix is verified:
- Return to the previous track and continue the fix counter if needed:
  - back to `v4.00-13-03` (feature track continues)

Rule:
- Hotfix suffix is only for urgent unrelated fixes.
- Hotfix must be logged and verified like any other version.
- Hotfix must not expand scope.

---

## 4. File naming convention for saved versions

Every saved HTML version file should include:
- the version number
- a short descriptor

Example:
- `Kraken_Ledger_Report_v4.00-13-02_ObjectiveD_labels.html`
- `Kraken_Ledger_Report_v4.00-13-02-hotfix-01_Remove_Exposed_Key.html`

---

## 5. Suggested repo structure

- `report.html` (or the “live” file used by GitHub Pages)
- `versions/` (archive of every published version file)

Example:
- `versions/Kraken_Ledger_Report_v4.00-12_Baseline.html`
- `versions/Kraken_Ledger_Report_v4.00-13-00_ObjectiveD_start.html`
- `versions/Kraken_Ledger_Report_v4.00-13-02-hotfix-00_API_exposure_fix.html`

---

End of document.
