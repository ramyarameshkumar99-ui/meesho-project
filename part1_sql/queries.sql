-- Part 1 — SQL Business Query Engine
-- Run against data/meesho_reseller.db
-- Usage example: sqlite3 data/meesho_reseller.db < part1_sql/queries.sql

-- ============================================================
-- Query 1: Monthly revenue by category
-- ============================================================
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END,
    category;

-- ============================================================
-- Query 2: Region-wise total revenue and order count
-- ============================================================
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;

-- ============================================================
-- Query 3: Top resellers by total spend (spend > 50000, top 5)
-- ============================================================
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- ============================================================
-- Query 4a: Resellers who have never placed an order
-- ============================================================
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

-- ============================================================
-- Query 4b: Why COUNT(*) is wrong for detecting the zero-match row
-- ------------------------------------------------------------
-- When we LEFT JOIN resellers -> orders for RS024, since RS024 has no
-- matching order, SQL still returns ONE row for RS024 with every
-- orders.* column set to NULL (this is what LEFT JOIN does: it keeps
-- the left-side row and pads the right side with NULLs).
-- COUNT(*) counts ROWS, so it counts this single NULL-padded row as 1,
-- even though there is truly ZERO real orders for RS024.
-- COUNT(order_id) counts NON-NULL values of order_id, so on this same
-- NULL-padded row it correctly returns 0.
-- Conclusion: to test "did this reseller ever order anything?" after a
-- LEFT JOIN, always use COUNT(order_id) = 0 (or COUNT(o.order_id)),
-- never COUNT(*) = 0 — COUNT(*) will never be 0 for a LEFT-JOINed row.
-- ============================================================
SELECT
    r.reseller_id,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;

-- ============================================================
-- Query 5: Average Order Value (AOV) for June, Delivered orders only
-- ============================================================
SELECT
    ROUND(SUM(quantity * unit_price) * 1.0 / COUNT(*), 2) AS aov_june_delivered
FROM orders
WHERE month = 'June' AND status = 'Delivered';
