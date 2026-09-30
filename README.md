# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end, offline, zero-API-key pipeline: SQL → Python guardrails/growth
engine → deterministic AI-narrative templates → agent spec + mock runner.

## 0. Requirements

- Python 3.10+ (uses the `sqlite3` and `csv` standard-library modules; the
  `tuple[bool, list[str]]` type hints in Part 2 need Python 3.9+).
- No pip packages, no API keys, no paid services, no internet access required
  anywhere in this pipeline.

## 1. Regenerate the dataset

```bash
cd data
python3 generate_dataset.py
```

This is a **seeded** script (`random.Random(42)`) — do not edit the seed,
weights, or row counts, or your numbers will diverge from the ones documented
below. It writes `resellers.csv` (24 rows), `orders.csv` (900 rows: 300 each
for April/May/June 2026), and `meesho_reseller.db` (same data as SQLite).

## 2. Part 1 — SQL

The queries live in `part1_sql/queries.sql`. The exact CSV outputs already
committed under `part1_sql/output/` were produced by running these queries
against the seeded database. To reproduce them yourself:

```bash
sqlite3 data/meesho_reseller.db < part1_sql/queries.sql
```

or use the equivalent Python export (any approach is fine — the SQL text
in `queries.sql` is the source of truth). `part1_sql/output/README.md`
explains, with the actual `COUNT(*)` vs `COUNT(order_id)` result, why
`COUNT(*)` cannot be used to detect a zero-match `LEFT JOIN` row.

Part 1's `monthly_category_revenue.csv` is the direct input to Part 2 and
Part 4 — its column names (`month,category,revenue,n_orders`) must stay
exact.

## 3. Part 2 — Python guardrail & growth-detection engine

```bash
python3 part2_engine/test_growth_engine.py
# or, if pytest is installed:
python3 -m pytest part2_engine/test_growth_engine.py -v
```

`part2_engine/growth_engine.py` implements `mom_growth`, `is_flagged`, and
`validate_feed`. All 7 Given-When-Then tests pass, including the exact
3-error corrupted-feed case and the full April→May / May→June MoM tables.
`part2_engine/fixtures/` holds `corrupted_feed.csv` (a deliberately broken
feed) and `monthly_category_revenue.csv` (a copy of Part 1's real, valid
output).

## 4. Part 3 — Reliable AI narrative & prompt pack

- `part3_narrative/prompt_pack.md` — the reusable Trigger / Input list /
  Prompt / Checklist prompt pack for turning a flagged category into a
  stakeholder update.
- `part3_narrative/narrative_report.md` — worked Context → Insight →
  Implication narratives for May Ethnic Wear (+77.1%) and June Ethnic Wear
  (-58.74%), self-scored against the 4-criterion checklist, plus the
  chart-choice justification for 3 business questions (text only, no chart
  images).
- `part3_narrative/masking.py` — `alias_for()` and
  `assert_no_raw_names_leak()`. Run it directly to see both the positive
  and negative masking test cases:

```bash
python3 part3_narrative/masking.py
```

Every "AI narrative" step here is a deterministic, fully offline
template-fill function — no real LLM call is required anywhere in this
project.

## 5. Part 4 — Agent spec + mock agent runner

`part4_agent/agent_spec.md` documents the agent's Goal / Tools /
Memory-State / Planner / Feedback Loop, all three guardrail types, the
success/error stopping conditions, and the 4 Given-When-Then specs (reused
from Part 2) phrased at the agent level.

`part4_agent/mock_agent_runner.py` implements `run(month, previous_month_csv,
current_month_csv)`, importing Part 2's `growth_engine` functions
**unmodified** and using Part 3's Context/Insight/Implication template
structure to draft messages. Run all three scenarios:

```bash
python3 part4_agent/mock_agent_runner.py
```

This prints three JSON objects:
1. **May scenario** (April→May): 3 drafted (Ethnic Wear 77.1%, Western Wear
   -23.6%, Kids Wear -23.48%), 2 suppressed (Beauty & Personal Care, Home &
   Kitchen).
2. **June scenario** (May→June): 3 drafted (Ethnic Wear -58.74%, Home &
   Kitchen 42.59%, Kids Wear 23.9%), 1 suppressed (Western Wear 11.97%);
   Beauty & Personal Care (5.67%, not flagged) appears in neither list.
3. **Corrupted feed scenario**: `validation_status = "invalid"`,
   `action_taken = "hard_stop"`, and the exact 3 validation errors from
   Part 2 — no MoM computation attempted.

`escalated_categories` is `[]` in all three real scenarios, since none of
the actual April/May/June transitions land exactly on the 8.0% boundary
(that path is covered separately by Part 2's synthetic boundary test).

`part4_agent/monthly_feeds/` holds the per-month split of Part 1's
`monthly_category_revenue.csv` (`april.csv`, `may.csv`, `june.csv`), which
the runner reads via `previous_month_csv` / `current_month_csv`.

## 6. Zero API keys, confirmed

Every stage above — dataset generation, SQL, the growth engine, the
narrative templates, and the mock agent runner — runs with **no
environment variables and no API keys set**. Nothing in this pipeline makes
a network call.

## 7. How the Parts connect (workflow pattern)

- **Part 1 → Part 2**: mirrors "compute real numbers via SQL first, then
  hand off" — Part 2 never recalculates revenue itself, it only consumes
  Part 1's `monthly_category_revenue.csv`.
- **Part 2 → Part 3**: Part 2's `is_flagged` decision gates whether Part
  3's prompt pack is triggered at all (only `"flagged"` categories get a
  narrative drafted).
- **Part 2/3 → Part 4**: Part 4 mirrors an **Intake → Summary → Report
  Draft → Validate** reporting flow — Intake (`validate_feed`), Summary
  (`mom_growth` + `is_flagged` per category), Report Draft (Part 3's
  template-fill, capped at top 3), Validate (every number in a draft is
  traceable back to Part 1/Part 2, and invalid input is a Hard Stop before
  any of the later stages run at all).

## Docs referenced

Only the official Python standard-library docs for `sqlite3`, `csv`, and
`random` were consulted while implementing this project.

## Repository layout

```
data/generate_dataset.py   data/resellers.csv   data/orders.csv   data/meesho_reseller.db
part1_sql/queries.sql       part1_sql/output/*.csv
part2_engine/growth_engine.py   part2_engine/test_growth_engine.py   part2_engine/fixtures/*.csv
part3_narrative/prompt_pack.md   part3_narrative/narrative_report.md   part3_narrative/masking.py
part4_agent/agent_spec.md   part4_agent/mock_agent_runner.py   part4_agent/monthly_feeds/*.csv
README.md
```
