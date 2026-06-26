#!/usr/bin/env python3
"""BriefLock pricing engine.

The model labels the request into an intake (which signals are present).
This script computes the number. Same intake in -> same number out.

Usage:
    python3 price_calc.py <intake.json> [profile.json]
    (profile defaults to reference/profile.json, else reference/profile.example.json)

It prints a decision object (JSON). Every priced line ships with a receipt:
the signals read, the points, the band, the source tier, and the math.

This file is the source of truth for the numbers. service-compendium.md is the
human-readable mirror of COMPENDIUM below; if they disagree, this file is right.
"""

import json
import os
import sys

# --- Market baseline: mirror of service-compendium.md -----------------------
# hours = [LOW, MID, HIGH], price = market sanity band, buffer = risk buffer.
COMPENDIUM = {
    "workflow-simple":     {"hours": [4, 10, 18],     "price": [500, 1200, 2000],     "buffer": 0.25, "run_cost": "$9-150/mo platform"},
    "workflow-multi":      {"hours": [15, 40, 65],     "price": [2000, 5000, 8000],    "buffer": 0.25, "run_cost": "$30-150/mo platform"},
    "workflow-complex":    {"hours": [40, 90, 200],    "price": [5000, 12000, 25000],  "buffer": 0.25, "run_cost": "$60-800/mo platform"},
    "chatbot-faq":         {"hours": [20, 60, 120],    "price": [3000, 8000, 15000],   "buffer": 0.25, "run_cost": None},
    "chatbot-llm":         {"hours": [60, 150, 300],   "price": [8000, 20000, 40000],  "buffer": 0.25, "run_cost": "API usage"},
    "rag-pipeline":        {"hours": [60, 130, 220],   "price": [8000, 18000, 30000],  "buffer": 0.25, "run_cost": "$1,000-5,000/mo vector DB+LLM"},
    "rag-multisource":     {"hours": [110, 220, 450],  "price": [15000, 30000, 60000], "buffer": 0.25, "run_cost": "$1,000-15,000/mo"},
    "ai-agent-single":     {"hours": [40, 80, 120],    "price": [5000, 10000, 15000],  "buffer": 0.25, "run_cost": "API usage"},
    "ai-agent-multistep":  {"hours": [160, 320, 600],  "price": [20000, 45000, 80000], "buffer": 0.25, "run_cost": "API usage"},
    "voice-agent-inbound": {"hours": [40, 80, 150],    "price": [5000, 10000, 20000],  "buffer": 0.25, "run_cost": "$0.14-0.50/min"},
    "prompt-optimization": {"hours": [10, 20, 35],     "price": [2000, 3500, 5000],    "buffer": 0.25, "run_cost": None},
    "prompt-strategy":     {"hours": [40, 65, 100],    "price": [8000, 12000, 15000],  "buffer": 0.25, "run_cost": None},
    "fine-tune-lora":      {"hours": [40, 90, 190],    "price": [5000, 12000, 25000],  "buffer": 0.25, "run_cost": "GPU rental"},
    "scrape-ai-pipeline":  {"hours": [60, 130, 300],   "price": [8000, 18000, 40000],  "buffer": 0.25, "run_cost": "scrape infra"},
    "doc-processing":      {"hours": [40, 90, 190],    "price": [5000, 12000, 25000],  "buffer": 0.25, "run_cost": "API usage"},
    "email-ai":            {"hours": [22, 60, 110],    "price": [3000, 8000, 15000],   "buffer": 0.25, "run_cost": "API usage"},
    "folder-agent":        {"hours": [12, 30, 60],     "price": [1500, 4000, 8000],    "buffer": 0.25, "run_cost": None},
    "ai-audit":            {"hours": [8, 16, 30],      "price": [3000, 5000, 10000],   "buffer": 0.15, "run_cost": None},
    "ai-roadmap":          {"hours": [40, 80, 140],    "price": [15000, 30000, 50000], "buffer": 0.15, "run_cost": None},
    "api-integration":     {"hours": [8, 20, 50],      "price": [700, 2000, 5000],     "buffer": 0.15, "run_cost": None},
    "landing-page":        {"hours": [10, 30, 70],     "price": [1000, 3500, 8000],    "buffer": 0.15, "run_cost": "hosting $0-50/mo"},
    "dashboard-internal":  {"hours": [22, 60, 150],    "price": [3000, 8000, 20000],   "buffer": 0.15, "run_cost": "hosting $20-200/mo"},
}

BAND_NAMES = ["LOW", "MID", "HIGH"]
REQUIRED_SIGNALS = ["integration_count", "accuracy_critical", "custom_ui", "data_access", "net_new_build"]

DISCOVERY = {
    "integration_count": "How many external systems or tools does this need to connect to?",
    "accuracy_critical": "Is there a hard accuracy or compliance bar (legal, medical, financial)?",
    "custom_ui": "Does this need a custom interface, or is a basic/existing UI fine?",
    "data_access": "Will this need access to the client's data or internal systems?",
    "net_new_build": "Is this built from scratch, or configuring something that already exists?",
    "model": ("Is the deliverable list fixed and final, or still being figured out? "
              "Is this a one-time build or an ongoing relationship? "
              "Is there a measurable dollar saving you can point to?"),
}


def score_signals(sig):
    """Sum the per-signal weights. Mirrors pricing-formula.md Step 1."""
    pts = 0
    ic = sig.get("integration_count") or 0
    if ic >= 3:
        pts += 2
    elif ic >= 1:
        pts += 1
    for key in ("accuracy_critical", "custom_ui", "data_access", "net_new_build"):
        if sig.get(key) is True:
            pts += 1
    return pts


def band_index(points):
    """Points -> band. 0-1 LOW, 2-3 MID, 4-6 HIGH."""
    if points <= 1:
        return 0
    if points <= 3:
        return 1
    return 2


def missing_signals(sig):
    return [k for k in REQUIRED_SIGNALS if sig.get(k) is None]


def resolve_model(eng, profile):
    """The pricing-model decision tree. First match wins, dangerous cases first."""
    cp, sb, og = eng.get("client_paced"), eng.get("scope_bounded"), eng.get("ongoing")
    rm, roi = eng.get("roi_measurable"), eng.get("roi_amount_usd")
    if cp is None and sb is None and og is None:
        return None  # cannot resolve honestly
    if cp is True or sb is False:
        return ("HOURLY", "fired on client_paced or scope_bounded=false",
                "avoids a flat fee on an open/client-paced scope and eating the overruns")
    if og is True:
        return ("RETAINER", "fired on ongoing=true",
                "avoids a one-time fee on a recurring relationship and giving away maintenance")
    if rm is True and roi is not None and roi >= profile.get("value_threshold", 50000):
        return ("VALUE-BASED", "fired on measurable ROI above the value threshold",
                "avoids billing hourly on high-ROI automation and capping your upside")
    if sb is True:
        return ("FLAT", "fired on scope_bounded=true, estimable, not ongoing",
                "avoids billing hourly on a clean bounded deliverable and capping your upside")
    return None  # scope unknown and nothing else fired -> block


def base_hours_for(line, profile):
    """Pick base hours by tier. Returns (hours, band_or_None, points_or_None, tier, source)."""
    key = line["service_key"]
    sig = line.get("signals", {})
    override = line.get("hours_override")
    if override is not None:
        return override, None, None, "USER-OVERRIDE", "your override of the looked-up hours"
    # Tier 1: a logged past job with the same key
    past = [j for j in profile.get("past_jobs", []) if j.get("service_key") == key and j.get("hours")]
    if past:
        avg = sum(j["hours"] for j in past) / len(past)
        ref = past[-1]
        return avg, None, None, "TIER-1", "based on your past %s at %s h / $%s" % (key, ref["hours"], ref.get("fee", "?"))
    # Tier 2: the market compendium
    row = COMPENDIUM[key]
    pts = score_signals(sig)
    bi = band_index(pts)
    return row["hours"][bi], BAND_NAMES[bi], pts, "TIER-2", "compendium %s band, %d pts" % (BAND_NAMES[bi], pts)


def blocked(reason, questions):
    return {"status": "QUOTE-BLOCKED", "reason": reason, "discovery_questions": questions}


def price_quote(intake, profile):
    line_items = intake.get("line_items", [])
    eng = intake.get("engagement", {})
    if not line_items:
        return blocked("No line items in the intake.", ["What is the work? Describe each deliverable."])

    # --- Validate before pricing -------------------------------------------
    questions, reasons = [], []
    for li in line_items:
        key = li.get("service_key")
        if key not in profile.get("service_menu", []):
            reasons.append("'%s' is not on your service menu" % key)
            questions.append("I don't have '%s' on your menu. Which listed service is it closest to, "
                             "or describe the deliverable so we can add a compendium row?" % key)
            continue
        if key not in COMPENDIUM:
            reasons.append("'%s' has no compendium row" % key)
            questions.append("'%s' isn't in the compendium yet. Add a row with its hours band first." % key)
            continue
        if li.get("hours_override") is None:
            for m in missing_signals(li.get("signals", {})):
                reasons.append("%s: signal '%s' is unknown" % (key, m))
                questions.append(DISCOVERY[m])
    if reasons:
        return blocked("; ".join(reasons), list(dict.fromkeys(questions)))

    model = resolve_model(eng, profile)
    if model is None:
        return blocked("Not enough engagement detail to pick a pricing model honestly.", [DISCOVERY["model"]])

    # --- Price each line ----------------------------------------------------
    rate = profile["rate"]
    overhead_pct = profile.get("overhead_pct", 0.10)
    priced, run_costs = [], []
    subtotal = 0.0
    labor_prebuffer = 0.0
    band_low_sum = band_high_sum = 0
    for li in line_items:
        key = li["service_key"]
        row = COMPENDIUM[key]
        base, band, pts, tier, source = base_hours_for(li, profile)
        buffer = row["buffer"]
        buffered = base * (1 + buffer)
        labor = buffered * rate
        subtotal += labor
        labor_prebuffer += base * rate
        band_low_sum += row["price"][0]
        band_high_sum += row["price"][2]
        if row["run_cost"]:
            run_costs.append({"service_key": key, "monthly": row["run_cost"]})
        priced.append({
            "service_key": key, "tier": tier, "source": source,
            "points": pts, "band": band,
            "base_hours": round(base, 1), "buffer_pct": buffer,
            "buffered_hours": round(buffered, 1), "labor": int(round(labor)),
        })

    overhead = subtotal * overhead_pct
    price_raw = subtotal + overhead
    floor = profile.get("floor", 0)
    floor_applied = price_raw < floor
    price = max(price_raw, floor)

    # --- Value-based ceiling, only if the tree said so ----------------------
    value_block = None
    if model[0] == "VALUE-BASED":
        share = profile.get("value_share", 0.15)
        value_price = share * eng["roi_amount_usd"]
        recommended = max(price, value_price)
        value_block = {
            "cost_based_floor": int(round(price)),
            "value_share": share,
            "roi_amount_usd": eng["roi_amount_usd"],
            "value_price": int(round(value_price)),
            "recommended": int(round(recommended)),
            "note": "Cost-plus is the floor; %d%% of first-year ROI is the target." % int(share * 100),
        }

    # --- Rate check: is the RATE sane? (base effort only, before buffer) -----
    # Checks the hourly rate, NOT the final quote. The quote is higher by design
    # (it adds the risk buffer and overhead). We also report where the final
    # quote lands vs. the market band, so nothing is hidden.
    base_labor = int(round(labor_prebuffer))
    tail = "The quote ($%s) adds the risk buffer and overhead on top of this base." % int(round(price))
    if base_labor < band_low_sum:
        rate_check = "Rate looks LOW: base effort $%s is under the market range $%s-$%s -- you may be underquoting. %s" % (base_labor, band_low_sum, band_high_sum, tail)
    elif base_labor > band_high_sum:
        rate_check = "Rate looks HIGH: base effort $%s is over the market range $%s-$%s -- justify the premium. %s" % (base_labor, band_low_sum, band_high_sum, tail)
    else:
        rate_check = "Rate is market-sane: base effort $%s sits inside $%s-$%s. %s" % (base_labor, band_low_sum, band_high_sum, tail)
    quote_vs_band = "above" if price > band_high_sum else ("below" if price < band_low_sum else "within")

    return {
        "status": "QUOTED",
        "studio": profile.get("studio_name", ""),
        "currency": "USD",
        "line_items": priced,
        "subtotal": int(round(subtotal)),
        "overhead_pct": overhead_pct,
        "overhead": int(round(overhead)),
        "price": int(round(price)),
        "floor_applied": floor_applied,
        "pricing_model": {"model": model[0], "reason": model[1], "trap_avoided": model[2]},
        "value_based": value_block,
        "rate_check": rate_check,
        "quote_vs_band": quote_vs_band,
        "market_band": [band_low_sum, band_high_sum],
        "run_costs": run_costs,
    }


def resolve_profile_path(explicit):
    """Durable profile resolution: an explicit path wins; else the user's saved
    profile.json next to this script; else the shipped demo. So a returning user
    is always priced against their own saved profile, with zero re-setup."""
    if explicit:
        return explicit
    here = os.path.dirname(os.path.abspath(__file__))
    own = os.path.join(here, "profile.json")
    demo = os.path.join(here, "profile.example.json")
    return own if os.path.exists(own) else demo


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 price_calc.py <intake.json> [profile.json]")
        print("  profile defaults to reference/profile.json, else profile.example.json")
        sys.exit(2)
    profile_path = resolve_profile_path(args[1] if len(args) > 1 else None)
    with open(args[0]) as f:
        intake = json.load(f)
    with open(profile_path) as f:
        profile = json.load(f)
    print(json.dumps(price_quote(intake, profile), indent=2))


if __name__ == "__main__":
    main()
