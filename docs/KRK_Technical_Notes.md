# Kraken Ledger Report — Technical Notes (vv3.044)

## Architecture
- Single static HTML file with embedded CSS + JavaScript.
- Served via GitHub Pages at repo root as:
  - `Kraken Ledger Report.html`

## Data flow
1. Read date range.
2. Call Kraken API (Ledgers) with pagination (`offset` batches).
3. Build normalized ledger entries list.
4. Generate report table (Kraken Statement).
5. Build Statement Summary from "source-of-truth" statement rows.
6. Compute GBP equivalents using FX rates (cached/fallback strategy).
7. Provide PDF exports using print CSS and programmatic print windows/sections.

## Key caches
- FX rates cache (observed in Trace: "Using cached rates for N dates").
- Withdrawal matching cache (recipient mapping / fallback) used to compute GBP equivalents for withdrawals-to-recipients.
- Statement Summary derived state (totals, closing balances, fees, etc.).

## Date-range fingerprinting
- Key: `startDate|endDate`
- On change:
  - Reset derived summary state.
  - Do NOT clear withdrawal cache (required for GBP equivalents fallback).
  - FX rate caching may be retained; new dates are fetched as needed.

## Persistence
- Credentials stored in localStorage (API config, proxy, sheet id).
- Sheet ID persistence rule:
  - Blank input must not overwrite stored Sheet ID.
  - On load, populate UI from storage.

## PDF export implementation
- Summary and Statement each have a dedicated print action.
- Print CSS enforces margins; multi-page table should paginate naturally.
- Output includes header + range subheader; filename includes date range.

## Change control checklist (every patch)
- Update `APP_VERSION` only once; header + trace must derive from it.
- Confirm Trace contains:
  - `Trace: v3.044 ... initialized.`
- Confirm no console errors.
- Run the "date-range switching" sequence to validate:
  - Summary recompute on change.
  - No "No match in withdrawalCache" spam.
  - Withdrawals-to-recipients GBP equivalents populated.
