# Pricing-Model Rules

Which pricing model to use, and the trap each choice avoids. The engine runs this tree top to bottom and takes the **first match**. Dangerous cases are checked first, so the tool never lands you on the model that loses money.

Inputs (the engagement flags from the intake):

- `scope_bounded` — is the deliverable list fixed and final?
- `client_paced` — does the client control the timeline or the number of iterations?
- `ongoing` — is this a recurring or maintenance relationship?
- `roi_measurable` — is there a quantifiable dollar saving or gain?
- `roi_amount_usd` — that annual dollar figure.

`value_threshold` comes from the profile (default **$50,000/yr**).

---

## The decision tree

**1. HOURLY (time-and-materials)** — if `client_paced == true` **OR** `scope_bounded == false`.
> **Trap avoided:** quoting a flat fee on a fuzzy or client-controlled scope. You eat every overrun. This is the "$60k of work delivered for an under-$20k flat quote" story. When you cannot see the bottom of the scope, you bill for time, not for a guess.

**2. RETAINER** — else if `ongoing == true`.
> **Trap avoided:** a one-time fee on a relationship that keeps asking for more. You give away maintenance for free and leave predictable recurring revenue on the table. Recurring work gets a recurring price.

**3. VALUE-BASED** — else if `roi_measurable == true` **AND** `roi_amount_usd >= value_threshold`.
> **Trap avoided:** billing hourly on an automation that prints money for the client. Cost-plus caps your pay at your hours while the client banks the gain forever. Price a slice of the value (see the value ceiling in `pricing-formula.md`), not just your time.

**4. FLAT** — else (the scope is bounded and estimable, no big measurable ROI, not ongoing).
> **Trap avoided:** billing hourly on a clean, bounded deliverable. It caps your upside if you work fast and it signals low confidence to the client. A defined deliverable gets a defined price.

---

## How the engine reports it

The decision object names the model, the branch that fired, and the trap that branch avoided — for example:

> **Model: HOURLY.** Fired on `scope_bounded = false`. Avoids quoting a flat fee on an open scope and eating the overruns.

The model recommendation always carries its reason. No silent defaults.

## When the flags are missing

If the flags needed to resolve the tree are all `null` (the request did not say whether the scope is bounded, ongoing, or measurable), the engine cannot pick a model honestly. It routes to **QUOTE-BLOCKED** and returns the discovery questions that fill those flags (see `../rules.md`). It does not default to flat and hope.

**A bounded scope is a deliberate FLAT default — so read the `ongoing` and `roi_measurable` signals.** When `scope_bounded = true`, FLAT is chosen even if `ongoing`/`roi_measurable` weren't flagged: a bounded job with no ongoing-work and no measurable-ROI signal *is* a flat job, and that is an honest default, not a guess. But the engine can only weigh the signals you give it — so set `ongoing = true` for a retainer-shaped ask, and `roi_measurable = true` (with `roi_amount_usd`) when the client names a dollar gain. Don't let a retainer or a high-ROI job fall through to FLAT by leaving those blank; if you genuinely can't tell whether it's ongoing or ROI-bearing, leave the relevant flag `null` and QUOTE-BLOCK to ask.
