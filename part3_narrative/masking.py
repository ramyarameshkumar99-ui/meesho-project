"""
Part 3.4 — Masking policy.

Any narrative that could reach an external-facing summary must never
expose a raw reseller name. This module provides:

  - alias_for(reseller_id): a stable, non-identifying alias for a reseller.
  - assert_no_raw_names_leak(text, reseller_names): a guardrail that
    checks a piece of narrative text for verbatim raw reseller names.
"""


def alias_for(reseller_id: str) -> str:
    """
    Turn a reseller_id like 'RS019' into an external-safe alias like
    'ALIAS-19'. The numeric suffix of the reseller_id (after the 'RS'
    prefix) is kept so the alias stays traceable internally, but the
    human-readable reseller_name is never exposed.
    """
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """
    Return False if any raw reseller_name string appears verbatim inside
    text. Return True only if none of the supplied raw names leak into
    the text at all.
    """
    for name in reseller_names:
        if name in text:
            return False
    return True


if __name__ == "__main__":
    # Positive-case sanity checks
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"

    top_reseller_names = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5",
    ]

    safe_narrative = (
        "In the West region, top performer ALIAS-19 continued to lead "
        "total spend this quarter, followed by ALIAS-22 in the same region. "
        "In the South, ALIAS-12 posted the third-highest spend nationally."
    )
    assert assert_no_raw_names_leak(safe_narrative, top_reseller_names) is True

    # Negative case: a version that still leaks a raw name
    leaky_narrative = (
        "In the West region, top performer Mumbai Reseller 1 continued to "
        "lead total spend this quarter."
    )
    assert assert_no_raw_names_leak(leaky_narrative, top_reseller_names) is False

    print("All masking.py self-checks passed.")
