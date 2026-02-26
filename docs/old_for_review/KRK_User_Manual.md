# Kraken Ledger Report — User Manual (vv3.044)

## What this tool does
- Fetches Kraken ledger activity for a selected date range.
- Produces:
  - Kraken Statement: detailed ledger-derived statement view.
  - Statement Summary: totals, withdrawals by recipient, fees, and closing balances with GBP equivalents.
- Exports:
  - PDF: Kraken Statement Summary.
  - PDF: Kraken Statement (multi-page).

## Typical workflow
1. Set Start Date and End Date.
2. Click "Fetch & Generate Report".
3. Open "Kraken Statement" to view the detailed statement.
4. Open "Statement Summary" to view aggregated totals and GBP equivalents.
5. Use Print-to-PDF buttons to export:
   - "Kraken Statement Summary" PDF.
   - "Kraken Statement" PDF (multi-page).

## How GBP equivalents are computed
- GBP row: GBP Equivalent displays "n/a".
- EUR/USDT/XRP rows:
  - If balance is 0 → GBP Equivalent shows 0.00.
  - If balance > 0 → GBP Equivalent uses end-date FX rate logic with fallbacks.

## Printing to PDF
- Printing opens the browser print dialog.
- Recommended "Save to PDF" destination.
- Default filename includes the date range (as displayed in the UI).
- Both PDFs include:
  - Main header: "Kraken Reports v3.044"
  - Subheader indicating whether the output is Statement or Statement Summary, plus date range.

## Reliability tips
- Changing the date range triggers a fresh summary computation automatically.
- Re-clicking Statement Summary without changing the date range reuses computed results.
- If any result looks inconsistent:
  - Review the Trace panel for:
    - Date range
    - Ledger record counts
    - FX rates cached/fetched
    - Summary generation row counts

## Known constraints
- Requires valid Kraken API credentials and proxy configuration as configured in the app.
- Large ranges increase runtime due to FX rate lookups and summary computation.
