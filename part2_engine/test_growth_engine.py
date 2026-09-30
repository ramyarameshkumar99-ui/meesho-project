"""
Given-When-Then style tests for Part 2's growth_engine.

Run with:  python3 -m pytest part2_engine/test_growth_engine.py -v
       or: python3 part2_engine/test_growth_engine.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from growth_engine import mom_growth, is_flagged, validate_feed

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def test_may_ethnic_wear_is_flagged():
    # GIVEN April -> May Ethnic Wear revenue moves from 104520.77 to 185107.61
    previous, current = 104520.77, 185107.61
    # WHEN mom_growth then is_flagged run on it
    pct = mom_growth(previous, current)
    result = is_flagged(pct)
    # THEN mom_growth returns 77.1 and is_flagged returns "flagged"
    assert pct == 77.1
    assert result == "flagged"


def test_june_beauty_is_not_flagged():
    # GIVEN May -> June Beauty & Personal Care revenue moves from 35542.11 to 37559.07
    previous, current = 35542.11, 37559.07
    # WHEN evaluated
    pct = mom_growth(previous, current)
    result = is_flagged(pct)
    # THEN mom_growth returns 5.67 and is_flagged returns "not_flagged"
    assert pct == 5.67
    assert result == "not_flagged"


def test_exact_boundary_escalates():
    # GIVEN a synthetic pair chosen so growth is exactly on the threshold boundary
    previous, current = 100000, 108000
    # WHEN evaluated
    pct = mom_growth(previous, current)
    result = is_flagged(pct)
    # THEN mom_growth returns exactly 8.0 and is_flagged returns
    # "escalate_exact_boundary" -- not "flagged" and not "not_flagged"
    assert pct == 8.0
    assert result == "escalate_exact_boundary"
    assert result != "flagged"
    assert result != "not_flagged"


def test_corrupted_feed_returns_exactly_three_errors_in_order():
    # GIVEN the corrupted feed fixture
    path = os.path.join(FIXTURES_DIR, "corrupted_feed.csv")
    # WHEN validate_feed runs on it
    ok, errors = validate_feed(path)
    # THEN it returns (False, errors) with exactly 3 entries in this order
    assert ok is False
    assert len(errors) == 3
    assert errors[0] == "line 3: negative revenue (-4200.0) for category=Western Wear"
    assert errors[1] == "line 4: missing category (month=July)"
    assert errors[2] == "line 6: missing revenue (category=Home & Kitchen)"


def test_clean_feed_passes_validation():
    # GIVEN the real, validated Part 1 output feed
    path = os.path.join(FIXTURES_DIR, "monthly_category_revenue.csv")
    # WHEN validate_feed runs on it
    ok, errors = validate_feed(path)
    # THEN all 15 rows pass with zero errors
    assert ok is True
    assert errors == []


def test_full_may_vs_april_mom_table():
    data = {
        "Ethnic Wear": (104520.77, 185107.61, 77.1, "flagged"),
        "Western Wear": (113866.15, 86998.18, -23.6, "flagged"),
        "Kids Wear": (59847.27, 45793.78, -23.48, "flagged"),
        "Home & Kitchen": (100446.23, 91152.57, -9.25, "flagged"),
        "Beauty & Personal Care": (40737.01, 35542.11, -12.75, "flagged"),
    }
    for category, (prev, curr, expected_pct, expected_flag) in data.items():
        pct = mom_growth(prev, curr)
        assert pct == expected_pct, f"{category}: expected {expected_pct}, got {pct}"
        assert is_flagged(pct) == expected_flag


def test_full_june_vs_may_mom_table():
    data = {
        "Ethnic Wear": (185107.61, 76371.53, -58.74, "flagged"),
        "Western Wear": (86998.18, 97415.64, 11.97, "flagged"),
        "Kids Wear": (45793.78, 56737.78, 23.9, "flagged"),
        "Home & Kitchen": (91152.57, 129971.22, 42.59, "flagged"),
        "Beauty & Personal Care": (35542.11, 37559.07, 5.67, "not_flagged"),
    }
    for category, (prev, curr, expected_pct, expected_flag) in data.items():
        pct = mom_growth(prev, curr)
        assert pct == expected_pct, f"{category}: expected {expected_pct}, got {pct}"
        assert is_flagged(pct) == expected_flag


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items()) if name.startswith("test_")]
    passed = 0
    for t in tests:
        t()
        passed += 1
        print(f"PASS: {t.__name__}")
    print(f"\n{passed}/{len(tests)} tests passed.")
