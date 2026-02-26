Here is the logic the program follows for each step of the process:

Step 1: Read Ledger (Button: "Read Ledger")

* Input: Date Range (Start/End), API Key (Query).
* Logic:
    1. Calls Kraken's Ledgers API endpoint.
    2. Fetches transactions in batches of 50.
    3. Filtration: It only keeps entries relevant to your report:
        * Crypto: USDT, XRP (and XXRP).
        * Fiat: GBP, EUR, USD.
    4. Storage: Saves these raw entries into memory (count: Ledger (...)).

* Outcome: You see the "Ledger" count increase (e.g., 660). These are the raw building blocks.

Step 2: Pull Addresses (Button: "Pull Addresses")

* Input: API Key (Withdraw/Fund), 2FA Code (if applicable).
* Logic:
    1. Calls Kraken's WithdrawAddresses API.
    2. Retrieves the list of saved withdrawal addresses (e.g., "Revolut", "Ledger Nano").
    3. Storage: Saves this list to cacheData.krakenAddresses.
* Purpose: The Ledger only gives a cryptic code (e.g., GC6...). This step provides the "dictionary" to translate that code into a human-readable name (e.g., "Revolut Ltd").

Step 3: Generate Trade/Withdrawal Report (Button: "Generate Report")

* Input: The raw Ledger data + The Addresses list.
* Logic:
    1. Iterates through every line in the Ledger.
    2. Enrichment:
        * Recipient: Matches the destination address against your Address list.
        * Rates: Checks the date of the transaction and fetches the GBP/EUR exchange rate for that specific day (via CryptoCompare API if not cached).
        * Classification: Determines if it’s a Trade, Withdrawal, or Deposit.
    3. Formatting: Formats the values (fees, amounts) for the table.
    4. Storage: Populates stagingRecords.

* Outcome: Updates the "Trade/Withdrawal Report" count. This is a flat list of all actions.

Step 4: Kraken Statement (Button: "Kraken Statement")
* Input: The raw Ledger data (again).
* Logic:
    1. Sorting: strictly sorts by Date/Time.
    2. Balance Calculation: Starts from 0 (or a calculated opening balance) and replays every single transaction to create a "Running Balance" for each asset.
    3. Merging: If it sees a "Trade" where you sold USDT for GBP, it attempts to merge these two ledger lines into a single "Exchange" line item.
    4. Storage: Populates bankRecords.
* Outcome: Updates the "Statement Report" count. This usually matches the specific date filtered view.

Step 5: Statement Summary (Button: "Statement Summary")
* Input: The Statement Report data (bankRecords).
* Logic:
    1. Aggregation: Loops through the Statement Report.
    2. Grouping: Groups amounts by Recipient.
    3. Sums up the totals (e.g., Total sent to "Revolut", Total sent to "Binance").
    4. Storage: Populates summaryRecords.
* Outcome: Displays the final summary tables. This does not have a "record count" in the same way, as it is a summary of the Statement Report."