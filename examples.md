# Examples

Worked quotes. The point is the **judgment** — watch where I only label and the code computes the number, where a "simple flat job" should really be billed hourly, and where a vague request earns questions instead of a price. Several of these are edge cases the obvious approach gets wrong. Every number is exactly what `reference/price_calc.py` prints on the shown intake against the demo profile. Examples calibrate the rules; they never override them.

---

## 1. Clean scope → FLAT (the happy path)

**Request:** *"We need an AI agent that pulls from our order system and our docs to answer customer questions accurately. Build from scratch. Just the agent, no custom UI. Fixed deliverable."*

**Intake the model fills:** `ai-agent-single` · integrations 2 · accuracy_critical ✓ · custom_ui ✗ · data_access ✓ · net_new ✓ · scope_bounded ✓.

**Engine:** 4 points → **HIGH** band → 120 h, +25% AI buffer → 150 h × $125 = $18,750, +10% overhead = **$20,625**. Model: **FLAT** (scope is bounded and estimable — avoids capping your upside on a clean deliverable).

**What the client sees:** a proposal for $20,625, a contract with the exclusions / revision-cap / kill-fee clauses, and a receipt showing the four signals that set the price. (Full output: `reference/sample-output.json`.)

---

## 2. The trap: looks flat, should be HOURLY

**Request:** *"Just a simple FAQ chatbot, give me a flat price. We'll keep tuning the answers as we go and add topics whenever we think of them."*

The instinct is to quote a flat ~$8k. That is the trap: "we'll add topics whenever" means the scope has no bottom. Flat fee → you eat every addition.

**Intake:** `chatbot-faq` · integrations 1 · net_new ✓ · **scope_bounded ✗ · client_paced ✓**.

**Engine:** 2 points → MID → 60 h, +25% → 75 h × $125 = $9,375, +10% = **$10,312**. Model: **HOURLY** — *fired on scope_bounded=false; avoids a flat fee on an open scope and eating the overruns.*

**The lesson:** the price is similar either way; the *model* is what saves you. BriefLock catches the open scope and bills for time, not for a guess.

---

## 3. Small build, big ROI → VALUE-BASED

**Request:** *"Automate our invoice-matching. It's a few steps. Our finance lead says the manual version costs us about $80k a year in labor."*

**Intake:** `workflow-multi` · integrations 1 · scope_bounded ✓ · **roi_measurable ✓ · roi_amount_usd 80000**.

**Engine:** 1 point → LOW → 15 h, +25% → 18.8 h × $125 = $2,344, +10% = **$2,578 cost floor**. ROI lever: 15% × $80,000 = $12,000. Model: **VALUE-BASED**, recommended **$12,000**.

**The lesson:** cost-plus would bill $2,578 for something worth $80k/yr to the client. Value-based prices a slice of the value. Cost is the floor; ROI is the ceiling.

---

## 4. Too vague → QUOTE-BLOCKED (questions, not a guess)

**Request:** *"Can you build us some kind of AI thing to help with support? Not sure exactly what yet."*

The model cannot honestly fill the signals — it does not know the integrations, the accuracy bar, or whether the scope is fixed.

**Engine:** `QUOTE-BLOCKED`. It returns discovery questions instead of a price:
- How many external systems does this connect to?
- Is there a hard accuracy or compliance bar?
- Is the scope fixed, or still forming? One-time or ongoing?

**The lesson:** a refused guess is a feature. BriefLock asks the three questions that unlock a real quote rather than inventing a number it would have to walk back.

---

## 5. MONITOR (bonus): catch scope creep mid-project

When BriefLock quoted the agent build from example 1 (Meridian Retail Co., $20,625), it auto-saved the lock to `quotes/meridian.json` — deliverables: *the agent only*; exclusions: *custom UI / dashboards*. Weeks later, in a fresh session, the user comes back.

**Returning user:** *"Meridian wants me to add a dashboard to see the agent's logs now."*

**BriefLock** loads `quotes/meridian.json` (STAGE 3) and measures the ask against the locked scope. Verdict: **out of scope** — a dashboard is new work, not a revision of a locked deliverable, and a UI is on the exclusion list. It builds a fresh intake for just the dashboard and runs the engine (`dashboard-internal` → ~$8k MID) for a *real* add-on price, then drafts the out-of-scope email (`reference/contract-templates.md §4`): warm, names the line, carries the number. The original $20,625 never moves; the relationship stays warm; the scope stays locked.
