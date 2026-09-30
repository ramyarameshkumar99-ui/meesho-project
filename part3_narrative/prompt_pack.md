# Prompt Pack — Flagged-Category Stakeholder Update

A single, reusable prompt pack for turning one flagged category's verified
Part 1/Part 2 numbers into a stakeholder-ready narrative, without ever
inventing a figure.

## Trigger

This prompt fires whenever a category's `is_flagged(mom_pct)` result is
exactly `"flagged"` (i.e. `abs(mom_pct) > 8.0`). It is never triggered for
`"not_flagged"` or `"escalate_exact_boundary"` categories — the boundary
case is routed to human review instead, not to auto-narration.

## Input list

Every placeholder the prompt needs, all of which must come directly from
Part 1/Part 2 output — never invented:

- `{category}` — the category name, e.g. "Ethnic Wear"
- `{month}` — the current month being reported, e.g. "May"
- `{prev_month}` — the prior month being compared against, e.g. "April"
- `{previous_revenue}` — prior month's revenue for this category (₹)
- `{current_revenue}` — current month's revenue for this category (₹)
- `{mom_pct}` — the signed Month-on-Month growth percentage from `mom_growth`

## Prompt

```
You are drafting a short stakeholder update for a Meesho regional category
manager. Use ONLY the numbers supplied below — never state a number that is
not one of the placeholders given to you.

Category: {category}
Comparing: {month} vs. {prev_month}
Previous month revenue: INR {previous_revenue}
Current month revenue: INR {current_revenue}
Month-on-Month change: {mom_pct}%

Write the update in exactly three labeled parts:

Context: One sentence stating what is being measured and over what period
(i.e. {category} revenue, {prev_month} vs. {month}).

Insight: One sentence stating the {mom_pct}% change as a labeled FACT
(the number must be copied exactly from the placeholder above, not
recalculated or rounded differently).

Implication: One or two sentences giving a specific, actionable next step.
If the recommendation proposes a CAUSE for the change that the numbers
alone do not prove, label that sentence explicitly as a HYPOTHESIS.
Do not give a vague instruction like "look into it" — name the concrete
thing to check (e.g. a specific report, a specific team, a specific
comparison to run).

Do not add any number, percentage, or figure anywhere in the output that
was not explicitly supplied above.
```

## Checklist

Run all of the following checks on the drafted output before it is used or
shown to anyone:

1. **Number-fidelity check** — every number that appears in the draft
   matches one of the supplied placeholder values exactly (same digits,
   same sign); no number appears that wasn't supplied.
2. **Fact/hypothesis labeling check** — every claim about *why* something
   happened is explicitly labeled a hypothesis, and every claim about
   *what* happened (the measured number) is explicitly labeled a fact.
3. **Actionability check** — the Implication names a specific, concrete
   next step (a report to pull, a team to contact, a comparison to run) —
   not a vague phrase like "look into" or "monitor closely."
4. **No-raw-name check** — no reseller is referenced by raw `reseller_name`
   anywhere in the draft; only `region` and `alias_for(reseller_id)` may be
   used if a specific reseller must be mentioned (see `masking.py`).
5. **Structure check** — the draft contains exactly the three labeled
   sections, Context / Insight / Implication, in that order, and nothing
   else.
