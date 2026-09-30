# Part 1 SQL Output — Notes

## Why COUNT(*) is the wrong way to detect a zero-match LEFT JOIN row

When we run:

```sql
SELECT r.reseller_id, COUNT(*) AS count_star, COUNT(o.order_id) AS count_order_id
FROM resellers r LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;
```

we get exactly one output row: `RS024, count_star=1, count_order_id=0`.

This is because a `LEFT JOIN` always keeps every row from the left table
(`resellers`), even when there is no matching row on the right (`orders`).
When there is no match, SQLite pads all of the right-side columns
(including `order_id`) with `NULL` — but it still returns **one row**.

- `COUNT(*)` counts **rows**, so it counts this single NULL-padded row as 1,
  even though RS024 truly has zero real orders.
- `COUNT(order_id)` counts only **non-NULL values** of `order_id`, so on
  this same row it correctly returns 0.

**Conclusion:** after a LEFT JOIN, always test `COUNT(order_id) = 0` (or
`COUNT(o.order_id) = 0`) to detect "no matching rows" — never `COUNT(*) = 0`,
because `COUNT(*)` will never be 0 for a row that a LEFT JOIN has already
produced.

## File map
- `monthly_category_revenue.csv` — Query 1. Feeds Part 2 and Part 4 directly.
- `region_revenue.csv` — Query 2.
- `top_resellers.csv` — Query 3.
- `resellers_never_ordered.csv` — Query 4a.
- `count_star_vs_count_order_id.csv` — Query 4b (see explanation above).
- `aov_june_delivered.csv` — Query 5.
