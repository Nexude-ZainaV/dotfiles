"""SQL snippets (portable ANSI first; MySQL / PostgreSQL / SQLite notes inline)."""

FAMILY = dict(key="sql", vscode="sql,mysql,postgres", sublime="source.sql")

SNIPPETS = [
    ("sel", "SELECT with filter, sort, limit", r"""
-- Logical evaluation order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
SELECT «1:id», «2:name»
FROM «3:customers»
WHERE «4:status = 'active'»
ORDER BY «5:created_at» DESC
LIMIT «6:20»;«0»
"""),
    ("join", "INNER / LEFT JOIN", r"""
-- INNER JOIN keeps only matching rows; LEFT JOIN keeps every row from the left table
-- and fills NULLs where the right side has no match.
SELECT «1:c».name, «2:o».id AS order_id, «2».total
FROM «3:customers» AS «1»
«4:LEFT» JOIN «5:orders» AS «2» ON «2».«6:customer_id» = «1».id
WHERE «1».«7:country» = '«8:US»';«0»
"""),
    ("grp", "GROUP BY / HAVING", r"""
-- WHERE filters rows before grouping; HAVING filters the groups after aggregation
SELECT «1:customer_id», COUNT(*) AS order_count, SUM(«2:total») AS revenue
FROM «3:orders»
WHERE «4:status» = 'paid'
GROUP BY «1»
HAVING COUNT(*) >= «5:3»
ORDER BY revenue DESC;«0»
"""),
    ("cte", "WITH (common table expression)", r"""
-- A CTE names a sub-result so the main query reads top-down instead of nested
WITH «1:recent_orders» AS (
    SELECT customer_id, total
    FROM «2:orders»
    WHERE created_at >= «3:DATE '2026-01-01'»
)
SELECT customer_id, SUM(total) AS spent
FROM «1»
GROUP BY customer_id;«0»
"""),
    ("win", "Window functions", r"""
-- Window functions compute across related rows WITHOUT collapsing them (unlike GROUP BY)
SELECT
    «1:customer_id»,
    «2:total»,
    ROW_NUMBER() OVER (PARTITION BY «1» ORDER BY «3:created_at» DESC) AS rn,        -- latest = 1
    SUM(«2»)     OVER (PARTITION BY «1» ORDER BY «3»)              AS running_total,
    RANK()       OVER (ORDER BY «2» DESC)                             AS overall_rank
FROM «4:orders»;«0»
"""),
    ("ins", "INSERT (multi-row)", r"""
-- Always list the columns: the statement keeps working if columns are added later
INSERT INTO «1:products» («2:name», «3:price»)
VALUES
    («4:'Keyboard'», «5:49.99»),
    («6:'Mouse'», «7:19.99»);«0»
"""),
    ("upd", "UPDATE (safe)", r"""
-- Run the WHERE as a SELECT first to see exactly which rows will change.
-- An UPDATE without WHERE changes every row in the table.
UPDATE «1:products»
SET «2:price» = «3:price * 0.9»
WHERE «4:category_id = 3»;«0»
"""),
    ("del", "DELETE (safe)", r"""
-- DELETE without WHERE empties the table. Inside a transaction you can still roll back.
DELETE FROM «1:sessions»
WHERE «2:expires_at < CURRENT_TIMESTAMP»;«0»
"""),
    ("upsert", "UPSERT (insert or update)", r"""
-- PostgreSQL / SQLite:
INSERT INTO «1:inventory» («2:sku», «3:qty») VALUES («4:'A-100'», «5:5»)
ON CONFLICT («2») DO UPDATE SET «3» = «1».«3» + EXCLUDED.«3»;
-- MySQL equivalent:
-- INSERT INTO «1» («2», «3») VALUES (...) AS new
-- ON DUPLICATE KEY UPDATE «3» = «1».«3» + new.«3»;«0»
"""),
    ("ct", "CREATE TABLE (migration)", r"""
-- Migration: create «1:orders». Constraints in the schema are the last line of defence
-- for data integrity: the database enforces them even if application code has a bug.
CREATE TABLE «1» (
    id           INTEGER PRIMARY KEY,                 -- MySQL: INT AUTO_INCREMENT, Postgres: GENERATED ALWAYS AS IDENTITY
    «2:customer_id»  INTEGER NOT NULL REFERENCES «3:customers»(id) ON DELETE CASCADE,
    «4:status»       VARCHAR(20) NOT NULL DEFAULT 'pending'
                 CHECK («4» IN ('pending', 'paid', 'shipped', 'cancelled')),
    total        DECIMAL(10, 2) NOT NULL CHECK (total >= 0),   -- DECIMAL for money, never FLOAT
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index the foreign key: joins and ON DELETE CASCADE both look rows up by it
CREATE INDEX idx_«1»_«2» ON «1» («2»);«0»
""", {"template": True}),
    ("idx", "CREATE INDEX", r"""
-- Index columns used in WHERE / JOIN / ORDER BY. Composite index column order matters:
-- (a, b) serves queries on a, and on a + b, but not on b alone.
CREATE INDEX idx_«1:orders»_«2:status_created» ON «1» («3:status», «4:created_at»);«0»
"""),
    ("view", "CREATE VIEW", r"""
-- A view is a saved query: reuse it like a table, with the logic in one place
CREATE VIEW «1:customer_revenue» AS
SELECT c.id, c.name, COALESCE(SUM(o.total), 0) AS revenue
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'paid'
GROUP BY c.id, c.name;«0»
"""),
    ("tx", "Transaction", r"""
-- All-or-nothing: if any statement fails, ROLLBACK leaves the data untouched
BEGIN;   -- MySQL: START TRANSACTION;

UPDATE accounts SET balance = balance - «1:100» WHERE id = «2:1»;
UPDATE accounts SET balance = balance + «1» WHERE id = «3:2»;
«0»
COMMIT;   -- or ROLLBACK; to undo
"""),
    ("case", "CASE expression", r"""
-- CASE is SQL's if/else inside an expression
SELECT «1:name»,
    CASE
        WHEN «2:total» >= «3:1000» THEN 'gold'
        WHEN «2» >= «4:500» THEN 'silver'
        ELSE 'bronze'
    END AS «5:tier»
FROM «6:customers»;«0»
"""),
    ("exists", "EXISTS subquery", r"""
-- EXISTS stops at the first matching row: efficient for "has at least one ..."
SELECT c.*
FROM «1:customers» c
WHERE EXISTS (
    SELECT 1 FROM «2:orders» o WHERE o.customer_id = c.id AND o.«3:status» = 'paid'
);«0»
"""),
    ("page", "Pagination (offset vs keyset)", r"""
-- OFFSET is simple but slows down on deep pages (the DB still reads the skipped rows):
SELECT * FROM «1:posts» ORDER BY id LIMIT «2:20» OFFSET «3:40»;

-- Keyset pagination stays fast at any depth: pass the last id you saw
SELECT * FROM «1» WHERE id > «4:last_seen_id» ORDER BY id LIMIT «2»;«0»
"""),
]
