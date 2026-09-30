# Narrative Report

## 3.2 — Worked narratives

### Narrative 1: May Ethnic Wear (+77.1% MoM, flagged)

**Context:** This update measures Ethnic Wear category revenue for May
2026 compared against April 2026, using Part 1's monthly revenue query
and Part 2's Month-on-Month growth calculation.

**Insight (FACT):** Ethnic Wear revenue grew from INR 104,520.77 in April
to INR 185,107.61 in May, a Month-on-Month change of **+77.1%**, well
above the 8% flag threshold.

**Implication:** Pull the April-vs-May order-count breakdown for Ethnic
Wear by region to see whether the growth is broad-based or concentrated
in one or two regions, and check whether May's category weighting (Ethnic
Wear made up a larger share of May's order mix than April's) reflects a
planned promotion or seasonal demand (HYPOTHESIS: this may be linked to a
seasonal/festive buying pattern or an active promotion in that category —
the revenue numbers alone do not tell us the cause). Recommend the
category team confirm current Ethnic Wear inventory levels can sustain
this order volume into June before it is treated as a durable trend.

### Narrative 2: June Ethnic Wear (-58.74% MoM, flagged)

**Context:** This update measures Ethnic Wear category revenue for June
2026 compared against May 2026, using the same Part 1/Part 2 pipeline.

**Insight (FACT):** Ethnic Wear revenue fell from INR 185,107.61 in May to
INR 76,371.53 in June, a Month-on-Month change of **-58.74%**, well beyond
the 8% flag threshold in the negative direction.

**Implication:** Compare June's Ethnic Wear order count (52) against May's
(104) to confirm whether the drop is a genuine demand fall-off or a
data/listing issue (e.g. stock-outs, delisted products), and pull the
status breakdown (Delivered/Returned/Cancelled/Pending) for June Ethnic
Wear orders specifically to rule out a spike in cancellations
(HYPOTHESIS: May's unusually high base, itself flagged as +77.1% growth,
may make June look like a steep drop by comparison rather than reflecting
a real new problem — this should be checked against April's baseline of
INR 104,520.77 before escalating further). Recommend the category
manager review reseller-level Ethnic Wear listings for the region with
the largest June order-count decline as the first concrete next step.

### Self-scoring against the refinement checklist

- **Specificity:** Passes — both narratives name the exact category
  ("Ethnic Wear"), the exact months compared ("April vs. May", "May vs.
  June"), and the exact revenue and percentage figures taken directly
  from Part 1/Part 2 output.
- **Audience fit:** Passes — both narratives are written in plain
  business language (revenue, order counts, promotions, inventory) aimed
  at a regional/category manager, with no SQL, code, or engineering
  terminology.
- **Completeness:** Passes — both narratives contain all three required
  sections (Context, Insight, Implication) in order, with no section
  missing.
- **Actionability:** Passes — each Implication names a concrete next
  step (pull a region-level order-count breakdown, check the status
  breakdown for cancellations, confirm inventory levels) rather than a
  vague instruction like "look into ethnic wear."

## 3.3 — Chart-choice justification

**Q1: "Which month had the highest total revenue?"**
(April = INR 419,417.43, May = INR 444,594.25, June = INR 398,055.24)

This is a **univariate comparison across 3 categorical time buckets**
(month), so a simple **vertical bar chart** is the right choice: one bar
per month, height = total revenue. A bar chart lets a reader see which
month is tallest within 10 seconds without needing to read exact labels,
the y-axis should start at zero so the bar heights are not visually
exaggerated, and no legend is needed since there is only a single series
(total revenue) being shown — a legend would just add clutter here. A
line chart is avoided because these are three independent monthly totals
being compared, not a continuous trend meant to be read as a slope.

**Q2: "What percentage share does Ethnic Wear represent of April's total
revenue?"** (INR 104,520.77 of INR 419,417.43 = 24.92%)

This is a **univariate part-to-whole comparison** (one category's share
of one month's total), so a **single stacked/100% bar** (or a simple
horizontal bar showing "Ethnic Wear" vs "Rest of April") communicates the
share faster than a pie chart. A 100%-stacked bar is preferred over a pie
chart here because bar length is easier for a reader's eye to judge
accurately than a pie wedge's angle, and it still reads within 10 seconds.
A legend is used only because there are two segments being shown (Ethnic
Wear vs. the remaining four categories combined), and 3D is avoided
entirely since 3D distorts the visual proportions of both bars and pies.

**Q3: "How do the four regions compare on total revenue?"**
(North = INR 337,125.46, South = INR 316,736.68, East = INR 275,098.45,
West = INR 333,106.33)

This is again a **univariate comparison across 4 categorical groups**
(region), so a **vertical bar chart**, one bar per region ordered either
alphabetically or by revenue descending, is the clearest choice — the
reader can see North and West are close to each other and clearly ahead
of East within 10 seconds. The y-axis starts at zero (per the
chart-selection principle) so the four bars are proportionally honest,
and since there is only one metric (revenue) being plotted per region, no
legend is required.

(No chart images are created or uploaded per the submission rules — the
above is written justification only.)
