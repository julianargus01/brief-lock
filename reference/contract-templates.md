# Contract Templates

The `PROPOSAL_DATA` field shape and the locked clause text the model injects into `proposal-template.html`.
**Which** variant to pick (job-type packs, pricing-model packs, scope shapes, terms tiers) lives in `proposal-assembly.md` —
read that first; this file is the legal/field source it points to. The model writes prose; it never edits a number the engine computed.

**Client-facing — no internal pricing math** (hours × rate, buffer %, overhead, points, band, tier) ever appears here.
The clean total shows as an investment; the internal receipt stays in the chat the freelancer sees.

> **Internal note to the freelancer (NOT printed):** these are confident drafting starting points, not a substitute for your own
> lawyer. Vet them with your own counsel before you rely on them. This line never appears in the client document. Each clause below
> is tagged **[verbatim]** (traceable to a filed/published contract, see the grounding ledger) or **[drafting]** (standard construction,
> shipped as confident locked language). The agreement the client receives carries no disclaimer — a vendor sends locked terms.

---

## 1. `PROPOSAL_DATA` field shape (what the model injects)

```
studio, tagline,
brand{ color_primary, color_accent, font, logo_svg|logo, voice },   // ABSENT brand → neutral default theme + name wordmark
client_name, date (issue date = today, from the host), valid_days (default 30),
deal_size_band,        // SMALL | MID | LARGE — derived from the engine's FINAL price (not the secret LOW/MID/HIGH bands)
exec_summary,          // MID/LARGE only
situation,             // the mirror-the-client narrative (string or paragraph array) — built only from intake signals
approach,              // the named-phases prose
deliverables[],        // from the job-type pack
acceptance[],          // "the finished result" / definition-of-done lines
exclusions[],          // family-specific + the universal set; closing line below
inputs_needed[],       // "what we need from you" — client-supplied dependencies
timeline, milestones[]{label,detail},   // label = short week tag ("Weeks 1–3") · detail = phase + work. Durations only, never hours
deadline{note, options[], recommendation},   // OPTIONAL — fires when the client's deadline is tighter than the grounded timeline. options[] = plain strings OR {label, detail} objects (the template renders either)
budget{note, options[], recommendation},   // OPTIONAL — fires when the quote materially exceeds the client's stated budget (honest gap + trim/phase/keep options). Same options[] shapes
why_us,                // ONLY from real profile proof (past_jobs); "" → section omitted
price,                 // FLAT/HOURLY/RETAINER = decision.price; VALUE-BASED = decision.value_based.recommended; verbatim string, never edited
pricing_label, price_frame_line, price_bridge, price_note,   // value framing — NO math
price_lines[]{label,value},   // OPTIONAL phase split / add-on ladder; sub-figures SUM to the engine total
payment_schedule, run_cost,   // run_cost "" → the run-cost line is omitted
assumptions[],         // quote-validity conditions (distinct from inputs_needed[])
terms_glance[]{k,v},   // OPTIONAL; default derived from terms{} + live fields (one source, two views)
terms{ revisions, deposit, acceptance, change_order, ip, confidentiality,
       late_fee, kill_fee, independent_contractor, warranty, liability, governing_law }
```
An **omitted client-content field renders empty** — the template blanks demo sample content for a real quote, so the demo's deadline callout, run-cost line, exec summary, etc. never bleed in (you may safely omit `deadline`/`budget`/`run_cost`/`exec_summary` when they don't apply). Only structural fields (`valid_days`, `pricing_label`, `deal_size_band`, `terms`, `brand`) fall back to `DEFAULT_DATA`. **So always set `pricing_label`** to the engine's model — it keeps a "Fixed-price project" fallback, and a non-FLAT quote that omits it would mislabel. Client language only —
"Fixed-price project" / "Value-based engagement" / "Time & materials" / "Monthly retainer" — never a band/tier/points label.

---

## 2. Service Agreement — 15 clauses (in order, locked, confident)

The template renders these from `terms{}` + the live fields. Defaults are the **Standard** tier; tier variants are noted —
pick the tier in `proposal-assembly.md §6` and fill `terms{}` accordingly.

1. **Parties** *[drafting]* — "…entered into as of the date of last signature, between {{studio}} (\"Contractor\") and {{client_name}} (\"Client\"). It governs the work in the Proposal above, which is incorporated into and forms part of this Agreement."
2. **Scope & deliverables** *[verbatim-anchored]* — exactly the items under "What you'll get"; each complete when it meets that description + "The finished result"; "Any service discussed, implied, or assumed but not explicitly listed is out of scope" (Law Insider out-of-scope) — handled only via a change order.
3. **Fees & payment** — "The total fee is {{price}}, payable: {{payment_schedule}}. {{late_fee}}" Engine owns {{price}}.
4. **Deposit** *[verbatim-anchored]* — "The deposit is non-refundable. Work does not commence until the deposit is received in cleared funds, and all timelines run from that date." (Law Insider deposit: lead times run from deposit payment).
5. **Acceptance** *[drafting]* — Standard: 14 days after delivery to flag non-conformance in writing, else deemed accepted. **High-risk: 7 days** against the stated acceptance criteria.
6. **Change orders & out-of-scope** *[verbatim-anchored]* — new/expanded scope via a written, pre-priced change order agreed before work begins; once signed it "becomes a binding part of this Agreement; all other terms remain in full force" (Afterpattern/SEC); no verbal changes.
7. **Intellectual property** *[drafting]* — Standard: ownership of the final work product transfers on payment in full; Contractor keeps pre-existing tools/know-how and may show the work in its portfolio. **High-risk: full assignment, no pre-payment license, portfolio needs written consent.** **Advisory-light: client owns the report; Contractor keeps methods/frameworks.**
8. **Confidentiality** *[drafting]* — mutual; only to perform the engagement; carve-out for public / legally-compelled info. **High-risk adds a 2-year survival.**
9. **Term, termination & kill fee** — either party may terminate with written notice; Client pays for work completed; deposit non-refundable. **{{kill_fee}}** *[verbatim-anchored]* — Standard "completed milestones billed in full + 30% of the remaining balance" (Law Insider 30%); **High-risk "50% mid-build / 100% complete, rights revert until paid"** (Law Insider); **Retainer "pro-rata of the retainer to 30 days post-termination"** (Law Insider); **Advisory-light "the deposit serves as the kill fee."**
10. **Revisions** *[drafting]* — "{{revisions}}" — Standard: "{{revision_cap}} revision rounds per deliverable; further rounds billed at {{revision_overage_rate}}/hr and added by change order. A round is one consolidated set of feedback, not a trickle of one-off changes." **Uses `revision_overage_rate` (a published client-facing rate set at SETUP) — NEVER the engine's internal `rate`.** Advisory-light: "one consolidation pass."
11. **Independent contractor** *[drafting]* — IC, not employee/partner/agent; controls how/when; own tools, taxes, insurance. Same across tiers.
12. **Limited warranty** *[drafting]* — professional/workmanlike + conforms to the Proposal; re-perform non-conforming at no charge (sole remedy); **no warranty of third-party platform/model/API results.** High-risk adds a 30-day post-acceptance bug-fix period. Advisory-light: no warranty of specific business outcomes.
13. **Limitation of liability** *[drafting]* — no indirect/consequential/lost-profits; total liability capped at fees paid. **High-risk: confidentiality breach + third-party IP infringement excluded from the cap.**
14. **Governing law & entire agreement** *[drafting]* — "{{governing_law}}" + entire-agreement + amendment-in-writing + severability.
15. **Signatures** — Name / Signature / Date for both parties; signing accepts BOTH the Proposal and this Agreement.

**Stock phrasings:** "Anything not listed here is out of scope and would be a separate quote." · IP: "ownership transfers once the Client has paid in full." · Late fee (Standard default, freelancer-set at SETUP): "overdue invoices accrue 1.5% per month, or the maximum rate permitted by law, whichever is less; work pauses on any invoice more than 14 days overdue." · Validity: "This proposal is valid for {{valid_days}} days from the date above."

---

## 3. Grounding ledger (honesty — verified vs drafting)

**[verbatim] — traceable to a filed/published contract** (`_build-artifacts/research/freelance-terms-contracts.md`):
- Out-of-scope "discussed, implied, or assumed… out of scope" — Law Insider.
- Change order "binding part… all other terms in full force and effect" — Afterpattern (SEC-filed).
- Deposit non-refundable + "lead times run from date of deposit" — Law Insider.
- Kill fee 30% / 50%-100%-rights-revert / pro-rata-retainer — Law Insider.

**[drafting] — standard construction, shipped as confident locked language (labeled, never cited to the client):**
Parties, Acceptance window, IP transfer-on-payment + portfolio, Confidentiality, Independent contractor, Warranty, Liability cap, Governing law/entire-agreement.

**Late fee:** the **1.5%/month** figure is template-sourced (Common Paper / blog), NOT a filed-contract verbatim — the only filed late fee in the research is a $100-flat-per-installment SEC clause. So the late fee is **asked at SETUP** (the freelancer sets their own policy into `profile.terms.late_fee`); the demo ships 1.5%/month as a suggested default the user confirms or changes.

---

## 4. MONITOR replies (a follow-up request against a locked scope)

STAGE 3 returns one of these. All are **client-facing — no internal math** (hours, band, rate, points). Every one stays warm and professional while holding the line; warmth is what makes the boundary easy to accept. **These are plain-text emails — write `&`, `<`, `>` literally; never HTML-escape them (no `&amp;` in the studio name).**

**IN-SCOPE — a revision of a locked deliverable, within the cap:**
> Hi {{client_name}} — good call, and yes, that's covered under what we agreed (it's part of {{the locked deliverable}}). I'll fold it into the current round at no change to the price or timeline. On it.

**IN-SCOPE but past the revision cap — a paid extra round:**
> Hi {{client_name}} — happy to make this change. One quick note: we'd set {{revision_cap}} revision rounds in our agreement, and this lands just past that, so it comes in as an additional round at {{revision_overage_rate}}/hr (added by a short change order, per our terms). Glad to get on it the moment you give the nod.

**OUT-OF-SCOPE — new work, or it hits an exclusion — the out-of-scope email:**
> Subject: Re: {{the new request}}
>
> Hi {{client_name}},
>
> Great to hear from you — and yes, this is absolutely something I'd love to take on. One quick note so we stay aligned: {{the new ask}} sits outside what we locked in our agreement (the scope we set was {{the locked deliverables}}), so it's new work rather than a revision of what's already underway.
>
> That's completely normal on a project like this — it just travels on its own line, which keeps the original timeline and price protected for both of us. {{if estimable}}To give you a sense of it, it runs about {{new_estimate}}; I'll send over a short add-on quote to confirm the details.{{else}}Let me put together a quick add-on quote so we both have the number before anything starts.{{/if}}
>
> Happy to kick it off the moment you give the word — just say go.
>
> Warmly,
> {{studio}}

Warm and easy to say yes to, but it names the line and protects the locked scope — the everyday tool that stops scope creep before it compounds.

---

## 5. Scope-lock record (`quotes/[client-slug].json`)

Auto-written at the end of STEP_04 for **every** quote (a re-quote for the same client overwrites the file). It is the memory STAGE 3 (MONITOR) reads in a later session. Lean — only what a follow-up check needs, and nothing the client doc wouldn't already show:

```
{
  "client": "Meridian Retail Co.",      // display name; the filename is its slug (meridian.json)
  "date": "2026-06-26",                 // issue date, from the host
  "price": 20625,                       // the engine's final number
  "pricing_model": "FLAT",
  "deliverables": ["..."],              // the locked "what you'll get" lines
  "exclusions": ["..."],                // the "not included" lines (family-specific + the universal set)
  "line_items": [{"service_key":"ai-agent-single","band":"HIGH","signals":{...}}],  // so an add-on re-prices the same deterministic way
  "revision_cap": 2,
  "revision_overage_rate": 125,         // for the "paid extra round" reply
  "change_order": "..."                 // the locked change-order term
}
```
`deliverables` + `exclusions` decide in vs out of scope; `line_items` feed `price_calc.py` for an add-on price; the revision fields decide free-revision vs paid-round.
