# Kraken Ledger Report — Project Notes (Antigravity/OpenCode Ready)

## Current release
- App Version: v3.045
- Single-file web app served via GitHub Pages from repo root:
  - `kraken-ledger-report/Kraken Ledger Report.html`

## Purpose
- Fetch Kraken ledger entries for a date range.
- Generate:
  - Kraken Statement (multi-page table).
  - Statement Summary (aggregations, GBP equivalents, fees, closing balances).
- Export:
  - PDF: Kraken Statement Summary.
  - PDF: Kraken Statement (multi-page).

## Critical behaviours proven in this chat
### A. App stability fixes
- Resolved console errors that previously broke button handlers:
  - Missing `logTrace` reference.
  - Invalid `await` usage outside `async` context.
  - Missing `saveCacheToLocalStorage` reference during summary build.

### B. Versioning consistency (header + trace)
- A single constant is used as source of truth:
  - `APP_VERSION`
- Header label and Trace first line must both be derived from `APP_VERSION`.
- Release rule: bump version for every GitHub deployment; sub-versions permitted for rapid fixes.

### C. Closing Balances GBP equivalents (Statement Summary)
- GBP row: GBP Equivalent displays `n/a`.
- EUR / USDT / XRP rows:
  - Balance == 0 → GBP Equivalent shows `0.00` (not dash).
  - Balance > 0 → compute GBP Equivalent using end-date rate logic already present (no new architecture).
- Dash `-` only when no rate can be obtained after fallbacks; should be rare.

### D. Statement Summary recompute and cache reset
- Date-range fingerprint: `startDate|endDate`
- Behaviour:
  - If date-range changed → reset *derived summary state* and recompute.
  - If unchanged → reuse existing computed summary (display again without recompute).
- Caution: do **not** clear `withdrawalCache` when recomputing summary; it is required for "Withdrawals to Recipients" GBP equivalents fallback matching.
- FX rates caching:
  - Internal cache exists (observed via Trace: "Using cached rates ...").
  - Rates should be recomputed only when required (new dates); otherwise reuse.

### E. Sheets ID persistence fix
- Sheet ID stored in localStorage must not be overwritten by blank value on "Save API Keys".
- On refresh, Sheet ID field must re-populate from storage.

### F. PDF export (print-to-PDF)
- Two buttons now exist in Statement Summary controls:
  - Print PDF: Kraken Statement Summary (single/multi-page depending on content).
  - Print PDF: Kraken Statement (multi-page; table content).
- Formatting requirements:
  - Reasonable margins in print CSS (approx 0.5–1.0 cm).
  - PDF filename default includes date range in required format.
  - Header + subheader included:
    - Main header: "Kraken Reports v3.045"
    - Subheader for Summary: "Kraken Statement Summary <range>"
    - Subheader for Statement: "Kraken Statement <range>"

## Guardrail note (future)
- If Statement/Summary/PDF buttons are moved earlier in the UI (e.g., header toolbar), implement a guardrail:
  - Disable/hide print and summary actions until source data exists (statement rows generated).

## Observability (Trace)
- Trace is treated as primary debug surface.
- Ensure trace lines exist for:
  - Date range chosen.
  - Ledger fetch batches and totals.
  - FX rate strategy: cached vs fetched; fallback sources used.
  - Summary generation: cache vs source-of-truth rows.
  - Any fallback misses (e.g., recipient withdrawal matching).

## Deployment protocol and change packaging
### Version Control rule-set
- Every change pushed to GitHub increments version.
- Format options:
  - Main releases: v3.045, v3.045, ...
  - Rapid bug-fix subreleases: v3.045-1, v3.045-2, ...
- A subrelease stays within the same functional scope; once stable, next new feature uses next main version.

### Patch delivery rule-set
- Deliver exactly one updated HTML file per patch.
- Provide exactly one command block for:
  - `cp` over `Kraken Ledger Report.html`
  - `git add`, `git commit -m`, `git push`

## Current file structure quick index (auto-extracted)
### Notable functions (partial; extracted)
_safeTrace, arrayBufferToBase64, base64ToArrayBuffer, boot, calculateGBPEquivalent, calculateGbpValue, callKrakenPrivateAPI, copyAddressesToClipboard, copyBankReport, copyLedgerToClipboard, copyNodeText, copyReportToClipboard, copySummaryReport, copyTraceToClipboard, createKrakenSignature, ensureTokenThen, escHtml, extractDestTag, extractFiatCurrency, extractWallet, fetchAndGenerateReport, fetchKrakenAddresses, fetchOHLC, fetchWithdrawalHistory, filterBankReport, filterDetails, findFiatCounterpart, findMatchingTrade, formatTime, formatTimestamp, gapiLoaded, generateBankReport, generateReport, generateReportFromCache, generateStatementSummary, getApiCredentials, getDateRangeKey, getKrakenRate, getSelectedProxy, getWithdrawCredentials, gisLoaded, handleDateChange, handleProxyChange, handleReportReset, handleResetConfirm, handleSync, handleWipeConfirm, initRefresh, loadLocalData, loadSavedCredentials, localReset, logTrace, parseDateString, printKrakenStatement, printStatementSummary, pullAddresses, readLedger, renderAddressTable, renderBankTable, renderLedgerTable, renderPreview, renderSummaryTable, requestToken, resetGenerateButton, resetStatementDerivedState, saveApiConfig, saveCacheToLocalStorage, saveLocalData, saveSheetId, toggleAddressViewer, toggleApiConfig, toggleBankReport, toggleLedgerViewer, toggleLog, toggleReportViewer, toggleSummaryReport, updateBankButtonLabel, updateGlobalRecordCounts, updateStatus, updateStatusCounts ...

### Notable DOM ids (partial; extracted)
addressCount, addressTable, addressTableBody, addressViewerSection, address_btn, apiConfigSection, api_btn, appVersion, auth_status, bankReportArea, bankStmtTable, btn_bank_statement, btn_statement_summary, corsProxy, corsProxySelect, descFilterInput, endDate, generate_btn, googleSheetId, krakenApiKey, krakenPrivateKey, ledgerTable, ledgerTableBody, ledgerViewerSection, ledger_btn, log_btn, previewArea, report_btn, resetBtn, stagingHint, startDate, statusSummary, summaryReportArea, trace_log, typeFilterInput, wipeBtn, withdrawApiKey, withdrawPrivateKey, withdrawalCount

### LocalStorage keys observed
g_token, g_token_expires_in, g_token_issued_at, kraken_api_key, kraken_bank_staging, kraken_cors_proxy, kraken_cors_proxy_type, kraken_last_date_range, kraken_private_key, kraken_sheet_id, kraken_staging, kraken_summary_staging, kraken_v2_addresses, kraken_v2_history, kraken_v2_rates, kraken_v2_withdrawals, kraken_v3_withdrawal_cache, kraken_withdraw_api_key, kraken_withdraw_private_key

### External endpoints observed (partial)
- https://accounts.google.com/gsi/client
- https://api.allorigins.win/raw?url=
- https://api.frankfurter.app/${dateStr}?from=USD&to=GBP`;
- https://api.kraken.com
- https://api.kraken.com/0/public/OHLC?pair=
- https://apis.google.com/js/api.js
- https://cors-anywhere.herokuapp.com/
- https://corsproxy.io/?
- https://docs.google.com/spreadsheets
- https://min-api.cryptocompare.com/data/v2/histoday?fsym=XRP&tsym=USD&limit=1&toTs=${timestamp}`;
- https://www.googleapis.com/auth/spreadsheets

## Next-stage improvement ideas (non-blocking)
- UI sequencing and button layout refinement (Statement vs Summary vs PDFs).
- Consolidated export workflow (print statement + summary as a single combined export).
- Defensive input validation (date range, missing keys).
- Make caches explicit and documented (rates cache, withdrawal cache).

## Statement Summary — Reconciliation Difference
- Add a final section in Statement Summary that displays a single GBP figure labelled **Reconciliation Difference**.
- Explanation text:
  - “A reconciliation difference of GBP 74.62 exists because GBP equivalents in the summary are computed using average/available rates for the period and may involve rounding and fallback pricing sources.”
