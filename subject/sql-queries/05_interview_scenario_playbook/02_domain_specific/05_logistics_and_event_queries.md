# Logistics, Shipping and Event SQL Scenarios — 100 Interview Q&A

> **Schema Reference (used across questions — columns may vary per question):**
>
> | Table | Key Columns |
> |---|---|
> | `shipments` | `shipment_id`, `origin`, `destination`, `weight`, `cost`, `status`, `created_at`, `delivered_at` |
> | `trucks` | `truck_id`, `capacity`, `driver_id`, `home_depot` |
> | `trips` | `trip_id`, `truck_id`, `route_id`, `driver_id`, `departure_at`, `arrival_at`, `miles` |
> | `routes` | `route_id`, `origin`, `destination`, `distance_miles` |
> | `waybill_events` | `event_id`, `shipment_id`, `truck_id`, `event_time`, `status`, `location` |
> | `warehouses` | `warehouse_id`, `name`, `region`, `capacity` |
> | `inventory` | `sku`, `warehouse_id`, `qty_on_hand`, `reorder_point`, `last_restock_at` |
> | `fuel_logs` | `trip_id`, `gallons`, `cost_per_gallon`, `logged_at` |
> | `exceptions` | `exception_id`, `shipment_id`, `reason_code`, `logged_at`, `resolved_at` |

---

## Q1: Average delivery duration by origin region

**Schema:** `shipments(shipment_id, origin, destination, weight, cost, status, created_at, delivered_at)`

```sql
SELECT
    origin,
    COUNT(*)                          AS total_shipments,
    ROUND(AVG(DATEDIFF(day, created_at, delivered_at)), 1) AS avg_days
FROM shipments
WHERE delivered_at IS NOT NULL
GROUP BY origin
ORDER BY avg_days DESC;
```

**Explanation:** `DATEDIFF` computes the calendar-day span; grouping by origin surfaces regional throughput differences.

**Alt1:** PostgreSQL version: `EXTRACT(DAY FROM delivered_at - created_at)` or `(delivered_at::date - created_at::date)` for integer days.

---

## Q2: On-time delivery percentage per route (SLA = 3 days)

**Schema:** `shipments(shipment_id, destination, status, created_at, delivered_at)`

```sql
SELECT
    destination,
    COUNT(*)                                                  AS total,
    SUM(CASE WHEN DATEDIFF(day, created_at, delivered_at) <= 3
             THEN 1 ELSE 0 END)                              AS on_time,
    ROUND(100.0 * SUM(CASE WHEN DATEDIFF(day, created_at, delivered_at) <= 3
                           THEN 1 ELSE 0 END) / COUNT(*), 1) AS on_time_pct
FROM shipments
WHERE delivered_at IS NOT NULL
GROUP BY destination
ORDER BY on_time_pct;
```

**Explanation:** Conditional aggregation flags rows within the SLA window and computes a percentage.

**Alt1:** For sliding-window SLA that accounts for weekends/holidays, join a `calendar` table and use `WORKDAY` logic instead of raw `DATEDIFF`.

---

## Q3: Delivery duration distribution — percentile buckets

**Schema:** `shipments(shipment_id, origin, delivered_at, created_at)`

```sql
-- PostgreSQL
SELECT
    width_bucket(DATEDIFF(day, created_at, delivered_at), 0, 15, 5) AS bucket,
    CONCAT(width_bucket(DATEDIFF(day, created_at, delivered_at), 0, 15, 5) * 3,
           '-', (width_bucket(DATEDIFF(day, created_at, delivered_at), 0, 15, 5) + 1) * 3,
           ' days') AS range_label,
    COUNT(*) AS cnt
FROM shipments
WHERE delivered_at IS NOT NULL
GROUP BY bucket
ORDER BY bucket;
```

**Explanation:** `width_bucket` bins continuous duration into equal-width buckets for histogram analysis.

**Alt1:** MySQL version: `FLOOR(DATEDIFF(day, created_at, delivered_at) / 3) AS bucket` with `CONCAT` for range labels.

---

## Q4: Late shipments — count and total cost penalty (SLA = 5 days)

**Schema:** `shipments(shipment_id, cost, status, created_at, delivered_at)`

```sql
SELECT
    COUNT(*)                                         AS late_count,
    SUM(cost)                                        AS late_revenue_at_risk,
    AVG(DATEDIFF(day, created_at, delivered_at) - 5) AS avg_days_overdue
FROM shipments
WHERE delivered_at IS NOT NULL
  AND DATEDIFF(day, created_at, delivered_at) > 5;
```

**Explanation:** Filters to shipments exceeding the SLA and aggregates cost exposure plus average tardiness.

---

## Q5: Transit stops count between first and last waybill event per shipment

**Schema:** `waybill_events(event_id, shipment_id, event_time, status, location)`

```sql
-- PostgreSQL
SELECT
    shipment_id,
    COUNT(*) - 1 AS intermediate_stops,
    MIN(event_time) AS first_event,
    MAX(event_time) AS last_event
FROM waybill_events
GROUP BY shipment_id
HAVING COUNT(*) >= 2;
```

**Explanation:** Minus one because the first and last events are origin/destination, not intermediate stops.

**Alt1:** Use `ROW_NUMBER()` ordered by `event_time` to label first/last, then `COUNT(*) - 2` for strict intermediates.

**Alt2 (SQL Server):** `DATEDIFF(HOUR, MIN(event_time), MAX(event_time))` to also get total transit duration alongside stop count.

---

## Q6: Time spent at each status using LAG — event-log gap analysis

**Schema:** `waybill_events(event_id, shipment_id, event_time, status)`

```sql
-- MySQL 8+
WITH ordered AS (
    SELECT
        shipment_id,
        status,
        event_time,
        LAG(event_time) OVER (PARTITION BY shipment_id ORDER BY event_time) AS prev_time
    FROM waybill_events
)
SELECT
    shipment_id,
    prev_time        AS entered_status_at,
    event_time       AS exited_status_at,
    TIMESTAMPDIFF(HOUR, prev_time, event_time) AS hours_in_status
FROM ordered
WHERE prev_time IS NOT NULL
ORDER BY shipment_id, entered_status_at;
```

**Explanation:** `LAG` retrieves the previous event's timestamp; subtracting gives dwell time per status.

**Alt1:** PostgreSQL interval arithmetic: `event_time - LAG(event_time) OVER (...) AS dwell_interval` for native interval output.

---

## Q7: Longest idle period at a warehouse before next movement

**Schema:** `waybill_events(event_id, shipment_id, location, event_time, status)`

```sql
-- PostgreSQL
WITH warehouse_events AS (
    SELECT
        shipment_id,
        location,
        event_time,
        status,
        LEAD(event_time) OVER (PARTITION BY shipment_id ORDER BY event_time) AS next_event
    FROM waybill_events
    WHERE status IN ('ARRIVED_WAREHOUSE', 'DEPARTED_WAREHOUSE')
)
SELECT
    shipment_id,
    location,
    EXTRACT(EPOCH FROM (next_event - event_time)) / 3600.0 AS idle_hours
FROM warehouse_events
WHERE status = 'ARRIVED_WAREHOUSE'
  AND next_event IS NOT NULL
ORDER BY idle_hours DESC
LIMIT 1;
```

**Explanation:** `LEAD` finds the subsequent event; for warehouse-arrival rows the gap is the dwell time.

---

## Q8: Weight vs cost correlation — Pearson coefficient

**Schema:** `shipments(shipment_id, weight, cost)`

```sql
-- PostgreSQL
SELECT
    ROUND(
      (COUNT(*) * SUM(weight * cost) - SUM(weight) * SUM(cost))
      / NULLIF(
          SQRT(
            (COUNT(*) * SUM(weight * weight) - SUM(weight) * SUM(weight))
            * (COUNT(*) * SUM(cost * cost) - SUM(cost) * SUM(cost))
          ), 0
        ), 4
    ) AS pearson_r
FROM shipments;
```

**Explanation:** Classic closed-form Pearson formula; `NULLIF` avoids division by zero for empty sets.

**Alt1:** Use `CORR(weight, cost)` built-in in PostgreSQL for a one-liner.

**Alt2:** Use `COVAR_SAMP(weight, cost) / (STDDEV(weight) * STDDEV(cost))` in Oracle for the same result.

---

## Q9: Top 10 most frequent origin-destination pairs

**Schema:** `shipments(shipment_id, origin, destination)`

```sql
SELECT
    origin,
    destination,
    COUNT(*) AS pair_count
FROM shipments
GROUP BY origin, destination
ORDER BY pair_count DESC
LIMIT 10;
```

**Explanation:** Simple GROUP BY with a descending sort surfaces the highest-traffic lanes.

---

## Q10: Route efficiency — cost per mile

**Schema:** `trips(trip_id, route_id, miles), shipments(shipment_id, trip_id, cost)`

```sql
-- SQL Server
SELECT
    r.route_id,
    r.origin,
    r.destination,
    r.distance_miles,
    SUM(s.cost)                                          AS total_cost,
    ROUND(SUM(s.cost) / NULLIF(r.distance_miles, 0), 2) AS cost_per_mile
FROM routes r
JOIN trips t      ON t.route_id = r.route_id
JOIN shipments s  ON s.trip_id  = t.trip_id
GROUP BY r.route_id, r.origin, r.destination, r.distance_miles
ORDER BY cost_per_mile DESC;
```

**Explanation:** Total shipment cost on a route divided by distance yields a cost-efficiency metric.

**Alt1:** Compute on trip level first (`trips.miles`) instead of route reference distance when actual driven miles differ from route distance.

---

## Q11: Truck utilization — trips per month

**Schema:** `trucks(truck_id), trips(trip_id, truck_id, departure_at)`

```sql
-- MySQL 8+
SELECT
    t.truck_id,
    DATE_FORMAT(tr.departure_at, '%Y-%m') AS month,
    COUNT(tr.trip_id)                      AS trips
FROM trucks t
JOIN trips tr ON tr.truck_id = t.truck_id
GROUP BY t.truck_id, DATE_FORMAT(tr.departure_at, '%Y-%m')
ORDER BY t.truck_id, month;
```

**Explanation:** `DATE_FORMAT` buckets trips by calendar month for utilization trending.

**Alt1:** PostgreSQL: `TO_CHAR(tr.departure_at, 'YYYY-MM')` achieves the same monthly bucketing.

---

## Q12: Driver load count — total shipments delivered per driver

**Schema:** `trips(trip_id, driver_id), shipments(shipment_id, trip_id, status)`

```sql
SELECT
    t.driver_id,
    COUNT(s.shipment_id) AS deliveries
FROM trips t
JOIN shipments s ON s.trip_id = t.trip_id
WHERE s.status = 'DELIVERED'
GROUP BY t.driver_id
ORDER BY deliveries DESC;
```

**Explanation:** Joining trips to delivered shipments counts each driver's completed workload.

**Alt1:** Add a `WHERE s.delivered_at >= DATEADD(month, 1, GETDATE())` filter for a trailing-30-day rolling view.

---

## Q13: Capacity overflow detection — planned weight vs truck capacity

**Schema:** `trucks(truck_id, capacity), trips(trip_id, truck_id), shipments(shipment_id, trip_id, weight)`

```sql
-- PostgreSQL
WITH trip_weights AS (
    SELECT
        t.trip_id,
        t.truck_id,
        SUM(s.weight) AS planned_weight
    FROM trips t
    JOIN shipments s ON s.trip_id = t.trip_id
    GROUP BY t.trip_id, t.truck_id
)
SELECT
    tw.trip_id,
    tw.truck_id,
    tw.planned_weight,
    tk.capacity,
    tw.planned_weight - tk.capacity AS overflow_weight
FROM trip_weights tw
JOIN trucks tk ON tk.truck_id = tw.truck_id
WHERE tw.planned_weight > tk.capacity
ORDER BY overflow_weight DESC;
```

**Explanation:** Aggregating shipment weight per trip and comparing to the truck's rated capacity flags overloads.

**Alt1:** Add dimensional capacity (`length/inches`, `volume/ft^3`) and check both weight and volume utilization with OR logic.

---

## Q14: Fuel consumption relation to miles driven

**Schema:** `fuel_logs(trip_id, gallons, cost_per_gallon), trips(trip_id, miles)`

```sql
-- Oracle
SELECT
    t.miles,
    f.gallons,
    ROUND(f.gallons / NULLIF(t.miles, 0), 3) AS gallons_per_mile,
    ROUND(t.miles    / NULLIF(f.gallons, 0), 1) AS miles_per_gallon
FROM fuel_logs f
JOIN trips t ON t.trip_id = f.trip_id;
```

**Explanation:** Simple ratio calculation; MPG and GPM are complementary efficiency views.

**Alt1:** Aggregate by truck_id or month to spot fleet-wide trends instead of per-trip granularity.

---

## Q15: Return freight — trucks coming back empty (no return shipment)

**Schema:** `trucks(truck_id), trips(trip_id, truck_id, route_id, arrival_at), routes(route_id, origin, destination)`

```sql
-- MySQL 8+
WITH outbound AS (
    SELECT t.truck_id, t.arrival_at AS outbound_arrival,
           r.origin, r.destination
    FROM trips t
    JOIN routes r ON r.route_id = t.route_id
),
return_check AS (
    SELECT
        o.truck_id,
        o.outbound_arrival,
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM trips t2
                JOIN routes r2 ON r2.route_id = t2.route_id
                WHERE t2.truck_id = o.truck_id
                  AND r2.origin = o.destination
                  AND r2.destination = o.origin
                  AND t2.departure_at > o.outbound_arrival
            ) THEN 'LOADED RETURN'
            ELSE 'EMPTY RETURN'
        END AS return_status
    FROM outbound o
)
SELECT return_status, COUNT(*) AS truck_count
FROM return_check
GROUP BY return_status;
```

**Explanation:** Checks whether a truck later made a reverse trip on the same lane; missing = empty deadhead.

---

## Q16: Milestone thresholds — P50 / P90 delivery time from pickup to delivered

**Schema:** `waybill_events(event_id, shipment_id, status, event_time)`

```sql
-- PostgreSQL
WITH milestones AS (
    SELECT
        shipment_id,
        MIN(CASE WHEN status = 'PICKUP'    THEN event_time END) AS pickup_at,
        MIN(CASE WHEN status = 'DELIVERED'  THEN event_time END) AS delivered_at
    FROM waybill_events
    GROUP BY shipment_id
)
SELECT
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (delivered_at - pickup_at))) / 86400.0 AS p50_days,
    PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (delivered_at - pickup_at))) / 86400.0 AS p90_days
FROM milestones
WHERE pickup_at IS NOT NULL AND delivered_at IS NOT NULL;
```

**Explanation:** Conditional aggregation pivots milestone rows into columns; `PERCENTILE_CONT` gives interpolated percentiles.

**Alt1:** For exact percentile (no interpolation), use `PERCENTILE_DISC(0.9)` or manually compute via `NTILE(100)` and label rank-90 buckets.

---

## Q17: Event funnel per shipment — which shipments stall at which milestone

**Schema:** `waybill_events(event_id, shipment_id, status, event_time)`

```sql
-- MySQL 8+
WITH funnel AS (
    SELECT
        shipment_id,
        MAX(CASE WHEN status = 'PICKUP'      THEN event_time END) AS pickup,
        MAX(CASE WHEN status = 'IN_TRANSIT'   THEN event_time END) AS in_transit,
        MAX(CASE WHEN status = 'ARRIVED_HUB'  THEN event_time END) AS arrived_hub,
        MAX(CASE WHEN status = 'OUT_FOR_DELIVERY' THEN event_time END) AS out_for_delivery,
        MAX(CASE WHEN status = 'DELIVERED'    THEN event_time END) AS delivered
    FROM waybill_events
    GROUP BY shipment_id
)
SELECT
    shipment_id,
    CASE
        WHEN delivered IS NOT NULL             THEN 'COMPLETED'
        WHEN out_for_delivery IS NOT NULL      THEN 'STALLED_OUT_FOR_DELIVERY'
        WHEN arrived_hub IS NOT NULL           THEN 'STALLED_ARRIVED_HUB'
        WHEN in_transit IS NOT NULL            THEN 'STALLED_IN_TRANSIT'
        WHEN pickup IS NOT NULL                THEN 'STALLED_PICKUP'
        ELSE 'NO_EVENTS'
    END AS funnel_stage
FROM funnel;
```

**Explanation:** Each milestone is pivoted; the first missing one identifies the bottleneck stage.

**Alt1:** Use `PERCENT_RANK()` over `stages_remaining` to compute the fraction of shipments stalled at each stage.

---

## Q18: Duplicate event detection — same shipment, same status, same timestamp

**Schema:** `waybill_events(event_id, shipment_id, status, event_time)`

```sql
SELECT
    shipment_id,
    status,
    event_time,
    COUNT(*) AS duplicate_count
FROM waybill_events
GROUP BY shipment_id, status, event_time
HAVING COUNT(*) > 1;
```

**Explanation:** A GROUP BY on the natural key with HAVING > 1 surfaces exact duplicates.

**Alt1:** Use `ROW_NUMBER()` partitioned by `(shipment_id, status, event_time)` and filter `rn > 1` to retain the row IDs for deletion.

---

## Q19: Out-of-sequence event detection — DELIVERED before PICKUP

**Schema:** `waybill_events(event_id, shipment_id, status, event_time)`

```sql
-- PostgreSQL
WITH extremes AS (
    SELECT
        shipment_id,
        MIN(CASE WHEN status = 'PICKUP'   THEN event_time END) AS pickup_at,
        MIN(CASE WHEN status = 'DELIVERED' THEN event_time END) AS delivered_at
    FROM waybill_events
    GROUP BY shipment_id
)
SELECT shipment_id, pickup_at, delivered_at
FROM extremes
WHERE delivered_at < pickup_at;
```

**Explanation:** Comparing the earliest timestamps of two milestones catches inverted sequences.

**Alt1:** Use `LAG(status)` over event_time ordering to flag any case where a 'DELIVERED' row precedes 'PICKUP' chronologically.

**Alt2 (SQL Server):** Use `FIRST_VALUE(event_time)` partitioned per shipment ordered by sequence, then compare statuses pairwise without a self-join.

---

## Q20: Live position — last known event per active truck

**Schema:** `waybill_events(event_id, shipment_id, truck_id, event_time, status, location)`

```sql
-- SQL Server
WITH ranked AS (
    SELECT
        w.truck_id,
        w.location,
        w.event_time,
        w.status,
        ROW_NUMBER() OVER (PARTITION BY w.truck_id ORDER BY w.event_time DESC) AS rn
    FROM waybill_events w
    JOIN shipments s ON s.shipment_id = w.shipment_id
    WHERE s.status IN ('IN_TRANSIT', 'OUT_FOR_DELIVERY')
)
SELECT truck_id, location, event_time, status
FROM ranked
WHERE rn = 1;
```

**Explanation:** `ROW_NUMBER` picks the most recent event per truck; filtering to active shipments excludes parked trucks.

---

## Q21: Drop-off cadence — average hours between consecutive deliveries per driver

**Schema:** `waybill_events(event_id, shipment_id, truck_id, status, event_time), trips(trip_id, truck_id, driver_id)`

```sql
-- MySQL 8+
WITH delivered_events AS (
    SELECT
        w.shipment_id,
        w.truck_id,
        w.event_time,
        t.driver_id,
        LEAD(w.event_time) OVER (PARTITION BY w.truck_id ORDER BY w.event_time) AS next_delivered
    FROM waybill_events w
    JOIN trips t ON t.truck_id = w.truck_id
    WHERE w.status = 'DELIVERED'
)
SELECT
    driver_id,
    ROUND(AVG(TIMESTAMPDIFF(HOUR, event_time, next_delivered)), 1) AS avg_hours_between
FROM delivered_events
WHERE next_delivered IS NOT NULL
GROUP BY driver_id;
```

**Explanation:** `LEAD` finds the next delivery event on the same truck; averaging the gaps gives cadence.

---

## Q22: Delivery density — identify clusters of deliveries by postal prefix

**Schema:** `shipments(shipment_id, destination, delivered_at)`

```sql
-- PostgreSQL
SELECT
    LEFT(destination, 3) AS postal_prefix,
    COUNT(*)             AS deliveries,
    MIN(delivered_at)    AS first_delivery,
    MAX(delivered_at)    AS last_delivery,
    EXTRACT(DAY FROM MAX(delivered_at) - MIN(delivered_at)) + 1 AS span_days,
    ROUND(COUNT(*) * 1.0 / (EXTRACT(DAY FROM MAX(delivered_at) - MIN(delivered_at)) + 1), 1) AS daily_density
FROM shipments
WHERE delivered_at IS NOT NULL
GROUP BY postal_prefix
ORDER BY daily_density DESC;
```

**Explanation:** Grouping by a coarse geographic key and dividing by the time span yields a delivery density metric.

**Alt1:** Use PostGIS `ST_ClusterDBSCAN` on lat/lng coordinates for true spatial clustering.

---

## Q23: Inventory restock triggered by depletion — SKUs below reorder point

**Schema:** `inventory(sku, warehouse_id, qty_on_hand, reorder_point, last_restock_at)`

```sql
SELECT
    sku,
    warehouse_id,
    qty_on_hand,
    reorder_point,
    reorder_point - qty_on_hand AS shortfall,
    last_restock_at
FROM inventory
WHERE qty_on_hand <= reorder_point
ORDER BY shortfall DESC;
```

**Explanation:** A simple threshold filter surfaces every SKU needing replenishment.

**Alt1:** Add a `demand_rate` column and compute `days_until_stockout = qty_on_hand / daily_demand` to prioritize by urgency.

---

## Q24: Days of supply per SKU

**Schema:** `inventory(sku, warehouse_id, qty_on_hand, last_restock_at)`

```sql
-- Oracle
WITH demand AS (
    SELECT
        sku,
        warehouse_id,
        qty_on_hand,
        NVL(qty_on_hand / NULLIF(
            EXTRACT(DAY FROM SYSDATE - last_restock_at), 0), 9999
        ) AS days_of_supply
    FROM inventory
)
SELECT sku, warehouse_id, ROUND(days_of_supply, 1) AS days_of_supply
FROM demand
ORDER BY days_of_supply ASC;
```

**Explanation:** Dividing current stock by the implied daily consumption rate (stock consumed / days since restock) gives remaining supply days.

**Alt1:** Use a `demand_forecast` table instead of historical consumption for forward-looking supply days.

---

## Q25: Warehouse transfer frequency — inter-warehouse moves in last 90 days

**Schema:** `waybill_events(event_id, shipment_id, location, status, event_time), warehouses(warehouse_id, name)`

```sql
-- MySQL 8+
SELECT
    w_from.name AS from_warehouse,
    w_to.name   AS to_warehouse,
    COUNT(*)    AS transfer_count
FROM waybill_events e1
JOIN waybill_events e2
    ON e1.shipment_id = e2.shipment_id
   AND e2.event_time > e1.event_time
   AND e2.event_time <= DATE_SUB(NOW(), INTERVAL 90 DAY)
JOIN warehouses w_from ON w_from.name = e1.location
JOIN warehouses w_to   ON w_to.name   = e2.location
WHERE e1.status = 'DEPARTED_WAREHOUSE'
  AND e2.status = 'ARRIVED_WAREHOUSE'
  AND e1.location <> e2.location
  AND e1.event_time >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY w_from.name, w_to.name
ORDER BY transfer_count DESC;
```

**Explanation:** Pairs consecutive warehouse events per shipment to count inter-facility transfers.

**Alt1:** Use a self-join on `shipment_id` with `LEAD(location)` window function for a single-pass approach.

---

## Q26: Next available truck scheduling — earliest truck free after its last trip

**Schema:** `trucks(truck_id, capacity), trips(trip_id, truck_id, arrival_at)`

```sql
-- PostgreSQL
WITH last_trip AS (
    SELECT
        truck_id,
        MAX(arrival_at) AS last_arrival
    FROM trips
    GROUP BY truck_id
)
SELECT
    t.truck_id,
    t.capacity,
    COALESCE(lt.last_arrival, '1970-01-01') AS available_after
FROM trucks t
LEFT JOIN last_trip lt ON lt.truck_id = t.truck_id
ORDER BY available_after ASC;
```

**Explanation:** The most recent `arrival_at` per truck marks when it becomes available; `COALESCE` handles trucks with no trips.

**Alt1:** Exclude trucks currently assigned to a live trip (`WHERE NOT EXISTS` on waybill events in the last N hours) before ranking availability.

---

## Q27: Co-route optimization candidates — two shipments share origin + direction

**Schema:** `shipments(shipment_id, origin, destination, created_at)`

```sql
SELECT
    a.shipment_id AS shipment_1,
    b.shipment_id AS shipment_2,
    a.origin,
    a.destination,
    GREATEST(a.created_at, b.created_at) AS combined_ready_at
FROM shipments a
JOIN shipments b
    ON a.origin      = b.origin
   AND a.destination  = b.destination
   AND a.shipment_id < b.shipment_id
   AND ABS(DATEDIFF(day, a.created_at, b.created_at)) <= 2
ORDER BY a.origin, a.destination;
```

**Explanation:** Self-join on same lane with a time window flag candidate shipments for consolidation.

**Alt1:** Add weight/capacity columns and filter `a.weight + b.weight <= truck_capacity` to ensure the consolidation is feasible.

**Alt2 (SQL Server):** Use `APPROX_COUNT_DISTINCT` lane-day combos for large fleets to estimate consolidation gain without exact counting.

---

## Q28: Exception rates by reason code

**Schema:** `exceptions(exception_id, shipment_id, reason_code, logged_at, resolved_at), shipments(shipment_id)`

```sql
-- SQL Server
SELECT
    e.reason_code,
    COUNT(*)                                          AS exception_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM shipments), 2) AS pct_of_all_shipments,
    AVG(DATEDIFF(HOUR, e.logged_at, e.resolved_at))  AS avg_resolution_hours
FROM exceptions e
GROUP BY e.reason_code
ORDER BY exception_count DESC;
```

**Explanation:** Aggregating exceptions by reason code with a subquery denominator gives fleet-wide exception rates.

---

## Q29: Seasonality of shipping volume — monthly trend with YoY comparison

**Schema:** `shipments(shipment_id, created_at)`

```sql
-- MySQL 8+
WITH monthly AS (
    SELECT
        DATE_FORMAT(created_at, '%Y-%m') AS month,
        COUNT(*)                         AS volume
    FROM shipments
    GROUP BY DATE_FORMAT(created_at, '%Y-%m')
)
SELECT
    month,
    volume,
    LAG(volume, 12) OVER (ORDER BY month) AS prev_year_volume,
    ROUND(100.0 * (volume - LAG(volume, 12) OVER (ORDER BY month))
          / NULLIF(LAG(volume, 12) OVER (ORDER BY month), 0), 1) AS yoy_change_pct
FROM monthly
ORDER BY month;
```

**Explanation:** `LAG(volume, 12)` aligns the same month from the previous year for YoY comparison.

**Alt1:** Compute a 12-month rolling total window (`ROWS BETWEEN 11 PRECEDING AND CURRENT ROW`) to smooth seasonality into an annualized trend.

---

## Q30: Real-time dashboard — last event per active shipment

**Schema:** `waybill_events(event_id, shipment_id, event_time, status, location), shipments(shipment_id, status)`

```sql
-- PostgreSQL
WITH ranked AS (
    SELECT
        w.shipment_id,
        w.event_time,
        w.status,
        w.location,
        ROW_NUMBER() OVER (PARTITION BY w.shipment_id ORDER BY w.event_time DESC) AS rn
    FROM waybill_events w
    JOIN shipments s ON s.shipment_id = w.shipment_id
    WHERE s.status NOT IN ('DELIVERED', 'CANCELLED')
)
SELECT shipment_id, event_time, status, location
FROM ranked
WHERE rn = 1;
```

**Explanation:** Window function picks the freshest event per active shipment for a live dashboard tile.

**Alt1:** Materialize as a PostgreSQL materialized view refreshed via `REFRESH MATERIALIZED VIEW CONCURRENTLY` for sub-second reads.

---

## Q31: Weight-band pricing — shipments bucketed by weight tiers

**Schema:** `shipments(shipment_id, weight, cost)`

```sql
-- Oracle
SELECT
    CASE
        WHEN weight < 100  THEN 'LIGHT'
        WHEN weight < 500  THEN 'MEDIUM'
        WHEN weight < 1000 THEN 'HEAVY'
        ELSE 'FREIGHT'
    END AS weight_band,
    COUNT(*)                        AS shipment_count,
    ROUND(AVG(cost), 2)            AS avg_cost,
    ROUND(AVG(cost / NULLIF(weight, 0)), 4) AS cost_per_lb
FROM shipments
GROUP BY CASE
        WHEN weight < 100  THEN 'LIGHT'
        WHEN weight < 500  THEN 'MEDIUM'
        WHEN weight < 1000 THEN 'HEAVY'
        ELSE 'FREIGHT'
    END
ORDER BY avg_cost DESC;
```

**Explanation:** CASE expression creates weight tiers; aggregating cost per tier reveals pricing structure.

**Alt1:** Use Oracle's `WIDTH_BUCKET(weight, 0, 1000, 4)` to generate buckets programmatically instead of hand-coding CASE branches.

---

## Q32: Rolling 7-day shipment volume

**Schema:** `shipments(shipment_id, created_at)`

```sql
-- SQL Server
SELECT
    CAST(created_at AS DATE) AS ship_date,
    COUNT(*)                 AS daily_volume,
    SUM(COUNT(*)) OVER (ORDER BY CAST(created_at AS DATE)
                        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7day
FROM shipments
GROUP BY CAST(created_at AS DATE);
```

**Explanation:** A window frame of 7 rows computes a running 7-day sum of daily shipment counts.

---

## Q33: Shipment age analysis — open shipments older than SLA

**Schema:** `shipments(shipment_id, origin, destination, status, created_at, delivered_at)`

```sql
SELECT
    shipment_id,
    origin,
    destination,
    status,
    created_at,
    DATEDIFF(day, created_at, GETDATE()) AS age_days
FROM shipments
WHERE delivered_at IS NULL
  AND DATEDIFF(day, created_at, GETDATE()) > 5
ORDER BY age_days DESC;
```

**Explanation:** Undelivered shipments exceeding 5 days are flagged for escalation.

---

## Q34: Warehouse throughput — shipments processed per day

**Schema:** `waybill_events(event_id, shipment_id, location, event_time, status), warehouses(warehouse_id, name)`

```sql
-- PostgreSQL
SELECT
    w.name AS warehouse_name,
    DATE(e.event_time)       AS event_date,
    COUNT(DISTINCT e.shipment_id) AS shipments_processed
FROM waybill_events e
JOIN warehouses w ON w.name = e.location
WHERE e.status IN ('ARRIVED_WAREHOUSE', 'DEPARTED_WAREHOUSE')
GROUP BY w.name, DATE(e.event_time)
ORDER BY w.name, event_date;
```

**Explanation:** Counting distinct shipments touching each warehouse per day measures facility throughput.

---

## Q35: Driver of the month — most deliveries in current month

**Schema:** `trips(trip_id, driver_id), shipments(shipment_id, trip_id, status, delivered_at)`

```sql
-- MySQL 8+
SELECT
    t.driver_id,
    COUNT(*) AS deliveries
FROM trips t
JOIN shipments s ON s.trip_id = t.trip_id
WHERE s.status = 'DELIVERED'
  AND MONTH(s.delivered_at) = MONTH(CURRENT_DATE())
  AND YEAR(s.delivered_at)  = YEAR(CURRENT_DATE())
GROUP BY t.driver_id
ORDER BY deliveries DESC
LIMIT 1;
```

**Explanation:** Filtering to the current calendar month and ranking by count identifies the top performer.

---

## Q36: Delayed shipment root-cause — status with longest average dwell

**Schema:** `waybill_events(event_id, shipment_id, status, event_time)`

```sql
-- PostgreSQL
WITH dwell AS (
    SELECT
        shipment_id,
        status,
        event_time - LAG(event_time) OVER (PARTITION BY shipment_id ORDER BY event_time) AS dwell_time
    FROM waybill_events
)
SELECT
    status,
    ROUND(AVG(EXTRACT(EPOCH FROM dwell_time)) / 3600.0, 1) AS avg_dwell_hours,
    ROUND(MAX(EXTRACT(EPOCH FROM dwell_time)) / 3600.0, 1) AS max_dwell_hours,
    COUNT(*) AS occurrences
FROM dwell
WHERE dwell_time IS NOT NULL
GROUP BY status
ORDER BY avg_dwell_hours DESC;
```

**Explanation:** Averaging dwell time per status identifies the process bottleneck causing delays.

---

## Q37: Multi-stop route profitability

**Schema:** `trips(trip_id, route_id, miles), routes(route_id, origin, destination), shipments(shipment_id, trip_id, cost, weight)`

```sql
-- SQL Server
SELECT
    t.trip_id,
    r.origin,
    r.destination,
    t.miles,
    COUNT(s.shipment_id) AS stops,
    SUM(s.cost)          AS revenue,
    SUM(s.weight)        AS total_weight,
    ROUND(SUM(s.cost) / NULLIF(t.miles, 0), 2) AS revenue_per_mile
FROM trips t
JOIN routes r    ON r.route_id = t.route_id
JOIN shipments s ON s.trip_id  = t.trip_id
GROUP BY t.trip_id, r.origin, r.destination, t.miles
HAVING COUNT(s.shipment_id) >= 3
ORDER BY revenue_per_mile DESC;
```

**Explanation:** Trips with 3+ stops are multi-stop routes; revenue per mile measures their profitability.

---

## Q38: SLA breach cost estimation

**Schema:** `shipments(shipment_id, cost, created_at, delivered_at), exceptions(exception_id, shipment_id, reason_code)`

```sql
-- Oracle
WITH sla_breach AS (
    SELECT
        s.shipment_id,
        s.cost,
        EXTRACT(DAY FROM s.delivered_at - s.created_at) AS delivery_days,
        EXTRACT(DAY FROM s.delivered_at - s.created_at) - 3 AS days_overdue
    FROM shipments s
    WHERE s.delivered_at IS NOT NULL
      AND EXTRACT(DAY FROM s.delivered_at - s.created_at) > 3
)
SELECT
    b.shipment_id,
    b.cost,
    b.days_overdue,
    b.days_overdue * b.cost * 0.05 AS estimated_penalty
FROM sla_breach b
ORDER BY estimated_penalty DESC;
```

**Explanation:** A hypothetical 5% per-day penalty multiplied by cost and overdue days quantifies breach exposure.

---

## Q39: Inter-warehouse distance matrix — shipment count between every warehouse pair

**Schema:** `waybill_events(event_id, shipment_id, location, status)`

```sql
-- PostgreSQL
SELECT
    e1.location AS origin_wh,
    e2.location AS dest_wh,
    COUNT(DISTINCT e1.shipment_id) AS shipment_count
FROM waybill_events e1
JOIN waybill_events e2
    ON e1.shipment_id = e2.shipment_id
   AND e2.event_time > e1.event_time
WHERE e1.status = 'DEPARTED_WAREHOUSE'
  AND e2.status = 'ARRIVED_WAREHOUSE'
GROUP BY e1.location, e2.location
ORDER BY shipment_count DESC;
```

**Explanation:** Pairing departure and arrival events per shipment builds an origin-destination frequency matrix.

---

## Q40: Shipment weight histogram — 50-lb buckets

**Schema:** `shipments(shipment_id, weight)`

```sql
-- MySQL 8+
SELECT
    CONCAT(FLOOR(weight / 50) * 50, '-', FLOOR(weight / 50) * 50 + 49, ' lb') AS weight_bucket,
    COUNT(*) AS shipment_count
FROM shipments
GROUP BY FLOOR(weight / 50)
ORDER BY FLOOR(weight / 50);
```

**Explanation:** `FLOOR(weight/50)*50` creates uniform 50-lb bins for a weight distribution histogram.

---

## Q41: Churned lane detection — routes with declining volume (3-month trend)

**Schema:** `shipments(shipment_id, origin, destination, created_at)`

```sql
-- SQL Server
WITH monthly_lane AS (
    SELECT
        origin,
        destination,
        FORMAT(created_at, 'yyyy-MM') AS month,
        COUNT(*) AS volume
    FROM shipments
    GROUP BY origin, destination, FORMAT(created_at, 'yyyy-MM')
),
ranked AS (
    SELECT
        *,
        LAG(volume, 1) OVER (PARTITION BY origin, destination ORDER BY month) AS prev_month,
        LAG(volume, 2) OVER (PARTITION BY origin, destination ORDER BY month) AS two_months_ago
    FROM monthly_lane
)
SELECT origin, destination, month, volume, prev_month, two_months_ago
FROM ranked
WHERE volume < prev_month
  AND prev_month < two_months_ago
  AND two_months_ago > 5
ORDER BY origin, destination, month;
```

**Explanation:** Two `LAG` offsets detect three consecutive months of declining volume on a lane.

---

## Q42: Cost anomaly detection — shipment cost > 2 standard deviations above route mean

**Schema:** `shipments(shipment_id, origin, destination, cost)`

```sql
-- PostgreSQL
WITH route_stats AS (
    SELECT
        origin,
        destination,
        AVG(cost)   AS mean_cost,
        STDDEV(cost) AS stddev_cost
    FROM shipments
    GROUP BY origin, destination
)
SELECT
    s.shipment_id,
    s.origin,
    s.destination,
    s.cost,
    rs.mean_cost,
    ROUND((s.cost - rs.mean_cost) / NULLIF(rs.stddev_cost, 0), 2) AS z_score
FROM shipments s
JOIN route_stats rs
    ON rs.origin = s.origin
   AND rs.destination = s.destination
WHERE (s.cost - rs.mean_cost) / NULLIF(rs.stddev_cost, 0) > 2
ORDER BY z_score DESC;
```

**Explanation:** Z-score > 2 flags a shipment whose cost is an outlier on its route.

---

## Q43: Peak-hour analysis — shipments created by hour of day

**Schema:** `shipments(shipment_id, created_at)`

```sql
-- MySQL 8+
SELECT
    HOUR(created_at) AS hour_of_day,
    COUNT(*)         AS shipments_created,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM shipments), 1) AS pct
FROM shipments
GROUP BY HOUR(created_at)
ORDER BY hour_of_day;
```

**Explanation:** Extracting the hour component reveals intra-day demand patterns.

---

## Q44: Truck idling time — hours between trip arrival and next departure

**Schema:** `trips(trip_id, truck_id, arrival_at, departure_at)`

```sql
-- PostgreSQL
WITH trip_gaps AS (
    SELECT
        truck_id,
        departure_at,
        arrival_at,
        LEAD(departure_at) OVER (PARTITION BY truck_id ORDER BY departure_at) AS next_departure
    FROM trips
)
SELECT
    truck_id,
    ROUND(AVG(EXTRACT(EPOCH FROM (next_departure - arrival_at)) / 3600.0), 1) AS avg_idle_hours,
    ROUND(MAX(EXTRACT(EPOCH FROM (next_departure - arrival_at)) / 3600.0), 1) AS max_idle_hours
FROM trip_gaps
WHERE next_departure IS NOT NULL
GROUP BY truck_id;
```

**Explanation:** The gap between arrival and next departure is idle time; averaging per truck surfaces under-utilization.

---

## Q45: On-time rate by carrier (via shipments.carrier_id)

**Schema:** `shipments(shipment_id, carrier_id, created_at, delivered_at)`

```sql
-- SQL Server
SELECT
    carrier_id,
    COUNT(*) AS total,
    SUM(CASE WHEN DATEDIFF(day, created_at, delivered_at) <= 3 THEN 1 ELSE 0 END) AS on_time,
    ROUND(100.0 * SUM(CASE WHEN DATEDIFF(day, created_at, delivered_at) <= 3 THEN 1 ELSE 0 END) / COUNT(*), 1) AS on_time_pct
FROM shipments
WHERE delivered_at IS NOT NULL
GROUP BY carrier_id
ORDER BY on_time_pct DESC;
```

**Explanation:** Carrier-level on-time percentages enable vendor scorecard comparisons.

---

## Q46: Cost per pound by route

**Schema:** `shipments(shipment_id, origin, destination, weight, cost)`

```sql
SELECT
    origin,
    destination,
    ROUND(SUM(cost) / NULLIF(SUM(weight), 0), 4) AS cost_per_lb,
    COUNT(*) AS shipment_count
FROM shipments
GROUP BY origin, destination
HAVING COUNT(*) >= 10
ORDER BY cost_per_lb DESC;
```

**Explanation:** Weight-normalized cost comparison across routes eliminates the bias of varying shipment sizes.

---

## Q47: Late delivery rate trend — weekly rolling average

**Schema:** `shipments(shipment_id, created_at, delivered_at)`

```sql
-- MySQL 8+
WITH weekly_late AS (
    SELECT
        DATE_FORMAT(created_at, '%Y-%u') AS week,
        COUNT(*) AS total,
        SUM(CASE WHEN DATEDIFF(delivered_at, created_at) > 5 THEN 1 ELSE 0 END) AS late
    FROM shipments
    WHERE delivered_at IS NOT NULL
    GROUP BY DATE_FORMAT(created_at, '%Y-%u')
)
SELECT
    week,
    late,
    total,
    ROUND(100.0 * late / total, 1) AS late_pct,
    ROUND(AVG(100.0 * late / total) OVER (ORDER BY week ROWS BETWEEN 3 PRECEDING AND CURRENT ROW), 1) AS rolling_4wk_avg
FROM weekly_late
ORDER BY week;
```

**Explanation:** A 4-week rolling average smooths out weekly noise in the late-delivery rate.

---

## Q48: Return-to-sender rate by origin warehouse

**Schema:** `shipments(shipment_id, origin, status)`

```sql
-- Oracle
SELECT
    origin,
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'RETURNED' THEN 1 ELSE 0 END) AS returns,
    ROUND(100.0 * SUM(CASE WHEN status = 'RETURNED' THEN 1 ELSE 0 END) / COUNT(*), 2) AS return_pct
FROM shipments
GROUP BY origin
ORDER BY return_pct DESC;
```

**Explanation:** Return rate per origin warehouse flags packaging or labeling quality issues.

---

## Q49: Transit time consistency — standard deviation of delivery duration per route

**Schema:** `shipments(shipment_id, origin, destination, created_at, delivered_at)`

```sql
-- PostgreSQL
SELECT
    origin,
    destination,
    COUNT(*)                            AS shipments,
    ROUND(AVG(DATEDIFF(day, created_at, delivered_at)), 2)   AS avg_days,
    ROUND(STDDEV(DATEDIFF(day, created_at, delivered_at)), 2) AS stddev_days,
    ROUND(STDDEV(DATEDIFF(day, created_at, delivered_at))
          / NULLIF(AVG(DATEDIFF(day, created_at, delivered_at)), 0), 3) AS coeff_of_variation
FROM shipments
WHERE delivered_at IS NOT NULL
GROUP BY origin, destination
HAVING COUNT(*) >= 5
ORDER BY coeff_of_variation DESC;
```

**Explanation:** Coefficient of variation (stddev/mean) measures transit-time predictability per route.

---

## Q50: Hub-and-spoke connectivity — how many destinations each hub serves

**Schema:** `shipments(shipment_id, origin, destination), warehouses(warehouse_id, name, region)`

```sql
-- MySQL 8+
SELECT
    w.name AS hub,
    w.region,
    COUNT(DISTINCT s.destination) AS destinations_served,
    COUNT(*) AS total_shipments
FROM shipments s
JOIN warehouses w ON w.name = s.origin
GROUP BY w.name, w.region
ORDER BY destinations_served DESC;
```

**Explanation:** Distinct destination count per origin warehouse quantifies hub reach.

---

## Q51: Shipment consolidation score — percentage of shipments that could share a truck

**Schema:** `shipments(shipment_id, origin, destination, weight, created_at)`

```sql
-- PostgreSQL
WITH paired AS (
    SELECT
        a.shipment_id,
        a.origin,
        a.destination,
        a.weight,
        a.created_at,
        COUNT(*) OVER (PARTITION BY a.origin, a.destination,
                       DATE_TRUNC('day', a.created_at)) AS lane_daily_count
    FROM shipments a
)
SELECT
    COUNT(*) FILTER (WHERE lane_daily_count >= 2) AS consolidatable,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE lane_daily_count >= 2) / COUNT(*), 1) AS consolidation_pct
FROM paired;
```

**Explanation:** When 2+ shipments share a lane and day, they could theoretically consolidate onto one truck.

---

## Q52: Maximum consecutive late deliveries per driver — streak detection

**Schema:** `trips(trip_id, driver_id), shipments(shipment_id, trip_id, created_at, delivered_at)`

```sql
-- SQL Server
WITH driver_late AS (
    SELECT
        t.driver_id,
        s.shipment_id,
        s.delivered_at,
        CASE WHEN DATEDIFF(day, s.created_at, s.delivered_at) > 5 THEN 1 ELSE 0 END AS is_late
    FROM trips t
    JOIN shipments s ON s.trip_id = t.trip_id
    WHERE s.delivered_at IS NOT NULL
),
streaks AS (
    SELECT
        driver_id,
        shipment_id,
        delivered_at,
        is_late,
        ROW_NUMBER() OVER (PARTITION BY driver_id ORDER BY delivered_at) -
        ROW_NUMBER() OVER (PARTITION BY driver_id, is_late ORDER BY delivered_at) AS grp
    FROM driver_late
)
SELECT
    driver_id,
    MAX(streak_len) AS max_late_streak
FROM (
    SELECT driver_id, grp, COUNT(*) AS streak_len
    FROM streaks
    WHERE is_late = 1
    GROUP BY driver_id, grp
) sub
GROUP BY driver_id
HAVING MAX(streak_len) >= 3
ORDER BY max_late_streak DESC;
```

**Explanation:** The classic islands-and-gaps technique identifies consecutive late-delivery streaks per driver.

---

## Q53: Seasonal capacity planning — average weight per trip by month

**Schema:** `trips(trip_id, departure_at), shipments(shipment_id, trip_id, weight)`

```sql
-- Oracle
SELECT
    TO_CHAR(t.departure_at, 'YYYY-MM') AS month,
    COUNT(DISTINCT t.trip_id) AS trip_count,
    ROUND(AVG(trip_w.total_weight), 1) AS avg_weight_per_trip,
    MAX(trip_w.total_weight) AS max_trip_weight
FROM trips t
JOIN (
    SELECT trip_id, SUM(weight) AS total_weight
    FROM shipments
    GROUP BY trip_id
) trip_w ON trip_w.trip_id = t.trip_id
GROUP BY TO_CHAR(t.departure_at, 'YYYY-MM')
ORDER BY month;
```

**Explanation:** Monthly aggregation of per-trip weight reveals seasonal capacity demands.

---

## Q54: FIFO shipment processing — oldest shipment delivered first per truck

**Schema:** `shipments(shipment_id, trip_id, created_at, delivered_at), trips(trip_id, truck_id)`

```sql
-- MySQL 8+
WITH ranked AS (
    SELECT
        s.shipment_id,
        t.truck_id,
        s.created_at,
        s.delivered_at,
        ROW_NUMBER() OVER (PARTITION BY t.truck_id ORDER BY s.created_at) AS pickup_seq,
        ROW_NUMBER() OVER (PARTITION BY t.truck_id ORDER BY s.delivered_at) AS delivery_seq
    FROM shipments s
    JOIN trips t ON t.trip_id = s.trip_id
    WHERE s.delivered_at IS NOT NULL
)
SELECT
    truck_id,
    COUNT(*) AS violations,
    SUM(CASE WHEN pickup_seq <> delivery_seq THEN 1 ELSE 0 END) AS fifo_breaches
FROM ranked
GROUP BY truck_id
HAVING SUM(CASE WHEN pickup_seq <> delivery_seq THEN 1 ELSE 0 END) > 0;
```

**Explanation:** Comparing pickup order vs delivery order via `ROW_NUMBER` detects FIFO violations.

---

## Q55: Shipment velocity — moving average of daily shipments over 30 days

**Schema:** `shipments(shipment_id, created_at)`

```sql
-- PostgreSQL
WITH daily AS (
    SELECT
        DATE(created_at) AS ship_date,
        COUNT(*) AS volume
    FROM shipments
    GROUP BY DATE(created_at)
)
SELECT
    ship_date,
    volume,
    ROUND(AVG(volume) OVER (ORDER BY ship_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW), 1) AS ma_30d
FROM daily
ORDER BY ship_date;
```

**Explanation:** A 30-row windowed average smooths daily shipment volume into a trend line.

---

## Q56: Distance-based pricing tier compliance

**Schema:** `shipments(shipment_id, origin, destination, cost), routes(route_id, origin, destination, distance_miles)`

```sql
-- SQL Server
SELECT
    s.shipment_id,
    r.distance_miles,
    s.cost,
    ROUND(s.cost / NULLIF(r.distance_miles, 0), 4) AS cost_per_mile,
    CASE
        WHEN r.distance_miles < 100  AND s.cost / NULLIF(r.distance_miles, 0) > 2.5 THEN 'OVERPRICED'
        WHEN r.distance_miles BETWEEN 100 AND 500 AND s.cost / NULLIF(r.distance_miles, 0) > 1.8 THEN 'OVERPRICED'
        WHEN r.distance_miles > 500  AND s.cost / NULLIF(r.distance_miles, 0) > 1.2 THEN 'OVERPRICED'
        ELSE 'OK'
    END AS pricing_status
FROM shipments s
JOIN routes r ON r.origin = s.origin AND r.destination = s.destination;
```

**Explanation:** Distance bands have different expected cost-per-mile rates; violations indicate pricing errors.

---

## Q57: Warehouse inventory turn rate

**Schema:** `inventory(sku, warehouse_id, qty_on_hand, last_restock_at), shipments(shipment_id, destination, delivered_at)`

```sql
-- MySQL 8+
WITH consumption AS (
    SELECT
        destination AS warehouse_id,
        COUNT(*) AS shipments_out,
        MIN(delivered_at) AS first_delivered,
        MAX(delivered_at) AS last_delivered
    FROM shipments
    WHERE delivered_at IS NOT NULL
    GROUP BY destination
)
SELECT
    i.warehouse_id,
    i.sku,
    i.qty_on_hand,
    COALESCE(c.shipments_out, 0) AS shipments_out_90d,
    ROUND(COALESCE(c.shipments_out, 0) * 1.0 / NULLIF(i.qty_on_hand, 0), 2) AS turn_ratio
FROM inventory i
LEFT JOIN consumption c ON c.warehouse_id = i.warehouse_id
WHERE c.last_delivered >= DATE_SUB(NOW(), INTERVAL 90 DAY)
   OR c.warehouse_id IS NULL;
```

**Explanation:** Turn ratio (outbound shipments / on-hand qty) measures how fast inventory moves through a warehouse.

---

## Q58: Late delivery prediction feature — historical late rate per lane-month

**Schema:** `shipments(shipment_id, origin, destination, created_at, delivered_at)`

```sql
-- PostgreSQL
WITH lane_month AS (
    SELECT
        origin,
        destination,
        DATE_TRUNC('month', created_at) AS month,
        COUNT(*) AS total,
        SUM(CASE WHEN delivered_at - created_at > INTERVAL '5 days' THEN 1 ELSE 0 END) AS late
    FROM shipments
    WHERE delivered_at IS NOT NULL
    GROUP BY origin, destination, DATE_TRUNC('month', created_at)
)
SELECT
    origin,
    destination,
    ROUND(AVG(100.0 * late / total), 1) AS avg_late_rate_pct,
    ROUND(STDDEV(100.0 * late / total), 1) AS late_rate_volatility
FROM lane_month
GROUP BY origin, destination
HAVING COUNT(*) >= 3
ORDER BY avg_late_rate_pct DESC;
```

**Explanation:** Average and volatility of lane-level late rates feed into predictive models.

---

## Q59: Cost optimization — cheapest route between two hubs

**Schema:** `shipments(shipment_id, origin, destination, cost, weight)`

```sql
SELECT
    origin,
    destination,
    MIN(cost)          AS min_cost,
    MAX(cost)          AS max_cost,
    ROUND(AVG(cost), 2) AS avg_cost,
    ROUND(AVG(weight), 1) AS avg_weight
FROM shipments
WHERE origin = 'CHICAGO_HUB' AND destination = 'DALLAS_HUB'
GROUP BY origin, destination;
```

**Explanation:** Min/max/avg cost on a specific lane identifies the baseline for rate negotiations.

---

## Q60: Event sequence validation — count shipments with incomplete milestone chains

**Schema:** `waybill_events(event_id, shipment_id, status)`

```sql
-- Oracle
WITH expected AS (
    SELECT shipment_id,
           MAX(CASE WHEN status = 'PICKUP'           THEN 1 ELSE 0 END) AS has_pickup,
           MAX(CASE WHEN status = 'IN_TRANSIT'        THEN 1 ELSE 0 END) AS has_transit,
           MAX(CASE WHEN status = 'ARRIVED_HUB'       THEN 1 ELSE 0 END) AS has_hub,
           MAX(CASE WHEN status = 'OUT_FOR_DELIVERY'  THEN 1 ELSE 0 END) AS has_ofd,
           MAX(CASE WHEN status = 'DELIVERED'         THEN 1 ELSE 0 END) AS has_delivered
    FROM waybill_events
    GROUP BY shipment_id
)
SELECT
    SUM(CASE WHEN has_pickup = 0  THEN 1 ELSE 0 END) AS missing_pickup,
    SUM(CASE WHEN has_transit = 0 THEN 1 ELSE 0 END) AS missing_transit,
    SUM(CASE WHEN has_hub = 0     THEN 1 ELSE 0 END) AS missing_hub,
    SUM(CASE WHEN has_ofd = 0     THEN 1 ELSE 0 END) AS missing_ofd,
    SUM(CASE WHEN has_delivered = 0 THEN 1 ELSE 0 END) AS missing_delivered
FROM expected;
```

**Explanation:** Pivoting milestones into boolean columns and summing zeros counts shipments missing each milestone.

---

## Q61: Driver overtime detection — trips exceeding 11-hour drive limit

**Schema:** `trips(trip_id, driver_id, departure_at, arrival_at, miles)`

```sql
-- MySQL 8+
SELECT
    trip_id,
    driver_id,
    departure_at,
    arrival_at,
    TIMESTAMPDIFF(HOUR, departure_at, arrival_at) AS trip_hours,
    miles
FROM trips
WHERE TIMESTAMPDIFF(HOUR, departure_at, arrival_at) > 11
ORDER BY trip_hours DESC;
```

**Explanation:** Hours-of-service rules limit continuous duty; flagging trips over 11 hours identifies compliance risk.

---

## Q62: Shipment dwell time at each hub stop — P90 by hub

**Schema:** `waybill_events(event_id, shipment_id, location, status, event_time)`

```sql
-- PostgreSQL
WITH hub_dwell AS (
    SELECT
        w1.shipment_id,
        w1.location AS hub,
        EXTRACT(EPOCH FROM (w2.event_time - w1.event_time)) / 3600.0 AS dwell_hours
    FROM waybill_events w1
    JOIN waybill_events w2
        ON w1.shipment_id = w2.shipment_id
       AND w2.event_time = (
           SELECT MIN(w3.event_time)
           FROM waybill_events w3
           WHERE w3.shipment_id = w1.shipment_id
             AND w3.event_time > w1.event_time
       )
    WHERE w1.status = 'ARRIVED_HUB'
)
SELECT
    hub,
    ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY dwell_hours), 1) AS p90_dwell_hours,
    ROUND(AVG(dwell_hours), 1) AS avg_dwell_hours,
    COUNT(*) AS measurements
FROM hub_dwell
GROUP BY hub
ORDER BY p90_dwell_hours DESC;
```

**Explanation:** P90 dwell time at each hub captures the worst-case experience for 90% of shipments.

---

## Q63: Cross-dock throughput — shipments transferred same day vs next day

**Schema:** `waybill_events(event_id, shipment_id, location, status, event_time)`

```sql
-- SQL Server
WITH cross_dock AS (
    SELECT
        e1.shipment_id,
        e1.location,
        e1.event_time AS arrived,
        e2.event_time AS departed,
        DATEDIFF(HOUR, e1.event_time, e2.event_time) AS hours_in_facility
    FROM waybill_events e1
    JOIN waybill_events e2
        ON e1.shipment_id = e2.shipment_id
       AND e2.event_time > e1.event_time
    WHERE e1.status = 'ARRIVED_WAREHOUSE'
      AND e2.status = 'DEPARTED_WAREHOUSE'
)
SELECT
    location,
    SUM(CASE WHEN hours_in_facility <= 24 THEN 1 ELSE 0 END) AS same_day_crossdock,
    SUM(CASE WHEN hours_in_facility > 24  THEN 1 ELSE 0 END) AS next_day_plus,
    COUNT(*) AS total,
    ROUND(100.0 * SUM(CASE WHEN hours_in_facility <= 24 THEN 1 ELSE 0 END) / COUNT(*), 1) AS same_day_pct
FROM cross_dock
GROUP BY location
ORDER BY same_day_pct DESC;
```

**Explanation:** Splitting dwell time at 24 hours separates same-day cross-docks from delayed transfers.

---

## Q64: Batch vs streaming approach — last 10 minutes of events

**Schema:** `waybill_events(event_id, shipment_id, truck_id, event_time, status)`

```sql
-- PostgreSQL (batch snapshot)
SELECT
    shipment_id,
    truck_id,
    status,
    event_time
FROM waybill_events
WHERE event_time >= NOW() - INTERVAL '10 minutes'
ORDER BY event_time DESC;
```

**Explanation:** This batch query pulls recent events for a dashboard refresh.

**Alt1 (streaming):** In a streaming architecture, use a windowed aggregation on a Kafka topic:
```sql
-- Materialize as a streaming view via Flink/ksqlDB
SELECT shipment_id, truck_id, status, TUMBLE_START(event_time, INTERVAL '1 MINUTE') AS window_start, COUNT(*) AS events_per_min
FROM waybill_events_stream
GROUP BY shipment_id, truck_id, status, TUMBLE(event_time, INTERVAL '1 MINUTE');
```
Streaming avoids repeated full-table scans and provides sub-second freshness.

---

## Q65: Supply-demand gap — shipments created vs delivered per day

**Schema:** `shipments(shipment_id, created_at, delivered_at)`

```sql
-- MySQL 8+
WITH created AS (
    SELECT DATE(created_at) AS d, COUNT(*) AS created_cnt
    FROM shipments GROUP BY DATE(created_at)
),
delivered AS (
    SELECT DATE(delivered_at) AS d, COUNT(*) AS delivered_cnt
    FROM shipments WHERE delivered_at IS NOT NULL GROUP BY DATE(delivered_at)
)
SELECT
    COALESCE(c.d, dl.d) AS ship_date,
    COALESCE(c.created_cnt, 0) AS created,
    COALESCE(dl.delivered_cnt, 0) AS delivered,
    COALESCE(c.created_cnt, 0) - COALESCE(dl.delivered_cnt, 0) AS backlog_delta
FROM created c
FULL OUTER JOIN delivered dl ON c.d = dl.d
ORDER BY ship_date;
```

**Explanation:** A FULL OUTER JOIN aligns creation and delivery counts; the delta reveals daily backlog growth or shrinkage.

---

## Q66: Loading dock congestion — simultaneous arrivals at warehouse

**Schema:** `waybill_events(event_id, shipment_id, location, status, event_time)`

```sql
-- PostgreSQL
WITH arrivals AS (
    SELECT
        location,
        event_time,
        shipment_id,
        EXTRACT(EPOCH FROM (event_time - LAG(event_time) OVER (
            PARTITION BY location ORDER BY event_time
        ))) / 60.0 AS minutes_since_prev
    FROM waybill_events
    WHERE status = 'ARRIVED_WAREHOUSE'
)
SELECT
    location,
    event_time,
    shipment_id,
    ROUND(minutes_since_prev, 1) AS gap_minutes,
    CASE WHEN minutes_since_prev < 5 THEN 'CONGESTED' ELSE 'NORMAL' END AS dock_status
FROM arrivals
WHERE minutes_since_prev IS NOT NULL
ORDER BY location, event_time;
```

**Explanation:** When consecutive arrivals at a facility are < 5 minutes apart, the dock is likely congested.

---

## Q67: Carrier cost benchmarking — avg cost per lb by carrier

**Schema:** `shipments(shipment_id, carrier_id, weight, cost)`

```sql
-- SQL Server
SELECT
    carrier_id,
    COUNT(*) AS shipments,
    ROUND(SUM(cost) / NULLIF(SUM(weight), 0), 4) AS cost_per_lb,
    ROUND(AVG(cost), 2) AS avg_cost
FROM shipments
GROUP BY carrier_id
ORDER BY cost_per_lb;
```

**Explanation:** Normalizing by weight enables apples-to-apples carrier cost comparisons.

---

## Q68: Deadhead miles estimation — empty return trips

**Schema:** `trips(trip_id, truck_id, route_id, miles), routes(route_id, origin, destination), shipments(shipment_id, trip_id)`

```sql
-- Oracle
WITH trip_load AS (
    SELECT
        t.trip_id,
        t.truck_id,
        t.miles,
        COUNT(s.shipment_id) AS loaded_shipments
    FROM trips t
    LEFT JOIN shipments s ON s.trip_id = t.trip_id
    GROUP BY t.trip_id, t.truck_id, t.miles
)
SELECT
    truck_id,
    SUM(CASE WHEN loaded_shipments = 0 THEN miles ELSE 0 END) AS deadhead_miles,
    SUM(CASE WHEN loaded_shipments > 0 THEN miles ELSE 0 END) AS loaded_miles,
    ROUND(100.0 * SUM(CASE WHEN loaded_shipments = 0 THEN miles ELSE 0 END)
          / NULLIF(SUM(miles), 0), 1) AS deadhead_pct
FROM trip_load
GROUP BY truck_id
HAVING SUM(CASE WHEN loaded_shipments = 0 THEN miles ELSE 0 END) > 0
ORDER BY deadhead_pct DESC;
```

**Explanation:** Trips with zero shipments are deadheads; their miles as a percentage indicate fleet efficiency.

---

## Q69: SLA compliance by time-of-year — monthly on-time % trend

**Schema:** `shipments(shipment_id, created_at, delivered_at)`

```sql
-- MySQL 8+
SELECT
    DATE_FORMAT(created_at, '%Y-%m') AS month,
    COUNT(*) AS total,
    SUM(CASE WHEN DATEDIFF(delivered_at, created_at) <= 5 THEN 1 ELSE 0 END) AS on_time,
    ROUND(100.0 * SUM(CASE WHEN DATEDIFF(delivered_at, created_at) <= 5 THEN 1 ELSE 0 END) / COUNT(*), 1) AS on_time_pct,
    CASE
        WHEN ROUND(100.0 * SUM(CASE WHEN DATEDIFF(delivered_at, created_at) <= 5 THEN 1 ELSE 0 END) / COUNT(*), 1) >= 95 THEN 'GREEN'
        WHEN ROUND(100.0 * SUM(CASE WHEN DATEDIFF(delivered_at, created_at) <= 5 THEN 1 ELSE 0 END) / COUNT(*), 1) >= 90 THEN 'YELLOW'
        ELSE 'RED'
    END AS sla_status
FROM shipments
WHERE delivered_at IS NOT NULL
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY month;
```

**Explanation:** Monthly SLA tracking with RAG status highlights seasonal dips in delivery performance.

---

## Q70: Route frequency heatmap data — origin × destination × month

**Schema:** `shipments(shipment_id, origin, destination, created_at)`

```sql
-- PostgreSQL
SELECT
    origin,
    destination,
    TO_CHAR(created_at, 'YYYY-MM') AS month,
    COUNT(*) AS volume
FROM shipments
GROUP BY origin, destination, TO_CHAR(created_at, 'YYYY-MM')
ORDER BY origin, destination, month;
```

**Explanation:** This output is suitable for pivoting into a heatmap visualization in BI tools.

---

## Q71: In-transit risk — shipments with no event in last 48 hours

**Schema:** `shipments(shipment_id, status), waybill_events(event_id, shipment_id, event_time)`

```sql
-- SQL Server
WITH last_event AS (
    SELECT
        shipment_id,
        MAX(event_time) AS last_event_time
    FROM waybill_events
    GROUP BY shipment_id
)
SELECT
    s.shipment_id,
    s.status,
    le.last_event_time,
    DATEDIFF(HOUR, le.last_event_time, GETDATE()) AS hours_silent
FROM shipments s
JOIN last_event le ON le.shipment_id = s.shipment_id
WHERE s.status = 'IN_TRANSIT'
  AND DATEDIFF(HOUR, le.last_event_time, GETDATE()) > 48
ORDER BY hours_silent DESC;
```

**Explanation:** In-transit shipments with no telemetry in 48 hours may be lost or stuck.

---

## Q72: Milestone completion rate per shipment cohort (weekly creation cohort)

**Schema:** `waybill_events(event_id, shipment_id, status, event_time), shipments(shipment_id, created_at)`

```sql
-- MySQL 8+
WITH cohort AS (
    SELECT
        s.shipment_id,
        DATE_FORMAT(s.created_at, '%Y-%u') AS cohort_week,
        MAX(CASE WHEN w.status = 'PICKUP'       THEN 1 ELSE 0 END) AS reached_pickup,
        MAX(CASE WHEN w.status = 'IN_TRANSIT'    THEN 1 ELSE 0 END) AS reached_transit,
        MAX(CASE WHEN w.status = 'DELIVERED'     THEN 1 ELSE 0 END) AS reached_delivered
    FROM shipments s
    LEFT JOIN waybill_events w ON w.shipment_id = s.shipment_id
    GROUP BY s.shipment_id, DATE_FORMAT(s.created_at, '%Y-%u')
)
SELECT
    cohort_week,
    COUNT(*) AS shipments,
    ROUND(100.0 * AVG(reached_pickup), 1)    AS pct_pickup,
    ROUND(100.0 * AVG(reached_transit), 1)   AS pct_transit,
    ROUND(100.0 * AVG(reached_delivered), 1) AS pct_delivered
FROM cohort
GROUP BY cohort_week
ORDER BY cohort_week;
```

**Explanation:** Weekly cohorts show how quickly shipments progress through the funnel over time.

---

## Q73: Warehouse capacity utilization — shipments processed vs warehouse capacity

**Schema:** `waybill_events(event_id, shipment_id, location, event_time, status), warehouses(warehouse_id, name, capacity)`

```sql
-- PostgreSQL
WITH daily_processed AS (
    SELECT
        e.location,
        DATE(e.event_time) AS process_date,
        COUNT(DISTINCT e.shipment_id) AS processed
    FROM waybill_events e
    WHERE e.status IN ('ARRIVED_WAREHOUSE', 'DEPARTED_WAREHOUSE')
    GROUP BY e.location, DATE(e.event_time)
)
SELECT
    dp.location,
    dp.process_date,
    dp.processed,
    w.capacity,
    ROUND(100.0 * dp.processed / NULLIF(w.capacity, 0), 1) AS utilization_pct
FROM daily_processed dp
JOIN warehouses w ON w.name = dp.location
ORDER BY utilization_pct DESC;
```

**Explanation:** Dividing daily throughput by rated warehouse capacity exposes over-utilization.

---

## Q74: Exception correlation — do exceptions predict late delivery?

**Schema:** `exceptions(exception_id, shipment_id, reason_code), shipments(shipment_id, created_at, delivered_at)`

```sql
-- MySQL 8+
WITH shipment_exception AS (
    SELECT
        s.shipment_id,
        COUNT(e.exception_id) AS exception_count,
        CASE WHEN DATEDIFF(s.delivered_at, s.created_at) > 5 THEN 1 ELSE 0 END AS is_late
    FROM shipments s
    LEFT JOIN exceptions e ON e.shipment_id = s.shipment_id
    WHERE s.delivered_at IS NOT NULL
    GROUP BY s.shipment_id,
             CASE WHEN DATEDIFF(s.delivered_at, s.created_at) > 5 THEN 1 ELSE 0 END
)
SELECT
    exception_count,
    COUNT(*) AS shipments,
    ROUND(100.0 * AVG(is_late), 1) AS late_rate_pct
FROM shipment_exception
GROUP BY exception_count
ORDER BY exception_count;
```

**Explanation:** Grouping by exception count and computing late rate reveals the correlation.

---

## Q75: Geospatial nearest-neighbor — find closest warehouse to each delivery destination

**Schema:** `shipments(shipment_id, destination, delivered_at), warehouses(warehouse_id, name, lat, lng)`

```sql
-- PostgreSQL with PostGIS
SELECT DISTINCT
    s.shipment_id,
    s.destination,
    w.name AS nearest_warehouse,
    ST_Distance(
        ST_MakePoint(s.dest_lng, s.dest_lat)::geography,
        ST_MakePoint(w.lng, w.lat)::geography
    ) / 1609.34 AS distance_miles
FROM shipments s
CROSS JOIN LATERAL (
    SELECT w2.name, w2.lat, w2.lng
    FROM warehouses w2
    ORDER BY ST_MakePoint(s.dest_lng, s.dest_lat)::geography <-> ST_MakePoint(w2.lng, w2.lat)::geography
    LIMIT 1
) w
LIMIT 20;
```

**Explanation:** `CROSS JOIN LATERAL` with nearest-neighbor ordering via PostGIS `<->` operator finds the closest warehouse per destination.

---

## Q76: Batch vs streaming — anomaly alert on rapid status flips

**Schema:** `waybill_events(event_id, shipment_id, status, event_time)`

```sql
-- PostgreSQL (batch)
WITH flips AS (
    SELECT
        shipment_id,
        status,
        event_time,
        LAG(status) OVER (PARTITION BY shipment_id ORDER BY event_time) AS prev_status,
        EXTRACT(EPOCH FROM (
            event_time - LAG(event_time) OVER (PARTITION BY shipment_id ORDER BY event_time)
        )) / 60.0 AS minutes_since_prev
    FROM waybill_events
)
SELECT shipment_id, prev_status, status, event_time, ROUND(minutes_since_prev, 1) AS gap_minutes
FROM flips
WHERE prev_status IS NOT NULL
  AND minutes_since_prev < 1
ORDER BY event_time DESC;
```

**Explanation:** Status flips within 1 minute likely indicate a sensor or data-entry error.

**Alt1 (streaming):** Use a sliding window on a stream to emit alerts:
```sql
-- Flink SQL / ksqlDB
SELECT shipment_id, status, prev_status, event_time
FROM (
    SELECT *, LAG(status) OVER (PARTITION BY shipment_id ORDER BY event_time) AS prev_status,
             LAG(event_time) OVER (PARTITION BY shipment_id ORDER BY event_time) AS prev_time
    FROM waybill_events_stream
)
WHERE event_time - prev_time < INTERVAL '1 MINUTE' AND status <> prev_status;
```

---

## Q77: Throughput bottleneck analysis — max concurrent shipments at each hub

**Schema:** `waybill_events(event_id, shipment_id, location, status, event_time)`

```sql
-- MySQL 8+
WITH events AS (
    SELECT shipment_id, location, event_time, 1 AS delta,
           CASE WHEN status = 'ARRIVED_WAREHOUSE' THEN 'IN' ELSE 'OUT' END AS direction
    FROM waybill_events
    WHERE status IN ('ARRIVED_WAREHOUSE', 'DEPARTED_WAREHOUSE')
),
running AS (
    SELECT
        location,
        event_time,
        SUM(CASE WHEN direction = 'IN' THEN delta ELSE -delta END)
            OVER (PARTITION BY location ORDER BY event_time
                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
    FROM events
)
SELECT location, MAX(concurrent) AS peak_concurrent
FROM running
GROUP BY location
ORDER BY peak_concurrent DESC;
```

**Explanation:** A running sum of arrivals minus departures tracks concurrent occupancy; the peak is the bottleneck.

---

## Q78: Carrier SLA penalty calculation

**Schema:** `shipments(shipment_id, carrier_id, cost, created_at, delivered_at)`

```sql
-- Oracle
WITH breach AS (
    SELECT
        carrier_id,
        shipment_id,
        cost,
        EXTRACT(DAY FROM delivered_at - created_at) AS days,
        CASE
            WHEN EXTRACT(DAY FROM delivered_at - created_at) BETWEEN 4 AND 7 THEN 0.05
            WHEN EXTRACT(DAY FROM delivered_at - created_at) BETWEEN 8 AND 14 THEN 0.10
            WHEN EXTRACT(DAY FROM delivered_at - created_at) > 14 THEN 0.20
            ELSE 0
        END AS penalty_rate
    FROM shipments
    WHERE delivered_at IS NOT NULL
)
SELECT
    carrier_id,
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN penalty_rate > 0 THEN 1 ELSE 0 END) AS penalized,
    ROUND(SUM(cost * penalty_rate), 2) AS total_penalty
FROM breach
GROUP BY carrier_id
ORDER BY total_penalty DESC;
```

**Explanation:** Tiered penalty rates based on overdue days quantify carrier SLA breach costs.

---

## Q79: Inventory depletion prediction — days until stockout per SKU

**Schema:** `inventory(sku, warehouse_id, qty_on_hand, last_restock_at), shipments(shipment_id, destination, delivered_at)`

```sql
-- MySQL 8+
WITH demand_rate AS (
    SELECT
        i.sku,
        i.warehouse_id,
        i.qty_on_hand,
        COUNT(s.shipment_id) /
            NULLIF(DATEDIFF(DAY, MIN(s.delivered_at), MAX(s.delivered_at)), 0) AS daily_demand
    FROM inventory i
    LEFT JOIN shipments s ON s.destination = i.warehouse_id
    WHERE s.delivered_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY i.sku, i.warehouse_id, i.qty_on_hand
)
SELECT
    sku,
    warehouse_id,
    qty_on_hand,
    ROUND(daily_demand, 2) AS daily_demand,
    ROUND(qty_on_hand / NULLIF(daily_demand, 0), 0) AS days_until_stockout
FROM demand_rate
WHERE daily_demand > 0
ORDER BY days_until_stockout ASC;
```

**Explanation:** Dividing on-hand quantity by recent daily demand yields projected days until stockout.

---

## Q80: Shipment aging buckets for open orders

**Schema:** `shipments(shipment_id, status, created_at)`

```sql
-- SQL Server
SELECT
    CASE
        WHEN DATEDIFF(day, created_at, GETDATE()) <= 2  THEN '0-2 days'
        WHEN DATEDIFF(day, created_at, GETDATE()) <= 5  THEN '3-5 days'
        WHEN DATEDIFF(day, created_at, GETDATE()) <= 10 THEN '6-10 days'
        WHEN DATEDIFF(day, created_at, GETDATE()) <= 20 THEN '11-20 days'
        ELSE '20+ days'
    END AS age_bucket,
    COUNT(*) AS open_shipments
FROM shipments
WHERE delivered_at IS NULL AND status <> 'CANCELLED'
GROUP BY CASE
        WHEN DATEDIFF(day, created_at, GETDATE()) <= 2  THEN '0-2 days'
        WHEN DATEDIFF(day, created_at, GETDATE()) <= 5  THEN '3-5 days'
        WHEN DATEDIFF(day, created_at, GETDATE()) <= 10 THEN '6-10 days'
        WHEN DATEDIFF(day, created_at, GETDATE()) <= 20 THEN '11-20 days'
        ELSE '20+ days'
    END
ORDER BY MIN(DATEDIFF(day, created_at, GETDATE()));
```

**Explanation:** Aging buckets on open orders provide a snapshot of backlog health.

---

## Q81: Multi-leg shipment timeline — Gantt-style view per shipment

**Schema:** `waybill_events(event_id, shipment_id, status, event_time, location)`

```sql
-- PostgreSQL
SELECT
    shipment_id,
    status,
    location,
    event_time,
    LEAD(event_time) OVER (PARTITION BY shipment_id ORDER BY event_time) AS next_event_time,
    EXTRACT(EPOCH FROM (
        LEAD(event_time) OVER (PARTITION BY shipment_id ORDER BY event_time) - event_time
    )) / 3600.0 AS leg_duration_hours
FROM waybill_events
ORDER BY shipment_id, event_time;
```

**Explanation:** Each row becomes a segment in a Gantt chart with its duration in hours.

---

## Q82: Overweight trip detection — total load exceeding capacity by percentage

**Schema:** `trucks(truck_id, capacity), shipments(shipment_id, trip_id, weight), trips(trip_id, truck_id)`

```sql
-- PostgreSQL
WITH load AS (
    SELECT
        t.trip_id,
        t.truck_id,
        SUM(s.weight) AS total_weight,
        tk.capacity
    FROM trips t
    JOIN shipments s ON s.trip_id = t.trip_id
    JOIN trucks tk   ON tk.truck_id = t.truck_id
    GROUP BY t.trip_id, t.truck_id, tk.capacity
)
SELECT
    trip_id,
    truck_id,
    total_weight,
    capacity,
    ROUND(100.0 * (total_weight - capacity) / NULLIF(capacity, 0), 1) AS overload_pct
FROM load
WHERE total_weight > capacity
ORDER BY overload_pct DESC;
```

**Explanation:** The percentage overload quantifies how far each trip exceeds the rated capacity.

---

## Q83: Shipment milestone duration trend — rolling average dwell at each stage

**Schema:** `waybill_events(event_id, shipment_id, status, event_time)`

```sql
-- MySQL 8+
WITH dwell AS (
    SELECT
        shipment_id,
        LAG(status) OVER (PARTITION BY shipment_id ORDER BY event_time) AS from_status,
        status AS to_status,
        TIMESTAMPDIFF(HOUR,
            LAG(event_time) OVER (PARTITION BY shipment_id ORDER BY event_time),
            event_time
        ) AS hours
    FROM waybill_events
)
SELECT
    CONCAT(from_status, ' → ', to_status) AS transition,
    COUNT(*) AS occurrences,
    ROUND(AVG(hours), 1) AS avg_hours,
    ROUND(AVG(hours) OVER (ORDER BY COUNT(*) DESC ROWS BETWEEN 4 PRECEDING AND CURRENT ROW), 1) AS rolling_avg
FROM dwell
WHERE from_status IS NOT NULL AND hours IS NOT NULL
GROUP BY from_status, to_status
ORDER BY occurrences DESC;
```

**Explanation:** Transition-level dwell time with a rolling average detects gradual slowdowns in specific stages.

---

## Q84: Revenue per mile by route — profitability ranking

**Schema:** `shipments(shipment_id, origin, destination, cost), routes(route_id, origin, destination, distance_miles)`

```sql
-- SQL Server
SELECT
    r.origin,
    r.destination,
    r.distance_miles,
    COUNT(s.shipment_id) AS shipments,
    SUM(s.cost) AS total_revenue,
    ROUND(SUM(s.cost) / NULLIF(r.distance_miles, 0), 2) AS revenue_per_mile
FROM routes r
JOIN shipments s ON s.origin = r.origin AND s.destination = r.destination
GROUP BY r.origin, r.destination, r.distance_miles
HAVING COUNT(s.shipment_id) >= 10
ORDER BY revenue_per_mile DESC;
```

**Explanation:** Revenue per mile per route identifies the most profitable corridors.

---

## Q85: Warehouse restock event chain — time between depletion and replenishment

**Schema:** `inventory(sku, warehouse_id, qty_on_hand, reorder_point, last_restock_at), waybill_events(event_id, shipment_id, location, status, event_time)`

```sql
-- Oracle
WITH depletion_events AS (
    SELECT
        w.shipment_id,
        w.location,
        w.event_time AS departed_at,
        LEAD(w.event_time) OVER (PARTITION BY w.location ORDER BY w.event_time) AS next_event
    FROM waybill_events w
    WHERE w.status = 'DEPARTED_WAREHOUSE'
),
restock AS (
    SELECT
        w.location,
        w.event_time AS restocked_at
    FROM waybill_events w
    WHERE w.status = 'ARRIVED_WAREHOUSE'
)
SELECT
    d.location,
    d.departed_at,
    r.restocked_at,
    ROUND(EXTRACT(HOUR FROM r.restocked_at - d.departed_at), 1) AS restock_lag_hours
FROM depletion_events d
JOIN restock r ON r.location = d.location AND r.restocked_at > d.departed_at
WHERE r.restocked_at = (
    SELECT MIN(r2.restocked_at)
    FROM restock r2
    WHERE r2.location = d.location AND r2.restocked_at > d.departed_at
)
ORDER BY restock_lag_hours DESC
FETCH FIRST 20 ROWS ONLY;
```

**Explanation:** For each outbound event, the next inbound arrival at the same warehouse is the restock; the gap is the replenishment lag.

---

## Q86: Corridor congestion index — shipments per day per lane vs historical average

**Schema:** `shipments(shipment_id, origin, destination, created_at)`

```sql
-- MySQL 8+
WITH daily AS (
    SELECT
        origin,
        destination,
        DATE(created_at) AS ship_date,
        COUNT(*) AS daily_count
    FROM shipments
    GROUP BY origin, destination, DATE(created_at)
),
historical AS (
    SELECT
        origin,
        destination,
        AVG(daily_count) AS hist_avg,
        STDDEV(daily_count) AS hist_stddev
    FROM daily
    GROUP BY origin, destination
)
SELECT
    d.origin,
    d.destination,
    d.ship_date,
    d.daily_count,
    ROUND(h.hist_avg, 1) AS avg_daily,
    ROUND((d.daily_count - h.hist_avg) / NULLIF(h.hist_stddev, 0), 2) AS z_score
FROM daily d
JOIN historical h ON h.origin = d.origin AND h.destination = d.destination
WHERE (d.daily_count - h.hist_avg) / NULLIF(h.hist_stddev, 0) > 1.5
ORDER BY z_score DESC;
```

**Explanation:** A z-score > 1.5 flags days with unusually high lane volume (congestion).

---

## Q87: Return freight rate — percentage of trucks returning empty by depot

**Schema:** `trucks(truck_id, home_depot), trips(trip_id, truck_id, route_id, departure_at), routes(route_id, origin, destination)`

```sql
-- PostgreSQL
WITH outbound AS (
    SELECT
        t.truck_id,
        tk.home_depot,
        t.trip_id,
        r.destination
    FROM trips t
    JOIN trucks tk ON tk.truck_id = t.truck_id
    JOIN routes r  ON r.route_id  = t.route_id
    WHERE r.origin = tk.home_depot
),
has_return AS (
    SELECT
        o.truck_id,
        o.home_depot,
        o.trip_id,
        CASE WHEN EXISTS (
            SELECT 1 FROM trips t2
            JOIN routes r2 ON r2.route_id = t2.route_id
            WHERE t2.truck_id = o.truck_id
              AND r2.origin = o.destination
              AND r2.destination = o.home_depot
        ) THEN 1 ELSE 0 END AS has_return_trip
    FROM outbound o
)
SELECT
    home_depot,
    COUNT(*) AS outbound_trips,
    SUM(has_return) AS loaded_returns,
    COUNT(*) - SUM(has_return) AS empty_returns,
    ROUND(100.0 * (COUNT(*) - SUM(has_return)) / COUNT(*), 1) AS empty_return_pct
FROM has_return
GROUP BY home_depot
ORDER BY empty_return_pct DESC;
```

**Explanation:** Checking for a reverse trip on the same lane determines if the return was loaded or empty.

---

## Q88: Truck age vs failure correlation (if maintenance_events table exists)

**Schema:** `trucks(truck_id, year Manufactured), maintenance_events(event_id, truck_id, event_date, event_type)`

```sql
-- MySQL 8+
SELECT
    YEAR(CURRENT_DATE()) - tk.year_manufactured AS truck_age_years,
    COUNT(DISTINCT tk.truck_id) AS trucks,
    COUNT(me.event_id) AS maintenance_events,
    ROUND(COUNT(me.event_id) / NULLIF(COUNT(DISTINCT tk.truck_id), 0), 2) AS events_per_truck
FROM trucks tk
LEFT JOIN maintenance_events me ON me.truck_id = tk.truck_id
GROUP BY YEAR(CURRENT_DATE()) - tk.year_manufactured
ORDER BY truck_age_years;
```

**Explanation:** A rising events-per-truck ratio with age confirms age-related failure patterns.

---

## Q89: Shipment consolidation opportunity — weight-based truck fill rate

**Schema:** `trucks(truck_id, capacity), shipments(shipment_id, trip_id, weight), trips(trip_id, truck_id)`

```sql
-- SQL Server
WITH trip_load AS (
    SELECT
        t.trip_id,
        t.truck_id,
        SUM(s.weight) AS load_weight,
        tk.capacity,
        ROUND(100.0 * SUM(s.weight) / NULLIF(tk.capacity, 0), 1) AS fill_pct
    FROM trips t
    JOIN shipments s ON s.trip_id = t.trip_id
    JOIN trucks tk   ON tk.truck_id = t.truck_id
    GROUP BY t.trip_id, t.truck_id, tk.capacity
)
SELECT
    CASE
        WHEN fill_pct < 25 THEN 'UNDER_UTILIZED (<25%)'
        WHEN fill_pct < 50 THEN 'LOW (25-50%)'
        WHEN fill_pct < 75 THEN 'MODERATE (50-75%)'
        ELSE 'HIGH (75%+)'
    END AS fill_bucket,
    COUNT(*) AS trips,
    ROUND(AVG(fill_pct), 1) AS avg_fill_pct
FROM trip_load
GROUP BY CASE
        WHEN fill_pct < 25 THEN 'UNDER_UTILIZED (<25%)'
        WHEN fill_pct < 50 THEN 'LOW (25-50%)'
        WHEN fill_pct < 75 THEN 'MODERATE (50-75%)'
        ELSE 'HIGH (75%+)'
    END
ORDER BY avg_fill_pct;
```

**Explanation:** Fill-rate bucketing reveals how much spare capacity exists across the fleet.

---

## Q90: Delay propagation — how one late shipment affects others on the same truck

**Schema:** `shipments(shipment_id, trip_id, created_at, delivered_at), trips(trip_id, truck_id)`

```sql
-- PostgreSQL
WITH trip_stats AS (
    SELECT
        t.trip_id,
        t.truck_id,
        MAX(CASE WHEN s.delivered_at - s.created_at > INTERVAL '5 days' THEN 1 ELSE 0 END) AS has_late,
        COUNT(s.shipment_id) AS total_on_trip,
        SUM(CASE WHEN s.delivered_at - s.created_at > INTERVAL '5 days' THEN 1 ELSE 0 END) AS late_on_trip
    FROM trips t
    JOIN shipments s ON s.trip_id = t.trip_id
    WHERE s.delivered_at IS NOT NULL
    GROUP BY t.trip_id, t.truck_id
)
SELECT
    has_late,
    COUNT(*) AS trips,
    ROUND(AVG(total_on_trip), 1) AS avg_shipments_per_trip,
    ROUND(AVG(late_on_trip), 1) AS avg_late_per_trip
FROM trip_stats
GROUP BY has_late;
```

**Explanation:** Comparing trip-level metrics for trips with vs without late shipments quantifies propagation.

---

## Q91: Holiday impact analysis — delivery performance around holidays

**Schema:** `shipments(shipment_id, created_at, delivered_at), holidays(holiday_date, holiday_name)`

```sql
-- MySQL 8+
WITH tagged AS (
    SELECT
        s.shipment_id,
        s.created_at,
        s.delivered_at,
        h.holiday_name,
        DATEDIFF(s.delivered_at, s.created_at) AS delivery_days,
        CASE
            WHEN EXISTS (
                SELECT 1 FROM holidays h
                WHERE h.holiday_date BETWEEN s.created_at AND COALESCE(s.delivered_at, CURRENT_DATE())
            ) THEN 'INCLUDES_HOLIDAY'
            ELSE 'NO_HOLIDAY'
        END AS holiday_flag
    FROM shipments s
)
SELECT
    holiday_flag,
    COUNT(*) AS shipments,
    ROUND(AVG(delivery_days), 1) AS avg_delivery_days
FROM tagged
WHERE delivered_at IS NOT NULL
GROUP BY holiday_flag;
```

**Explanation:** Splitting delivery metrics by holiday overlap quantifies the holiday effect on transit times.

---

## Q92: Fuel cost as % of shipment revenue

**Schema:** `fuel_logs(trip_id, gallons, cost_per_gallon), trips(trip_id), shipments(shipment_id, trip_id, cost)`

```sql
-- Oracle
WITH trip_fuel AS (
    SELECT
        f.trip_id,
        SUM(f.gallons * f.cost_per_gallon) AS fuel_cost
    FROM fuel_logs f
    GROUP BY f.trip_id
),
trip_revenue AS (
    SELECT
        trip_id,
        SUM(cost) AS revenue
    FROM shipments
    GROUP BY trip_id
)
SELECT
    tf.trip_id,
    tf.fuel_cost,
    tr.revenue,
    ROUND(100.0 * tf.fuel_cost / NULLIF(tr.revenue, 0), 1) AS fuel_pct_of_revenue
FROM trip_fuel tf
JOIN trip_revenue tr ON tr.trip_id = tf.trip_id
WHERE tr.revenue > 0
ORDER BY fuel_pct_of_revenue DESC;
```

**Explanation:** Fuel cost as a percentage of revenue highlights routes where fuel erodes profitability.

---

## Q93: Duplicate shipment detection — same origin, destination, weight within 1 hour

**Schema:** `shipments(shipment_id, origin, destination, weight, created_at)`

```sql
-- MySQL 8+
SELECT
    a.shipment_id AS shipment_1,
    b.shipment_id AS shipment_2,
    a.origin,
    a.destination,
    a.weight,
    TIMESTAMPDIFF(MINUTE, a.created_at, b.created_at) AS minutes_apart
FROM shipments a
JOIN shipments b
    ON a.origin = b.origin
   AND a.destination = b.destination
   AND ABS(a.weight - b.weight) < 0.1
   AND ABS(TIMESTAMPDIFF(MINUTE, a.created_at, b.created_at)) <= 60
   AND a.shipment_id < b.shipment_id
ORDER BY minutes_apart;
```

**Explanation:** Same lane, similar weight, and within 60 minutes strongly suggests duplicate entries.

---

## Q94: Shipment priority scoring — composite weighted score

**Schema:** `shipments(shipment_id, weight, cost, created_at, delivered_at, status)`

```sql
-- PostgreSQL
SELECT
    shipment_id,
    ROUND(
        0.3 * NTILE(10) OVER (ORDER BY weight DESC)::numeric / 10.0 +
        0.4 * NTILE(10) OVER (ORDER BY cost DESC)::numeric  / 10.0 +
        0.3 * NTILE(10) OVER (ORDER BY created_at ASC)::numeric  / 10.0,
    2) AS priority_score
FROM shipments
WHERE status NOT IN ('DELIVERED', 'CANCELLED')
ORDER BY priority_score DESC;
```

**Explanation:** NTILE binning normalizes disparate metrics to 0-1; weighted sum produces a composite priority.

---

## Q95: Lane utilization heatmap — trips per week per lane

**Schema:** `trips(trip_id, route_id, departure_at), routes(route_id, origin, destination)`

```sql
-- SQL Server
SELECT
    r.origin,
    r.destination,
    FORMAT(t.departure_at, 'yyyy-MM') AS month,
    COUNT(*) AS trips
FROM trips t
JOIN routes r ON r.route_id = t.route_id
GROUP BY r.origin, r.destination, FORMAT(t.departure_at, 'yyyy-MM')
ORDER BY r.origin, r.destination, month;
```

**Explanation:** Monthly trip counts per lane produce data for a utilization heatmap.

---

## Q96: Batch vs streaming — windowed aggregation for live throughput metric

**Schema:** `shipments(shipment_id, created_at)`

```sql
-- MySQL 8+ (batch)
SELECT
    DATE(created_at) AS ship_date,
    HOUR(created_at) AS hour,
    COUNT(*) AS shipments_per_hour
FROM shipments
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(created_at), HOUR(created_at)
ORDER BY ship_date, hour;
```

**Explanation:** This batch query computes hourly throughput for the past week.

**Alt1 (streaming):**
```sql
-- Flink SQL tumbling window
SELECT
    TUMBLE_START(event_time, INTERVAL '1 HOUR') AS window_start,
    COUNT(*) AS shipments_per_hour
FROM shipments_stream
WHERE event_time > CURRENT_TIMESTAMP - INTERVAL '7 DAY'
GROUP BY TUMBLE(event_time, INTERVAL '1 HOUR');
```
Streaming windows update in real-time without rescanning historical data.

---

## Q97: Time between order and first movement — warehouse processing time

**Schema:** `shipments(shipment_id, created_at), waybill_events(event_id, shipment_id, status, event_time)`

```sql
-- PostgreSQL
SELECT
    s.shipment_id,
    s.created_at,
    MIN(w.event_time) AS first_movement,
    EXTRACT(EPOCH FROM (MIN(w.event_time) - s.created_at)) / 3600.0 AS processing_hours
FROM shipments s
JOIN waybill_events w ON w.shipment_id = s.shipment_id
WHERE w.status = 'PICKUP'
GROUP BY s.shipment_id, s.created_at
ORDER BY processing_hours DESC;
```

**Explanation:** The gap between order creation and first pickup event is warehouse processing time.

---

## Q98: Fleet availability matrix — truck status by day

**Schema:** `trucks(truck_id), trips(trip_id, truck_id, departure_at, arrival_at)`

```sql
-- MySQL 8+
WITH calendar AS (
    SELECT DATE(d) AS day
    FROM (
        SELECT DATE_SUB(CURRENT_DATE(), INTERVAL n DAY) AS d
        FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3
              UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) nums
    ) dates
),
truck_days AS (
    SELECT
        tk.truck_id,
        c.day,
        CASE WHEN t.trip_id IS NOT NULL THEN 'IN_USE' ELSE 'AVAILABLE' END AS status
    FROM trucks tk
    CROSS JOIN calendar c
    LEFT JOIN trips t ON t.truck_id = tk.truck_id
        AND c.day BETWEEN DATE(t.departure_at) AND DATE(t.arrival_at)
)
SELECT
    day,
    SUM(CASE WHEN status = 'AVAILABLE' THEN 1 ELSE 0 END) AS available_trucks,
    SUM(CASE WHEN status = 'IN_USE' THEN 1 ELSE 0 END) AS in_use_trucks
FROM truck_days
GROUP BY day
ORDER BY day;
```

**Explanation:** Cross-joining trucks with a calendar and checking trip overlap produces a daily availability matrix.

---

## Q99: Exception resolution SLA — time to resolve by severity

**Schema:** `exceptions(exception_id, shipment_id, reason_code, severity, logged_at, resolved_at)`

```sql
-- Oracle
SELECT
    severity,
    reason_code,
    COUNT(*) AS exceptions,
    ROUND(AVG(EXTRACT(HOUR FROM resolved_at - logged_at)), 1) AS avg_resolution_hours,
    ROUND(MAX(EXTRACT(HOUR FROM resolved_at - logged_at)), 1) AS max_resolution_hours,
    SUM(CASE WHEN EXTRACT(HOUR FROM resolved_at - logged_at) > 24 THEN 1 ELSE 0 END) AS unresolved_over_24h
FROM exceptions
WHERE resolved_at IS NOT NULL
GROUP BY severity, reason_code
ORDER BY severity, avg_resolution_hours DESC;
```

**Explanation:** Resolution time by severity and reason code identifies which exception types need faster response processes.

---

## Q100: Capstone — ETA recomputation pipeline from waybill events with running delay

**Schema:** `waybill_events(event_id, shipment_id, status, event_time, location), shipments(shipment_id, origin, destination, created_at, delivered_at), routes(origin, destination, distance_miles)`

```sql
-- PostgreSQL
WITH milestone_pivot AS (
    SELECT
        w.shipment_id,
        MIN(CASE WHEN w.status = 'PICKUP'            THEN w.event_time END) AS pickup_at,
        MIN(CASE WHEN w.status = 'IN_TRANSIT'         THEN w.event_time END) AS transit_at,
        MIN(CASE WHEN w.status = 'ARRIVED_HUB'        THEN w.event_time END) AS hub_at,
        MIN(CASE WHEN w.status = 'OUT_FOR_DELIVERY'   THEN w.event_time END) AS ofd_at,
        MIN(CASE WHEN w.status = 'DELIVERED'          THEN w.event_time END) AS delivered_at_actual
    FROM waybill_events w
    GROUP BY w.shipment_id
),
historical_benchmarks AS (
    SELECT
        s.origin,
        s.destination,
        AVG(EXTRACT(EPOCH FROM (s.delivered_at - s.created_at)) / 86400.0) AS avg_total_days,
        PERCENTILE_CONT(0.5) WITHIN GROUP (
            ORDER BY EXTRACT(EPOCH FROM (s.delivered_at - s.created_at)) / 86400.0
        ) AS median_total_days,
        PERCENTILE_CONT(0.9) WITHIN GROUP (
            ORDER BY EXTRACT(EPOCH FROM (s.delivered_at - s.created_at)) / 86400.0
        ) AS p90_total_days
    FROM shipments s
    WHERE s.delivered_at IS NOT NULL
    GROUP BY s.origin, s.destination
),
segment_benchmarks AS (
    SELECT
        s.origin,
        s.destination,
        AVG(EXTRACT(EPOCH FROM (mp.hub_at - mp.pickup_at)) / 86400.0)    AS avg_pickup_to_hub,
        AVG(EXTRACT(EPOCH FROM (mp.ofd_at - mp.hub_at)) / 86400.0)       AS avg_hub_to_ofd,
        AVG(EXTRACT(EPOCH FROM (mp.delivered_at_actual - mp.ofd_at)) / 86400.0) AS avg_ofd_to_delivered
    FROM shipments s
    JOIN milestone_pivot mp ON mp.shipment_id = s.shipment_id
    WHERE mp.delivered_at_actual IS NOT NULL
    GROUP BY s.origin, s.destination
),
active_shipments AS (
    SELECT
        s.shipment_id,
        s.origin,
        s.destination,
        s.created_at,
        mp.pickup_at,
        mp.transit_at,
        mp.hub_at,
        mp.ofd_at,
        mp.delivered_at_actual,
        CASE
            WHEN mp.delivered_at_actual IS NOT NULL THEN 'DELIVERED'
            WHEN mp.ofd_at IS NOT NULL              THEN 'OUT_FOR_DELIVERY'
            WHEN mp.hub_at IS NOT NULL              THEN 'AT_HUB'
            WHEN mp.transit_at IS NOT NULL          THEN 'IN_TRANSIT'
            WHEN mp.pickup_at IS NOT NULL           THEN 'PICKED_UP'
            ELSE 'PENDING'
        END AS current_stage,
        CASE
            WHEN mp.delivered_at_actual IS NOT NULL THEN 0
            WHEN mp.ofd_at IS NOT NULL              THEN 1
            WHEN mp.hub_at IS NOT NULL              THEN 2
            WHEN mp.transit_at IS NOT NULL          THEN 3
            WHEN mp.pickup_at IS NOT NULL           THEN 4
            ELSE 5
        END AS stages_remaining
    FROM shipments s
    JOIN milestone_pivot mp ON mp.shipment_id = s.shipment_id
    WHERE s.delivered_at IS NULL
),
eta_calculation AS (
    SELECT
        a.shipment_id,
        a.origin,
        a.destination,
        a.current_stage,
        a.stages_remaining,
        a.created_at,
        sb.avg_pickup_to_hub,
        sb.avg_hub_to_ofd,
        sb.avg_ofd_to_delivered,
        hb.median_total_days,
        COALESCE(a.pickup_at, a.created_at) AS effective_start,
        CASE
            WHEN a.stages_remaining = 0 THEN a.delivered_at_actual
            WHEN a.stages_remaining = 1 THEN COALESCE(a.ofd_at, NOW()) + (sb.avg_ofd_to_delivered || ' days')::INTERVAL
            WHEN a.stages_remaining = 2 THEN COALESCE(a.hub_at, NOW()) + (sb.avg_hub_to_ofd + sb.avg_ofd_to_delivered) || ' days')::INTERVAL
            WHEN a.stages_remaining = 3 THEN COALESCE(a.transit_at, NOW()) + (sb.avg_pickup_to_hub + sb.avg_hub_to_ofd + sb.avg_ofd_to_delivered) || ' days')::INTERVAL
            ELSE COALESCE(a.created_at, NOW()) + (hb.median_total_days || ' days')::INTERVAL
        END AS estimated_delivery,
        CASE
            WHEN a.stages_remaining = 0 THEN 0
            ELSE EXTRACT(EPOCH FROM (
                CASE
                    WHEN a.stages_remaining = 1 THEN COALESCE(a.ofd_at, NOW()) + (sb.avg_ofd_to_delivered || ' days')::INTERVAL
                    WHEN a.stages_remaining = 2 THEN COALESCE(a.hub_at, NOW()) + ((sb.avg_hub_to_ofd + sb.avg_ofd_to_delivered) || ' days')::INTERVAL
                    WHEN a.stages_remaining = 3 THEN COALESCE(a.transit_at, NOW()) + ((sb.avg_pickup_to_hub + sb.avg_hub_to_ofd + sb.avg_ofd_to_delivered) || ' days')::INTERVAL
                    ELSE COALESCE(a.created_at, NOW()) + (hb.median_total_days || ' days')::INTERVAL
                END - NOW()
            )) / 86400.0
        END AS days_remaining,
        CASE
            WHEN a.stages_remaining > 0 AND
                 EXTRACT(EPOCH FROM (
                     NOW() - (COALESCE(a.created_at, NOW()) + (hb.median_total_days || ' days')::INTERVAL)
                 )) / 86400.0 > 0
            THEN EXTRACT(EPOCH FROM (
                     NOW() - (COALESCE(a.created_at, NOW()) + (hb.median_total_days || ' days')::INTERVAL)
                 )) / 86400.0
            ELSE 0
        END AS running_delay_days
    FROM active_shipments a
    JOIN historical_benchmarks hb ON hb.origin = a.origin AND hb.destination = a.destination
    JOIN segment_benchmarks sb    ON sb.origin = a.origin AND sb.destination = a.destination
)
SELECT
    shipment_id,
    origin,
    destination,
    current_stage,
    stages_remaining,
    TO_CHAR(estimated_delivery, 'YYYY-MM-DD HH24:MI') AS recomputed_eta,
    ROUND(days_remaining, 1)   AS days_until_delivery,
    ROUND(running_delay_days, 1) AS delay_days,
    CASE
        WHEN running_delay_days <= 0   THEN 'ON_TRACK'
        WHEN running_delay_days <= 1   THEN 'MINOR_DELAY'
        WHEN running_delay_days <= 3   THEN 'MODERATE_DELAY'
        ELSE 'CRITICAL_DELAY'
    END AS delay_status
FROM eta_calculation
ORDER BY running_delay_days DESC, estimated_delivery ASC;
```

**Explanation:** This capstone query: (1) pivots waybill events into milestone timestamps, (2) computes historical segment-level benchmarks, (3) identifies the current stage of each active shipment, (4) projects remaining time using segment averages from the current stage forward, and (5) calculates a running delay by comparing elapsed time against the historical median — producing a real-time ETA recomputation pipeline suitable for operations dashboards.

**Alt1:** For a streaming architecture, materialize the `milestone_pivot` as a Flink/ksqlDB aggregation over the `waybill_events_stream` topic, then join with a periodically-refreshed benchmark table. This avoids rescanning the full event log on every dashboard refresh and provides sub-second ETA updates as new events arrive.

---

*End of 100 interview scenarios.*
