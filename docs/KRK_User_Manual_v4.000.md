# Kraken Ledger Report — User Manual (v4.000)

## Overview
This tool generates a UK Accounting-compliant Ledger Report for your Kraken account. It converts complex crypto flows into a simple "Bank Statement" view in GBP.

## Workflow
1.  **Set Dates**: Select your Start Date and End Date.
    -   *Recommendation*: For the most accurate "Zero Variance" result, run from your **Account Start** (e.g., 01/01/2020) to Present.
2.  **Step 1: Read Ledger**: Click the button.
    -   *Wait*: The app will fetch all records. The "Generate" button is **disabled** during this time.
    -   *Status*: Watch the purple status bar.
3.  **Step 2: Pull Addresses** (Optional but Recommended):
    -   If requested, enter 2FA to fetch readable names for withdrawal addresses.
4.  **Step 3: Generate Report**: Click "Generate Report".
    -   The report table will appear.

## Exports
-   **Print Summary**: Click "Print PDF" in the blue bar to save the 1-page Summary.
-   **Print Statement**: Click "Display Trade/Withdrawal Report" -> "Print PDF" to save the detailed transaction list.

## Troubleshooting
-   **"Error" on Read**: Check your API Keys in "API Config".
-   **Buttons Disabled**: If a button is grayed out, the app is busy (reading ledger). Wait for it to finish.
-   **Variance**: A small "Reconciliation Difference" (pennies) is normal. A large variance (~£9k) is expected ONLY if you include 2020-2021 XRP history.

## Version Info
-   Current Version: **v4.000**
-   All updates follow strictly **vX.YYY** format (e.g., v4.001).
