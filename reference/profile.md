# Profile

**This page documents your profile — the one thing you change to make BriefLock yours.** Everything else (the logic, the compendium, the templates) stays as is.

The engine reads a **JSON** profile: a real user's is `profile.json`; the shipped demo is `profile.example.json`. The engine uses `profile.json` if it is present, otherwise the demo. You set it up **once** (SETUP writes the file); after that it is always there, across every session and project. This `.md` is documentation; the engine does not read it.

---

## The fields

| Field | Type | What it is |
|---|---|---|
| `studio_name` | string | Your business name. Used in every document. |
| `rate` | number | Your hourly rate (USD). Drives every price. |
| `floor` | number | Smallest job you'll take. The engine never quotes below it. |
| `overhead_pct` | number | Non-billable PM/admin, added to labor. Default `0.10`. |
| `value_threshold` | number | Annual ROI (USD) above which value-based pricing fires. Default `50000`. |
| `value_share` | number | Slice of first-year ROI a value-based quote targets. Default `0.15`. |
| `service_menu` | string[] | The `service_key`s you sell. The engine blocks any request needing a key not listed. |
| `terms` | object | `payment_schedule`, `revision_cap`, `revision_overage_rate`, `kill_fee_pct`, `late_fee`, `change_order`. `revision_overage_rate` is the **published client-facing** rate for revisions beyond the cap (default `125`) — kept separate from your internal `rate` on purpose, so the client-facing contract never exposes the number the engine prices from. `late_fee` is your own policy, set at SETUP. |
| `past_jobs` | object[] | Optional Tier-1 history: `{service_key, hours, fee, note}`. |
| `brand` | object | Optional. Styles the branded proposal PDF (see below). |

### The `brand` block (optional)

| Field | Default if missing | Used for |
|---|---|---|
| `tagline` | none (omitted) | Sub-line under the name on the proposal. |
| `voice` | "clean, direct, professional" | How the proposal prose reads. |
| `logo` | none → name shown as a text wordmark | Path to a logo image **inside the folder** (`reference/brand/logo.png`). |
| `color_primary` | `#1f2937` (charcoal) | Headings / text accent. |
| `color_accent` | `#2563eb` (blue) | Rules, highlights, the price. |
| `font` | system sans-serif stack | Proposal typeface. |

Every brand field is optional. Anything missing falls back to the default, so the proposal always looks clean — never broken or bare. A user with no brand kit still gets a polished PDF: their name as a styled wordmark on the neutral default theme.

---

## How it gets filled (SETUP)

You do not hand-edit JSON. On first use the agent runs SETUP and writes the file for you. You can either answer its questions or **drop files** and let it extract:

- **Rate card / service menu** → it pulls your rate and your service list.
- **Brand kit** → it pulls your brand values into `brand`, and **copies your logo into `reference/brand/`**, storing the path. (It copies the asset in, so the folder stays self-contained and the pointer never breaks.)
- **Past jobs** → it logs them under `past_jobs` (Tier 1).

## Tier-1 past-jobs (optional flywheel)

```
past_jobs:
  - service_key: rag-pipeline
    hours: 95
    fee: 14000
    note: "Legal-docs Q&A for a 3-person firm, Q1 2026"
```

When a new request's `service_key` matches a logged job, the engine uses your real hours instead of the market band, and the receipt says "based on your past rag-pipeline at 95 h / $14,000." This is a keyed lookup the engine does, not a model guess. Several jobs under one key are averaged; the risk buffer still applies, since a new job carries fresh uncertainty. The demo ships with none, on purpose, to prove the tool needs no personal data to work.

## To retarget by hand

You can also just edit `profile.json` directly: change the rate, trim `service_menu` to what you sell, adjust the terms. To serve a different field entirely, add rows to `service-compendium.md` and list their keys. No code changes either way.
