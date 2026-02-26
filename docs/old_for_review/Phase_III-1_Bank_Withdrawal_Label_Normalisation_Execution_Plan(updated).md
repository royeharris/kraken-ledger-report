# Phase III-1 — Bank Withdrawal Label Normalisation

## Status
**CONFIRMED with REVISION (multi-account safe).**

This document is the single authoritative execution plan to be handed to the Antigravity agent, equivalent in role and rigor to the Phase II rebuild checklist and handover.

---

## Why this revision exists
The earlier draft included a **single verified candidate** fallback for fiat (ZGBP/ZEUR). That fallback is safe but **not sufficient** if there are **multiple verified bank addresses for the same fiat asset** (e.g., two ZGBP accounts).

This revision adds a deterministic, transaction-driven join that works for:
- one bank account per currency
- multiple bank accounts per currency

and preserves the single-candidate shortcut only as a last-resort fallback.

---

## Objective
Normalize **fiat withdrawal (GBP / EUR) recipient labels** so they are resolved and displayed consistently across:
- Withdrawals / Deposits / Trades report (TWD report)
- Kraken Statement
- Kraken Statement Summary

The change is strictly a **presentation-layer overlay**. No numeric logic, reconciliation logic, or aggregation paths may change.

---

## Scope classification
- **Change type:** Safe overlay  
- **Permitted impact:** String labels only  
- **Forbidden impact:** Any change to amounts, balances, reconciliation, FX logic, or trade math  

---

## Correct asset model (critical)

| Asset | Meaning | Included |
|------|--------|----------|
| USDT | Crypto (Tether) | Yes |
| XRP  | Crypto | Yes |
| ZGBP | Fiat GBP balance | Yes |
| ZEUR | Fiat EUR balance | Yes |
| ZUSD | Fiat USD balance | **No (out of scope)** |

There are **no USD bank withdrawals** in this application.  
Any invalid symbol such as **ZUSDT** must not be used.

---

## Kraken API feasibility + required permissions (verification gate)

### Why the transactional join is expected to work
- Ledger entries include a `refid` that is the “Reference Id of the parent transaction (trade, deposit, withdrawal, etc.)”. This is the designed linkage for funding events. (Kraken REST: Get Ledgers / Query Ledgers) https://docs.kraken.com/api/docs/rest-api/get-ledgers-info/
- Kraken funding endpoints use `refid` as the withdrawal identifier (e.g., `Withdraw` returns `refid`; `WithdrawCancel` accepts `refid`). (Kraken Support: “Funding via the API”) https://support.kraken.com/hc/en-us/articles/13307454640020-Funding-via-the-API
- Therefore, the intended deterministic link is: **Ledger.refid ↔ WithdrawStatus(refid)**, and then **WithdrawStatus.key ↔ WithdrawAddresses.key**. (WithdrawAddresses defines `key` as the withdrawal key name.) https://docs.kraken.com/api/docs/rest-api/get-withdrawal-addresses/

### Required API-key permissions (must be enabled or the join will fail)
- **WithdrawStatus**: requires `Funds permissions - Withdraw` or `Data - Query ledger entries`. https://docs.kraken.com/api/docs/rest-api/get-status-recent-withdrawals/
- **WithdrawAddresses**: requires `Funds permissions - Query` AND `Funds permissions - Withdraw`. https://docs.kraken.com/api/docs/rest-api/get-withdrawal-addresses/
- **QueryLedgers / Ledgers**: requires `Data - Query ledger entries`. https://docs.kraken.com/api/docs/rest-api/get-ledgers-info/

### Verification gate (must be run before implementing multi-bank logic)
For at least one known bank withdrawal (ZGBP or ZEUR):
1) Confirm the ledger row has `refid`.
2) Confirm WithdrawStatus results include a record whose `refid` matches that ledger `refid`.
3) Confirm that WithdrawStatus record includes either:
   - `key` directly (preferred), or
   - enough fields to map deterministically to a key (see fallback below).
4) Confirm WithdrawAddresses contains that key for the same asset and the entry is verified.

If step (2) or (3) fails, proceed with the fallback strategy below (still safe overlay), and record the limitation for Phase III-A diagnostics.

### Deterministic fallback if WithdrawStatus does not expose `key`
If WithdrawStatus does not provide `key` for fiat withdrawals, then resolve bank destination by matching on a constrained tuple:
- asset (ZGBP/ZEUR)
- method (if provided)
- amount (exact string match preferred)
- timestamp proximity (within a strict tolerance window, e.g., ±2 minutes)

Only apply this fallback when the tuple produces exactly one candidate; otherwise return null (do not guess).


---

## Core insight (root cause)
Kraken represents:
- **Crypto withdrawals** using wallet address + optional tag/memo
- **Fiat withdrawals** using a **withdrawal key** (saved bank address name)

For fiat withdrawals:
- address-like fields may be blank/redacted
- the stable identifier is the **withdrawal key**
- the stable transactional join is the **withdrawal refid** (ledger ↔ withdrawal status)

Therefore fiat bank withdrawals must be resolved by:
1) **refid → withdrawal status → key**, then  
2) **key → WithdrawAddresses entry**, then  
3) **display = first two words of key**

---

## Withdrawal classes

| Class | Assets | Deterministic join | Resolution method |
|------|--------|--------------------|-------------------|
| Crypto → recipient | USDT, XRP | address (+ tag/memo) | WithdrawAddresses lookup |
| Fiat → bank | ZGBP, ZEUR | **refid** | WithdrawStatus(refid) → key → display |

Both classes use the **same WithdrawAddresses table** but must be resolved differently.

---

## Canonical resolution rule
All reports must use **one shared resolver**.

### Display rule
- Use **first two words** of the resolved Kraken WithdrawAddresses **key**
- Remove parentheses/suffixes first
- **Do not append asset names** to labels (asset is already visible in columns)
- **No bank names may be hard-coded** (must work for any bank)

Examples:
- `"Revolut B (EUR)" → "Revolut B"`
- `"Revolut Business" → "Revolut Business"`
- `"Santander B (GBP)" → "Santander B"`
- `"Aleksey Trofimov (USDT)" → "Aleksey Trofimov"`

---

## Implementation steps (exact)

### Patch 1 — Withdrawal status coverage (assets + refid index)
**Function:** `fetchWithdrawalHistory()`

1) Replace queried asset list with:

```js
const assets = ["USDT", "XXRP", "ZGBP", "ZEUR"];
```

2) Build a dictionary keyed by **refid** (critical for multi-bank support):

```js
// After fetching and normalizing withdrawal status records into an array `all`:
cacheData.withdrawalHistoryByRefid = {};
for (const w of all) {
  if (w && w.refid) cacheData.withdrawalHistoryByRefid[w.refid] = w;
}
```

Notes:
- `cacheData.withdrawalHistory` may continue to exist, but resolution must prefer `withdrawalHistoryByRefid` when refid is available.

---

### Patch 2 — Add canonical resolver (new helper)
Add the following helper functions near existing utility helpers (before report builders):

```js
function resolveRecipientLabel({ asset, refid, historyMatch, krakenAddresses, withdrawalHistoryByRefid }) {
  // --- 1) Fiat bank withdrawals (ZGBP/ZEUR): prefer refid → key ---
  if (asset === "ZGBP" || asset === "ZEUR") {
    const w = (refid && withdrawalHistoryByRefid) ? withdrawalHistoryByRefid[refid] : null;

    // If WithdrawStatus provides a withdrawal key (common for fiat), use it
    if (w && w.key) return trimLabel(w.key);

    // If key is not present, try to resolve by matching info/address fields to address book key
    // (best-effort; may be empty for fiat)
    if (w && w.info) {
      const k = tryMatchKeyFromInfo(w.info, krakenAddresses, asset);
      if (k) return trimLabel(k);
    }

    // Last-resort fallback: ONLY if there is exactly one verified address for this asset
    const candidates = krakenAddresses.filter(a => a.asset === asset && a.verified === true);
    if (candidates.length === 1) return trimLabel(candidates[0].key);

    // Ambiguous: multiple candidates and no key => do not guess
    return null;
  }

  // --- 2) Crypto withdrawals (USDT/XRP): address+tag join ---
  if (asset === "USDT" || asset === "XRP") {
    if (historyMatch?.address) {
      const addr = krakenAddresses.find(a =>
        a.address === historyMatch.address &&
        (a.tag || "") === (historyMatch.tag || "")
      );
      if (addr?.key) return trimLabel(addr.key);
    }
  }

  // --- 3) Generic fallback ---
  if (historyMatch?.info) return trimLabel(historyMatch.info);

  return null;
}

function tryMatchKeyFromInfo(infoStr, krakenAddresses, asset) {
  if (!infoStr) return null;
  const n = norm(infoStr);
  for (const a of krakenAddresses) {
    if (a.asset !== asset) continue;
    if (a.key && norm(a.key) === n) return a.key;
  }
  return null;
}

function norm(s) {
  return String(s).toUpperCase().replace(/\s+/g, " ").trim();
}

function trimLabel(str) {
  return String(str)
    .replace(/\(.*?\)/g, "")
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .join(" ");
}
```

Key safety properties:
- If multiple bank accounts exist per currency, the resolver uses **refid → key** and stays deterministic.
- If refid→key is missing and multiple candidates exist, the resolver returns null (safe) rather than guessing.

---

### Patch 3 — Apply resolver in TWD report
Replace existing recipient derivation logic with:

```js
const label = resolveRecipientLabel({
  asset: row.asset,
  refid: row.refid,
  historyMatch,
  krakenAddresses: cacheData.krakenAddresses,
  withdrawalHistoryByRefid: cacheData.withdrawalHistoryByRefid
});

if (label) row.recipient = label;
```

Remove any logic that appends `(USDT)` or similar suffixes to recipient names.

---

### Patch 4 — Apply resolver in Statement row construction
When building `bankRecords`, apply:

```js
const label = resolveRecipientLabel({
  asset: cleanAsset,
  refid: e.refid,
  historyMatch,
  krakenAddresses: cacheData.krakenAddresses,
  withdrawalHistoryByRefid: cacheData.withdrawalHistoryByRefid
});

if (label) {
  detail = label;
  recipient = label;
}
```

---

### Patch 5 — Stop appending asset to resolved labels
Replace:

```js
if (detail && !detail.includes(cleanAsset)) {
  detail += ` (${cleanAsset})`;
}
```

With:

```js
if (!label && detail && !detail.includes(cleanAsset)) {
  detail += ` (${cleanAsset})`;
}
```

---

## Regression checklist (mandatory)

### Must remain identical
- Deposits totals
- Withdrawals totals
- Fees
- Closing balances
- Reconciliation difference
- Net trade activity

### Must change
- For any fiat bank withdrawal (ZGBP/ZEUR), the displayed label must be derived **dynamically** from WithdrawStatus/WithdrawAddresses **key**, then rendered as **first two words of key**.
- The same derived label must appear identically in:
  - TWD report
  - Statement
  - Statement Summary
- **No hard-coded bank names** are permitted.

---

## Documentation update (additive)
Add a section titled **“Withdrawal Label Resolution”** describing:
- Two withdrawal classes
- Why fiat has no wallet address fields usable for joining
- Multi-account safe strategy: `refid → WithdrawStatus(key) → label`
- Labels are presentation-only and do not affect reconciliation

---

## Mini-handover summary (for Antigravity)
Rules:
- No numeric logic changes permitted
- One canonical resolver
- ZGBP + ZEUR supported
- ZUSD excluded
- Identical labels across all reports
- Dynamic key-driven labels only (no bank-name hard-coding)
- Multi-account safe: prefer `refid → key`, never guess when ambiguous

**Expected result:** Stable v4.01 with consistent bank withdrawal labelling, including multi-bank-per-currency support.

---

## Next phase
After Phase III-1 is complete and validated, proceed to **Phase III-A diagnostics**.
