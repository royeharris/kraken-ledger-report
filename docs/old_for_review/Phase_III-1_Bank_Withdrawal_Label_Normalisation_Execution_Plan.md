# Phase III-1 — Bank Withdrawal Label Normalisation

## Status
**CONFIRMED** for execution.

This document is the single authoritative execution plan to be handed to the Antigravity agent, equivalent in role and rigor to the Phase II rebuild checklist and handover.

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

## Core insight (root cause)
Kraken represents:
- **Crypto withdrawals** using wallet address + optional tag/memo
- **Fiat withdrawals** using a **withdrawal key** (saved bank address name)

For fiat withdrawals:
- `address` may be blank
- `bank info` may be blank or redacted
- the **withdrawal key is the stable identifier**

Therefore fiat bank withdrawals must be resolved by **key-oriented logic**, not wallet-style logic.

---

## Withdrawal classes

| Class | Assets | Identifier | Resolution method |
|------|--------|------------|-------------------|
| Crypto → recipient | USDT, XRP | Wallet address + tag | Address table lookup |
| Fiat → bank | ZGBP, ZEUR | Withdrawal key | Key-based lookup |

Both classes use the **same address table** but must be resolved differently.

---

## Canonical resolution rule
All reports must use **one shared resolver**.

### Display rule
- Use **first two words** of the resolved Kraken WithdrawAddresses **key**
- Remove parentheses/suffixes first
- **Do not append asset names** to labels (asset is already visible in columns)
- **No bank names may be hard-coded** (must work for any bank, e.g., Revolut, Santander, etc.)

Examples:
- `"Revolut B (EUR)" → "Revolut B"`
- `"Revolut Business" → "Revolut Business"`
- `"Santander B (GBP)" → "Santander B"`
- `"Aleksey Trofimov (USDT)" → "Aleksey Trofimov"`

---

## Implementation steps (exact)

### Patch 1 — Withdrawal history asset set
**Function:** `fetchWithdrawalHistory()`

Replace the queried asset list with:

```js
const assets = ["USDT", "XXRP", "ZGBP", "ZEUR"];
```

Remove any inclusion of `ZUSD`.

---

### Patch 2 — Add canonical resolver (new helper)

Add the following helper functions near existing utility helpers (before report builders):

```js
function resolveRecipientLabel({ asset, historyMatch, krakenAddresses }) {
  // Crypto withdrawals
  if (asset === "USDT" || asset === "XRP") {
    if (historyMatch?.address) {
      const addr = krakenAddresses.find(a =>
        a.address === historyMatch.address &&
        (a.tag || "") === (historyMatch.tag || "")
      );
      if (addr?.key) return trimLabel(addr.key);
    }
  }

  // Fiat withdrawals
  if (asset === "ZGBP" || asset === "ZEUR") {
    const candidates = krakenAddresses.filter(a =>
      a.asset === asset && a.verified === true
    );
    if (candidates.length === 1) {
      return trimLabel(candidates[0].key);
    }
  }

  // Fallback
  if (historyMatch?.info) return trimLabel(historyMatch.info);

  return null;
}

function trimLabel(str) {
  return str
    .replace(/\(.*?\)/g, "")
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .join(" ");
}
```

---

### Patch 3 — Apply resolver in TWD report
Replace existing recipient derivation logic with:

```js
const label = resolveRecipientLabel({
  asset: row.asset,
  historyMatch,
  krakenAddresses: cacheData.krakenAddresses
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
  historyMatch,
  krakenAddresses: cacheData.krakenAddresses
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
- For any fiat bank withdrawal (ZGBP/ZEUR), the displayed label must be derived **dynamically** from Kraken WithdrawAddresses **key** for the matched bank destination, then rendered as **first two words of key**.
- The same derived label must appear identically in:
  - TWD report
  - Statement
  - Statement Summary
- **No hard-coded bank names** are permitted.

---

## Documentation update (additive)
Add a section titled **“Withdrawal Label Resolution”** describing:
- Two withdrawal classes
- Why fiat has no wallet address
- Key-based resolution
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

**Expected result:** Stable v4.01 with consistent bank withdrawal labelling.

---

## Next phase
After Phase III-1 is complete and validated, proceed to **Phase III-A diagnostics**.
