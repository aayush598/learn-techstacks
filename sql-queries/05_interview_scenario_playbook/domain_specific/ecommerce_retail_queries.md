# E-commerce and Retail SQL Scenarios — 100 Interview Q&A

## Q1: What is the total lifetime revenue from all completed orders?

**Schema:** orders (order_id, customer_id, order_date, status, total_amount)

**Query:**
```sql
SELECT COUNT(*) AS order_count,
       SUM(total_amount) AS lifetime_revenue
FROM orders
WHERE status = 'completed';
```
**Explanation:** Filters out cancelled/pending orders and sums the order-level amount; COUNT gives context.

## Q2: What is revenue per month?

**Schema:** orders (order_id, customer_id, order_date, status, total_amount)

**Query:**
```sql
-- MySQL
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       SUM(total_amount) AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```
**Explanation:** Groups by truncated month string so each calendar month is one row; sort keeps chronological order.

**Alt1:**
```sql
-- PostgreSQL
SELECT to_char(order_date, 'YYYY-MM') AS month,
       SUM(total_amount) AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY to_char(order_date, 'YYYY-MM')
ORDER BY month;
```

## Q3: Revenue per month but with months that have zero sales included.

**Schema:** orders (order_id, customer_id, order_date, status, total_amount)

**Query:**
```sql
-- PostgreSQL
WITH months AS (
  SELECT generate_series(
           date_trunc('month', MIN(order_date)),
           date_trunc('month', MAX(order_date)),
           interval '1 month') AS month
  FROM orders
)
SELECT to_char(m.month, 'YYYY-MM') AS month,
       COALESCE(SUM(o.total_amount), 0) AS revenue
FROM months m
LEFT JOIN orders o
       ON date_trunc('month', o.order_date) = m.month
      AND o.status = 'completed'
GROUP BY m.month
ORDER BY m.month;
```
**Explanation:** generate_series builds a dense month spine so gaps become zero-revenue rows instead of disappearing.

**Alt1:**
```sql
-- MySQL 8+ recursive CTE
WITH RECURSIVE months AS (
  SELECT DATE_FORMAT(MIN(order_date), '%Y-%m-01') AS m FROM orders
  UNION ALL
  SELECT DATE_FORMAT(DATE_ADD(STR_TO_DATE(m, '%Y-%m-01'), INTERVAL 1 MONTH), '%Y-%m-01')
  FROM months
  WHERE m < (SELECT DATE_FORMAT(MAX(order_date), '%Y-%m') FROM orders)
)
SELECT LEFT(m, 7) AS month, COALESCE(SUM(o.total_amount), 0) AS revenue
FROM months
LEFT JOIN orders o ON DATE_FORMAT(o.order_date, '%Y-%m') = LEFT(m, 7)
GROUP BY m
ORDER BY m;
```

## Q4: Top 10 best-selling products by quantity sold.

**Schema:** products (product_id, name, price), order_items (order_id, product_id, quantity, unit_price), orders (order_id, status)

**Query:**
```sql
SELECT p.product_id, p.name, SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY p.product_id, p.name
ORDER BY units_sold DESC
LIMIT 10;
```
**Explanation:** Aggregates line quantities per product and takes the largest ten; only completed orders count.

**Alt1:**
```sql
-- SQL Server
SELECT TOP 10 p.product_id, p.name, SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY p.product_id, p.name
ORDER BY SUM(oi.quantity) DESC;
```

## Q5: Top 10 products by revenue generated.

**Schema:** products (product_id, name), order_items (order_id, product_id, quantity, unit_price), orders (order_id, status)

**Query:**
```sql
SELECT p.product_id, p.name,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY p.product_id, p.name
ORDER BY revenue DESC
LIMIT 10;
```
**Explanation:** Extended price (qty x unit price) is the revenue measure; ranks highest first.

**Alt1:**
```sql
-- ranked alternative without LIMIT
SELECT product_id, name, revenue
FROM (
  SELECT p.product_id, p.name,
         SUM(oi.quantity * oi.unit_price) AS revenue,
         RANK() OVER (ORDER BY SUM(oi.quantity * oi.unit_price) DESC) AS rk
  FROM order_items oi
  JOIN products p ON p.product_id = oi.product_id
  JOIN orders o ON o.order_id = oi.order_id
  WHERE o.status = 'completed'
  GROUP BY p.product_id, p.name
) t
WHERE rk <= 10;
```

## Q6: What is the average number of items per order?

**Schema:** order_items (order_id, product_id, quantity), orders (order_id, order_date, status)

**Query:**
```sql
SELECT AVG(item_qty) AS avg_items_per_order
FROM (
  SELECT oi.order_id, SUM(oi.quantity) AS item_qty
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  WHERE o.status = 'completed'
  GROUP BY oi.order_id
) t;
```
**Explanation:** First computes total units per order, then averages across orders; the derived table avoids double-counting.

**Alt1:**
```sql
-- fast ratio method (slightly different meaning: weighted by nothing)
SELECT SUM(oi.quantity) * 1.0 / COUNT(DISTINCT o.order_id) AS avg_items_per_order
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'completed';
```

## Q7: What is the average order value (AOV)?

**Schema:** orders (order_id, customer_id, order_date, status, total_amount)

**Query:**
```sql
SELECT AVG(total_amount) AS average_order_value,
       SUM(total_amount) AS revenue,
       COUNT(*) AS orders
FROM orders
WHERE status = 'completed';
```
**Explanation:** Simple mean of completed order totals; AOV = revenue divided by order count.

## Q8: How many orders are in each status?

**Schema:** orders (order_id, status)

**Query:**
```sql
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;
```
**Explanation:** Standard GROUP BY over the status dimension to snapshot the order pipeline.

**Alt1:**
```sql
-- MySQL pivot across statuses
SELECT SUM(status = 'pending')      AS pending,
       SUM(status = 'paid')         AS paid,
       SUM(status = 'shipped')      AS shipped,
       SUM(status = 'completed')    AS completed,
       SUM(status = 'cancelled')    AS cancelled
FROM orders;
```

## Q9: Customers who registered but never completed an order.

**Schema:** customers (customer_id, name, signup_date), orders (customer_id, status)

**Query:**
```sql
SELECT c.customer_id, c.name, c.signup_date
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
WHERE o.order_id IS NULL;
```
**Explanation:** LEFT JOIN plus NULL check is a classic anti-join; the customer survives because no completed order matches.

**Alt1:**
```sql
-- Oracle-style NOT EXISTS
SELECT customer_id, name, signup_date
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.customer_id AND o.status = 'completed'
);
```

## Q10: First order date per customer (acquisition cohort base).

**Schema:** orders (order_id, customer_id, order_date, status), customers (customer_id, name)

**Query:**
```sql
SELECT customer_id, MIN(order_date) AS first_order_date
FROM orders
WHERE status = 'completed'
GROUP BY customer_id;
```
**Explanation:** The minimum date per customer defines when they were acquired; the building block for cohort analysis.

**Alt1:**
```sql
-- SQL Server, gives the order id too
SELECT customer_id, order_id, order_date AS first_order_date
FROM (
  SELECT customer_id, order_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS rn
  FROM orders
  WHERE status = 'completed'
) t
WHERE rn = 1;
```

## Q11: Revenue by product category.

**Schema:** categories (category_id, name), products (product_id, category_id), order_items (order_id, product_id, quantity, unit_price), orders (order_id, status)

**Query:**
```sql
SELECT c.name AS category, SUM(oi.quantity * oi.unit_price) AS revenue
FROM categories c
JOIN products p ON p.category_id = c.category_id
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY c.name
ORDER BY revenue DESC;
```
**Explanation:** Chains categories -> products -> line items -> orders to roll revenue up the hierarchy.

## Q12: Category revenue growth % — current month vs previous month.

**Schema:** categories (category_id, name), products (category_id), order_items, orders (order_date, status, total_amount)

**Query:**
```sql
-- MySQL window-free version
WITH current_m AS (
  SELECT p.category_id, SUM(oi.quantity * oi.unit_price) AS revenue
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.order_id
  JOIN products p ON p.product_id = oi.product_id
  WHERE o.status = 'completed'
    AND o.order_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
    AND o.order_date <  DATE_FORMAT(DATE_ADD(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
  GROUP BY p.category_id
),
previous_m AS (
  SELECT p.category_id, SUM(oi.quantity * oi.unit_price) AS revenue
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.order_id
  JOIN products p ON p.product_id = oi.product_id
  WHERE o.status = 'completed'
    AND o.order_date >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
    AND o.order_date <  DATE_FORMAT(CURDATE(), '%Y-%m-01')
  GROUP BY p.category_id
)
SELECT c.name, cur.revenue AS current_rev, prev.revenue AS prev_rev,
       ROUND((cur.revenue - prev.revenue) / NULLIF(prev.revenue, 0) * 100, 1) AS growth_pct
FROM current_m cur
JOIN previous_m prev ON prev.category_id = cur.category_id
JOIN categories c ON c.category_id = cur.category_id
ORDER BY growth_pct DESC;
```
**Explanation:** Computes each month's revenue in a CTE then grows by percentage change; NULLIF guards divide-by-zero.

## Q13: How many customers are repeat buyers (2+ completed orders)?

**Schema:** orders (order_id, customer_id, status)

**Query:**
```sql
SELECT COUNT(*) AS repeat_buyer_count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 1) AS repeat_rate_pct
FROM (
  SELECT customer_id
  FROM orders
  WHERE status = 'completed'
  GROUP BY customer_id
  HAVING COUNT(*) >= 2
) t;
```
**Explanation:** Inner query keeps only customers with two or more orders; outer counts them and expresses as a share of all customers.

## Q14: Average repeat-order interval — days between a customer's first and second order.

**Schema:** orders (order_id, customer_id, order_date, status)

**Query:**
```sql
WITH ranked AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders
  WHERE status = 'completed'
)
SELECT AVG(TIMESTAMPDIFF(DAY, o1.order_date, o2.order_date)) AS avg_repeat_interval_days
FROM ranked o1
JOIN ranked o2
  ON o2.customer_id = o1.customer_id
 AND o2.rn = o1.rn + 1;
```
**Explanation:** Self-join on consecutive row numbers; row 2 minus row 1 is the first repeat gap, averaged across customers.

**Alt1:**
```sql
-- PostgreSQL date subtraction returns integer days
WITH ranked AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders WHERE status = 'completed'
)
SELECT AVG(o2.order_date - o1.order_date) AS avg_repeat_interval_days
FROM ranked o1
JOIN ranked o2 ON o2.customer_id = o1.customer_id AND o2.rn = o1.rn + 1;
```

## Q15: Best customers by lifetime value (LTV) — top 10.

**Schema:** customers (customer_id, name), orders (order_id, customer_id, status), order_items (order_id, product_id, quantity, unit_price)

**Query:**
```sql
SELECT c.customer_id, c.name,
       SUM(oi.quantity * oi.unit_price) AS ltv,
       COUNT(DISTINCT o.order_id) AS order_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.name
ORDER BY ltv DESC
LIMIT 10;
```
**Explanation:** LTV is the sum of extended prices across all a customer's completed orders; sorted descending, capped at ten.

## Q16: New vs returning customers per month.

**Schema:** customers (customer_id), orders (order_id, customer_id, order_date, status)

**Query:**
```sql
-- MySQL
WITH firsts AS (
  SELECT customer_id, DATE_FORMAT(MIN(order_date), '%Y-%m') AS first_month
  FROM orders WHERE status = 'completed'
  GROUP BY customer_id
)
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS month,
       COUNT(DISTINCT CASE WHEN f.first_month = DATE_FORMAT(o.order_date, '%Y-%m')
            THEN o.customer_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN f.first_month != DATE_FORMAT(o.order_date, '%Y-%m')
            THEN o.customer_id END) AS returning_customers
FROM orders o
JOIN firsts f ON f.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;
```
**Explanation:** Each customer's acquisition month is precomputed; a purchase in the same month is "new", otherwise "returning".

## Q17: Orders anomaly — orders that have no item lines at all.

**Schema:** orders (order_id, order_date, total_amount, status), order_items (order_id, product_id, quantity)

**Query:**
```sql
SELECT o.order_id, o.order_date, o.total_amount, o.status
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.order_id
WHERE oi.product_id IS NULL;
```
**Explanation:** Any order surviving the LEFT JOIN without a matching line is an orphan row — a data integrity anomaly worth investigating.

**Alt1:**
```sql
-- anomaly variant: order total does not match sum of its lines
SELECT o.order_id, o.total_amount, l.line_total,
       o.total_amount - l.line_total AS discrepancy
FROM orders o
JOIN (
  SELECT order_id, SUM(quantity * unit_price) AS line_total
  FROM order_items GROUP BY order_id
) l ON l.order_id = o.order_id
WHERE ABS(o.total_amount - l.line_total) > 0.01;
```

## Q18: Products that have never been sold.

**Schema:** products (product_id, name, price), order_items (order_id, product_id)

**Query:**
```sql
SELECT p.product_id, p.name, p.price
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
WHERE oi.order_id IS NULL;
```
**Explanation:** Anti-join over order_items reveals SKUs with zero purchase history — candidates for markdown or delisting.

**Alt1:**
```sql
SELECT product_id, name, price
FROM products
WHERE product_id NOT IN (SELECT DISTINCT product_id FROM order_items WHERE product_id IS NOT NULL);
```

## Q19: Abandoned carts and the cart abandonment rate.

**Schema:** carts (cart_id, customer_id, created_date, order_id)

**Query:**
```sql
SELECT COUNT(*)                                              AS total_carts,
       SUM(CASE WHEN order_id IS NOT NULL THEN 1 ELSE 0 END) AS converted,
       SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END)     AS abandoned,
       ROUND(SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END)
             / COUNT(*) * 100, 1)                            AS abandonment_rate_pct
FROM carts;
```
**Explanation:** A cart that never became an order is abandoned; the rate is abandoned over all carts.

**Alt1:**
```sql
-- per-day abandonment rate
SELECT DATE(created_date) AS day,
       COUNT(*) AS carts,
       ROUND(SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS abandoned_pct
FROM carts
GROUP BY DATE(created_date)
ORDER BY day;
```

## Q20: Cart-to-order conversion per day.

**Schema:** carts (cart_id, customer_id, created_date, order_id), orders (order_id, status)

**Query:**
```sql
SELECT DATE(c.created_date) AS day,
       COUNT(c.cart_id)     AS carts,
       COUNT(o.order_id)    AS orders,
       ROUND(COUNT(o.order_id) / COUNT(c.cart_id) * 100, 1) AS conversion_pct
FROM carts c
LEFT JOIN orders o ON o.order_id = c.order_id AND o.status IN ('paid', 'shipped', 'completed')
GROUP BY DATE(c.created_date)
ORDER BY day;
```
**Explanation:** Join carts to their resulting orders, count both, and divide; the LEFT JOIN keeps unconverted carts visible.

## Q21: Cohort table — how many customers were acquired (first purchase) in each month.

**Schema:** orders (order_id, customer_id, order_date, status)

**Query:**
```sql
SELECT DATE_FORMAT(MIN(order_date), '%Y-%m') AS cohort_month,
       COUNT(DISTINCT customer_id)            AS customers_acquired
FROM orders
WHERE status = 'completed'
GROUP BY DATE_FORMAT(MIN(order_date), '%Y-%m')
ORDER BY cohort_month;
```
**Explanation:** Grouping by the monthly minimum order date distributes customers into acquisition cohorts.

## Q22: Average number of reviews per product.

**Schema:** reviews (review_id, product_id, rating, review_date), products (product_id)

**Query:**
```sql
SELECT ROUND(AVG(review_count), 1) AS avg_reviews_per_product
FROM (
  SELECT product_id, COUNT(*) AS review_count
  FROM reviews
  GROUP BY product_id
) t;
```
**Explanation:** Counts reviews per product first, then takes the mean across all reviewed products.

**Alt1:**
```sql
-- includes products with zero reviews via LEFT JOIN
SELECT ROUND(AVG(r.cnt), 1) AS avg_reviews_per_product
FROM (
  SELECT p.product_id, COUNT(r.review_id) AS cnt
  FROM products p
  LEFT JOIN reviews r ON r.product_id = p.product_id
  GROUP BY p.product_id
) r;
```

## Q23: Average days between a customer's first and second order (only repeat purchasers).

**Schema:** orders (order_id, customer_id, order_date, status)

**Query:**
```sql
WITH ranked AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders
  WHERE status = 'completed'
)
SELECT AVG(TIMESTAMPDIFF(DAY, o1.order_date, o2.order_date)) AS avg_days_to_second_order,
       COUNT(DISTINCT o1.customer_id) AS repeat_customers
FROM ranked o1
JOIN ranked o2 ON o2.customer_id = o1.customer_id
              AND o2.rn = o1.rn + 1
WHERE o1.rn = 1;
```
**Explanation:** Joins the first purchase row (rn=1) to the second purchase row (rn=2) only; averaged only over those who came back.

## Q24: Distribution of items per order.

**Schema:** order_items (order_id, product_id, quantity)

**Query:**
```sql
SELECT item_qty AS items_per_order, COUNT(*) AS order_frequency
FROM (
  SELECT order_id, SUM(quantity) AS item_qty
  FROM order_items
  GROUP BY order_id
) t
GROUP BY item_qty
ORDER BY item_qty;
```
**Explanation:** Histogram of basket sizes — each bucket is number of items, value is how many orders hit it.

## Q25: Customers with exactly one completed order, and what they spent.

**Schema:** customers (customer_id, name), orders (order_id, customer_id, total_amount, status)

**Query:**
```sql
SELECT o.customer_id, c.name, SUM(o.total_amount) AS one_time_value
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY o.customer_id, c.name
HAVING COUNT(o.order_id) = 1;
```
**Explanation:** HAVING filters groups to those with a single order, isolating the one-and-done customer segment.


## Q26: Cross-sell — which product pairs are bought together most often?

**Schema:** products (product_id, name), order_items (order_id, product_id, quantity)

**Query:**
```sql
SELECT a.product_id                                        AS product_a,
       b.product_id                                        AS product_b,
       COUNT(DISTINCT a.order_id)                          AS times_together
FROM order_items a
JOIN order_items b ON b.order_id = a.order_id
                  AND b.product_id > a.product_id
GROUP BY a.product_id, b.product_id
ORDER BY times_together DESC
LIMIT 10;
```
**Explanation:** Self-join on the same order; the `>` condition keeps each unordered pair once, and DISTINCT handles duplicate rows.

**Alt1:**
```sql
-- with product names and only strongly-linked pairs
SELECT pa.name AS product_a, pb.name AS product_b, COUNT(DISTINCT a.order_id) AS times_together
FROM order_items a
JOIN order_items b ON b.order_id = a.order_id AND b.product_id > a.product_id
JOIN products pa ON pa.product_id = a.product_id
JOIN products pb ON pb.product_id = b.product_id
GROUP BY pa.name, pb.name
HAVING COUNT(DISTINCT a.order_id) >= 50
ORDER BY times_together DESC;
```

## Q27: Cross-sell confidence — probability that product B is in the same order as A.

**Schema:** products (product_id, name), order_items (order_id, product_id), orders (order_id, status)

**Query:**
```sql
WITH basket AS (
  SELECT DISTINCT order_id, product_id
  FROM order_items
),
a_orders AS (
  SELECT product_id, COUNT(DISTINCT order_id) AS orders_with_a
  FROM basket GROUP BY product_id
)
SELECT pa.name AS product_a, pb.name AS product_b,
       COUNT(DISTINCT ab.order_id)                            AS co_orders,
       ROUND(COUNT(DISTINCT ab.order_id) * 100.0
             / a.orders_with_a, 1)                            AS confidence_pct
FROM basket ab
JOIN basket b  ON b.order_id = ab.order_id AND b.product_id <> ab.product_id
JOIN a_orders a ON a.product_id = ab.product_id
JOIN products pa ON pa.product_id = ab.product_id
JOIN products pb ON pb.product_id = b.product_id
GROUP BY pa.name, pb.name, a.orders_with_a
ORDER BY confidence_pct DESC
LIMIT 10;
```
**Explanation:** Confidence = times pair appears together divided by total orders containing the anchor product — the classic association rule.

## Q28: Stock-out risk — products whose on-hand inventory can't cover the last 30 days of sales velocity.

**Schema:** inventory (product_id, warehouse_id, quantity_on_hand), order_items (product_id, quantity), orders (order_id, status, order_date)

**Query:**
```sql
-- MySQL
WITH sales30 AS (
  SELECT oi.product_id, SUM(oi.quantity) AS qty_30d
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  WHERE o.status = 'completed'
    AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
  GROUP BY oi.product_id
)
SELECT p.product_id, p.name,
       i.quantity_on_hand,
       COALESCE(s.qty_30d, 0) AS qty_sold_30d,
       ROUND(i.quantity_on_hand / NULLIF(s.qty_30d, 0) * 30, 1) AS days_of_stock_left,
       CASE WHEN i.quantity_on_hand < COALESCE(s.qty_30d, 0) * 2 THEN 'STOCK-OUT RISK'
            ELSE 'OK' END AS flag
FROM products p
JOIN inventory i ON i.product_id = p.product_id
LEFT JOIN sales30 s ON s.product_id = p.product_id;
```
**Explanation:** Compares stock on hand against 30-day demand run-rate; if stock is under roughly two weeks of demand it is flagged.

## Q29: Restock recommendations — SKUs at or below reorder point with their daily demand.

**Schema:** inventory (product_id, quantity_on_hand, reorder_point), products (product_id, name), order_items, orders

**Query:**
```sql
WITH demand AS (
  SELECT oi.product_id, SUM(oi.quantity) / 30.0 AS daily_demand
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  WHERE o.status = 'completed'
    AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
  GROUP BY oi.product_id
)
SELECT p.product_id, p.name,
       i.quantity_on_hand, i.reorder_point,
       ROUND(COALESCE(d.daily_demand, 0), 2)   AS daily_demand,
       ROUND((i.reorder_point - i.quantity_on_hand) / NULLIF(d.daily_demand, 0), 0) AS days_to_restock
FROM inventory i
JOIN products p ON p.product_id = i.product_id
LEFT JOIN demand d ON d.product_id = p.product_id
WHERE i.quantity_on_hand <= i.reorder_point
ORDER BY daily_demand DESC;
```
**Explanation:** Flags anything at or under reorder point and suggests purchase urgency by dividing the shortfall by demand rate.

## Q30: Inventory aging — slow-moving SKUs with stock older than 90 days.

**Schema:** inventory (product_id, quantity_on_hand, restock_date), products (name), order_items, orders

**Query:**
```sql
-- MySQL
SELECT p.product_id, p.name,
       i.quantity_on_hand, DATE(i.restock_date) AS last_restocked,
       COALESCE(s.qty, 0) AS units_sold_90d,
       DATEDIFF(CURDATE(), i.restock_date) AS days_since_restock
FROM products p
JOIN inventory i ON i.product_id = p.product_id
LEFT JOIN (
  SELECT oi.product_id, SUM(oi.quantity) AS qty
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
  GROUP BY oi.product_id
) s ON s.product_id = p.product_id
WHERE i.quantity_on_hand > 0
  AND COALESCE(s.qty, 0) = 0
ORDER BY i.quantity_on_hand DESC;
```
**Explanation:** Identifies inventory aging: units still on hand that haven't moved in 90 days are cash tied up in stock.

## Q31: Stock turnover by category — weeks of supply on hand.

**Schema:** categories (category_id, name), products (category_id), inventory (product_id, quantity_on_hand), order_items, orders

**Query:**
```sql
WITH sales7 AS (
  SELECT p.category_id, SUM(oi.quantity) AS units_7d
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  JOIN products p ON p.product_id = oi.product_id
  WHERE o.status = 'completed'
    AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
  GROUP BY p.category_id
),
stock AS (
  SELECT p.category_id, SUM(i.quantity_on_hand) AS on_hand
  FROM inventory i
  JOIN products p ON p.product_id = i.product_id
  GROUP BY p.category_id
)
SELECT c.name AS category,
       COALESCE(st.on_hand, 0)        AS units_on_hand,
       COALESCE(s.units_7d, 0)        AS units_sold_7d,
       ROUND(COALESCE(st.on_hand, 0) / NULLIF(s.units_7d, 0), 1) AS weeks_of_supply
FROM categories c
LEFT JOIN stock st ON st.category_id = c.category_id
LEFT JOIN sales7 s ON s.category_id = c.category_id
ORDER BY weeks_of_supply;
```
**Explanation:** Weeks of supply equals inventory at hand divided by weekly demand; low numbers mean fast sell-through and restock pressure.

## Q32: Replenishment trigger — units below the safety-stock level (demand x lead time + buffer).

**Schema:** inventory (product_id, warehouse_id, quantity_on_hand), warehouses (warehouse_id, lead_time_days), products (name), order_items, orders

**Query:**
```sql
WITH demand AS (
  SELECT product_id, SUM(quantity) / 30.0 AS daily_demand,
         SUM(quantity) AS qty_30d
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  WHERE o.status = 'completed'
    AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
  GROUP BY product_id
)
SELECT p.product_id, p.name,
       i.quantity_on_hand,
       ROUND(d.daily_demand, 2)                                  AS daily_demand,
       w.lead_time_days,
       ROUND(d.daily_demand * (w.lead_time_days + 3), 0)         AS safety_stock_level,
       ROUND(d.daily_demand * (w.lead_time_days + 3)
             - i.quantity_on_hand, 0)                            AS qty_to_order
FROM inventory i
JOIN warehouses w ON w.warehouse_id = i.warehouse_id
JOIN products p  ON p.product_id = i.product_id
JOIN demand d    ON d.product_id = p.product_id
WHERE i.quantity_on_hand < d.daily_demand * (w.lead_time_days + 3)
ORDER BY qty_to_order DESC;
```
**Explanation:** Safety stock covers forecast demand over lead time plus a 3-day buffer; anything below it generates a replenishment order.

**Alt1:**
```sql
-- PostgreSQL version (same logic, INTERVAL math style)
SELECT p.product_id, i.quantity_on_hand,
       ROUND(d.daily_demand * (w.lead_time_days + 3), 0) AS safety_stock_level
FROM inventory i
JOIN warehouses w ON w.warehouse_id = i.warehouse_id
JOIN products p ON p.product_id = i.product_id
JOIN (
  SELECT oi.product_id, SUM(oi.quantity) / 30.0 AS daily_demand
  FROM order_items oi JOIN orders o ON o.order_id = oi.order_id
  WHERE o.status = 'completed' AND o.order_date >= now() - interval '30 days'
  GROUP BY oi.product_id
) d ON d.product_id = p.product_id
WHERE i.quantity_on_hand < d.daily_demand * (w.lead_time_days + 3);
```

## Q33: Warehouse order fulfillment lag — average days from order to ship.

**Schema:** shipments (shipment_id, order_id, warehouse_id, ship_date), orders (order_id, order_date)

**Query:**
```sql
-- MySQL
SELECT s.warehouse_id,
       COUNT(*)                                    AS shipments,
       ROUND(AVG(DATEDIFF(s.ship_date, o.order_date)), 1) AS avg_fulfillment_days
FROM shipments s
JOIN orders o ON o.order_id = s.order_id
GROUP BY s.warehouse_id
ORDER BY avg_fulfillment_days DESC;
```
**Explanation:** DATEDIFF between order placement and shipment per warehouse surfaces the slowest fulfillment hubs.

**Alt1:**
```sql
-- SQL Server
SELECT s.warehouse_id,
       AVG(DATEDIFF(day, o.order_date, s.ship_date)) AS avg_fulfillment_days
FROM shipments s
JOIN orders o ON o.order_id = s.order_id
GROUP BY s.warehouse_id;
```

## Q34: Fulfillment lag by product category.

**Schema:** shipments (order_id, ship_date), orders (order_id, order_date), order_items, products (category_id), categories (name)

**Query:**
```sql
SELECT c.name AS category,
       ROUND(AVG(DATEDIFF(s.ship_date, o.order_date)), 1) AS avg_fulfillment_days,
       COUNT(*) AS lines
FROM shipments s
JOIN orders o ON o.order_id = s.order_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
JOIN categories c ON c.category_id = p.category_id
GROUP BY c.name
ORDER BY avg_fulfillment_days DESC;
```
**Explanation:** Same lag metric aggregated up to category to find which merchandise types pack and ship slowest.

## Q35: Shipping cost vs margin per product — which SKUs the shipping eats into.

**Schema:** products (product_id, name, price, cost), order_items (unit_price), orders (total_amount, status), shipments (order_id, shipping_cost)

**Query:**
```sql
SELECT p.product_id, p.name,
       ROUND(p.price - p.cost, 2)           AS unit_margin,
       ROUND(AVG(s.shipping_cost), 2)       AS avg_shipping_cost,
       ROUND((p.price - p.cost) - AVG(s.shipping_cost), 2) AS net_after_shipping
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
JOIN shipments s ON s.order_id = o.order_id
GROUP BY p.product_id, p.name, p.price, p.cost
ORDER BY net_after_shipping ASC;
```
**Explanation:** Avg shipping per product is compared against unit margin; negative results signal SKUs that lose money to logistics.

## Q36: Orders where shipping cost exceeds product profit (net-negative orders).

**Schema:** orders (order_id, total_amount, status), order_items (order_id, product_id, quantity, unit_price), products (cost), shipments (shipping_cost)

**Query:**
```sql
SELECT o.order_id,
       SUM(oi.quantity * oi.unit_price - p.cost * oi.quantity) AS product_profit,
       s.shipping_cost,
       SUM(oi.quantity * oi.unit_price - p.cost * oi.quantity) - s.shipping_cost AS net
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
JOIN shipments s ON s.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY o.order_id, s.shipping_cost
HAVING SUM(oi.quantity * oi.unit_price - p.cost * oi.quantity) - s.shipping_cost < 0;
```
**Explanation:** Reconstructs gross profit per line, subtracts freight, and keeps only orders where the result is negative.

## Q37: Average review rating per product, best and worst.

**Schema:** products (product_id, name), reviews (review_id, product_id, rating)

**Query:**
```sql
SELECT p.product_id, p.name,
       ROUND(AVG(r.rating), 2) AS avg_rating,
       COUNT(r.review_id)      AS review_count
FROM products p
LEFT JOIN reviews r ON r.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY avg_rating ASC, review_count DESC;
```
**Explanation:** LEFT JOIN keeps unrated products visible; ordering ascending surfaces the worst-rated SKUs first.

## Q38: Products with the exact same star-rating distribution.

**Schema:** reviews (review_id, product_id, rating)

**Query:**
```sql
WITH dist AS (
  SELECT product_id, rating, COUNT(*) AS cnt
  FROM reviews
  GROUP BY product_id, rating
)
SELECT d1.product_id AS product_a,
       d2.product_id AS product_b,
       COUNT(*)       AS matching_rating_levels
FROM dist d1
JOIN dist d2
  ON d2.rating = d1.rating
 AND d2.cnt = d1.cnt
 AND d2.product_id > d1.product_id
GROUP BY d1.product_id, d2.product_id
HAVING COUNT(*) = 5;
```
**Explanation:** Joins the per-rating counts; matching count and count of levels across all 5 stars proves identical distributions.

## Q39: Reviews grouped by star rating.

**Schema:** reviews (review_id, product_id, rating, review_date)

**Query:**
```sql
SELECT rating, COUNT(*) AS reviews
FROM reviews
GROUP BY rating
ORDER BY rating DESC;
```
**Explanation:** Straight histogram over the rating dimension to see the overall review shape.

**Alt1:**
```sql
-- MySQL one-row pivot
SELECT SUM(rating = 5) AS five_star,
       SUM(rating = 4) AS four_star,
       SUM(rating = 3) AS three_star,
       SUM(rating = 2) AS two_star,
       SUM(rating = 1) AS one_star
FROM reviews;
```

## Q40: Sales vs return rate per product.

**Schema:** products (product_id, name), order_items (product_id, quantity), orders (status), returns (return_id, product_id)

**Query:**
```sql
WITH sold AS (
  SELECT oi.product_id, SUM(oi.quantity) AS units_sold
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  GROUP BY oi.product_id
),
ret AS (
  SELECT product_id, COUNT(*) AS return_count
  FROM returns
  GROUP BY product_id
)
SELECT p.product_id, p.name,
       s.units_sold,
       COALESCE(r.return_count, 0) AS return_count,
       ROUND(COALESCE(r.return_count, 0) * 100.0 / NULLIF(s.units_sold, 0), 1) AS return_rate_pct
FROM products p
JOIN sold s ON s.product_id = p.product_id
LEFT JOIN ret r ON r.product_id = p.product_id
ORDER BY return_rate_pct DESC;
```
**Explanation:** Return rate = returned units divided by sold units per product; the LEFT JOIN keeps low/no-return rows at the bottom.

## Q41: High-return products — alert on SKUs above average return rate and with real volume.

**Schema:** products (product_id, name), order_items, orders (status), returns (product_id)

**Query:**
```sql
WITH stats AS (
  SELECT p.product_id, p.name,
         COUNT(DISTINCT r.return_id)                     AS returns,
         COUNT(DISTINCT oi.order_id)                     AS orders,
         COUNT(DISTINCT r.return_id) * 100.0
             / NULLIF(COUNT(DISTINCT oi.order_id), 0)    AS return_rate_pct
  FROM products p
  JOIN order_items oi ON oi.product_id = p.product_id
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  LEFT JOIN returns r ON r.product_id = p.product_id
  GROUP BY p.product_id, p.name
)
SELECT product_id, name, returns, orders, ROUND(return_rate_pct, 1) AS return_rate_pct
FROM stats
WHERE orders >= 50
  AND return_rate_pct > (SELECT AVG(return_rate_pct) FROM stats)
ORDER BY return_rate_pct DESC;
```
**Explanation:** Filters to SKUs with meaningful volume whose return rate beats the catalog average — review/packaging suspects.

## Q42: Promo / discount share of total revenue.

**Schema:** orders (order_id, order_date, total_amount, discount_amount, status)

**Query:**
```sql
SELECT DATE_FORMAT(order_date, '%Y-%m')                              AS month,
       SUM(total_amount)                                            AS total_revenue,
       SUM(CASE WHEN discount_amount > 0 THEN discount_amount ELSE 0 END) AS discount_given,
       ROUND(SUM(CASE WHEN discount_amount > 0 THEN total_amount ELSE 0 END)
             / NULLIF(SUM(total_amount), 0) * 100, 1)               AS promo_revenue_share_pct
FROM orders
WHERE status = 'completed'
GROUP BY DATE_FORMAT(order_date, '%Y-%m');
```
**Explanation:** Measures what fraction of dollar sales carried a discount and how much margin was given away.

## Q43: Discount depth vs volume — does deeper discounting lift units?

**Schema:** orders (order_id, discount_amount, status), order_items (order_id, product_id, quantity)

**Query:**
```sql
SELECT CASE WHEN o.discount_amount = 0 THEN '0'
            WHEN o.discount_amount < 20 THEN '1-19'
            WHEN o.discount_amount < 50 THEN '20-49'
            ELSE '50+' END                      AS discount_band,
       COUNT(DISTINCT o.order_id)               AS orders,
       SUM(oi.quantity)                         AS units_sold
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY CASE WHEN o.discount_amount = 0 THEN '0'
              WHEN o.discount_amount < 20 THEN '1-19'
              WHEN o.discount_amount < 50 THEN '20-49'
              ELSE '50+' END
ORDER BY MIN(o.discount_amount);
```
**Explanation:** Buckets orders by absolute discount, then compares order and unit volume per band — a crude promo-effectiveness test.

## Q44: Price elasticity proxy — units sold against price change per product between two periods.

**Schema:** products (product_id, name), order_items (order_id, product_id, quantity, unit_price), orders (order_date, status)

**Query:**
```sql
SELECT p.product_id, p.name,
       ROUND(AVG(CASE WHEN o.order_date < '2024-07-01' THEN oi.unit_price END), 2) AS price_before,
       ROUND(AVG(CASE WHEN o.order_date >= '2024-07-01' THEN oi.unit_price END), 2) AS price_after,
       SUM(CASE WHEN o.order_date < '2024-07-01' THEN oi.quantity END) AS units_before,
       SUM(CASE WHEN o.order_date >= '2024-07-01' THEN oi.quantity END) AS units_after
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name
HAVING SUM(CASE WHEN o.order_date < '2024-07-01' THEN oi.quantity END) > 0
   AND SUM(CASE WHEN o.order_date >= '2024-07-01' THEN oi.quantity END) > 0;
```
**Explanation:** Pairs realized price and unit volume pre/post a date so the price-change/volume-change relationship can be inspected.

**Alt1:**
```sql
-- Oracle version (no type conversion needed for dates)
SELECT p.product_id, p.name,
       AVG(CASE WHEN o.order_date < DATE '2024-07-01' THEN oi.unit_price END) AS price_before,
       SUM(CASE WHEN o.order_date >= DATE '2024-07-01' THEN oi.quantity END)  AS units_after
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name;
```

## Q45: Day-of-week sales pattern (revenue by weekday).

**Schema:** orders (order_id, order_date, total_amount, status)

**Query:**
```sql
-- MySQL
SELECT DAYOFWEEK(order_date) AS dow_index,
       DAYNAME(order_date)   AS day_name,
       COUNT(*)              AS orders,
       SUM(total_amount)     AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY DAYOFWEEK(order_date), DAYNAME(order_date)
ORDER BY dow_index;
```
**Explanation:** Aggregates revenue per calendar weekday to expose the weekly purchase rhythm for staffing and promotions.

**Alt1:**
```sql
-- PostgreSQL (isodow: Monday = 1 through Sunday = 7)
SELECT extract(isodow FROM order_date) AS dow_index,
       SUM(total_amount)               AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY extract(isodow FROM order_date)
ORDER BY dow_index;
```

## Q46: Weekend vs weekday revenue split.

**Schema:** orders (order_id, order_date, total_amount, status)

**Query:**
```sql
SELECT CASE WHEN DAYOFWEEK(order_date) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END AS period,
       COUNT(*)          AS orders,
       SUM(total_amount) AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY CASE WHEN DAYOFWEEK(order_date) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END;
```
**Explanation:** Buckets dates into two classes and compares order and revenue totals between the against the work week.

## Q47: Seasonal peaks — holiday lift measured as each month vs that month's historical average.

**Schema:** orders (order_id, order_date, total_amount, status)

**Query:**
```sql
SELECT DATE_FORMAT(order_date, '%m') AS month,
       DATE_FORMAT(order_date, '%Y') AS year,
       SUM(total_amount)             AS revenue,
       ROUND(AVG(SUM(total_amount)) OVER (PARTITION BY DATE_FORMAT(order_date, '%m')), 1) AS monthly_avg,
       ROUND(SUM(total_amount) / AVG(SUM(total_amount))
                                 OVER (PARTITION BY DATE_FORMAT(order_date, '%m')), 2)  AS holiday_lift_index
FROM orders
WHERE status = 'completed'
GROUP BY DATE_FORMAT(order_date, '%m'), DATE_FORMAT(order_date, '%Y')
ORDER BY year, month;
```
**Explanation:** Each year-month is divided by the same calendar month's multi-year average; an index well above 1 signals the peak.

**Alt1:**
```sql
-- without window function; Christmas-month lift only
SELECT DATE_FORMAT(order_date, '%Y') AS year,
       SUM(CASE WHEN DATE_FORMAT(order_date, '%m') = '12' THEN total_amount END) AS dec_revenue,
       SUM(total_amount) AS year_revenue,
       ROUND(SUM(CASE WHEN DATE_FORMAT(order_date, '%m') = '12' THEN total_amount END)
             / NULLIF(SUM(total_amount), 0) * 100, 1) AS dec_share_pct
FROM orders
WHERE status = 'completed'
GROUP BY DATE_FORMAT(order_date, '%Y');
```

## Q48: Month-over-month revenue change with LAG.

**Schema:** orders (order_id, order_date, total_amount, status)

**Query:**
```sql
WITH monthly AS (
  SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
         SUM(total_amount) AS revenue
  FROM orders
  WHERE status = 'completed'
  GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month)                         AS prev_revenue,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month))
             / LAG(revenue) OVER (ORDER BY month) * 100, 1)       AS mom_change_pct
FROM monthly
ORDER BY month;
```
**Explanation:** LAG pulls the prior month's revenue into the same row so the growth percent is computed row-wise.

**Alt1:**
```sql
-- processed further: keep only months with latest comparable revenue
WITH monthly AS (
  SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(total_amount) AS revenue
  FROM orders WHERE status = 'completed' GROUP BY month
),
mo AS (
  SELECT month, revenue,
         LAG(revenue) OVER (ORDER BY month) AS prev_revenue
  FROM monthly
)
SELECT month, revenue, prev_revenue,
       ROUND((revenue - prev_revenue) * 100.0 / prev_revenue, 1) AS mom_change_pct
FROM mo WHERE prev_revenue IS NOT NULL;
```

## Q49: Category month-over-month revenue change (per category, same formula).

**Schema:** categories (category_id, name), products (category_id), order_items, orders (order_date, status)

**Query:**
```sql
WITH cat_month AS (
  SELECT c.category_id, c.name AS category,
         DATE_FORMAT(o.order_date, '%Y-%m') AS month,
         SUM(oi.quantity * oi.unit_price)   AS revenue
  FROM categories c
  JOIN products p ON p.category_id = c.category_id
  JOIN order_items oi ON oi.product_id = p.product_id
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  GROUP BY c.category_id, c.name, DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT category, month, revenue,
       LAG(revenue) OVER (PARTITION BY category_id ORDER BY month) AS prev_revenue,
       ROUND((revenue - LAG(revenue) OVER (PARTITION BY category_id ORDER BY month))
             * 100.0 / LAG(revenue) OVER (PARTITION BY category_id ORDER BY month), 1) AS mom_change_pct
FROM cat_month
ORDER BY category, month;
```
**Explanation:** Same trend formula as the overall business but PARTITION BY category so each category computes its own chain.

## Q50: Seller (marketplace vendor) performance — GMV, orders, SKUs and rating.

**Schema:** vendors (vendor_id, vendor_name), products (vendor_id, product_id), order_items, orders (status), reviews (rating)

**Query:**
```sql
SELECT vt.vendor_id, vt.vendor_name,
       COUNT(DISTINCT o.order_id)          AS orders,
       COUNT(DISTINCT oi.product_id)       AS skus_sold,
       SUM(oi.quantity * oi.unit_price)    AS gmv,
       ROUND(AVG(r.rating), 2)             AS avg_rating
FROM vendors vt
JOIN products p ON p.vendor_id = vt.vendor_id
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
LEFT JOIN reviews r ON r.product_id = p.product_id
GROUP BY vt.vendor_id, vt.vendor_name
ORDER BY gmv DESC;
```
**Explanation:** Marketplace scorecard: volume and quality metrics per vendor so underperformers are visible.


## Q51: Fulfillment scorecard per seller — on-time delivery share.

**Schema:** vendors (vendor_id, vendor_name), products (vendor_id), order_items, shipments (shipment_id, order_id, delivered_date, expected_date)

**Query:**
```sql
SELECT vt.vendor_name,
       COUNT(DISTINCT s.shipment_id)                                        AS shipments,
       SUM(CASE WHEN s.delivered_date <= s.expected_date THEN 1 ELSE 0 END) AS on_time,
       ROUND(SUM(CASE WHEN s.delivered_date <= s.expected_date THEN 1 ELSE 0 END)
             * 100.0 / COUNT(DISTINCT s.shipment_id), 1)                    AS on_time_pct
FROM vendors vt
JOIN products p ON p.vendor_id = vt.vendor_id
JOIN order_items oi ON oi.product_id = p.product_id
JOIN shipments s ON s.order_id = oi.order_id
GROUP BY vt.vendor_name
ORDER BY on_time_pct;
```
**Explanation:** Measures each seller's share of shipments delivered at or before the promise date.

## Q52: Delay in delivery — distribution of days delivered late.

**Schema:** shipments (shipment_id, order_id, delivered_date, expected_date)

**Query:**
```sql
SELECT CASE WHEN delay < 0 THEN 'early'
            WHEN delay = 0 THEN 'on_time'
            WHEN delay <= 2 THEN '1-2 days late'
            WHEN delay <= 5 THEN '3-5 days late'
            WHEN delay <= 10 THEN '6-10 days late'
            ELSE '10+ days late' END   AS delay_band,
       COUNT(*)                        AS shipments
FROM (
  SELECT shipment_id, DATEDIFF(delivered_date, expected_date) AS delay
  FROM shipments
  WHERE delivered_date IS NOT NULL
) t
GROUP BY CASE WHEN delay < 0 THEN 'early'
              WHEN delay = 0 THEN 'on_time'
              WHEN delay <= 2 THEN '1-2 days late'
              WHEN delay <= 5 THEN '3-5 days late'
              WHEN delay <= 10 THEN '6-10 days late'
              ELSE '10+ days late' END
ORDER BY MIN(delay);
```
**Explanation:** Casts raw day deltas into customer-facing bands to see how often service promises are breached.

**Alt1:**
```sql
-- continuous distribution (Oracle-style comment, portable)
SELECT delay_days, COUNT(*) AS shipments
FROM (
  SELECT TRUNC(delivered_date) - TRUNC(expected_date) AS delay_days
  FROM shipments WHERE delivered_date IS NOT NULL
)
GROUP BY delay_days
ORDER BY delay_days;
```

## Q53: Fulfillment SLA violations by region.

**Schema:** shipments (shipment_id, order_id, region, ship_date, delivered_date)

**Query:**
```sql
SELECT s.region,
       COUNT(*)                                        AS shipments,
       SUM(CASE WHEN DATEDIFF(s.delivered_date, s.ship_date) > 5 THEN 1 ELSE 0 END) AS violations,
       ROUND(SUM(CASE WHEN DATEDIFF(s.delivered_date, s.ship_date) > 5 THEN 1 ELSE 0 END)
             * 100.0 / COUNT(*), 1)                    AS violation_pct
FROM shipments s
WHERE s.delivered_date IS NOT NULL
GROUP BY s.region
ORDER BY violation_pct DESC;
```
**Explanation:** A 5-day max transit is assumed; ratios per region spotlight geographies breaking the SLA.

**Alt1:**
```sql
-- SQL Server with 7-day SLA
SELECT region,
       SUM(CASE WHEN DATEDIFF(day, ship_date, delivered_date) > 7 THEN 1 ELSE 0 END) AS violations,
       COUNT(*) AS shipments
FROM shipments
WHERE delivered_date IS NOT NULL
GROUP BY region;
```

## Q54: SLA-violating shipments broken down by product hotspot.

**Schema:** shipments (delivered_date, ship_date, order_id), order_items, products (name)

**Query:**
```sql
SELECT p.name AS product,
       COUNT(*) AS violating_lines
FROM shipments s
JOIN order_items oi ON oi.order_id = s.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE DATEDIFF(s.delivered_date, s.ship_date) > 5
GROUP BY p.name
ORDER BY violating_lines DESC
LIMIT 10;
```
**Explanation:** Crosses late shipments into their line items to identify which products disproportionately travel late.

## Q55: Refund reason breakdown.

**Schema:** returns (return_id, order_id, product_id, reason, refund_amount, return_date)

**Query:**
```sql
SELECT reason,
       COUNT(*)                 AS claims,
       SUM(refund_amount)       AS refunded_amount
FROM returns
GROUP BY reason
ORDER BY claims DESC;
```
**Explanation:** Count and dollar value per return reason shows where quality/courier costs leak.

**Alt1:**
```sql
-- share of total claims per reason
SELECT reason,
       COUNT(*) AS claims,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS share_pct
FROM returns
GROUP BY reason
ORDER BY claims DESC;
```

## Q56: Refund rate by payment method.

**Schema:** orders (order_id, payment_method, status), returns (return_id, order_id)

**Query:**
```sql
SELECT o.payment_method,
       COUNT(DISTINCT o.order_id) AS orders,
       COUNT(DISTINCT r.return_id) AS returns,
       ROUND(COUNT(DISTINCT r.return_id) * 100.0
             / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS refund_rate_pct
FROM orders o
LEFT JOIN returns r ON r.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY o.payment_method;
```
**Explanation:** LEFT JOIN couples every order to its return (if any); per-method rates surface channel risk.

## Q57: Gift card usage — how much revenue used gift cards vs other methods.

**Schema:** orders (order_id, payment_method, total_amount, status)

**Query:**
```sql
SELECT SUM(CASE WHEN payment_method = 'gift_card' THEN total_amount ELSE 0 END)      AS gift_card_revenue,
       SUM(CASE WHEN payment_method != 'gift_card' THEN total_amount ELSE 0 END)     AS other_revenue,
       ROUND(SUM(CASE WHEN payment_method = 'gift_card' THEN total_amount ELSE 0 END)
             / NULLIF(SUM(total_amount), 0) * 100, 1)                                AS gift_card_share_pct
FROM orders
WHERE status = 'completed';
```
**Explanation:** Splits completed revenue between gift-card-funded and other, reporting the share gift cards carry.

## Q58: Gift card usage trend per month.

**Schema:** orders (order_id, order_date, payment_method, total_amount, status)

**Query:**
```sql
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       COUNT(CASE WHEN payment_method = 'gift_card' THEN 1 END) AS gift_card_orders,
       ROUND(SUM(CASE WHEN payment_method = 'gift_card' THEN total_amount ELSE 0 END), 2) AS gift_card_value
FROM orders
WHERE status = 'completed'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```
**Explanation:** Monthly linearization of gift-card order counts and dollar value to watch redemption cycles.

## Q59: Gift wrapping flag — revenue from wrapped orders.

**Schema:** orders (order_id, gift_wrap, total_amount, status), order_items (gift_wrap_fee... )

**Query:**
```sql
SELECT o.gift_wrap,
       COUNT(*)          AS orders,
       SUM(o.total_amount) AS revenue
FROM orders o
WHERE o.status = 'completed'
GROUP BY o.gift_wrap;
```
**Explanation:** Compares wrapped vs unwrapped order volume and revenue to size the gift services opportunity.

**Alt1:**
```sql
-- add optional gift_wrap_fee found on the order line
SELECT ROUND(SUM(oi.gift_wrap_fee), 2) AS gift_wrap_fees_collected,
       SUM(CASE WHEN oi.gift_wrap THEN 1 ELSE 0 END) AS wrapped_lines
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed';
```

## Q60: Basket analysis — is average cart size growing over time?

**Schema:** orders (order_id, order_date, status), order_items (order_id, quantity)

**Query:**
```sql
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS month,
       COUNT(DISTINCT o.order_id)         AS orders,
       ROUND(AVG(b.item_qty * 1.0), 2)    AS avg_items_per_order,
       ROUND(AVG(b.item_qty * 1.0) - FIRST_VALUE(AVG(b.item_qty * 1.0))
             OVER (ORDER BY DATE_FORMAT(o.order_date, '%Y-%m')), 2) AS growth_vs_first_month
FROM orders o
JOIN (
  SELECT order_id, SUM(quantity) AS item_qty
  FROM order_items
  GROUP BY order_id
) b ON b.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;
```
**Explanation:** Tracks basket-size mean per month and a delta against the first month to show the growth trend cleanly.

## Q61: AOV by acquisition cohort — do newer customers spend more per order?

**Schema:** customers (customer_id), orders (order_id, customer_id, order_date, total_amount, status)

**Query:**
```sql
WITH firsts AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM orders WHERE status = 'completed'
  GROUP BY customer_id
)
SELECT DATE_FORMAT(f.first_date, '%Y-%m') AS cohort,
       COUNT(DISTINCT f.customer_id)      AS customers,
       ROUND(AVG(o.total_amount), 2)      AS aov
FROM firsts f
JOIN orders o ON o.customer_id = f.customer_id AND o.status = 'completed'
GROUP BY DATE_FORMAT(f.first_date, '%Y-%m')
ORDER BY cohort;
```
**Explanation:** Cohort = month of first purchase; AOV averaged inside each cohort answers if newer signups transact larger.

**Alt1:**
```sql
-- PostgreSQL version
WITH firsts AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM orders WHERE status = 'completed' GROUP BY customer_id
)
SELECT to_char(f.first_date, 'YYYY-MM') AS cohort,
       COUNT(DISTINCT f.customer_id)    AS customers,
       ROUND(AVG(o.total_amount), 2)    AS aov
FROM firsts f
JOIN orders o ON o.customer_id = f.customer_id AND o.status = 'completed'
GROUP BY to_char(f.first_date, 'YYYY-MM')
ORDER BY cohort;
```

## Q62: Region-wise revenue concentration.

**Schema:** customers (customer_id, region), orders (customer_id, total_amount, status)

**Query:**
```sql
SELECT c.region,
       SUM(o.total_amount) AS revenue,
       ROUND(SUM(o.total_amount) / (
         SELECT SUM(total_amount) FROM orders WHERE status = 'completed'
       ) * 100, 1) AS share_pct
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
GROUP BY c.region
ORDER BY revenue DESC;
```
**Explanation:** Region revenue as a share of the whole catalog, ranked, reveals single-market dependency risk.

## Q63: Revenue concentration — running cumulative share per region (80/20 view).

**Schema:** customers (customer_id, region), orders (total_amount, status)

**Query:**
```sql
WITH region_rev AS (
  SELECT c.region, SUM(o.total_amount) AS revenue
  FROM customers c
  JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
  GROUP BY c.region
)
SELECT region, revenue,
       ROUND(SUM(revenue) OVER (ORDER BY revenue DESC) * 100.0
             / SUM(revenue) OVER (), 1) AS cumulative_share_pct
FROM region_rev
ORDER BY revenue DESC;
```
**Explanation:** Running sum of the revenue window divided by the grand total shows how fast the largest regions saturate the business.

## Q64: Top N products per category with ties preserved (RANK).

**Schema:** categories (category_id, name), products (category_id, product_id, name), order_items, orders (status)

**Query:**
```sql
WITH ranked AS (
  SELECT c.category_id, c.name AS category,
         p.product_id, p.name AS product,
         SUM(oi.quantity * oi.unit_price) AS revenue,
         RANK() OVER (PARTITION BY p.category_id
                      ORDER BY SUM(oi.quantity * oi.unit_price) DESC) AS rk
  FROM categories c
  JOIN products p ON p.category_id = c.category_id
  JOIN order_items oi ON oi.product_id = p.product_id
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  GROUP BY c.category_id, c.name, p.product_id, p.name
)
SELECT category, product, revenue
FROM ranked
WHERE rk <= 3;
```
**Explanation:** RANK keeps ties — if two products share rank 2 both appear, so the top-3 can exceed three rows.

**Alt1:**
```sql
-- ROW_NUMBER guarantees exactly N rows; breaks ties arbitrarily/ deterministically
WITH ranked AS (
  SELECT category, product, revenue,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC, product) AS rn
  FROM ... -- same base as above
)
SELECT * FROM ranked WHERE rn <= 3;
```

## Q65: Top products in each category — SQL Server DENSE_RANK and no ties at the cutting edge.

**Schema:** categories (category_id, name), products (category_id, product_id, name), order_items, orders

**Query:**
```sql
;WITH ranked AS (
  SELECT c.name AS category, p.product_id, p.name AS product,
         SUM(oi.quantity * oi.unit_price) AS revenue,
         DENSE_RANK() OVER (PARTITION BY p.category_id
                            ORDER BY SUM(oi.quantity * oi.unit_price) DESC) AS dr
  FROM categories c
  JOIN products p ON p.category_id = c.category_id
  JOIN order_items oi ON oi.product_id = p.product_id
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  GROUP BY c.name, p.product_id, p.name
)
SELECT category, product, revenue
FROM ranked
WHERE dr <= 5;
```
**Explanation:** DENSE_RANK compresses gap between ranks so equal values share the same leaderboard position.

## Q66: Running total of daily revenue.

**Schema:** orders (order_id, order_date, total_amount, status)

**Query:**
```sql
SELECT DATE_FORMAT(order_date, '%Y-%m-%d') AS day,
       SUM(total_amount)                   AS daily_revenue,
       SUM(SUM(total_amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m-%d')) AS running_total
FROM orders
WHERE status = 'completed'
GROUP BY DATE_FORMAT(order_date, '%Y-%m-%d')
ORDER BY day;
```
**Explanation:** The window SUM over cumulative order of days builds a running revenue curve from the grouped daily totals.

## Q67: 90-day moving average of revenue.

**Schema:** orders (order_id, order_date, total_amount, status)

**Query:**
```sql
WITH daily AS (
  SELECT DATE(order_date) AS day, SUM(total_amount) AS revenue
  FROM orders
  WHERE status = 'completed'
  GROUP BY DATE(order_date)
)
SELECT day, revenue,
       ROUND(AVG(revenue) OVER (ORDER BY day
                ROWS BETWEEN 89 PRECEDING AND CURRENT ROW), 2) AS moving_avg_90d
FROM daily
ORDER BY day;
```
**Explanation:** A 90-row window (one row per day) smooths the daily noise into an annualized trend line.

## Q68: Customer cohort retention — % of each acquisition cohort active per month.

**Schema:** customers (customer_id), orders (customer_id, order_date, status)

**Query:**
```sql
WITH cohort AS (
  SELECT customer_id, DATE_FORMAT(MIN(order_date), '%Y-%m') AS cohort
  FROM orders WHERE status = 'completed' GROUP BY customer_id
),
active AS (
  SELECT c.cohort,
         DATE_FORMAT(o.order_date, '%Y-%m') AS month,
         COUNT(DISTINCT c.customer_id)      AS active_customers
  FROM cohort c
  JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
  GROUP BY c.cohort, DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT cohort, month, active_customers,
       FIRST_VALUE(active_customers) OVER (PARTITION BY cohort ORDER BY month) AS cohort_size,
       ROUND(active_customers * 100.0 /
             FIRST_VALUE(active_customers) OVER (PARTITION BY cohort ORDER BY month), 1) AS retention_pct
FROM active
ORDER BY cohort, month;
```
**Explanation:** Month zero activity = cohort size; every later month is expressed as a percentage of it — the canonical retention table.

**Alt1:**
```sql
-- PostgreSQL variant (same logic, to_char)
WITH cohort AS (
  SELECT customer_id, to_char(MIN(order_date), 'YYYY-MM') AS cohort
  FROM orders WHERE status = 'completed' GROUP BY customer_id
)
SELECT cohort, active_customers FROM active ...;
```

## Q69: Time from first to second purchase, bucketed.

**Schema:** orders (order_id, customer_id, order_date, status)

**Query:**
```sql
WITH ranked AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders WHERE status = 'completed'
),
seconds AS (
  SELECT customer_id,
         MAX(CASE WHEN rn = 1 THEN order_date END) AS first_date,
         MAX(CASE WHEN rn = 2 THEN order_date END) AS second_date
  FROM ranked
  GROUP BY customer_id
  HAVING COUNT(*) >= 2
)
SELECT CASE WHEN DATEDIFF(second_date, first_date) <= 30 THEN '0-30 days'
            WHEN DATEDIFF(second_date, first_date) <= 60 THEN '31-60 days'
            WHEN DATEDIFF(second_date, first_date) <= 90 THEN '61-90 days'
            ELSE '90+ days' END AS gap_bucket,
       COUNT(*) AS customers
FROM seconds
GROUP BY CASE WHEN DATEDIFF(second_date, first_date) <= 30 THEN '0-30 days'
              WHEN DATEDIFF(second_date, first_date) <= 60 THEN '31-60 days'
              WHEN DATEDIFF(second_date, first_date) <= 90 THEN '61-90 days'
              ELSE '90+ days' END
ORDER BY MIN(DATEDIFF(second_date, first_date));
```
**Explanation:** Collapses each repeat customer to a single first-to-second gap then buckets the distribution into weeks.

## Q70: Reorder rate per product — how many orders have ever contained it.

**Schema:** products (product_id, name), order_items (order_id, product_id, quantity), orders (status)

**Query:**
```sql
SELECT p.product_id, p.name,
       COUNT(DISTINCT o.order_id) AS orders_containing,
       SUM(oi.quantity)           AS units_sold
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
GROUP BY p.product_id, p.name
HAVING COUNT(DISTINCT o.order_id) >= 2
ORDER BY orders_containing DESC;
```
**Explanation:** Filtering buyers who carried an SKU more than once identifies repeat-order merchandise vs one-off stock.

## Q71: Warranty claims by product batch.

**Schema:** warranty_claims (claim_id, product_id, batch_no, claim_type, claim_date), products (product_id, name)

**Query:**
```sql
SELECT p.product_id, p.name,
       w.batch_no,
       COUNT(w.claim_id) AS claims,
       SUM(CASE WHEN w.claim_type = 'defect' THEN 1 ELSE 0 END) AS defect_claims
FROM warranty_claims w
JOIN products p ON p.product_id = w.product_id
GROUP BY p.product_id, p.name, w.batch_no
ORDER BY claims DESC;
```
**Explanation:** Grouping claims by manufacturing batch flags production runs with abnormally high failures.

## Q72: Warranty claim rate per category (claims per 1k units sold).

**Schema:** categories (category_id, name), products (category_id), order_items (product_id, quantity), orders (status), warranty_claims (product_id)

**Query:**
```sql
WITH claims AS (
  SELECT product_id, COUNT(*) AS c
  FROM warranty_claims GROUP BY product_id
)
SELECT c.name AS category,
       SUM(oi.quantity)                       AS units_sold,
       COALESCE(SUM(cl.c), 0)                 AS claims,
       ROUND(COALESCE(SUM(cl.c), 0) * 1000.0
             / NULLIF(SUM(oi.quantity), 0), 1) AS claims_per_1k_units
FROM categories c
JOIN products p ON p.category_id = c.category_id
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
LEFT JOIN claims cl ON cl.product_id = p.product_id
GROUP BY c.name
ORDER BY claims_per_1k_units DESC;
```
**Explanation:** Pre-aggregated claim counts avoid row multiplication; normalizing by sales volume compares quality fairly across categories.

## Q73: Duplicate-order anomaly — same customer and amount on the same day.

**Schema:** orders (order_id, customer_id, total_amount, order_date, status)

**Query:**
```sql
SELECT customer_id, total_amount, DATE(order_date) AS order_day,
       COUNT(*) AS suspicious_orders,
       GROUP_CONCAT(order_id) AS order_ids
FROM orders
WHERE status = 'completed'
GROUP BY customer_id, total_amount, DATE(order_date)
HAVING COUNT(*) > 1;
```
**Explanation:** Same customer + same total + same day is a classic accidental double-submit fingerprint; GROUP_CONCAT shows the rows.

## Q74: Partial shipments — orders split across more than one shipment.

**Schema:** orders (order_id, status), shipments (shipment_id, order_id), order_items (order_id, product_id)

**Query:**
```sql
SELECT o.order_id,
       COUNT(DISTINCT s.shipment_id) AS shipment_count,
       COUNT(DISTINCT oi.product_id) AS distinct_products
FROM orders o
LEFT JOIN shipments s ON s.order_id = o.order_id
LEFT JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY o.order_id
HAVING COUNT(DISTINCT s.shipment_id) > 1;
```
**Explanation:** HAVING > 1 shipment for one order exposes split orders — useful for a carrier-cost and SLA deep dive.

## Q75: Do late deliveries correlate with higher returns?

**Schema:** shipments (shipment_id, order_id, delivered_date, expected_date), returns (return_id, order_id)

**Query:**
```sql
SELECT CASE WHEN s.delivered_date > s.expected_date THEN 'Late delivery'
            ELSE 'On-time delivery' END                AS delivery_class,
       COUNT(DISTINCT s.order_id)                      AS orders,
       COUNT(DISTINCT r.return_id)                     AS returns,
       ROUND(COUNT(DISTINCT r.return_id) * 100.0
             / COUNT(DISTINCT s.order_id), 1)          AS return_pct
FROM shipments s
LEFT JOIN returns r ON r.order_id = s.order_id
WHERE s.delivered_date IS NOT NULL
GROUP BY CASE WHEN s.delivered_date > s.expected_date THEN 'Late delivery'
              ELSE 'On-time delivery' END;
```
**Explanation:** Compares the return rate of on-time vs late orders — a quick test of the delivery-quality hypothesis.


## Q76: Monthly cancellation rate trend.

**Schema:** orders (order_id, order_date, status)

**Query:**
```sql
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       COUNT(*)                         AS all_orders,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)
             * 100.0 / COUNT(*), 1)     AS cancel_rate_pct
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```
**Explanation:** All orders (not just completed) form the denominator; rising cancellation share flags funnel friction.

## Q77: Distribution of days between consecutive customer orders.

**Schema:** orders (order_id, customer_id, order_date, status)

**Query:**
```sql
WITH ranked AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders WHERE status = 'completed'
)
SELECT DATEDIFF(o2.order_date, o1.order_date) AS gap_days,
       COUNT(*)                               AS occurrences
FROM ranked o1
JOIN ranked o2
  ON o2.customer_id = o1.customer_id
 AND o2.rn = o1.rn + 1
GROUP BY DATEDIFF(o2.order_date, o1.order_date)
ORDER BY gap_days;
```
**Explanation:** Every consecutive order pair yields one inter-purchase gap; the histogram shows the natural repurchase cadence.

## Q78: Revenue attribution by marketing channel.

**Schema:** orders (order_id, channel, total_amount, status)

**Query:**
```sql
SELECT channel,
       COUNT(DISTINCT order_id) AS orders,
       SUM(total_amount)        AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY channel
ORDER BY revenue DESC;
```
**Explanation:** Slices completed sales by acquisition channel to rank marketing sources by dollar contribution.

**Alt1:**
```sql
-- SQL Server ROLLUP adds a grand-total summary row
SELECT COALESCE(channel, 'ALL') AS channel,
       COUNT(DISTINCT order_id) AS orders,
       SUM(total_amount)        AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY ROLLUP(channel);
```

## Q79: Cart abandonment by device type.

**Schema:** carts (cart_id, customer_id, created_date, device, order_id)

**Query:**
```sql
SELECT device,
       COUNT(*)                 AS carts,
       SUM(CASE WHEN order_id IS NOT NULL THEN 1 ELSE 0 END) AS converted,
       ROUND(SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS abandonment_pct
FROM carts
GROUP BY device
ORDER BY abandonment_pct DESC;
```
**Explanation:** Carts that never reach an order decide the funnel gap; grouping by device localizes the weakest surface.

## Q80: Average order value by device.

**Schema:** orders (order_id, device, total_amount, status)

**Query:**
```sql
SELECT device,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(AVG(total_amount), 2) AS aov
FROM orders
WHERE status = 'completed'
GROUP BY device
ORDER BY aov DESC;
```
**Explanation:** AOV by device answers whether mobile or desktop customers carry larger baskets.

## Q81: Discount-first vs full-price-first customers — effect on lifetime value.

**Schema:** orders (customer_id, order_date, total_amount, discount_amount, status)

**Query:**
```sql
WITH firsts AS (
  SELECT customer_id,
         FIRST_VALUE(total_amount)
           OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS first_amount,
         FIRST_VALUE(discount_amount)
           OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS first_discount
  FROM orders
  WHERE status = 'completed'
),
ltv AS (
  SELECT customer_id, SUM(total_amount) AS ltv
  FROM orders WHERE status = 'completed'
  GROUP BY customer_id
)
SELECT CASE WHEN f.first_discount > 0 THEN 'Discount-first' ELSE 'Full-price-first' END AS cohort,
       COUNT(DISTINCT f.customer_id) AS customers,
       ROUND(AVG(l.ltv), 2)          AS avg_ltv
FROM firsts f
JOIN ltv l ON l.customer_id = f.customer_id
GROUP BY CASE WHEN f.first_discount > 0 THEN 'Discount-first' ELSE 'Full-price-first' END
ORDER BY avg_ltv DESC;
```
**Explanation:** Splits customers by whether their very first order carried a discount, then compares total lifetime spend.

## Q82: Customer spend percentile ranks.

**Schema:** customers (customer_id), orders (customer_id, total_amount, status)

**Query:**
```sql
WITH spend AS (
  SELECT customer_id, SUM(total_amount) AS ltv
  FROM orders WHERE status = 'completed'
  GROUP BY customer_id
)
SELECT customer_id, ROUND(ltv, 2) AS ltv,
       ROUND(PERCENT_RANK() OVER (ORDER BY ltv) * 100, 1) AS spend_percentile
FROM spend
ORDER BY ltv DESC;
```
**Explanation:** PERCENT_RANK normalizes each customer's LTV to a 0-100 position in the spend distribution.

**Alt1:**
```sql
-- SQL Server NTILE deciles
SELECT customer_id, ROUND(ltv, 2) AS ltv,
       NTILE(10) OVER (ORDER BY ltv) AS spend_decile
FROM (SELECT customer_id, SUM(total_amount) AS ltv
      FROM orders WHERE status = 'completed' GROUP BY customer_id) t;
```

## Q83: Revenue share by payment method.

**Schema:** orders (order_id, payment_method, total_amount, status)

**Query:**
```sql
SELECT payment_method,
       COUNT(DISTINCT order_id) AS orders,
       SUM(total_amount)        AS revenue,
       ROUND(SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER (), 1) AS share_pct
FROM orders
WHERE status = 'completed'
GROUP BY payment_method
ORDER BY revenue DESC;
```
**Explanation:** Window SUM over the grouped rows produces the grand total without a second scan; each method gets its share.

## Q84: Days of inventory on hand per product.

**Schema:** inventory (product_id, quantity_on_hand), order_items (product_id, quantity), orders (status, order_date)

**Query:**
```sql
-- MySQL
WITH demand AS (
  SELECT oi.product_id, SUM(oi.quantity) / 30.0 AS daily_demand
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  WHERE o.status = 'completed'
    AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
  GROUP BY oi.product_id
)
SELECT p.product_id, p.name,
       i.quantity_on_hand,
       ROUND(i.quantity_on_hand / NULLIF(d.daily_demand, 0), 1) AS days_on_hand
FROM products p
JOIN inventory i ON i.product_id = p.product_id
LEFT JOIN demand d ON d.product_id = p.product_id
ORDER BY days_on_hand;
```
**Explanation:** Days on hand = current stock divided by average daily demand; the ranking separates fast movers from overstock.

## Q85: Deadstock — positive stock but zero sales in the last 180 days.

**Schema:** inventory (product_id, quantity_on_hand), products (product_id, name), order_items, orders (order_date)

**Query:**
```sql
SELECT p.product_id, p.name,
       i.quantity_on_hand,
       i.warehouse_id
FROM inventory i
JOIN products p ON p.product_id = i.product_id
WHERE i.quantity_on_hand > 0
  AND NOT EXISTS (
    SELECT 1
    FROM order_items oi
    JOIN orders o ON o.order_id = oi.order_id
    WHERE oi.product_id = p.product_id
      AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 180 DAY)
  )
ORDER BY i.quantity_on_hand DESC;
```
**Explanation:** NOT EXISTS proof of zero recent movement isolates SKUs occupying warehouse space without returning revenue.

## Q86: Seasonality index per category (month revenue vs category average).

**Schema:** categories (category_id, name), products (category_id), order_items (product_id), orders (order_date, status)

**Query:**
```sql
WITH monthly AS (
  SELECT c.category_id, c.name AS category,
         DATE_FORMAT(o.order_date, '%Y-%m') AS ym,
         DATE_FORMAT(o.order_date, '%m')    AS month,
         SUM(oi.quantity * oi.unit_price)   AS revenue
  FROM categories c
  JOIN products p ON p.category_id = c.category_id
  JOIN order_items oi ON oi.product_id = p.product_id
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  GROUP BY c.category_id, c.name,
           DATE_FORMAT(o.order_date, '%Y-%m'), DATE_FORMAT(o.order_date, '%m')
)
SELECT category, month, ROUND(revenue, 2) AS revenue,
       ROUND(AVG(revenue) OVER (PARTITION BY category_id), 2) AS avg_monthly,
       ROUND(revenue / AVG(revenue) OVER (PARTITION BY category_id), 2) AS seasonality_index
FROM monthly
ORDER BY category, month;
```
**Explanation:** Each month's revenue is divided by the category's average month — values well above 1 reveal the high season.

## Q87: Year-over-year revenue growth by month.

**Schema:** orders (order_id, order_date, total_amount, status)

**Query:**
```sql
WITH monthly AS (
  SELECT DATE_FORMAT(order_date, '%Y-%m') AS ym, SUM(total_amount) AS revenue
  FROM orders WHERE status = 'completed'
  GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT ym, revenue,
       LAG(revenue, 12) OVER (ORDER BY ym) AS same_month_last_year,
       ROUND((revenue / LAG(revenue, 12) OVER (ORDER BY ym) - 1) * 100, 1) AS yoy_growth_pct
FROM monthly
ORDER BY ym;
```
**Explanation:** LAG with an offset of 12 rows pairs each month with its counterpart a year prior for YoY growth.

## Q88: Weekly active buyers over time.

**Schema:** orders (order_id, order_date, customer_id, status)

**Query:**
```sql
SELECT YEARWEEK(order_date, 1) AS week_no,
       COUNT(DISTINCT customer_id) AS active_buyers
FROM orders
WHERE status = 'completed'
GROUP BY YEARWEEK(order_date, 1)
ORDER BY week_no;
```
**Explanation:** YEARWEEK collapses dates into ISO weeks; distinct buyers per week is the standard WAU metric.

**Alt1:**
```sql
-- PostgreSQL equivalent using date_trunc
SELECT date_trunc('week', order_date)::date AS week_start,
       COUNT(DISTINCT customer_id)          AS active_buyers
FROM orders
WHERE status = 'completed'
GROUP BY date_trunc('week', order_date)
ORDER BY week_start;
```

## Q89: Premium vs economy segment split by basket value.

**Schema:** orders (order_id, total_amount, status), customers (customer_id, segment)

**Query:**
```sql
SELECT c.segment,
       COUNT(DISTINCT o.order_id) AS orders,
       SUM(o.total_amount)        AS revenue,
       ROUND(AVG(o.total_amount), 2) AS aov
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
GROUP BY c.segment
ORDER BY revenue DESC;
```
**Explanation:** Segments the customer base by signup tier and compares how each drives orders, revenue, and basket size.

## Q90: Top 1% heavy buyers and their revenue share (whale check).

**Schema:** customers (customer_id), orders (customer_id, total_amount, status)

**Query:**
```sql
WITH spend AS (
  SELECT customer_id, SUM(total_amount) AS ltv,
         NTILE(100) OVER (ORDER BY SUM(total_amount) DESC) AS pct_bucket
  FROM orders
  WHERE status = 'completed'
  GROUP BY customer_id
)
SELECT ROUND(SUM(CASE WHEN pct_bucket = 1 THEN ltv ELSE 0 END), 2)    AS top_1pct_revenue,
       ROUND(SUM(ltv), 2)                                             AS total_revenue,
       ROUND(SUM(CASE WHEN pct_bucket = 1 THEN ltv ELSE 0 END) * 100.0 / SUM(ltv), 1) AS top_1pct_share_pct
FROM spend;
```
**Explanation:** NTILE(100) buckets customers into percentiles; the top bucket's revenue share exposes concentration risk.

## Q91: RFM segmentation — recency, frequency, monetary score per customer.

**Schema:** customers (customer_id), orders (customer_id, order_date, total_amount, status)

**Query:**
```sql
WITH rfm AS (
  SELECT customer_id,
         DATEDIFF(CURDATE(), MAX(order_date))                                  AS recency,
         COUNT(DISTINCT order_id)                                              AS frequency,
         SUM(total_amount)                                                     AS monetary
  FROM orders
  WHERE status = 'completed'
  GROUP BY customer_id
)
SELECT customer_id,
       NTILE(5) OVER (ORDER BY recency ASC)  AS r_score,
       NTILE(5) OVER (ORDER BY frequency DESC) AS f_score,
       NTILE(5) OVER (ORDER BY monetary DESC)  AS m_score,
       CONCAT(NTILE(5) OVER (ORDER BY recency ASC),
              NTILE(5) OVER (ORDER BY frequency DESC),
              NTILE(5) OVER (ORDER BY monetary DESC)) AS rfm_code
FROM rfm;
```
**Explanation:** Each dimension is bucketed 1-5 (newest/most/richest = 5); the 3-digit code feeds churn and win-back targeting.

## Q92: Product affinity — strongest item pairs with both directions.

**Schema:** products (product_id, name), order_items (order_id, product_id)

**Query:**
```sql
WITH basket AS (
  SELECT DISTINCT order_id, product_id FROM order_items
)
SELECT pa.name AS product_a, pb.name AS product_b,
       COUNT(*) AS co_occurrences,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT order_id) FROM order_items), 2) AS support_pct
FROM basket a
JOIN basket b
  ON b.order_id = a.order_id
 AND b.product_id > a.product_id
JOIN products pa ON pa.product_id = a.product_id
JOIN products pb ON pb.product_id = b.product_id
GROUP BY pa.name, pb.name
ORDER BY co_occurrences DESC
LIMIT 10;
```
**Explanation:** Pair co-occurrence with global support % ranks the bundles most worth merchandising together.

## Q93: Churn-risk customers — previously frequent, now silent for 60+ days.

**Schema:** customers (customer_id, name), orders (customer_id, order_date, order_id, status)

**Query:**
```sql
WITH last_order AS (
  SELECT customer_id, MAX(order_date) AS last_order_date,
         COUNT(DISTINCT order_id)     AS total_orders
  FROM orders WHERE status = 'completed'
  GROUP BY customer_id
)
SELECT c.customer_id, c.name,
       l.total_orders,
       l.last_order_date,
       DATEDIFF(CURDATE(), l.last_order_date) AS days_since_last_order
FROM last_order l
JOIN customers c ON c.customer_id = l.customer_id
WHERE l.total_orders >= 3
  AND l.last_order_date < DATE_SUB(CURDATE(), INTERVAL 60 DAY)
ORDER BY days_since_last_order DESC;
```
**Explanation:** "Was loyal (3+ orders) but silent 60+ days" defines the churn-risk segment for re-engagement.

## Q94: Each customer's next category — category-level repurchase signal.

**Schema:** categories (category_id, name), products (category_id), orders, order_items

**Query:**
```sql
WITH cat_orders AS (
  SELECT oi.order_id AS order_id,
         MAX(c.category_name) AS category
  FROM order_items oi
  JOIN products p ON p.product_id = oi.product_id
  JOIN categories c ON c.category_id = p.category_id
  GROUP BY oi.order_id
)
SELECT category,
       COUNT(*) AS orders_in_category,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS share_pct
FROM cat_orders
GROUP BY category
ORDER BY orders_in_category DESC;
```
**Explanation:** Flattens every order to one category (highest-name tie-break) and measures category demand mix.

## Q95: Pareto concentration — revenue share of the biggest (top 2% of) customers.

**Schema:** orders (order_id, customer_id, total_amount, status)

**Query:**
```sql
WITH spend AS (
  SELECT customer_id, SUM(total_amount) AS ltv,
         PERCENT_RANK() OVER (ORDER BY SUM(total_amount) DESC) AS pct
  FROM orders
  WHERE status = 'completed'
  GROUP BY customer_id
)
SELECT ROUND(SUM(ltv), 2) AS total_revenue,
       ROUND(SUM(CASE WHEN pct < 0.02 THEN ltv ELSE 0 END), 2) AS top_2pct_customer_revenue,
       ROUND(SUM(CASE WHEN pct < 0.02 THEN ltv ELSE 0 END) * 100.0 / SUM(ltv), 1) AS top_2pct_share_pct
FROM spend;
```
**Explanation:** PERCENT_RANK positions each customer in the spend curve; the top 2% bucket's take shows how concentrated revenue is on the biggest spenders.

## Q96: Full-funnel conversion — cart to checkout to paid to shipped to delivered.

**Schema:** carts (cart_id, created_date, order_id), orders (status), shipments (order_id)

**Query:**
```sql
SELECT COUNT(*) AS carts_created,
       COUNT(CASE WHEN c.order_id IS NOT NULL THEN 1 END)                                              AS orders_placed,
       COUNT(CASE WHEN o.status IN ('paid', 'shipped', 'completed') THEN 1 END)                        AS paid,
       COUNT(CASE WHEN s.shipment_id IS NOT NULL THEN 1 END)                                           AS shipped,
       COUNT(CASE WHEN s.delivered_date IS NOT NULL THEN 1 END)                                        AS delivered,
       ROUND(COUNT(CASE WHEN o.status IN ('paid', 'shipped', 'completed') THEN 1 END) * 100.0 / COUNT(*), 1) AS cart_to_paid_pct
FROM carts c
LEFT JOIN orders o ON o.order_id = c.order_id
LEFT JOIN shipments s ON s.order_id = c.order_id;
```
**Explanation:** One chain of LEFT JOINs maps every cart to its order and shipment, exposing where each step drops off.

## Q97: Funnel drop-off between each consecutive stage.

**Schema:** carts (cart_id, order_id), orders (status), shipments (order_id)

**Query:**
```sql
WITH f AS (
  SELECT COUNT(*) AS carts,
         SUM(CASE WHEN c.order_id IS NOT NULL THEN 1 ELSE 0 END) AS orders,
         SUM(CASE WHEN o.status IN ('paid', 'shipped', 'completed') THEN 1 ELSE 0 END) AS paid,
         SUM(CASE WHEN s.delivered_date IS NOT NULL THEN 1 ELSE 0 END) AS delivered
  FROM carts c
  LEFT JOIN orders o ON o.order_id = c.order_id
  LEFT JOIN shipments s ON s.order_id = c.order_id
)
SELECT carts AS stage0_carts,
       orders AS stage1_orders,
       paid   AS stage2_paid,
       ROUND((carts - orders) * 100.0 / carts, 1) AS cart_to_order_drop_pct,
       ROUND((orders - paid) * 100.0 / orders, 1) AS order_to_paid_drop_pct,
       ROUND((paid - delivered) * 100.0 / paid, 1) AS paid_to_delivered_drop_pct
FROM f;
```
**Explanation:** Absolute counts plus inter-stage drop percentages identify the funnel step losing the most volume.

**Alt1:**
```sql
-- PostgreSQL: full stage chain plus neighbouring-stage retention in one row
WITH f AS (
  SELECT COUNT(*) AS carts,
         COUNT(DISTINCT o.order_id) AS orders,
         COUNT(DISTINCT CASE WHEN o.status IN ('paid', 'shipped', 'completed')
              THEN o.order_id END)  AS paid,
         COUNT(DISTINCT s.order_id) AS shipped,
         COUNT(DISTINCT CASE WHEN s.delivered_date IS NOT NULL
              THEN s.order_id END)  AS delivered
  FROM carts c
  LEFT JOIN orders o  ON o.order_id = c.order_id
  LEFT JOIN shipments s ON s.order_id = c.order_id
)
SELECT carts, orders, paid, shipped, delivered,
       ROUND(paid * 100.0 / carts, 1)      AS cart_to_paid_pct,
       ROUND(delivered * 100.0 / paid, 1)  AS paid_to_delivered_pct
FROM f;
```

## Q98: Funnel per seller — which vendor loses most orders before delivery.

**Schema:** vendors (vendor_id, vendor_name), products (vendor_id), order_items, orders (status), shipments (order_id)

**Query:**
```sql
SELECT vt.vendor_name,
       COUNT(DISTINCT o.order_id) AS orders,
       SUM(CASE WHEN o.status IN ('paid', 'shipped', 'completed') THEN 1 ELSE 0 END) AS paid,
       COUNT(DISTINCT s.shipment_id) AS shipped,
       SUM(CASE WHEN s.delivered_date IS NOT NULL THEN 1 ELSE 0 END) AS delivered,
       ROUND(SUM(CASE WHEN s.delivered_date IS NOT NULL THEN 1 ELSE 0 END) * 100.0
             / COUNT(DISTINCT o.order_id), 1) AS paid_to_delivered_pct
FROM vendors vt
JOIN products p ON p.vendor_id = vt.vendor_id
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id
LEFT JOIN shipments s ON s.order_id = o.order_id
GROUP BY vt.vendor_name
ORDER BY paid_to_delivered_pct;
```
**Explanation:** The seller-level funnel isolates vendors whose delivery stage underperforms the marketplace average.

## Q99: Channel funnel comparison — conversion by acquisition channel.

**Schema:** carts (cart_id, customer_id), customers (customer_id, channel), orders (order_id, status), shipments

**Query:**
```sql
SELECT cu.channel,
       COUNT(DISTINCT ca.cart_id) AS carts,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(COUNT(DISTINCT o.order_id) * 100.0 / COUNT(DISTINCT ca.cart_id), 1) AS cart_to_order_pct
FROM customers cu
JOIN carts ca ON ca.customer_id = cu.customer_id
LEFT JOIN orders o ON o.order_id = ca.order_id AND o.status IN ('paid', 'shipped', 'completed')
GROUP BY cu.channel
ORDER BY cart_to_order_pct DESC;
```
**Explanation:** Joins customers -> their carts -> resulting orders and measures each channel's success at closing the funnel.

## Q100: CAPSTONE — full-funnel revenue pipeline with per-stage rollup and diagnostics.

**Schema:** carts (cart_id, customer_id, created_date, order_id, device), customers (customer_id, region, channel), orders (order_id, customer_id, order_date, status, total_amount, discount_amount, payment_method, device), order_items (order_id, product_id, quantity, unit_price), products (product_id, name, price, cost, category_id, vendor_id), categories (category_id, name), inventory (product_id, quantity_on_hand, reorder_point), shipments (shipment_id, order_id, region, ship_date, delivered_date, expected_date, shipping_cost), reviews (review_id, product_id, rating), returns (return_id, order_id, product_id, reason, refund_amount), warranty_claims (claim_id, product_id, batch_no, claim_date)

**Query:**
```sql
WITH funnel AS (
  SELECT c.customer_id,
         COUNT(DISTINCT c.cart_id)                                              AS carts,
         COALESCE(COUNT(DISTINCT o.order_id), 0)                                AS orders,
         SUM(CASE WHEN o.status IN ('paid', 'shipped', 'completed') THEN 1 ELSE 0 END) AS paid,
         SUM(CASE WHEN s.shipment_id IS NOT NULL THEN 1 ELSE 0 END)             AS shipped,
         SUM(CASE WHEN s.delivered_date IS NOT NULL THEN 1 ELSE 0 END)          AS delivered
  FROM carts c
  LEFT JOIN orders o ON o.order_id = c.order_id
  LEFT JOIN shipments s ON s.order_id = c.order_id
  GROUP BY c.customer_id
),
customer_metrics AS (
  SELECT o.customer_id,
         SUM(oi.quantity * oi.unit_price) AS gross_revenue,
         SUM(oi.quantity * oi.unit_price - p.cost * oi.quantity) AS product_margin,
         SUM(o.discount_amount)           AS discounts,
         SUM(s.shipping_cost)             AS shipping_cost,
         COUNT(DISTINCT r.return_id)      AS returns,
         COUNT(DISTINCT w.claim_id)       AS warranty_claims
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.order_id
  JOIN products p ON p.product_id = oi.product_id
  LEFT JOIN shipments s ON s.order_id = o.order_id
  LEFT JOIN returns r ON r.order_id = o.order_id
  LEFT JOIN warranty_claims w ON w.product_id = oi.product_id
  GROUP BY o.customer_id
)
SELECT cu.region,
       COUNT(DISTINCT cu.customer_id)                          AS customers,
       SUM(f.carts)                                            AS carts,
       SUM(f.orders)                                           AS orders,
       SUM(f.paid)                                             AS paid,
       SUM(f.shipped)                                          AS shipped,
       SUM(f.delivered)                                        AS delivered,
       ROUND(SUM(f.paid) * 100.0 / NULLIF(SUM(f.carts), 0), 1) AS cart_to_paid_pct,
       ROUND(SUM(cm.gross_revenue), 2)                         AS gross_revenue,
       ROUND(SUM(cm.product_margin) - SUM(cm.discounts) - SUM(cm.shipping_cost), 2) AS net_contribution,
       ROUND(SUM(cm.returns) * 100.0 / NULLIF(SUM(f.paid), 0), 1) AS return_rate_pct,
       SUM(cm.warranty_claims)                                 AS warranty_claims
FROM customers cu
LEFT JOIN funnel f ON f.customer_id = cu.customer_id
LEFT JOIN customer_metrics cm ON cm.customer_id = cu.customer_id
GROUP BY cu.region
HAVING SUM(f.carts) > 0
ORDER BY gross_revenue DESC;
```
**Explanation:** Pulls the whole picture in one pass: funnel stages, gross revenue, contribution after discounts and freight, plus returns and warranty loads, rolled up by region.

**Alt1 — final polish:** pull out the net contribution and returns widgets into a hand-maintained region_view so downstream reports never recompute freight and discounts twice:
```sql
CREATE VIEW vw_region_revenue_pipeline AS
SELECT region, SUM(gross_revenue) AS gross_revenue,
       SUM(product_margin - discounts - shipping_cost) AS net_contribution
FROM customer_metrics cm
JOIN customers cu ON cu.customer_id = cm.customer_id
GROUP BY region;
```
