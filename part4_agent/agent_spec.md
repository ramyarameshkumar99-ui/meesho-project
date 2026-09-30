# Agent Specification — Reseller Growth & Alert Monitoring Agent

## Goal

Keep Meesho category managers informed of any category whose
Month-on-Month revenue moves beyond the 8% threshold, with a human
approving every message before it is considered sent.

## Tools

The concrete functions this agent calls, reused unmodified:

- `validate_feed(csv_path)` — Part 2. Input guardrail on the revenue feed.
- `mom_growth(previous, current)` — Part 2. Computes MoM growth %.
- `is_flagged(mom_pct)` — Part 2. Classifies growth as flagged /
  not_flagged / escalate_exact_boundary.
- Part 3's prompt-pack template-fill function — turns a flagged category's
  numbers into a Context → Insight → Implication draft message, using
  only the supplied placeholders (no invented numbers).

## Memory / State

Between runs, the agent must remember **the previous month's revenue per
category**, so that the next run's `mom_growth` has something to compare
the new month against. In this project that state is simply "the prior
month's `monthly_category_revenue.csv` feed," passed explicitly into
`run()` as `previous_month_csv` — a real deployment would persist this as
a small key-value store (category → last known revenue) instead of
requiring the caller to supply it each time.

## Planner

See the ordered subtasks in §4.2 below — load & validate, compute growth,
classify, rank, cap-and-draft, suppress the rest, escalate boundary cases,
emit one structured JSON object.

## Feedback Loop

Every drafted message is held in the `flagged_categories[].message` field
with `drafted = true`. No message is ever actually transmitted by this
agent — `action_taken` is set to `"drafted_and_held_for_approval"`, and a
human (the category manager or an analyst) must review and approve each
draft before any real send happens outside this system. This project
intentionally simulates that boundary as a flag in the JSON output; no
Gmail/SMTP integration is implemented or in scope.

## Guardrails

- **Input guardrail:** `validate_feed` must return `(True, [])` before
  anything else runs. If it returns `(False, errors)`, the run is a Hard
  Stop — no MoM computation, no drafting, is attempted on invalid data.
- **Action guardrail:** no message is ever auto-sent by this agent — every
  message is only drafted and held for human approval
  (`action_taken = "drafted_and_held_for_approval"`).
- **Output guardrail:** every number that appears inside a drafted
  message (the category name and the `mom_pct` value) must trace back
  directly to a Part 1/Part 2 value — no invented figures are ever
  written into a message string.

## Success and error stopping conditions

- **Success:** the run produces drafts for the top flagged categories (or
  correctly produces zero drafts if nothing crossed the threshold), and
  every number in every draft is traceable to Part 1/Part 2 output.
- **Error:** `validate_feed` returns `False` — the run is a **Hard Stop**.
  The validation errors are surfaced in `validation_errors`, and the run
  is never silently skipped or partially processed.

## Given-When-Then specs (agent-level, reused from Part 2)

1. **GIVEN** April→May Ethnic Wear revenue moves from 104520.77 to
   185107.61, **WHEN** the agent computes `mom_growth` then `is_flagged`
   on it, **THEN** the agent records `mom_pct = 77.1` and classification
   `"flagged"` for Ethnic Wear in that run's output.
2. **GIVEN** May→June Beauty & Personal Care revenue moves from 35542.11
   to 37559.07, **WHEN** the agent evaluates it, **THEN** the agent
   records `mom_pct = 5.67` and classification `"not_flagged"`, and
   Beauty & Personal Care appears in neither `flagged_categories` nor
   `suppressed_categories` for that run.
3. **GIVEN** a synthetic category pair where growth lands exactly on the
   8.0% threshold boundary, **WHEN** the agent evaluates it, **THEN** the
   agent records classification `"escalate_exact_boundary"` and adds that
   category to `escalated_categories` — it is never drafted and never
   silently dropped.
4. **GIVEN** a corrupted current-month feed (as in Part 2's
   `corrupted_feed.csv` fixture), **WHEN** the agent runs `validate_feed`
   on it as subtask 1, **THEN** the agent immediately Hard Stops with
   `validation_status = "invalid"`, `action_taken = "hard_stop"`, and the
   exact 3 validation error strings surfaced — no MoM computation or
   drafting is attempted.

## 4.2 — Ordered subtasks (Planner)

1. Load the monthly revenue feed and run `validate_feed`.
2. If invalid, **Hard Stop** and report the validation errors.
3. If valid, compute `mom_growth` for every category against the previous
   month.
4. Run `is_flagged` on every category's growth percentage.
5. Sort flagged categories by `abs(mom_pct)` descending.
6. Draft a message (via Part 3's template) for **at most the top 3** by
   magnitude — this cap exists specifically to prevent the
   notification-flooding failure mode of drafting (and eventually
   sending) one message per flagged item with no limit.
7. Log any remaining flagged categories beyond the cap as
   `"suppressed, review manually"`, without drafting a message for them.
7b. Separately, log any category whose `is_flagged` result is
   `"escalate_exact_boundary"` into `escalated_categories`, without
   drafting a message for it — an exact-boundary category is neither
   flagged nor not_flagged, so it must never be silently dropped from
   both lists or mistaken for either one.
8. Emit one structured JSON object per run (see §4.3).

## 4.3 — Structured JSON output schema

Every run emits exactly this shape:

```json
{
  "run_month": "May",
  "validation_status": "valid",
  "validation_errors": [],
  "flagged_categories": [
    {
      "category": "Ethnic Wear",
      "mom_pct": 77.1,
      "previous_revenue": 104520.77,
      "current_revenue": 185107.61,
      "drafted": true,
      "message": "..."
    }
  ],
  "suppressed_categories": ["Beauty & Personal Care", "Home & Kitchen"],
  "escalated_categories": [],
  "action_taken": "drafted_and_held_for_approval"
}
```
