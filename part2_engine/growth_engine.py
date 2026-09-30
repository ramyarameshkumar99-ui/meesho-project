"""
Part 2 — Python Guardrail & Growth-Detection Engine.

Three small, pure functions:
  - mom_growth: compute Month-on-Month growth percentage.
  - is_flagged: turn a growth number into a decision string
                ("flagged" / "not_flagged" / "escalate_exact_boundary").
  - validate_feed: an input guardrail that checks a
                    month,category,revenue,n_orders CSV for bad rows.

These are imported UNMODIFIED by Part 4's mock agent runner.
"""

import csv


def mom_growth(previous: float, current: float) -> float:
    """Return the Month-on-Month growth percentage, rounded to 2 decimals."""
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """
    Classify a MoM growth percentage against a threshold.

    Returns one of three strings (never a bare boolean):
      - "flagged"                 if abs(mom_pct) > threshold
      - "not_flagged"             if abs(mom_pct) < threshold
      - "escalate_exact_boundary" if abs(mom_pct) == threshold exactly
        (held for human review — never silently auto-decided).
    """
    magnitude = abs(mom_pct)
    if magnitude == threshold:
        return "escalate_exact_boundary"
    if magnitude > threshold:
        return "flagged"
    return "not_flagged"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """
    Guardrail over a month,category,revenue,n_orders CSV.

    Checks every data row (line 2 onward, 1-indexed including the header
    as line 1) for:
      - blank category
      - blank revenue
      - revenue that is not parseable as a float
      - revenue that parses but is negative

    Returns (True, []) if there are zero errors, else (False, errors).
    """
    errors: list[str] = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            line_number = i + 2  # header is line 1, first data row is line 2
            month = row.get("month", "")
            category = row.get("category", "")
            revenue_raw = row.get("revenue", "")

            if category is None or category.strip() == "":
                errors.append(f"line {line_number}: missing category (month={month})")
                continue

            if revenue_raw is None or revenue_raw.strip() == "":
                errors.append(f"line {line_number}: missing revenue (category={category})")
                continue

            try:
                revenue = float(revenue_raw)
            except ValueError:
                errors.append(f"line {line_number}: revenue not numeric: {revenue_raw!r}")
                continue

            if revenue < 0:
                errors.append(
                    f"line {line_number}: negative revenue ({revenue}) for category={category}"
                )

    return (len(errors) == 0, errors)
