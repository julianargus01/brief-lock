# Pricing Formula

The exact logic `price_calc.py` runs. Plain English here; the code mirrors it line for line. Nothing on this page is improvised by the model — it is all arithmetic the engine does the same way every time.

A reader who follows this page by hand will get the same number the script prints. That is the point.

---

## Step 1 — Score each line item's signals into points

The model reads which signals are present (it does not score them). The engine scores. Each signal adds points:

| Signal | Value | Points |
|---|---|---|
| `integration_count` | 0 | 0 |
| | 1–2 | 1 |
| | 3 or more | 2 |
| `accuracy_critical` | true | 1 |
| `custom_ui` | true | 1 |
| `data_access` | true | 1 |
| `net_new_build` | true | 1 |

A `false` boolean adds 0. Maximum possible = **6 points**.

These weights are shared across every compendium row — the signal taxonomy is universal, applied the same way to every service.

## Step 2 — Points decide the band

| Total points | Band |
|---|---|
| 0–1 | LOW |
| 2–3 | MID |
| 4–6 | HIGH |

Pull the matching **hours** value (LOW / MID / HIGH) from that line item's compendium row. (Thresholds are numeric on purpose — there is no "high complexity" judgment call.)

## Step 3 — Risk buffer on the hours

Hours are an estimate, so the engine pads them:

- **+15%** for a standard build.
- **+25%** for an AI or automation build (edge cases, model drift, integration surprises — the top of the verified 10–25% range).

The buffer rate comes from the compendium row's `buffer` field (`0.25` for ai/automation rows, `0.15` for adjacent rows).

```
buffered_hours = band_hours × (1 + buffer)
```

This is the only buffer applied to hours. It is the "risk buffer." It is not applied twice.

## Step 4 — Price the labor

```
line_labor   = buffered_hours × profile.rate
subtotal     = sum of every line_labor
overhead     = subtotal × profile.overhead_pct      # non-billable PM/admin, default 0.10
price_raw    = subtotal + overhead
price        = max(price_raw, profile.floor)         # never quote below the floor
```

If `price_raw < profile.floor`, the engine returns `price = floor` and flags `floor_applied: true` so the user sees the floor moved the number.

## Step 5 — Monthly run-cost (separate line, never in the build price)

If the line item's compendium row carries `run_cost`, the engine reports it as its **own** line:

> Estimated monthly run-cost (pass-through): $LOW–$HIGH. Not included in the build price. Bill it through, or fold it into a retainer.

This is the cost the persona keeps forgetting (API, hosting, vector DB). It is surfaced, not buried, and it is kept out of the one-time build price so the price stays honest.

## Step 6 — Value-based ceiling (only when the model tree says VALUE-BASED)

When `pricing-model-rules.md` resolves to **value-based**, the engine also computes an ROI-anchored number:

```
value_price = profile.value_share × engagement.roi_amount_usd   # value_share default 0.15
```

It then recommends `max(price, value_price)` with the cost-based `price` named as the floor. Cost-plus is the floor; ROI is the ceiling. (Source: AI/automation work supports 10–25% of first-year ROI — see `service-compendium.md` sources.)

---

## The receipt the engine returns

Every priced line ships with: the signals read, the points, the band, the source tier and row, the buffered hours, and this formula. Same intake in → same number out. A human can audit every step and correct any signal.

## Worked check (hand-calculable)

Line item: `ai-agent-single`, signals `{integration_count: 2, accuracy_critical: true, custom_ui: false, data_access: true, net_new_build: true}`.

- Points: 1 (integrations) + 1 (accuracy) + 0 (ui) + 1 (data) + 1 (net-new) = **4 → HIGH**.
- HIGH hours for `ai-agent-single` = 120. Buffer (ai) +25% → 120 × 1.25 = **150 h**.
- Rate $125 → labor = 150 × 125 = $18,750. Overhead 10% → $1,875. `price_raw` = **$20,625**. Above the $1,500 floor → final **$20,625**.

The script prints this same number. See `sample-output.json`.
