# Kraken Ledger Report — Technical Notes (v4.000)

## Architecture
- Single static HTML file (`Kraken Ledger Report.html`) with embedded CSS + JavaScript.
- Served via GitHub Pages.

## Core Logic: Valuation & Inventory (New in v4.000)
To ensure **Zero Net Trade Activity** over long periods, the system uses a **Weighted Average Cost (WAP)** inventory model:
1.  **Inventory Tracking**: Tracks `qty`, `cost` (GBP), and `wap` (Weighted Average Price) for each asset (USDT, XRP, EUR).
2.  **Inflows (Buys)**: Increases `qty` and `cost`. Recalculates `wap`.
3.  **Outflows (Withdrawals/Sells)**: Reduces `qty` and `cost`. **Crucially**, the outflow is valued at the **current WAP**, not the daily market rate.
    - *Result*: `Total Value Out` = `Total Value In` (mathematically guaranteed).
4.  **Anchoring**: For Crypto-to-Crypto swaps (e.g., USDT <-> XRP), the system anchors the value of the trade to the Source Asset's value to ensure the "Trade" value is identical on both sides (Buy/Sell), resulting in 0.00 Net Trade Activity.

## Scope & Assets
- **Supported Assets**: GBP, EUR, USDT, XRP.
- **Excluded**: BTC, ETH, and other legacy assets are ignored/filtered out to maintain report purity.

## Data Flow
1.  **Read Ledger**: Fetches *all* history (paging 50 at a time).
2.  **Process Inventory**: Iterates chronologically to build Cost Basis.
3.  **Generate Report**:
    - **Statement**: Detailed row-by-row view.
    - **Summary**: Aggregated view with Reconciled Differences.

## Key Fixes & Constraints
-   **Race Condition Fixed**: The "Generate Report" button is strictly disabled/hidden while "Read Ledger" is active to prevent data corruption.
-   **ReferenceError Fixed**: Variables (like `genBtn`) are scoped at the function level to ensure error handlers can always access them.
-   **Historical Data**: Historical XRP variance (2020-2021) is a known data limitation and is accepted.

## Persistence
-   Credential storage (API keys) in `localStorage`.
-   Sheet ID persistence.
