# Proposal Assembly

How the model turns a `QUOTED` decision object + the profile into a comprehensive, client-winning
proposal + service agreement. This is the **playbook**: the section order, the selection tables
(which variant fires when), and the content packs the model picks from. The exact legal clause text
and the `PROPOSAL_DATA` field shape live in `contract-templates.md`; the renderer is `proposal-template.html`.

**Three rules govern everything here:**
1. **The engine owns the number.** Use the price from the decision object verbatim. For FLAT / HOURLY / RETAINER that is `decision.price`; for VALUE-BASED it is `decision.value_based.recommended`. Never edit, re-derive, or invent a number.
2. **Client-facing — no internal math.** Never print hours, rate, buffer %, overhead %, points, band names (LOW/MID/HIGH), source tiers, `value_share`, or the ROI formula. The client sees a clean total + value. The receipt math stays in the chat.
3. **Presentation fields you compose must reconcile to the engine.** `price_lines[]`, a phase split, an HOURLY range, a RETAINER per-month figure, and option add-ons are things YOU assemble — the engine does not emit them. Any sub-figure must sum/round to the engine total or be a separately engine-priced line; otherwise omit it. Never let a composed figure imply a different total than the engine returned.
4. **The timeline is looked up, not guessed.** Read each line item's `band` from the engine receipt (`line_items[].band` = LOW/MID/HIGH), look up `service-compendium.md` → **Build timeline (weeks)** for that `service_key` at that band, and render it as a ~2-week window from signing (band figure 12 → "about 10–12 weeks"). Split milestones **≈20% discovery · 55% build · 25% review + handover**; each milestone is `{label, detail}` where **`label` is ONLY the short week tag** ("Weeks 1–3") and **`detail` is the phase name + what happens** — never put the phase name in `label` (it's a narrow fixed-width tag) or bury the weeks inside `detail`. Multi-line: use the **longest single line's** weeks — work overlaps, never sum. If the receipt shows **no band** (a Tier-1 past job or an `hours_override` set the hours directly), pick the week band whose compendium **hours** band brackets the quoted hours, or default to **MID**. The rough week ranges in the job-type packs below are illustrative only; the **quoted** timeline is always the compendium Build-weeks at the band. Durations only — never show hours. (The band is internal, like the hours — it drives the lookup; the client sees only the weeks.)
5. **Deadline check — flag tension, never quietly miss it.** If the client states a hard deadline, compute weeks-from-today (use the host date, e.g. `date`) and compare it to the build timeline (rule 4). If the deadline sits **comfortably past** the timeline, add at most a one-line reassurance. If it's **tighter than the timeline's low end**, set the `deadline` field: an honest `note` (the gap in the client's frame — "an honest build is ~X weeks; your date is ~Y weeks out, so the full scope won't safely make it"), 2–3 `options` (**Phase it** to the deadline · **Trim scope** to fit · **Compress** as a rush — quoted separately, never an invented number), and a `recommendation` (usually phasing — it protects the accuracy that matters most). Never promise a date the grounded timeline can't hit.
6. **Budget check — flag the gap, never silently overshoot.** If the client states a budget, compare it to the engine's price. If the price **materially exceeds** it (~20%+ over), set the `budget` field: an honest `note` (the gap in the client's frame — "the full scope comes to {price}; you mentioned about {their budget}, so there's a real gap"), 2–3 `options` (**Trim scope** to the must-haves so it fits · **Phase it** so the first slice lands in budget · **Keep the full scope** with the value spelled out — why it's worth more), and a `recommendation`. **Never quietly quote 2–3× the stated budget** — that's the over-scope failure. (If the price is comfortably *under* budget, you may note there's room to add scope; never pad the price to use it up.) The number itself is still the engine's — the budget note frames it, it doesn't change it.

---

## 1. Section order (the proposal)

Arc: **PROBLEM → PLAN → PROOF → PRICE → TERMS.** Sections marked *(cond.)* render only when their condition holds.

| # | Section | Renders when |
|---|---|---|
| 1 | Cover page | always |
| 2 | Running header (per part) | MID/LARGE *(cond.)* — omit for SMALL |
| 3 | Executive summary | MID/LARGE *(cond.)* |
| 4 | The situation | always (1 sentence for SMALL) |
| 5 | Our approach | always |
| 6 | What you'll get (deliverables) | always |
| 7 | The finished result (def-of-done) | always |
| 8 | What's not included (exclusions) | always |
| 9 | What we need from you (inputs) | when `inputs_needed[]` present (always for builds) |
| 10 | Timeline & milestones | always |
| 11 | Why us | only when the profile has real proof *(cond.)* — mandatory for LARGE |
| 12 | Investment (hero) | always |
| 13 | Payment schedule | always |
| 14 | Terms at a glance | always |
| 15 | Assumptions | when `assumptions[]` present; mandatory for OPEN scope |
| 16 | Next steps + signatures | always |
| 17 | Footer (per part) | always |

**The agreement** follows on a new printed page: 15 clauses, in the order fixed by `contract-templates.md`.

---

## 2. Selection tables (which variant fires)

### deal_size_band — from the engine's FINAL price (NOT the secret LOW/MID/HIGH bands)
| Band | Final price | Tone | Conditional sections |
|---|---|---|---|
| SMALL | < ~$5,000 | tight, fast, low-ceremony | drop Exec summary, Running header, Why us |
| MID | ~$5,000–$25,000 | confident, full arc | Exec summary on; Why us only if proof |
| LARGE | > ~$25,000 | de-risked, phased, proof-forward | Exec summary + Why us mandatory; foreground "how we de-risk this" |

*(Cutoffs are drafting defaults — tune in one place here, never surface them to the client.)*

### pricing model → pack + price source
| Engine model | pricing_label | price source | pack |
|---|---|---|---|
| FLAT | Fixed-price project | `decision.price` | §4 FLAT |
| VALUE-BASED | Value-based engagement | `decision.value_based.recommended` | §4 VALUE-BASED |
| HOURLY | Time & materials | `decision.price` → shown as an **estimate range**, never a fixed total | §4 HOURLY |
| RETAINER | Monthly retainer | `decision.price` → shown as a **/month** figure | §4 RETAINER |

### scope shape — from the engagement signals
| Shape | Fires when | §5 pack |
|---|---|---|
| Bounded one-shot | `scope_bounded=true`, single deliverable set | Bounded |
| Phased / multi-milestone | large hours (multistep agent, multi-source RAG, complex workflow) or client wants staged risk | Phased |
| Open / discovery-first | `scope_bounded=false/null` **and the engine QUOTED a discovery line item** (e.g. `ai-audit`). A hard `QUOTE-BLOCKED` returns NO price — ask the discovery questions instead, do not render a proposal. | Open |

### terms tier — from model + signals + family
| Tier | Fires when | §6 |
|---|---|---|
| Standard | most bounded builds (FLAT) | Standard |
| High-risk / high-value | `accuracy_critical=true` OR deal_size_band=LARGE OR VALUE-BASED | High-risk |
| Advisory-light | `ai-audit` / `ai-roadmap` (advisory rows) | Advisory-light |
| Retainer | engine model = RETAINER | Retainer |

Pick exactly one tier — never mix clauses across tiers. The chosen tier sets the `terms{}` values; render those into BOTH the agreement clauses and the Terms-at-a-glance grid (one source, two views).

### value register (the angle for `price_note`) — first match wins
1. **ROI** — only when `pricing_model == VALUE-BASED` (so `roi_amount_usd ≥ value_threshold` is already true). "a fraction of the ~${{roi_amount}} you expect this to return in year one."
2. **Time saved** — the brief signals a repetitive manual task. "hands your team back the hours they spend on [the task] today."
3. **Risk reduction** — FLAT/bounded. "one fixed number protects the scope for both of us — no hourly meter, no surprises."
4. **Certainty** — RETAINER. "predictable monthly cost and priority access, no per-task haggling."

The number always sits beside the client's own outcome, **never** beside your cost. Never a % of value, an invented multiple ("save 10x"), or an unsourced benchmark ("agencies charge $80k").

---

## 3. Job-type packs (pick by the line item's `service_key` family)

Each pack gives the `overview`, `deliverables[]`, `exclusions[]`, `acceptance[]` (definition-of-done),
`timeline`/`milestones[]`, and `inputs_needed[]`. Fill `[bracketed]` slots from the actual request.
Universal exclusions to add to every build: third-party license/subscription fees · hosting + API/run usage
beyond the build · content/copy the client supplies · ongoing maintenance/retainer · training beyond the named session.
Closing line on exclusions (verbatim-anchored, Law Insider): **"Anything not listed here is out of scope and would be a separate quote."**

### Workflow automation — `workflow-simple` / `workflow-multi` / `workflow-complex`
- **Overview:** Your team is moving the same information between [System A] and [System B] by hand, and as volume climbs it gets slower and more error-prone. We'll connect the two so the hand-off runs automatically and accurately, without anyone babysitting it.
- **Deliverables:** an automated workflow connecting [A]→[B] · the trigger, logic, and actions that run it end-to-end · error handling + a failure alert (multi/complex) · a short how-it-works doc + one handover walkthrough.
- **Exclusions:** changes to the connected systems themselves · new licenses/paid-plan upgrades · workflows beyond the one(s) described · monitoring/maintenance after handover · historical data clean-up/migration.
- **Done when:** it runs end-to-end on real cases you provide, handles the error cases we listed, and completes one clean run in front of you at handover.
- **Inputs:** admin access to [A] and [B] · a few real sample records · confirmation of the exact trigger and action.
- **Timeline:** simple ~1–2 wks · multi ~3–4 wks · complex ~6–10 wks.

### Chatbot / conversational — `chatbot-faq` / `chatbot-llm`
- **Overview:** Your customers ask the same questions over and over, and your team answers them one at a time. We'll build a chatbot that handles those on its own, so your people only step in for the cases that truly need them.
- **Deliverables:** a [FAQ / AI-powered] chatbot for your common questions · conversation flows + fallback for the unknown · connection to your [website/channel] · tuning to your tone and answer quality · one handover walkthrough + a short edit guide.
- **Exclusions:** live human-handoff / help-desk integration unless listed · writing the source content · multi-language unless listed · custom-designed chat UI beyond the standard widget · model API + hosting beyond the build.
- **Done when:** FAQ — it correctly answers the agreed question list and routes the rest to your fallback. LLM (accuracy-gated) — it answers a test set of real questions you approve at the accuracy bar we agree, stays on-topic, and hands off cleanly when unsure.
- **Inputs:** your current FAQ/answer content · access to the site/channel · a list of real questions customers ask (for testing).
- **Timeline:** faq ~3–4 wks · llm ~6–10 wks.

### RAG / knowledge-base — `rag-pipeline` / `rag-multisource`
- **Overview:** Your team loses time hunting through [docs/policies/past tickets] for answers that already exist somewhere. We'll build a system that answers questions from your own knowledge directly, with the source shown — so the answer is trusted, not guessed.
- **Deliverables:** a Q&A system grounded in your [single / multiple sources] · source citations on each answer · ingestion of your documents · accuracy tuning to a question set you approve · one handover + a refresh guide for adding documents.
- **Exclusions:** cleaning/de-duplicating/re-organizing your sources · OCR/rescue of low-quality scans unless listed · a custom search UI beyond the delivered interface · keeping answers fresh after handover (retainer item) · vector DB + model + hosting run-costs (billed separately).
- **Done when:** it answers a question set you approve at the accuracy bar we agree, shows the correct source for each answer, and says "I don't know" rather than guessing when the answer isn't in your documents.
- **Inputs:** the documents/sources in a usable format · access to any live source · a gold-set of real questions with the answers you'd expect.
- **Timeline:** pipeline (single source) ~6–9 wks · multisource ~10–16 wks. **Run-cost line always shown** (vector DB + LLM is real and recurring).

### AI agent — `ai-agent-single` / `ai-agent-multistep`
- **Overview:** single — Your team spends hours on [the repetitive task] that follows the same steps every time. We'll build an AI agent that does it for you — reading the input, deciding what to do, and completing the task — so your people are freed for the work that needs judgment. multistep — …an agent that reasons across several steps and uses your tools to get a whole job done.
- **Deliverables:** a from-scratch AI agent that [does the job] · connection to the [named systems/tools] it needs to act · decision logic + guardrails that keep it on task · accuracy tuning to your agreed quality bar · one handover + a how-it-works doc.
- **Exclusions:** actions/systems beyond the [named] tools · a customer-facing UI/dashboard unless listed · letting the agent take irreversible actions without your sign-off · model API + hosting beyond the build · ongoing tuning after handover (retainer item).
- **Done when:** it completes the task end-to-end on a test set of real cases you approve, at the accuracy bar we agree, and stops for a human on the edge cases we flag as risky.
- **Inputs:** access to the systems/tools · real example cases with the correct outcome · your call on which actions need a human approval step.
- **Timeline:** single ~6–10 wks · multistep ~12–20 wks, phased. *(`ai-agent-single` is the committed demo — the $20,625 worked example.)*

### Voice agent — `voice-agent-inbound`
- **Overview:** Your phone line is tied up with the same routine calls — [order status, hours, basic questions] — and callers wait on hold. We'll build a voice agent that answers those calls naturally and handles them on its own, so your team picks up only the calls that need a person.
- **Deliverables:** an inbound voice agent for [the named call types] · natural flows with a clean hand-off to a human · connection to [your phone system / data source] · voice + tone tuned to your brand · one handover + an edit guide.
- **Exclusions:** outbound calling / dialer campaigns · phone-number provisioning + carrier/telephony fees · call types beyond the [named] ones · per-minute voice/transcription/model run-costs (billed separately) · ongoing tuning (retainer item).
- **Done when:** it answers the named call types correctly on a set of real test calls you approve, hands off to a human cleanly when unsure, and sounds on-brand — we sign off together on recorded test calls.
- **Inputs:** access to your phone system / call routing · the data the agent needs (e.g. order lookups) · a few real call recordings or scripts.
- **Timeline:** ~6–10 wks. **Run-cost line always shown** (per-minute stack).

### Prompt engineering — `prompt-optimization` / `prompt-strategy`
- **Overview:** optimization — Your [AI feature] gives inconsistent or off-target answers, and tweaking it by hand hasn't fixed it. We'll systematically optimize the prompt behind it so the output is reliable and on-brand. strategy — …design the full prompt strategy behind your product so every AI touchpoint behaves consistently.
- **Deliverables:** an optimized system prompt for [the feature] (optimization) / a prompt architecture across [the product's AI touchpoints] (strategy) · a before/after comparison on a test set · reusable prompt templates + guardrail patterns (strategy) · a test set + evaluation approach (strategy) · a short maintenance guide/handover.
- **Exclusions:** building the app/feature the prompts run inside · model fine-tuning / training-data work · ongoing prompt maintenance as your product changes · model API usage during testing beyond the build.
- **Done when:** the optimized prompt(s) beat the current version on a test set you approve, measured against the quality criteria we agree up front.
- **Inputs:** access to the current prompts + the feature they run in · examples of good and bad outputs · the quality criteria that matter most.
- **Timeline:** optimization ~1–2 wks · strategy ~4–8 wks. *(No run-cost line — these rows carry none.)*

### Data / document processing — `doc-processing` / `scrape-ai-pipeline` / `email-ai` / `fine-tune-lora`
- **Overview:** doc-processing — Your team manually reads [invoices/contracts/forms] and types the details into [system]. We'll build a pipeline that extracts the data automatically into the structured format you need, so the typing — and the typos — go away. scrape — …collect [the data] from [sources] and enrich/classify it automatically. email-ai — …triage and label incoming email so the right messages reach the right place.
- **Deliverables:** a pipeline that turns [source docs/data] into [the structured output] · extraction/classification tuned to your fields and rules · a review step that flags low-confidence items for a human · one handover + a maintenance guide · *(fine-tune-lora)* a fine-tuned [7B] model on your dataset.
- **Exclusions:** cleaning/fixing the quality of your source docs/data · building the system the output feeds into · handling doc/data types beyond the [named] ones · bypassing a site's terms or access controls (scrape) · model API / scrape-infra / GPU-rental run-costs (billed separately).
- **Done when:** it processes a real batch you provide at the accuracy bar we agree, outputs the exact structured format you specified, and flags the low-confidence cases instead of guessing. *(fine-tune-lora — the fine-tuned model beats the base model on your held-out test set.)*
- **Inputs:** a representative batch of real source files/data · the exact output format/fields · a small labeled sample to measure accuracy.
- **Timeline:** ~6–10 wks. *(fine-tune-lora and scrape carry a run-cost line — GPU / scrape infra.)*

### Folder-agent — `folder-agent` (ICM-style build)
- **Overview:** You want an AI specialist that thinks and works the way your best person does on [the task] — consistently, every time. We'll build a folder-based AI agent: its knowledge, rules, and examples live in plain files you can read and edit, so it's transparent and yours to grow.
- **Deliverables:** a folder-based AI agent for [the task], from scratch · its identity, rules, reference knowledge, and worked examples as editable files · tuning so its behavior matches your standard · one handover + a guide on how to extend it yourself.
- **Exclusions:** a hosted app/chat UI around the agent unless listed · integrations to live systems unless listed · writing the source knowledge beyond what we agree · model API + hosting beyond the build · ongoing tuning (retainer item).
- **Done when:** it handles a set of real example cases you approve the way your standard expects, and the files are organized so your team can read and edit them without us.
- **Inputs:** examples of the task done well · the rules and knowledge the specialist relies on · a point of contact who knows what "good" looks like.
- **Timeline:** ~2–5 wks. *(`folder-agent` is a derived band — a vague request may QUOTE-BLOCK; render the discovery-first shape until scope is bounded.)*

### Advisory / strategy — `ai-audit` / `ai-roadmap`
- **Overview:** audit — You suspect AI could save real time or money, but you don't yet know where to start or what's worth doing. We'll run a focused audit of your workflows and hand you a ranked, costed list of the highest-value opportunities. roadmap — …build a sequenced roadmap that turns those opportunities into a plan you can act on, with or without us.
- **Deliverables:** a review of your [workflows/teams] for AI/automation opportunities · a ranked shortlist with rough effort + payoff (audit) · a sequenced roadmap — what to build, in what order, why (roadmap) · effort/impact + dependency notes per initiative · a written findings/strategy document + a working session to walk you through it.
- **Exclusions:** building any of the recommended solutions (separate quote) · procuring/licensing tools on your behalf · ongoing advisory after the engagement (retainer item) · implementation support during a build phase.
- **Done when:** you've received the written deliverable and we've completed the agreed working session/presentation. This is advisory — the deliverable is the analysis and plan, not a built system.
- **Inputs:** time with the right people for interviews · visibility into the workflows/tools in scope · any cost/volume numbers that help size the opportunities.
- **Timeline:** audit ~1–3 wks · roadmap ~4–8 wks. *(No run-cost line.)* Use the **Advisory-light** terms tier.

### Web / dashboard-adjacent — `api-integration` / `landing-page` / `dashboard-internal`
- **Overview:** api-integration — Your [System A] and [System B] don't talk to each other, so someone keeps re-entering the same data. We'll connect them so the data flows automatically. landing-page — You need a clean, fast page that turns visitors into [leads/signups]. We'll design and build it. dashboard-internal — Your team can't see [the key numbers] in one place. We'll build an internal dashboard that surfaces them clearly.
- **Deliverables:** the [integration / page / dashboard] as described · the connections/data sources it needs · a responsive, tested build delivered to your [environment] · one handover walkthrough.
- **Exclusions:** content/copy/imagery you supply · ongoing site/tool maintenance after handover · hosting/domain/platform fees · SEO/paid-ad/analytics strategy (landing-page) · new features beyond the [named] scope.
- **Done when:** it matches the agreed design/spec, works on the standard devices/browsers we agreed, and passes your review round.
- **Inputs:** access to the systems/environment · your content, branding, and credentials · sign-off on the design/spec before build starts.
- **Timeline:** api-integration ~1–3 wks · landing-page ~2–5 wks · dashboard-internal ~4–10 wks.

---

## 4. Pricing-model packs

For each: `pricing_label`, the `price_frame_line` (one line under the price in the hero band), the `price_note`
(value framing, NO math — pick the angle from the §2 value-register table), `payment_schedule`, and run-cost framing.

### FLAT — "Fixed-price project"
- **frame:** "A single fixed price for a bounded, well-defined build — you know the number up front."
- **note:** "One fixed price for a bounded, well-defined build. You know the exact number before we start, and it protects the scope for both of us — no hourly meter, no creeping invoice, no surprises at the end. The price holds as long as the scope above holds."
- **payment:** "50% deposit on signing, 50% on delivery. The deposit is non-refundable once work has started and books your start date."
- **run-cost:** show "Model API usage and hosting are billed separately at cost — not part of the build price. We'll estimate it before launch." Suppress entirely when the compendium row has no run-cost.

### VALUE-BASED — "Value-based engagement" — price = `decision.value_based.recommended`
- **frame:** "Priced against the value this creates for you, not the hours it takes."
- **note (ROI register, attributed — NOT a guarantee):** "This engagement is priced against the outcome, not the hours. By the figures you shared, you expect this to return on the order of ${{roi_amount}} in its first year — so the investment here is a fraction of that." *(Fill `${{roi_amount}}` only from `engagement.roi_amount_usd`. Never print `value_share`, the word "share", the `max(price, value_price)` logic, or "15% of value". Do not promise the result — attribute it to the client's own figures.)*
- **payment:** "40% on signing, 40% at deployment, 20% once the system is live. The deposit is non-refundable once work has started."
- **run-cost:** "Model API usage and hosting are billed separately at cost. We'll size it with you before launch."

### HOURLY — "Time & materials" — price shown as an **estimate range**
- **frame:** "Billed for time and materials as the work unfolds — right when the scope is still forming."
- **note:** "The shape of this work is still forming, so a single fixed price would mean one of us guessing — and that guess always costs someone. Instead you pay for the time the work actually takes, billed transparently against a log you can see. The figure above is our honest estimate of the range, not a cap; if we can do it in less, you pay less — and we'll flag before we approach it."
- **payment:** "Billed every two weeks against time logged, due within 14 days of each invoice. Work pauses on any invoice more than 14 days overdue."
- **run-cost:** "Any model API, hosting, or infrastructure usage is passed through at cost on the same invoice."
- **CRITICAL:** `price` renders as a RANGE ("Est. $14,000–$18,000") bracketing the engine number, or "Billed at actuals" — never a single fixed total (a flat number here re-creates the "$60k-for-a-$20k-quote" trap HOURLY exists to avoid). **Never** present good-better-best on HOURLY (scope too unbounded to package).

### RETAINER — "Monthly retainer" — price shown as a **/month** figure
- **frame:** "Billed monthly for an ongoing engagement — predictable cost, continuous coverage."
- **note:** "A flat monthly fee that keeps the system healthy and keeps us on call for the changes that come up — model drift, new edge cases, the small asks that would otherwise each become their own quote. You get predictable cost and priority access; we reserve the time for you each month. No per-task haggling."
- **payment:** "Billed monthly in advance on the 1st; the first month is due on signing. Month-to-month — either of us can end it with 30 days' written notice. Unused time does not roll over."
- **run-cost:** may be folded into the monthly fee: "Infrastructure and ordinary API usage are included in your monthly fee; any unusual spike is flagged and passed through at cost before it's incurred." *(The internal receipt still reports run-cost separately — only the client-facing retainer doc folds it in.)*
- The Timeline section becomes a cadence line ("Ongoing, reviewed monthly"), not dated milestones.

---

## 5. Scope shapes

### Bounded one-shot (default)
Standard layout: full `deliverables[]`, one def-of-done block, `exclusions[]`, a single-delivery timeline ending in handover, one investment total. Maps to FLAT (or VALUE-BASED if ROI fired). Approach closes: "The deliverables above are the whole scope — anything new is a separate, quoted line, agreed in writing before we start it." *(This is the committed demo shape.)*

### Phased / multi-milestone
For large hours or staged risk. Deliverables grouped under named phases, a def-of-done **per phase**, an optional `price_lines[]` split by phase, staged payment tied to milestone acceptance. `pricing_label` stays "Fixed-price project" (or "Value-based engagement"). note: "A fixed price, delivered in clear phases. Each phase has its own deliverables and sign-off, so you see value land step by step." Payment: "40% on signing, 30% on acceptance of Phase 2, 30% on final delivery." **`price_lines[]` sub-figures MUST sum to the engine total** — never derive a phase figure from hours, never imply a different total.

### Open / discovery-first
Only when the engine **QUOTED a discovery line item** (e.g. `ai-audit`) on a not-yet-bounded scope — never on a hard `QUOTE-BLOCKED`. Sells a paid discovery that produces the bounded scope; the build is explicitly **not yet priced** as a fixed total. Situation: "The shape of this is still forming — which is good; it means we can adapt as we learn instead of locking in guesses." Discovery deliverables: a scoped build plan (exact deliverables, integrations, acceptance criteria) · a fixed-price quote for the build · a go/no-go recommendation. Exclusions: "The build itself is not included in this discovery — it's quoted at the end of it." note: "Quoting a fixed build price on a fuzzy scope would mean padding it to be safe — discovery first means you pay for exactly what the build turns out to need." Agreement Scope clause adds: "The build scope is defined by the discovery deliverable and quoted separately once approved." **Never show a confident fixed build total here** (that is the HOURLY trap).

---

## 6. Terms tiers

Each tier sets the `terms{}` values; the **full clause text and tier variants live in `contract-templates.md`**.
Here is which tier to pick and what changes:

- **Standard** — default bounded build (FLAT). 14-day acceptance · 2 revision rounds, extras at `revision_overage_rate` (NOT your engine rate) · IP transfers on full payment + portfolio · kill fee: completed milestones billed in full + 30% of the remaining balance (Law Insider verbatim) · liability capped at fees paid.
- **High-risk / high-value** — `accuracy_critical=true` OR LARGE OR VALUE-BASED. Tightens acceptance to 7 days against the stated acceptance criteria · kill fee 50% mid-build / 100% complete, rights revert until paid (Law Insider verbatim) · stronger IP (full assignment, no pre-payment license, portfolio needs consent) · confidentiality gains a 2-year survival · warranty adds a 30-day post-acceptance bug-fix period · liability cap excludes confidentiality breach + third-party IP infringement · adds a data-handling line only when `data_access=true`. Foreground the "how we de-risk this" note in Our Approach.
- **Advisory-light** — `ai-audit` / `ai-roadmap`. Scope = findings, not a built system; no software warranted · accepted on delivery of the final report (no conformance-cure cycle) · one consolidation pass instead of revision rounds · client owns the report, you keep methods/frameworks · kill fee = the deposit (no further termination charge) · warranty: professional/good-faith, no warranty of specific business outcomes.
- **Retainer** — engine model = RETAINER. Month-to-month, 30 days' written notice · reserves time each month, billed in advance · unused hours don't roll over; client may pause with 30 days' notice · kill fee = pro-rata of the retainer to 30 days post-termination (Law Insider verbatim) · IP of each month's work transfers as that month is paid · revisions = within the monthly scope, more is a separate line.

---

## 7. Good-better-best options (an add-on ladder, never a second price)

The engine returns ONE number — do not fabricate three competing totals. Render options in `price_lines[]` as:
the recommended engagement (the engine total, labeled "Recommended") **plus** genuinely-separate add-on rows that
the engine ALSO priced (an extra integration via the `api-integration` row, a care/maintenance retainer, a compressed timeline).
Each add-on is an engine-computed figure or the literal string **"quoted on request"**. Anchor by ORDER and LABEL only —
lead with the fuller scope, mark the middle "Recommended" — **never** by inventing inflated decoy numbers or unsourced benchmarks.

```
price_lines: [
  {"label":"Core build (recommended) — everything in What you'll get", "value":"$20,625"},
  {"label":"Add: second system integration",                          "value":"+$2,400"},
  {"label":"Add: 3-month care retainer after launch",                 "value":"+$4,000/mo"},
  {"label":"Add: compressed 4-week timeline",                         "value":"quoted on request"}
]
```
note: "The recommended scope above is the build we'd ship. The add-ons are optional — take them now or add them later; each is a separate line so you only pay for what you choose."
**Use single-price (the default) when:** the engine returned one number with no priced add-ons, OR any HOURLY engagement.

---

## 8. Multi-line-item assembly

When the request is several deliverables across different families, the engine sums them into ONE total.
Assemble ONE proposal: **merge** the packs — concatenate each line item's `deliverables[]` under "What you'll get"
(grouped by deliverable, not by pack), union the `exclusions[]` (drop duplicates; keep the universal set once),
list each line's def-of-done under "The finished result", and union `inputs_needed[]`. The Situation/Approach
narrate the combined outcome, not each piece separately. Pick the terms tier by the **highest-risk** line
(any `accuracy_critical` line → High-risk for the whole agreement). Use the phased scope shape if the combined
hours are large. The single investment total is the engine's summed `price` — `price_lines[]` may show one row
per line item, and those rows MUST sum to that total.

---

## 9. Agent-composed vs engine-authored (the guard)

The engine emits: `price` (one integer), `pricing_model`, `value_based` (for VALUE-BASED), `run_costs[]`, `line_items[]` receipts, `market_band`.
**You compose** (and must reconcile to the engine): the HOURLY range, the RETAINER /month figure, any `price_lines[]`/phase split, and the option add-ons.
Rule: a composed figure either sums/rounds to the engine total, or is a separately engine-priced line, or is the literal "quoted on request". If you can't satisfy that, omit it and show the single engine total. Never let the client infer a number the engine did not produce.

---

## 10. Rendering the branded PDF

STEP_04's final move: turn the assembled `PROPOSAL_DATA` into a saved, self-contained, branded HTML file the freelancer prints to PDF — all in the **same turn** as the receipt, no "one moment" pause.

- **Copy the template — never hand-write HTML.** Copy `reference/proposal-template.html` to `proposal-[client].html` and inject `<script>window.PROPOSAL_DATA = {…}</script>` into `<head>`, before the template's own `<script>`. Don't rewrite the layout: copying keeps the brand styling, the section logic, the demo-bleed guard, and the built-in **`Print / Save as PDF`** button. A profile with no `brand` renders the neutral default theme.
- **Set `date` to today, from the host** (e.g. run `date`) — NEVER a date pulled from the client's files.
- **Set only the fields this quote needs.** Omitted client-content fields render **empty by design** — the template blanks demo sample content for a real quote — so leave out `deadline` / `budget` / `run_cost` / `exec_summary` when they don't apply; never copy the demo's. Always set `pricing_label` to the engine's model.
- **Embed the logo, never link it.** SVG → pass its raw markup as `brand.logo_svg`; raster (png/jpg) → a base64 `data:` URI as `brand.logo`. The saved file must be self-contained; no `brand`/logo → the studio name renders as a text wordmark. Confirm the mark shows before handing over.
- **Open it automatically** in the default browser (`open` macOS · `xdg-open` Linux · `start` Windows) — do NOT tell the user to open it; they Print → Save as PDF for their client. **No browser available → hand over the file path.**
