# Service Compendium

A market baseline for the AI-consultant / automation-builder niche, plus the common adjacent asks. Each row carries an **hours band** (LOW / MID / HIGH), a **price band** (a market sanity check, not what the engine charges), a **risk buffer**, an optional **monthly run-cost**, and a **source**.

This file is a sourced cold-start baseline, **not** the moat. The moat is the logic applied over it — the signal taxonomy, the scoring, the trap rules in `pricing-model-rules.md`. The numbers here ship usable with zero personal data; as a user logs real jobs (`profile.md` → Tier 1), the estimates ground in their own history too.

**Weights:** every row uses the standard signal-weight table in `pricing-formula.md` — the signal set is identical across rows and matches the intake schema exactly.

**Sync note:** the machine-readable copy of these bands lives in `price_calc.py` (the `COMPENDIUM` dict). This page is the human/judge-readable mirror. The worked examples and the cold test are the drift check — if a number here disagrees with the script, the script is the source of truth and this page is the bug.

The engine prices from **hours × the profile rate** (Tier 2), never from the price band. The price band only triggers a market-sanity flag if the computed price lands outside it.

---

## AI / automation (core) — risk buffer +25%

| `service_key` | What it is | Hours L/M/H | Price L/M/H | Run-cost/mo | Source |
|---|---|---|---|---|---|
| `workflow-simple` | 3–5 step n8n/Make/Zapier workflow, 1 trigger 1 action | 4 / 10 / 18 | $500 / $1,200 / $2,000 | $9–150 platform | A |
| `workflow-multi` | Multi-step workflow, conditions + API calls | 15 / 40 / 65 | $2,000 / $5,000 / $8,000 | $30–150 platform | A |
| `workflow-complex` | Multi-branch, error handling, webhooks | 40 / 90 / 200 | $5,000 / $12,000 / $25,000 | $60–800 platform | A |
| `chatbot-faq` | Simple FAQ / rule-based bot | 20 / 60 / 120 | $3,000 / $8,000 / $15,000 | — | B |
| `chatbot-llm` | GPT/Claude-powered chatbot (stateless) | 60 / 150 / 300 | $8,000 / $20,000 / $40,000 | API usage | B |
| `rag-pipeline` | RAG / knowledge-base Q&A, single source | 60 / 130 / 220 | $8,000 / $18,000 / $30,000 | $1,000–5,000 vector DB+LLM | C |
| `rag-multisource` | Multi-source doc Q&A (PDF, web, DB) | 110 / 220 / 450 | $15,000 / $30,000 / $60,000 | $1,000–15,000 | C |
| `ai-agent-single` | Single-purpose automation agent | 40 / 80 / 120 | $5,000 / $10,000 / $15,000 | API usage | D |
| `ai-agent-multistep` | Multi-step reasoning agent w/ tool use | 160 / 320 / 600 | $20,000 / $45,000 / $80,000 | API usage | D |
| `voice-agent-inbound` | Inbound voice bot (FAQ / IVR replacement) | 40 / 80 / 150 | $5,000 / $10,000 / $20,000 | $0.14–0.50 /min | E |
| `prompt-optimization` | Single-system prompt optimization | 10 / 20 / 35 | $2,000 / $3,500 / $5,000 | — | F |
| `prompt-strategy` | Full-product prompt strategy | 40 / 65 / 100 | $8,000 / $12,000 / $15,000 | — | F |
| `fine-tune-lora` | LoRA/QLoRA fine-tune, 7B, small dataset | 40 / 90 / 190 | $5,000 / $12,000 / $25,000 | GPU rental | G |
| `scrape-ai-pipeline` | Scrape + AI enrichment (extract/classify) | 60 / 130 / 300 | $8,000 / $18,000 / $40,000 | scrape infra | H |
| `doc-processing` | PDF extraction → structured output | 40 / 90 / 190 | $5,000 / $12,000 / $25,000 | API usage | I |
| `email-ai` | Email triage / labeling automation | 22 / 60 / 110 | $3,000 / $8,000 / $15,000 | API usage | J |
| `folder-agent` | Folder-based AI specialist (ICM-style) build | 12 / 30 / 60 | $1,500 / $4,000 / $8,000 | — | K (derived) |

## Advisory — risk buffer +15%

| `service_key` | What it is | Hours L/M/H | Price L/M/H | Run-cost/mo | Source |
|---|---|---|---|---|---|
| `ai-audit` | AI opportunity audit / 1-day discovery workshop | 8 / 16 / 30 | $3,000 / $5,000 / $10,000 | — | L |
| `ai-roadmap` | AI roadmap / strategy project | 40 / 80 / 140 | $15,000 / $30,000 / $50,000 | — | L |

## Adjacent asks — risk buffer +15%

| `service_key` | What it is | Hours L/M/H | Price L/M/H | Run-cost/mo | Source |
|---|---|---|---|---|---|
| `api-integration` | Connect two systems (per integration) | 8 / 20 / 50 | $700 / $2,000 / $5,000 | — | M |
| `landing-page` | Simple marketing / landing site | 10 / 30 / 70 | $1,000 / $3,500 / $8,000 | hosting $0–50 | N |
| `dashboard-internal` | Internal tool / admin dashboard | 22 / 60 / 150 | $3,000 / $8,000 / $20,000 | hosting $20–200 | O |

---

## Sources

US freelance/agency build rates, 2025–2026. Composite of the cited market guides; offshore typically 40–60% lower.

- **A** — Workflow automation: n8n/Make/Zapier market rates (Latenode, TaskIP, Jobbers, platform pricing pages).
- **B** — Chatbot: Altamira, Amplework, MasterOfCode, CustomGPT.
- **C** — RAG / knowledge base: Altamira, Azilen, ITRex; ongoing vector-DB+LLM run-cost per the same.
- **D** — AI agent: Amplework, ReapMind, GroovyWeb.
- **E** — Voice AI: RetellAI, Vapi, per-minute stack costs (Deepgram/ElevenLabs/Retell).
- **F** — Prompt engineering: Opinosis Analytics, PricePerToken, NicolaLazzari.
- **G** — Fine-tuning: AISuperior, Debutinfotech; GPU rental market rates.
- **H** — Scraping + AI: Fiverr, Upwork scraper rates, Apify/Firecrawl infra.
- **I** — Document processing: Altamira, Scopicsoftware.
- **J** — Email AI: agency composite (Growth-tier automation packages).
- **K** — Folder-based specialist: **derived**, not a direct market figure. Blended from prompt-strategy (F) and single-agent (D) low ends, for a markdown-folder build. Flagged so it is never mistaken for a sourced market band; firm it up with a discovery question or a logged Tier-1 job.
- **L** — AI strategy / advisory: independent-consultant day rates and roadmap-project ranges (DigitalAgencyNetwork, RevenueExperts).
- **M** — API integration: per-integration SaaS market ($700–5,000), no-code/integration partner pricing.
- **N** — Landing / brochure site: web-dev freelance market (Clutch, WebFX, Upwork).
- **O** — Internal dashboard: AI add-on "admin dashboard" line + web-app tool market.

---

## Build timeline (weeks)

The client-facing delivery estimate, keyed to the **same LOW/MID/HIGH band as the hours** — a more complex quote
(higher band) gets a longer timeline. This is the one number the agent looks up here, not the hours (hours stay internal).
Render the band's figure as a ~2-week window from signing; split milestones **≈20% discovery · 55% build · 25% review + handover**.
**Sourced** for the core AI-build families (delivery times converge across multiple 2025–2026 agency/market guides — verified-readable, not gated);
**derived** rows are honest estimates from a comparable sourced family or a standard market norm, flagged so they're never mistaken for a cited figure.

| `service_key` | Weeks L/M/H | Source |
|---|---|---|
| `workflow-simple` | 1 / 1 / 2 | W1 |
| `workflow-multi` | 2 / 3 / 4 | W1 |
| `workflow-complex` | 4 / 6 / 8 | W1 |
| `chatbot-faq` | 2 / 3 / 4 | W2 |
| `chatbot-llm` | 6 / 8 / 10 | W2·W3 |
| `rag-pipeline` | 6 / 8 / 10 | W3 |
| `rag-multisource` | 10 / 13 / 16 | W3 |
| `ai-agent-single` | 6 / 9 / 12 | W4 |
| `ai-agent-multistep` | 12 / 16 / 20 | W4 |
| `voice-agent-inbound` | 5 / 7 / 10 | W5 |
| `prompt-optimization` | 1 / 2 / 3 | derived |
| `prompt-strategy` | 4 / 6 / 8 | derived |
| `fine-tune-lora` | 5 / 8 / 12 | derived |
| `scrape-ai-pipeline` | 6 / 9 / 12 | derived |
| `doc-processing` | 5 / 8 / 11 | derived |
| `email-ai` | 3 / 5 / 8 | derived |
| `folder-agent` | 2 / 3 / 5 | derived (K-band) |
| `ai-audit` | 1 / 2 / 3 | derived (advisory) |
| `ai-roadmap` | 4 / 6 / 8 | derived (advisory) |
| `api-integration` | 1 / 2 / 3 | derived (web norm) |
| `landing-page` | 2 / 3 / 5 | derived (web norm) |
| `dashboard-internal` | 4 / 7 / 10 | derived (web norm) |

**Timeline sources** (2025–2026, US agency/market delivery-time guides; figures converge across multiple independent sources):
- **W1** — Workflow automation: simple single-workflow 1–2 wks · medium (multi-step logic) 2–4 wks · complex/enterprise (custom code, webhooks) 4–8 wks. (Buildberg, Makeitfuture, automation-agency guides.)
- **W2** — Chatbot: FAQ/rule-based 2–3 wks · AI/NLP-powered 4–6 wks · enterprise 12–20 wks. (Enterprisebot, Treesha Infotech, ProCoders.)
- **W3** — RAG / knowledge base: simple 3–4 wks · mid-complexity ~10 wks · multi-source/multi-channel 10–16 wks. (ABCloudz, Treesha Infotech, ment.tech.)
- **W4** — AI agent: Tier 1 simple platform 2–4 wks · Tier 2 mid-complexity custom (2–4 integrations) 8–16 wks · Tier 3 enterprise multi-agent 4–9 mo. (Bananalabs — citing Deloitte AI Adoption Survey 2026; corroborated by RaftLabs, Moveworks.)
- **W5** — Voice agent: platform 1–2 wks · from-scratch custom 4–16 wks · enterprise w/ CRM + custom voice 6–10 wks. (Riseup Labs, Ringlyn, Appinventiv.)
- **derived** — NOT a cited delivery time: estimated from a comparable sourced family (e.g. fine-tune / scrape / doc-processing ≈ the AI-pipeline class) or a standard web/advisory market norm. Firm up with a logged Tier-1 job.
