"""
Part 4 — Mock Agent Runner.

Ties Parts 1-3 together into one repeatable, guarded, human-reviewed
pipeline. Imports Part 2's growth_engine functions UNMODIFIED and uses
Part 3's prompt-pack structure (Context -> Insight -> Implication) as a
deterministic, offline template-fill for drafting -- no API key, no
network call, no real message send anywhere in this file.
"""

import csv
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "part2_engine"))

from growth_engine import mom_growth, is_flagged, validate_feed  # noqa: E402

TOP_N_TO_DRAFT = 3
MONTH_ORDER = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


def _read_month_feed(csv_path: str) -> dict:
    """Read a month,category,revenue,n_orders CSV into {category: revenue}."""
    revenues = {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            revenues[row["category"]] = float(row["revenue"])
    return revenues


def _draft_message(category: str, prev_month: str, month: str,
                    previous_revenue: float, current_revenue: float,
                    mom_pct: float) -> str:
    """
    Part 3's prompt-pack template-fill, applied offline/deterministically.
    Every number placed into the message is one of the supplied arguments
    -- nothing here is invented or recalculated differently.
    """
    direction = "grew" if mom_pct > 0 else "fell"
    return (
        f"Context: {category} revenue is being measured for {month} vs. {prev_month}. "
        f"Insight (FACT): {category} revenue {direction} from INR {previous_revenue} "
        f"in {prev_month} to INR {current_revenue} in {month}, a Month-on-Month change "
        f"of {mom_pct}%. "
        f"Implication: Review the {category} order-count and status breakdown for "
        f"{month} to confirm the driver of this change before escalating further "
        f"(HYPOTHESIS: the cause has not yet been confirmed from revenue figures alone)."
    )


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """
    Execute subtasks 1-8 of the agent's Planner (see part4_agent/agent_spec.md)
    and return the structured JSON-serializable result dict.
    """
    prev_month_index = MONTH_ORDER.index(month) - 1
    prev_month = MONTH_ORDER[prev_month_index] if prev_month_index >= 0 else "Prior"

    # Subtask 1: load the monthly revenue feed and run validate_feed.
    is_valid, errors = validate_feed(current_month_csv)

    # Subtask 2: if invalid, Hard Stop and report errors.
    if not is_valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    # Subtask 3: compute mom_growth for every category against the previous month.
    previous_revenues = _read_month_feed(previous_month_csv)
    current_revenues = _read_month_feed(current_month_csv)

    evaluations = []
    for category, current_revenue in current_revenues.items():
        if category not in previous_revenues:
            continue
        previous_revenue = previous_revenues[category]
        pct = mom_growth(previous_revenue, current_revenue)
        # Subtask 4: run is_flagged on every category.
        classification = is_flagged(pct)
        evaluations.append({
            "category": category,
            "mom_pct": pct,
            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
            "classification": classification,
        })

    flagged = [e for e in evaluations if e["classification"] == "flagged"]
    escalated = [e for e in evaluations if e["classification"] == "escalate_exact_boundary"]

    # Subtask 5: sort flagged categories by abs(mom_pct) descending.
    flagged.sort(key=lambda e: abs(e["mom_pct"]), reverse=True)

    # Subtask 6: draft a message for at most the top 3 by magnitude.
    flagged_categories_out = []
    for e in flagged[:TOP_N_TO_DRAFT]:
        message = _draft_message(
            e["category"], prev_month, month,
            e["previous_revenue"], e["current_revenue"], e["mom_pct"],
        )
        flagged_categories_out.append({
            "category": e["category"],
            "mom_pct": e["mom_pct"],
            "previous_revenue": e["previous_revenue"],
            "current_revenue": e["current_revenue"],
            "drafted": True,
            "message": message,
        })

    # Subtask 7: log remaining flagged categories beyond the cap as suppressed.
    suppressed_categories_out = [e["category"] for e in flagged[TOP_N_TO_DRAFT:]]

    # Subtask 7b: log escalate_exact_boundary categories separately.
    escalated_categories_out = [e["category"] for e in escalated]

    # Subtask 8: emit one structured JSON object.
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories_out,
        "suppressed_categories": suppressed_categories_out,
        "escalated_categories": escalated_categories_out,
        "action_taken": "drafted_and_held_for_approval",
    }


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    feeds = os.path.join(base, "monthly_feeds")
    fixtures = os.path.join(base, "..", "part2_engine", "fixtures")

    print("=== May scenario (April -> May) ===")
    may_result = run("May", os.path.join(feeds, "april.csv"), os.path.join(feeds, "may.csv"))
    print(json.dumps(may_result, indent=2))

    print("\n=== June scenario (May -> June) ===")
    june_result = run("June", os.path.join(feeds, "may.csv"), os.path.join(feeds, "june.csv"))
    print(json.dumps(june_result, indent=2))

    print("\n=== Corrupted feed scenario (May -> corrupted July) ===")
    corrupted_result = run(
        "July",
        os.path.join(feeds, "may.csv"),
        os.path.join(fixtures, "corrupted_feed.csv"),
    )
    print(json.dumps(corrupted_result, indent=2))
