# Version History

This document tracks the evolution of the Kraken Ledger Report project from Version 4.00 onwards.

## [v4.10-05-DECOUPLING] - 2026-02-26
### Changed
- **Staged Roadmap:** Transitioned to a staged refinement process collecting changes towards a future v5.00 release.
- **Stage 1 Label Decoupling:** Fully decoupled the Deposits section naming logic from Withdrawal recipient data in the Statement Summary. Deposits now consistently default to "Haricom Bank" instead of leaking "Withdrawal (EUR)" strings from the API.
- **Code Cleanup:** Removed duplicate `loadSavedCredentials` function to prevent maintenance errors.

## [v4.10-04-HOTFIX] - 2026-02-26
### Changed
- Improved EUR/GBP rate fetching: Now prioritizes Kraken OHLC data (primary) with Frankfurter as a 5-second fallback.

## [v4.10-03-HOTFIX] - 2026-02-25
### Changed
- Direct Kraken OHLC API integration: Simplified rate fetching by calling the public API directly, removing proxy dependency.

## [v4.10-02] - 2026-02-24
### Changed
- Increased API timeout to 20 seconds to accommodate network latency (e.g., Cloudflare Zero Trust).
- Improved error messaging for API timeouts to identify specific failing calls.

## [v4.10-01-HOTFIX] - 2026-02-24
### Fixed
- Resolved rate fetch stalls by implementing better timeout handling and persistent caching.
- Optimized OHLC skip logic for very old dates.

## [v4.10-00-Baseline] - 2026-02-22
### Added
- Established a clean baseline for future development.
- Synchronized all canonical files and standardized versioning.

## [v4.00-59] - 2026-02-22
### Fixed
- **Critical Bug:** Corrected fiat detection logic where `USDT` was incorrectly swallowed by a loose `includes('USD')` regex. Replaced with strict explicit array matching.

## [v4.00-58] - 2026-02-22
### Added
- Dynamic fiat history lookup for deposits (eliminating reliance on Address Book fallback).
### Fixed
- Rebuilt Crypto matching block to restore legacy behavior for individual crypto addresses.

## [v4.00-57] - 2026-02-22
### Changed
- **Bank Label Normalization:** Removed complex address book fallbacks for fiat assets in favor of direct Kraken API info string matching.

## [v4.00-56] - 2026-02-22
### Fixed
- Resolved missing reconciliation deposits in both the UI and Google Sheets export.

## [v4.00-55] - 2026-02-22
### Changed
- Replaced legacy deposit rendering loop with a standardized 4-column "Haricom Bank Account" format.

## [v4.00-54] - 2026-02-22
### Fixed
- Removed a rogue `continue` statement that was blocking fiat deposits from appearing in the Statement Summary.
- Fixed `ReferenceError` caused by variable scope mismatch (`stmtBankDepositTotals`).

## [v4.00-53] - 2026-02-22
### Changed
- Surgical merge of `generateStatementSummary` and `renderSummaryTable` logic into v4.00-13 to preserve Objective D bank labels while updating math.

## [v4.00-52] - 2026-02-02
### Fixed
- **Phase III-1 Enforcement:** Implemented strict deposit aggregation.
- Cleaned "code leaks" and syntax errors (removed embedded/nested scripts).
- Resolved "w is not defined" crash in Statement generation.

## [v4.00-50] to [v4.00-51] - 2026-02-02
### Added
- **Full Bank Alignment:** Standardized bank labels across TWD, Kraken Statement, and Statement Summary.
- Fixed bank summary deposit display.

## [v4.00-40] - 2026-02-01
### Fixed
- **Button Locking:** Finalized mutual exclusion for "Read Ledger", "Pull Addresses", and "Generate" buttons.
- **Crash Protection:** Added `parseFloat` casting to balance operations to prevent `.toFixed` errors.
- Added missing HTML IDs to the UI buttons.

## [v4.00-01] to [v4.00-13] - Early Feb 2026
### Added
- **Objective D:** Initial implementation of Bank Label Normalization (GBP/EUR).
- Feature: Persistent Google Sheets API keys and OAuth client IDs in API Config.
- Feature: Password manager prompt suppression.
- Security: Removed hard-coded/leaked Google API keys.
