# Intake Schema

The closed contract the model fills from a raw request — the only thing the model produces; the engine decides the rest. `rules.md` STAGE 2 points here to fill the intake, and the QUOTE-BLOCKED lane uses the discovery questions below.

## The intake (what you fill)

```
line_items:
  - service_key: string        # an exact key from the profile service_menu
    signals:
      integration_count: int    # external systems to connect (0, 1-2, 3+)
      accuracy_critical: bool    # a hard accuracy/compliance bar
      custom_ui: bool            # bespoke interface required
      data_access: bool          # needs client data or internal systems
      net_new_build: bool        # from scratch vs. configured
    hours_override: number|null  # only if the user gives you firm hours
engagement:
  scope_bounded: bool|null       # deliverable list fixed and final
  ongoing: bool|null             # recurring/maintenance relationship
  roi_measurable: bool|null      # quantifiable dollar saving
  roi_amount_usd: number|null    # that annual figure
  client_paced: bool|null        # client controls timeline/iteration
```

Set every field you can read from the request; leave anything you genuinely cannot determine as `null`. The signal set is **fixed**: do not add a signal the engine ignores, and do not *score* a signal — that is the engine's job. Use only `service_key`s from the profile's `service_menu`.

## Discovery questions (the QUOTE-BLOCKED lane)

When a required field is missing, the engine routes to QUOTE-BLOCKED and emits the matching question. `price_calc.py` is the runtime source; this table is its human-readable mirror — keep the two in sync.

| Missing | Ask |
|---|---|
| `integration_count` | How many external systems or tools does this connect to? |
| `accuracy_critical` | Is there a hard accuracy or compliance bar (legal, medical, financial)? |
| `custom_ui` | Does this need a custom interface, or is a basic/existing UI fine? |
| `data_access` | Will this need access to the client's data or internal systems? |
| `net_new_build` | Built from scratch, or configuring something that exists? |
| pricing model | Is the scope fixed or still forming? One-time or ongoing? Any measurable dollar saving? |
| unknown `service_key` | Which menu service is this closest to, or describe it so we can add a row? |
