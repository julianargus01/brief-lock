<p align="center">
  <img src="assets/brieflock-logo.png" alt="BriefLock" width="110">
</p>

<h1 align="center">BriefLock</h1>

<p align="center"><strong>Drop the request. Lock the scope. Quote the price.</strong></p>

**Paste a messy client request → get a scoped, market-priced quote, the right pricing model, a computed price with a receipt, and a scope-creep-proof contract.**

BriefLock is a folder-based AI specialist for freelancers and consultants. The model reads the request into a structured intake; a tiny Python engine computes the number from market data. You label, the code computes, so the same request always yields the same price — and every price ships with a receipt you can audit and correct.

**What it is NOT:** not a hosted app (no e-signatures, signing links, project tracker, or invoicing) and not legal advice. It *generates* the documents; you send them. And it never guesses a price — a too-vague request gets discovery questions instead.

Built for the AI-consultant / automation-builder niche out of the box. Retarget to any niche by editing your profile and adding rows to `reference/service-compendium.md`.

---

## 90-second try (no setup)

The repo ships a filled demo profile, so you can run it cold:

```bash
python3 reference/price_calc.py reference/sample-intake.json reference/profile.example.json
```

You'll get a quote for a from-scratch AI agent:

- **Price: $20,625**, model **FLAT**.
- A receipt: 4 signal points → **HIGH** band → 120 h, +25% AI risk buffer → 150 h × $125 = $18,750, +10% overhead = $20,625.
- A market-sanity check and the monthly run-cost flagged separately.

Hand-check it against `reference/pricing-formula.md`. You'll get the same number. The expected output is committed at `reference/sample-output.json`, so you can read the result even without running Python.

## Use it on your own request

1. In your AI tool of choice, load this folder and read `identity.md`, then `rules.md`. (First time, with no profile saved, it runs a short **SETUP** wizard — your rate, services, floor, and terms — before it quotes. See "Make it yours" below.)
2. Paste your client's request.
3. The model fills the intake, runs the engine, and writes your proposal + contract — or, if the request is too vague, hands you the discovery questions to ask first.

See `examples.md` for five worked cases: a clean flat quote, a "looks-flat-but-bill-hourly" trap, a value-based call, a vague request that routes to questions, and a mid-project scope-creep catch (MONITOR).

Every quote is auto-saved to a `quotes/` scope-lock, so weeks later when a client asks "can you also…", BriefLock loads that job, measures the new ask against the locked deliverables, and drafts the reply — in-scope (covered), or out-of-scope with a real engine-priced add-on. Your folder becomes a library of locked jobs.

## Make it yours

Two ways: (a) run **SETUP** — tell the agent your rate, floor, the services you sell, and your terms, and it writes your own `reference/profile.json` (the file it reads every session after); or (b) copy `reference/profile.example.json` to `reference/profile.json` and edit it by hand. `reference/profile.md` documents every field. That is the whole retarget, no code changes. To serve a different field entirely, add rows to `reference/service-compendium.md`.

## How it's built — the ICM methodology

BriefLock is an **ICM** build — **Interpretable Context Methodology** — and that's the real story, not the code. The ICM idea: you don't *build an agent*, you build a **workspace** — a folder of plain-English markdown navigated by a routing table — and the agent **emerges** when a model reads it and follows the routing. No framework, no orchestration, no deployment. The folder *is* the agent.

So BriefLock is that folder:

- **Routing is the keystone.** `rules.md` opens with a mode router that the model resolves from the folder's own state: no `profile.json` yet → **SETUP**; a request → **QUOTE**; a request too thin to price → **discovery questions**; a follow-up against a locked job → **MONITOR**. Nothing is hard-coded as "the agent" — the right behavior is *selected* by the table.
- **Each file is one layer, doing one job.** `identity.md` = who it is · `rules.md` = the workflow + routing · `examples.md` = the worked cases that calibrate the judgment · `reference/` = the knowledge and tools, loaded only when a step needs them. Lean files on top, depth in reference; the model reads *down* and stops when it has enough.
- **Legible and editable — no black box.** Every rule, every market band, every contract clause is plain markdown a freelancer can open, read, and change. If a quote looks off, you open the file and see exactly what the agent was told.
- **Retarget by editing one file.** Fill in `profile.json` — your rate, services, terms — and the same folder becomes *your* pricing operator. A stranger fills it differently and it's theirs. That's ICM's "context is the program" in one move.

**Where the methodology meets code (the small part).** A price must be the *same* every time, so the one spot a number is decided is a tiny Python tool (`reference/price_calc.py`) — and even its logic is written in plain English (`pricing-formula.md`, `pricing-model-rules.md`, sourced bands in `service-compendium.md`) so the judgment still lives in the folder, auditable. The model labels the request; the code computes the number. The engine is just one tool in the reference layer. **The moat is the encoded judgment in the workspace — the signal taxonomy, the scoring, the trap rules — not the script.**

## Files

```
brief.md       the problem, in the builder's voice
identity.md    what the agent is + the mode routing table
rules.md       the workflow, intake schema, discovery questions, refusals
examples.md    five worked cases
reference/
  service-compendium.md   market hours/price bands, sourced
  pricing-formula.md      the scoring + price math, in English
  pricing-model-rules.md  flat/hourly/retainer/value-based + the traps
  profile.md              the one file you edit to retarget
  profile.example.json    the filled demo profile
  proposal-assembly.md    the proposal playbook — job/pricing/scope/terms variants + selection
  contract-templates.md   the 15 agreement clauses + field shapes + the MONITOR replies + the scope-lock record
  proposal-template.html  the branded, print-ready proposal + agreement (Print → Save as PDF)
  price_calc.py           the engine
  sample-intake.json      a committed sample request
  sample-output.json      its expected output
```

## Not legal advice

The generated contract is a drafting starting point, not legal advice. Have your own counsel review before signing.
